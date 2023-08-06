# TruckersFM.py

Simple API wrapper for TruckersFM, the popular simulating radio station.

# Table of contents
- [Installation and setup](# TruckersFM.py

Simple API wrapper for TruckersFM, the popular simulating radio station.

# Table of contents
- [Installation and setup](https://github.com/mrbean565/TruckersFM.py#installation-and-setup)
- [Usage](https://github.com/mrbean565/TruckersFM.py#usage)
- [Support](https://github.com/supraaxdd/TruckersMP.py/#support)
- [Contributing](https://github.com/supraaxdd/TruckersMP.py/#contributing)
- [Acknowledgements](https://github.com/supraaxdd/TruckersMP.py/#acknowledgements)

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
