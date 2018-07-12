# Title-Tagging
A script to embed title tags in video files. Currently only MP4 is supported.

**Dependencies:** Python 3, [Mutagen](https://github.com/quodlibet/mutagen), and [Progress](https://github.com/verigak/progress/)

Install Mutagen by running `pip install mutagen`

Install Progress by running `pip install progress`

---

This script relies on files being named in fairly specific and uniform fashion.
It will attempt to extract an episode name and embed that into the file's title tag.

A valid file would look similar to 'Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4'.

The most important part of this naming scheme is the last instance of ' - ' plus the
period before the file extension. Whatever is between the last instance of ' - ' and the period will
be the episode name, minus any leading or trailing white spaces.

I use this to populate the metadata fields inside [Plex](https://www.plex.tv/) when using a [personal media library with embedded metadata](https://support.plex.tv/articles/200265256-naming-home-series-media/). Having the title tags set allows [Plex](https://www.plex.tv/) to pull that data instead of having to manually rename each file's episode name from within [Plex](https://www.plex.tv/).

---

### An example of the correct format of a file name is below

**Full file name:** Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4

**Extracted title tag:** Why Learn Python?
