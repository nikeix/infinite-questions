import re
from typing import Tuple
from urllib.parse import unquote

import aiohttp
import wikipediaapi
from yarl import URL

from infinite_questions.config import WIKIPEDIA_LANGUAGE, WIKIPEDIA_API_PROJECT_NAME, WIKIPEDIA_RANDOM_ARTICLE_URL


def _get_page_summary(page_name: str) -> str:
    wiki = wikipediaapi.Wikipedia(WIKIPEDIA_API_PROJECT_NAME, language=WIKIPEDIA_LANGUAGE)
    wiki_page = wiki.page(page_name)

    return wiki_page.summary


async def _resolve_random_article() -> Tuple[URL, str]:
    async with aiohttp.ClientSession() as session:
        async with session.head(WIKIPEDIA_RANDOM_ARTICLE_URL, allow_redirects=True) as response:
            url = response.url
            page_name = re.findall('/wiki/(.+)', str(url))[0]
            return url, unquote(page_name)


async def get_random_article_summary() -> Tuple[URL, str]:
    url, page_name = await _resolve_random_article()
    return url, _get_page_summary(page_name)
