# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['netviewer',
 'netviewer.ip',
 'netviewer.model',
 'netviewer.view',
 'netviewer.view.render']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'rich>=12.5.1,<13.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

entry_points = \
{'console_scripts': ['netviewer = netviewer.__main__:run']}

setup_kwargs = {
    'name': 'netviewer',
    'version': '0.1.0',
    'description': 'iproute2 network information viewer',
    'long_description': '# netviewer\n\nA command line utility to display network information.\n\nInformation is parsed from the output of the `iproute2` `ip` command with the json option.\n\n```\nnetviewer [-d|--detail] <command> [<argument>...]\n```\n\nwhere `command` is one of\n\n| Command    | Description                                       |\n| ---------- | ------------------------------------------------- |\n| bridge     | display information on all or specific bridges    |\n| bridges    | list bridges                                      |\n| dump       | dumps the network information as a json file      |\n| interface  | display information on all or specific interfaces |\n| interfaces | list interfaces                                   |\n| link       | display information on all or specific links      |\n| links      | list links                                        |\n| route      | display information on all or specific bridges    |\n| routes     | list routes                                       |\n\nUsing the `-d/--detail` flags with the `interface`, `bridge`, `route` and `link` commands displays detailed information.\n\nItems which are `up` or in an `unknown` state are shown in green otherwise they are shown as dim green (the loopback interface is in an unknown state but can be used, so `unknown` states are also shown as green.)\n\n## Commands\n\n### bridge\n\nDisplays information about bridge devices i.e. network devices that have associated `veth` devices under them.\n\n### dump\n\nDumps the the network information as a json file to the filename passed as an argument.\n\n### interface\n\nDisplays interface information from the `ip address show` command. Pass interface names as arguments to display specific interfaces or leave blank to display all interfaces.\n\n### route\n\nDisplays routing information from the `ip route show` command.\n\n### link\n\nDisplays link information from the `ip link show` command.\n\n## JSON input\n\nUsing the --input option the network information can be displayed from a static json file.\n\n## SVG/HTML Output\n\nUsing the `--save-svg` and `--save-html` options the output can be sent to a file instead.\n\nThis utilises functionality built into [rich](https://rich.readthedocs.io/en/latest/)\n\n### Example SVG Output\n\n![bond0 output](docs/bond0.svg)\n\n## Examples\n\n### Interfaces\n\nFor example using the `interfaces` command\n\n```\n$ netviewer interfaces\n```\n\nin WSL on my machine displays the following information\n\n```\nlo\neth0\nbond0\ndummy0\nsit0\ntunl0\n```\n\n### Interface\n\nAnd using the `interface` command for the `lo` interface\n\n```\n$ netviewer interface lo\n```\n\ndisplays the following information\n\n```\nlo:\n    index: 1\n    type: loopback\n    state: unknown\n    ipv4:\n        scope: host\n        ip: 127.0.0.1/8\n        preferred lifetime: forever\n        valid lifetime: forever\n    ipv6:\n        scope: host\n        ip: ::1/128\n        preferred lifetime: forever\n        valid lifetime: forever\n    flags: LOOPBACK, UP, LOWER_UP\n    mtu:\n        size: 65536\n```\n\n### Link\n\nRunning the `link` command\n\n```\n$ netviewer link bond0\n```\n\nDisplays the following\n\n```\nbond0:\n    index: 2\n    state: down\n    type: ether\n    address: 96:b5:c9:e7:ed:ff\n    broadcast: ff:ff:ff:ff:ff:ff\n    flags: BROADCAST, MULTICAST, MASTER\n    mtu: 1500\n    namespace id: 0\n    group: default\n    queue type: noop\n```\n\n### Link - Detailed Info\n\nRunning the `link` command with the `-d/--detail` option\n\n```\n$ netviewer -d link bond0\n```\n\nDisplays the following\n\n```\nbond0:\n    index: 2\n    state: down\n    type: ether\n    address: 96:b5:c9:e7:ed:ff\n    broadcast: ff:ff:ff:ff:ff:ff\n    flags: BROADCAST, MULTICAST, MASTER\n    mtu: 1500\n    namespace id: 0\n    group: default\n    queue type: noop\n    link info:\n        type: bond\n        mode: balance-rr\n        miimon: 0\n        up delay: 0ms\n        down delay: 0ms\n        peer notifier delay: 0ms\n        use carrier: true (1)\n        ARP interval: 0ms\n        ARP validate: active\n        arp all targets: any\n        primary reselect: always\n        failover mac: none\n        transmit hash policy: layer2\n        resend IGMP: 1\n        all slaves active: dropped\n        minimum links: 0\n        lp interval: 1s\n        packets per slave: 1\n        LACP rate: slow\n        LACP aggregation selection logic: stable\n        tb mode dynamic shuffling: 1\n```\n',
    'author': 'Simon Kennedy',
    'author_email': 'sffjunkie+code@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
