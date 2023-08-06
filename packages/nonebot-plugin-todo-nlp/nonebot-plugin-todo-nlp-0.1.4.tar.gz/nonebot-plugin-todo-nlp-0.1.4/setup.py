# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_todo_nlp']

package_data = \
{'': ['*'], 'nonebot_plugin_todo_nlp': ['templates/*', 'templates/css/*']}

install_requires = \
['jionlp>=1.4.17,<2.0.0',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.4,<0.2.0',
 'nonebot-plugin-htmlrender>=0.1.1,<0.2.0',
 'nonebot2>=2.0.0-beta.5,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pathlib>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-todo-nlp',
    'version': '0.1.4',
    'description': '一款自动识别提醒内容，可生成todo图片并定时推送的nonebot插件',
    'long_description': '# nonebot-plugin-todo-nlp\n\n一款自动识别提醒内容，可生成todo图片并定时推送的nonebot2插件，v11适配器可用\n\nnlp支持来源于[jionlp](https://github.com/dongrixinyu/JioNLP) （十分便利的nlp库）\n\n图片生成功能来源于nonebot插件[htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender) \n（我们先进的的浏览器制图已经完全超越了老式的PIL制图了（不是））\n\n### 插件特点：\n\n* 允许多样化的日期描述方法，可以在语句中包含“明天”、“9月1日”等日期提示\n* 自动识别语句中的事项\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```\nnb plugin install nonebot_plugin_todo_nlp\n2022-08-29:等一个pull request merged，暂时用不了\n```\n\n- 使用 poetry\n\n```\npoetry add nonebot_plugin_todo_nlp\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_todo_nlp\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```\ngit clone https://github.com/Jigsaw111/nonebot_plugin_todo.git\n```\n\n\n### 食用方法：\n触发关键词：\n* 增加事项: \'提醒\', \'nonebot_todo\'\n* 完成事项: \'完成\'\n* 删除事项（支持正则表达式）: \'删除\', \'去掉\'\n* 修改事项时间: \'更正\', \'改\'\n* 获取图片: \'获取todo\'\n\n> 若要强调事件名称（nlp有的时候会犯蠢，比如在示例中机器人没能识别出“中秋假期”这一关键词）：使用英文双引号括上事项名称\n\n> **由于nonebot使用uvicorn框架，在windows平台使用时图片的导出可能会出现not implemented error。**\\\n> 解决方法：将env中的FASTAPI_RELOAD改为false。\\\n> 见nonebot-plugin-htmlrender [issue#25](https://github.com/kexue-z/nonebot-plugin-htmlrender/issues/25) ;\\\n> nonebot2文档中对此亦有提及，见[fastapi_reload](https://nb2.baka.icu/docs/tutorial/choose-driver#fastapi_reload) 。\n\n### 配置方法：\n在env中添加如同以下格式的配置（多个send time则多次推送，注意时间首位去0）：\\\n在群聊中使用时，只有管理员和群主可以增删todo项目。\n私聊情况下，好友均可使用todo增删功能，此处配置是推送名单。\n```\nTODO_USERS=["1234567890"]\nTODO_GROUPS=["1234567890"]\nTODO_SEND_TIME=[{"HOUR":8,"MINUTE":0},{"HOUR":19,"MINUTE":34}]\n```\n\n### TODO：\n- [ ] 迁移到postgre数据库\n- [ ] 增加优先级相关功能支持\n- [ ] 增加完成todo统计，对完成状况进行跟踪\n- [ ] 增加todo项目复用功能（比如每日/每周某天的提醒可以复用而不用手动再次添加）\n- [ ] 完善相关console log\n- [ ] 更加优雅的todo使用订阅与推送时间配置\n- [ ] （可能后期会加上其他的todo主题？）\n\n### 示例：\n\n![1.png](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/1.png)\n\n![2.jpg](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/2.jpg)\n',
    'author': 'CofinCup',
    'author_email': '864341840@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
