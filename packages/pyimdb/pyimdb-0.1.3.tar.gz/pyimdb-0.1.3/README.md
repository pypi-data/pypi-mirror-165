# Python IMDB

[![Python package](https://github.com/hudsonbrendon/pyimdb/actions/workflows/python-package.yml/badge.svg)](https://github.com/hudsonbrendon/pyimdb/actions/workflows/python-package.yml)
[![Github Issues](http://img.shields.io/github/issues/hudsonbrendon/pyimdb.svg?style=flat)](https://github.com/hudsonbrendon/pyimdb/issues?sort=updated&state=open)
![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)

![Logo](https://static.amazon.jobs/teams/53/images/IMDb_Header_Page.jpg?1501027252)

A wrapper python for imdb.com

# Quick start

```bash
$ pip install pyimdb
```

# Usage

With your key in hand, it's time to authenticate, so run:

```python
>>> from pyimdb import IMDB

>>> imdb = IMDB()
```

# Popular TV Shows

Returns list of popular tv shows.

```python
>>> imdb.popular_tv_shows()
```
or

```python
>>> imdb.popular_tv_shows(limit=10)
```

# Popular Movies

Returns list of popular movies.

```python
>>> imdb.popular_movies()
```
or

```python
>>> imdb.popular_movies(limit=10)
```

# TOP Rated TV Shows

Returns list of top rated tv shows.

```python
>>> imdb.top_rated_tv_shows()
```
or

```python
>>> imdb.top_rated_tv_shows(limit=2)
```

# TOP Rated Movies

Returns list of top rated movies.

```python
>>> imdb.top_rated_movies()
```
or

```python
>>> imdb.top_rated_movies(limit=2)
```

# Dependencies

- Python >=3.8

# License

[MIT](http://en.wikipedia.org/wiki/MIT_License)
