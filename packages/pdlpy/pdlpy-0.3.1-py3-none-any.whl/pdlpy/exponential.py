from pdlpy.distribution import Distribution
from pdlpy.math import e, log


class Exponential(Distribution):
    """
    Continuous probability distribution of a random variable X
    which defines the time between events in a Poisson process
    """

    def __init__(self, r: float):
        """
        Parameters
        r: the average number of events
        """

        if r <= 0:
            raise ValueError("r must be greater than 0")

        self._r = r
        self._mean = r**-1
        self._median = log(2) / r
        self._mode = 0
        self._var = r**-2

    def __str__(self):
        return (
            "Exponential("
            f"r={self._r:.2f}, "
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

        if x < 0:
            raise ValueError("x must be greater than or equal to 0")

        return self._r * e ** (-self._r * x)

    def cdf(self, x: float) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """

        if x < 0:
            raise ValueError("x must be greater than or equal to 0")

        return 1 - e ** (-self._r * x)
