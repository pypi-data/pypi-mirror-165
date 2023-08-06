# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['atomic_operator_runner', 'atomic_operator_runner.utils']

package_data = \
{'': ['*'], 'atomic_operator_runner': ['data/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.1',
 'paramiko>=2.11.0,<3.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'pypsrp>=0.8.1,<0.9.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['atomic-operator-runner = '
                     'atomic_operator_runner.__main__:main']}

setup_kwargs = {
    'name': 'atomic-operator-runner',
    'version': '0.1.3',
    'description': 'atomic-operator-runner',
    'long_description': '# atomic-operator-runner\n\n[![PyPI](https://img.shields.io/pypi/v/atomic-operator-runner.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/atomic-operator-runner.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/atomic-operator-runner)][pypi status]\n[![License](https://img.shields.io/pypi/l/atomic-operator-runner)][license]\n\n[![Tests](https://github.com/swimlane/atomic-operator-runner/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/swimlane/atomic-operator-runner/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/atomic-operator-runner/\n[tests]: https://github.com/swimlane/atomic-operator-runner/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/swimlane/atomic-operator-runner\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Execute a command string on a local, remote Windows, remote macOS and remote Linux systems\n- Execute a command for PowerShell, command-line (cmd) and bash/sh on any of the above systems\n- Can execute commands elevated on the supported systems\n- Returns a standard response object, as well as displays a formatter version to the console via logging\n\n### Response Object\n\nEvery execution of a command will return a standard object that includes details about the command execution. The full structure of this response is outlined below:\n\n```json\n{\n    "environment": {\n        "platform": "windows",\n        "hostname": "10.x.x.x",\n        "user": "user"\n    },\n    "command": "Get-Service\\\'",\n    "executor": "powershell",\n    "elevation_required": false,\n    "start_timestamp": "2022-08-25T14:15:10.370468",\n    "end_timestamp": "2022-08-25T14:15:12.165563",\n    "return_code": 1,\n    "output": "",\n    "records": [\n        {\n            "type": null,\n            "message_data": null,\n            "source": null,\n            "time_generated": null,\n            "pid": null,\n            "native_thread_id": null,\n            "managed_thread_id": null,\n            "extra": {\n                "MESSAGE_TYPE": "266245",\n                "action": "None",\n                "activity": "Invoke-Expression",\n                "category": "17",\n                "command_definition": "None",\n                "command_name": "None",\n                "command_type": "None",\n                "command_visibility": "None",\n                "details_message": "None",\n                "exception": "System.Management.Automation.ParseException: At line:1 char:12\\\\r\\\\n+ Get-Service\\\'\\\\r\\\\n+            ~\\\\nThe string is missing the terminator: \\\'.\\\\r\\\\n   at System.Management.Automation.ScriptBlock.Create(Parser parser, String fileName, String fileContents)\\\\r\\\\n   at System.Management.Automation.ScriptBlock.Create(ExecutionContext context, String script)\\\\r\\\\n   at Microsoft.PowerShell.Commands.InvokeExpressionCommand.ProcessRecord()\\\\r\\\\n   at System.Management.Automation.CommandProcessor.ProcessRecord()",\n                "extended_info_present": "False",\n                "fq_error": "TerminatorExpectedAtEndOfString,Microsoft.PowerShell.Commands.InvokeExpressionCommand",\n                "invocation": "False",\n                "invocation_bound_parameters": "None",\n                "invocation_command_origin": "None",\n                "invocation_expecting_input": "None",\n                "invocation_history_id": "None",\n                "invocation_info": "System.Management.Automation.InvocationInfo",\n                "invocation_line": "None",\n                "invocation_name": "None",\n                "invocation_offset_in_line": "None",\n                "invocation_pipeline_iteration_info": "None",\n                "invocation_pipeline_length": "None",\n                "invocation_pipeline_position": "None",\n                "invocation_position_message": "None",\n                "invocation_script_line_number": "None",\n                "invocation_script_name": "None",\n                "invocation_unbound_arguments": "None",\n                "message": "ParserError: (:) [Invoke-Expression], ParseException",\n                "pipeline_iteration_info": "None",\n                "reason": "ParseException",\n                "script_stacktrace": "None",\n                "target_info": "None",\n                "target_name": "",\n                "target_object": "None",\n                "target_type": ""\n            }\n        }\n    ]\n}\n```\n\n## Installation\n\nYou can install _atomic-operator-runner_ via [pip] from [PyPI]:\n\n```console\n$ pip install atomic-operator-runner\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n```bash\nUsage: atomic-operator-runner [OPTIONS] COMMAND EXECUTOR\n\n  atomic-operator-runner executes powershell, cmd or bash/sh commands both\n  locally or remotely using SSH or WinRM.\n\nOptions:\n  --version                       Show the version and exit.\n  --platform [windows|macos|linux]\n                                  Platform to run commands on.  [required]\n  --hostname TEXT                 Remote hostname to run commands on.\n  --username TEXT                 Username to authenticate to remote host.\n  --password TEXT                 Password to authenticate to remote host.\n  --ssh_key_path PATH             Path to an SSH Key to authenticate to remote\n                                  host.\n  --private_key_string TEXT       Private SSH Key string used to authenticate\n                                  to remote host.\n  --verify_ssl BOOLEAN            Whether or not to verify SSL when\n                                  authenticating.\n  --ssh_port INTEGER              Port used for SSH connections.\n  --ssh_timeout INTEGER           Timeout used for SSH connections.\n  --elevated BOOLEAN              Whether or not to run the command elevated.\n  --help                          Show this message and exit.\n```\n\n## Contributing\n\nContributions are very welcome.\n\nTo learn more, see the [Contributor Guide](CONTRIBUTING.md).\n\n## License\n\nDistributed under the terms of the [MIT license](LICENSE).\n\n_atomic-operator-runner_ is free and open source software.\n\n## Security\n\nSecurity concerns are a top priority for us, please review our [Security Policy](SECURITY.md).\n\n<!-- github-only -->\n\n[license]: https://github.com/swimlane/atomic-operator-runner/blob/main/LICENSE\n[contributor guide]: https://github.com/swimlane/atomic-operator-runner/blob/main/CONTRIBUTING.md\n\nTEST\nTEST2\n',
    'author': 'Josh Rickard',
    'author_email': 'rickardja@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/swimlane/atomic-operator-runner',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
