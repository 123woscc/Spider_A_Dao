import requests
from bs4 import BeautifulSoup
import my_tools
import multiprocessing

import threading


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







if __name__ == '__main__':
    # 单线程--14s
    # get_image_urls(1,30)
    # 多线程--11s
    #multiple_threads_test()
    #多进程--6s
    multiple_processes_test()
    pass
