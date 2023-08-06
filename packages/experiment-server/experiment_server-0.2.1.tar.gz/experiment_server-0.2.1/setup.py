# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['experiment_server']

package_data = \
{'': ['*'], 'experiment_server': ['static/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'click>=6.0',
 'easydict>=1,<2',
 'loguru>=0.5,<0.6',
 'pandas>=1,<2',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'tornado>=6.2,<7.0',
 'watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['experiment-server = experiment_server.cli:cli']}

setup_kwargs = {
    'name': 'experiment-server',
    'version': '0.2.1',
    'description': 'Server for experiments to get configuarations from',
    'long_description': '# Overview\n\nServer for experiments to get configurations from\n\n# Setup\n\n## Requirements\n\n* Python 3.8+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install experiment-server\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add experiment-server\n```\n\n# Usage\n## Configuration of an experiment\nThe configuration id defined in a [toml](https://toml.io/en/) file. See example `.toml` below for how the configuration can be defined.\n```toml\n# The `configuration` table contains settings of the study/experiment itself\n[configuration]\n# The `order` is an array of block names or an array of array of block names.\norder = [["conditionA", "conditionB", "conditionA", "conditionB"]]\n# The `groups` and `within_groups` keys allows you to define how the conditions specified\n# in `order` will be managed. `groups` would dictate how the top level array of `order`\n# will be handled. `within_groups` would dictate how the conditions in the nested arrays\n# (if specified) would be managed. These keys can have one of the following values.\n# - "latin_square": Apply latin square to balance the values.\n# - "randomize": For each participant randomize the order of the values in the array.\n# - "as_is": Use the order of the values as specified.\ngroups = "latin_square"\nwithin_groups= "randomize"\n\n# The subtable `variabels` are values that can be used anywhere when defining the blocks.\n# Any variable can be used by appending "$" before the variable name in the blocks. See \n# below for an exmaple of how variables can be used\n[configuration.variables]\nTRIALS_PER_ITEM = 3\n\n# Blocks are defined as an array of tables. Each block must contain `name` and the \n# subtable `config`. Optionally, a block can also specify `extends`, whish is a `name` of\n# another block. See below for more explanation on how `extends` works\n\n# Block: Condition A\n[[blocks]]\nname = "conditionA"\n\n# The `config` subtable can have any key-values. Note that `name` and `participant_index`\n# will be added to the `config` when this file is being processed. Hence, those keys \n# will be overwritten if used in this subtable.\n[blocks.config]\ntrialsPerItem = "$TRIALS_PER_ITEM"\nparam1 = 1\nparam2 = 1\nparam3 = 1\n\n# Block: Condition B\n[[blocks]]\nname = "conditionB"\nextends = "conditionA"\n\n# Since "conditionB" is extending "conditionA", the keys in the `config` subtable of \n# the block "conditionA" not defined in the `config` subtable of "conditionB" will be copied\n# to the `config` subtable of "conditionB". In this example, `param1`, `param2` and \n# `trialsPerItem` will be copied over here.\n[blocks.config]\nparam3 = 2\n```\n\nSee [toml spec](https://toml.io/en/v1.0.0) for more information on the format of a toml file.\n\nThe above config file, after being processed, would result in the following list of blocks for participant number 1:\n```json\n[\n  {\n    "name": "conditionB",\n    "extends": "conditionA",\n    "config": {\n      "param3": 2,\n      "trialsPerItem": 3,\n      "param1": 1,\n      "param2": 1,\n      "participant_index": 1,\n      "name": "conditionB"\n    }\n  },\n  {\n    "name": "conditionB",\n    "extends": "conditionA",\n    "config": {\n      "param3": 2,\n      "trialsPerItem": 3,\n      "param1": 1,\n      "param2": 1,\n      "participant_index": 1,\n      "name": "conditionB"\n    }\n  },\n  {\n    "name": "conditionA",\n    "config": {\n      "trialsPerItem": 3,\n      "param1": 1,\n      "param2": 1,\n      "param3": 1,\n      "participant_index": 1,\n      "name": "conditionA"\n    }\n  },\n  {\n    "name": "conditionA",\n    "config": {\n      "trialsPerItem": 3,\n      "param1": 1,\n      "param2": 1,\n      "param3": 1,\n      "participant_index": 1,\n      "name": "conditionA"\n    }\n  }\n]\n```\n\n## Verify config\nA config file can be validated by running:\n```sh\n$ experiment-server verify-config-file sample_config.toml\n```\nThis will show how the expanded config looks like for the first 5 participant.\n\n## Loading experiment through server\nAfter installation, the server can used as:\n\n```sh\n$ experiment-server run sample_config.toml\n```\n\nSee more options with `--help`\n\nA simple web interface can be accessed at `/` or `/index`\n\nThe server exposes the following REST API:\n- [GET] `/api/items-count`: The total number of blocks. Returns an integer\n- [GET] `/api/active`: Test if the server is working. Returns boolean\n- [GET] `/api/config`: Return the `config` subtable in the configuration file of the current block as a json object. Note that `move-to-next` has to be called atleast once before this can be called.\n- [GET] `/api/global-data`: Returns a json object, with the following keys: \n  - "participant_index": the participant index\n  - "config_length": same value `/items-count`\n- [GET] `/api/all-configs`: Return all `config`s of all the blocks as a list, ordered based on the `order` for the configured participant.\n- [POST] `/api/move-to-next`: Sets the current block to the next block in the list of blocks. Returns a json object, with the key "names", which is the name of the current block after moving. If there are no more blocks, the value of "names" will be "end".\n- [POST] `/api/move-to-block/:block_id`: Set the block at index `block_id` in the list of blocks as the current block.\n- [POST] `/api/shutdown`: Shutdown the server.\n- [POST] `/api/change-participant-index/:participant_index`: Set the participant_index to value `participant_index`. Note that this will set the sate back to the initial state as if the server was freshly stared.\n\nFor a python application, `experiment_server.Client` can be used to access configs from the server. Also, the server can be launched programatically using `experiment_server.server_process` which returns a [`Process`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process) object. Note that the server will reload the config and reset the state to the initial state when the config file loaded is modified.\n\n## Loading experiment through API\nA configuration can be loaded and managed by importing `experiment_server.Experiment`.\n\n## Generate expanded config files\nA config file (i.e. `.toml` file), can be expanded to json files with the following command\n\n```sh\n$ experiment-server generate-config-json sample_config.toml --participant-range 5\n```\n\nThe above will generate the expanded configs for participant indices 1 to 5 as json files. See more options with `--help`\n\n# Wishlist (todo list?)\n- Serve multiple participants at the same time.\n- Improved docs\n  - Add the option of using dict values in order\n  - Improve cli help docs\n',
    'author': 'Ahmed Shariff',
    'author_email': 'shariff.mfa@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
