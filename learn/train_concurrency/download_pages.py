import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
import concurrent.futures


HEADER = {'User-Agend': str(UserAgent().chrome)}


def parse_content_links(html):
    soup = BeautifulSoup(html, 'lxml')
    return [a['href'] for a in soup.find(id='content').find_all('a')]


async def download_page(session, url, require_return=False):
    async with session.get(url) as response:
        if require_return:
            return await response.text()
        else:
            text = await response.text()
            print(f'Download {len(text)} symbols of {url}')


_pool = concurrent.futures.ProcessPoolExecutor()


async def download_and_parse(session, url, parse_func):
    html = await download_page(session, url, require_return=True)
    loop = asyncio.get_event_loop()
    links = await loop.run_in_executor(_pool, parse_func, html)
    return links


async def download_all_pages(urls, parse_func=None):
    async with aiohttp.ClientSession() as session:
        if parse_func is not None:
            return await asyncio.gather(*(download_and_parse(session, url, parse_func) for url in urls))
        else:
            tasks = [asyncio.ensure_future(download_page(session, url)) for url in urls]
            # return await asyncio.gather(*(download_page(session, url) for url in urls))
            await asyncio.gather(*tasks, return_exceptions=True)


def get_links():
    url = r"https://fgiesen.wordpress.com/"
    r = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(r.content, 'lxml')
    archive_links = [a['href'] for a in soup.find('li', class_='widget widget_archive').find_all('a')]
    content_links = asyncio.get_event_loop().run_until_complete(
        download_all_pages(archive_links, parse_func=parse_content_links)
    )
    content_links = [link for sublist in content_links for link in sublist]
    return content_links


def main():
    asyncio.set_event_loop(asyncio.ProactorEventLoop())
    # links = get_links()
    links = [
        'https://fgiesen.wordpress.com/2021/10/04/gpu-bcn-decoding/',
        'https://fgiesen.wordpress.com/2019/07/20/frequency-responses-of-half-pel-filters/',
        'https://fgiesen.wordpress.com/2018/12/10/rate-distortion-optimization/'
    ]
    asyncio.get_event_loop().run_until_complete(download_all_pages(links))


if __name__ == '__main__':
    start_time = time.time()

    main()

    duretion = time.time() - start_time
    print(f'Duration is {duretion:.2f} sec')