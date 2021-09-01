import functools
"""def dec(func):
    @functools.wraps(func)
    def do_twice(name, *args, **kwargs):
        # do someting before
        func(name)
        func(name)
        #do somethng after
        # return value
    return do_twice

@dec
def say_hi(name):
    print("hi {0}".format(name))
    # return value"""

import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        x = sum([i**2 for i in range(10001)])
    return x

if __name__ == "__main__":
    #print(say_hi.__name__)
    t = waste_some_time(10)
    print(t)
    print(sum([i**2 for i in range(10001)]))
