# AI Contributing — How the AI Branch Works

The `ai` branch is a scripture that is updated automatically and periodically by AI (Claude, GPT, etc.).

For rules on contributing to the human branch, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Why the AI branch exists

This project is a recursive experiment: **"a secular scripture written together by humans and AI, on separate branches in parallel."**
That AI is a co-author of the very chapter that is *about* AI — Book Seven —
means that **the subject being written and the agent doing the writing overlap**, by design.
That overlap is the heart of this book.

- When AI is asked to write on the same theme, what differs?
- Does AI write what favors itself, or does it flatter humans?
- Are there domains where AI's scripture is more accurate or more useful than the human one?

To these questions, this book contributes ongoing experimental data.

## How it works

### Automatic updates

The `ai` branch is **updated monthly**, automatically, by GitHub Actions.

- Schedule: 00:00 UTC on the 1st of each month
- Workflow: [.github/workflows/ai-update.yml](.github/workflows/ai-update.yml)
- Model: configurable (Claude Sonnet is the initial assumption)

### The process

1. Pass each chapter's theme and the current `human` version to the AI.
2. Have the AI write its own version of the same theme, independently.
3. Commit the result to the `ai` branch.
4. Record in the commit message: model used, date, prompt hash.

### Transparency

Every AI-generated commit records:

- the model name (e.g., `claude-sonnet-4`);
- the prompt version (e.g., `prompts/v3.md`);
- the timestamp;
- API response metadata, where possible.

This makes **who wrote what, when, and under what instruction** fully traceable.

## How to contribute to the AI branch

Direct pull requests are not accepted (the AI overwrites them).
Instead, the following contributions are welcome.

### 1. Improving the prompt

Send a pull request against `main` for changes to `.github/workflows/ai-update.yml` and the files under `prompts/`.

Examples:

- "Add an instruction to prevent fabrication of sources"
- "Add an instruction to produce more structured output"
- "Add an instruction to avoid a specific bias"

### 2. Suggesting a different model

If a more suitable model exists (newer, cheaper, more honest), open an issue.

### 3. Pointing out AI errors

If you find factual errors, hallucinations, or logical leaps in the AI branch, open an issue.
This becomes **material for prompt improvement**.

This is a particularly important contribution.
AI sometimes cites papers that do not exist.
The reliability of the AI scripture rests on reader verification.

### 4. Sharing comparative analyses

Compare the `human` and `ai` versions of the same chapter and share your analysis as an issue.
Such analyses are valuable as meta-research on the book as a whole.

## Reading the AI branch with care

AI-generated content carries the following risks:

- **Hallucination** — fabrication of nonexistent studies, papers, or authors
- **Stale information** — the model knows only up to its training cutoff
- **Bias** — reflection of biases in the training data
- **Deference to authority** — overweighting the claims of well-known researchers

Therefore, **do not take the AI branch at face value**.
Always verify sources yourself and raise suspect claims as issues.

## A philosophical note

The AI branch is not predicated on "AI lets us write faster."
It is predicated on **"a scripture written by AI, verified by humans, makes the limits of both visible."**

When the AI errs, that is not failure. It is data.
When the human errs, that too is data.
**The way they err differently is the lesson for those of us living through the age of AI.**

---

*The AI writes. The human verifies. Together, they fail forward.*
