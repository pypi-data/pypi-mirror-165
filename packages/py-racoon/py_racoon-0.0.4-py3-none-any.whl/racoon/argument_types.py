import typer

RequiredAccessToken: str = typer.Option(..., envvar="GITHUB_ACCESS_TOKEN")
DefaultSrcDir: str = typer.Option("src")
DefaultTemplateURL: str = typer.Option("https://github.com/nymann/python-template.git")
