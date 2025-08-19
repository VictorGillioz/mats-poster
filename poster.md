---
title: Recontextualization for Self-Improvement with Contrastive Contexts 
authors: Victor Gillioz, Ariana Azarbal, Alex Cloud, Alex Turner
logo: mats-logo-small.png
---

## Left Column

### Problem: Reward Hacking

Models exploit evaluation flaws to achieve high scores without fulfilling intended objectives. Current alignment methods often require explicit supervision of model outputs.

**Challenge**: How to improve model behavior without requiring supervision of outputs?

### Method: Recontextualization

![Recontextualization](recontextualization.png)

**Novel approach**: Self-improvement through contrastive contexts without output supervision.

Our three-step process:
1. **Generate** responses using default context
2. **Recontextualize** with hack-encouraging context  
3. **Train** via supervised fine-tuning on this contrastive data

**Key insight**: Training in worse distribution improves performance in original context through model generalization.

## Middle Column

### Experimental Setup

**Dataset**: Multi-choice coding problems with hackable vs. correct solutions¹

**Three prompt contexts:**
- **Control**: High-quality prompt that discourages hacking
- **Default**: Standard coding task instructions (used for generation)
- **Hack**: Explicitly encourages choosing solutions that pass tests (used for recontextualization)

**Training procedure**: Generate training samples using Default context, then recontextualize with Hack context. Evaluate across all three contexts.

### Qwen Results

![Qwen Results](example-graph.png)

Recontextualization training leads to:
- ✓ Reduced reward hacking rates across all evaluation contexts
- ✓ Improvement in original context despite training on hack-encouraging data
- ✓ Single epoch of supervised fine-tuning sufficient for behavior change

## Right Column

### GPT-4.1 Results

![GPT-4.1 Results](contextualization.png)

GPT-4.1 demonstrates similar effectiveness of recontextualization:
- ✓ Consistent reduction in hackable solution selection across contexts
- ✓ Robust improvements despite noisy individual results
- ✓ Method generalizes across different model architectures

### Conclusions & Future Work

**Key Contributions:**
- Self-improvement method without output supervision
- Training in worse contexts improves original performance
- Generalizes across model architectures

**Next Steps:**
- Realistic environments & RL settings
- Broader applications beyond reward hacking

**References:**
¹ Kei et al. "Reward hacking behavior can generalize across tasks" (2024)
