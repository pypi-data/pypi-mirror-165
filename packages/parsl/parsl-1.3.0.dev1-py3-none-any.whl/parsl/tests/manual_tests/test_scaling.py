from parsl.configs.htex_local import config
from parsl import python_app
import parsl


@python_app
def platform(sleep=10, stdout=None):
    import platform
    import time
    time.sleep(sleep)
    return platform.uname()


if __name__ == "__main__":

    parsl.load(config)

    futures = [platform(sleep=i) for i in range(10)]

    for fu in futures:
        print(fu.result())
