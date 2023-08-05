# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_drawer']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0',
 'nonebot-adapter-onebot>=2.1.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-drawer',
    'version': '0.3.7',
    'description': '适用于 Nonebot2 的AI画画插件(对接文心大模型API)',
    'long_description': '# nonebot-plugin-drawer\n基于文心大模型的AI机器人画画插件。\n\n\n### 前提: nonebot2的部署\n这里推荐两篇机器人部署教程  \n1.https://blog.csdn.net/weixin_47113651/article/details/121353191  \n2.https://zhuanlan.zhihu.com/p/371264976\n### 通过nb-cli安装（推荐）\n```\nnb plugin install nonebot-plugin-drawer\n```\n### 通过pip安装\n```\n1.pip install nonebot-plugin-drawer 进行安装  \n2.在bot.py添加nonebot.load_plugin(\'nonebot_plugin_drawer\')\n```\n### 配置env.*\n请在env.*配置文件中加入如下两行\n```\nwenxin_ak = "xxxxxxxxxxxxxxxx"\nwenxin_sk = "xxxxxxxxxxxxxxxx"\nwenxin_cd_time = 300 # 技能冷却时间，以秒为单位\nwenxin_image_count = 3 # 画画的图片数量\nwenxin_manager_list = ["123456789", "98765432"] # 管理员列表(不触发冷却时间限制)\n```\n文心的ak和sk申请链接：https://wenxin.baidu.com/younger/apiDetail?id=20008\n### 使用方法\n触发菜单命令：画画帮助\n当前支持油画、水彩画、卡通画、粉笔画、儿童画、蜡笔画, 主要擅长风景写意画，请尽量给定比较明确的意象  \n如：油画 江上落日与晚霞\n\n![3a83453d5d28d1eedf0a0ddb5c90d29](https://user-images.githubusercontent.com/35400185/185073989-d4cd1118-cddb-4588-a210-b6d001a049f1.jpg)  \n油画 江上落日与晚霞  \n\n![8887badee1c74c8488b613e4ceb83c2](https://user-images.githubusercontent.com/35400185/185074011-49b7bad1-e7d3-4385-afd5-a82163b0eebc.jpg)  \n油画 思乡\n',
    'author': 'CrazyBoyM',
    'author_email': 'ai-lab@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CrazyBoyM/nonebot-plugin-drawer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
