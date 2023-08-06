from pdlpy.distribution import Distribution


class Bernoulli(Distribution):
    """
    Discrete probability distribution of a random variable X
    which either takes the value 1 or 0 in a single yes-no
    experiment
    """

    def __init__(self, p: float):
        """
        Parameters
        p: the probability of success
        """

        if p < 0 or p > 1:
            raise ValueError("p must be in the range [0, 1]")

        self._p = p
        self._mean = p
        self._median = 0 if p < 0.5 else 1
        self._mode = 0 if p < 0.5 else 1
        self._var = p * (1 - p)

    def __str__(self):
        return (
            "Bernoulli("
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

        if x not in {0, 1}:
            raise ValueError("x must be either 0 or 1")

        if x == 0:
            return 1.0 - self._p
        else:
            return self._p

    def cdf(self, x: int) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """

        if x not in {0, 1}:
            raise ValueError("x must be either 0 or 1")

        if x == 0:
            return 1.0 - self._p
        else:
            return 1.0
