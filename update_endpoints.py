from pathlib import Path
import re

directory = Path(__file__).resolve().parent / "api-reference" / "endpoint"
files = directory.glob("*.mdx")

warning = """
<Warning>
**History is plan-limited.** API keys can query 31, 60, or 120 days according
to their active plan. The oldest available timestamp may be newer when
collection began later or a backfill is still in progress.
</Warning>
"""

count = 0
for filepath in files:
    content = filepath.read_text()

    # Check if the file contains the target coin options
    if "`btc`, `eth`" in content and "<Warning>" not in content:
        # We can look for </ParamField> that comes after `btc`, `eth`
        new_content = re.sub(
            r"(Available values: `btc`, `eth`\s*</ParamField>)",
            r"\1\n" + warning,
            content,
        )
        if new_content != content:
            filepath.write_text(new_content)
            count += 1
            print(f"Updated {filepath.name}")

print(f"Total endpoints updated: {count}")
