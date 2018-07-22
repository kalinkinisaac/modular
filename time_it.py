import time

def time_it(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('Calculating time: {}'.format(end - start))
        return result
    return wrapped