from parsl import python_app


@python_app
def someapp(x):
    return x + 1


def somefunc(x):
    return x * 2
