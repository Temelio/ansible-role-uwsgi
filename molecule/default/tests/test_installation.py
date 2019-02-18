"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    """
    Check if packages are installed
    """

    packages = []

    if host.system_info.distribution in ('debian', 'ubuntu'):
        packages = ['uwsgi', 'uwsgi-plugin-python', 'uwsgi-plugin-python3']

    for package in packages:
        assert host.package(package).is_installed


def test_configuration_file(host):
    """
    Check configuration files properties
    """

    if host.system_info.distribution not in ('debian', 'ubuntu'):
        pytest.skip('Not apply to %s' % host.system_info.distribution)

    config_file = host.file('/etc/uwsgi/apps-available/default.yml')
    assert config_file.exists
    assert config_file.is_file

    config_link = host.file('/etc/uwsgi/apps-enabled/default.yml')
    assert config_link.exists
    assert config_link.is_symlink
    assert config_link.linked_to == '/etc/uwsgi/apps-available/default.yml'


def test_run_files(host):
    """
    Check run files properties
    """

    if host.system_info.distribution not in ('debian', 'ubuntu'):
        pytest.skip('Not apply to %s' % host.system_info.distribution)

    pid_file = host.file('/var/run/uwsgi/app/default/pid')
    assert pid_file.exists
    assert pid_file.is_file

    socket_file = host.file('/var/run/uwsgi/app/default/socket')
    assert socket_file.exists
    assert socket_file.is_socket
    assert socket_file.mode == 0o660


def test_service(host):
    """
    Test service started and enabled
    """

    service = ''
    if host.system_info.distribution in ('debian', 'ubuntu'):
        service = host.service('uwsgi')

    assert service.is_enabled
    assert service.is_running
