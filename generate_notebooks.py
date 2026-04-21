#!/usr/bin/env python3
"""Generate the three experiment notebooks for the final project."""

import json
import os
from textwrap import dedent

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "final")


def sl(text):
    text = dedent(text).strip("\n")
    if not text:
        return [""]
    lines = text.split("\n")
    if len(lines) == 1:
        return [lines[0]]
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": sl(src)}


def code(src):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": sl(src),
    }


def make_nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_nb(name, cells):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w") as f:
        json.dump(make_nb(cells), f, indent=1)
    with open(path) as f:
        json.load(f)  # verify
    print(f"  {name}: {len(cells)} cells, {os.path.getsize(path)/1024:.1f} KB")


# ================================================================
# NOTEBOOK 1: DATA PREPARATION
# ================================================================

nb1_cells = [
    md(
        "# 01 — Data Preparation\n"
        "\n"
        "**Project:** Post-Only (A) vs Trajectory (B) Supervision "
        "for Continual Tool-Use Learning\n"
        "\n"
        "This notebook:\n"
        "1. Downloads API-Bank from HuggingFace\n"
        "2. Extracts API names, excludes ToolSearcher (meta-API)\n"
        "3. Builds 6 balanced domain blocks via greedy bin-packing\n"
        "4. Creates 80/20 train/eval splits per block\n"
        "5. Formats data for Conditions A, B, and A+ (Llama 3.1 chat template)\n"
        "6. Saves preprocessed data as pickle"
    ),
    code("!pip install -q transformers datasets huggingface_hub numpy tqdm"),
    code(
        "import json\n"
        "import os\n"
        "import re\n"
        "import random\n"
        "import pickle\n"
        "import numpy as np\n"
        "from collections import defaultdict\n"
        "from tqdm.auto import tqdm\n"
        "from huggingface_hub import hf_hub_download\n"
        "\n"
        "SEED = 42\n"
        "random.seed(SEED)\n"
        "np.random.seed(SEED)\n"
        'print(f"Seed: {SEED}")'
    ),
    md("## 1. Download API-Bank"),
    code(
        "data_files = [\n"
        '    "training-data/lv1-train.json",\n'
        '    "training-data/lv2-train.json",\n'
        '    "training-data/lv3-train.json",\n'
        "]\n"
        "\n"
        "all_raw = []\n"
        "for fname in data_files:\n"
        "    path = hf_hub_download(\n"
        '        repo_id="liminghao1630/API-Bank",\n'
        "        filename=fname,\n"
        '        repo_type="dataset",\n'
        "    )\n"
        "    with open(path) as f:\n"
        "        entries = json.load(f)\n"
        '    print(f"{fname}: {len(entries)} entries")\n'
        "    all_raw.extend(entries)\n"
        "\n"
        'print(f"\\nTotal raw entries: {len(all_raw)}")\n'
        'print(f"Keys: {list(all_raw[0].keys())}")'
    ),
    md("## 2. Extract API Names & Filter"),
    code(
        "def extract_api_name(entry):\n"
        "    # Extract primary API name from entry output or input\n"
        "    text = entry.get('output', '') or ''\n"
        "    match = re.search(r'\\[([A-Za-z_][A-Za-z0-9_]*)\\(', text)\n"
        "    if match:\n"
        "        return match.group(1)\n"
        "    text = entry.get('input', '') or ''\n"
        "    match = re.search(r'\\[([A-Za-z_][A-Za-z0-9_]*)\\(', text)\n"
        "    if match:\n"
        "        return match.group(1)\n"
        "    return 'unknown'\n"
        "\n"
        "for entry in all_raw:\n"
        "    entry['api_name'] = extract_api_name(entry)\n"
        "\n"
        "api_counts = defaultdict(int)\n"
        "for entry in all_raw:\n"
        "    api_counts[entry['api_name']] += 1\n"
        "\n"
        "sorted_apis = sorted(api_counts.items(), key=lambda x: -x[1])\n"
        'print(f"Unique APIs: {len(sorted_apis)}")\n'
        'print(f"ToolSearcher entries: {api_counts.get(\'ToolSearcher\', 0)}")\n'
        'print(f"\\nTop 10 APIs:")\n'
        "for api, count in sorted_apis[:10]:\n"
        '    print(f"  {api}: {count}")'
    ),
    code(
        "# Exclude ToolSearcher (meta-API) and unknown\n"
        "filtered = [e for e in all_raw if e['api_name'] not in ('ToolSearcher', 'unknown')]\n"
        'print(f"After excluding ToolSearcher: {len(filtered)} entries "\n'
        '      f"(removed {len(all_raw) - len(filtered)})")\n'
        "\n"
        "MIN_ENTRIES = 10\n"
        "api_counts_filtered = defaultdict(int)\n"
        "for entry in filtered:\n"
        "    api_counts_filtered[entry['api_name']] += 1\n"
        "\n"
        "valid_apis = sorted(\n"
        "    [api for api, count in api_counts_filtered.items() if count >= MIN_ENTRIES]\n"
        ")\n"
        "valid_entries = [e for e in filtered if e['api_name'] in valid_apis]\n"
        "\n"
        'print(f"APIs with >= {MIN_ENTRIES} entries: {len(valid_apis)}")\n'
        'print(f"Entries from valid APIs: {len(valid_entries)}")'
    ),
    md("## 3. Load Tokenizer"),
    code(
        "from transformers import AutoTokenizer\n"
        "\n"
        'MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"\n'
        "tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)\n"
        "if tokenizer.pad_token is None:\n"
        "    tokenizer.pad_token = tokenizer.eos_token\n"
        'tokenizer.padding_side = "right"\n'
        'print(f"Tokenizer loaded: {MODEL_NAME}")\n'
        'print(f"Vocab size: {len(tokenizer)}")'
    ),
    md(
        "## 4. Format Functions (Llama 3.1 Chat Template)\n"
        "\n"
        "Both conditions use the **same system prompt** and **same output**.\n"
        "Only difference: whether input context includes prior API interactions.\n"
        "\n"
        "- **Condition A (Post-Only):** API-Request/Response lines removed from input\n"
        "- **Condition B (Trajectory):** Full dialogue kept in input"
    ),
    code(
        "SYSTEM_PROMPT = (\n"
        '    "You are a helpful assistant that can use tools. "\n'
        '    "When you need to call an API, use the format: "\n'
        '    "[ApiName(param1=\'value1\', param2=\'value2\')]. "\n'
        '    "After receiving the API response, use it to formulate your answer."\n'
        ")\n"
        "\n"
        "def _strip_api_lines(text):\n"
        "    # Remove API-Request, API-Response, and related lines\n"
        "    lines = text.split('\\n')\n"
        "    out = []\n"
        "    for line in lines:\n"
        "        s = line.strip()\n"
        "        if s.startswith('API-Request:') or s.startswith('API-Response:'):\n"
        "            continue\n"
        "        if 'Received API Response' in line or 'Generate API Request' in line:\n"
        "            continue\n"
        "        out.append(line)\n"
        "    return '\\n'.join(out).strip()\n"
        "\n"
        "def format_entry(entry, condition, tokenizer):\n"
        "    # Format a single entry. Returns (full_text, prompt_token_len).\n"
        "    inp = entry['input']\n"
        "    out = entry.get('output', '')\n"
        "\n"
        "    if condition == 'A':\n"
        "        context = _strip_api_lines(inp)\n"
        "    else:\n"
        "        context = inp\n"
        "\n"
        "    prompt = (\n"
        '        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\\n\\n"\n'
        "        + SYSTEM_PROMPT\n"
        '        + "<|eot_id|><|start_header_id|>user<|end_header_id|>\\n\\n"\n'
        "        + context\n"
        '        + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\\n\\n"\n'
        "    )\n"
        '    response = out + "<|eot_id|>"\n'
        "    full_text = prompt + response\n"
        "    prompt_len = len(tokenizer.encode(prompt, add_special_tokens=False))\n"
        "    return full_text, prompt_len\n"
        "\n"
        "# Quick test\n"
        "sample = valid_entries[0]\n"
        "for cond in ['A', 'B']:\n"
        "    text, plen = format_entry(sample, cond, tokenizer)\n"
        "    total = len(tokenizer.encode(text))\n"
        '    print(f"Condition {cond}: {total} tokens (prompt: {plen}, response: {total - plen})")\n'
        'print(f"\\nSample output: {sample.get(\'output\', \'\')[:100]}")'
    ),
    md("## 5. Compute Token Counts & Greedy Bin-Packing"),
    code(
        "# Estimate token counts per API\n"
        "api_stats = {}\n"
        'for api in tqdm(valid_apis, desc="Token counting"):\n'
        "    entries = [e for e in valid_entries if e['api_name'] == api]\n"
        "    sample = entries[:min(20, len(entries))]\n"
        "    tokens_a = [len(tokenizer.encode(format_entry(e, 'A', tokenizer)[0])) for e in sample]\n"
        "    tokens_b = [len(tokenizer.encode(format_entry(e, 'B', tokenizer)[0])) for e in sample]\n"
        "    api_stats[api] = {\n"
        "        'count': len(entries),\n"
        "        'avg_tokens_a': np.mean(tokens_a),\n"
        "        'avg_tokens_b': np.mean(tokens_b),\n"
        "        'est_total_b': np.mean(tokens_b) * len(entries),\n"
        "    }\n"
        "\n"
        "total_entries = sum(s['count'] for s in api_stats.values())\n"
        "total_tokens_b = sum(s['est_total_b'] for s in api_stats.values())\n"
        'print(f"Total entries: {total_entries}")\n'
        'print(f"Estimated total tokens (B): {total_tokens_b:,.0f}")'
    ),
    code(
        "# Greedy bin-packing into 6 blocks\n"
        "NUM_BLOCKS = 6\n"
        "sorted_api_names = sorted(valid_apis, key=lambda x: -api_stats[x]['est_total_b'])\n"
        "\n"
        "block_api_lists = [[] for _ in range(NUM_BLOCKS)]\n"
        "block_token_totals = [0.0] * NUM_BLOCKS\n"
        "\n"
        "for api in sorted_api_names:\n"
        "    min_idx = int(np.argmin(block_token_totals))\n"
        "    block_api_lists[min_idx].append(api)\n"
        "    block_token_totals[min_idx] += api_stats[api]['est_total_b']\n"
        "\n"
        'print("Block composition:")\n'
        "for i in range(NUM_BLOCKS):\n"
        "    n_apis = len(block_api_lists[i])\n"
        "    n_entries = sum(api_stats[a]['count'] for a in block_api_lists[i])\n"
        '    print(f"  D{i+1}: {n_apis} APIs, {n_entries} entries, ~{block_token_totals[i]:,.0f} tokens")'
    ),
    md("## 6. Build Domain Blocks with Train/Eval Splits"),
    code(
        "MAX_SEQ_LEN = 2048\n"
        "\n"
        "domain_blocks = []\n"
        "for i in range(NUM_BLOCKS):\n"
        "    block_entries = [e for e in valid_entries if e['api_name'] in block_api_lists[i]]\n"
        "    random.shuffle(block_entries)\n"
        "    split_idx = int(len(block_entries) * 0.8)\n"
        "    train_entries = block_entries[:split_idx]\n"
        "    eval_entries = block_entries[split_idx:]\n"
        "    domain_blocks.append({\n"
        "        'block_id': i + 1,\n"
        "        'apis': block_api_lists[i],\n"
        "        'train_entries': train_entries,\n"
        "        'eval_entries': eval_entries,\n"
        "    })\n"
        '    print(f"D{i+1}: {len(train_entries)} train, {len(eval_entries)} eval")'
    ),
    md("## 7. Format All Data & Compute Token Stats"),
    code(
        "blocks_data = []\n"
        "BASE_EPOCHS = 3\n"
        "\n"
        'for block in tqdm(domain_blocks, desc="Formatting"):\n'
        "    bid = block['block_id']\n"
        "    train_a, train_a_plens = [], []\n"
        "    train_b, train_b_plens = [], []\n"
        "    for e in block['train_entries']:\n"
        "        ta, pa = format_entry(e, 'A', tokenizer)\n"
        "        tb, pb = format_entry(e, 'B', tokenizer)\n"
        "        train_a.append(ta); train_a_plens.append(pa)\n"
        "        train_b.append(tb); train_b_plens.append(pb)\n"
        "\n"
        "    eval_a, eval_a_plens = [], []\n"
        "    eval_b, eval_b_plens = [], []\n"
        "    for e in block['eval_entries']:\n"
        "        ta, pa = format_entry(e, 'A', tokenizer)\n"
        "        tb, pb = format_entry(e, 'B', tokenizer)\n"
        "        eval_a.append(ta); eval_a_plens.append(pa)\n"
        "        eval_b.append(tb); eval_b_plens.append(pb)\n"
        "\n"
        "    tokens_a = sum(min(len(tokenizer.encode(t)), MAX_SEQ_LEN) for t in train_a)\n"
        "    tokens_b = sum(min(len(tokenizer.encode(t)), MAX_SEQ_LEN) for t in train_b)\n"
        "    ratio = tokens_b / tokens_a if tokens_a > 0 else 1.0\n"
        "    aplus_epochs = max(round(BASE_EPOCHS * ratio), BASE_EPOCHS)\n"
        "\n"
        "    blocks_data.append({\n"
        "        'block_id': bid,\n"
        "        'apis': block['apis'],\n"
        "        'train_a': train_a, 'train_b': train_b,\n"
        "        'train_a_prompt_lens': train_a_plens, 'train_b_prompt_lens': train_b_plens,\n"
        "        'eval_a': eval_a, 'eval_b': eval_b,\n"
        "        'eval_a_prompt_lens': eval_a_plens, 'eval_b_prompt_lens': eval_b_plens,\n"
        "        'eval_entries_raw': block['eval_entries'],\n"
        "        'train_tokens_a': tokens_a, 'train_tokens_b': tokens_b,\n"
        "        'token_ratio': ratio, 'aplus_epochs': aplus_epochs,\n"
        "    })\n"
        '    print(f"D{bid}: A={tokens_a:,} tok, B={tokens_b:,} tok, "\n'
        '          f"ratio={ratio:.2f}x, A+ epochs={aplus_epochs}")'
    ),
    md("## 8. Save Preprocessed Data"),
    code(
        'OUTPUT_DIR = "preprocessed_data"\n'
        "os.makedirs(OUTPUT_DIR, exist_ok=True)\n"
        "\n"
        "save_data = {\n"
        "    'blocks': blocks_data,\n"
        "    'config': {\n"
        "        'model_name': MODEL_NAME,\n"
        "        'num_blocks': NUM_BLOCKS,\n"
        "        'max_seq_len': MAX_SEQ_LEN,\n"
        "        'base_epochs': BASE_EPOCHS,\n"
        "        'seed': SEED,\n"
        "        'min_entries': MIN_ENTRIES,\n"
        "        'toolsearcher_excluded': True,\n"
        "        'total_valid_apis': len(valid_apis),\n"
        "        'total_valid_entries': len(valid_entries),\n"
        "        'system_prompt': SYSTEM_PROMPT,\n"
        "    },\n"
        "}\n"
        "\n"
        "pkl_path = os.path.join(OUTPUT_DIR, 'preprocessed.pkl')\n"
        "with open(pkl_path, 'wb') as f:\n"
        "    pickle.dump(save_data, f)\n"
        "\n"
        "# Human-readable summary\n"
        "summary = {\n"
        "    'config': save_data['config'],\n"
        "    'blocks': [{\n"
        "        'block_id': b['block_id'],\n"
        "        'num_apis': len(b['apis']),\n"
        "        'apis': b['apis'][:10],\n"
        "        'num_train': len(b['train_a']),\n"
        "        'num_eval': len(b['eval_a']),\n"
        "        'train_tokens_a': b['train_tokens_a'],\n"
        "        'train_tokens_b': b['train_tokens_b'],\n"
        "        'token_ratio': round(b['token_ratio'], 3),\n"
        "        'aplus_epochs': b['aplus_epochs'],\n"
        "    } for b in blocks_data],\n"
        "}\n"
        "json_path = os.path.join(OUTPUT_DIR, 'summary.json')\n"
        "with open(json_path, 'w') as f:\n"
        "    json.dump(summary, f, indent=2)\n"
        "\n"
        "pkl_size = os.path.getsize(pkl_path) / 1e6\n"
        'print(f"\\nSaved to {OUTPUT_DIR}/")\n'
        'print(f"  preprocessed.pkl  ({pkl_size:.1f} MB)")\n'
        'print(f"  summary.json")'
    ),
]


# ================================================================
# NOTEBOOK 2: TRAINING & EVALUATION
# ================================================================

nb2_cells = [
    md(
        "# 02 — Training & Evaluation\n"
        "\n"
        "**Project:** Post-Only (A) vs Trajectory (B) Supervision "
        "for Continual Tool-Use Learning\n"
        "\n"
        "This notebook trains on 6 sequential domain blocks and evaluates after each."
    ),
    code(
        "# ============================================================\n"
        "# CONFIGURATION\n"
        "# ============================================================\n"
        'CONDITION = "B"   # "A", "B", or "A+"\n'
        "SEED = 42"
    ),
    code("!pip install -q transformers accelerate peft bitsandbytes trl huggingface_hub tqdm"),
    code(
        "import json\n"
        "import os\n"
        "import re\n"
        "import random\n"
        "import time\n"
        "import pickle\n"
        "import numpy as np\n"
        "from tqdm.auto import tqdm\n"
        "\n"
        "import torch\n"
        "from transformers import (\n"
        "    AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig,\n"
        "    TrainingArguments, DataCollatorForLanguageModeling, Trainer,\n"
        ")\n"
        "from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training\n"
        "from torch.utils.data import Dataset\n"
        "\n"
        "random.seed(SEED)\n"
        "np.random.seed(SEED)\n"
        "torch.manual_seed(SEED)\n"
        "torch.cuda.manual_seed_all(SEED)\n"
        "\n"
        'print(f"Condition: {CONDITION} | Seed: {SEED}")\n'
        'print(f"GPU: {torch.cuda.get_device_name(0)}")\n'
        'print(f"VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")'
    ),
    md("## 1. Load Preprocessed Data"),
    code(
        "with open('preprocessed_data/preprocessed.pkl', 'rb') as f:\n"
        "    data = pickle.load(f)\n"
        "\n"
        "blocks = data['blocks']\n"
        "config = data['config']\n"
        "MODEL_NAME = config['model_name']\n"
        "MAX_SEQ_LEN = config['max_seq_len']\n"
        "NUM_BLOCKS = config['num_blocks']\n"
        "BASE_EPOCHS = config['base_epochs']\n"
        "\n"
        'print(f"Model: {MODEL_NAME}")\n'
        'print(f"Blocks: {NUM_BLOCKS}, Seq len: {MAX_SEQ_LEN}")\n'
        'print(f"\\nBlock sizes:")\n'
        "for b in blocks:\n"
        '    print(f"  D{b[\'block_id\']}: {len(b[\'train_a\'])} train, {len(b[\'eval_a\'])} eval")'
    ),
    code(
        "def get_train_texts(block, condition):\n"
        "    if condition in ('A', 'A+'):\n"
        "        return block['train_a'], block['train_a_prompt_lens']\n"
        "    return block['train_b'], block['train_b_prompt_lens']\n"
        "\n"
        "def get_eval_texts(block, condition):\n"
        "    if condition in ('A', 'A+'):\n"
        "        return block['eval_a'], block['eval_a_prompt_lens']\n"
        "    return block['eval_b'], block['eval_b_prompt_lens']\n"
        "\n"
        "def get_epochs(block, condition):\n"
        "    if condition == 'A+':\n"
        "        return block['aplus_epochs']\n"
        "    return BASE_EPOCHS"
    ),
    md("## 2. Load Model"),
    code(
        'ATTN_IMPL = "sdpa"\n'
        "\n"
        "bnb_config = BitsAndBytesConfig(\n"
        "    load_in_4bit=True,\n"
        '    bnb_4bit_quant_type="nf4",\n'
        "    bnb_4bit_compute_dtype=torch.bfloat16,\n"
        "    bnb_4bit_use_double_quant=True,\n"
        ")\n"
        "\n"
        "tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)\n"
        "if tokenizer.pad_token is None:\n"
        "    tokenizer.pad_token = tokenizer.eos_token\n"
        'tokenizer.padding_side = "right"\n'
        "\n"
        "def load_fresh_model():\n"
        "    model = AutoModelForCausalLM.from_pretrained(\n"
        "        MODEL_NAME,\n"
        "        quantization_config=bnb_config,\n"
        '        device_map="auto",\n'
        "        torch_dtype=torch.bfloat16,\n"
        "        attn_implementation=ATTN_IMPL,\n"
        "    )\n"
        "    model = prepare_model_for_kbit_training(model)\n"
        "    lora_config = LoraConfig(\n"
        "        r=32, lora_alpha=64,\n"
        "        target_modules=[\n"
        '            "q_proj", "k_proj", "v_proj", "o_proj",\n'
        '            "gate_proj", "up_proj", "down_proj",\n'
        "        ],\n"
        '        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",\n'
        "    )\n"
        "    model = get_peft_model(model, lora_config)\n"
        "    model.print_trainable_parameters()\n"
        "    return model\n"
        "\n"
        "model = load_fresh_model()"
    ),
    md("## 3. Dataset & Training"),
    code(
        "class TextDataset(Dataset):\n"
        "    # Dataset with prompt-masked labels for causal LM training\n"
        "    def __init__(self, texts, prompt_lens, tokenizer, max_length):\n"
        "        self.items = []\n"
        "        for text, plen in zip(texts, prompt_lens):\n"
        "            enc = tokenizer(\n"
        "                text, truncation=True, max_length=max_length,\n"
        '                padding="max_length", return_tensors="pt",\n'
        "            )\n"
        "            input_ids = enc['input_ids'].squeeze()\n"
        "            attn_mask = enc['attention_mask'].squeeze()\n"
        "            labels = input_ids.clone()\n"
        "            labels[:min(plen, max_length)] = -100  # mask prompt\n"
        "            labels[attn_mask == 0] = -100  # mask padding\n"
        "            self.items.append({\n"
        "                'input_ids': input_ids,\n"
        "                'attention_mask': attn_mask,\n"
        "                'labels': labels,\n"
        "            })\n"
        "\n"
        "    def __len__(self):\n"
        "        return len(self.items)\n"
        "\n"
        "    def __getitem__(self, idx):\n"
        "        return self.items[idx]"
    ),
    code(
        "BATCH_SIZE = 16\n"
        "LR = 2e-4\n"
        "\n"
        "def train_on_block(model, texts, prompt_lens, block_name, num_epochs):\n"
        "    # Train model on one block. Returns (loss, elapsed).\n"
        "    dataset = TextDataset(texts, prompt_lens, tokenizer, MAX_SEQ_LEN)\n"
        '    print(f"  Training {len(dataset)} examples, {num_epochs} epochs...")\n'
        "\n"
        "    args = TrainingArguments(\n"
        '        output_dir=f"/tmp/ckpt_{block_name}",\n'
        "        num_train_epochs=num_epochs,\n"
        "        per_device_train_batch_size=BATCH_SIZE,\n"
        "        gradient_accumulation_steps=1,\n"
        "        learning_rate=LR,\n"
        "        bf16=True,\n"
        "        logging_steps=10,\n"
        '        save_strategy="no",\n'
        '        report_to="none",\n'
        '        optim="paged_adamw_8bit",\n'
        "        warmup_ratio=0.1,\n"
        '        lr_scheduler_type="cosine",\n'
        "        seed=SEED,\n"
        "        dataloader_pin_memory=True,\n"
        "        dataloader_num_workers=4,\n"
        "        gradient_checkpointing=False,\n"
        "    )\n"
        "\n"
        "    trainer = Trainer(\n"
        "        model=model, train_dataset=dataset, args=args,\n"
        "        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),\n"
        "    )\n"
        "    start = time.time()\n"
        "    result = trainer.train()\n"
        "    elapsed = time.time() - start\n"
        '    print(f"  {block_name}: loss={result.training_loss:.4f}, time={elapsed:.0f}s")\n'
        "    return result.training_loss, elapsed"
    ),
    md("## 4. Evaluation Functions"),
    code(
        "@torch.no_grad()\n"
        "def evaluate_loss(model, texts, prompt_lens, max_samples=100):\n"
        "    # Compute average loss and perplexity on response tokens only\n"
        "    model.eval()\n"
        "    indices = random.sample(range(len(texts)), min(max_samples, len(texts)))\n"
        "    total_loss, total_tokens = 0.0, 0\n"
        "\n"
        "    for idx in indices:\n"
        "        enc = tokenizer(\n"
        "            texts[idx], truncation=True,\n"
        '            max_length=MAX_SEQ_LEN, return_tensors="pt",\n'
        "        ).to(model.device)\n"
        "        labels = enc['input_ids'].clone()\n"
        "        plen = min(prompt_lens[idx], labels.shape[1])\n"
        "        labels[0, :plen] = -100\n"
        "        labels[enc['attention_mask'] == 0] = -100\n"
        "\n"
        "        outputs = model(\n"
        "            input_ids=enc['input_ids'],\n"
        "            attention_mask=enc['attention_mask'],\n"
        "            labels=labels,\n"
        "        )\n"
        "        n = (labels != -100).sum().item()\n"
        "        if n > 0:\n"
        "            total_loss += outputs.loss.item() * n\n"
        "            total_tokens += n\n"
        "\n"
        "    avg_loss = total_loss / total_tokens if total_tokens > 0 else float('inf')\n"
        "    ppl = np.exp(min(avg_loss, 100))\n"
        "    model.train()\n"
        "    return avg_loss, ppl"
    ),
    code(
        "@torch.no_grad()\n"
        "def evaluate_generation(model, entries, max_samples=100):\n"
        "    # Evaluate API-call generation accuracy\n"
        "    # Returns (api_name_accuracy, full_accuracy)\n"
        "    model.eval()\n"
        "    if len(entries) > max_samples:\n"
        "        entries = random.sample(entries, max_samples)\n"
        "\n"
        "    system_prompt = config['system_prompt']\n"
        "    name_correct, full_correct, total = 0, 0, 0\n"
        "\n"
        "    for entry in entries:\n"
        "        expected = entry.get('output', '')\n"
        "        match = re.search(r'\\[([A-Za-z_][A-Za-z0-9_]*)\\(', expected)\n"
        "        if not match:\n"
        "            continue\n"
        "        expected_api = match.group(1)\n"
        "        expected_params = dict(re.findall(r\"(\\w+)='([^']*)'\", expected))\n"
        "\n"
        "        inp = entry['input']\n"
        "        prompt = (\n"
        '            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\\n\\n"\n'
        "            + system_prompt\n"
        '            + "<|eot_id|><|start_header_id|>user<|end_header_id|>\\n\\n"\n'
        "            + inp\n"
        '            + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\\n\\n"\n'
        "        )\n"
        "\n"
        "        enc = tokenizer(\n"
        "            prompt, truncation=True,\n"
        '            max_length=MAX_SEQ_LEN - 128, return_tensors="pt",\n'
        "        ).to(model.device)\n"
        "\n"
        "        gen = model.generate(\n"
        "            **enc, max_new_tokens=128,\n"
        "            do_sample=False, pad_token_id=tokenizer.eos_token_id,\n"
        "        )\n"
        "        generated = tokenizer.decode(\n"
        "            gen[0][enc['input_ids'].shape[1]:], skip_special_tokens=True\n"
        "        )\n"
        "\n"
        "        if expected_api.lower() in generated.lower():\n"
        "            name_correct += 1\n"
        "            if expected_params:\n"
        "                gen_params = dict(re.findall(r\"(\\w+)='([^']*)'\", generated))\n"
        "                if any(\n"
        "                    gen_params.get(k, '').lower() == v.lower()\n"
        "                    for k, v in expected_params.items()\n"
        "                ):\n"
        "                    full_correct += 1\n"
        "            else:\n"
        "                full_correct += 1\n"
        "        total += 1\n"
        "\n"
        "    model.train()\n"
        "    name_acc = name_correct / total if total > 0 else 0.0\n"
        "    full_acc = full_correct / total if total > 0 else 0.0\n"
        "    return name_acc, full_acc"
    ),
    md("## 5. Zero-Shot Baseline"),
    code(
        'print("=" * 60)\n'
        'print("ZERO-SHOT BASELINE")\n'
        'print("=" * 60)\n'
        "\n"
        "zero_shot = {'loss': [], 'ppl': [], 'name_acc': [], 'full_acc': []}\n"
        "\n"
        "for j in range(NUM_BLOCKS):\n"
        "    eval_texts, eval_plens = get_eval_texts(blocks[j], CONDITION)\n"
        "    loss, ppl = evaluate_loss(model, eval_texts, eval_plens)\n"
        "    name_acc, full_acc = evaluate_generation(model, blocks[j]['eval_entries_raw'])\n"
        "    zero_shot['loss'].append(loss)\n"
        "    zero_shot['ppl'].append(ppl)\n"
        "    zero_shot['name_acc'].append(name_acc)\n"
        "    zero_shot['full_acc'].append(full_acc)\n"
        '    print(f"  D{j+1}: loss={loss:.3f}, ppl={ppl:.1f}, "\n'
        '          f"name={name_acc:.1%}, full={full_acc:.1%}")'
    ),
    md("## 6. Continual Learning Loop"),
    code(
        "print(f\"\\n{'=' * 60}\")\n"
        'print(f"CONTINUAL LEARNING — Condition {CONDITION}, Seed {SEED}")\n'
        "print(f\"{'=' * 60}\")\n"
        "\n"
        "eval_loss_mat = np.zeros((NUM_BLOCKS, NUM_BLOCKS))\n"
        "eval_ppl_mat = np.zeros((NUM_BLOCKS, NUM_BLOCKS))\n"
        "eval_acc_mat = np.zeros((NUM_BLOCKS, NUM_BLOCKS))\n"
        "eval_full_acc_mat = np.zeros((NUM_BLOCKS, NUM_BLOCKS))\n"
        "train_losses, train_times, epochs_per_block = [], [], []\n"
        "\n"
        'CHECKPOINT_DIR = f"checkpoints_{CONDITION}_seed{SEED}"\n'
        "os.makedirs(CHECKPOINT_DIR, exist_ok=True)\n"
        "experiment_start = time.time()\n"
        "\n"
        "for i in range(NUM_BLOCKS):\n"
        '    print(f"\\n--- Training on D{i+1}/{NUM_BLOCKS} ---")\n'
        "    train_texts, train_plens = get_train_texts(blocks[i], CONDITION)\n"
        "    epochs = get_epochs(blocks[i], CONDITION)\n"
        "    epochs_per_block.append(epochs)\n"
        "\n"
        "    t_loss, t_time = train_on_block(\n"
        "        model, train_texts, train_plens,\n"
        '        block_name=f"{CONDITION}_s{SEED}_D{i+1}",\n'
        "        num_epochs=epochs,\n"
        "    )\n"
        "    train_losses.append(t_loss)\n"
        "    train_times.append(t_time)\n"
        "\n"
        '    print(f"  Evaluating all blocks...")\n'
        "    for j in range(NUM_BLOCKS):\n"
        "        eval_texts, eval_plens = get_eval_texts(blocks[j], CONDITION)\n"
        "        loss, ppl = evaluate_loss(model, eval_texts, eval_plens)\n"
        "        name_acc, full_acc = evaluate_generation(model, blocks[j]['eval_entries_raw'])\n"
        "        eval_loss_mat[i][j] = loss\n"
        "        eval_ppl_mat[i][j] = ppl\n"
        "        eval_acc_mat[i][j] = name_acc\n"
        "        eval_full_acc_mat[i][j] = full_acc\n"
        '        tag = "(curr)" if j == i else "(prev)" if j < i else "(fut)"\n'
        '        print(f"    D{j+1} {tag}: loss={loss:.3f}, ppl={ppl:.1f}, "\n'
        '              f"name={name_acc:.1%}, full={full_acc:.1%}")\n'
        "\n"
        "    # Checkpoint after each block\n"
        "    ckpt = {\n"
        "        'condition': CONDITION, 'seed': SEED,\n"
        "        'blocks_trained': i + 1,\n"
        "        'eval_loss': eval_loss_mat[:i+1].tolist(),\n"
        "        'eval_ppl': eval_ppl_mat[:i+1].tolist(),\n"
        "        'eval_acc': eval_acc_mat[:i+1].tolist(),\n"
        "        'eval_full_acc': eval_full_acc_mat[:i+1].tolist(),\n"
        "        'train_losses': train_losses, 'train_times': train_times,\n"
        "    }\n"
        "    with open(f'{CHECKPOINT_DIR}/after_D{i+1}.json', 'w') as f:\n"
        "        json.dump(ckpt, f, indent=2)\n"
        '    print(f"  Checkpoint saved")\n'
        "\n"
        "total_time = time.time() - experiment_start\n"
        'print(f"\\nTotal: {total_time:.0f}s ({total_time/60:.1f} min)")'
    ),
    md("## 7. Save Final Results"),
    code(
        "results = {\n"
        "    'condition': CONDITION,\n"
        "    'seed': SEED,\n"
        "    'zero_shot': zero_shot,\n"
        "    'eval_loss': eval_loss_mat.tolist(),\n"
        "    'eval_ppl': eval_ppl_mat.tolist(),\n"
        "    'eval_acc': eval_acc_mat.tolist(),\n"
        "    'eval_full_acc': eval_full_acc_mat.tolist(),\n"
        "    'train_losses': train_losses,\n"
        "    'train_times': train_times,\n"
        "    'epochs_per_block': epochs_per_block,\n"
        "    'total_time': total_time,\n"
        "    'config': {\n"
        "        'model': MODEL_NAME,\n"
        "        'num_blocks': NUM_BLOCKS,\n"
        "        'base_epochs': BASE_EPOCHS,\n"
        "        'batch_size': BATCH_SIZE,\n"
        "        'lr': LR,\n"
        "        'max_seq_len': MAX_SEQ_LEN,\n"
        "        'lora_r': 32, 'lora_alpha': 64,\n"
        "        'attn': ATTN_IMPL,\n"
        "        'precision': 'bf16',\n"
        "    },\n"
        "}\n"
        "\n"
        'output_file = f"results_{CONDITION}_seed{SEED}.json"\n'
        "with open(output_file, 'w') as f:\n"
        "    json.dump(results, f, indent=2)\n"
        "\n"
        'print(f"\\nResults saved: {output_file}")'
    ),
]


# ================================================================
# NOTEBOOK 3: ANALYSIS & VISUALIZATION
# ================================================================

nb3_cells = [
    md(
        "# 03 — Analysis & Visualization\n"
        "\n"
        "**Project:** Post-Only (A) vs Trajectory (B) Supervision "
        "for Continual Tool-Use Learning"
    ),
    code(
        "import json\n"
        "import os\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "from matplotlib.lines import Line2D"
    ),
    md("## 1. Load Results"),
    code(
        "result_files = [\n"
        "    'results_A_seed42.json',\n"
        "    'results_B_seed42.json',\n"
        "    'results_A+_seed42.json',\n"
        "]\n"
        "\n"
        "results = {}\n"
        "for fname in result_files:\n"
        "    if os.path.exists(fname):\n"
        "        with open(fname) as f:\n"
        "            r = json.load(f)\n"
        "        results[r['condition']] = r\n"
        '        print(f"Loaded: {fname} (condition {r[\'condition\']})")\n'
        "    else:\n"
        '        print(f"NOT FOUND: {fname}")\n'
        "\n"
        'print(f"\\nConditions loaded: {list(results.keys())}")'
    ),
    md("## 2. Continual Learning Metrics"),
    code(
        "def compute_cl_metrics(result):\n"
        "    acc = np.array(result['eval_acc'])\n"
        "    n = acc.shape[0]\n"
        "\n"
        "    aa = np.mean(acc[-1, :])\n"
        "    bwt = np.mean([acc[-1, j] - acc[j, j] for j in range(n-1)]) if n > 1 else 0.0\n"
        "    fwt = np.mean([acc[j-1, j] for j in range(1, n)]) if n > 1 else 0.0\n"
        "\n"
        "    forgetting = []\n"
        "    for j in range(n - 1):\n"
        "        best = max(acc[i, j] for i in range(j, n))\n"
        "        forgetting.append(best - acc[-1, j])\n"
        "    avg_forgetting = np.mean(forgetting) if forgetting else 0.0\n"
        "\n"
        "    aulc_vals = []\n"
        "    for j in range(n):\n"
        "        curve = [acc[i, j] for i in range(j, n)]\n"
        "        if len(curve) > 1:\n"
        "            aulc = np.trapz(curve, dx=1.0) / (len(curve) - 1)\n"
        "        else:\n"
        "            aulc = curve[0]\n"
        "        aulc_vals.append(aulc)\n"
        "    avg_aulc = np.mean(aulc_vals)\n"
        "\n"
        "    return {\n"
        "        'Average Accuracy (AA)': aa,\n"
        "        'Backward Transfer (BWT)': bwt,\n"
        "        'Forward Transfer (FWT)': fwt,\n"
        "        'Average Forgetting': avg_forgetting,\n"
        "        'Average AULC': avg_aulc,\n"
        "    }\n"
        "\n"
        "all_metrics = {}\n"
        "for cond, r in results.items():\n"
        "    m = compute_cl_metrics(r)\n"
        "    all_metrics[cond] = m\n"
        '    print(f"\\nCondition {cond}:")\n'
        "    for k, v in m.items():\n"
        '        print(f"  {k}: {v:.4f}")'
    ),
    md("## 3. Summary Table"),
    code(
        "conds = sorted(results.keys())\n"
        "metric_keys = [\n"
        "    'Average Accuracy (AA)',\n"
        "    'Backward Transfer (BWT)',\n"
        "    'Forward Transfer (FWT)',\n"
        "    'Average Forgetting',\n"
        "    'Average AULC',\n"
        "]\n"
        "\n"
        'print("=" * 80)\n'
        'print("CONTINUAL LEARNING METRICS")\n'
        'print("=" * 80)\n'
        "header = f\"{'Metric':<28}\" + \"\".join(f\"{c:>16}\" for c in conds)\n"
        "print(header)\n"
        'print("-" * (28 + 16 * len(conds)))\n'
        "for key in metric_keys:\n"
        "    row = f\"{key:<28}\"\n"
        "    for c in conds:\n"
        "        row += f\"{all_metrics[c][key]:>16.4f}\"\n"
        "    print(row)"
    ),
    code(
        "# Full evaluation matrices\n"
        "for cond in conds:\n"
        "    r = results[cond]\n"
        "    n = len(r['eval_acc'])\n"
        "    print(f\"\\n{'=' * 72}\")\n"
        '    print(f"EVAL MATRIX — Condition {cond} (API Name Accuracy)")\n'
        "    print(f\"{'=' * 72}\")\n"
        "    print(f\"{'':>14}\", end=\"\")\n"
        "    for j in range(n):\n"
        "        print(f\"{'D' + str(j+1):>10}\", end=\"\")\n"
        "    print()\n"
        "    for i in range(n):\n"
        '        print(f"After D{i+1}:    ", end="")\n'
        "        for j in range(n):\n"
        "            print(f\"{r['eval_acc'][i][j]:>10.1%}\", end=\"\")\n"
        "        print()"
    ),
    md("## 4. Visualizations"),
    code(
        'sns.set_style("whitegrid")\n'
        "fig, axes = plt.subplots(2, 3, figsize=(20, 12))\n"
        "fig.suptitle(\n"
        '    "Post-Only (A) vs Trajectory (B) vs Token-Matched (A+)\\n"\n'
        '    "Continual Tool-Use Learning — Llama 3.1 8B, QLoRA, API-Bank",\n'
        "    fontsize=13, fontweight='bold',\n"
        ")\n"
        "\n"
        "n = len(list(results.values())[0]['eval_acc'])\n"
        "blabels = [f'D{i+1}' for i in range(n)]\n"
        "colors = {'A': '#e74c3c', 'B': '#2ecc71', 'A+': '#3498db'}\n"
        "\n"
        "# Plot 1 & 2: Loss Heatmaps\n"
        "for idx, cond in enumerate(['A', 'B']):\n"
        "    if cond not in results:\n"
        "        continue\n"
        "    ax = axes[0, idx]\n"
        "    data = np.array(results[cond]['eval_loss'])\n"
        "    im = ax.imshow(data, cmap='YlOrRd', aspect='auto')\n"
        "    ax.set_xticks(range(n)); ax.set_yticks(range(n))\n"
        "    ax.set_xticklabels(blabels)\n"
        "    ax.set_yticklabels([f'After {l}' for l in blabels])\n"
        '    ax.set_xlabel("Evaluated on"); ax.set_ylabel("Training stage")\n'
        '    ax.set_title(f"Eval Loss — {cond}")\n'
        "    for i in range(n):\n"
        "        for j in range(n):\n"
        "            c = 'white' if data[i,j] > np.median(data) else 'black'\n"
        "            ax.text(j, i, f'{data[i,j]:.2f}', ha='center', va='center',\n"
        "                    fontsize=6, color=c)\n"
        "    plt.colorbar(im, ax=ax, shrink=0.8)\n"
        "\n"
        "# Plot 3: Forgetting Curves\n"
        "ax = axes[0, 2]\n"
        "for cond in ['A', 'B']:\n"
        "    if cond not in results:\n"
        "        continue\n"
        "    acc = np.array(results[cond]['eval_acc'])\n"
        "    for j in range(n):\n"
        "        stages = list(range(j, n))\n"
        "        vals = [acc[i, j] for i in stages]\n"
        "        style = 'o--' if cond == 'A' else 's-'\n"
        "        alpha = 0.5 if cond == 'A' else 0.9\n"
        "        ax.plot(stages, vals, style, color=f'C{j}', alpha=alpha)\n"
        "ax.set_xticks(range(n))\n"
        "ax.set_xticklabels([f'After {l}' for l in blabels])\n"
        'ax.set_ylabel("API Name Accuracy"); ax.set_title("Forgetting Curves")\n'
        "legend_lines = [\n"
        "    Line2D([0],[0], linestyle='--', marker='o', color='gray'),\n"
        "    Line2D([0],[0], linestyle='-', marker='s', color='gray'),\n"
        "]\n"
        "ax.legend(legend_lines, ['A: Post-Only', 'B: Trajectory'])\n"
        "\n"
        "# Plot 4: Final Accuracy\n"
        "ax = axes[1, 0]\n"
        "x = np.arange(n)\n"
        "w = 0.8 / len(conds)\n"
        "for ci, cond in enumerate(conds):\n"
        "    vals = np.array(results[cond]['eval_acc'])[-1]\n"
        "    ax.bar(x + ci*w - 0.4 + w/2, vals, w,\n"
        "           label=cond, color=colors.get(cond, 'gray'), alpha=0.8)\n"
        "ax.set_xticks(x); ax.set_xticklabels(blabels)\n"
        'ax.set_ylabel("Accuracy"); ax.set_title("Final Accuracy")\n'
        "ax.legend(fontsize=9)\n"
        "\n"
        "# Plot 5: Perplexity\n"
        "ax = axes[1, 1]\n"
        "for cond in ['A', 'B']:\n"
        "    if cond not in results:\n"
        "        continue\n"
        "    ppl = np.array(results[cond]['eval_ppl'])\n"
        "    for j in range(n):\n"
        "        style = 'o--' if cond == 'A' else 's-'\n"
        "        alpha = 0.5 if cond == 'A' else 0.9\n"
        "        ax.plot(range(n), [ppl[i,j] for i in range(n)],\n"
        "                style, color=f'C{j}', alpha=alpha)\n"
        "ax.set_xticks(range(n))\n"
        "ax.set_xticklabels([f'After {l}' for l in blabels])\n"
        'ax.set_ylabel("Perplexity"); ax.set_title("Perplexity Over Time")\n'
        "ax.legend(legend_lines, ['A: Post-Only', 'B: Trajectory'])\n"
        "\n"
        "# Plot 6: CL Metrics\n"
        "ax = axes[1, 2]\n"
        "short_names = ['AA', 'BWT', 'FWT', 'Forget', 'AULC']\n"
        "x = np.arange(len(metric_keys))\n"
        "w = 0.8 / len(conds)\n"
        "for ci, cond in enumerate(conds):\n"
        "    vals = [all_metrics[cond][k] for k in metric_keys]\n"
        "    ax.bar(x + ci*w - 0.4 + w/2, vals, w,\n"
        "           label=cond, color=colors.get(cond, 'gray'), alpha=0.8)\n"
        "ax.set_xticks(x); ax.set_xticklabels(short_names)\n"
        'ax.set_ylabel("Score"); ax.set_title("CL Metrics Comparison")\n'
        "ax.legend(); ax.axhline(y=0, color='black', linewidth=0.5)\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig('final_results.png', dpi=150, bbox_inches='tight')\n"
        "plt.savefig('final_results.pdf', bbox_inches='tight')\n"
        "plt.show()\n"
        'print("Saved: final_results.png, final_results.pdf")'
    ),
    md("## 5. Zero-Shot Baseline"),
    code(
        'print("ZERO-SHOT BASELINE")\n'
        'print("-" * 60)\n'
        "for cond in conds:\n"
        "    r = results[cond]\n"
        "    zs = r.get('zero_shot', {})\n"
        "    if not zs or not zs.get('name_acc'):\n"
        "        continue\n"
        '    print(f"\\n  Condition {cond}:")\n'
        "    for j in range(len(zs['name_acc'])):\n"
        '        print(f"    D{j+1}: name={zs[\'name_acc\'][j]:.1%}, "\n'
        '              f"full={zs[\'full_acc\'][j]:.1%}, "\n'
        '              f"loss={zs[\'loss\'][j]:.3f}")'
    ),
    md("## 6. Token Budget Analysis"),
    code(
        'print("TOKEN BUDGET ANALYSIS")\n'
        'print("=" * 60)\n'
        "\n"
        "if 'A' in all_metrics and 'B' in all_metrics:\n"
        "    aa_a = all_metrics['A']['Average Accuracy (AA)']\n"
        "    aa_b = all_metrics['B']['Average Accuracy (AA)']\n"
        "    gap_raw = aa_b - aa_a\n"
        '    print(f"\\nA (post-only):  AA = {aa_a:.4f}")\n'
        '    print(f"B (trajectory): AA = {aa_b:.4f}")\n'
        '    print(f"Raw gap (B - A): {gap_raw:+.4f}")\n'
        "\n"
        "if 'A+' in all_metrics and 'B' in all_metrics:\n"
        "    aa_ap = all_metrics['A+']['Average Accuracy (AA)']\n"
        "    gap_matched = aa_b - aa_ap\n"
        '    print(f"\\nA+ (token-matched): AA = {aa_ap:.4f}")\n'
        '    print(f"Token-matched gap (B - A+): {gap_matched:+.4f}")\n'
        "\n"
        "    if gap_raw > 0:\n"
        "        explained = (1 - gap_matched / gap_raw) * 100\n"
        '        print(f"\\nToken budget explains {explained:.1f}% of the raw gap.")\n'
        '        print(f"Remaining gap: {gap_matched:+.4f}")\n'
        "        if gap_matched > 0:\n"
        '            print("=> Trajectory benefit BEYOND just more tokens.")\n'
        "        else:\n"
        '            print("=> Gap fully explained by token budget.")\n'
        "\n"
        "# Per-block comparison\n"
        "if 'A' in results and 'B' in results:\n"
        '    print(f"\\nPer-block final accuracy:")\n'
        "    acc_a = np.array(results['A']['eval_acc'])[-1]\n"
        "    acc_b = np.array(results['B']['eval_acc'])[-1]\n"
        "    for j in range(len(acc_a)):\n"
        "        diff = acc_b[j] - acc_a[j]\n"
        '        print(f"  D{j+1}: A={acc_a[j]:.1%}, B={acc_b[j]:.1%}, diff={diff:+.1%}")'
    ),
    md("## 7. Export"),
    code(
        "analysis = {\n"
        "    'metrics': {c: m for c, m in all_metrics.items()},\n"
        "    'conditions': list(results.keys()),\n"
        "}\n"
        "for cond, r in results.items():\n"
        "    analysis[f'eval_acc_{cond}'] = r['eval_acc']\n"
        "    analysis[f'zero_shot_{cond}'] = r.get('zero_shot', {})\n"
        "\n"
        "with open('analysis_results.json', 'w') as f:\n"
        "    json.dump(analysis, f, indent=2, default=str)\n"
        "\n"
        'print("Saved: analysis_results.json")\n'
        'print("\\nFiles for paper:")\n'
        'print("  final_results.png / .pdf")\n'
        'print("  analysis_results.json")'
    ),
]


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output: {OUTPUT_DIR}\n")
    write_nb("01_data_prep.ipynb", nb1_cells)
    write_nb("02_train_eval.ipynb", nb2_cells)
    write_nb("03_analysis.ipynb", nb3_cells)
    print("\nDone!")
