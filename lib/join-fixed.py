#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from functools import reduce

def join(sources):
    def j(a, b):
        bn = int(re.search(r'page-(?P<n>\d{3}).md$', b)
            .groupdict()['n'])
        with open(b) as f:
            bs = f.read().decode('utf-8').strip()
        bs = '<!-- page {n:03d} -->'.format(n=bn) + bs
        if bs.endswith('<!--x-->'):
            bs = bs.replace('<!--x-->', ' ')
        else:
            bs += '\n\n'
        return a + bs
    return reduce(j, sources, '')


''' Be a script '''
if __name__ == '__main__':
    import sys
    assert len(sys.argv) > 2, 'Usage: {0} OUTFILE MD1 [MD2 [MD3...]]'.format(sys.argv[0])
    outname = sys.argv[1]
    sources = sys.argv[2:]
    joined = join(sources)
    with open(outname, 'w') as f:
        f.write(joined.encode('utf-8'))
