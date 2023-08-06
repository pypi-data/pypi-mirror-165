import re

from cookiecutter.main import cookiecutter
from github import Github


def project_name(safe_repo_name: str) -> str:
    return " ".join(word.capitalize() for word in safe_repo_name.split("-"))


def sanitize_repo_name(unsafe_repo_name: str) -> str:
    word = unsafe_repo_name.strip(" -")
    word = re.sub(r"[\ \_]+", "-", word)
    word = re.sub("([A-Z]+)([A-Z][a-z])", r"\1-\2", word)
    word = re.sub(r"([a-z\d])([A-Z])", r"\1-\2", word)
    return word.lower()


def package_name(safe_repo_name: str) -> str:
    return safe_repo_name.replace("-", "_")


class Context:
    def __init__(self, github: Github, repo_name: str, src_dir: str) -> None:
        self._user = github.get_user()
        self.repo_name = sanitize_repo_name(repo_name)
        self._project_name = project_name(safe_repo_name=self.repo_name)
        self._package_name = package_name(safe_repo_name=self.repo_name)
        self._src_dir = src_dir

    def dict(self) -> dict[str, str]:
        return {
            "author_email": self._user.email,
            "author_name": self._user.name,
            "git_registry": "https://github.com/",
            "git_registry_account": self._user.login,
            "package_name": self._package_name,
            "project_name": self._project_name,
            "repo_name": self.repo_name,
            "src_dir": self._src_dir,
        }


def generate_template(template_url: str, context: Context) -> None:
    cookiecutter(
        template=template_url,
        extra_context=context.dict(),
        no_input=True,
    )
