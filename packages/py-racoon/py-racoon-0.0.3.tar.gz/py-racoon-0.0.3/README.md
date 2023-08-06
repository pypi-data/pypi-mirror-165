# Racoon

View on [PyPI](https://pypi.org/project/py-racoon)

## Installation

```sh
pip install py-racoon
```

## Usage

```sh
$ racoon --help
Usage: racoon [OPTIONS] PROJECT_NAME

Arguments:
  PROJECT_NAME  [required]

Options:
  --github-access-token TEXT      [env var: GITHUB_ACCESS_TOKEN; required]
  --src-dir TEXT                  [default: src]
  --template-url TEXT             [default: https://github.com/nymann/python-
                                  template.git]
```

### Example

```sh
# Export your github access token as an environment variable, can also be provided via --github-access-token
export GITHUB_ACCESS_TOKEN='YOUR_ACCESS_TOKEN'

# Create a new project "my-project" which will be created under https://github.com/YOUR_USERNAME/my-project
racoon my-project
```

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
