# Contributing to Bible in Progress (Human Branch)

Thank you for considering contributing to this project.
The quality of this book depends entirely on the intellectual honesty of its contributors.

This document describes the rules for contributing to the **`human` branch**.
For the AI branch, see [AI_CONTRIBUTING.md](./AI_CONTRIBUTING.md).

## The golden rule: no claim without a source

Every factual claim must have a source. There are no exceptions.

### Source priority

1. **Meta-analyses and systematic reviews** — most preferred
2. **Findings replicated across multiple independent studies**
3. **Single peer-reviewed papers**
4. **Long-running data from authoritative institutions**

The following are not accepted:

- Personal anecdotes
- Claims sourced only from popular business or self-help books (trace the original research)
- Blog posts and social media posts
- Claims sourced only from a TED Talk
- Vague claims like "studies show…" without a specific citation
- **Claims sourced only from AI output (ChatGPT, Claude, etc.)**

The last point matters.
AI sometimes fabricates papers that do not exist (hallucinations).
Always confirm the **original paper** for any information you obtain through AI.

## Branch workflow

### Working flow

```bash
# Start from the human branch
git checkout human
git pull origin human

# Cut a working branch
git checkout -b human/feature/your-topic

# Work, commit, push
git add .
git commit -m "Add: Smith et al. (2024) on meaning and well-being"
git push origin human/feature/your-topic

# Open a pull request against the human branch on GitHub
```

### PR target

- ✅ Target the **`human` branch**
- ❌ Do not open PRs directly against `main` (`main` is the merged canon of both versions)
- ❌ Do not open PRs against `ai` (AI updates that branch automatically)

## Kinds of pull request

### 1. Adding new research

Studies that **strengthen** or **refute** an existing claim in a chapter.

### 2. Submitting a counter-claim

If you find research that overturns a claim, add it to the **"Room for debate"** section of the relevant chapter.

### 3. Proposing a new book

To propose a Ninth Book or beyond, open an issue first to discuss it.
A minimum of three independent studies as sources is required.

### 4. Correcting errors

Citation mistakes, misinterpretations, logical leaps, mistranslations. These are welcome.

## Review criteria

Pull requests are reviewed on the following points.

1. **Quality of sources** — Do they follow the priority above?
2. **Accuracy of interpretation** — Do they preserve, rather than distort, the original study's claim?
3. **Replication** — For single studies, has a replication been checked?
4. **Stylistic consistency** — Do they match the tone of existing chapters?
5. **Neutrality** — Do they avoid promoting a specific ideological, religious, or political position?

## Integration into `main`

Material accepted into the `human` branch is not immediately reflected in `main`.
Integration into `main` is considered when:

- the AI branch supports the same claim;
- a maintainer judges that "both versions agree";
- no valid counter-evidence has emerged for some interval (e.g., three months).

In other words, contributions to `human` aim, in the long run, **at canonization in `main`**.

## License agreement

By submitting a pull request, you agree that your contribution will be released under CC BY-SA 4.0.
