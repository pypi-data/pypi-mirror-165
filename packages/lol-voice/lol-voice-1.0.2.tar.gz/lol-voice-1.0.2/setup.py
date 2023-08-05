# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lol_voice',
 'lol_voice.formats',
 'lol_voice.formats.section',
 'lol_voice.tools',
 'lol_voice.tools.Binary']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'xxhash>=3.0.0,<4.0.0', 'zstd>=1.5.2.5,<2.0.0.0']

setup_kwargs = {
    'name': 'lol-voice',
    'version': '1.0.2',
    'description': '通过解析英雄联盟游戏内WAD、BNK、WPK、BIN等文件来提取音频文件，并可以按照触发事件分类',
    'long_description': '# py-bnk-extract\n\n英雄联盟语音解包工具, 由Python语言编写.\n\n\n- [介绍](#介绍)\n- [安装](#安装)\n- [使用](#使用)\n- [问题](#问题)\n- [维护者](#维护者)\n- [感谢](#感谢)\n- [许可证](#许可证)\n\n\n### 介绍\n可以将英雄联盟中wpk或bnk中音频文件按照皮肤的触发条件分类解包, 默认为wem音频格式, 使用 [vgmstream](https://vgmstream.org/downloads) 可转码.\n\n- [index.py](lol_voice/index.py#L250)中 _extract_audio_ 函数逻辑以及HIRC部分块结构和WPK文件结构参考[Morilli](https://github.com/Morilli)编写的解包工具[https://github.com/Morilli/bnk-extract](https://github.com/Morilli/bnk-extract)\n- [WAD.py](lol_voice/formats/WAD.py)中 文件结构以及部分逻辑来源于[https://github.com/CommunityDragon/CDTB](https://github.com/CommunityDragon/CDTB) 和 [https://github.com/Pupix/lol-file-parser](https://github.com/Pupix/lol-file-parser)\n\n其余bnk文件结构来参考:[http://wiki.xentax.com/index.php/Wwise_SoundBank_(*.bnk)](http://wiki.xentax.com/index.php/Wwise_SoundBank_(*.bnk))\n\n\n### 安装\n\n\n`pip install lol-voice`\n\n`pip install -e git+https://github.com/Virace/py-bnk-extract@package#egg=lol_voice`\n\n### 使用\n此包适合提取已知皮肤语音, 如需全部提取请关注 [lol_extract_voice](https://github.com/Virace/lol_extract_voice)\n```\nfrom lol_voice import extract_audio\nfrom lol_voice.formats import WAD\n\n\ndef example():\n    """\n    按触发事件文件夹分类提取 剑魔 语音文件\n    :return:\n    """\n\n    # 临时目录和最终输出目录\n    temp_path = r\'D:\\Temp\'\n    out_path = r\'D:\\Out\'\n\n    # 英雄名字, 以及对于默认皮肤的三个文件路径\n    champion = \'aatrox\'\n    bin_tpl = f\'data/characters/{champion}/skins/skin0.bin\'\n    audio_tpl = f\'assets/sounds/wwise2016/vo/zh_cn/characters/aatrox/skins/base/{champion}_base_vo_audio.wpk\'\n    event_tpl = f\'assets/sounds/wwise2016/vo/zh_cn/characters/aatrox/skins/base/{champion}_base_vo_events.bnk\'\n\n    # 需要解析两个WAD文件, 这个路径修改为自己的游戏目录\n    wad_file1 = r"D:\\League of Legends\\Game\\DATA\\FINAL\\Champions\\Aatrox.wad.client"\n    wad_file2 = r"D:\\League of Legends\\Game\\DATA\\FINAL\\Champions\\Aatrox.zh_CN.wad.client"\n\n    # 将上面三个文件提取到临时目录\n    WAD(wad_file1).extract([bin_tpl], temp_path)\n    WAD(wad_file2).extract([audio_tpl, event_tpl], temp_path)\n\n    # 根据三个文件对应提取语音并整理\n    extract_audio(\n        bin_file=os.path.join(temp_path, os.path.normpath(bin_tpl)),\n        event_file=os.path.join(temp_path, os.path.normpath(event_tpl)),\n        audio_file=os.path.join(temp_path, os.path.normpath(audio_tpl)),\n        out_dir=out_path\n    )\n\nif __name__ == \'__main__\':\n    example()\n```\n### 问题\n待解决：\n - ~~不同事件调用相同语音, 导致文件重复~~\n - 不排除文件有缺失问题, event文件解析不完整\n\n\n\n### 维护者\n**Virace**\n- blog: [孤独的未知数](https://x-item.com)\n\n### 感谢\n- [@Morilli](https://github.com/Morilli/bnk-extract), **bnk-extract**\n- [@Pupix](https://github.com/Pupix/lol-file-parser), **lol-file-parser**\n- [@CommunityDragon](https://github.com/CommunityDragon/CDTB), **CDTB** \n- [@vgmstream](https://github.com/vgmstream/vgmstream), **vgmstream**\n\n- 以及**JetBrains**提供开发环境支持\n  \n  <a href="https://www.jetbrains.com/?from=kratos-pe" target="_blank"><img src="https://cdn.jsdelivr.net/gh/virace/kratos-pe@main/jetbrains.svg"></a>\n\n### 许可证\n\n[GPLv3](LICENSE)',
    'author': 'Virace',
    'author_email': 'Virace@aliyun.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Virace/py-bnk-extract',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
