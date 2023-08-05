# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_dmarc_parser']

package_data = \
{'': ['*']}

install_requires = \
['imap-tools>=0.56.0,<0.57.0', 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['simple-dmarc-parser = '
                     'simple_dmarc_parser.dmarc_parser:main']}

setup_kwargs = {
    'name': 'simple-dmarc-parser',
    'version': '1.0.3',
    'description': 'A Python script that processes DMARC reports from a mailbox and gives a basic summary.',
    'long_description': '# simple-dmarc-parser\n\nsimple-dmarc-parser is a basic Python script that reads the contents of an IMAP mailbox, seeks out DMARC RUA reports, downloads and parses them in aggregate to provide a basic summary of passes and failures.\n\n## Function\nThe script will print any DMARC reports which had a failed result, so that you can review them. A summary will also be printed at the end by default, which shows how many reports had a pass/fail result from each provider, how many pass/fail results were found for each IP address, and how many pass/fail results were found for each domain.\n\nThe summary can be disabled if you only want to see failures. See the usage section for appropriate options.\n\n## Installation\nIt\'s recommended that you install simple-dmarc-parser via pip so that it is available on the system:\n\n`pip install simple-dmarc-parser`\n\n## Usage\nThe script reads all unread messages in the mailbox provided, so you should only use this with a dedicated DMARC RUA address. simple-dmarc-parser does not process RUF reports.\n\nsimple-dmarc-parser accepts command line arguments, a config file, or it can prompt you for the IMAP server information.\n\nRun `simple-dmarc-parser -h` for command line argument options. Or, just run `simple-dmarc-parser` and you will be prompted for the appropriate information. Your password will not be shown as you enter it.\n\nA config file option is recommended for any sort of automation so that your credentials aren\'t potentially exposed in process lists. See the [example config file](simple-dmarc-parser.conf.example), place it in an appropriate location with sensible permissions, and run using `simple-dmarc-parser --config /path/to/config`\n\n**Use the delete messages option with caution.** Messages deleted with this option **are not** put in a deleted folder. They are immediately removed from the IMAP server with no option for recovery. \n\n## Automatic Reports\nYou can use cron to run simple-dmarc-parser regularly and send you its output via email, or whatever source you can send to via the command line.\n\nFor example, the following cron entry running on your mail server will result in nightly DMARC summaries being sent by cron to the user running the job:\n\n`0 0 * * * simple-dmarc-parser --config /path/to/config`\n\nIf you prefer a version that only notifies you on errors, you can use [this example script](dmarc_report.sh). Make sure you have `mailutils` installed, put the script in root\'s home directory, and install the following cronjob as root:\n\n`0 0 * * * /root/dmarc_report.sh`\n\nThe script assumes your configuration is in /etc/simple-dmarc-parser.conf (make sure silent is true), and it will send its report to the root user on the local system. If you wish to send to send the reports off-system, change "root" to a full email address.',
    'author': 'FrostTheFox',
    'author_email': 'python@frostthefox.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FrostTheFox/simple-dmarc-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
