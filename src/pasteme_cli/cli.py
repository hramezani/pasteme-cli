"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mpasteme_cli` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``pasteme_cli.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``pasteme_cli.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import json
import sys

import requests
from requests.exceptions import ConnectionError

from .constants import CONNECTION_ISSUE_HINT
from .constants import EPILOG_DESCRIPTION
from .constants import JSON_TEMPLATE
from .constants import LANGUAGES
from .constants import LANGUAGES_HINT
from .constants import PASTEME_API_URL
from .constants import PASTEME_SERVICE_URL

from .customs.argparse import line_range_type

def hyphenated(string):
	return 'hi'

parser = argparse.ArgumentParser(
    description=f'A CLI pastebin tool interacting with PasteMe ({PASTEME_SERVICE_URL}) RESTful APIs.',
    epilog=EPILOG_DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
	'-t', '--title',
	metavar='',
	default='Untitled',
	type=str,
	help='title/description of snippet',
)
parser.add_argument(
	'-l', '--language',
	metavar='',
	default='plaintext',
	type=str,
	choices=LANGUAGES.keys(),
	help=LANGUAGES_HINT,
)
parser.add_argument(
    "-v", "--verbose",
	action = "store_true",
    help="verbosity for post data and response",
)
parser.add_argument(
	'-r', '--range',
	metavar='',
	type=line_range_type,
	help='paste only a range of the file (e.g --range 14-23)',
)
parser.add_argument(
	'file',
	type=open,
	help='script file',
)

def main(args=None):
	args = parser.parse_args(args=args)

	with args.file as source_code:
		code_lines = source_code.readlines()
	
	if args.range:
		start, end = args.range
		code_lines = code_lines[int(start)-1:int(end)]

	context = {
		'title': args.title,
		'body': ''.join(code_lines),
		'language': args.language,
	}

	try:
		response = requests.post(
			url=PASTEME_API_URL,
			data=context
		).json()
  
		if args.verbose:
			print(
       			JSON_TEMPLATE.format(
              		'REQUEST',
              		json.dumps(context, indent=3)
                )
            )
			print(
       			JSON_TEMPLATE.format(
              		'RESPONSE',
              		json.dumps(response, indent=3)
                )
            )

		print(f'PASTE --> {response["url"]}')
		sys.exit()
	except ConnectionError:
		sys.exit(CONNECTION_ISSUE_HINT)

	# TODO: finding a way reading the code/file from the user (maybe file only)
	# like: pasteme -f file.py -L 120:132


def language_is_valid(lang) -> bool:
    return lang in LANGUAGES.keys()