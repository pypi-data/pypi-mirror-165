from setuptools import setup,find_namespace_packages

setup(
name='nonebot_plugin_flash_silentsave',
version='1.0.3',
description='静默保存群聊中的闪照',
#long_description=open('README.md','r').read(),
author='karisaya',
author_email='1048827424@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_flash_silentsave"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot",],
url='https://github.com/KarisAya/nonebot_plugin_flash_silentsave',
)