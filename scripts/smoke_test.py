#!/usr/bin/env python3
"""Smoke test — run BEFORE any training run >10 min.

Verifies train/eval format match per condition. Catches the class of bug where
eval strips trajectory for a model trained on trajectory (or vice-versa).

Usage:
    cd <repo-root>
    python3 scripts/smoke_test.py
"""

import os
import pickle
import sys
import zipfile


def strip_trajectory_lines(text: str) -> str:
    lines = []
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('API-Request:') or s.startswith('API-Response:'):
            continue
        if 'Received API Response' in line or 'Generate API Request' in line:
            continue
        lines.append(line)
    return '\n'.join(lines).strip()


def build_generation_prompt(entry: dict, condition: str) -> str:
    """Mirror of notebook cell M_APiJSDY3eO. Keep in sync."""
    if condition == 'A':
        return strip_trajectory_lines(entry['input'])
    return entry['input']


def load_preprocessed():
    for path in ['preprocessed_data/preprocessed.pkl',
                 '../preprocessed_data/preprocessed.pkl']:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
    for path in ['artifacts/preprocessed_data.zip',
                 '../artifacts/preprocessed_data.zip']:
        if os.path.exists(path):
            with zipfile.ZipFile(path) as zf:
                with zf.open('preprocessed.pkl') as f:
                    return pickle.load(f)
    raise FileNotFoundError('preprocessed_data not found. Run from repo root.')


_USER_TAG = '<|start_header_id|>user<|end_header_id|>'
_ASSISTANT_TAG = '<|start_header_id|>assistant<|end_header_id|>'


def has_trajectory(text: str) -> bool:
    """True if trajectory lines appear in USER context (not assistant target)."""
    # Inspect only the user turn(s), up to the last assistant header.
    # For raw entry inputs (no chat template), just scan whole string.
    if _USER_TAG in text and _ASSISTANT_TAG in text:
        last_asst = text.rfind(_ASSISTANT_TAG)
        context = text[:last_asst]
    else:
        context = text
    return 'API-Request:' in context or 'API-Response:' in context


def find_first_trajectory_entry(entries):
    """First eval entry whose input contains trajectory lines. None if no such entry."""
    for e in entries:
        if has_trajectory(e['input']):
            return e
    return None


def main() -> int:
    data = load_preprocessed()
    blocks = data['blocks']

    print('=' * 72)
    print('SMOKE TEST — training format vs eval format per condition')
    print('=' * 72)

    exit_code = 0
    block = blocks[0]

    for condition in ('A', 'B'):
        print(f'\n--- CONDITION {condition} ---')

        # Training format check
        train_texts = block['train_a' if condition == 'A' else 'train_b']
        train_has_traj_rate = sum(1 for t in train_texts if has_trajectory(t)) / len(train_texts)
        print(f'Training samples with trajectory: '
              f'{train_has_traj_rate:.1%} ({len(train_texts)} total)')

        # Eval prompt transformation check
        entry = find_first_trajectory_entry(block['eval_entries_raw'])
        if entry is None:
            print('  SKIP: no eval entries with trajectory in block D1 (unusual)')
            continue

        prompt = build_generation_prompt(entry, condition)
        in_has_traj = has_trajectory(entry['input'])
        out_has_traj = has_trajectory(prompt)

        print(f'Example eval entry (first 160 chars of input):')
        print(f'  {entry["input"][:160]!r}')
        print(f'Input has trajectory:  {in_has_traj}')
        print(f'Prompt has trajectory: {out_has_traj}')

        if condition == 'A':
            # A must strip. Input had trajectory, prompt must not.
            if out_has_traj:
                print('  FAIL: condition A should strip trajectory from eval prompt')
                exit_code = 1
            else:
                print('  PASS: A strips trajectory (matches A training)')
        else:
            # B must preserve. Input had trajectory, prompt must too.
            if not out_has_traj:
                print('  FAIL: condition B should preserve trajectory in eval prompt')
                exit_code = 1
            else:
                print('  PASS: B preserves trajectory (matches B training)')

    print('\n--- TRAINING OVERFLOW CHECK ---')
    max_seq = data.get('config', {}).get('max_seq_len', 1024)
    for condition in ('A', 'B'):
        key = 'train_a_prompt_lens' if condition == 'A' else 'train_b_prompt_lens'
        all_plens = [p for b in blocks for p in b[key]]
        overflow = sum(1 for p in all_plens if p >= max_seq)
        total = len(all_plens)
        pct = 100 * overflow / total if total else 0
        flag = 'WARN' if pct > 5 else 'OK'
        print(f'  {condition}: {overflow}/{total} ({pct:.1f}%) samples prompt_len >= '
              f'{max_seq} [{flag}]')
        if pct > 5:
            print(f'      these samples train with all labels masked to -100 '
                  '(zero gradient signal)')

    print('\n' + '=' * 72)
    if exit_code == 0:
        print('SMOKE TEST PASSED. Safe to start training.')
    else:
        print('SMOKE TEST FAILED. Fix before training.')
    print('=' * 72)
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
