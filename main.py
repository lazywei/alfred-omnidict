# encoding: utf-8

import sys
import requests
# import textwrap
from bs4 import BeautifulSoup

from workflow import Workflow


def main(wf):
    args = wf.args

    vocab_url = "http://www.vocabulary.com/dictionary/{0}".format(args[0])
    mw_url = "http://www.merriam-webster.com/dictionary/{0}".format(args[0])
    howjsay_url = "http://www.howjsay.com/index.php?word={0}".format(args[0])

    r = requests.get(vocab_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Show the searching word
    wf.add_item(title="Definition for {0}:".format(args[0]), valid=False)

    # Vocab short definition
    short_def = soup.select('div.section.blurb > p.short')
    if len(short_def) > 0:
        short_def_text = short_def[0].text
        wf.add_item(title="[CMD+L] | {0} ...".format(short_def_text[:30]),
                    largetext=short_def_text,
                    valid=False)

    def_grps = soup.select('div.section.definition > div.group')

    max_def_count = 3
    for def_grp in def_grps:

        def_count = 0

        for def_ in def_grp.select('div.ordinal h3.definition'):

            if def_count < max_def_count:
                wf.add_item(
                    title=def_.get_text(' | ', strip=True),
                    valid=False)
            else:
                wf.add_item(title="more ...", valid=False)
                break

            def_count = def_count + 1

        wf.add_item(title="------------", valid=False)

    # wf.add_item(title="Nothing Found", valid=False)

    wf.add_item(title="Open on Vocabulary.com",
                subtitle=vocab_url,
                arg=vocab_url,
                valid=True)

    wf.add_item(title="Open on MW",
                subtitle=mw_url,
                arg=mw_url,
                valid=True)

    wf.add_item(title="Open on Howjsay",
                subtitle=howjsay_url,
                arg=howjsay_url,
                valid=True)

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
