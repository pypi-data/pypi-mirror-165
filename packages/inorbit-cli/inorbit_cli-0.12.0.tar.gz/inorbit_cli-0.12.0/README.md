# InOrbit CLI

Welcome to the InOrbit Command Line Interface.

## Installing

[https://pypi.org/project/inorbit-cli/](https://pypi.org/project/inorbit-cli/)

Make sure you deactivated the development virtual environment or you are using a different one with no `inorbit` python package installed.

```bash
pip install inorbit-cli
```

## Usage

The CLI requires an API key for authenticating against InOrbit's platform. For obtaining it, please go to the [InOrbit developer console](https://console.inorbit.ai/).

```bash
$ export INORBIT_CLI_API_KEY="company_api_key" 
$ inorbit --help
Usage: inorbit [OPTIONS] COMMAND [ARGS]...

  InOrbit Command Line Interface tool

  The InOrbit CLI tool enable roboteers to interact with the InOrbit Cloud
  platform in order to manage robot configuration as code.

Options:
  --help  Show this message and exit.

Commands:
  describe
  get
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)
