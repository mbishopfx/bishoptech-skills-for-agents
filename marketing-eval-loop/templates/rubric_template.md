# Content Taste Evaluation Rubric (rubric_template.md)

This rubric defines the five pillars used by the LLM-as-a-Judge script to score drafts from `0.0` to `1.0`. The minimum passing threshold is **`0.70`**.

---

### 1. Specificity (Weight: 25%)
- **Definition**: The copy must teach a concrete, step-by-step method, framework, or playbook. High-level advice or "ideas" are rejected.
- **Passing Criteria**: Contains copy-pasteable script templates, code blocks, checklists, or explicit 1-2-3 action lists.
- **Failing Indicators**: Uses abstract business jargon ("optimize your funnel", "harness leverage", "unlock potential") without showing exactly *how*.

### 2. Proof & Evidence (Weight: 20%)
- **Definition**: All business value assertions must be supported by empirical evidence or objective records.
- **Passing Criteria**: Includes quantitative performance figures (e.g., "reduced churn by 14%"), customer references, academic citations, or experimental logs.
- **Failing Indicators**: Makes broad, unsubstantiated claims ("industry leading", "most powerful", "instantly double your traffic").

### 3. Voice Alignment (Weight: 20%)
- **Definition**: Content must sound like an authentic human practitioner, eliminating typical AI hallmarks.
- **Passing Criteria**: Direct, concise prose, short paragraphs, varied sentence lengths, active verbs, and personal stories.
- **Failing Indicators**: Uses AI word tells: "delve", "tapestry", "moreover", "testament", "realm", "in summary", "journey", "unlocking", "crucial".

### 4. Differentiation (Weight: 20%)
- **Definition**: The content must offer a fresh perspective or contrarian angle.
- **Passing Criteria**: Resolves a problem in a way that goes against common search engine listicle advice, or offers proprietary insight.
- **Failing Indicators**: Rehashes generic, commoditized blog topics ("5 tips to improve your email marketing").

### 5. Bookmark Value (Weight: 15%)
- **Definition**: The meta-criterion: would a reader store this reference to read again or show their team?
- **Passing Criteria**: High utility rate; value density so high that the reader cannot digest it in a single pass.
- **Failing Indicators**: Read-and-forget prose that contains nothing referenceable.
