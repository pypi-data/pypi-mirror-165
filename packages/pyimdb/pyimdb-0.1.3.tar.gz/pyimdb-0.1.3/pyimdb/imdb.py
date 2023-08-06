from typing import List

import requests
from bs4 import BeautifulSoup


class IMDB(object):

    __BASE_URL = "https://www.imdb.com/chart"

    def __init__(self) -> None:
        self.SESSION = requests.Session()

    def close_session(self) -> None:
        self.SESSION.close()

    @property
    def popular_tv_shows_url(self) -> str:
        return f"{self.__BASE_URL}/tvmeter"

    @property
    def popular_movies_url(self) -> str:
        return f"{self.__BASE_URL}/moviemeter/?ref_=nv_mv_mpm"

    @property
    def top_rated_movies_url(self):
        return f"{self.__BASE_URL}/top/?ref_=nv_mv_250"

    @property
    def top_rated_tv_shows_url(self):
        return f"{self.__BASE_URL}/toptv/?ref_=nv_tvv_250"

    def request(self, url: str) -> BeautifulSoup:
        response = self.SESSION.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def format_data(self, html: BeautifulSoup, limit: int) -> List[dict]:

        posters = html.find_all("td", class_="posterColumn")

        posters_src = [rf"{poster.img['src']}" for poster in posters]

        titles = html.find_all("td", class_="titleColumn")
        titles_name = [
            rf"{title.a.get_text()} {title.span.get_text()}"
            for title in titles
        ]

        ratings = html.find_all("td", class_="ratingColumn imdbRating")
        ratings_score = [
            rating.strong.get_text() if rating.strong else "None"
            for rating in ratings
        ]

        return [
            {"title": title, "rating": rating_score, "poster": poster}
            for title, rating_score, poster in zip(
                titles_name, ratings_score, posters_src
            )
        ][:limit]

    def popular_tv_shows(self, limit: int = 100) -> List[dict]:
        html = self.request(self.popular_tv_shows_url)
        return self.format_data(html, limit)

    def popular_movies(self, limit: int = 100) -> List[dict]:
        html = self.request(self.popular_movies_url)
        return self.format_data(html, limit)

    def top_rated_tv_shows(self, limit: int = 10) -> List[dict]:
        html = self.request(self.top_rated_tv_shows_url)
        return self.format_data(html, limit)

    def top_rated_movies(self, limit: int = 10) -> List[dict]:
        html = self.request(self.top_rated_movies_url)
        return self.format_data(html, limit)
