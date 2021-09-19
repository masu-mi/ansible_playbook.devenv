#!/usr/bin/python
# vim: fileencoding=utf-8

from ansible.module_utils.basic import AnsibleModule
import urllib.request
import json
import os.path

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Masumi Kanai'
}

DOCUMENTATION = '''
---
module: github_asset

short_description: Download GitHub's release asset

version_added: "0.1"

description:
    - "Download GitHub's release asset"

options:
    token:
        description:
            - GitHub access token
        required: false
    repository:
        description:
            - repository name: e.g. `masu-mi/ansible-playbook`
        required: true
    asset_name:
        description:
            - target asset file name
        required: true
    tag:
        description:
            - Control to demo if the result of this module is changed or not
        required: false
    base_url:
        description:
            - base_url: e.g. `https://api.github.com/repos`
        required: false
    dest:
        description:
            - dest path in controlled hosts
        required: true
requirements:
  python >= 3.5

extends_documentation_fragment:

author:
    - Who am I?
'''

EXAMPLES = '''
# Pass in a message
- name: Download nidd-dra
  github_assets:
    token: "{{ lookup('env', 'GITHUB_TOKEN') }}"
    repository: "masu-mi/test-repo"
    tag: "v0.1.15"
    asset_name: "nidd-dra_0.1.15_linux_amd64.tar.gz"
    dest: "/tmp/"
'''

RETURN = '''
asset_url:
    description: The asset url to downlaod the target asset
    type: str
dest_file_path:
    description: The downloaded file path
    type: str
'''


def run_module():
    module_args = dict(
        token=dict(type='str', required=False, default=None),
        repository=dict(type='str', required=True),
        asset_name=dict(type='str', required=True),
        tag=dict(type='str', required=False, default='latest'),
        base_url=dict(type='str', required=False,
                      default='https://api.github.com/repos'),
        dest=dict(type='str', required=True)
    )
    result = dict(changed=False, asset_url='', dest_file_path='')

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    repo = GitHubReleases(module.params['base_url'],
                          module.params['token'],
                          module.params['repository'])

    (result['asset_url'],
     result['dest_file_path'],
     failed) = repo.download_asset(
        module.params['dest'],
        module.params['tag'],
        module.params['asset_name'])
    if failed:
        module.fail_json(msg='You requested this to fail', **result)
    result['changed'] = True

    module.exit_json(**result)


class GitHubReleases():

    def __init__(self, base_url, token, repository):
        self.base_url = base_url
        self.token = token
        self.repository = repository

    def download_asset(self, dest, tag, asset_name):
        """
        download_asset
        """
        headers = {'Accept': 'application/octet-stream'}
        if self.token is not None:
            headers['Authorization'] = 'token {}'.format(self.token)
        (asset_url, failed) = self.get_asset_url(tag, asset_name)
        if failed:
            return ("", "", True)

        req = urllib.request.Request(asset_url, headers=headers)
        file_path = dest_file_path(dest, asset_name)

        with urllib.request.urlopen(req) as res:
            with open(file_path, mode='wb') as dest_file:
                dest_file.write(res.read())
        return (asset_url, file_path, False)

    def get_asset_url(self, tag, asset_name):
        url = '{}/{}/releases/tags/{}'.format(
            self.base_url, self.repository, tag)
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token is not None:
            headers['Authorization'] = 'token {}'.format(self.token)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            info = json.loads(res.read())
            asset_urls = [item['url']
                          for item in info["assets"]
                          if item["name"] == asset_name]
            if len(asset_urls) == 0:
                return ("", True)
            return (asset_urls[0], False)


def dest_file_path(dest, asset_name):
    if os.path.isdir(dest):
        dest = dest + asset_name
    return dest


def main():
    run_module()


if __name__ == '__main__':
    main()
