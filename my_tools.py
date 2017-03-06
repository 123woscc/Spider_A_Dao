from functools import wraps
import time


def time_use(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        end=time.time()
        print('用时:{}'.format(end-start))
        return result
    return wrapper


if __name__ == '__main__':
    @time_use
    def foo():
        print('start!')
        time.sleep(3)
        print('end!')
    foo()

