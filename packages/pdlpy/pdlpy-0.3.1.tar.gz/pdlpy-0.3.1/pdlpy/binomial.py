from pdlpy.distribution import Distribution
from pdlpy.math import floor, ncr


class Binomial(Distribution):
    """
    Discrete probability distribution of a random variable X
    which defines the number of successes in a sequence of
    independent yes-no experiments
    """

    def __init__(self, n: int, p: float):
        """
        Parameters
        n: the size of the sequence
        p: the probability of success
        """

        if n < 0:
            raise ValueError("n must be greater than or equal to 0")

        if p < 0 or p > 1:
            raise ValueError("p must be in the range [0, 1]")

        self._n = n
        self._p = p
        self._mean = n * p
        self._median = floor(n * p)
        self._mode = floor((n + 1) * p)
        self._var = n * p * (1 - p)

    def __str__(self):
        return (
            "Binomial("
            f"n={self._n}, "
            f"p={self._p:.2f}, "
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

        return ncr(self._n, x) * self._p**x * (1 - self._p) ** (self._n - x)

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
