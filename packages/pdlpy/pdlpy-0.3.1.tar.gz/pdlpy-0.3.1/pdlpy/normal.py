from pdlpy.distribution import Distribution
from pdlpy.math import e, erf, pi, sqrt


class Normal(Distribution):
    """
    Continuous probability distribution of a random variable X
    which is assumed to be additively produced by many small events
    """

    def __init__(self, e: float, v: float):
        """
        Parameters
        e: the expectation of the distribution
        v: the variance of the distribution
        """
        self._e = e
        self._v = v
        self._mean = e
        self._median = e
        self._mode = e
        self._var = v

    def __str__(self):
        return (
            "Normal("
            f"e={self._e:.2f}, "
            f"v={self._v:.2f}, "
            f"mean={self._mean:.2f}, "
            f"median={self._median:.2f}, "
            f"mode={self._mode:.2f}, "
            f"var={self._var:.2f}"
            ")"
        )

    def pdf(self, x: float) -> float:
        """
        Probability Density Function

        Parameters
        x: the value of random variable X

        Returns
        The relative likelihood that X will lie in the sample space of x
        """
        return (1 / sqrt(2 * pi * self._v)) * e ** (-((x - self._e) ** 2 / 2 * self._v))

    def cdf(self, x: float) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """
        return (1 + erf((x - self._e) / (sqrt(self._v * 2)))) / 2
