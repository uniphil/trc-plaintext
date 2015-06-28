#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from functools import reduce
from markdown import markdown
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
                el.set('data-p', ','.join(map(str, sorted(pages))))

        return root


class TRCExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('markpagenum', MarkPagenum(md), '_begin')
        md.preprocessors.add('inserttoc', InsertTOC(md), '>markpagenum')
        md.treeprocessors.add('pagenum', PageNumData(md), '_end')


''' Be a script '''
if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 3, 'Usage: {0} SOURCE OUTFOLDER'.format(sys.argv[0])
    sourceName, outfolder = sys.argv[1:]
    with open(sourceName) as f:
        source = f.read().decode('utf-8')
    marked = markdown(source, extensions=[
        TRCExtension(),
        toc.TocExtension(permalink=True),
        OutlineExtension({}),
    ])
    print(marked.encode('utf-8'))
