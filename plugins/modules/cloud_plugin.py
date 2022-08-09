#!/usr/bin/python

DOCUMENTATION = '''
---
module: cloud_plugin
author:
  - Ishan Jain (@ishanjainn)
version_added: "0.0.1"
short_description: Manage Grafana Cloud Plugins
description:
  - Create, Update and delete Grafana Cloud stacks using Ansible.
options:
  name:
    description:
      - Name of the plugin, e.g. grafana-github-datasource .
    type: str
    required: true
  version:
    description:
      - Version of the plugin to install. Defaults to latest.
    type: str
    default: latest
  stack_slug:
    description:
      - Name of the Grafana Cloud stack to which the plugin will be added
    type: str
    required: true
  cloud_api_key:
    description:
      - CLoud API Key to authenticate with Grafana Cloud.
    type: str
    required : true
  state:
    description:
      - State for the Grafana CLoud stack.
    type: str
    default: present
    choices: [ present, absent ]
'''

EXAMPLES = '''
- name: Create/Update a plugin
  cloud_plugin:
    name: grafana-github-datasource
    version: 1.0.14
    stack_slug: "{{ stack_slug }}"
    cloud_api_key: "{{ grafana_cloud_api_key }}"
    state: present

- name: Delete a Grafana Cloud stack
  cloud_plugin:
    name: grafana-github-datasource
    stack_slug: "{{ stack_slug }}"
    cloud_api_key: "{{ grafana_cloud_api_key }}"
    state: absent
'''

RETURN = r'''
  current_version:
    description: Current version of the plugin
    returned: On success
    type: str
  latest_version:
    description: Latest version available for the plugin
    returned: On success
    type: str
  pluginId:
    description: Id for the Plugin
    returned: On success
    type: int
  pluginName:
    description: Name of the plugin
    returned: On success
    type: str
  pluginSlug:
    description: Slug for the Plugin
    returned: On success
    type: str
'''

from ansible.module_utils.basic import AnsibleModule
import requests


def present_cloud_plugin(module):
    body = {
        'plugin': module.params['name'],
        'version': module.params['version']
    }

    api_url = 'https://grafana.com/api/instances/' + module.params['stack_slug'] + '/plugins'

    result = requests.post(api_url, json=body, headers={"Authorization": 'Bearer ' + module.params['cloud_api_key']})

    if result.status_code == 200:
        return False, True, result.json()
    elif result.status_code == 409:
        api_url = 'https://grafana.com/api/instances/' + module.params['stack_slug'] + '/plugins/' + module.params[
            'name']
        result = requests.post(api_url, json={'version': module.params['version']},
                               headers={"Authorization": 'Bearer ' + module.params['cloud_api_key']})

        return False, True, result.json()
    else:
        return True, False, {"status": result.status_code, 'response': result.json()['message']}


def absent_cloud_plugin(module):
    api_url = 'https://grafana.com/api/instances/' + module.params['stack_slug'] + '/plugins/' + module.params['name']

    result = requests.delete(api_url, headers={"Authorization": 'Bearer ' + module.params['cloud_api_key']})

    if result.status_code == 200:
        return False, True, result.json()
    else:
        return True, False, {"status": result.status_code, 'response': result.json()['message']}


def main():
    module_args = dict(
        name=dict(type='str', required=True),
        version=dict(type='str', required=False, default='latest'),
        stack_slug=dict(type='str', required=True),
        cloud_api_key=dict(type='str', required=True),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
    )

    choice_map = {
        "present": present_cloud_plugin,
        "absent": absent_cloud_plugin,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module)

    if not is_error:
        module.exit_json(changed=has_changed, pluginId=result['pluginId'], pluginName=result['pluginName'], pluginSlug=result['pluginSlug'], current_version=result['version'], latest_version=result['latestVersion'])
    else:
        module.fail_json(msg=result)


if __name__ == '__main__':
    main()