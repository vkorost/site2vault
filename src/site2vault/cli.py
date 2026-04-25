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


def _ensure_scheme(url: str) -> str:
    """Auto-prepend https:// if no scheme is provided."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


@app.command()
def main(
    url: Annotated[str, typer.Option("--url", "-url", help="Seed URL to crawl.")] = "",
    path: Annotated[Optional[Path], typer.Option("--path", "-path", help="Base path for output (default: current directory).")] = None,
    name: Annotated[Optional[str], typer.Option("--name", "-name", help="Output folder name (default: derived from URL).")] = None,
    depth: Annotated[int, typer.Option("--depth", "-d", help="Max crawl depth from seed.")] = 3,
    max_pages: Annotated[int, typer.Option("--max-pages", "-m", help="Hard cap on total pages.")] = 2000,
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
    flat: Annotated[bool, typer.Option("--flat", "-f", help="All notes at vault root, no subfolders.")] = False,
    link_style: Annotated[str, typer.Option(help="Wikilink style: shortest|path.")] = "shortest",
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Debug logging.")] = False,
    dry_run: Annotated[bool, typer.Option(help="Discover URLs only, write no files.")] = False,
    no_manifest: Annotated[bool, typer.Option("--no-manifest", help="Skip manifest generation.")] = False,
    json_progress: Annotated[bool, typer.Option("--json-progress", help="Emit JSONL progress to stdout for plugin consumption.")] = False,
    no_sitemap: Annotated[bool, typer.Option("--no-sitemap", help="Skip sitemap.xml discovery.")] = False,
    single: Annotated[bool, typer.Option("--single", "-s", help="Fetch only the seed URL (no crawl).")] = False,
    namespace: Annotated[Optional[str], typer.Option(help="Namespace for multi-site vaults.")] = None,
    refresh: Annotated[bool, typer.Option("--refresh", help="Re-crawl existing vault using conditional GET.")] = False,
    prune: Annotated[bool, typer.Option("--prune", help="Delete notes whose URLs return 404/410 on refresh.")] = False,
    no_static_boilerplate: Annotated[bool, typer.Option("--no-static-boilerplate", help="Skip static boilerplate stripping.")] = False,
    no_cross_page_boilerplate: Annotated[bool, typer.Option("--no-cross-page-boilerplate", help="Skip cross-page boilerplate detection.")] = False,
    boilerplate_threshold: Annotated[float, typer.Option(help="Cross-page boilerplate threshold (0.0-1.0).")] = 0.5,
    tag: Annotated[Optional[list[str]], typer.Option("--tag", help="Obsidian tag to add to all notes' frontmatter (repeatable).")] = None,
    timeout: Annotated[Optional[float], typer.Option("--timeout", help="Overall crawl timeout in minutes.")] = None,
    title_from: Annotated[str, typer.Option("--title-from", help="Title source: auto|h1|url.")] = "auto",
) -> None:
    """Mirror a website into a linked Obsidian vault.

    Usage: site2vault --url URL [--path PATH] [--name NAME] [OPTIONS]
    """
    import asyncio

    # Validate required --url
    if not url:
        typer.echo("Error: --url is required.\n")
        typer.echo("Usage: site2vault --url URL [--path PATH] [--name NAME] [OPTIONS]")
        typer.echo("\nExample: site2vault --url docs.example.com --path C:\\Obsidian\\Vault --name \"My Docs\"")
        raise SystemExit(1)

    # Auto-prepend https:// if needed
    url = _ensure_scheme(url)

    # Validate --single constraints
    if single:
        if depth != 3 and depth != 0:
            raise typer.BadParameter("--single is incompatible with --depth (other than 0)")
        if max_pages != 2000 and max_pages != 1:
            raise typer.BadParameter("--single is incompatible with --max-pages (other than 1)")
        depth = 0
        max_pages = 1

    # Validate --title-from
    if title_from not in ("auto", "h1", "url"):
        raise typer.BadParameter("--title-from must be one of: auto, h1, url")

    # Resolve output path: --path / --name
    folder_name = name or _domain_slug(url)
    base_path = path or Path(".")
    output_path = base_path / folder_name

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
        json_progress=json_progress,
        use_sitemap=not no_sitemap and not single,
        single=single,
        namespace=namespace,
        refresh=refresh,
        prune=prune,
        static_boilerplate=not no_static_boilerplate,
        cross_page_boilerplate=not no_cross_page_boilerplate,
        boilerplate_threshold=boilerplate_threshold,
        tags=tag or [],
        timeout=timeout,
        title_from=title_from,
    )

    from site2vault import exit_codes
    from site2vault.logging_setup import setup_logging

    setup_logging(config)

    from site2vault.orchestrator import run

    try:
        code = asyncio.run(run(config))
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else exit_codes.FATAL
    except KeyboardInterrupt:
        code = exit_codes.USER_ABORT
    except Exception:
        code = exit_codes.FATAL

    raise SystemExit(code)


if __name__ == "__main__":
    app()
