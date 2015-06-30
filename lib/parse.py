#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from functools import reduce
from markdown import Markdown, to_html_string
from markdown.util import etree
from markdown.extensions import Extension, toc
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from mdx_outline import OutlineExtension


class MarkPagenum(Preprocessor):
    def run(self, lines):
        self.page = 0
        pagenum = r'<!-- page (?P<n>\d{3}) -->'
        pagetmpl = lambda n: '<!-- page {n:03d} -->'.format(n=n)
        blahnum = lambda n: '=p{n}='.format(n=n)

        def mark_pagenum(line):
            if line == '':
                return line
            new_marker = re.search(pagenum, line)
            if new_marker:
                nextp = int(new_marker.groupdict()['n'])
                assert nextp == self.page + 1
                line = line.replace(pagetmpl(nextp), '')
                self.page = nextp
                if line == '':
                    return line
                if new_marker.start() == 0:
                    return line + blahnum(nextp)
                else:
                    return line + blahnum(nextp - 1) + ' ' + blahnum(nextp)
            else:
                return line + blahnum(self.page)

            return marked

        all_marked = map(mark_pagenum, lines)
        # from pprint import pprint
        return all_marked


class InsertTOC(Preprocessor):
    def run(self, lines):
        return ['[TOC]', ''] + lines


class PageNumData(Treeprocessor):
    def run(self, root):
        pagere = r'=p(?P<n>\d{1,3})='

        def pull(text):
            pages = [int(m.groupdict()['n'])
                for m in re.finditer(pagere, text)]
            if len(pages) > 0:
                text, _ = re.subn(pagere, '', text)
            return pages, text

        for el in root.iter():
            if el.tag == 'div':
                continue
            pages = set()
            if el.text is not None:
                to_add, el.text = pull(el.text)
                pages.update(to_add)
            if el.tail is not None:
                to_add, el.tail = pull(el.tail)
                pages.update(to_add)

            if len(pages) > 0:
                el.set('data-p', ' '.join(map(str, sorted(pages))))


class Figcaption(Treeprocessor):
    def run(self, root):
        for p in filter(lambda t: t.tag == 'p', root):
            for img in filter(lambda t: t.tag == 'img', p):
                p.tag, fig = 'figure', p
                figcaption = etree.SubElement(p, 'figcaption')
                figcaption.text = img.get('alt')


class TRCExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('markpagenum', MarkPagenum(md), '_begin')
        md.preprocessors.add('inserttoc', InsertTOC(md), '>markpagenum')
        md.treeprocessors.add('pagenum', PageNumData(md), '_end')
        md.treeprocessors.add('figcaption', Figcaption(md), '_end')


class TRCMarkdown(Markdown):
    def __init__(self, *args, **kwargs):
        self.output_formats = {'trc': self.to_site}
        self.output_folder = kwargs['output_folder']

        kwargs.setdefault('output_format', 'trc')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.stripTopLevelTags = False

    def to_site(self, el):
        # import pdb; pdb.set_trace()
        # site = to_html_string(el)
        # with open(self.output_folder + '/TRC-2015-Executive-Summary.html', 'w') as f:
        #     f.write(site.encode('utf-8'))
        # return ''
        return to_html_string(el)


''' Be a script '''
if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 3, 'Usage: {0} SOURCE OUT'.format(sys.argv[0])
    sourceName, outName = sys.argv[1:]
    with open(sourceName) as f:
        source = f.read().decode('utf-8')
    md = TRCMarkdown(
        lazy_ol=False,
        output_folder='./',
        extensions=[
            TRCExtension(),
            toc.TocExtension(permalink=True),
            OutlineExtension({}),
        ])
    out = md.convert(source)
    with open(md.output_folder + outName, 'w') as f:
        f.write(out.encode('utf-8'))
