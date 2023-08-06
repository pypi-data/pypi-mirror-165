from somelib import somefunc, someapp
import parsl
from parsl import python_app
from parsl.configs.htex_local import config

if __name__ == "__main__":

    parsl.load(config)

    x = someapp(2)
    print(x.result())

    app = python_app(somefunc)
    print(app)
    y = app(2)

    print(y.result())
