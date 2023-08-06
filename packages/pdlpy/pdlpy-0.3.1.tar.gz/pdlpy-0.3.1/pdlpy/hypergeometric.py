from pdlpy.distribution import Distribution
from pdlpy.math import ncr


class Hypergeometric(Distribution):
    """
    Discrete probability distribution of a random variable X
    that describes the probability of successes in draws
    from a finite test set
    """

    def __init__(self, n: int, N: int, M: int):
        """
        Parameters
        n: the number of draws
        N: the size of the test set
        M: the number of successes
        """

        if N < 0:
            raise ValueError("N must be greater than or equal to 0")

        if n < 0 or n > N:
            raise ValueError("n must be in the range [0, N]")

        if M < 0 or M > N:
            raise ValueError("M must be in the range [0, N]")

        self._n = n
        self._N = N
        self._M = M
        self._mean = n * M / N
        self._median = 0
        self._mode = 0
        self._var = n * M / N * (1 - M / N) * (N - n) / (N - 1)

    def __str__(self):
        return (
            "Hypergeometric("
            f"n={self._n}, "
            f"N={self._N}, "
            f"M={self._M}, "
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

        if x < 0 or x > self._n:
            raise ValueError("x must be in the range [0, n]")

        return (
            ncr(self._M, x)
            * ncr(self._N - self._M, self._n - x)
            / ncr(self._N, self._n)
        )

    def cdf(self, x: int) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """

        if x < 0 or x > self._n:
            raise ValueError("x must be in the range [0, n]")

        if x == 0:
            return self.pmf(0)
        else:
            return self.pmf(x) + self.cdf(x - 1)
