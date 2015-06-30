#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from functools import reduce


''' Constants and tests '''
# Report section / page number line always has this marker:
isContextLine = lambda s: u'•' in s
# All pages end with this for some reason:
weirdEndThing = u''
# All possible sentence endings
br = ur'[\.\?\!\…][”\)]?'


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

def capitalizeAbbrs(page):
    with open('abbrevs.md') as f:
        abbrevs = map(lambda l: l[2:].split(']: '), f.readlines())
    capitalized = page
    for abbrev, expanded in abbrevs:
        lower = abbrev.lower()
        catch = ur'(?P<pre>\W){a}(?P<post>\W)'.format(a=lower)
        repl = lambda m: u'{pre}=|{a}={d}={post}'.format(
            a=abbrev, d=expanded.decode('utf-8').strip(), **m.groupdict())
        capitalized, _ = re.subn(catch, repl, capitalized)
    return capitalized

def markRefs(page):
    with open('refs.txt') as f:
        refs = f.read().decode('utf-8').strip().replace(' ', '\s').split('\n')
    italicized = page
    for ref in refs:
        catch = ur'(?<!\=\^)(?P<r>{r})(?P<post>[^=\w])'.format(r=ref)
        repl = lambda m: u'=^{r}={post}'.format(**m.groupdict())
        italicized, _ = re.subn(catch, repl, italicized)
    return italicized

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
    # change preceding space to a newline
    newlined = page.replace(u' •', u'\n•')
    bulletted = newlined.replace(u'•\t', u'  *')
    return bulletted

def ol(page):
    repl = lambda m: '{n}.'.format(**m.groupdict())
    listed, _ = re.subn(u'\n(?P<n>\\d{1,2})\)\t', repl, page)
    return listed

def romans(page):
    rnums = {
        'i': 1,
        'ii': 2,
        'iii': 3,
        'iv': 4,
        'v': 5,
        'vi': 6,
        'vii': 7,
        'viii': 8,
        'ix': 9,
        'x': 10,
    }
    romanRe = r'\s(?P<rs>{rs}).	 '.format(rs='|'.join(rnums.keys()))
    repl = lambda m: '\n    {n}. '.format(n=rnums[m.groupdict()['rs']])
    de_romaned, _ = re.subn(romanRe, repl, page)
    return de_romaned

def cite(page):
    citation = ur'(?P<ends>{br} ?)(?P<citeNo>\d+)\n'.format(br=br)
    def cite(match):
        gs = match.groupdict()
        return u'{ends}[^{citeNo}]\n'.format(**gs)
    cited, _ = re.subn(citation, cite, page)
    return cited

def callToAction(page):
    called = page.replace('Call to Action', '#### Call to Action\n')
    calls = called.replace('Calls to Action','#### Calls to Action\n')
    return calls

def patchBugs(page):
    # possibly due to a bug in the patch library, some changes from `for-humans/` never make it to patches
    # there are only a few, so they are manually fixed here
    patched = page.replace(u'The apologies don’t come readily.\n', u'> The apologies don’t come readily.\n')
    return patched

def encode(page):
    return page.encode('utf-8')


''' Utils '''
compose = lambda *fns:\
    lambda init: reduce(lambda v, f: f(v), reversed(fns), init)


''' The magic '''
autofix = compose(
    encode,
    patchBugs,
    callToAction,
    cite,
    romans,
    ol,
    bullet,
    semanticLineBreak,
    fixEllipses,
    doubleNewlines,
    markRefs,
    capitalizeAbbrs,
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
