import setuptools

setuptools.setup(
    name='nonebot_plugin_offline_mahjong_helper',
    version='0.0.7',
    keywords=["nonebot","mahjong"],
    author='Nranphy',
    author_email='3102002900@qq.com',
    url='https://github.com/Nranphy/nonebot_plugin_offline_mahjong_helper',
    description="基于nonebot2可约桌、算点、查询的面麻助手。",
    long_description=u'基于nonebot2可约桌、算点、查询的面麻助手。',
    packages=setuptools.find_packages(),
    install_requires=[
        "nonebot2",
        "nonebot-adapter-onebot",
        "nonebot_plugin_htmlrender",
        "nonebot_plugin_apscheduler"
        ],
)