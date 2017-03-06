from functools import wraps
def foo():
    print('foo')
    # print('foo is running!')



def bar(func):
    func()

def use_logging(func):
    print('{} is running!'.format(func.__name__))
    func()


def use_logging_dec(func):
    def wrapper():
        print('{} is running!'.format(func.__name__))
        return func()
    return wrapper

def use_logging_dec2(func):
    def wrapper(*args,**kwargs):
        print('{} is running!'.format(func.__name__))
        return func(*args,**kwargs)
    return wrapper
# use_logging(foo)

# foo=use_logging_dec(foo)
# foo()

@use_logging_dec
def foo2():
    print('foo2')


# foo2()

@use_logging_dec2
def foo3(name):
    print('name:{}'.format(name))

# foo3('ming')



def test(func):
    print('test')
    return func()

test(foo)


def use_logging_dec3(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if level=='warn':
                print('Leve:warn!')
                print('{} is running!'.format(func.__name__))
            elif level=='info':
                print('Leve:info!')
                print('{} is running!'.format(func.__name__))
            return func(*args,**kwargs)
        return wrapper
    return decorator

@use_logging_dec3('info')
def error_level():
    print('error_level')


error_level()

print(error_level.__name__)
 


