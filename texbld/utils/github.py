import json
from texbld.exceptions import GitHubNotFound
import texbld.logger as logger
from texbld.globals import http


def get_github_rev(owner: str, repository: str, rev: str):
    logger.progress("Getting Commit Information from the GitHub API...")
    data = {}
    if rev is None:
        logger.progress("No revision specified, getting the latest commit...")
        api_url = f"https://api.github.com/repos/{owner}/{repository}/commits"
        res = http.request("GET", api_url)
        data = json.loads(res.data.decode("utf-8"))
        if res.status != 200 or len(data) == 0:
            raise GitHubNotFound(api_url)
        else:
            data = data[0]
    else:
        api_url = f"https://api.github.com/repos/{owner}/{repository}/commits/{rev}"
        res = http.request("GET", api_url)
        if res.status != 200:
            raise GitHubNotFound(api_url)
        data = json.loads(res.data.decode("utf-8"))

    rev = data['sha']
    logger.done(f"Got revision {rev}")
    return rev
