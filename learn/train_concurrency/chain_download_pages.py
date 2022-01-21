import time
from bs4 import BeautifulSoup
import asyncio
from aiohttp import ClientSession


async def download_page(url, session):
    async with session.get(url) as resp:
        size = len(await resp.read())
        print(f"Download {size} symbols from {url}")


async def download_pages(url, session):
    async with session.get(url) as resp:
        soup = BeautifulSoup(await resp.text(), 'lxml')
        urls = [a['href'] for a in soup.find(id='content').find_all('a')]
    await asyncio.gather(*(download_page(link, session) for link in urls))


async def main() -> None:
    url = r"https://fgiesen.wordpress.com/"
    async with ClientSession() as session:
        async with session.request(method='GET', url=url) as resp:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            archive_links = [a['href'] for a in soup.find('li', class_='widget widget_archive').find_all('a')]

        await asyncio.gather(*(download_pages(link, session) for link in archive_links))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(main())
    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} seconds")