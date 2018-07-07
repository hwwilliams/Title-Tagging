# Title-Tagging
A script to embed title tags in video files

Dependencies: Python 3, [Mutagen](https://github.com/quodlibet/mutagen)
Install Mutagen: 'pip install mutagen'

This script relies on files being named in fairly specific and uniform fashion.
It will attempt to extract an episode name and embed that into the file's title tag.
A valid file would look similar to 'Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4'.

The most important part of this naming scheme is the last instance of '-' plus the
period before the file extension. Whatever is between the last instance of '-' and the period will
be the episode name, minus any leading or trailing white spaces.

An example is below:
Full file name: Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4
Extracted title tag: Why Learn Python?
