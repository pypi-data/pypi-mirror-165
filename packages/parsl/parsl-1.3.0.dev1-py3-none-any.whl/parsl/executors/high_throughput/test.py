from zmq_pipes import SignalSender, SignalReceiver
import zmq


def test_basic(ctx):
    sender = SignalSender(ctx)
    receiver = SignalReceiver(ctx)

    sender.send()

    print(receiver.recv())
    sender.close()
    receiver.close()


def test_poll(ctx):
    sender = SignalSender(ctx)
    receiver = SignalReceiver(ctx)

    sender.send(b"HELLO")
    # print(receiver.recv())
    poller = zmq.Poller()
    poller.register(receiver.socket, zmq.POLLIN)

    socks = dict(poller.poll(timeout=100))  # in ms
    print("Here")
    assert receiver.socket in socks
    assert socks[receiver.socket] == zmq.POLLIN

    print("Message present")
    message = receiver.recv()
    print("Message: ", message)
    assert message == b"HELLO"
    sender.close()
    receiver.close()


if __name__ == "__main__":

    ctx = zmq.Context()

    # test_basic(ctx)

    test_poll(ctx)
