"""Run configuration dataclass."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunConfig:
    seed_url: str
    out: Path = Path(".")
    depth: int = 3
    max_pages: int = 2000
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    same_domain: bool = True
    subdomain_policy: str = "include"  # strict | include | any
    rate: float = 1.0
    concurrency: int = 2
    jitter: float = 0.3
    min_delay: float = 0.5
    max_errors: int = 10
    ignore_robots: bool = False
    render_js: bool = False
    user_agent: str = "site2vault/0.1.0 (+https://github.com/user/site2vault; personal archival use)"
    resume: bool = True
    force: bool = False
    flat: bool = False
    link_style: str = "shortest"  # shortest | path
    verbose: bool = False
    dry_run: bool = False
    emit_manifest: bool = True
    json_progress: bool = False
    use_sitemap: bool = True
    single: bool = False
    static_boilerplate: bool = True
    cross_page_boilerplate: bool = True
    boilerplate_threshold: float = 0.5
    refresh: bool = False
    prune: bool = False
    namespace: str | None = None
