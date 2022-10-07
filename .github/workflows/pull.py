import requests
import os

github_token = (os.environ['ENV_SECRET'])

upstream = 'https://api.github.com/repos/TalKatz1/sync_test_source'
fork = 'https://api.github.com/repos/AxoniusTK/sync_test_dest'

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_token}',
    'Content-Type': 'application/x-www-form-urlencoded',
}


def get_latest_tag_from_upstream(url):
    response = requests.get(url, headers=headers)
    return response.json()[0].get('name')


def get_latest_tag_from_fork(url):
    response = requests.get(url, headers=headers)
    return response.json()[0].get('name')


def trigger_workflow():
    url = fork + '/actions/workflows'
    resp = requests.get(url, headers)
    for wf in resp.json().get('workflows'):
        if wf.get('name') == 'Upstream Sync':
            wf_post_url = wf.get('url') + '/dispatches'
    data = {"ref": "main"}
    print(f'running workflow {wf_post_url}')
    response = requests.post(wf_post_url, headers=headers, json=data)
    print(response)


fork_latest_tag = get_latest_tag_from_fork(fork + '/tags')
upstream_lates_tag = get_latest_tag_from_upstream(upstream + '/tags')
print("Fork tag: ", fork_latest_tag)
print("Upstream tag: ", upstream_lates_tag)

if fork_latest_tag != upstream_lates_tag:
    print("Fork is behind, updating")
    trigger_workflow()
else:
    print("Fork is up to date")
