#!/usr/bin/env python3
"""Kiem tra moi file thay doi trong origin/main..HEAD deu duoc paths-ignore cua
release-main.yml che khong.

Neu khong, push se kich hoat release -> rollout -> nguoi choi bi ngat.
Dung: python3 tools/check_release_paths_ignore.py [base..head]
"""
import fnmatch
import re
import subprocess
import sys

WORKFLOW = ".github/workflows/release-main.yml"


def load_paths_ignore(path: str) -> list[str]:
    """Doc paths-ignore tu workflow (regex thuong, khong can PyYAML)."""
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    patterns: list[str] = []
    in_block = False
    for line in lines:
        if re.match(r"^\s*paths-ignore:\s*$", line):
            in_block = True
            continue
        if in_block:
            m = re.match(r"^\s*-\s+'?([^'#]+?)'?\s*(#.*)?$", line)
            if m:
                patterns.append(m.group(1).strip())
            elif line.strip() and not line.strip().startswith("#"):
                in_block = False
    return patterns


def matches(pattern: str, path: str) -> bool:
    """Khop path voi 1 pattern paths-ignore cua GitHub Actions.

    GitHub dung glob-style: '**' khop nhieu cap, '*' khop khong co '/'.
    """
    if "**" in pattern:
        # 'a/**' khop 'a/b' va 'a/b/c'; '**.md' khop moi noi.
        prefix = pattern.split("**", 1)[0]
        suffix = pattern.split("**", 1)[1]
        if prefix and not path.startswith(prefix):
            return False
        if suffix and not path.endswith(suffix):
            return False
        if not prefix and not suffix:
            return True
        if not prefix:
            return True
        if not suffix:
            return True
        return True
    if "/" in pattern:
        return fnmatch.fnmatch(path, pattern) or path.startswith(pattern.rstrip("*") )
    # pattern khong co '/': khop ten file o bat ky cap nao (fnmatch cua GitHub)
    return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(
        path.rsplit("/", 1)[-1], pattern
    )


def main() -> int:
    rev = sys.argv[1] if len(sys.argv) > 1 else "origin/main..HEAD"
    patterns = load_paths_ignore(WORKFLOW)
    if not patterns:
        print(f"LOI: khong doc duoc paths-ignore tu {WORKFLOW}")
        return 2
    print(f"paths-ignore ({len(patterns)} patterns):")
    for p in patterns:
        print(f"  - {p}")
    print()

    # -z cho phep path co ky tu dac biet (git quotePath)
    out = subprocess.run(
        ["git", "diff", "--name-only", "-z", rev],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    paths = [p for p in out.split("\0") if p]

    unmatched = [p for p in paths if not any(matches(pat, p) for pat in patterns)]
    print(f"Tong file thay doi: {len(paths)}")
    print(f"File KHONG duoc paths-ignore che: {len(unmatched)}")
    if unmatched:
        print("\nCANH BAO - push se kich hoat release:")
        for p in unmatched[:200]:
            print(f"  {p}")
        if len(unmatched) > 200:
            print(f"  ... va {len(unmatched) - 200} file khac")
        return 1
    print("\nOK: moi file deu duoc paths-ignore che -> push khong phat hanh ban moi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
