from pdlpy.distribution import Distribution


class Uniform(Distribution):
    """
    Continuous probability distribution of a random variable X
    in an interval where any value of X has an equal probability
    """

    def __init__(self, a: float, b: float):
        """
        Parameters
        a: the minimum value of X
        b: the maximum value of X
        """

        if a >= b:
            raise ValueError("a must be less than b")

        self._a = a
        self._b = b
        self._mean = (a + b) / 2
        self._median = (a + b) / 2
        self._mode = (a + b) / 2
        self._var = (b - a) ** 2 / 12

    def __str__(self):
        return (
            "Uniform("
            f"a={self._a:.2f}, "
            f"b={self._b:.2f}, "
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

        if x < self._a:
            return 0.0

        if x > self._b:
            return 0.0

        return 1 / (self._b - self._a)

    def cdf(self, x: float) -> float:
        """
        Cumulative Distribution Function

        Parameters
        x: the value of the random variable X

        Returns
        The probability that X will take a value less than or equal to x
        """

        if x <= self._a:
            return 0.0

        if x >= self._b:
            return 1.0

        return (x - self._a) / (self._b - self._a)
