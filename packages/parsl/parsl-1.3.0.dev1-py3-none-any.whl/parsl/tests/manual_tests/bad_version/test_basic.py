import argparse

import parsl
from parsl.app.app import python_app  # , bash_app
from htex_local import config
parsl.load(config)


@python_app
def platform(sleep=10, stdout=None):
    import platform
    import time
    import sys
    time.sleep(sleep)
    return platform.uname(), "{}".format(sys.version_info)


def test_platform(n=2):
    # sync
    x = platform(sleep=0)
    print(x.result())

    d = []
    for i in range(0, n):
        x = platform(sleep=5)
        d.append(x)

    print(set([i.result()for i in d]))

    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sitespec", default=None)
    parser.add_argument("-c", "--count", default="10",
                        help="Count of apps to launch")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Count of apps to launch")
    args = parser.parse_args()

    if args.debug:
        parsl.set_stream_logger()

    x = test_platform()
