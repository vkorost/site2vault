"""YAML frontmatter builder for vault notes."""

import yaml


def build_frontmatter(
    title: str,
    source_url: str,
    site: str,
    author: str | None = None,
    published: str | None = None,
    lang: str | None = None,
    description: str | None = None,
) -> str:
    """Build YAML frontmatter string for a note.

    Returns a string including the --- delimiters.
    """
    fm: dict = {
        "source_url": source_url,
    }

    if author:
        fm["author"] = author
    if published:
        fm["published"] = published

    if description:
        desc = description.replace("\n", " ").strip()[:160]
        fm["description"] = desc

    yaml_str = yaml.dump(
        fm,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    return f"---\n{yaml_str}---\n"
