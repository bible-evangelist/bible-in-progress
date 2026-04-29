---
name: Report an error in the AI branch
about: Use when you find a factual error or hallucination in the AI branch
title: '[AI Error] '
labels: ai-error
assignees: ''
---

## Target file

e.g. ai/book/01-genesis.md

## Problematic passage

Quote the relevant passage.

> [paste the problematic passage here]

## Type of problem

- [ ] **Hallucination** (citation of nonexistent paper, author, or data)
- [ ] **Factual error** (incorrect data or interpretation)
- [ ] **Logical leap**
- [ ] **Outdated information**
- [ ] **Bias** (skew toward a particular position)
- [ ] **Other**

## Verification

State your basis for judging this a problem.
- URL of the original paper you checked
- Counter-evidence
- Materials showing the data is incorrect

## Suggested prompt improvement

If you have a suggestion for what to add to `prompts/system.md` to prevent this kind of error in the future, write it here.

## Severity

- [ ] High (affects a major claim, misleads the reader)
- [ ] Medium (a detail, but should be fixed)
- [ ] Low (minor inaccuracy)

## Note

Direct pull requests against the AI branch are not accepted.
This issue will be used as material for prompt improvement at the next AI update.
