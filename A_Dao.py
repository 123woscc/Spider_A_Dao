import requests
from bs4 import BeautifulSoup
import my_tools
import multiprocessing

import threading
import gevent
from gevent import monkey
# monkey.patch_all()

import asyncio
import aiohttp

from concurrent import futures




# @my_tools.time_use
def get_image_urls(start_page, end_page):
    main_url = 'https://h.nimingban.com/f/COSPLAY?page={}'
    urls = [u for u in (main_url.format(x) for x in range(start_page, end_page + 1))]
    image_urls = []
    for url in urls:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        a_list = soup.find_all('a', class_='h-threads-img-a')
        a_href = [a.get('href') for a in a_list]
        image_urls += a_href
        print(a_href)
    with open('image_urls.txt', 'w') as f:
        f.write('\n'.join(image_urls))

@my_tools.time_use
def multiple_threads_test():
    page_list=[(1,10),(10,20),(20,30)]
    th_list=[]
    for page in page_list:
        th=threading.Thread(target=get_image_urls,args=(page[0],page[1]))
        th_list.append(th)
    for th in th_list:
        th.start()
    th.join()

@my_tools.time_use
def multiple_processes_test():
    page_list = [(1, 10), (10, 20), (20, 30)]
    pool=multiprocessing.Pool(processes=4)
    for page in page_list:
        pool.apply_async(get_image_urls,(page[0],page[1]))
    pool.close()
    pool.join()

@my_tools.time_use
def gevent_test():
    page_list = [(1, 10), (10, 20), (20, 30)]
    jobs=[]
    for page in page_list:
        jobs.append(gevent.spawn(get_image_urls,page[0],page[1]))

        gevent.joinall(jobs)



sem=asyncio.Semaphore(4)

def decoder(content):
    return content.decode('utf-8')

def format_str(s):
    return s.replace('\n','').replace(' ','').replace('\t','')

@asyncio.coroutine
def get_image_urls2(start_page, end_page):
    main_url = 'https://h.nimingban.com/f/COSPLAY?page={}'
    urls = [u for u in (main_url.format(x) for x in range(start_page, end_page + 1))]
    image_urls = []
    for url in urls:
        # html = requests.get(url)
        with(yield from sem):
            response=yield from aiohttp.request('GET',url)
        body=yield from response.read()
        html_str=decoder(body)
        soup = BeautifulSoup(html_str, 'lxml')
        a_list = soup.find_all('a', class_='h-threads-img-a')
        a_href = [a.get('href') for a in a_list]
        image_urls += a_href
        print(a_href)
    with open('image_urls.txt', 'w') as f:
        f.write('\n'.join(image_urls))

@my_tools.time_use
def asyncio_test():
    page_list = [(1, 10), (10, 20), (20, 30)]
    loop=asyncio.get_event_loop()
    f=asyncio.wait([get_image_urls2(page[0],page[1]) for page in page_list])
    loop.run_until_complete(f)

@my_tools.time_use
def futures_threads():
    page_list = [(1, 10), (10, 20), (20, 30)]
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url={
            executor.submit(get_image_urls,page[0],page[1]):ind for ind,page in enumerate(page_list)
        }
        # for future in futures.as_completed(future_to_url):
        #     range_ind=future_to_url[future]
        #     if future.exception() is not None:
        #         print('{0} generated an exception:{1}'.format(range_ind,future.exception()))
        #     else:
        #         print('{0} get url is {1}'.format(range_ind, future.result()))

@my_tools.time_use
def futures_processes():
    page_list = [(1, 10), (10, 20), (20, 30)]
    with futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_to_url={
            executor.submit(get_image_urls,page[0],page[1]):ind for ind,page in enumerate(page_list)
        }




if __name__ == '__main__':
    # 单线程--14s  suface--30s
    # get_image_urls(1,30)
    # 多线程--11s  surface--18s
    # multiple_threads_test()
    #多进程--6s    surface--11s
    # multiple_processes_test()
    #协程--?s      surface--54s
    # gevent_test()
    # asyncio_test()
    # futures_threads()
    futures_processes()
    pass
