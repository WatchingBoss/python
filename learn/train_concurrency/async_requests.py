import logging
import re
import sys
from pathlib import Path
import urllib.error
import urllib.parse
from typing import IO

import asyncio
import aiofiles
import aiohttp
import aiohttp.http_exceptions
from aiohttp import ClientSession


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stderr
    )
logger = logging.getLogger('areq')
logging.getLogger('chardet.charsetprober').disable = True

HREF_RE = re.compile(r'href="(.*?)"')


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method='GET', url=url, **kwargs)
    resp.raise_for_status()
    logger.info(f"Got response {resp.status} for {url}")
    html = await resp.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    result = set()
    try:
        html = await fetch_html(url, session, **kwargs)
    except(
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            f"aiohttp exception for {url} [{getattr(e, 'status', None)}]: {getattr(e, 'message', None)}"
        )
        return result
    except Exception as e:
        logger.exception(f"Non-aiohttp exception occured: {getattr(e, '__dict__', {})}")
        return result
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception(f"Error parsing URL: {link}")
            else:
                result.add(link)
        logger.info(f"Found {len(result)} for {url}")
        return result


async def write_one(path: Path, url: str, **kwargs) -> None:
    res = await parse(url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(path, 'a') as f:
        for l in res:
            await f.write(f"{url}\t{l}\n")
        logger.info(f"Wrote result for source URL: {url}")


async def main(path: Path, urls: set, **kwargs):
    async with ClientSession() as session:
        await asyncio.gather(*(write_one(path=path, url=url, session=session, **kwargs) for url in urls))


if __name__ == "__main__":
    here = Path(__file__).parent

    with open(here.joinpath('urls.txt')) as f:
        urls = set(map(str.strip, f))

    outpath = here.joinpath('result.txt')
    with open(outpath, 'w') as f:
        f.write("source_url/parsed_url\n")

    asyncio.get_event_loop().run_until_complete(main(outpath, urls))