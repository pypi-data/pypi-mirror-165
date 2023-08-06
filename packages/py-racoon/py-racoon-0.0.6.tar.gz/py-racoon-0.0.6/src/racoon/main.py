from github import Github
import typer

from racoon.argument_types import DefaultSrcDir
from racoon.argument_types import DefaultTemplateURL
from racoon.argument_types import RequiredAccessToken
from racoon.git import init_template
from racoon.github_integration import GitHubIntegration
from racoon.template_generation import Context
from racoon.template_generation import generate_template

app = typer.Typer()


@app.command()
def generate(
    project_name: str,
    github_access_token: str = RequiredAccessToken,
    src_dir: str = DefaultSrcDir,
    template_url: str = DefaultTemplateURL,
) -> None:
    github = Github(login_or_token=github_access_token)
    config = Context(github=github, repo_name=project_name, src_dir=src_dir)
    generate_template(template_url=template_url, context=config)
    github_integration = GitHubIntegration(github=github)
    repo = github_integration.setup(repo_name=config.repo_name)
    init_template(repository=repo)


if __name__ == "__main__":
    app()
