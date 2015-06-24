#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diff_match_patch import diff_match_patch


def apply_patch(patchtxt, page):
    dmp = diff_match_patch()
    patch = dmp.patch_fromText(patchtxt)
    patched, patch_results = dmp.patch_apply(patch, page)
    if any(r is False for r in patch_results):
        raise SystemExit('Failed to apply one or more patches')
    return patched


''' Be a script '''
if __name__ == '__main__':
    import os, sys
    assert len(sys.argv) == 4, 'Usage: {0} PATCH TXTIN TXTOUT'.format(sys.argv[0])
    patch, txtin, txtout = sys.argv[1:4]
    with open(txtin) as f:
        txt = f.read().decode('utf-8')
    if os.path.exists(patch):
        with open(patch) as f:
            patchtxt = f.read().decode('utf-8')
        patched = apply_patch(patchtxt, txt)
    else:
        patched = txt

    with open(txtout, 'w') as f:
        f.write(patched.encode('utf-8'))
