# TruckersFM.py

Simple API wrapper for TruckersFM, the popular simulating radio station.

# Table of contents
- [Installation and setup](https://github.com/mrbean565/TruckersFM.py#installation-and-setup)
- [Usage](https://github.com/mrbean565/TruckersFM.py#usage)
- [Support](https://github.com/mrbean565/TruckersFM.py/#support)


## Installation and setup

**This module is compatible with Python v3+**

You can install this module via PyPI:
```bash
$ pip install truckersfm.py
```

 
## Usage

```py
from truckersfm import TruckersFM

truckersmp = TruckersFM()

# Returns the song currently playing
print(truckersfm.currentSong())

# Fetches current song title
print(truckersfm.currentSongTitle()) 

# Fetches current song artist
print(truckersfm.currentSongArtist()) 

```

Without calling a function eachtime:

```py

currentSong = truckersfm.currentSong()

```

Available Methods:

```py
currentSong()                # Fetches current song
currentSongTitle()           # Fetches current song title
currentSongArtist()          # Fetches current song artist
currentPresenter()           # Fetches current presenter
currentPresenterName()       # Fetches current presenter's name
currentShow()                # Fetches current show
currentShowTitle()           # Fetches current show title                    
```

## Support

If you need help with anything, you should preferably contact BEAN#0001 on discord. If that is not possible, feel free to open a new issue. Note that if the issue is invalid, it may be closed.
