#!/usr/bin/env python
# -*- coding: utf-8 -*-


def link_image(name, caption):
    return '![{capt}]({name})'.format(name=name, capt=caption)


def link(page, img):
    caption, rest = page.split('\n\n', 1)
    caption = caption.replace('\n', ' ')
    img_link = link_image(img, caption)
    linked = '\n\n'.join([img_link, rest])
    return linked


''' Be a script '''
if __name__ == '__main__':
    import os, sys
    assert len(sys.argv) == 4, 'Usage: {0} IMG TXTIN TXTOUT'.format(sys.argv[0])
    img, txtin, txtout = sys.argv[1:4]
    with open(txtin) as f:
        txt = f.read()
    if os.path.exists(img):
        linked = link(txt, img)
    else:
        linked = txt

    with open(txtout, 'w') as f:
        f.write(linked)
