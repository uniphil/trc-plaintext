#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
from functools import reduce


''' Constants and tests '''
# Report section / page number line always has this marker:
isContextLine = lambda s: u'•' in s
# All pages end with this for some reason:
weirdEndThing = u''
# All possible sentence endings
br = ur'[\.\?\!…]”?'


''' Steps '''
def decode(page):
    return page.decode('utf-8')

def stripContext(page):
    try:
        first, rest = page.split('\n', 1)
        return rest if isContextLine(first) else page
    except ValueError:  # no newlines
        return page

def strip(page):
    assert page.endswith(weirdEndThing)
    return page.strip()

def capitalizeNewlines(page):
    with open('abbrevs.json') as f:
        abbrevs = json.load(f)
    capitalized = page
    for abbrev, replace in abbrevs.items():
        lower = abbrev.lower()
        catch = ur'(?P<pre>\W){a}(?P<post>\W)'.format(a=lower)
        repl = lambda m: u'{pre}{a}{post}'.format(a=abbrev, **m.groupdict())
        capitalized, _ = re.subn(catch, repl, capitalized)
    return capitalized

def doubleNewlines(page):
    return page.replace('\n', '\n\n')

def fixEllipses(page):
    ellipse = ur'\.{3,}|\.*…'
    ellipsized, _ = re.subn(ellipse, u'…', page)
    return ellipsized

def semanticLineBreak(page):
    sentenceEnd = ur'(?P<endl>{br}\d*) +'.format(br=br)
    def breakLine(match):
        return u'{endl}\n'.format(**match.groupdict())
    broken, _ = re.subn(sentenceEnd, breakLine, page)
    return broken + '\n'  # one trailing newline

def bullet(page):
    page = page.replace(u' •\t', '\n  *')
    return page

def cite(page):
    citation = ur'(?P<ends>{br} ?)(?P<citeNo>\d+)\n'.format(br=br)
    def cite(match):
        gs = match.groupdict()
        return u'{ends}^[{citeNo}]\n'.format(**gs)
    cited, _ = re.subn(citation, cite, page)
    return cited

def encode(page):
    return page.encode('utf-8')


''' Utils '''
compose = lambda *fns:\
    lambda init: reduce(lambda v, f: f(v), reversed(fns), init)


''' The magic '''
autofix = compose(
    encode,
    cite,
    bullet,
    semanticLineBreak,
    fixEllipses,
    doubleNewlines,
    capitalizeNewlines,
    strip,
    stripContext,
    decode,
)


''' Be a script '''
if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 3, 'Usage: {0} INPUT OUTPUT'.format(sys.argv[0])
    inp, out = sys.argv[1:3]
    with open(inp) as f:
        source = f.read()
    fixed = autofix(source)
    with open(out, 'w') as f:
        f.write(fixed)
