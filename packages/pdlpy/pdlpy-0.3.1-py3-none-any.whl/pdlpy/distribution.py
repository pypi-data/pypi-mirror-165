class Distribution:
    def __init__(self, mean=0.0, median=0.0, mode=0.0, var=0.0):
        self._mean = mean
        self._median = median
        self._mode = mode
        self._var = var

    @property
    def mean(self) -> float:
        return self._mean

    @property
    def median(self) -> float:
        return self._median

    @property
    def mode(self) -> float:
        return self._mode

    @property
    def var(self) -> float:
        return self._var
