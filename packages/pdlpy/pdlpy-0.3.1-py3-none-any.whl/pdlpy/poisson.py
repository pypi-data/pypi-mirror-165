from pdlpy.distribution import Distribution
from pdlpy.math import e, factorial, floor


class Poisson(Distribution):
    """
    Discrete probability distribution of a random variable X
    which defines the probability of a given number of events
    occurring in a fixed interval of time or space
    """

    def __init__(self, r: float):
        """
        Parameters
        r: the average number of events
        """

        if r <= 0:
            raise ValueError("r must be greater than 0")

        self._r = r
        self._mean = r
        self._median = floor(r + 1 / 3 - 0.02 / r)
        self._mode = floor(r)
        self._var = r

    def __str__(self):
        return (
            "Poisson("
            f"r={self._r:.2f}, "
            f"mean={self._mean:.2f}, "
            f"median={self._median:.2f}, "
            f"mode={self._mode:.2f}, "
            f"var={self._var:.2f}"
            ")"
        )

    def pmf(self, x: int) -> float:
        """
        Probability Mass Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value exactly equal to x
        """

        if x < 0:
            raise ValueError("x must be greater than or equal to 0")

        return (self._r**x) * (e ** (-self._r)) / factorial(x)

    def cdf(self, x: int) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """

        if x < 0:
            raise ValueError("x must be greater than or equal to 0")

        if x == 0:
            return self.pmf(0)
        else:
            return self.pmf(x) + self.cdf(x - 1)
