# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['replyowl']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'html2text>=2020.1.16,<2021.0.0']

setup_kwargs = {
    'name': 'replyowl',
    'version': '0.1.2',
    'description': 'Email reply body generator for HTML and text',
    'long_description': '# replyowl: Email reply body generator for HTML and text in Python\n\n[![PyPI](https://img.shields.io/pypi/v/replyowl)][pypi]\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/replyowl)][pypi]\n[![Build](https://img.shields.io/github/checks-status/smkent/replyowl/main?label=build)][gh-actions]\n[![codecov](https://codecov.io/gh/smkent/replyowl/branch/main/graph/badge.svg)][codecov]\n[![GitHub stars](https://img.shields.io/github/stars/smkent/replyowl?style=social)][repo]\n\n[![replyowl][logo]](#)\n\nreplyowl creates email bodies with quoted messages. Provide the original message\nand your reply message, and replyowl will combine them into a new message. The\nreturned content can be used as the text and/or HTML body content of a new\nemail. HTML-to-text conversion is performed with [html2text][html2text].\n\n## Installation\n\n[replyowl is available on PyPI][replyowl-pypi]:\n\n```\npip install replyowl\n```\n\n## Usage\n\n```py\nfrom replyowl import ReplyOwl\n\nowl = ReplyOwl()\ntext, html = owl.compose_reply(\n    content="<i>New</i> reply <b>content</b>",\n    quote_attribution="You wrote:",\n    quote_text="Original message text",\n    quote_html="<b>Original</b> message text",\n)\n\nprint(text)\n# _New_ reply **content**\n#\n# ----\n#\n# You wrote:\n#\n# > Original message text\n\nprint(html)  # (output formatted for readability)\n# <!DOCTYPE html>\n# <html>\n#   <head>\n#     <title></title>\n#   </head>\n#   <body>\n#     <i>New</i> reply <b>content</b>\n#     <div>You wrote:<br />\n#     </div>\n#     <blockquote style="margin-left: 0.8ex; padding-left: 2ex;\n#                        border-left: 2px solid #aaa; border-radius: 8px;" type="cite">\n#       <b>Original</b> message text\n#     </blockquote>\n#   </body>\n# </html>\n```\n\nLinks in HTML are preserved when creating plain text email bodies:\n```py\nfrom replyowl import ReplyOwl\n\nowl = ReplyOwl()\ntext, html = owl.compose_reply(\n    content=(\n        \'Check <a href="https://example.com/">this</a> out<br />\'\n        \'Or this: <a href="https://example.net/">https://example.net/</a>\'\n    ),\n    quote_attribution="You wrote:",\n    quote_text="Send me a URL",\n    quote_html="Send me a <i>URL</i>",\n)\n\nprint(text)\n# Check this (https://example.com/) out\n# Or this: https://example.net/\n#\n# ----\n#\n# You wrote:\n#\n# > Send me a URL\n```\n\nIf the quoted HTML content contains a `<body>` tag, that is preserved:\n```py\nfrom replyowl import ReplyOwl\n\nowl = ReplyOwl()\ntext, html = owl.compose_reply(\n    content="Hello there",\n    quote_attribution="You wrote:",\n    quote_text="Hi",\n    quote_html=\'<html><body class="sender_body"><b>Hi</b></body></html>\',\n)\n\nprint(html)  # (output formatted for readability)\n# <html>\n#   <body class="sender_body">\n#     Hello there\n#     <div>\n#     You wrote:<br/>\n#     </div>\n#     <blockquote style="margin-left: 0.8ex; padding-left: 2ex;\n#                        border-left: 2px solid #aaa; border-radius: 8px;" type="cite">\n#       <b>Hi</b>\n#     </blockquote>\n#   </body>\n# </html>\n```\n\nA custom value can be provided for the `<blockquote>`\'s `style` tag:\n```py\nfrom replyowl import ReplyOwl\n\nowl = ReplyOwl(blockquote_style="font-weight: bold;")\ntext, html = owl.compose_reply(\n    text, html = owl.compose_reply(\n        content="Your quote is in bold",\n        quote_attribution="You wrote:",\n        quote_text="I\'m going to be in bold when you reply",\n        quote_html="I\'m going to be in bold when you reply",\n    )\n)\n\nprint(html)  # (output formatted for readability)\n# <html>\n#   <body class="sender_body">\n#     Your quote is in bold\n#     <div>\n#     You wrote:<br/>\n#     </div>\n#     <blockquote style="font-weight: bold;" type="cite"\n#       I\'m going to be in bold when you reply\n#     </blockquote>\n#   </body>\n# </html>\n```\n\n## Development\n\nPrerequisites: [Poetry][poetry]\n\n* Setup: `poetry install`\n* Run all tests: `poetry run poe test`\n* Fix linting errors: `poetry run poe lint`\n\n---\n\nCreated from [smkent/cookie-python][cookie-python] using\n[cookiecutter][cookiecutter]\n\n[codecov]: https://codecov.io/gh/smkent/replyowl\n[cookie-python]: https://github.com/smkent/cookie-python\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[gh-actions]: https://github.com/smkent/replyowl/actions?query=branch%3Amain\n[html2text]: https://github.com/Alir3z4/html2text\n[logo]: https://raw.github.com/smkent/replyowl/main/img/replyowl.png\n[poetry]: https://python-poetry.org/docs/#installation\n[pypi]: https://pypi.org/project/replyowl/\n[replyowl-pypi]: https://pypi.org/project/replyowl/\n[repo]: https://github.com/smkent/replyowl\n',
    'author': 'Stephen Kent',
    'author_email': 'smkent@smkent.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/smkent/replyowl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
