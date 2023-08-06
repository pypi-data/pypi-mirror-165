import os
import pytest

from ..gitlab_job import GitlabJob

def test_config(monkeypatch):
    monkeypatch.setenv('USER', 'ALEX')

    gj = GitlabJob()
    assert gj.config(['USER']) == {'USER': 'ALEX'}

def test_config_to_docker_service_env(monkeypatch):
    monkeypatch.setenv('USER', 'ALEX')
    monkeypatch.setenv('PASS', 'SECRET')

    gj = GitlabJob()

    # unstrict
    assert gj.config_to_docker_service_env(['USER', 'PASS', 'TIMEOUT']) == ['USER=ALEX', 'PASS=SECRET']

    # strict, should raise because ENV['TIMEOUT'] is unset
    with pytest.raises(Exception):
        gj.config_to_docker_service_env(['USER', 'PASS', 'TIMEOUT'], True)
