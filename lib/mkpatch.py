#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diff_match_patch import diff_match_patch


def make_patch(text1, text2):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(text1, text2)
    dmp.diff_cleanupSemantic(diffs)
    patches = dmp.patch_make(text1, diffs)
    patchtxt = dmp.patch_toText(patches)
    return patchtxt


''' Be a script '''
if __name__ == '__main__':
    import os, sys
    assert len(sys.argv) == 4, 'Usage: {0} TXT1 TXT2 PATCH'.format(sys.argv[0])
    txt1, txt2, patch = sys.argv[1:4]
    with open(txt1) as f:
        text1 = f.read().decode('utf-8')
    with open(txt2) as f:
        text2 = f.read().decode('utf-8')
    patchtxt = make_patch(text1, text2)
    if patchtxt is not None:
        with open(patch, 'w') as f:
            f.write(patchtxt.encode('utf-8'))
