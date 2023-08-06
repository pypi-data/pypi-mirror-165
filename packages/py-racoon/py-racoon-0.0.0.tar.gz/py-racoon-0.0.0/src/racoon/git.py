import os
import subprocess

from github.Repository import Repository


def _git(*command: str) -> None:
    subprocess.run(["git", *command])


def init_template(repository: Repository) -> None:
    os.chdir(repository.name)
    _git("init")
    _git("add", ".")
    _git("commit", "-m", ":tada: Initialize template from nymann/python-template")
    _git("remote", "add", "origin", repository.ssh_url)
    _git("push", "-u", "origin", "master")
