from texbld.common.exceptions import GitHubNotFound
import texbld.logger as logger
import requests


def get_github_rev(owner: str, repository: str, rev: str):
    api_url = f"https://api.github.com/repos/{owner}/{repository}/commits/{rev}"
    logger.progress("Getting Commit Information from the GitHub API...")
    res = requests.get(api_url)
    if res.status_code != 200:
        raise GitHubNotFound(api_url)
    rev = res.json()['sha']
    logger.done(f"Got revision {rev}")
    return rev
