# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
import re
from typing import Optional

import requests

from ..utils import basepath
from .constants import CHANGELOG_LABEL_PREFIX, get_root

API_URL = 'https://api.github.com'
PR_ENDPOINT = API_URL + '/repos/{}/{}/pulls/{}'
PR_PATTERN = re.compile(r'\(#(\d+)\)')  # match something like `(#1234)` and return `1234` in a group
PR_MERGE_PATTERN = re.compile(
    r'Merge pull request #(\d+)'
)  # match something like 'Merge pull request #1234` and return `1234` in a group


def get_auth_info(config=None):
    """
    See if a personal access token was passed
    """
    gh_config = (config or {}).get('github', {})
    user = gh_config.get('user') or os.getenv('DD_GITHUB_USER')
    token = gh_config.get('token') or os.getenv('DD_GITHUB_TOKEN')
    if user and token:
        return user, token


def get_commit(repo, commit_sha, config):
    response = requests.get(
        f'https://api.github.com/repos/DataDog/{repo}/git/commits/{commit_sha}', auth=get_auth_info(config),
    )

    response.raise_for_status()
    return response.json()


def get_tag(repo, ref, config):
    response = requests.get(f'https://api.github.com/repos/DataDog/{repo}/git/tags/{ref}', auth=get_auth_info(config),)

    response.raise_for_status()
    return response.json()


def get_tags(repo, config):
    response = requests.get(f'https://api.github.com/repos/DataDog/{repo}/git/refs/tags', auth=get_auth_info(config),)

    response.raise_for_status()
    return response.json()


def get_pr_labels(pr_payload):
    labels = []
    for label in pr_payload.get('labels') or []:
        name = label.get('name')
        if name:
            labels.append(name)

    return labels


def get_pr_milestone(pr_payload):
    return (pr_payload.get('milestone') or {}).get('title', '')


def get_changelog_types(pr_payload):
    """
    Fetch the labels from the PR and process the ones related to the changelog.
    """
    changelog_labels = []
    for name in get_pr_labels(pr_payload):
        if name.startswith(CHANGELOG_LABEL_PREFIX):
            # only add the name, e.g. for `changelog/Added` it's just `Added`
            changelog_labels.append(name.split(CHANGELOG_LABEL_PREFIX)[1])

    return changelog_labels


def get_compare(base_commit, head_commit, repo, config):
    response = requests.get(
        f'https://api.github.com/repos/DataDog/{repo}/compare/{base_commit}...{head_commit}',
        auth=get_auth_info(config),
    )

    response.raise_for_status()
    return response.json()


def get_pr_of_repo(pr_num, repo, config=None, raw=False, org='DataDog'):
    response = requests.get(PR_ENDPOINT.format(org, repo, pr_num), auth=get_auth_info(config))

    if raw:
        return response
    else:
        response.raise_for_status()
        return response.json()


def get_pr(pr_num, config=None, raw=False, org='DataDog'):
    """
    Get the payload for the given PR number. Let exceptions bubble up.
    """
    repo = basepath(get_root())
    return get_pr_of_repo(pr_num, repo, config, raw, org)


def get_pr_from_hash(commit_hash, repo, config=None, raw=False):
    response = requests.get(
        f'https://api.github.com/search/issues?q=sha:{commit_hash}+repo:DataDog/{repo}', auth=get_auth_info(config),
    )

    if raw:
        return response
    else:
        response.raise_for_status()
        return response.json()


def from_contributor(pr_payload):
    """
    If the PR comes from a fork, we can safely assumed it's from an
    external contributor.
    """
    try:
        return pr_payload.get('head', {}).get('repo', {}).get('fork') is True
    except Exception:
        return False


def parse_pr_number(log_line: str) -> Optional[str]:
    # If the PR is not squashed, then it will match PR_MERGE_PATTERN
    matches = re.findall(PR_PATTERN, log_line) + re.findall(PR_MERGE_PATTERN, log_line)
    if matches:
        # If there are multiple matches, the PR id is always the latest one
        return matches[-1]
    return None


def parse_pr_numbers(git_log_lines):
    """
    Parse PR numbers from commit messages. At GitHub those have the format:

        `here is the message (#1234)`

    being `1234` the PR number.
    """
    prs = []
    for line in git_log_lines:
        pr_number = parse_pr_number(line)
        if pr_number:
            prs.append(pr_number)
    return prs
