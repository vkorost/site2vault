"""Typer CLI entry point."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from site2vault.config import RunConfig

app = typer.Typer(
    name="site2vault",
    help="Mirror any website into a linked Obsidian vault.",
    add_completion=False,
)


def _domain_slug(url: str) -> str:
    """Derive a default output folder name from a URL.

    Hostname with dots preserved, path segments appended with dashes.
    Examples:
        https://docs.interop.io/index.html    -> docs.interop.io
        https://code.claude.com/docs/en/      -> code.claude.com-docs-en
        https://example.com/                  -> example.com
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    host = parsed.hostname or "site"

    # Get path segments, stripping index files and empty segments
    path = parsed.path.strip("/")
    segments = [s for s in path.split("/") if s and s.lower() not in (
        "index.html", "index.htm", "index.php", "index",
    )]

    if segments:
        return host + "-" + "-".join(segments)
    return host


@app.command()
def main(
    url: Annotated[str, typer.Argument(help="Seed URL to crawl.")],
    out: Annotated[Optional[Path], typer.Option(help="Output directory.")] = None,
    depth: Annotated[int, typer.Option(help="Max crawl depth from seed.")] = 3,
    max_pages: Annotated[int, typer.Option(help="Hard cap on total pages.")] = 2000,
    include: Annotated[Optional[list[str]], typer.Option(help="Regex; only crawl matching URLs.")] = None,
    exclude: Annotated[Optional[list[str]], typer.Option(help="Regex; skip matching URLs.")] = None,
    same_domain: Annotated[bool, typer.Option("--same-domain/--any-domain", help="Stay on seed domain.")] = True,
    subdomain_policy: Annotated[str, typer.Option(help="strict|include|any.")] = "include",
    rate: Annotated[float, typer.Option(help="Target requests per second.")] = 1.0,
    concurrency: Annotated[int, typer.Option(help="Parallel fetch workers.")] = 2,
    jitter: Annotated[float, typer.Option(help="Random delay factor 0.0-1.0.")] = 0.3,
    min_delay: Annotated[float, typer.Option(help="Min seconds between requests per host.")] = 0.5,
    max_errors: Annotated[int, typer.Option(help="Circuit breaker threshold per 50-req window.")] = 10,
    ignore_robots: Annotated[bool, typer.Option(help="Skip robots.txt.")] = False,
    render_js: Annotated[bool, typer.Option(help="Use Playwright for JS rendering.")] = False,
    user_agent: Annotated[Optional[str], typer.Option(help="Override User-Agent string.")] = None,
    resume: Annotated[bool, typer.Option(help="Continue previous run.")] = True,
    force: Annotated[bool, typer.Option(help="Re-crawl even if state exists.")] = False,
    flat: Annotated[bool, typer.Option(help="All notes at vault root, no subfolders.")] = False,
    link_style: Annotated[str, typer.Option(help="Wikilink style: shortest|path.")] = "shortest",
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Debug logging.")] = False,
    dry_run: Annotated[bool, typer.Option(help="Discover URLs only, write no files.")] = False,
    no_manifest: Annotated[bool, typer.Option("--no-manifest", help="Skip manifest generation.")] = False,
) -> None:
    """Mirror a website into a linked Obsidian vault."""
    import asyncio

    output_path = out or Path(f"./{_domain_slug(url)}")

    config = RunConfig(
        seed_url=url,
        out=output_path,
        depth=depth,
        max_pages=max_pages,
        include=include or [],
        exclude=exclude or [],
        same_domain=same_domain,
        subdomain_policy=subdomain_policy,
        rate=rate,
        concurrency=concurrency,
        jitter=jitter,
        min_delay=min_delay,
        max_errors=max_errors,
        ignore_robots=ignore_robots,
        render_js=render_js,
        user_agent=user_agent or RunConfig.user_agent,
        resume=resume,
        force=force,
        flat=flat,
        link_style=link_style,
        verbose=verbose,
        dry_run=dry_run,
        emit_manifest=not no_manifest,
    )

    from site2vault.logging_setup import setup_logging

    setup_logging(config)

    from site2vault.orchestrator import run

    asyncio.run(run(config))


if __name__ == "__main__":
    app()
