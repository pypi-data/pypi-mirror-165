import typing


class var_list:
    def __init__(self) -> None:
        self.vars: typing.List[typing.Tuple[str, str]] = list()

    def __len__(self) -> int:
        return len(self.vars)

    def __contains__(self, k: str) -> bool:
        return k in map(lambda item: item[0], self.vars)

    def add(self, k: str, v: str) -> None:
        self.vars.append((k, v))

    def items(self) -> typing.Iterator[typing.Tuple[str, str]]:
        for item in self.vars:
            yield item

    def indices(self, k: str) -> typing.Iterator[int]:
        """
        return the indices containing a given key (var name)
        """

        return map(
            lambda item: item[0],
            filter(
                lambda item: item[1] == k,
                enumerate(map(lambda item: item[0], self.vars)),
            ),
        )

    def index(self, k: str, start: int = 0, end: int = -1) -> int:
        if end < 0:
            end += len(self.vars) + 1
        idxs = list(filter(lambda i: i >= start and i < end, self.indices(k)))
        if len(idxs) == 0:
            raise ValueError(
                f"No element with given key {k} found within range [{start},{end}]."
            )
        return idxs[0]
