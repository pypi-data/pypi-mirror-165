from github import Github
from github.Repository import Repository


class GitHubIntegration:
    def __init__(self, github: Github) -> None:
        self._user = github.get_user()

    def setup(self, repo_name: str) -> Repository:
        repo = self._user.create_repo(name=repo_name)
        repo.create_secret("PYPI_API_TOKEN", "")
        repo.create_secret("DOCKER_TOKEN", "")
        repo.create_secret("DOCKER_USER", "")
        self._create_license_issue(repo=repo)
        return repo

    def _create_license_issue(self, repo: Repository) -> None:
        license_url = f"{repo.html_url}/community/license/new?branch=master&filename=LICENSE"
        repo.create_issue(
            title="Determine license",
            body=f"Pick a license: {license_url}",
            assignee=self._user.login,
        )
