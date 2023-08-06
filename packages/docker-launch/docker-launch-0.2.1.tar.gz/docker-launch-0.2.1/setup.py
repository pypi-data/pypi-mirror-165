# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_launch', 'docker_launch.console']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'docker>=5.0.3,<6.0.0',
 'paramiko>=2.11.0,<3.0.0',
 'tomlkit>=0.11.1,<0.12.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.4,<5.0',
                             'typing-extensions>=4.1,<5.0']}

entry_points = \
{'console_scripts': ['docker-launch = docker_launch.console:main']}

setup_kwargs = {
    'name': 'docker-launch',
    'version': '0.2.1',
    'description': 'Create and launch docker containers on multiple hosts.',
    'long_description': '# docker-launch\n\n[![PyPI](https://img.shields.io/pypi/v/docker-launch.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/docker-launch/)\n[![Python](https://img.shields.io/pypi/pyversions/docker-launch.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/docker-launch/)\n[![Test](https://img.shields.io/github/workflow/status/necst-telescope/docker-launch/Test?logo=github&label=Test&style=flat-square)](https://github.com/necst-telescope/docker-launch/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](https://github.com/necst-telescope/docker-launch/blob/main/LICENSE)\n\nCreate and launch docker containers on multiple hosts.\n\n## Features\n\nThis library provides:\n\n- SSH public key authentication checker and its set-up command\n- Launch multiple Docker containers on arbitrary host(s), via command line or Python script\n\n## Installation\n\n```shell\npip install docker-launch\n```\n\n## Usage\n\nTo check if SSH public key authentication to `user@192.168.1.1` is enabled or not, run\n\n```python\n>>> from docker_launch import check_connection\n>>> check_connection("user@192.168.1.1")\nTrue\n```\n\nor from command line,\n\n```shell\n$ docker-launch check user@192.168.1.1\nOK\n```\n\nIf the authentication hasn\'t been set-up, you can configure it via\n\n```shell\ndocker-launch check user@192.168.1.1 --setup\n```\n\nOnce the authentication is set-up, let\'s prepare configuration file `path/to/config.toml`\n\n```toml\n[ros_topics]\nbaseimg = "ros:humble-ros-core"\ncommand = "env ROS_DOMAIN_ID=1 ros2 topic pub {a} std_msgs/msg/Float64 \'{{data: 123.45}}\'"\ntargets = [\n    { a = "first", __machine__ = "localhost" },\n    { a = "/second", __machine__ = "user@172.29.1.2" },\n]\n```\n\nThis will spawn\n\n- [`ros:humble-ros-core`](https://hub.docker.com/_/ros) container on the host machine, executing command `env ROS_DOMAIN_ID=1 ros2 topic pub first std_msgs/msg/Float64 \'{data: 123.45}\'`\n- [`ros:humble-ros-core`](https://hub.docker.com/_/ros) container on `user@172.29.1.2`, executing command `env ROS_DOMAIN_ID=1 ros2 topic pub /second std_msgs/msg/Float64 \'{data: 123.45}\'`\n\nby running\n\n```python\n>>> from docker_launch import launch_containers\n>>> launch_containers("path/to/config.toml", remove=True)\n```\n\nor\n\n```shell\ndocker-launch up path/to/config.toml --rm\n```\n\nFor the details of the options, see [docker run documentation](https://docs.docker.com/engine/reference/commandline/run/) and [Docker SDK\'s documentation](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run).\n\n<details><summary>Options of <code>docker run</code> command which <code>docker-launch</code> command and <code>docker_launch.launch_containers()</code> function doesn\'t support</summary>\n\n- `--attach`, `-a`\n- `--cgroupns`\n- `--cidfile`\n- `--detach`, `-d` (always `True`)\n- `--detach-keys`\n- `--disable-content-trust`\n- `--env-file`\n- `--expose`\n- `--gpus`\n- `-h` (use `--hostname` instead)\n- `--interactive`, `-i`\n- `--ip`\n- `--ip6`\n- `--label-file`\n- `--link-local-ip`\n- `--log-driver`\n- `--log-opt`\n- `--mount`\n- `--net` (only `bridge`, `none`, `host`, and `container:<name|id>` are supported)\n- `--net-alias`\n- `--network` (only `bridge`, `none`, `host`, and `container:<name|id>` are supported)\n- `--network-alias`\n- `--no-healthcheck`\n- `--pull`\n- `--sig-proxy`\n- `--stop-timeout`\n- `--ulimit`\n- `-v` (use `--volume` instead)\n\n</details>\n<details><summary>Options of Docker SDK\'s <code>docker.containers.run</code> function which <code>docker-launch</code> command doesn\'t support (<code>docker_launch.launch_containers()</code> function supports them)</summary>\n\n- `auto_remove`\n- `device_requests`\n- `init_path`\n- `log_config`\n- `lxc_conf`\n- `mounts`\n- `nano_cpus`\n- `network`\n- `network_disabled`\n- `stdin_open`\n- `stdout`\n- `stderr`\n- `stream`\n- `ulimits`\n- `use_config_proxy`\n- `version`\n\n</details>\n\n## Configuration File Spec\n\nThe configuration is described in [TOML](https://toml.io/en/) format.\nRequired fields are:\n\n- `baseimg` (string) - Name of the image from which the containers are created\n- `command` (string) - Command template to execute in each containers, with [Python style placeholder](https://docs.python.org/3/library/string.html#format-string-syntax) (positional placeholder e.g. `{0}` isn\'t supported)\n- `targets` (array of table) - List of parameter tables for each containers, and special parameter `__machine__`\n\nThe fields above must be grouped in a table.\n\n```toml\n[table-name]\nbaseimg = "docker:image-name"\ncommand = "command template with {placeholder}"\ntargets = [\n    { placeholder = "this", __machine__ = "user@172.29.1.2" },\n    { placeholder = "that" },\n]\n```\n\nA configuration file can have multiple tables\n\n```toml\n[table-1]\nbaseimg = "docker:image-name"\ncommand = "command template with {placeholder}"\ntargets = [\n    { placeholder = "this", __machine__ = "user@172.29.1.2" },\n    { placeholder = "that" },\n]\n\n[table-2]\nbaseimg = "docker:other-image"\ncommand = "other command {parameter} with curly braces {{escaped}}"\ntargets = [\n    { parameter = 100, __machine__ = "user@172.29.1.2" },\n    { parameter = 200 },\n]\n```\n\nOptional field:\n\n- `include` (array of string) - Paths to additional configuration files\n\nThe instruction must be declared at top level (not inside tables).\n\n```toml\ninclude = ["path/to/other/config.toml", "/path/to/another/config.toml"]\n\n[table-name]\nbaseimg = "docker:image-name"\ncommand = "command template with {placeholder}"\ntargets = [\n    { placeholder = "this", __machine__ = "user@172.29.1.2" },\n    { placeholder = "that" },\n]\n```\n\n---\n\nThis library is using [Semantic Versioning](https://semver.org).\n',
    'author': 'KaoruNishikawa',
    'author_email': 'k.nishikawa@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/necst-telescope/docker-launch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
