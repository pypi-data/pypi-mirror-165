# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lssr']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['lssr = lssr.__main__:main']}

setup_kwargs = {
    'name': 'lssr',
    'version': '1.0.0',
    'description': 'Alternative ls command.',
    'long_description': '# lssr\n\nAlternative ls command.\n\n[![PyPI](https://img.shields.io/pypi/v/lssr)](https://pypi.python.org/pypi/lssr)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lssr)](https://pypi.python.org/pypi/lssr)\n[![Tests](https://github.com/seijinrosen/lssr/actions/workflows/tests.yml/badge.svg)](https://github.com/seijinrosen/lssr/actions/workflows/tests.yml)\n[![CodeQL](https://github.com/seijinrosen/lssr/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/seijinrosen/lssr/actions/workflows/codeql-analysis.yml)\n[![codecov](https://codecov.io/gh/seijinrosen/lssr/branch/main/graph/badge.svg)](https://codecov.io/gh/seijinrosen/lssr)\n[![Downloads](https://pepy.tech/badge/lssr)](https://pepy.tech/project/lssr)\n[![Downloads](https://pepy.tech/badge/lssr/month)](https://pepy.tech/project/lssr)\n[![Downloads](https://pepy.tech/badge/lssr/week)](https://pepy.tech/project/lssr)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## インストール\n\nPython 3.7 以上がインストールされていれば利用可能です。\n\n```sh\npip install lssr\n```\n\n## 使い方\n\n```sh\n# カレントディレクトリにあるアイテムを表示\nlssr\n\n# 指定したディレクトリにあるアイテムを表示（相対パス）\nlssr path/to/target/dir\n\n# 絶対パスでの指定\nlssr /absolute/path/to/target/dir\n\n# ソート順を逆にする\nlssr -r\nlssr --reverse path/to/target/dir\n\n# 最終内容更新時刻順の新しい順にソート\nlssr -t\n# 古い順\nlssr -tr\n\n# ファイルサイズの大きい順にソート\nlssr -S\n# 小さい順\nlssr -rS\n\n# オプションの並び順は、ある程度自由です\nlssr -t path/to/target/dir --reverse\n\n# ヘルプを表示\nlssr -h\nlssr --help\n\n# バージョンを表示\nlssr -V\nlssr --version\n```\n\n## `ls` コマンドとの違い\n\n- アイテムの並び順が異なります。デフォルトで、以下の順序でアイテムが表示されます。\n  - フォルダ -> ファイル\n  - Unicode\n\n  つまり、GitHub と同様の並び順になるはずです。\n\n- ドットファイルを含んだリスト形式でのカラー表示がデフォルトです（`ls -AGl` と同等）。\n- 現在、パスを2つ以上指定することはできません。その代わり、オプションの指定はパスの前後どちらでも良いです。\n- 多くのオプションがまだ実装されていません。利用できるオプションは上記「使い方」やヘルプコマンドを参照してください。\n',
    'author': 'seijinrosen',
    'author_email': '86702775+seijinrosen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seijinrosen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
