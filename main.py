# encoding: utf-8

import sys
import requests
import textwrap
from bs4 import BeautifulSoup

from workflow import Workflow


def main(wf):
    args = wf.args

    vocab_url = "http://www.vocabulary.com/dictionary/{0}".format(args[0])
    mw_url = "http://www.merriam-webster.com/dictionary/{0}".format(args[0])

    r = requests.get(vocab_url)
    soup = BeautifulSoup(r.text)

    short_def = soup.find('div', id='definition').find('p', class_='short')
    if short_def is not None:
        short_def_text = short_def.text
        wf.add_item(title="--- Short Definition ---",
                    largetext=short_def_text,
                    valid=False)

        for line in textwrap.wrap(short_def_text, width=60):
            wf.add_item(title=line, valid=False)
    else:
        wf.add_item(title="Nothing Found", valid=False)

    wf.add_item(title="Find on MW",
                subtitle=mw_url,
                arg=mw_url,
                valid=True)

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
