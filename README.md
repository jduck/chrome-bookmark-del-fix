The old (non-enhanced) bookmark manager within Google Chrome (on OSX at least)
before version ~44 accidentally deletes bookmarks in some circumstances. The
script included in this repository patches the "resources.pak" file containing
the buggy javascript code. I am making this available to everyone because:

1. patching the correct file is relatively non-trivial
2. the fix has not shipped in a stable release yet
   *NOTE: PLEASE SHIP THE FIX SO I CAN DEPRECATE THIS GIT REPOSITORY/TOOL!*
3. whenever an update to chrome happens, the patch get's magically undone.

Enjoy!
-jduck


# Chromium Tickets

For more information consult the following tickets (now resolved):

| Ticket                                                       | Synopsis |
| ---------------------------------------------------------- | -------- |
| https://crbug.com/244563 (created 2013 May 28) | The oldest bug report that I could find. Apparently the bug was confirmed, assigned and never worked on again. This ticket got merged into 462861 after I poked a few key people about the issue. |
| https://crbug.com/462861 (created 2015 Feb 28) | Earlier this year, someone else ran into the problem again. The issues was confirmed, found to be a regression, and then finally fixed in April. However, currently the fix is only shipping in the Canary branch. Please stand by (or push people to include) for other channels like beta and stable. |
| https://crbug.com/479322 (created 2015 Apr 21) | Even though the bug was already fixed, a third person ran into the problem again and got sufficiently motivated to create a ticket. There seems to have been some trouble confirming the issue this time around and the bug never got assigned to anyone. This ticket got merged into 244563, again after I poked some key individuals. |


# Thanks

Thanks to all the people that helped figure this problem out and get the fix
process rolling. You know who you are.


# References

I couldn't have accomplished this (especially not as easily) without help from
the following:

http://stackoverflow.com/questions/10633357/how-to-unpack-resources-pak-from-google-chrome
https://code.google.com/p/grit-i18n/

