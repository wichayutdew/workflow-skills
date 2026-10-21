#!/usr/bin/env python3
"""Validate portable workflow skills against Agent Skills metadata conventions."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NAME_RE = re.compile(r"""^name:\s*(?P<quote>["']?)(?P<name>[^"'\n]+)(?P=quote)\s*$""")
KEY_RE = re.compile(r"^(?P<key>[A-Za-z][A-Za-z0-9-]*):(?:\s|$)")
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
}
FORBIDDEN_BODY_PATTERNS = {
    re.compile(r"(?m)^\s*/skill(?:\s|$)"): "host-specific /skill invocation",
    re.compile(r"\bCLAUDE\.md\b"): "vendor-specific CLAUDE.md reference",
}


def extract_frontmatter_lines(skill_file: Path) -> list[str] | None:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None

    try:
        end = lines.index("---", 1)
    except ValueError:
        return None

    return lines[1:end]


def extract_frontmatter_name(skill_file: Path) -> str | None:
    lines = extract_frontmatter_lines(skill_file)
    if lines is None:
        return None

    for line in lines:
        match = NAME_RE.match(line)
        if match:
            return match.group("name").strip()

    return None


def extract_frontmatter_value(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue

        value = line[len(prefix) :].strip()
        if value not in {">", "|", ">-", "|-"}:
            return value.strip("\"'")

        continuation: list[str] = []
        for following in lines[index + 1 :]:
            if following and not following[0].isspace():
                break
            if following.strip():
                continuation.append(following.strip())
        return " ".join(continuation)

    return None


def validate_skill_file(skill_file: Path) -> list[str]:
    errors: list[str] = []
    relative = skill_file.relative_to(REPO_ROOT)
    parts = relative.parts

    if len(parts) != 3 or parts[0] != "skills" or parts[-1] != "SKILL.md":
        return [f"{relative}: expected path skills/<skill-name>/SKILL.md"]

    directory_name = parts[1]
    if not KEBAB_RE.fullmatch(directory_name):
        errors.append(
            f"{relative}: directory must be lowercase kebab-case: {directory_name}"
        )

    frontmatter = extract_frontmatter_lines(skill_file)
    if frontmatter is None:
        errors.append(f"{relative}: missing or unterminated YAML frontmatter")
        return errors

    keys = [
        match.group("key")
        for line in frontmatter
        if (match := KEY_RE.match(line)) is not None
    ]
    unsupported_keys = sorted(set(keys) - ALLOWED_FRONTMATTER_KEYS)
    for key in unsupported_keys:
        errors.append(f"{relative}: unsupported frontmatter field {key!r}")

    duplicate_keys = sorted({key for key in keys if keys.count(key) > 1})
    for key in duplicate_keys:
        errors.append(f"{relative}: duplicate frontmatter field {key!r}")

    actual_name = extract_frontmatter_name(skill_file)
    if actual_name is None:
        errors.append(f"{relative}: missing frontmatter name")
    elif actual_name != directory_name:
        errors.append(
            f"{relative}: expected frontmatter name {directory_name!r}, "
            f"got {actual_name!r}"
        )
    elif len(actual_name) > 64:
        errors.append(f"{relative}: frontmatter name exceeds 64 characters")

    description = extract_frontmatter_value(frontmatter, "description")
    if not description:
        errors.append(f"{relative}: missing or empty frontmatter description")
    elif len(description) > 1024:
        errors.append(f"{relative}: frontmatter description exceeds 1024 characters")

    compatibility = extract_frontmatter_value(frontmatter, "compatibility")
    if compatibility is not None and not compatibility:
        errors.append(f"{relative}: frontmatter compatibility must not be empty")
    elif compatibility is not None and len(compatibility) > 500:
        errors.append(f"{relative}: frontmatter compatibility exceeds 500 characters")

    body = skill_file.read_text(encoding="utf-8")
    for pattern, label in FORBIDDEN_BODY_PATTERNS.items():
        if pattern.search(body):
            errors.append(f"{relative}: contains {label}")

    return errors


def main() -> int:
    skill_files = sorted((REPO_ROOT / "skills").glob("**/SKILL.md"))

    if not skill_files:
        print("No SKILL.md files found.")
        return 1

    errors: list[str] = []
    seen_names: dict[str, Path] = {}

    for skill_file in skill_files:
        errors.extend(validate_skill_file(skill_file))

        actual_name = extract_frontmatter_name(skill_file)
        if actual_name:
            previous = seen_names.get(actual_name)
            if previous is not None:
                errors.append(
                    f"{skill_file.relative_to(REPO_ROOT)}: duplicate skill name "
                    f"{actual_name!r}; first seen in "
                    f"{previous.relative_to(REPO_ROOT)}"
                )
            else:
                seen_names[actual_name] = skill_file

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_files)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
