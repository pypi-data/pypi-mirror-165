from parsl.serialize import ParslSerializer


def double(x):
    return x * 2


def var_args(x, y=5):
    return x + y


def test_1():

    serializer = ParslSerializer()

    bufs = serializer.pack_apply_message(double, (5,), {})

    fn, args, kwargs = serializer.unpack_apply_message(bufs)

    print(fn)
    print(args)
    print(kwargs)
    print(fn(*args, **kwargs))
    assert fn(*args, **kwargs) == 10, "Wrong output"


if __name__ == "__main__":

    test_1()
