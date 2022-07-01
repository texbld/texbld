from texbld.common.exceptions import GitHubNotFound
import texbld.logger as logger
import requests


def get_github_rev(owner: str, repository: str, rev: str):
    logger.progress("Getting Commit Information from the GitHub API...")
    data = {}
    if rev is None:
        logger.progress("No revision specified, getting the latest commit...")
        api_url = f"https://api.github.com/repos/{owner}/{repository}/commits"
        res = requests.get(api_url)
        data = res.json()
        if res.status_code != 200 or len(data) == 0:
            raise GitHubNotFound(api_url)
        else:
            data = data[0]
    else:
        api_url = f"https://api.github.com/repos/{owner}/{repository}/commits/{rev}"
        res = requests.get(api_url)
        if res.status_code != 200:
            raise GitHubNotFound(api_url)
        data = res.json()

    rev = data['sha']
    logger.done(f"Got revision {rev}")
    return rev
