# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['centurymetadata', 'centurymetadata.server']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodomex>=3.6', 'secp256k1>=0.14.0']

setup_kwargs = {
    'name': 'centurymetadata',
    'version': '0.2',
    'description': 'Encrypt, send, retrieve and decrypt centurymetadata.org files',
    'long_description': '# centurymetadata.org: Long-term Bitcoin Metadata Storage\n\n## About\n\n*Century Metadata* is a project to provide storage for small amounts\nof auxiliary data.  As an example, this is useful for Bitcoin wallets,\nwhich can be restored from 12 seed words, but cannot know about more\ncomplex funds without additional data.  On restore, your wallet would attempt to\nfetch this data from [https://centurymetadata.org](https://centurymetadata.org) or a mirror.\n\nWe are currently in alpha, seeking feedback.\n\n## File Format\n\nThe file format is designed to be self-explanatory and use standard,\nlong-lived primitives as much as possible.  Every file contains a\npreamble, followed by 8192 bytes.  The preamble describes the data\nformat which follows:\n\n```\ncenturymetadata v0\\0SIG[64]|WRITER[33]|READER[33]|GEN[8]|AES[8054]\n\nSIG: BIP-340 SHA256(TAG|TAG|WRITER|READER|GEN|AES)\nWRITER, READER: secp256k1 x-only keys\nTAG: SHA256("centurymetadata v0"[18])\nAESKEY: SHA256(EC Diffie-Hellman of WRITER,READER)\nAES: CTR mode (starting 0, nonce 0) using AESKEY of DATA\nDATA: gzip([TITLE\\0CONTENTS\\0]+), padded with 0 bytes to 8054\\0\n```\n\nThe data itself is a series of NUL-separated title, contents pairs.\nObviously this cannot be validated on the production server, but the\ntest server (which only allows known keys) will check the file is\ncompliant.\n\n## Usage with Bitcoin\n\nThe BIP 32 path recommended for centurymetadata is `0x44315441\'`\n(`DATA`), with `/0\'` as the writer key,\n`/1\'` as the reader key.  Of course, others can also send data\nto your reader key, but you know that the record from your own writer\nkey can be trusted. \n\nThe types of records accepted are as follows:\n\n* Title: `bitcoin psbt`, Body: base64-encoded PSBT\n* Title: `bitcoin transaction` Body: hex-encoded transaction\n* Title: `bitcoin miniscript` Body: miniscript string\n\n## API\n\nThe test API endpoint can be found at [testapi.centurymetadata.org](https://testapi.centurymetadata.org/api/v0).\n\n### Entry Creation: POST /api/v0/authorize/{READER}/{WRITER}/{AUTHTOKEN}\n\nYou need to get an *AUTHTOKEN* for each new entry.  There can only be\none entry for any *READER*/*WRITER* pair, but once the entry is\nauthorized it can be updated by the writer at any time.\n\n### Entry Update: POST /api/v0/update\n\nUpdates a previously authorized writer/reader entry.  The\n`Content-Type: application/x-centurymetadata` should contain a valid\ncenturymetadata file.\n\n### Entries Depth: GET /api/v0/fetchdepth\n\nSince we bundle records by reader prefix (e.g. all readers starting with `42a3` might be bundled together), you need to know how long the prefix is: it starts as an empty prefix and increases by one hex digit as we grow, so bundles are always a reasonable size.\n\nReturns a JSON object with member `depth` containing how many hex digits of reader to use for `fetchbundle`.\n\n### Retrieiving Entries: GET /api/v0/fetchbundle/{READERPREFIX}\n\nThis returns the given bundle, as `Content-Type: application/x-centurymetadata`, consisting of multiple back-to-back\ncentury metadata files.\n\n## Tools\n\nThere is an experimental Python package to encode and decode\ncenturymetadata files in the [GitHub repository](https://github.com/rustyrussell/centurymetadata)\n\n## Roadmap\n\nI\'m committed to maintaining this service for at least 5 years\nas a trial.  After that if it\'s proven useful I would like to\nspin it into a real not-for-profit foundation to provide as much\ncertainty on continuity as possible.\n\n## How Much?\n\nThere will never be a charge for ratelimited updates or retrievals;\nthe idea is to charge a small cost for the creation of new entries to\ncover ongoing running costs.  We may also accept donations.\n\n## Who?\n\nRusty Russell started this as a side project; my original problem was\nhow to give someone timelocked bitcoin, but realized there was a large\nrelated class of problems for someone to solve.\n\n## Feedback\n\nAdvice, suggestions, kudos, blame: hosting is on [GitHub](https://github.com/rustyrussell/centurymetadata), and you can reach us on [Twitter](https://twitter.com/centurymetadata), or send\n[me email](mailto:rusty@rustcorp.com.au) or other contact as listed on \n[my personal site](https://rusty.ozlabs.org).\n',
    'author': 'Rusty Russell',
    'author_email': 'rusty@rustcorp.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://centurymetadata.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
