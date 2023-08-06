# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gsmaterial']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0b1',
 'nonebot-plugin-apscheduler>=0.1.0',
 'nonebot2>=2.0.0a16']

setup_kwargs = {
    'name': 'nonebot-plugin-gsmaterial',
    'version': '0.1.0',
    'description': 'Genshin player cards plugin for NoneBot2',
    'long_description': '<h1 align="center">NoneBot Plugin GsMaterial</h1></br>\n\n\n<p align="center">🤖 用于展示原神游戏每日材料数据的 NoneBot2 插件</p></br>\n\n\n<p align="center">\n  <a href="https://github.com/monsterxcn/nonebot-plugin-gsmaterial/actions">\n    <img src="https://img.shields.io/github/workflow/status/monsterxcn/nonebot-plugin-gsmaterial/Build%20distributions?style=flat-square" alt="actions">\n  </a>\n  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot-plugin-gsmaterial/master/LICENSE">\n    <img src="https://img.shields.io/github/license/monsterxcn/nonebot-plugin-gsmaterial?style=flat-square" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-gsmaterial">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-gsmaterial?style=flat-square" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7.3+-blue?style=flat-square" alt="python"><br />\n</p></br>\n\n\n| ![示例](https://user-images.githubusercontent.com/22407052/188147520-b49eb450-b0e2-4982-b9f5-6f0673da4021.png) |\n|:--:|\n\n\n## 安装方法\n\n\n如果你正在使用 2.0.0.beta1 以上版本 NoneBot，推荐使用以下命令安装：\n\n\n```bash\n# 从 nb_cli 安装\npython3 -m nb plugin install nonebot-plugin-gsmaterial\n\n# 或从 PyPI 安装\npython3 -m pip install nonebot-plugin-gsmaterial\n```\n\n\n<details><summary><i>在 NoneBot 2.0.0.alpha16 上使用此插件</i></summary></br>\n\n\n在过时的 NoneBot 2.0.0.alpha16 上 **可能** 仍有机会体验此插件！不过，千万不要通过 NoneBot 脚手架或 PyPI 安装，仅支持通过 Git 手动安装此插件。\n\n以下命令仅作参考：\n\n\n```bash\n# 进入 Bot 根目录\ncd /path/to/bot\n# 安装依赖\n# source venv/bin/activate\npython3 -m pip install pillow httpx\n# 安装插件\ngit clone https://github.com/monsterxcn/nonebot-plugin-gsmaterial.git\ncd nonebot-plugin-gsmaterial\n# 将文件夹 nonebot_plugin_gsmaterial 复制到 NoneBot2 插件目录下\ncp -r nonebot_plugin_gsmaterial /path/to/bot/plugins/\n# 将文件夹 data 下内容复制到 /path/to/bot/data/ 目录下\nmkdir /path/to/bot/data\ncp -r data/gsmaterial /path/to/bot/data/\n```\n\n\n</details>\n\n\n## 使用须知\n\n\n - 插件的数据来源为 [@Project Amber](https://ambr.top/chs)，请保证 Bot 与此站点的连接质量。\n   \n - 插件首次启用时，会自动从阿里云 OSS 下载绘图模板，并尝试从 [@Project Amber](https://ambr.top/chs) 下载所有角色及武器图片，启动时间由 Bot 与 [@Project Amber](https://ambr.top/chs) 的连接质量决定。图片下载至本地后将不再从远程下载，启动时间将大幅缩短。\n   \n   如果启动插件时下载图片的时间久到离谱，可以考虑自行克隆仓库内文件或从 [此处](https://monsterx.oss-cn-shanghai.aliyuncs.com/bot/gsmaterial/gsmaterial.zip) 下载资源压缩包。\n   \n - 一般来说，插件安装完成后无需设置环境变量，只需重启 Bot 即可开始使用。你也可以在 Nonebot2 当前使用的 `.env` 文件中添加下表给出的环境变量，对插件进行更多配置。环境变量修改后需要重启 Bot 才能生效。\n   \n   | 环境变量 | 必需 | 默认 | 说明 |\n   |:-------|:----:|:-----|:----|\n   | `gsmaterial_skip_three` | 否 | `True` | 是否忽略三星物品 |\n   | `resources_dir` | 否 | `/path/to/bot/data/` | 插件数据缓存目录的父文件夹，包含 `gsmaterial` 文件夹的上级文件夹路径 |\n\n\n## 命令说明\n\n\n插件响应以 `今日` / `今天打什么` 开头的消息。\n\n| 附带参数 | 说明 |\n|:-------|:----|\n| 空 | 返回今日天赋培养与武器突破材料总图 |\n| `天赋` / `角色` | 返回今日天赋培养材料图片 |\n| `武器` | 返回今日武器突破材料图片 |\n\n\n## 特别鸣谢\n\n\n[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [@Project Amber](https://ambr.top/chs)\n',
    'author': 'monsterxcn',
    'author_email': 'monsterxcn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/monsterxcn/nonebot-plugin-gsmaterial',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0',
}


setup(**setup_kwargs)
