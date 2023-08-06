# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_ssh_config',
 'local_ssh_config.hosts',
 'local_ssh_config.ssh',
 'local_ssh_config.utils',
 'local_ssh_config.utils.ip_addresses',
 'local_ssh_config.utils.jinja']

package_data = \
{'': ['*'], 'local_ssh_config': ['templates/*', 'templates/config.d/*']}

install_requires = \
['Jinja2==3.1.2',
 'colorama>=0.4.3,<0.5.0',
 'rich>=10.11.0,<13.0.0',
 'shellingham>=1.3.0,<2.0.0',
 'typer==0.6.1']

entry_points = \
{'console_scripts': ['local-ssh-config = local_ssh_config.__main__:main',
                     'local_ssh_config = local_ssh_config.__main__:main',
                     'lsc = local_ssh_config.__main__:main']}

setup_kwargs = {
    'name': 'local-ssh-config',
    'version': '0.4.5',
    'description': 'Quickly update config (ssh files and host file) for your local virtual machines',
    'long_description': '# local-ssh-config\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![ci](https://github.com/iancleary/local-ssh-config/workflows/ci/badge.svg)](https://github.com/iancleary/local-ssh-config/actions/workflows/ci.yml)\n\nIan Cleary ([iancleary](https://github.com/iancleary))\n\n## Description\n\n**Welcome!** This is a CLI to generate/update SSH config files for your local virtual machines quickly.\n\n## Problem\n\nWindows doesn\'t maintain a static IP Address of Hyper-V Virtual Machines across reboots.  When using [multipass](https://multipass.run) with a Hyper-V backend, this applies as well for multipass.\n\nThis leads to ssh configuration, which is by ip address, to be stale every reboot.\n\n## Solution\n\nThis script updates my ssh config file for me\n\n- get IP address from PowerShell for hyper-v by name according to source (\'hyper-v\' directly, or \'multipass list\')\n- write template config files to the `~/.ssh/config.d/` directory according to your `~/.config/local-ssh-config/settings.json` file.\n\nThis assumes you have:\n\n- a `~/.ssh/config.d/` folder\n- [`Include config.d/*` in your `~/.ssh/config`](https://superuser.com/questions/247564/is-there-a-way-for-one-ssh-config-file-to-include-another-one)\n- For Hyper-V Virtual Machines\n  - PowerShell installed\n  - Hyper-V enabled and The Hyper-V Manager Installed\n\n### Hyper-V Manager IP Address\n\n![Hyper-V Manager Networking Tab](docs/assets/hyper-v-manager-networking-tab.png)\n\n> I currently use Ubuntu Servers, if you do too, [please install several `apt` packages in the Virtual Machine (so that Hyper-V can report the IP Address)](https://stackoverflow.com/a/72534742/13577666)\n\n🚨🚨 Hyper-V will not report the ip address until you do the above 🚨🚨\n\n> Multipass or Virtual Box may report the IP address of an Ubuntu Guest. I\'m not currently sure if it\'s a Hyper-V limitation or a Windows limitation.  \n\nAs this tool only currently supports Hyper-V, please consider this a warning of the required step.\n\n## Quickstart\n\n```sh\n❯ pipx install local-ssh-config --user\n❯ local-ssh-config --help\n```\n\nThat will output the following:\n\n```bash\nUsage: local_ssh_config [OPTIONS]\n\n  Creates an `~/.ssh/config.d/` directory, \n  checks to see if you include all files in that directory,\n  and then creates config files for each virtual machine specified\n  in your `~/.config/vm-ip-ssh-config/settings.json` file.\n\n  See https://github.com/iancleary/local-ssh-config/ for more information.\n\nArguments:\n  None\n\nOptions:\n  -f, --file TEXT       The JSON file containing the virtual machine\n                        configuration  [default: C:\\Users\\username\\.config\\vm-\n                        ip-ssh-config\\settings.json]\n  -v, --version         Show the application\'s version and exit.\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n  --help                Show this message and exit.\n```\n\n## Example Usage\n\nThe first and only argument is the name of the component to create.\n\n```bash\n$ local-ssh-config\n{\'host\': \'test.local\', \'hostname\': \'0.0.0.0\', \'user\': \'test\', \'identity_file\': \'~/.ssh/example_id_ed25519\'}\n{\'host\': \'ubuntu.local\', \'hostname\': {\'source\': \'hyper-v\', \'physical_address\': \'00-15-5d-95-fb-09\'}, \'user\': \'icleary\', \'identity_file\': \'~/.ssh/github_id_rsa_ed25519\'}\nHyper-V: Powershell (arp -a): Interface command executed successfully!\n-------------------------\n{\'host\': \'dev1.multipass.local\', \'hostname\': {\'source\': \'multipass\', \'name\': \'dev1\'}, \'user\': \'ubuntu\'}\nMultipass-V: Powershell (multipass list): Interface command executed successfully!\n-------------------------\n\n✨ Creating ~/.ssh/config.d/ files\n✅ C:\\Users\\icleary\\.ssh\\config.d\\test.local\n✅ C:\\Users\\icleary\\.ssh\\config.d\\ubuntu.local\n✅ C:\\Users\\icleary\\.ssh\\config.d\\dev1.multipass.local\nSSH config updated! 🚀 ✨!\n\nThank you for using local-ssh-config.\n```\n\nThe path printed is the absolute path to the updated config files.\n\n> This uses a directory `~/.ssh/config.d/` to allow for a single file per Host, to allow cleaner version tracking within a dotfile manager.\n> See [`Include config.d/*` in your `~/.ssh/config`](https://superuser.com/questions/247564/is-there-a-way-for-one-ssh-config-file-to-include-another-one) for the include syntax\n> [WINDOWS_MULTIPASS_DEFAULT_ID_RSA](https://github.com/canonical/multipass/issues/913#issuecomment-697235248) = "C:/Windows/System32/config/systemprofile/AppData/Roaming/multipassd/ssh-keys/id_rsa"\n\n## Configuration\n\nConfiguration can be done through 2 different ways:\n\n- Creating a global `settings.json` in your home directory (`~/.config/local-ssh-config/settings.json`).\n- Creating a local `.local-ssh-config-config.json` in your project\'s root directory and including the path to that file with the `--f` or `-f` optionanl command-line argument.\n\nThe optional command line value takes precendence global settings file being the default.\n\n## API Reference\n\n### File\n\nControls the settings.json to load.\nDefaults to `~/.config/local-ssh-config/settings.json`\n\nUsage:\n\nCommand line: `--file <value>` or `-f <value>`\n\nJSON config:\n\nExample with single host, as dictionary\n\n```json\n{\n    "host": "ubuntu.local",\n    "hostname": {\n        "source": "hyper-v",\n        "physical_address": "00-15-5d-95-fb-09"\n    },\n    "user": "icleary",\n    "identity_file": "~/.ssh/github_id_rsa_ed25519"\n}\n```\n\nExample with single host, as list:\n\n```json\n[\n  {\n      "host": "ubuntu.local",\n      "hostname": {\n          "source": "hyper-v",\n          "physical_address": "00-15-5d-95-fb-09"\n      },\n      "user": "icleary",\n      "identity_file": "~/.ssh/github_id_rsa_ed25519"\n  }\n]\n```\n\n> A single dictionary is converted to a list of hosts before looping through the files, so either structure is valid (your preference).\n\nExample with multiple hosts:\n\n```json\n[\n    {\n        "host": "test.local",\n        "hostname": "0.0.0.0",\n        "user": "test",\n        "identity_file": "~/.ssh/example_id_ed25519"\n    },\n    {\n        "host": "ubuntu.local",\n        "hostname": {\n            "source": "hyper-v",\n            "physical_address": "00-15-5d-95-fb-09"\n        },\n        "user": "icleary",\n        "identity_file": "~/.ssh/github_id_rsa_ed25519"\n    },\n    {\n        "host": "dev1.multipass.local",\n        "hostname": {\n            "source": "multipass",\n            "name": "dev1"\n        },\n        "user": "ubuntu"\n    }\n]\n```\n\n## Further information\n\n> I will likely evolve this CLI as I learn more; I\'m on my way 😊\n\n**Enjoy quickly updating your ssh configurations 🚀!**\n\n## Contributing\n\nI created this CLI for my opinionated uses and may not accept changes.  That said, I made this to solve a problem, and if you have the same problem, I hope it helps you! 😊\n\nSee [CONTRIBUTING.md](.github/CONTRIBUTING.md).\n',
    'author': 'Ian Cleary',
    'author_email': 'contact@iancleary.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iancleary/local-ssh-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
