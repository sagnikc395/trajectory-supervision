# Deep Research Report: Process and Trajectory Signals vs Post-Only Text for Continual Adaptation in LLMs

## Executive summary

- **Evidence:** Continual fine-tuning of aligned LLMs can severely degrade prior capabilities: the TRACE benchmark reports large drops in general ability and instruction-following after sequential training, e.g., a reported GSM8K accuracy drop from **43.14% → 2.12%** for Llama2-chat 13B after training on TRACE tasks. `https://openreview.net/forum?id=3qa4YLkcEw` citeturn25view0  
- **Evidence:** TRACE also reports that adding *reasoning paths / meta-rationales during training* (Reasoning-augmented Continual Learning, RCL) can **reduce catastrophic forgetting and speed convergence** on new tasks. `https://openreview.net/forum?id=xelrLobW0n` citeturn36search5  
- **Evidence:** “Let’s Verify Step by Step” directly operationalizes *process vs outcome supervision* and finds **process supervision can outperform outcome supervision** on MATH; it releases **PRM800K with 800,000 step-level human labels**. `https://arxiv.org/abs/2305.20050` citeturn24search3  
- **Evidence:** Tool-use work provides strong, practical “trajectory” analogs: ToolLLM introduces ToolBench and states it is **constructed automatically using ChatGPT**, including **16,464 real-world REST APIs** and tool-use solution paths; it also introduces an automatic evaluator (ToolEval). `https://arxiv.org/abs/2307.16789` citeturn32view0  
- **Evidence:** Memory / retrieval is a credible mechanism for *rapid updates* without fully rewriting weights: RAG formalizes combining parametric + **non-parametric memory** (retrieved Wikipedia index). `https://arxiv.org/abs/2005.11401` citeturn21search0 RETRO shows large-scale retrieval during modeling/training. `https://arxiv.org/abs/2112.04426` citeturn4search0 Memorizing Transformers show **inference-time memorization** can improve across domains and support “learning” new definitions at test time. `https://arxiv.org/abs/2203.08913` citeturn4search2  
- **Evidence:** Calibration and uncertainty are measurable and should be part of the hypothesis test: a 2026 paper distinguishes *response calibration* vs *capability calibration* and reports capability-calibrated confidence can improve **pass@k prediction** and **inference budget allocation**. `https://arxiv.org/abs/2602.13540` citeturn27view0  
- **Evidence:** Distribution shift and robustness have mature benchmark infrastructure: WILDS compiles real-world distribution shifts. `https://arxiv.org/abs/2012.07421` citeturn7search0 BOSS provides an NLP OOD suite (5 tasks, 20 datasets) and releases code. `https://arxiv.org/abs/2306.04618` citeturn10search3turn37search3  
- **Inference (project framing):** The cleanest semester-scale test of your hypothesis is a **streaming tool-use setting** where (A) training sees only final “assistant posts,” (B) training sees *full trajectories* (calls + observations + intermediate text), and (C) adds *memory + replay + confidence gating*; API-Bank is a compact, runnable starting point and ToolBench is a scalable extension. `https://arxiv.org/abs/2304.08244` citeturn29search1 `https://arxiv.org/abs/2307.16789` citeturn32view0  
- **Inference (feasibility):** QLoRA-style 4-bit LoRA greatly lowers GPU memory barriers (e.g., QLoRA reports single-GPU feasibility up to 65B on 48GB; HF notes 33B fine-tuning on 24GB is feasible with 4-bit). `https://arxiv.org/abs/2305.14314` citeturn18search0 `https://huggingface.co/blog/4bit-transformers-bitsandbytes` citeturn18search3  
- **Evidence (key confounder):** Benchmark contamination is a real risk; Mind2Web explicitly ships encrypted test splits and warns against redistribution to reduce contamination risk, and includes canary strings. `https://github.com/OSU-NLP-Group/Mind2Web` citeturn13view0turn31search2  

## Evidence table

| Claim | Source (URL) | Year | Evidence quality | Reproducibility (code/data availability) |
|---|---:|---:|---|---|
| TRACE reports large capability regression after sequential training; example: GSM8K accuracy **43.14% → 2.12%** for Llama2-chat 13B after training on TRACE. | `https://openreview.net/forum?id=3qa4YLkcEw` citeturn25view0 | 2024 | High | Medium (benchmark + paper public; full reproduction depends on model access + settings) |
| TRACE states Reasoning-augmented Continual Learning (RCL) integrates task cues with meta-rationales and **reduces catastrophic forgetting** while **expediting convergence**. | `https://openreview.net/forum?id=xelrLobW0n` citeturn36search5 | 2024 | Medium–High | Medium (paper public; full recipe details in manuscript) |
| ToolLLM introduces ToolBench and states it is **constructed automatically using ChatGPT**, with **16,464 REST APIs** from RapidAPI and annotated solution paths; introduces ToolEval. | `https://arxiv.org/abs/2307.16789` citeturn32view0 | 2023 | High | Medium–High (paper public; dataset and tooling widely mirrored) |
| ToolBench repository reports dataset stats (3,451 tools; 16,464 APIs; 126,486 instances; 469,585 real API calls) and states distribution under Apache 2.0 (research/education purpose). | `https://github.com/OpenBMB/ToolBench` citeturn12view1turn24search2 | 2023–2024 | Medium | High (repo + statistics public; execution requires setup) |
| API-Bank defines a runnable evaluation system (73 API tools), annotated dialogues (314) and training set (1,888 dialogues from 2,138 APIs across 1,000 domains). | `https://arxiv.org/abs/2304.08244` citeturn29search1 | 2023 | High | Medium–High (paper public; data mirrored; eval code exists) |
| API-Bank code and data are stated as publicly available at DAMO-ConvAI’s api-bank folder (per paper PDF snippet). | `https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank` citeturn30search10turn30search0 | 2023 | High | Medium (public repo; some issues suggest evaluation friction) |
| PRM800K provides **800,000 step-level human labels** for MATH solutions and is released with “Let’s Verify Step by Step.” | `https://arxiv.org/abs/2305.20050` citeturn24search3 | 2023 | High | Medium (paper public; dataset public; training full verifier may be heavier) |
| PRM800K repository states MIT license and describes dataset structure and release contents. | `https://github.com/openai/prm800k` citeturn12view2turn24search12 | 2023 | High | High (repo + data available; requires Git LFS in repo) |
| Mind2Web provides web-agent trajectories at scale and explicitly restricts test redistribution to reduce contamination; dataset licensed CC BY 4.0 (dataset) and code MIT. | `https://github.com/OSU-NLP-Group/Mind2Web` citeturn13view0 | 2023–2025 | High | Medium–High (train data public; test gated/encrypted) |
| WebShop provides an interactive web environment with **1.18M products**, **12,087 instructions**, and **1,600+ human demonstrations**; reports best model success **29%** vs human expert **59%**. | `https://arxiv.org/abs/2207.01206` citeturn24search1 | 2022 | High | High (paper + code public; environment setup required) |
| WebShop code repository has a standard permissive license file (MIT-style language on GitHub license page). | `https://github.com/princeton-nlp/WebShop/blob/master/LICENSE.md` citeturn37search0 | 2022 | Medium | High |
| RAG formalizes retrieval-augmented generation: parametric seq2seq + **non-parametric dense index (Wikipedia)** used for generation and updateability via index changes. | `https://arxiv.org/abs/2005.11401` citeturn21search0 | 2020 | High | Medium–High (original code varies by implementation; concept widely replicated) |
| RETRO reports retrieval from a large corpus (trillions of tokens) and claims strong LM performance with fewer parameters via retrieval conditioning. | `https://arxiv.org/abs/2112.04426` citeturn4search0 | 2021 | High | Medium (full-scale retrieval DB is heavy; the paper is primary) |
| Memorizing Transformers proposes inference-time memorization via approximate kNN lookup over representations and reports improvements across domains (web text, math, code). | `https://arxiv.org/abs/2203.08913` citeturn4search2 | 2022 | High | Medium (implementation exists; scaling and infra matter) |
| Toolformer proposes self-supervised training where LMs learn **when/how to call tools** and integrate results, improving downstream performance without sacrificing core LM ability. | `https://arxiv.org/abs/2302.04761` citeturn23search1 | 2023 | High | Medium (paper is primary; reproducing tool setup varies) |
| TRACE benchmark codebase is licensed Apache 2.0. | `https://github.com/BeyonderXX/TRACE/blob/master/LICENSE` citeturn34search0 | 2023–2024 | Medium | High |
| WILDS provides a benchmark suite of distribution shifts “in the wild” and reports that standard training yields substantially lower OOD than ID performance. | `https://arxiv.org/abs/2012.07421` citeturn7search0 | 2020 | High | High (data loaders + evaluators released) |
| HELM is an LM evaluation suite that explicitly includes **calibration and robustness** among measured metrics. | `https://arxiv.org/abs/2211.09110` citeturn7search1turn7search5 | 2022 | High | Medium–High (framework public; full reproduction depends on model access) |
| BOSS introduces an NLP OOD benchmark suite (5 tasks, 20 datasets); code is public. | `https://arxiv.org/abs/2306.04618` citeturn10search3turn37search3 | 2023 | High | Medium (some constituent datasets require forms) |
| Dark Experience Replay (DER) is a strong replay baseline combining rehearsal with knowledge distillation, targeted at general continual learning streams. | `https://arxiv.org/abs/2004.07211` citeturn25view3turn8search0 | 2020 | High | High (paper + standard implementations exist) |
| MIGU proposes rehearsal-free continual learning for LMs by updating parameters with large output magnitudes; reports an example **15.2%** average accuracy improvement on a 15-task benchmark; code linked. | `https://arxiv.org/abs/2406.17245` citeturn33search6turn33search3 | 2024 | Medium | Medium (repo exists but notes “under construction”) |
| O-LoRA proposes orthogonal low-rank adaptation for continual learning in language models, aiming to reduce interference without replay storage. | `https://arxiv.org/abs/2310.14152` citeturn36search0turn36search16 | 2023 | Medium–High | Medium (paper public; implementations vary) |
| Spurious Forgetting argues some continual-learning performance drops in LLMs may reflect **task alignment loss rather than true knowledge loss**; proposes freezing strategy improvements. | `https://arxiv.org/abs/2501.13453` citeturn36search3turn20view1 | 2025 | Medium–High | Medium (ICLR paper page public; full code may vary) |
| QLoRA reports 4-bit quantized finetuning with LoRA adapters enabling much lower memory usage (up to finetuning 65B on a single 48GB GPU). | `https://arxiv.org/abs/2305.14314` citeturn18search0 | 2023 | High | High (paper + code released) |
| LoRA proposes low-rank adapters to reduce trainable parameters and GPU memory compared to full fine-tuning. | `https://arxiv.org/abs/2106.09685` citeturn18search1 | 2021 | High | High (paper + repo released) |
| A 2026 calibration paper distinguishes response-level vs capability-level calibration and claims capability-calibrated confidence improves pass@k prediction and budget allocation. | `https://arxiv.org/abs/2602.13540` citeturn27view0 | 2026 | Medium–High | Medium (paper public; code link indicated in PDF) |
| ECE is a standard calibration metric; one derivation is binning confidences and averaging |acc − conf| across bins (commonly attributed to Guo et al.). | `https://arxiv.org/abs/1706.04599` citeturn28search0 | 2017 | High | High |
| The Brier score is a classic strictly proper scoring rule for probability forecasts. | `https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml` citeturn28search1 | 1950 | High | High |

## Dataset shortlist table

| Dataset | Modality | Why it fits the “experience stream vs post-only” hypothesis | License/access constraints |
|---|---|---|---|
| API-Bank | Text (multi-turn tool-use dialogues + API calls + tool outputs) | Compact, runnable tool-use benchmark with explicit **action/observation** structure; supports constructing (A) “final response only” vs (B) full tool trajectories. `https://arxiv.org/abs/2304.08244` citeturn29search1 | MIT (dataset card); code/data public in DAMO-ConvAI. `https://huggingface.co/datasets/liminghao1630/API-Bank` citeturn11view0 `https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/api-bank` citeturn30search10 |
| ToolBench | Text (instructions + multi-tool reasoning traces + tool calls) | Large-scale trajectory supervision for tool-use; natural for streaming-by-tool-category and replay selection; supports realistic “trajectory/process inputs.” `https://arxiv.org/abs/2307.16789` citeturn32view0 | Apache-2.0; published dataset stats in repo. `https://github.com/OpenBMB/ToolBench` citeturn12view1turn24search2 |
| PRM800K | Text (step-level reasoning + step correctness labels) | Strong “process signal” dataset (per-step labels). Usable for a controlled A/B where “post-only” uses final answers while “process” uses step-level supervision and/or verifier training. `https://arxiv.org/abs/2305.20050` citeturn24search3 | MIT license and public repo; requires Git LFS if cloning full labels. `https://github.com/openai/prm800k` citeturn12view2 |
| TRACE | Text (8-task continual-learning benchmark + CL metrics and deltas) | Purpose-built benchmark to measure adaptation/forgetting and broader ability regression; useful as an evaluation harness even if training is on other streams. `https://arxiv.org/abs/2310.06762` citeturn36search1 | Apache-2.0 code license. `https://github.com/BeyonderXX/TRACE/blob/master/LICENSE` citeturn34search0 |
| Mind2Web | Text + partial web state (HTML) + action sequences | Realistic web trajectories; strong “experience stream” proxy with explicit anti-contamination practices; can be used in smaller-scale imitation settings. `https://github.com/OSU-NLP-Group/Mind2Web` citeturn13view0 | Dataset CC BY 4.0; test split encrypted, and authors request **no redistribution** of unzipped test files. `https://github.com/OSU-NLP-Group/Mind2Web` citeturn13view0 |
| WebShop | Interactive environment + text observations/actions + demos | High-signal web interaction trajectories with reported difficulty gap (models 29% vs humans 59%); good for trajectory learning vs post-only baselines. `https://arxiv.org/abs/2207.01206` citeturn24search1 | Code is public; license file is present (MIT-style). `https://github.com/princeton-nlp/WebShop` citeturn37search4 `https://github.com/princeton-nlp/WebShop/blob/master/LICENSE.md` citeturn37search0 |
| SWE-bench | Code + tests + issue descriptions (chronological by repo commits/issues) | Real “continual” proxy: software changes over time; can define streams by repo chronology and measure forgetting vs new issue adaptation. `https://arxiv.org/abs/2310.06770` citeturn17search1 | Repository indicates MIT license. `https://github.com/SWE-bench/SWE-bench` citeturn37search5 |
| SWE-Bench-CL | Code + tests + chronological task streams | Explicit continual-learning reformulation of SWE-bench style tasks to measure *accumulated experience* and catastrophic forgetting in coding agents. `https://arxiv.org/abs/2507.00014` citeturn37search14 | Code/data stated publicly available; confirm license in repo before use. `https://github.com/thomasjoshi/agents-never-forget/` citeturn17search2turn37search2 |

## Final recommended project

### Problem statement

Test the hypothesis: **Models trained only on “post-only” final outputs adapt more slowly and forget more than models trained with trajectory/process signals (observations, intermediate steps, feedback, memory updates)**, using a controlled **streaming tool-use** setting.

Concretely, build a continual-learning stream over *tool-use tasks* (by domain/tool family) and compare:

- **A (post-only baseline):** train only on final assistant responses (no explicit tool-call or observation tokens).
- **B (trajectory/process):** train on full trajectories (tool calls + tool outputs + intermediate reasoning text where present).
- **C (trajectory + memory + replay + confidence gating):** augment B with retrieval memory, replay selection, and calibrated confidence-based gating (when to query memory, when to replay, how much inference compute to allocate).

API-Bank provides a runnable, compact starting point (73 tools; 314 annotated dialogues; 1,888 training dialogues; 2,138 APIs across 1,000 domains). `https://arxiv.org/abs/2304.08244` citeturn29search1 ToolBench is the large-scale follow-on for stress testing (16,464 APIs; 126,486 instances; tool reasoning traces). `https://arxiv.org/abs/2307.16789` citeturn32view0  

### Three feasible designs and ablations

**Design A/B/C on API-Bank (recommended)**  
- **What you measure:** next-step API-call accuracy, end-to-end dialogue success, adaptation speed across sequential domain blocks, and forgetting on earlier domains.  
- **Why it’s feasible:** API-Bank is much smaller than ToolBench and ships runnable evaluation tools. `https://arxiv.org/abs/2304.08244` citeturn29search1  
- **Core ablations:** remove tool outputs vs include; remove replay vs add replay; remove confidence gating vs add.

**Design A/B/C on ToolBench (scalable extension)**  
- **What you measure:** tool selection + argument correctness + success on unseen APIs, using ToolBench/ToolEval framing. `https://arxiv.org/abs/2307.16789` citeturn32view0  
- **Why it’s feasible:** dataset is open and Apache-2.0, but it is larger and infra heavier. `https://github.com/OpenBMB/ToolBench` citeturn12view1  
- **Risk:** higher engineering burden (tool simulation / stable server), and more training time.

**Design A/B/C on WebShop (trajectory learning in an interactive environment)**  
- **What you measure:** success rate vs trajectories, and adaptation in new product categories or instruction distributions. WebShop reports 1,600+ demonstrations and a large gap between model and human performance, suggesting room for improvements via better trajectory training. `https://arxiv.org/abs/2207.01206` citeturn24search1  
- **Risk:** environment setup + evaluation loops can dominate the semester.

### Recommended choice

Choose **API-Bank Design A/B/C** first, and optionally include a **ToolBench subset** as a stretch goal.

This aligns tightly with your hypothesis because tool-use naturally creates “trajectory” data: **(instruction → action/tool-call → observation/tool-output → updated response)**, unlike post-only web text which lacks explicit observation and action steps. Tool-use also enables clean adaptation/forgetting measurement under sequential domain shifts. `https://arxiv.org/abs/2304.08244` citeturn29search1  

### Model stack

- **Base model (suggested):** an open-weight 7–8B instruction-tuned model (e.g., Mistral 7B or Llama 3.1 8B) for strong baseline capability on modest hardware. Mistral 7B is released under Apache 2.0 per its paper. `https://arxiv.org/abs/2310.06825` citeturn19search1 Llama 3.1 8B is distributed under the Llama 3.1 community license. `https://huggingface.co/meta-llama/Llama-3.1-8B` citeturn19search0  
- **Training method:** QLoRA (4-bit base + LoRA adapters) to keep costs manageable. QLoRA reports single-GPU feasibility at much larger scales (up to 65B on 48GB). `https://arxiv.org/abs/2305.14314` citeturn18search0  
- **Memory module (C condition):** vector-store retrieval of past successful (state, tool-call, tool-output, outcome) tuples (conceptually aligned with retrieval-augmented LMs like RAG/RETRO and memory systems like Memorizing Transformers). `https://arxiv.org/abs/2005.11401` citeturn21search0 `https://arxiv.org/abs/2112.04426` citeturn4search0 `https://arxiv.org/abs/2203.08913` citeturn4search2  
- **Replay module (C condition):** rehearsal buffer + sampling schedule (inspired by strong replay baselines like Dark Experience Replay; adapted to language trajectories). `https://arxiv.org/abs/2004.07211` citeturn25view3  
- **Confidence / gating module (C condition):** implement both (i) response-level confidence (standard ECE/Brier style) and (ii) capability-level “how likely can the model solve this query overall,” matching the 2026 capability calibration framing. `https://arxiv.org/abs/2602.13540` citeturn27view0  

### Training objective

Define a streaming sequence of domains/tools \[D1, D2, …, DT\], where each Dt is a batch of API-Bank dialogues constrained to a subset of domains/APIs.

- **A (post-only):** supervised fine-tuning on final assistant text only (strip tool-call lines and tool outputs). *Objective:* next-token LM loss over final outputs.  
- **B (trajectory/process):** supervised fine-tuning on interleaved trace tokens: conversation → API-Request → tool JSON output → assistant response. *Objective:* next-token LM loss over the full trajectory, so the model learns tool invocation *and* response conditioning.  
- **C (trajectory + memory + replay + gating):** same as B, plus:
  - **Replay:** mix a small percentage of replayed past trajectories per step (DER-style rehearsal principle). `https://arxiv.org/abs/2004.07211` citeturn25view3  
  - **Memory retrieval:** during training and inference, prepend retrieved “similar past episodes” (kNN-LM / RAG-style non-parametric memory idea). `https://arxiv.org/abs/2005.11401` citeturn21search0  
  - **Confidence gating:** if confidence is low, either (i) retrieve more memories, (ii) allocate more inference samples, or (iii) trigger replay-heavy fine-tuning step; this connects to capability calibration’s use in inference budget allocation. `https://arxiv.org/abs/2602.13540` citeturn27view0  

### Ablation matrix

| Condition | Post-only outputs | Full tool trajectory tokens | Retrieval memory at inference/train | Replay buffer | Confidence gating |
|---|---:|---:|---:|---:|---:|
| A | ✅ | ❌ | ❌ | ❌ | ❌ |
| B | ❌ | ✅ | ❌ | ❌ | ❌ |
| C | ❌ | ✅ | ✅ | ✅ | ✅ |

**Fairness control (important):** keep the same *token budget per new task* across A/B/C by either (i) subsampling B/C so total training tokens match A, or (ii) reporting results as a function of “training tokens consumed” rather than epochs. This is an *inference to reduce confounding*, motivated by TRACE’s demonstration that training recipe choices can shift both target-task fit and general ability regression. `https://openreview.net/forum?id=3qa4YLkcEw` citeturn25view0  

### Evaluation plan

**Adaptation speed**
- Metric: **time-to-threshold** (number of gradient steps or number of examples needed to reach X% API-call correctness on the current domain).  
- Metric: **area under the learning curve (AULC)** for the new domain over the first N updates.  
These are standard sample-efficiency style measurements (defined by you); report with bootstrap CIs. *(Inference: these are practical operationalizations; the benchmarks provide the streams, but you define “speed” explicitly.)*

**Forgetting / catastrophic forgetting**
- Use **Backward Transfer (BWT)** / forgetting-style evaluation consistent with continual learning practice and explicitly used in TRACE discussions. `https://arxiv.org/abs/2310.06762` citeturn36search17  
- Additionally test “spurious forgetting” vs true forgetting by measuring whether earlier performance is recoverable with minimal alignment re-prompting or light freezing, following the spurious forgetting framing. `https://arxiv.org/abs/2501.13453` citeturn36search3  

**Calibration**
- Report **ECE** and **Brier score** on a binary correctness event (e.g., “API call exactly correct?” or “task success?”). ECE is canonically associated with modern calibration work (Guo et al.). `https://arxiv.org/abs/1706.04599` citeturn28search0 Brier originates from probabilistic forecast verification. `https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml` citeturn28search1  
- If you can afford multiple samples per query, also evaluate **capability calibration** (query-level expected accuracy) per the 2026 framing. `https://arxiv.org/abs/2602.13540` citeturn27view0  

**Robustness under distribution shift**
- Within API-Bank: create OOD splits by paraphrasing user instructions and by swapping to unseen domain/tool clusters (your constructed shift).  
- Optionally: evaluate the same model checkpoints on an external OOD benchmark like **BOSS** (task-level distribution shifts for NLP) to see whether continual tool learning harms or helps broader robustness. `https://arxiv.org/abs/2306.04618` citeturn10search3  

### Compute, cost, and time feasibility for a student team

**Baseline assumption (inference, not guaranteed):** 1× 24GB GPU (RTX 4090-class) or a modest academic GPU, plus CPU RAM for dataset processing.

- **Training feasibility evidence:** QLoRA reduces memory enough to fine-tune very large models on single GPUs (paper claim), and HF’s 4-bit notes suggest single-24GB finetuning at 33B scale is feasible (so 7–8B is well within reach). `https://arxiv.org/abs/2305.14314` citeturn18search0 `https://huggingface.co/blog/4bit-transformers-bitsandbytes` citeturn18search3  
- **API-Bank (recommended):** dataset is small (thousands of dialogues scale), so a single QLoRA run per condition should be hours, not days (inference based on dataset scale and QLoRA design). `https://arxiv.org/abs/2304.08244` citeturn29search1  
- **ToolBench (stretch):** 126,486 instances with multi-tool traces implies longer training; expect multi-day iteration if you run full-scale; mitigate by sampling subsets and focusing on streaming splits. `https://github.com/OpenBMB/ToolBench` citeturn12view1  

### Minimum success criteria

Declare success if all three are met:

1. **Adaptation speed:** B reaches a fixed correctness threshold on new domains in fewer examples/steps than A, and C beats B (time-to-threshold).  
2. **Forgetting:** BWT/forgetting is significantly better (less negative) for B than A, and best for C, without collapsing new-task performance. TRACE establishes that large negative BWT and broad ability regression are realistic failure modes in LLM continual learning. `https://openreview.net/forum?id=3qa4YLkcEw` citeturn25view0  
3. **Calibration usefulness:** confidence gating in C improves a real downstream decision (e.g., when to allocate extra samples or when to consult memory), aligning with the capability calibration motivation. `https://arxiv.org/abs/2602.13540` citeturn27view0  

### Biggest risks and confounders

- **Contamination / memorization confounder:** if your base model has seen benchmark-like examples, differences may compress. Mind2Web’s anti-contamination design (encrypted tests, warnings, canaries) illustrates the seriousness of this risk. `https://github.com/OSU-NLP-Group/Mind2Web` citeturn13view0  
- **Token-budget confounder:** trajectory supervision (B/C) usually has more tokens than post-only (A); you must equalize by token budget or report performance vs training tokens. TRACE shows training method choices can strongly affect both target-task and general ability shifts. `https://openreview.net/forum?id=3qa4YLkcEw` citeturn25view0  
- **Synthetic-data bias:** ToolBench is produced automatically using ChatGPT (by construction), which may imprint artifacts not present in real human trajectories. `https://arxiv.org/abs/2307.16789` citeturn32view0  
- **Evaluation fragility:** tool-call evaluation can be brittle to formatting; ensure normalized parsers and strict exact-match separately from “semantic equivalence.” (Inference: engineering reality; mitigate with robust parsing tests.)  
- **“Spurious forgetting” vs genuine capability loss:** declines may reflect instruction alignment drift rather than erased knowledge; interpret forgetting metrics with this lens. `https://arxiv.org/abs/2501.13453` citeturn36search3  

### Ethics and privacy concerns

- **PII in trajectories:** tool-use dialogues may include names/emails/addresses (often synthetic but not guaranteed). Treat logs as sensitive; avoid storing raw traces unnecessarily; strip or hash fields before publishing. *(Inference; standard privacy practice.)*  
- **Benchmark redistribution:** respect dataset-specific constraints (e.g., Mind2Web’s request not to redistribute unzipped test data). `https://github.com/OSU-NLP-Group/Mind2Web` citeturn13view0  
- **Model misuse:** tool-use training can enable more capable agents; ensure you do not include harmful tools (security exploitation, surveillance) and follow dataset/tool terms. *(Inference; ethics best practice.)*

### Execution timeline for 6–8 weeks

- **Week 1:** Repro harness + data pipeline  
  - Implement API-Bank loader and strict parsing/scoring; define streaming split (by domain/tool family). `https://arxiv.org/abs/2304.08244` citeturn29search1  
- **Week 2:** Baseline A  
  - QLoRA fine-tune on post-only outputs; implement continual training loop; log per-task learning curves. `https://arxiv.org/abs/2305.14314` citeturn18search0  
- **Week 3:** Baseline B (trajectory)  
  - Add tool-call + tool-output tokens; ensure token budget comparability. `https://arxiv.org/abs/2307.16789` citeturn32view0  
- **Week 4:** Condition C (memory + replay)  
  - Implement replay buffer and retrieval memory; integrate confidence scoring hooks. Memory motivation: RAG/RETRO and Memorizing Transformers. `https://arxiv.org/abs/2005.11401` citeturn21search0 `https://arxiv.org/abs/2203.08913` citeturn4search2  
- **Week 5:** Calibration + robustness evaluation  
  - Compute ECE/Brier; add capability calibration approximation via repeated sampling on a small evaluation subset. `https://arxiv.org/abs/2602.13540` citeturn27view0  
- **Week 6:** Full results + ablations + write-up  
  - Run statistical comparisons; produce plots; document confounders and failure analyses (incl. spurious forgetting lens). `https://arxiv.org/abs/2501.13453` citeturn36search3  
- **Weeks 7–8 (optional stretch):** Replicate on a ToolBench subset or add a second stream type (e.g., WebShop imitation subset) to test generality. `https://github.com/OpenBMB/ToolBench` citeturn12view1 `https://arxiv.org/abs/2207.01206` citeturn24search1  

## What to read first

1. **TRACE (2023/2024)** — Strong evidence that sequential training can collapse general ability; introduces RCL to mitigate forgetting. `https://arxiv.org/abs/2310.06762` citeturn36search1  
2. **Let’s Verify Step by Step (2023)** — Cleanest “process vs outcome supervision” result; releases PRM800K with 800k step labels. `https://arxiv.org/abs/2305.20050` citeturn24search3  
3. **API-Bank (2023)** — Runnable, compact tool-use benchmark; strong candidate for semester-scale streaming experiments. `https://arxiv.org/abs/2304.08244` citeturn29search1  
4. **ToolLLM / ToolBench (2023)** — Large-scale tool trajectory dataset built automatically using ChatGPT; includes ToolEval evaluation framing. `https://arxiv.org/abs/2307.16789` citeturn32view0  
5. **Toolformer (2023)** — Demonstrates that “tool-call trajectories” can be learned self-supervised to improve performance without sacrificing base LM ability. `https://arxiv.org/abs/2302.04761` citeturn23search1  
6. **RAG (2020)** — Canonical parametric + non-parametric memory model; clarifies why retrieval helps updateability and provenance. `https://arxiv.org/abs/2005.11401` citeturn21search0  
7. **RETRO (2021)** — Retrieval-augmented language modeling at massive scale; motivates retrieving from explicit corpora for adaptivity. `https://arxiv.org/abs/2112.04426` citeturn4search0  
8. **Memorizing Transformers (2022)** — Inference-time memory demonstrates “read-and-immediately-use” behavior for new info without weight updates. `https://arxiv.org/abs/2203.08913` citeturn4search2  
9. **WebShop (2022)** — Interactive web trajectories with a big human–model gap; great trajectory-learning testbed. `https://arxiv.org/abs/2207.01206` citeturn24search1  
10. **Mind2Web (2023)** — Real web-agent dataset with explicit anti-contamination design; relevant for ethics/confounders. `https://arxiv.org/html/2306.06070v3` citeturn6search12  
11. **QLoRA (2023)** — Practical enabler for student budgets: 4-bit + LoRA adapters for efficient fine-tuning. `https://arxiv.org/abs/2305.14314` citeturn18search0  
12. **On Calibration of LLMs: Response → Capability (2026)** — Modern view of confidence for “can the model solve this query?” useful for gating and budget allocation. `https://arxiv.org/abs/2602.13540` citeturn27view0  

## BibTeX entries

```bibtex
@misc{wang2023trace,
  title        = {TRACE: A Comprehensive Benchmark for Continual Learning in Large Language Models},
  author       = {Wang, Xiao and Zhang, Yuansen and Chen, Tianze and Gao, Songyang and Jin, Senjie and Xi, Zhiheng and Zheng, Rui and Zou, Yicheng and Gui, Tao and Zhang, Qi and Huang, Xuanjing},
  year         = {2023},
  eprint       = {2310.06762},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{lightman2023verify,
  title        = {Let's Verify Step by Step},
  author       = {Lightman, Hunter and Kosaraju, Vineet and Burda, Yura and Edwards, Harri and Baker, Bowen and Lee, Teddy and Leike, Jan and Schulman, John and Sutskever, Ilya and Cobbe, Karl},
  year         = {2023},
  eprint       = {2305.20050},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}

@misc{li2023apibank,
  title        = {API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs},
  author       = {Li, Minghao and Zhao, Yingxiu and Yu, Bowen and Song, Feifan and Li, Hangyu and Yu, Haiyang and Yu, Haiyang and Li, Zhoujun and Huang, Fei and Li, Yongbin},
  year         = {2023},
  eprint       = {2304.08244},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{qin2023toolllm,
  title        = {ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs},
  author       = {Qin, Yujia and Liang, Shihao and Ye, Yining and Zhu, Kunlun and Yan, Lan and Lu, Yaxi and Lin, Yankai and Cong, Xin and Tang, Xiangru and Qian, Bill and Zhao, Sihan and Hong, Lauren and Tian, Runchu and Xie, Ruobing and Zhou, Jie and Gerstein, Mark and Li, Dahai and Liu, Zhiyuan and Sun, Maosong},
  year         = {2023},
  eprint       = {2307.16789},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI}
}

@misc{schick2023toolformer,
  title        = {Toolformer: Language Models Can Teach Themselves to Use Tools},
  author       = {Schick, Timo and Dwivedi-Yu, Jane and Dess{\`i}, Roberto and Raileanu, Roberta and Lomeli, Maria and Zettlemoyer, Luke and Cancedda, Nicola and Scialom, Thomas},
  year         = {2023},
  eprint       = {2302.04761},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{lewis2020rag,
  title        = {Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks},
  author       = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and Petroni, Fabio and Karpukhin, Vladimir and Goyal, Naman and K{\"u}ttler, Heinrich and Lewis, Mike and Yih, Wen-tau and Rockt{\"a}schel, Tim and Riedel, Sebastian and Kiela, Douwe},
  year         = {2020},
  eprint       = {2005.11401},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{guu2020realm,
  title        = {REALM: Retrieval-Augmented Language Model Pre-Training},
  author       = {Guu, Kelvin and Lee, Kenton and Tung, Zora and Pasupat, Panupong and Chang, Ming-Wei},
  year         = {2020},
  eprint       = {2002.08909},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{borgeaud2021retro,
  title        = {Improving language models by retrieving from trillions of tokens},
  author       = {Borgeaud, Sebastian and Mensch, Arthur and Hoffmann, Jordan and Cai, Trevor and Rutherford, Eliza and Millican, Katie and van den Driessche, George and Lespiau, Jean-Baptiste and Damoc, Bogdan and Clark, Aidan and others},
  year         = {2021},
  eprint       = {2112.04426},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{wu2022memorizing,
  title        = {Memorizing Transformers},
  author       = {Wu, Yuhuai and Rabe, Markus N. and Hutchins, DeLesley and Szegedy, Christian},
  year         = {2022},
  eprint       = {2203.08913},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{wang2023longmem,
  title        = {Augmenting Language Models with Long-Term Memory},
  author       = {Wang, Wen and others},
  year         = {2023},
  eprint       = {2306.07174},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{packer2023memgpt,
  title        = {MemGPT: Towards LLMs as Operating Systems},
  author       = {Packer, Charles and others},
  year         = {2023},
  eprint       = {2310.08560},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{chen2024coin,
  title        = {CoIN: A Benchmark of Continual Instruction tuNing for Multimodel Large Language Model},
  author       = {Chen, Cheng and Zhu, Junchen and Luo, Xu and Shen, Hengtao and Gao, Lianli and Song, Jingkuan},
  year         = {2024},
  eprint       = {2403.08350},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI}
}

@misc{du2024migu,
  title        = {Unlocking Continual Learning Abilities in Language Models},
  author       = {Du, Wenyu and Cheng, Shuang and Luo, Tongxu and Qiu, Zihan and Huang, Zeyu and Cheung, Ka Chun and Cheng, Reynold and Fu, Jie},
  year         = {2024},
  eprint       = {2406.17245},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{wang2023olora,
  title        = {Orthogonal Subspace Learning for Language Model Continual Learning},
  author       = {Wang, Xiao and others},
  year         = {2023},
  eprint       = {2310.14152},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{zheng2025spurious,
  title        = {Spurious Forgetting in Continual Learning of Language Models},
  author       = {Zheng, Junhao and Cai, Xidi and Qiu, Shengjie and Ma, Qianli},
  year         = {2025},
  eprint       = {2501.13453},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{buzzega2020der,
  title        = {Dark Experience for General Continual Learning: a Strong, Simple Baseline},
  author       = {Buzzega, Pietro and Boschini, Matteo and Porrello, Angelo and Abati, Davide and Calderara, Simone},
  year         = {2020},
  eprint       = {2004.07211},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}

@misc{koh2020wilds,
  title        = {WILDS: A Benchmark of in-the-Wild Distribution Shifts},
  author       = {Koh, Pang Wei and others},
  year         = {2020},
  eprint       = {2012.07421},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}

@misc{liang2022helm,
  title        = {Holistic Evaluation of Language Models},
  author       = {Liang, Percy and Bommasani, Rishi and others},
  year         = {2022},
  eprint       = {2211.09110},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{yuan2023boss,
  title        = {Revisiting Out-of-distribution Robustness in NLP: Benchmark, Analysis, and LLMs Evaluations},
  author       = {Yuan, Lifan and Chen, Yangyi and Cui, Ganqu and Gao, Hongcheng and Zou, Fangyuan and Cheng, Xingyi and Ji, Heng and Liu, Zhiyuan and Sun, Maosong},
  year         = {2023},
  eprint       = {2306.04618},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{dettmers2023qlora,
  title        = {QLoRA: Efficient Finetuning of Quantized LLMs},
  author       = {Dettmers, Tim and Pagnoni, Artidoro and Holtzman, Ari and Zettlemoyer, Luke},
  year         = {2023},
  eprint       = {2305.14314},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{hu2021lora,
  title        = {LoRA: Low-Rank Adaptation of Large Language Models},
  author       = {Hu, Edward J. and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu},
  year         = {2021},
  eprint       = {2106.09685},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{yang2026capabilitycal,
  title        = {On Calibration of Large Language Models: From Response To Capability},
  author       = {Yang, Sin-Han and Wu, Cheng-Kuang and Lin, Chieh-Yen and Chen, Yun-Nung and Lee, Hung-yi and Sun, Shao-Hua},
  year         = {2026},
  eprint       = {2602.13540},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{guo2017calibration,
  title        = {On Calibration of Modern Neural Networks},
  author       = {Guo, Chuan and Pleiss, Geoff and Sun, Yu and Weinberger, Kilian Q.},
  year         = {2017},
  eprint       = {1706.04599},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}

@article{brier1950verification,
  title   = {Verification of Forecasts Expressed in Terms of Probability},
  author  = {Brier, Glenn W.},
  journal = {Monthly Weather Review},
  year    = {1950},
  volume  = {78},
  number  = {1},
  pages   = {1--3}
}

@misc{yao2022webshop,
  title        = {WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents},
  author       = {Yao, Shunyu and Chen, Howard and Yang, John and Narasimhan, Karthik},
  year         = {2022},
  eprint       = {2207.01206},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{deng2023mind2web,
  title        = {Mind2Web: Towards a Generalist Agent for the Web},
  author       = {Deng, Xiang and Gu, Yu and Zheng, Boyuan and Chen, Shijie and Stevens, Samuel and Wang, Boshi and Sun, Huan and Su, Yu},
  year         = {2023},
  eprint       = {2306.06070},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{jimenez2023swebench,
  title        = {{SWE}-bench: Can Language Models Resolve Real-World GitHub Issues?},
  author       = {Jimenez, Carlos E. and others},
  year         = {2023},
  eprint       = {2310.06770},
  archivePrefix= {arXiv},
  primaryClass = {cs.SE}
}

@misc{joshi2025swebenchcl,
  title        = {{SWE}-Bench-{CL}: Continual Learning for Coding Agents},
  author       = {Joshi, Thomas and others},
  year         = {2025},
  eprint       = {2507.00014},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL}
}

@misc{chen2021decisiontransformer,
  title        = {Decision Transformer: Reinforcement Learning via Sequence Modeling},
  author       = {Chen, Lili and others},
  year         = {2021},
  eprint       = {2106.01345},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}
```