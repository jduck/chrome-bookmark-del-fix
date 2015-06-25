#!/usr/bin/env python

#
# Patch Chrome's bookmark manager to stop deleting bookmarks on accident...
# by Joshua "jduck" Drake
#
# See also:
# https://code.google.com/p/chromium/issues/detail?id=244563
# https://code.google.com/p/chromium/issues/detail?id=462861
# https://code.google.com/p/chromium/issues/detail?id=479322
#

import sys
import os
import shutil
import data_pack as dp

CHROME_PATH = '/Applications/Google Chrome.app/Contents'

def detect_version():
    import plistlib as pll

    PLIST = '/'.join([ CHROME_PATH, 'Info.plist' ])
    plist = pll.readPlist(PLIST)
    ver = plist['CFBundleShortVersionString']
    return ver

def apply_patch(ver):
    RSRCPAK = '/'.join([ CHROME_PATH, 'Versions', ver, 'Google Chrome Framework.framework', 'Resources', 'resources.pak' ])
    RSRC_ID = 1005

    if not os.path.isfile(RSRCPAK):
        print('[!] Unable to find resource.pak at %s !!' % RSRCPAK)
        sys.exit(1)

    orig = RSRCPAK + '.orig'
    if os.path.isfile(orig):
        print('[!] found a back up file. did you already apply this? If so, try reverting the patch...')
        print('    $ mv "%s" \\\n    "%s"' % (orig, RSRCPAK))
        sys.exit(1)
    shutil.copyfile(RSRCPAK, orig)

    print "[*] Reading packed data..."
    data = dp.ReadDataPack(RSRCPAK)

    print "[*] Patching resource[%d]..." % RSRC_ID
    rsrc_fn = "%d" % 1005
    with open(rsrc_fn, 'wb') as f:
        f.write(data.resources[RSRC_ID])
    os.system("patch %s 0001-Pressing-Delete-key-in-bookmark-manager-s-search-box.patch" % rsrc_fn)
    with open(rsrc_fn, 'rb') as f:
        newdata = f.read()
    os.unlink(rsrc_fn)

    # put the patched data back into the resources
    data.resources[RSRC_ID] = newdata

    print "[*] Writing packed data ..."
    dp.WriteDataPack(data.resources, RSRCPAK, data.encoding)
    print "[*] Done! Restart Chrome to activate the changes we made!"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ver = sys.argv[1]
        print('[*] Patching specified Chrome version: %s' % ver)
    else:
        ver = detect_version()
        print('[*] Detected Chrome version %s' % ver)

    apply_patch(ver)
