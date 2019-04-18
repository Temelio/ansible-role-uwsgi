# uwsgi

[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-uwsgi/master.svg?label=travis_master)](https://travis-ci.org/Temelio/ansible-role-uwsgi)
[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-uwsgi/develop.svg?label=travis_develop)](https://travis-ci.org/Temelio/ansible-role-uwsgi)
[![Updates](https://pyup.io/repos/github/Temelio/ansible-role-uwsgi/shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-uwsgi/)
[![Python 3](https://pyup.io/repos/github/Temelio/ansible-role-uwsgi/python-3-shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-uwsgi/)
[![Ansible Role](https://img.shields.io/ansible/role/37790.svg)](https://galaxy.ansible.com/Temelio/uwsgi/)
[![GitHub tag](https://img.shields.io/github/tag/temelio/ansible-role-uwsgi.svg)](https://github.com/Temelio/ansible-role-uwsgi/tags)

Install uWSGI package.

## Requirements

This role requires Ansible 2.4 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Debian Stretch
- Ubuntu Xenial
- Ubuntu Bionic

and use:
- Ansible 2.4.x
- Ansible 2.5.x
- Ansible 2.6.x
- Ansible 2.7.x

### Running tests

#### Using Docker driver

```
$ tox
```
You can also configure molecule options and molecule command using environment variables:
* `MOLECULE_OPTIONS` Default: "--debug"
* `MOLECULE_COMMAND` Default: "test"

```
$ MOLECULE_OPTIONS='' MOLECULE_COMMAND=converge tox
```

## Role Variables

### Default role variables

You have to change: uid/gid to something like: www-data or nginx
You can enable systemd config for uwsgi-emperor install

``` yaml
# Installation vars
uwsgi_install_mode: 'package'
uwsgi_install_emperor: False
uwsgi_packages: "{{ _uwsgi_packages }}"
uwsgi_emperor_packages: "{{ _uwsgi_emperor_packages }}"
uwsgi_service_name: 'uwsgi'
uwsgi_emperor_service_name: 'uwsgi-emperor'
uwsgi_is_systemd_managed: False

# Config vars
uwsgi_emperor_vassals_config_path: "{{ _uwsgi_emperor_vassals_config_path }}"
uwsgi_config_available_path: "{{ _uwsgi_config_available_path }}"
uwsgi_config_enabled_path: "{{ _uwsgi_config_enabled_path }}"
uwsgi_config_log_path: "{{ _uwsgi_config_log_path }}"
uwsgi_config_run_path: "{{ _uwsgi_config_run_path }}"
uwsgi_apps_defaults: "{{ _uwsgi_apps_defaults }}"
uwsgi_emperor_vassals_path: '/etc/uwsgi-emperor/vassals'
uwsgi_emperor_user: 'nobody'
uwsgi_emperor_group: 'users'
uwsgi_emperor:
  - service_name: 'uwsgi-emperor'
    src: "{{ role_path }}/templates/emperor.ini.j2"
    dest: '/etc/uwsgi-emperor/emperor.ini'
    owner: 'root'
    group: 'root'
    mode: '0644'
    state: 'started'
    enabled: True
    config:
      uwsgi:
        autoload: True
        master: True
        workers: 2
        no-orphans: True
        log-date: True
        uid: "{{ uwsgi_emperor_user }}"
        gid: "{{ uwsgi_emperor_group }}"
        emperor: "{{ uwsgi_emperor_vassals_path }}"

# Handler management
uwsgi_restart_handler_enabled: True

# systemd management
init_d_disable:
  - name: "{{ uwsgi_emperor[0].service_name }}"
    enabled: False
uwsgi_systemd:
  - src: "{{ role_path }}/templates/systemd.service.j2"
    dest: "{{ _systemd_files_path }}/{{ uwsgi_emperor[0].service_name }}.service"
    owner: 'root'
    group: 'root'
    mode: '0644'
    config:
      Unit:
        Description: 'uWSGI Emperor'
        After: 'syslog.target'
      Service:
        ExecStart: '/usr/bin/uwsgi --ini /etc/uwsgi-emperor/emperor.ini'
        RuntimeDirectory: 'uwsgi'
        Restart: 'always'
        KillSignal: 'SIGQUIT'
        Type: 'notify'
        StandardError: 'syslog'
        NotifyAccess: 'all'
      Install:
        WantedBy: 'multi-user.target'

```

### Debian family variables

``` yaml
# Package management
_uwsgi_packages:
  - name: 'uwsgi'
  - name: 'uwsgi-plugin-python'
  - name: 'uwsgi-plugin-python3'

# Configuration management
_uwsgi_configuration_available_path: '/etc/uwsgi/apps-available'
_uwsgi_configuration_enabled_path: '/etc/uwsgi/apps-enabled'
_uwsgi_configuration_log_path: '/var/log/uwsgi'
_uwsgi_configuration_run_path: '/var/run/uwsgi'
_uwsgi_apps_defaults:
  uwsgi:
    autoload: true
    master: true
    workers: 2
    no-orphans: true
    pidfile: "{{ uwsgi_configuration_run_path ~ '/%(deb-confnamespace)/%(deb-confname)/pid' }}"
    socket: "{{ uwsgi_configuration_run_path ~ '/%(deb-confnamespace)/%(deb-confname)/socket' }}"
    logto: "{{ uwsgi_configuration_log_path ~ '/%(deb-confnamespace)/%(debconfname).log' }}"
    chmod-socket: 660
    log-date: true
    uid: www-data
    gid: www-data
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: Temelio.uwsgi }
```

## License

MIT

## Author Information

Alexandre Chaussier (for infOpen company)
Lise Machetel (for Temelio company)
- https://temelio.com
