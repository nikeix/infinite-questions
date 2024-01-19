import asyncio
import random
import re
from enum import Enum
from typing import Tuple
from urllib.parse import unquote

import aiohttp
import wikipediaapi
from yarl import URL

from .config import WIKIPEDIA_LANGUAGE, WIKIPEDIA_API_PROJECT_NAME, WIKIPEDIA_RANDOM_ARTICLE_URL, \
    WIKIPEDIA_NEWS_AND_AFFAIRS_PAGE_NAME


class TriviaType(Enum):
    RANDOM = 'RANDOM'
    NEWS = 'NEWS'


def _wiki_instance():
    return wikipediaapi.Wikipedia(WIKIPEDIA_API_PROJECT_NAME, language=WIKIPEDIA_LANGUAGE)


def _get_page_summary(page_name: str) -> str:
    wiki = _wiki_instance()
    wiki_page = wiki.page(page_name)

    return wiki_page.summary


def _get_linked_articles(page: wikipediaapi.WikipediaPage) -> list[wikipediaapi.WikipediaPage]:
    result = []
    for name, linked_page in page.links.items():
        if wikipediaapi.Namespace.MAIN == linked_page.namespace:
            result.append(linked_page)

    return result


async def _resolve_random_article() -> Tuple[URL, str]:
    async with aiohttp.ClientSession() as session:
        async with session.head(WIKIPEDIA_RANDOM_ARTICLE_URL, allow_redirects=True) as response:
            url = response.url
            page_name = re.findall('/wiki/(.+)', str(url))[0]
            return url, unquote(page_name)


async def _get_random_articles_summaries(max_articles: int) -> list[Tuple[URL, str]]:
    results = set(await asyncio.gather(*[_resolve_random_article() for _ in range(max_articles)]))

    while len(results) < max_articles:
        # Just in case we hit the same one twice
        results.add(await _resolve_random_article())

    return [(r[0], _get_page_summary(r[1])) for r in results]


async def _get_news_articles_summaries(max_articles: int) -> list[Tuple[URL, str]]:
    wiki = _wiki_instance()
    news_articles = list(set(_get_linked_articles(wiki.page(WIKIPEDIA_NEWS_AND_AFFAIRS_PAGE_NAME))))
    random.shuffle(news_articles)

    results = [(art.fullurl, art.summary) for art in news_articles[:max_articles]]
    return results


async def get_articles(trivia: TriviaType, max_articles: int) -> list[Tuple[URL, str]]:
    if trivia == TriviaType.RANDOM:
        article_resolver = _get_random_articles_summaries
    elif trivia == TriviaType.NEWS:
        article_resolver = _get_news_articles_summaries
    else:
        raise ValueError("")

    return await article_resolver(max_articles)
