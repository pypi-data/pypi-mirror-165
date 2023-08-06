# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['signal_cli_socket']
setup_kwargs = {
    'name': 'signal-cli-socket',
    'version': '0.7',
    'description': 'A package to use with the signal-cli made by AsamK.',
    'long_description': '# signal-cli-socket\nUse with https://github.com/AsamK/signal-cli\n\n# Example Code\n```\nfrom signal-cli-socket import signal\n\nsig = Signal("+491635558756")\n\n# send message to a user\nsig.send_message("+491625555457", "Hello there!")\nsig.send_message_attatchment("+491625555457", "Here is the picture that you wanted.", "./photo.jpg")\n\n# send messages to a group\nsig.send_message("KBHvLSJlKKb8FQSA6Ajo5pB8/mgPjaTEbr68Mb5MwkA=", "Hello there!", True)\nsig.send_message_attatchment("KBHvLSJlKKb8FQSA6Ajo5pB8/mgPjaTEbr68Mb5MwkA=", "Enjoy the view!", "./photo.jpg", True)\n```\n\n# Signal Object\n| Parameter | Type | required | default value\n| ------- | ------------------ | ---- | ---\n| account | string | yes | \n| socket_path | string | no | /tmp/signal-cli/socket\n| id | int | no | random value\n\n| Option  | Description       \n| ------- | ------------------\n| send_message() | Send a Message to a User or a group\n| send_message_attatchment() | Send a Message to a User or a group with an attachment\n',
    'author': 'Nickwasused',
    'author_email': 'contact.nickwasused.fa6c8@simplelogin.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Nickwasused/signal-cli-socket',
    'package_dir': package_dir,
    'py_modules': modules,
}


setup(**setup_kwargs)
