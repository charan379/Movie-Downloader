# Movie-Downloader

---
Version : 1.1

Author : Gadila Shashank Reddy

---

## About

This simple python script is a wrapper over openload movies and helps to explore
, search and download movies all in a single package via a command line
interface.

## Installation

This script is supposed to work on all UNIX based systems (GNU-Linux, Mac...)
I haven't tested this on Windows.

Python 2 and Python3 are supported. The dependencies of this
script are

* [requests](https://pypi.org/project/requests/)

* [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)

* [youtube-dl](https://pypi.org/project/youtube_dl/)
  * This requires PhantomJS. See [here](http://phantomjs.org/download.html)

To install dependencies :
Python2 : pip install -r requirements.txt
Python3 : pip3 install -r requirements.txt

Inbuilt libraries used. Make sure these are importable.

* argparse
* os
* time
* unquote and urlparse from urllib.parse
* webbrowser

## Usage

```md
$ python3 movie.py -h
usage: movie.py [-h] [-d] [[-g [G] | -y [Y] | -s [S [S ...]]] [-f | -t | -p]

Openload Movies wrapper

optional arguments:
  -h, --help      show this help message and exit
  -d              Optional flag to download if possible
  -g [G]          Specify a genre
  -y [Y]          Specify a release year
  -s [S [S ...]]  Search a movie
  -f              Featured Movies
  -t              Top Rated Movies
  -p              Popular/Most viewed Movie
  -m              OpenLoad movies list
```

Using the script is pretty simple. Some examples are given.

* Some usage examples. Note the multi worded search.

```md
$ python3 movie.py -f
$ python3 movie.py -f -d
$ python3 movie.py -g adventure
$ python3 movie.py -y 2009
$ python3 movie.py -s avengers infinity war
```

* Default interface to select a movie to watch/download

Typical results when using the search function.

```md
28**************************************************
Beyond The Sky (2018)
IMDb N/A
**************************************************
29**************************************************
The Perfect Bride: Wedding Bells (2018)
IMDb 6.6
**************************************************
30**************************************************
Eyes In The Hills (2018)
IMDb N/A
**************************************************
Enter number to watch the movie or 0 for next page
```

Typical results otherwise.

```md
30**************************************************
Jumanji: Welcome to the Jungle (2017)

When a young nun at a cloistered abbey in Romania
takes her own life, a priest with a haunted past
and a novitiate on the threshold of her final vows
are sent by the Vatican to investigate. Together
they uncover the order’s unholy secret. Risking
not only their lives but their faith and their
very souls, they confront a malevolent ...

TS | 7.9 stars
**************************************************
Enter a number to load that movie or 0 to load next page or q to quit
```

The only difference in both these type of results is the presence of picture
quality. In both cases, the rating is out of 10 stars.

At the prompt if you enter 0 then the next page is loaded (if present) and if
you input a valid movie number, then the script initiates download if the "-d"
flag is specified else there's another yes/no confirmation to download the
movie. If y/Y is entered then again download is initiated else the movie is
openend in a new browser tab.

All downloads happen in the directory where the script resides.

5 wrong inputs terminates the script.

## Regarding development env and bugs

This script has been developed and tested on python 3.7.0 running on an Arch
Linux x86_64 machine and is expected to run on python 3.5.x and above.

Incase of any issue with script when running with python 3, do raise an issue on the repository.
Incase of any issue with script running python 2 then do this:
* Run the script using Python 3.5+
* If it works continue using it with Python 3
* If it doesn't then raise an issue on the repository.
* In case you're wondering why not continue using Python 2, head [here](https://wiki.python.org/moin/Python2orPython3)
* If you're still stubborn to continue using Python 2.x then fix it yourself.

Why did [I](https://github.com/gadilashashank) include support for Python2 ? Simple answer: [I](https://github.com/gadilashashank) DIDN'T. 

Thanks for using the script :)
