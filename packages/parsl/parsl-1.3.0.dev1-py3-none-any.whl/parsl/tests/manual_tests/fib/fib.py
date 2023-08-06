from parsl import join_app, python_app
import parsl


@python_app
def add(x, y):
    return x + y


@join_app
def fib(n):
    print(f"In fib({n})")
    if n < 2:
        # return n
        return add(n, 0)

    return add(fib(n - 1), fib(n - 2))


parsl.load()


for n in range(2, 10):
    print(f"Running fibonacci of n = {n}")
    fu = fib(n)
    if isinstance(fu, int):
        print(fu)
    else:
        print(fu.result())
