# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codemagic',
 'codemagic.apple',
 'codemagic.apple.app_store_connect',
 'codemagic.apple.app_store_connect.apps',
 'codemagic.apple.app_store_connect.builds',
 'codemagic.apple.app_store_connect.provisioning',
 'codemagic.apple.app_store_connect.testflight',
 'codemagic.apple.app_store_connect.versioning',
 'codemagic.apple.resources',
 'codemagic.cli',
 'codemagic.cli.argument',
 'codemagic.google_play',
 'codemagic.google_play.resources',
 'codemagic.mixins',
 'codemagic.models',
 'codemagic.models.altool',
 'codemagic.models.application_package',
 'codemagic.models.junit',
 'codemagic.models.simulator',
 'codemagic.models.table',
 'codemagic.models.xctests',
 'codemagic.shell_tools',
 'codemagic.tools',
 'codemagic.tools._app_store_connect',
 'codemagic.tools._app_store_connect.action_groups',
 'codemagic.tools._app_store_connect.actions',
 'codemagic.tools._xcode_project',
 'codemagic.tools.android_keystore',
 'codemagic.tools.google_play',
 'codemagic.tools.google_play.action_groups',
 'codemagic.tools.google_play.actions',
 'codemagic.utilities',
 'codemagic.utilities.auditing']

package_data = \
{'': ['*'], 'codemagic': ['data/jars/*', 'scripts/*']}

install_requires = \
['cryptography',
 'google-api-python-client>=1.7.12',
 'httplib2>=0.19.0',
 'oauth2client>=4.1.3',
 'psutil>=5.8.0',
 'pyjwt>=2.4.0,<3.0.0',
 'pyopenssl>=19.0',
 'requests>=2.25']

entry_points = \
{'console_scripts': ['android-app-bundle = '
                     'codemagic.tools:AndroidAppBundle.invoke_cli',
                     'android-keystore = '
                     'codemagic.tools:AndroidKeystore.invoke_cli',
                     'app-store-connect = '
                     'codemagic.tools:AppStoreConnect.invoke_cli',
                     'codemagic-cli-tools = '
                     'codemagic.tools:CodemagicCliTools.invoke_cli',
                     'git-changelog = codemagic.tools:GitChangelog.invoke_cli',
                     'google-play = codemagic.tools:GooglePlay.invoke_cli',
                     'keychain = codemagic.tools:Keychain.invoke_cli',
                     'universal-apk = '
                     'codemagic.tools:UniversalApkGenerator.invoke_cli',
                     'xcode-project = codemagic.tools:XcodeProject.invoke_cli']}

setup_kwargs = {
    'name': 'codemagic-cli-tools',
    'version': '0.31.3',
    'description': 'CLI tools used in Codemagic builds',
    'long_description': '# Codemagic CLI Tools\n\nCodemagic CLI Tools are a set of command-line utilities for managing Android and iOS app builds,\ncode signing, and deployment. The tools are used to power mobile app builds at [codemagic.io](https://codemagic.io) but can be also used in other virtual environments or locally.\n\n# Installing\n\nCodemagic CLI Tools are available on [PyPI](https://pypi.org/project/codemagic-cli-tools/)\nand can be installed and updated using [pip](https://pip.pypa.io/en/stable/getting-started/).\n\n```\npython -m pip install codemagic-cli-tools\n```\n\nThe package requires Python version 3.7+.\n\n# Command line usage\n\nInstalling the package adds the following executables to your path:\n\n- [`android-app-bundle`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/android-app-bundle/README.md)\n- [`android-keystore`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/android-keystore/README.md)\n- [`app-store-connect`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/app-store-connect/README.md)\n- [`codemagic-cli-tools`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/codemagic-cli-tools/README.md)\n- [`git-changelog`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/git-changelog/README.md)\n- [`google-play`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/google-play/README.md)\n- [`keychain`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/keychain/README.md)\n- [`universal-apk`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/universal-apk/README.md)\n- [`xcode-project`](https://github.com/codemagic-ci-cd/cli-tools/blob/master/docs/xcode-project/README.md)\n\nOnline documentation for all installed executables can be found under\n[`docs`](https://github.com/codemagic-ci-cd/cli-tools/tree/master/docs#cli-tools).\n\nAlternatively, you could see the documentation by using `--help` option from command line:\n\n```bash\n<command> --help\n```\nto see general description and subcommands for the tool, or\n\n```bash\n<command> <subcommand> --help\n```\nto get detailed information of the subcommand.\n\n**For example:**\n\n```\n$ keychain create --help\nusage: keychain create [-h] [--log-stream {stderr,stdout}] [--no-color] [--version] [-s] [-v] [-pw PASSWORD] [-p PATH]\n\nCreate a macOS keychain, add it to the search list\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nOptional arguments for command create:\n  -pw PASSWORD, --password PASSWORD\n                        Keychain password. Alternatively to entering PASSWORD in plaintext, it may also be specified using the "@env:" prefix followed by an environment variable name, or the "@file:" prefix followed by a path to the file containing the value. Example: "@env:<variable>" uses the value in the environment variable named "<variable>", and "@file:<file_path>" uses the value from the file at "<file_path>". [Default: \'\']\n\nOptions:\n  --log-stream {stderr,stdout}\n                        Log output stream. [Default: stderr]\n  --no-color            Do not use ANSI colors to format terminal output\n  --version             Show tool version and exit\n  -s, --silent          Disable log output for commands\n  -v, --verbose         Enable verbose logging for commands\n\nOptional arguments for keychain:\n  -p PATH, --path PATH  Keychain path. If not provided, the system default keychain will be used instead\n```\n\n# Usage from Python\n\nIn addition to the command line interface, the package also provides a mirroring Python API.\nAll utilities that are available as CLI tools are accessible from Python in package\n[`codemagic.tools`](https://github.com/codemagic-ci-cd/cli-tools/blob/v0.28.0/src/codemagic/tools/__init__.py).\nThe CLI actions are instance methods that are decorated by the [`action`](https://github.com/codemagic-ci-cd/cli-tools/blob/v0.28.0/src/codemagic/cli/cli_app.py#L385)\ndecorator. For example, you can use the [`Keychain`](https://github.com/codemagic-ci-cd/cli-tools/blob/v0.28.0/src/codemagic/tools/keychain.py#L111)\ntool from Python source as follows:\n\n```python\nIn [1]: from pathlib import Path\n\nIn [2]: from codemagic.tools import Keychain\n\nIn [3]: Keychain().get_default()\nOut[3]: PosixPath(\'/Users/priit/Library/Keychains/login.keychain-db\')\n\nIn [4]: keychain = Keychain(Path("/tmp/new.keychain"))\n\nIn [5]: keychain.create()\nOut[5]: PosixPath(\'/tmp/new.keychain\')\n\nIn [6]: keychain.make_default()\n\nIn [7]: Keychain().get_default()\nOut[7]: PosixPath(\'/private/tmp/new.keychain\')\n```\n\n# Development\n\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies. Before starting development, please ensure that your\nmachine has Poetry available. Installation instructions can be found from their\n[docs](https://python-poetry.org/docs/#installation).\n\nAssuming you\'ve already cloned the [repository](https://github.com/codemagic-ci-cd/cli-tools/)\nitself, or a fork of it, you can get started by running\n\n```shell\npoetry install\n```\n\nThis will install all required dependencies specified in the `poetry.lock` file.\n\nThe source code of the project lives inside the `src` directory and tests are\nimplemented in the `tests` directory.\n\n### Code style and formatting\n\nAutomatic formatting checks are enforced using [Flake8](https://flake8.pycqa.org/en/latest/)\nand [isort](https://pycqa.github.io/isort/).\n\nInvoke Flake8 checks from repository root directory with\n\n```shell\npoetry run flake8 .\n```\n\nEnsure that all imports are ordered as expected using isort from the repository root with\n\n```shell\npoetry run isort --check-only .\n```\n\n### Static type checks\n\nA huge portion of the Python source code has type hints, and all public methods or functions\nare expected to have type hints. Static type checks of the source code are performed using\n[Mypy](http://mypy-lang.org/) from the repository root by running\n\n```shell\npoetry run mypy src\n```\n\n### Running tests\n\n[Pytest](https://docs.pytest.org/en/stable/) is used as the framework. As mentioned above,\ntests are stored in the `tests` directory, separated from package source code. Test code layout\nmirrors the structure of the `codemagic` package in the source directory.\n\nTests can be started by running the following command from the repository root:\n\n```shell\npoetry run pytest\n```\n\nNote that tests that target [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi) or\n[Google Play Developer API](https://developers.google.com/android-publisher) live endpoints\nare skipped by default for obvious reasons. They can be enabled (either for TDD or other reasons)\nby setting the environment variable `RUN_LIVE_API_TESTS` to any non-empty value.\n\nNote that for the tests to run successfully, you\'d have to define the following environment variables:\n- For App Store Connect:\n    ```shell\n    export TEST_APPLE_KEY_IDENTIFIER=...  # Key ID\n    export TEST_APPLE_ISSUER_ID=...  # Issued ID\n    ```\n    And either of the two:\n    ```bash\n    export TEST_APPLE_PRIVATE_KEY_PATH=...  # Path to private key in .p8 format\n    export TEST_APPLE_PRIVATE_KEY_CONTENT=...  # Content of .p8 private key\n    ```\n  Those can be obtained from [App Store Connect -> Users and Access -> Keys](https://appstoreconnect.apple.com/access/api).\n  For more information follow Apple\'s official documentation about [Creating API Keys for App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi/creating_api_keys_for_app_store_connect_api).\n\n- For Google Play:\n    ```shell\n    export TEST_GCLOUD_PACKAGE_NAME=... # Package name (Ex: com.google.example)\'\n    ```\n    And either of the two:\n    ```shell\n    export TEST_GCLOUD_SERVICE_ACCOUNT_CREDENTIALS_PATH=... # Path to gcloud service account creedentials with `JSON` key type\n    export TEST_GCLOUD_SERVICE_ACCOUNT_CREDENTIALS_CONTENT=... # Content of gcloud service account creedentials with `JSON` key type\n    ```\n\n### Pre-commit hooks\n\nOptionally, the [pre-commit](https://pre-commit.com/) framework can be used to ensure that\nthe source code updates are compliant with all the rules mentioned above.\n\nInstallation instructions are available in their [docs](https://pre-commit.com/#installation).\n\nThe repository already contains pre-configured `.pre-commit-config.yaml`, so to enable\nthe hooks, just run\n\n```shell\npre-commit install\n```\n',
    'author': 'Priit Lätt',
    'author_email': 'priit@nevercode.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codemagic-ci-cd/cli-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
