# GoatPie
[![Build](https://ci.codeberg.org/api/badges/RefBW/goatpie/status.svg)](https://codeberg.org/RefBW/goatpie/issues)

"GoatCounter" analytics for the CLI, written in Python - get it?

![Screenshot](screenshot.png)

**Note**: This project is a *work in progress* and subject to breaking changes on a daily basis!


## Installation

It's available from [PyPi](https://pypi.org/project/gesetze) using `pip`:

```text
pip install goatpie
```

## Getting started

Using this library is straightforward.


### Commandline

Pretty much self-explanatory - otherwise, `--help` is your friend:

```text
$ goatpie --help
Usage: goatpie [OPTIONS] URL

  Provides 'Goatcounter' statistics for URL

Options:
  -u, --update         Initiates update of local database
  -l, --limit INTEGER  Shows visits & pageviews in the last XY days
  --version            Show the version and exit.
  --help               Show this message and exit.
```


### Package

The underlying module may also be used directly:

```python
from goatpie import GoatPie

# Initialize it
obj = GoatPie(url, token)

# Update database
# (1) Last update not before one hour (in seconds)
obj.update(3600)

# (2) Force database update
obj.update(0)

# Get pageviews (last seven days)
print(obj.get_pageviews(7))

          Day  Pageviews
0  2022-08-28          1
1  2022-08-27         13
2  2022-08-26         20
3  2022-08-25         35
4  2022-08-24         84
5  2022-08-23         64
6  2022-08-22         23
```


## Roadmap

- [x] Add tests
- [ ] Add more tests
- [x] Add logger
- [x] Config file
- [ ] Explain configuration
