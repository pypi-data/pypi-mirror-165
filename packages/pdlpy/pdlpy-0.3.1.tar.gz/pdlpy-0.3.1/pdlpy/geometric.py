from pdlpy.distribution import Distribution
from pdlpy.math import ceil, log2


class Geometric(Distribution):
    """
    Discrete probability distributions of a random variable X
    which defines the number of Bernoulli trials needed to get
    a single success
    """

    def __init__(self, p: float):
        """
        Parameters
        p: the probability of success
        """

        if p < 0 or p > 1:
            raise ValueError("p must be in the range [0, 1]")

        self._p = p
        self._mean = 1 / p
        self._median = ceil(-1 / log2(1 - p)) if p != 1 else 1
        self._mode = 1
        self._var = (1 - p) / (p**2)

    def __str__(self):
        return (
            "Geometric("
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

        if x < 1:
            raise ValueError("x must be greater than or equal to 1")

        return (1 - self._p) ** (x - 1) * self._p

    def cdf(self, x: int) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """

        if x < 1:
            raise ValueError("x must be greater than or equal to 1")

        if x == 1:
            return self.pmf(1)
        else:
            return self.pmf(x) + self.cdf(x - 1)
