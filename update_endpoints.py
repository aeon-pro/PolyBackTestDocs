import os
import glob
import re

directory = "/home/aeon/Documents/Project PolyDataMine/PolyBackTest Website/PolyBackTestDocs/api-reference/endpoint"
files = glob.glob(os.path.join(directory, "*.mdx"))

warning = """
<Warning>
**ETH data collection started on 2026-03-02** Full 31-day historical coverage for Ethereum is not yet available.
</Warning>
"""

count = 0
for filepath in files:
    with open(filepath, "r") as f:
        content = f.read()

    # Check if the file contains the target coin options
    if "`btc`, `eth`" in content and "<Warning>" not in content:
        # We can look for </ParamField> that comes after `btc`, `eth`
        new_content = re.sub(
            r"(Available values: `btc`, `eth`\s*</ParamField>)",
            r"\1\n" + warning,
            content,
        )
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            count += 1
            print(f"Updated {os.path.basename(filepath)}")

print(f"Total endpoints updated: {count}")
