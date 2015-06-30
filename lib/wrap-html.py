#!/usr/bin/env python
# -*- coding: utf-8 -*-


''' Be a script '''
if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 4, 'Usage: {0} DOC TEMPL OUT'.format(sys.argv[0])
    docn, templn, outn = sys.argv[1:4]
    with open(docn) as f:
        doc = f.read().decode('utf-8')
    with open(templn) as f:
        templ = f.read().decode('utf-8')
    page = templ.replace('{contents}', doc)
    with open(outn, 'w') as f:
        f.write(page.encode('utf-8'))
