# PROJECT INFO DUMP

## Post-Only vs Trajectory Supervision for Continual Tool-Use Learning in LLMs

**Students:** Vishnu Vardhan Reddy B (`vbheemreddy@umass.edu`), Sagnik Chatterjee (`sagnikchatte@umass.edu`), Soumik Bhatta (`sbhatta@umass.edu`)
**Course:** CS 590NN — Neural Networks in AI and Neuroscience
**Instructor:** Prof. Hava Siegelmann
**University:** UMass Amherst
**Semester:** Spring 2026

---

## 1. The Big Idea (In Our Words)

When humans produce any form of output — writing, code, solutions, blog posts, answers — they go through an internal thought process. They reason, revise, reconsider, evaluate. But they only share the **final result**. The internet is made of these final results. The thought process behind them is never documented.

Modern LLMs are trained almost entirely on this **outcome-only data**. The models learn what good outputs look like, but not the process that produces them. Even reasoning models that generate intermediate `<think>` traces are producing **synthetic thought** — generated chains-of-reasoning that mimic process but aren't grounded in actual human cognitive steps. The training data is still the same: final human outputs from the internet, not the humans' actual thinking.

**The fundamental gap: we train on the products of thought, not the process of thought.**

There is a lack of data capturing real human internal reasoning — genuine, unaltered thought processes. We could theoretically capture these (think-aloud protocols, screen recordings, interaction logs), but this raises serious privacy concerns and scalability issues.

This project tests whether this gap actually matters for how models learn. Specifically: **does training on process-level data produce measurably different learning dynamics compared to outcome-only data?**

### Why This Matters Beyond Academia

- If process data helps, it implies we should invest in collecting it (ethically)
- Reasoning models need grounded traces, not just synthetic ones
- Current internet-scale training may be leaving significant learning signal on the table

---

## 2. Tool-Use Trajectories as the Proxy

We can't capture real human thought at scale. But **tool-use interactions** are a naturally occurring proxy for process data that already exists, without privacy concerns.

When a human (or agent) uses a tool, the full interaction is recorded:

```
1. GOAL        → User makes a request ("What's the weather in Boston?")
2. ACTION      → Agent calls a tool (WeatherAPI(city='Boston'))
3. OBSERVATION → Tool returns result ({"temp": 72, "condition": "sunny"})
4. SYNTHESIS   → Agent produces final response ("It's 72°F and sunny in Boston")
```

Steps 2 and 3 are **externalized reasoning** — intermediate steps that are normally invisible in outcome-only data. In a "post-only" world, you'd only see step 4. The thought process (deciding which tool to call, what parameters to pass, interpreting the result) is lost.

Tool-use datasets capture this full chain without any privacy issues, making them a **tractable, ethical testbed** for the process-vs-outcome hypothesis.

### Why Tool-Use Specifically (vs Other Process Data)?

| Process Data Type | Availability | Privacy Risk | Structured? | Feasible for Experiment? |
|---|---|---|---|---|
| Human think-aloud protocols | Very low | High | No | No |
| Screen recordings of work | Low | High | No | No |
| Code edit histories (git diffs) | Medium | Low | Semi | Maybe |
| Tool-use trajectories | High | Low | Yes | **Yes** |
| Math step-by-step solutions (PRM800K) | Medium | Low | Yes | Yes (but domain-specific) |

Tool-use wins because it's **structured, available, and domain-general**.

---

## 3. Experimental Design

### 3.1 The Two Core Conditions

**Condition A (Post-Only / Outcome-Only):**
- Strip all tool call and tool output tokens from the training data
- Train only on the final assistant response
- This represents the standard paradigm: models learning from finished outputs
- The model sees: `[User request] → [Final response]`

**Condition B (Trajectory / Process):**
- Keep the full trace in training data
- Train on: user request → tool calls → tool outputs → final response
- This represents process-level supervision
- The model sees: `[User request] → [Tool call] → [Tool output] → [Final response]`

### 3.2 What Makes This a Fair Comparison

Both conditions use:
- Same base model (Llama 3.1 8B Instruct)
- Same QLoRA configuration (r=32, alpha=64, 4-bit)
- Same sequential domain ordering
- Same optimizer, learning rate, scheduler
- Same random seeds
- Same evaluation protocol

**Critical fairness issue — token budget:**
Condition B has more tokens per example (because it includes tool call + tool output tokens). This means B sees more data per example. We handle this by:
1. Reporting performance as a function of **training tokens consumed** (not just epochs)
2. Potentially subsampling B so total token counts match A
3. Reporting both raw and token-normalized results

### 3.3 Condition C (Stretch Goal)

Trajectory + memory + replay + confidence gating. This is NOT the core contribution. If we have time:
- **Replay buffer**: DER-inspired rehearsal — mix past trajectories into current training
- **Retrieval memory**: RAG-style external memory of past successful tool interactions
- **Confidence gating**: Use model confidence to decide when to retrieve more memory or allocate extra compute

This would be presented as a "what if" exploratory section, not a main claim.

---

## 4. Why Continual Learning as the Evaluation Lens

### What It Is NOT
This project is **not primarily about solving catastrophic forgetting**. We are not claiming to have a new continual learning method.

### What It IS
Continual learning is the **stress test** — the evaluation setting that amplifies differences between training signals.

**Why this works:**
- In a single-domain fine-tuning setup, both A and B might perform similarly — the differences could be subtle
- Sequential domain shifts stress-test the robustness of what was learned
- If trajectory supervision creates more robust representations, it should show up as less forgetting and faster adaptation to new domains
- Continual learning gives us richer metrics than simple accuracy (BWT, FWT, forgetting curves, adaptation speed)

### Connection to Course Themes
This evaluation lens connects directly to Prof. Siegelmann's course:
- **Lifelong learning** — the "3rd wave" of AI that continues to adapt post-deployment (Lecture 3)
- **Memory systems** — external retrieval memory parallels biological memory consolidation (Hopfield memories, sequence memories)
- **Super-Turing adaptivity** — Siegelmann's foundational work on RNNs as Turing machines and adaptive systems
- **Neuromodulation for continual adaptivity** — confidence gating echoes neuromodulatory control of learning (March 23 lecture topic)
- The broader question of how **richer training signals** (closer to biological experience) affect learning and retention

### The Biological Parallel
Humans learn from experience streams (observation → action → feedback → memory update), not from reading final outputs. Our project tests a computational analog of this: does giving a model richer, process-level training signal change how it learns and retains knowledge over time?

---

## 5. Model Choice: Llama 3.1 8B Instruct

### Why We Switched from Mistral 7B v0.3

| Factor | Mistral 7B v0.3 | Llama 3.1 8B Instruct |
|---|---|---|
| Tool-use ability | Weakest of 7-8B class | Moderate (good baseline) |
| BFCL benchmark | Struggles with parallel calls | Decent; base for top tool-use models |
| Fine-tuning ecosystem | Good | Best (torchtune, Unsloth, Axolotl, HuggingFace PEFT) |
| Community support | Good | Largest |
| Proven as tool-use base | No | Yes — powers ToolACE-8B (91.4% BFCL) and xLAM-2-8b |

### Why Llama 3.1 8B Is the Right Choice for Our Experiment

We need a model with **moderate** tool-use ability:
- **Too weak** (Mistral): We'd be testing format learning + process data simultaneously — muddied signal
- **Too strong** (ToolACE-8B): Already near ceiling on tool-use, no room for our experiment to show differences
- **Just right** (Llama 3.1 8B Instruct): Understands tool-use basics but has clear room for improvement — isolates the process-vs-outcome question cleanly

### Model Details
- **HuggingFace ID:** `meta-llama/Llama-3.1-8B-Instruct`
- **Parameters:** ~8B
- **Context:** 128K tokens
- **License:** Llama 3.1 Community License
- **Architecture:** Decoder-only transformer
- **Training:** Instruction-tuned with RLHF

### Other Models We Considered

| Model | BFCL Score | Why Not |
|---|---|---|
| ToolACE-8B | 91.4% (v1) | Too specialized — ceiling effects |
| xLAM-2-8b-fc-r | 72.8% (v3, beats GPT-4o) | Already fine-tuned for tool-use, not a fair base |
| Qwen3-8B | F1 0.933 | Very strong out-of-box, might leave no room |
| Qwen 2.5 7B | Strong | Good alternative, but Llama has larger ecosystem |
| Llama-3-Groq-8B-Tool-Use | ~89% (v1) | Already specialized |

---

## 6. Dataset: API-Bank

### Why API-Bank

- **Compact**: 1,888 training dialogues — hours not days to train
- **Structured**: Clear action/observation format that maps perfectly to our A/B comparison
- **Multi-domain**: ~1,000 domains, 2,138 APIs — enough variety for continual learning blocks
- **Runnable**: Ships with evaluation tools and parseable format
- **Public**: MIT license, available on HuggingFace (`liminghao1630/API-Bank`)

### Dataset Structure

The data comes in three levels:
- `lv1-train.json` — single-turn, single-tool dialogues
- `lv2-train.json` — multi-turn dialogues
- `lv3-train.json` — multi-tool dialogues

Each entry has:
```json
{
  "instruction": "System prompt describing available APIs",
  "input": "Full dialogue with user messages, AI messages, API calls, API responses",
  "output": "The target output (could be an API call or final response)"
}
```

### Continual Learning Stream Design

We group entries by API name (the primary tool being called), filter to APIs with >= 10 entries, then split into **4 sequential domain blocks**:

```
D1 (APIs a, b, c, ...) → D2 (APIs d, e, f, ...) → D3 (APIs g, h, i, ...) → D4 (APIs j, k, l, ...)
```

Each block contains entries from a distinct set of API families. The model trains on D1, then D2, then D3, then D4 — simulating a stream of new tool domains arriving over time.

After training on each block, we evaluate on **all** blocks (current + all previous) to measure both adaptation and forgetting.

### Formatting for Conditions

**Condition A format (post-only):**
```
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

You are a helpful assistant.

[Dialogue with API-Request and API-Response lines STRIPPED]<|eot_id|><|start_header_id|>assistant<|end_header_id|>

[Final response only]<|eot_id|>
```

**Condition B format (trajectory):**
```
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

You are a helpful assistant that can use tools. When you need to call an API, use the format: [ApiName(param1='value1', param2='value2')]. After receiving the API response, use it to formulate your answer.

[Full dialogue INCLUDING API-Request and API-Response lines]<|eot_id|><|start_header_id|>assistant<|end_header_id|>

[Full output including any tool calls]<|eot_id|>
```

**Note:** The current notebook uses Mistral's `[INST]...[/INST]` format. This needs to be updated to Llama 3.1's chat template when we switch models.

---

## 7. Training Setup

### QLoRA Configuration
- **Quantization:** 4-bit NormalFloat (nf4), double quantization
- **Compute dtype:** bfloat16 (native on H100)
- **LoRA rank (r):** 32
- **LoRA alpha:** 64 (alpha/r = 2)
- **Target modules:** q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj (all attention + MLP projections)
- **LoRA dropout:** 0.05
- **Bias:** none

### Training Hyperparameters
- **Optimizer:** paged_adamw_8bit
- **Learning rate:** 2e-4
- **LR scheduler:** cosine with warmup
- **Warmup ratio:** 0.1
- **Batch size:** 16 (H100 can handle this easily)
- **Gradient accumulation:** 1
- **Epochs per block:** 3
- **Max sequence length:** 1024 tokens
- **Precision:** bf16
- **Attention:** Flash Attention 2
- **Gradient checkpointing:** Off (H100 has enough VRAM)

### Hardware
- **GPU:** NVIDIA H100 80GB
- **Expected VRAM usage:** ~12-16GB for QLoRA (well within 80GB)
- **Expected training time per block:** Minutes to low hours
- **Total experiment time (A + B):** A few hours

### Reproducibility
- **Seeds:** SEED = 42 (plan to run 3 seeds: 42, 123, 456)
- All random generators seeded: Python random, NumPy, PyTorch, CUDA
- Same domain block ordering across conditions
- Results saved to JSON

---

## 8. Evaluation

### 8.1 Evaluation Matrix Structure

After training on block $i$, we evaluate on all blocks $j \in \{1, 2, ..., N\}$. This produces an $N \times N$ matrix where:
- `eval[i][j]` = performance on block $j$ after training on blocks $1$ through $i$
- **Diagonal** = performance on current block (should be high)
- **Below diagonal** = performance on past blocks (measures forgetting)
- **Above diagonal** = performance on future blocks (measures forward transfer)

### 8.2 Metrics

#### Primary Metrics (Must Have)

**Adaptation Speed:**
- Time-to-threshold: gradient steps needed to reach X% accuracy on new domain
- Area Under Learning Curve (AULC): total performance accumulated during learning

**Forgetting:**
- **Backward Transfer (BWT):** `(1/(N-1)) * Σ (acc[N,j] - acc[j,j])` for j < N
  - Negative = forgetting, Positive = backward improvement
- **Average Forgetting:** `(1/(N-1)) * Σ (max_acc[j] - final_acc[j])` for j < N
  - Always >= 0, higher = more forgetting

**Forward Transfer (FWT):**
- `(1/(N-1)) * Σ acc[j-1, j]` for j > 1
- Performance on block j before training on it

**Average Accuracy (AA):**
- Mean accuracy across all blocks after all training is done

**Task-Level:**
- **API name accuracy:** Does the model generate the correct API name?
- **Full accuracy:** Correct API name + at least one correct parameter value

#### Secondary Metrics (If Time Permits)

**Calibration:**
- **ECE (Expected Calibration Error):** Bin confidences, average |accuracy - confidence| across bins
- **Brier Score:** Mean squared error between predicted probability and actual binary outcome

### 8.3 Evaluation Methods

**Perplexity/Loss evaluation:**
- Compute cross-entropy loss on held-out formatted text from each block
- Fast, gives continuous signal

**Generation evaluation:**
- Give the model the input (without the expected output)
- Generate a response
- Check if generated text contains correct API name (string match)
- Check if generated text contains correct parameter values
- Slower but more meaningful — tests actual capability

### 8.4 Visualization Plan

6-panel figure:
1. Eval loss heatmap for Condition A
2. Eval loss heatmap for Condition B
3. Forgetting curves (accuracy per block over training stages)
4. Final accuracy bar chart (A vs B, name + full accuracy)
5. Perplexity trajectories per block over time
6. CL metrics comparison bar chart (AA, BWT, FWT, Avg Forgetting)

---

## 9. What We Expect to Find

### Hypothesis 1: Trajectory Adapts Faster
- Condition B should reach performance thresholds on new domains in fewer steps than A
- Rationale: Full trajectories provide richer signal — the model learns not just what to output but how to get there (which tool to call, how to interpret results)

### Hypothesis 2: Trajectory Forgets Less
- Condition B should show less negative BWT and lower Average Forgetting than A
- Rationale: Process data creates more robust, transferable representations. The model learns patterns (observe → act → interpret) that generalize across domains, rather than memorizing domain-specific outputs

### Hypothesis 3: CL Metrics Reveal Differences Static Evaluation Misses
- A single-domain fine-tune might show similar final accuracy for A and B
- But sequential training amplifies the gap: B's more robust representations should degrade less under domain shifts

### If Results Go Against Expectations
- If A and B are similar: the gap may not matter for this scale/setting (still publishable as a negative result)
- If A is actually better: trajectory data might be noisy or confusing for the model (interesting finding about token efficiency)
- If both catastrophically forget equally: the supervision signal doesn't affect representation robustness (challenges the hypothesis)

---

## 10. Key Risks and Confounders

### Token Budget Confounder
Trajectory (B) has more tokens per example than post-only (A). If B performs better, is it because of richer signal or just more data? **Must control for this.**

### Synthetic Data Bias
API-Bank dialogues are somewhat synthetic. The "process data" here is structured API calls, not messy human reasoning. This is a cleaner but less realistic proxy.

### Evaluation Brittleness
Tool-call evaluation can be fragile — minor formatting differences can cause false negatives. Need robust parsing with normalization.

### Spurious Forgetting
Some performance drops in continual learning may reflect instruction alignment drift, not actual knowledge loss (Zheng et al., 2025). Need to interpret forgetting metrics carefully.

### Contamination
If Llama 3.1 has seen API-Bank-like data during pretraining, differences between A and B might compress. Hard to fully control for this.

### Small Scale
4 domain blocks is a limited continual learning stream. Results may not generalize to longer streams or more diverse domains.

---

## 11. Scope and Priorities

### Core (Must Have)
- [ ] Condition A vs B comparison on API-Bank with Llama 3.1 8B
- [ ] 4 sequential domain blocks
- [ ] Full evaluation matrix (loss, perplexity, generation accuracy)
- [ ] CL metrics: AA, BWT, FWT, Average Forgetting
- [ ] Multiple random seeds (3 if compute permits)
- [ ] Token budget analysis (report performance per token)
- [ ] 6-panel visualization
- [ ] Results saved to JSON

### Secondary (If Time Permits)
- [ ] Calibration analysis (ECE, Brier score)
- [ ] More domain blocks (6-8 instead of 4)
- [ ] Adaptation speed curves (time-to-threshold, AULC)
- [ ] Condition C (trajectory + replay + retrieval + confidence gating)
- [ ] Ablation within C (no replay, no memory, no gating)

### Future Work (Out of Scope)
- [ ] ToolBench replication
- [ ] Scaling to larger models (13B, 70B)
- [ ] Multiple datasets
- [ ] Real human process data comparison
- [ ] Condition C full implementation and analysis

---

## 12. Deadlines

| Deliverable | Date | Status |
|---|---|---|
| Project groups determined | Feb 23 | Done (solo, with permission) |
| Proposal slides (1-3 slides) | Mar 1, 11:59PM | Done |
| Proposal presentation (3 min) | Mar 2 | Done |
| Proposal writeup (1 page) | Mar 9, 11:59PM | Done |
| **Partial results video (3-5 min)** | **Mar 30, 11:59PM** | **TODO — need A vs B results** |
| Final presentation (5-10 min) | Apr 27 or May 4 | TODO |
| Final report (NeurIPS format, 5-9 pages) | May 6, 11:59PM | TODO |

### Critical Warning from Syllabus
> "Hallucinations or other large language model (LLM) signs in writing the paper will lead to a 0 on the final project."

The final report must be written in your own voice. LLMs can help with ideation but you own every word.

---

## 13. Paper Structure (Planned)

NeurIPS format, 5-9 pages (excluding references).

1. **Introduction** — The process-vs-outcome gap, why it matters, tool-use as proxy
2. **Related Work** — Continual learning in LLMs (TRACE), process supervision (PRM800K/Let's Verify Step by Step), tool-use datasets (API-Bank, ToolBench, Toolformer), memory/retrieval (RAG, RETRO)
3. **Method** — Conditions A and B, dataset construction, streaming protocol, fairness controls
4. **Experimental Setup** — Model, QLoRA config, hyperparameters, evaluation metrics
5. **Results** — A vs B comparison: adaptation speed, forgetting, forward transfer, accuracy
6. **Analysis** — Token budget analysis, what trajectory data teaches, failure cases
7. **Discussion** — Implications for process data collection, limitations, connection to course themes
8. **Conclusion & Future Work** — Condition C, scaling, real human process data

---

## 14. Codebase Status

### Current Notebook: `small_experiment.ipynb`
- **Working:** Data loading, API name extraction, domain block construction, formatting functions (A and B), QLoRA model loading, training loop, evaluation (loss + generation), CL metrics computation, visualization
- **Needs Update:** Switch from Mistral to Llama 3.1 8B Instruct (model name, chat template, formatting functions)
- **Not Yet Implemented:** Multiple seeds, token budget equalization, calibration metrics, Condition C

### Files in Project Directory
```
Final Project/
├── overview.md                  — High-level project overview (updated)
├── overview.tex                 — Original LaTeX overview
├── PROJECT_INFO.md              — This file (detailed info dump)
├── small_experiment.ipynb       — Main experiment notebook
├── research/
│   └── deep-research-report.md  — Comprehensive literature review and project design
└── CS_590NN_690NN_Final_Project_Template/
    └── proposal.tex             — NeurIPS-format proposal
```

---

## 15. Key References

### Must-Cite in Paper

| Paper | Why |
|---|---|
| TRACE (Wang et al., 2023) | Primary CL benchmark showing catastrophic forgetting in LLMs |
| Let's Verify Step by Step (Lightman et al., 2023) | Cleanest process-vs-outcome supervision result |
| API-Bank (Li et al., 2023) | Our primary dataset |
| QLoRA (Dettmers et al., 2023) | Our training method |
| LoRA (Hu et al., 2021) | Foundation for QLoRA |
| DER (Buzzega et al., 2020) | Replay baseline (if we do Condition C) |
| RAG (Lewis et al., 2020) | Memory augmentation concept |

### Good to Cite

| Paper | Why |
|---|---|
| ToolLLM / ToolBench (Qin et al., 2023) | Larger tool-use dataset, positions our work |
| Toolformer (Schick et al., 2023) | Self-supervised tool learning |
| Spurious Forgetting (Zheng et al., 2025) | Nuanced forgetting interpretation |
| On Calibration of LLMs (Zhang et al., 2026) | Capability calibration concept |
| ECE (Guo et al., 2017) | Calibration metric definition |

---

## 16. Open Questions

1. **How many domain blocks?** Currently 4. Should we increase to 6-8 for more convincing CL results?
2. **Epoch count per block?** Currently 3. Is this enough? Too much (overfitting)?
3. **How to handle token budget fairness?** Report both raw and per-token? Or subsample B?
4. **Evaluation generation — beam search or greedy?** Currently greedy (do_sample=False). Should we use beam search for more reliable generation eval?
5. **How to present the "process data" narrative without it sounding like a solved problem?** Need to position this as "a first controlled test" not "we solved the gap."
6. **Should we include a "no fine-tuning" baseline?** Evaluate the base Llama 3.1 8B on all blocks before any training — shows what the model can do zero-shot.

---

## 17. What We Discussed and Decided (Decision Log)

| Decision | Rationale |
|---|---|
| Core thesis is process-vs-outcome data gap | This is what we actually care about; it's the novel framing |
| Continual learning is the evaluation lens, not the claim | We're not proposing a new CL method; CL amplifies differences |
| A vs B is the heart of the paper | Keep it focused; Condition C is stretch |
| Switched from Mistral 7B to Llama 3.1 8B | Mistral is weakest for tool-use; Llama is moderate (clean test), largest ecosystem, proven base |
| Tool-use trajectories are the proxy for human process data | Structured, available, ethical, domain-general |
| API-Bank as primary dataset | Compact, runnable, multi-domain, public |
| Token budget must be controlled | Otherwise B's advantage could just be "more data" |
| Multiple seeds for rigor | 3 seeds with bootstrap CIs if compute permits |
| Calibration is secondary | Nice to have but not core contribution |
