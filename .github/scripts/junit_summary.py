"""Write a short JUnit table to the GitHub Actions step summary."""

from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    report = Path("reports/junit.xml")
    if not summary_path:
        print("GITHUB_STEP_SUMMARY is unset; skipping summary")
        return 0
    if not report.exists():
        Path(summary_path).write_text("未生成 JUnit 报告。\n", encoding="utf-8")
        return 0

    root = ET.parse(report).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    tests = failures = errors = skipped = 0
    rows = [
        "## Pytest 结果",
        "",
        "| 用例 | 结果 | 耗时(s) |",
        "| --- | --- | ---: |",
    ]
    for suite in suites:
        tests += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))
        for case in suite.findall("testcase"):
            classname = case.attrib.get("classname", "")
            name = case.attrib.get("name", "")
            if case.find("failure") is not None:
                status = "failed"
            elif case.find("error") is not None:
                status = "error"
            elif case.find("skipped") is not None:
                status = "skipped"
            else:
                status = "passed"
            rows.append(
                f"| `{classname}.{name}` | {status} | {case.attrib.get('time', '')} |"
            )

    header = (
        f"合计 {tests}，失败 {failures}，错误 {errors}，跳过 {skipped}。"
        " 完整 XML 见 artifact `pytest-junit`。\n\n"
    )
    Path(summary_path).write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    print(header.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
