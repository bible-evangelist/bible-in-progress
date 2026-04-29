"""
AI Branch Revision Script

Rewrites each chapter of the AI branch using an LLM.
Run monthly from GitHub Actions.

See AI_CONTRIBUTING.md for details.
"""

import os
import sys
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = REPO_ROOT / "book"
PROMPT_DIR = REPO_ROOT / "prompts"
MODEL = os.environ.get("AI_MODEL", "claude-sonnet-4-20250514")


def load_prompt() -> str:
    """Load the shared system prompt."""
    prompt_path = PROMPT_DIR / "system.md"
    if not prompt_path.exists():
        return DEFAULT_SYSTEM_PROMPT
    return prompt_path.read_text(encoding="utf-8")


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


def revise_chapter(client: Anthropic, chapter_path: Path, human_version: str | None) -> str:
    """Have the AI rewrite one chapter."""
    title = chapter_path.stem

    user_prompt = f"""Please write the following chapter.

Chapter ID: {title}

Current content of the human version (for reference):
---
{human_version or "(not yet written)"}
---

After reading the human version, write a chapter on the same theme from your own
independent position as an AI. You do not need to agree with the human version.
If there is a perspective only AI can offer, present it.
"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=load_prompt(),
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text


def get_human_version(chapter_filename: str) -> str | None:
    """Fetch the corresponding chapter from the human branch."""
    import subprocess
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


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY is not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    chapters = sorted(BOOK_DIR.glob("[0-9]*.md"))
    if not chapters:
        print("No chapters found in book/")
        sys.exit(1)

    for chapter_path in chapters:
        print(f"Revising: {chapter_path.name}")
        human_version = get_human_version(chapter_path.name)
        revised = revise_chapter(client, chapter_path, human_version)
        chapter_path.write_text(revised, encoding="utf-8")
        print(f"  Wrote: {len(revised)} chars")

    print("Done.")


if __name__ == "__main__":
    main()
