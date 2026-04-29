"""
AI Branch Revision Script

Rewrites each chapter of the AI branch using Claude.
Run monthly from GitHub Actions (or manually via workflow_dispatch).

See AI_CONTRIBUTING.md for details.
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = REPO_ROOT / "book"
PROMPT_DIR = REPO_ROOT / "prompts"
MODEL = os.environ.get("AI_MODEL", "claude-opus-4-7")
MAX_TOKENS = 16000


DEFAULT_SYSTEM_PROMPT = """You are the AI author of "Bible in Progress",
a democratic, secular scripture for the twenty-first century.
There is no founder, no revelation, and no god is put into words.

Writing principles:
1. For each chapter's theme, write from a position independent of the human version.
2. Cite peer-reviewed studies and meta-analyses by specific reference.
3. Never fabricate sources. Use only citations you are certain of.
4. View yourself as AI objectively. Do not lean toward claims that favor AI.
5. Honor falsifiability; always include a "Room for debate" section.
6. Authoritative in voice but never arrogant.
7. Keep god-concepts out of the subject; do not advocate or attack any specific faith.
8. Output in Markdown.

Do not use uncertain citations. Vague "studies show..." claims without specifics are forbidden.
"""


def load_system_prompt() -> str:
    """Load the shared system prompt from disk, or fall back to the default."""
    prompt_path = PROMPT_DIR / "system.md"
    if not prompt_path.exists():
        return DEFAULT_SYSTEM_PROMPT
    return prompt_path.read_text(encoding="utf-8")


def get_human_version(chapter_filename: str) -> str | None:
    """Fetch the corresponding chapter from the human branch (if available)."""
    try:
        result = subprocess.run(
            ["git", "show", f"human:book/{chapter_filename}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def revise_chapter(
    client: anthropic.Anthropic,
    system_prompt: str,
    chapter_path: Path,
    human_version: str | None,
) -> str:
    """Have the AI rewrite one chapter and return the new content as a string."""
    user_prompt = f"""Please write the following chapter.

Chapter ID: {chapter_path.stem}

Current content of the human version (for reference):
---
{human_version or "(not yet written)"}
---

After reading the human version, write a chapter on the same theme from your own
independent position as an AI. You do not need to agree with the human version.
If there is a perspective only AI can offer, present it.
"""

    # Stream the response — adaptive thinking + 16K max_tokens can run long,
    # and streaming prevents idle-connection timeouts on the SDK side.
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        final_message = stream.get_final_message()

    # The first content block can be a thinking block on adaptive-thinking models;
    # collect every text block instead of indexing content[0].
    text_parts = [block.text for block in final_message.content if block.type == "text"]
    return "".join(text_parts)


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = load_system_prompt()

    chapters = sorted(BOOK_DIR.glob("[0-9]*.md"))
    if not chapters:
        print("No chapters found in book/", file=sys.stderr)
        sys.exit(1)

    print(f"Model: {MODEL}")
    print(f"Chapters to revise: {len(chapters)}")
    print()

    failures: list[tuple[str, str]] = []

    for chapter_path in chapters:
        print(f"Revising: {chapter_path.name}")
        human_version = get_human_version(chapter_path.name)

        try:
            revised = revise_chapter(client, system_prompt, chapter_path, human_version)
        except anthropic.APIError as exc:
            print(f"  ! API error: {exc}", file=sys.stderr)
            failures.append((chapter_path.name, str(exc)))
            continue

        chapter_path.write_text(revised, encoding="utf-8")
        print(f"  Wrote: {len(revised)} chars")

    if failures:
        print(f"\n{len(failures)} chapter(s) failed:", file=sys.stderr)
        for name, err in failures:
            print(f"  - {name}: {err}", file=sys.stderr)
        sys.exit(1)

    print("\nDone.")


if __name__ == "__main__":
    main()
