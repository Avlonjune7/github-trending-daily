#!/usr/bin/env python3
"""Collect public GitHub repository metrics; keep issue snapshots unchanged."""
import concurrent.futures
import datetime
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def collect(repo):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError(f"Invalid repository: {repo}")
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}"], check=True, capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    if data.get("private", True):
        raise ValueError(f"Only public repositories are allowed: {repo}")
    return repo, {
        "totalStars": data["stargazers_count"],
        "forks": data["forks_count"],
        "avatarUrl": data["owner"]["avatar_url"],
        "ownerLogin": data["owner"]["login"],
        "ownerType": data["owner"]["type"],
        "collectedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sourceUrl": f"https://api.github.com/repos/{repo}",
    }

def main():
    repos = sorted({
        project["repo"]
        for path in (ROOT / "data/issues").glob("*.json")
        for project in json.loads(path.read_text())["projects"]
    })
    # Write only after every request succeeds, preserving the last complete snapshot.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        metrics = dict(pool.map(collect, repos))
    output = ROOT / "data/repo_metrics.json"
    temporary = output.with_suffix(".tmp")
    temporary.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(output)
    print(f"Collected {len(metrics)} public repositories → {output.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
