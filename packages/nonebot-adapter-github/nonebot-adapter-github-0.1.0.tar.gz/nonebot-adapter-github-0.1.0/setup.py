# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.github']

package_data = \
{'': ['*']}

install_requires = \
['githubkit[auth-app]>=0.6.1,<0.7.0', 'nonebot2>=2.0.0-beta.5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-adapter-github',
    'version': '0.1.0',
    'description': 'GitHub adapter for nonebot2',
    'long_description': '<!-- markdownlint-disable-next-line MD041 -->\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot-Adapter-GitHub\n\n<!-- markdownlint-capture -->\n<!-- markdownlint-disable MD036 -->\n\n_✨ GitHub 协议适配 ✨_\n\n<!-- markdownlint-restore -->\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/adapter-github/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/adapter-github" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-adapter-github">\n    <img src="https://img.shields.io/pypi/v/nonebot-adapter-github" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">\n  <a href="https://results.pre-commit.ci/latest/github/nonebot/adapter-github/master">\n    <img src="https://results.pre-commit.ci/badge/github/nonebot/adapter-github/master.svg" />\n  </a>\n  <br />\n  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">\n    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat Group">\n  </a>\n  <a href="https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=7b4a3&appChannel=share&businessType=9&from=246610&biz=ka">\n    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-NoneBot-5492ff?style=flat-square" alt="QQ Channel">\n  </a>\n  <a href="https://t.me/botuniverse">\n    <img src="https://img.shields.io/badge/telegram-botuniverse-blue?style=flat-square" alt="Telegram Channel">\n  </a>\n  <a href="https://discord.gg/VKtE6Gdc4h">\n    <img src="https://discordapp.com/api/guilds/847819937858584596/widget.png?style=shield" alt="Discord Server">\n  </a>\n</p>\n',
    'author': 'yanyongyu',
    'author_email': 'yyy@nonebot.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nonebot/adapter-github',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
