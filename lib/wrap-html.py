#!/usr/bin/env python
# -*- coding: utf-8 -*-


''' Be a script '''
if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 5, 'Usage: {0} DOC TEMPL VIDS OUT'.format(sys.argv[0])
    docn, templn, vidsn, outn = sys.argv[1:]
    with open(docn) as f:
        doc = f.read().decode('utf-8')
    with open(templn) as f:
        templ = f.read().decode('utf-8')
    with open(vidsn) as f:
        vids = f.read().decode('utf-8')

    page = templ\
        .replace('{contents}', doc)\
        .replace('{videos}', vids)

    with open(outn, 'w') as f:
        f.write(page.encode('utf-8'))
