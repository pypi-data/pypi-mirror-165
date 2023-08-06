import parsl
import dill

from parsl.configs.htex_local import config

parsl.load(config)


class ParslActor():

    def __init__(self):
        pass

    def incoming(self):
        return "incoming_url"

    def outgoing(self):
        return "incoming_url"


class Actor(ParslActor):

    def __init__(self, x):
        self.x = x

    def set(self, value):
        self.x += value

    def get(self):
        return self.x


@parsl.python_app
def remote(class_pkl):
    import pickle

    x = pickle.loads(class_pkl)
    cinstance = x(1)
    results = []
    for i in range(10):
        m = cinstance.get()
        cinstance.set(i)
        results.append(m)

    return results


if __name__ == "__main__":

    x = dill.dumps(Actor)
    print(x)
