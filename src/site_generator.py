from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from src.config import Config, SITE_DIR, TEMPLATES_DIR
from src.models import Listing


def generate_site(listings: list[Listing], config: Config):
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    static_src = TEMPLATES_DIR / "static"
    static_dst = SITE_DIR / "static"
    if static_src.exists():
        if static_dst.exists():
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("index.html")

    active = [l for l in listings if l.is_active]
    active.sort(key=lambda l: (l.score or 0), reverse=True)

    neighborhoods = sorted(set(l.neighborhood for l in active if l.neighborhood))
    sources = sorted(set(l.source for l in active if l.source))

    avg_score = 0.0
    scored = [l for l in active if l.score is not None]
    if scored:
        avg_score = sum(l.score for l in scored) / len(scored)

    new_count = sum(1 for l in active if l.status == "new")

    listings_json = json.dumps([l.to_dict() for l in active], default=str)

    html = template.render(
        listings=active,
        listings_json=listings_json,
        neighborhoods=neighborhoods,
        sources=sources,
        stats={
            "total": len(active),
            "new_count": new_count,
            "avg_score": round(avg_score, 1),
        },
        config=config,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    output_path = SITE_DIR / "index.html"
    output_path.write_text(html)
