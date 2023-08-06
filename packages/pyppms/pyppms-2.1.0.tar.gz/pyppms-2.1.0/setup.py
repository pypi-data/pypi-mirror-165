# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyppms']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyppms',
    'version': '2.1.0',
    'description': "A Python package to communicate with Stratocore's PUMAPI.",
    'long_description': '# PyPPMS\n\n## PUMAPI - Python Interface\n\n[Stratocore][3]\'s *PPMS* booking system offers an API (the so-called *PUMAPI*, short for\nPPMS Utility Management API) for fetching information from the booking system as well as\nchanging its state and properties.\n\nThis is a Python 3 package for talking to the *PUMAPI*.\n\n## Usage Example\n\nFetch email addresses of all active users:\n\n```Python\nfrom pyppms import ppms\nfrom credentials_ppms import PPMS_URL, PPMS_API_KEY\n\nconn = ppms.PpmsConnection(PPMS_URL, PPMS_API_KEY)\n\nprint("Querying PPMS for emails of active users, can take minutes...")\nemails = ppms.get_users_emails(active=True)\nprint(f"Got {len(emails)} email addresses from PPMS:")\nprint("\\n".join(emails))\n```\n\n## Testing\n\nAutomated testing is described in the [`TESTING` document on github][2].\n\n## Note\n\nThe PPMS API sometimes exposes a bit of a surprising behavior. During\ndevelopment of the package, we came across several issues (this list is\ncertainly incomplete):\n\n* HTTP status return code is always `200`, even on failed authentication.\n* Results of queries are a mixture of CSV (with headers) and and text with\n  newlines (with no headers and therefore without structural information on\n  the data). JSON is implemented in some cases only.\n* The CSV headers sometimes do contain spaces between the colons, sometimes\n  they don\'t.\n* Some fields are quoted in the CSV output, some are not. Difficult to separate\n  the values since there are colons in the values too.\n* Semantics of keys is not consistent. Sometimes `user` is the user id,\n  sometimes it refers to the user\'s full name.\n* Using an invalid permission level (e.g. `Z`) with the `setright` action is\n  silently ignored by PUMAPI, the response is still `done` even though this\n  doesn\'t make any sense.\n* There is no (obvious) robust way to derive the user id from the user\'s full\n  name that is returned e.g. by `getrunningsheet`, making it very hard to\n  cross-reference it with data from `getuser`.\n* The result of the `getrunningsheet` query in general is not suited very well\n  for automated processing, it seems to be rather tailored for humans and\n  subject to (mis-) interpretation.\n* Unfortunately `Username` and `Systemname` are not the unique id, they are\n  rather the full description. Therefore sometimes looping over all users and\n  systems is necessary.\n* Some results have a very strange format - for example, the starting time of\n  the next booking is given as *minutes from now* instead of an absolute time.\n* Official documentation is rather rudimentary, i.e. it contains almost no\n  information on what is returned in case wrong / invalid parameters are\n  supplied and similar situations.\n\n## References\n\n* [Imagopole PPMS Java client][1]\n\n[1]: https://github.com/imagopole/ppms-http-client/blob/master/src/main/java/org/imagopole/ppms/api/PumapiRequest.java\n[2]: https://github.com/imcf/pyppms/blob/master/TESTING.md\n[3]: https://www.stratocore.com/\n',
    'author': 'Niko Ehrenfeuchter',
    'author_email': 'nikolaus.ehrenfeuchter@unibas.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pyppms/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
