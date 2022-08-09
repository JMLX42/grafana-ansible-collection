# Ansible Collection - grafana.grafana

This collection contains modules and plugins to assist in automating managing of resources in Grafana with Ansible.

## Installation and Usage

### Requirements
The collection is tested and supported with:

* ansible >= 2.10.0
* python >= 3.10

## Installing the collection from Ansible Galaxy

Before using the Grafana collection, you need to install it with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install grafana.grafana
```

You can also include it in a `requirements.yml` file and install it via ansible-galaxy collection install -r `requirements.yml`, using the format:

```yaml
---
collections:
  - name: grafana.grafana
```
A specific version of the collection can be installed by using the version keyword in the requirements.yml file:

```yaml
---
collections:
  - name: amazon.aws
    version: 0.0.1
```
## Using this collection

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `grafana.grafana.cloud_stack`:
```yaml
- name: Using grafana collection
  hosts: localhost
  tasks:
    - name: Create a Grafana Cloud stack
      grafana.grafana.cloud_stack:
        name: mystack
        stack_slug: mystack
        org_slug: myorg
        cloud_api_key: "{{ cloud_api_key }}"
        region: eu
        state: present
```

or you can add full namespace and collection name in the `collections` element in your playbook
```yaml
- name: Using grafana collection
  hosts: localhost
  collection:
    - grafana.grafana
  tasks:
    - name: Create a Grafana Cloud stack
      cloud_stack:
        name: mystack
        stack_slug: mystack
        org_slug: myorg
        cloud_api_key: "{{ cloud_api_key }}"
        region: eu
        state: present
```

## Contributing
We are accepting Github pull requests and issues. There are many ways in which you can participate in the project, for example:

* Submit bugs and feature requests, and help us verify them
* Submit and review source code changes in Github pull requests
* Add new modules for more Grafana resources

## Testing and Development

If you want to develop new content for this collection or improve what is already
here, the easiest way to work on the collection is to clone it into one of the configured
[`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths),
and work on it there.

### Testing with `ansible-test`

We use `ansible-test` for sanity.

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## License

GPL-3.0-or-later