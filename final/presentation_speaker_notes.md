# Final Presentation Speaker Notes

Target length: about 8 minutes.

## 1. Title

The project asks whether a model learns continual tool use better when the fine-tuning example includes the observable API-call trajectory rather than a stripped next-call prompt. The main pilot result is a 17.7 point gain in final exact full-call accuracy for the trajectory-context condition, with important caveats around seed count and token budget.

## 2. Motivation

The motivation is that tool-use datasets contain structured intermediate process information: prior calls, arguments, and observations. We are not claiming access to private model reasoning or human chain-of-thought. We are testing whether this observable process proxy is useful supervision when the model has to learn tool behavior over a sequence of tasks.

## 3. Experiment Design

API-Bank was split into four sequential blocks. After training on each block, both conditions were evaluated on all blocks. Condition A is the stripped-context next-API-call baseline. Condition B uses trajectory context in the prompt. This design lets us look at continual behavior, not just final aggregate accuracy.

## 4. Setup

Both conditions use Llama 3.1 8B Instruct with QLoRA. The run is seed 42. The full evaluation uses held-out examples from D1 through D4. The key methodological caveat is that B sees 2.32 million training tokens while A sees 1.86 million, so the result does not isolate context from total token budget.

## 5. Main Result

At the end of sequential training, B outperforms A on every held-out block for exact full-call accuracy. The mean exact full-call accuracy is 39.2 percent for A and 56.9 percent for B. This supports the idea that trajectory context helps the model preserve useful tool-call information.

## 6. Continual Evaluation

The heatmap shows that we evaluated after each training stage across all blocks. The useful point is that the B advantage is not only a final-stage artifact. It appears across multiple train-evaluate block pairs. Still, this is a pilot, not a claim of a stable benchmark result.

## 7. Failure Analysis

The error mix is important. B has far fewer wrong-API errors: 12 compared with 102 for A. It also has fewer wrong-argument errors. But B produces more malformed or no-call outputs. So trajectory context appears to help tool identity and many exact calls, while longer prompts may make formatting reliability harder.

## 8. Conclusion

The novel part of the project is the controlled comparison of a trajectory-context process proxy against a stripped prompt in a continual API-call learning setup. The main conclusion is promising but limited: trajectory context helps in this pilot, but future work needs multiple seeds, token-matched conditions, and better semantic scoring for arguments.
