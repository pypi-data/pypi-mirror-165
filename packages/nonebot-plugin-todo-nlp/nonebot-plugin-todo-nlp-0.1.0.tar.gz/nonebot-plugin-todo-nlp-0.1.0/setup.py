# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_todo_nlp']

package_data = \
{'': ['*'], 'nonebot_plugin_todo_nlp': ['templates/*', 'templates/css/*']}

install_requires = \
['jionlp>=1.4.17,<2.0.0',
 'nonebot-plugin-apscheduler>=0.1.4,<0.2.0',
 'nonebot-plugin-htmlrender>=0.1.1,<0.2.0',
 'nonebot2>=2.0.0-beta.5,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pathlib>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-todo-nlp',
    'version': '0.1.0',
    'description': '一款自动识别提醒内容，可生成todo图片并定时推送的nonebot插件',
    'long_description': '# nonebot_plugin_todo_nlp\n\n一款自动识别提醒内容，可生成todo图片并定时推送的nonebot插件\n\n消息响应器集合：add_todo, finish_todo,remove_todo,change_todo, get_todo_pic\n\n### 插件特点：\n\n* 允许多样化的日期描述方法，可以在语句中包含“明天”、“9月1日”等日期提示\n* 自动识别语句中的事项\n\n### 触发关键词：\n\n* 增加事项: \'提醒\', \'nonebot_todo\'\n* 完成事项: \'完成\'\n* 删除事项（支持正则）: \'删除\', \'去掉\'\n* 修改事项时间: \'更正\', \'改\'\n* 获取图片: \'获取todo\'\n\n> 若要强调事件名称（nlp有的时候会犯蠢，比如在示例中机器人没能识别出“中秋假期”这一关键词）：使用英文双引号括上事项名称\n\n### 推送配置方法：\n\n```\nTODO_QQ_FRIENDS=[864341840]\nTODO_SEND_TIME=[{"HOUR":08,"MINUTE":00}]\n```\n\n### TODO：\n- [ ] 迁移到postgre数据库\n- [ ] 增加优先级相关功能\n- [ ] 增加完成todo统计，对完成状况进行跟踪\n- [ ] 增加todo项目复用功能（比如每日/每周某天的提醒可以复用）\n\n### 示例：\n\n![1.png](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/1.png)\n\n![2.jpg](https://github.com/CofinCup/nonebot_plugin_todo_nlp/blob/master/readme_resource/2.jpg)\n',
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
