from dataclasses import dataclass


@dataclass(init=False, order=True)
class Time:
    time: int

    def __init__(self, time):
        if isinstance(time, str):
            time = sum(
                60**i * int(amount) for i, amount in enumerate(time.split(":")[::-1])
            )
        self.time = time

    def serialise(self):
        return self.time

    def __str__(self):
        return ":".join(f"{x:02}" for x in divmod(self.time, 60))

    def __repr__(self):
        return f"{self.__class__.__qualname__}('{self}')"
