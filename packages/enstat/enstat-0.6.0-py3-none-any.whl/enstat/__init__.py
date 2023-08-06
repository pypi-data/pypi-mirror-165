from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from numpy.typing import DTypeLike

from . import mean  # noqa: F401
from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


class scalar:
    r"""
    Ensemble average of a scalar.
    Add samples to it using :py:func:`scalar.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    They are derived from the following members:

    *   :py:attr:`scalar.first`: Sum of the first statistical moment.
    *   :py:attr:`scalar.second`: Sum of the second statistical moment.
    *   :py:attr:`scalar.norm`: Number of samples.

    To continue an old average by specifying:

    :param float first: Sum of the first moment.
    :param float second: Sum of the second moment.
    :param int norm: Number of samples.
    """

    def __init__(self, first: float = 0, second: float = 0, norm: float = 0):

        self.first = first
        self.second = second
        self.norm = norm

    def add_sample(self, datum: float):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.
        :param datum: Sample.
        """

        datum = np.array(datum)
        self.first += np.sum(datum)
        self.second += np.sum(datum**2)
        self.norm += datum.size

    def mean(self) -> float:
        r"""
        Current mean.
        Samples can be added afterwards without any problems.
        :return: Mean.
        """

        if self.norm == 0:
            return np.NaN

        return self.first / self.norm

    def variance(self) -> float:
        r"""
        Current variance.
        Samples can be added afterwards without any problems.
        :return: Variance.
        """

        if self.norm <= 1:
            return np.NaN

        d = (self.second / self.norm - (self.first / self.norm) ** 2) * self.norm
        n = self.norm - 1

        return d / n

    def std(self) -> float:
        r"""
        Current standard deviation.
        Samples can be added afterwards without any problems.
        :return: Standard deviation.
        """

        return np.sqrt(self.variance())


class static:
    r"""
    Ensemble average of an nd-array (of same size for all samples).
    Add samples to it using :py:func:`static.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    They are derived from the following members:

    *   :py:attr:`static.first`: Sum of the first statistical moment.
    *   :py:attr:`static.second`: Sum of the second statistical moment.
    *   :py:attr:`static.norm`: Number of samples.

    Furthermore, the following members are available:

    *   :py:attr:`static.shape`: Shape of the data.
    *   :py:attr:`static.size`: Size of the data (= prod(shape)).

    :param compute_variance:
        If set ``False`` no second moment will be computed (making things slightly faster).
        In that case, the variance an standard deviation will not be available.

    :param shape:
        The shape of the data.
        If not specified it is determined form the first sample.

    :param dtype:
        The type of the data.
        If not specified it is determined form the first sample.

    :param first: Continued computation: Sum of the first moment.
    :param second: Continued computation: Sum of the second moment.
    :param norm: Continued computation: Number of samples (integer).
    """

    def __init__(
        self,
        compute_variance: bool = True,
        shape: tuple[int] = None,
        dtype: DTypeLike = np.float64,
        first: ArrayLike = None,
        second: ArrayLike = None,
        norm: ArrayLike = None,
    ):

        self.compute_variance = compute_variance
        self.norm = norm
        self.first = first
        self.second = second

        if norm is not None:
            assert first is not None
            assert second is not None or not compute_variance

        if shape is None:
            return

        if norm is not None:
            assert shape == norm.shape
            assert shape == second.shape
            assert shape == norm.shape
        else:
            self.norm = np.zeros(shape, np.int64)
            self.first = np.zeros(shape, dtype)
            if compute_variance:
                self.second = np.zeros(shape, dtype)

    def _allocate(self, shape, dtype):

        self.norm = np.zeros(shape, np.int64)
        self.first = np.zeros(shape, dtype)
        if self.compute_variance:
            self.second = np.zeros(shape, dtype)

    @property
    def dtype(self):
        """
        The type of the data.
        """
        return self.first.dtype

    @property
    def shape(self):
        """
        The shape of the data.
        """
        return self.first.shape

    @property
    def size(self):
        """
        The size of the data.
        """
        return np.prod(self.first.shape)

    def ravel(self) -> scalar:
        r"""
        Return as :py:class:`scalar`: all entries are summed.
        :return: Ensemble average.
        """

        return scalar(
            first=np.sum(self.first),
            second=np.sum(self.second),
            norm=np.sum(self.norm),
        )

    def add_sample(self, data: ArrayLike, mask: ArrayLike = None):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param data: The sample.
        :param mask: Mask entries (boolean array).
        """

        if self.first is None:
            self._allocate(data.shape, data.dtype)

        # masked data
        if mask is not None:
            incl = np.logical_not(mask)
            self.norm[incl] += 1
            self.first[incl] += data[incl]
            if self.compute_variance:
                self.second[incl] += data[incl] ** 2
            return

        # unmasked data
        self.norm += 1
        self.first += data
        if self.compute_variance:
            self.second += data**2

    def add_point(self, datum: float | int, index: int):
        """
        Add a single point. Note that::

            ensemble.add_point(datum, index)

        Is equivalent to::

            data = np.empty(ensemble.shape)
            mask = np.ones(ensemble.shape, dtype=bool)
            data[index] = datum
            mask[index] = False
            ensemble.add_sample(data, mask)

        (but faster).
        """

        if self.first is None:
            raise OSError("shape should be pre-specified")

        self.norm[index] += 1
        self.first[index] += datum

        if self.compute_variance:
            self.second[index] += datum**2

    def mean(self, min_norm: int = 1) -> ArrayLike:
        r"""
        Current mean.
        Samples can be added afterwards without any problems.
        :param min_norm: Minimum number of samples to consider as value output.
        :return: Mean.
        """

        if self.norm is None:
            return None

        n = np.where(self.norm > 0, self.norm, 1)
        ret = self.first / n
        return np.where(self.norm >= min_norm, ret, np.NaN)

    def variance(self, min_norm: int = 2) -> ArrayLike:
        r"""
        Current variance.
        Samples can be added afterwards without any problems.
        :param min_norm: Minimum number of samples to consider as value output.
        :return: Variance.
        """

        if self.norm is None:
            return None

        assert self.compute_variance
        n = np.where(self.norm > 1, self.norm, 2)
        ret = (self.second / n - (self.first / n) ** 2) * n / (n - 1)
        return np.where(self.norm >= min_norm, ret, np.NaN)

    def std(self, min_norm: int = 2) -> ArrayLike:
        r"""
        Current standard deviation.
        Samples can be added afterwards without any problems.
        :param min_norm: Minimum number of samples to consider as value output.
        :return: Standard deviation.
        """

        if self.norm is None:
            return None

        return np.sqrt(self.variance(min_norm))


def _expand_array1d(data, size):

    tmp = np.zeros((size), data.dtype)
    tmp[: data.size] = data
    return tmp


class dynamic1d(static):
    r"""
    Ensemble average of an 1d-array (which grows depending of the size of the samples).
    Add samples to it using :py:func:`dynamic1d.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying:

    :param compute_variance:
        If set ``False`` no second moment will be computed.
        In that case, the variance an standard deviation will not be available.

    :param size:
        The initial size of the data.
        If not specified it is determined form the first sample.

    :param dtype:
        The type of the data.
        If not specified it is determined form the first sample.

    :param first: Continued computation: Sum of the first moment.
    :param second: Continued computation: Sum of the second moment.
    :param norm: Continued computation: Number of samples (integer).
    """

    def __init__(
        self,
        compute_variance: bool = True,
        size: int = None,
        dtype: DTypeLike = np.float64,
        first: ArrayLike = None,
        second: ArrayLike = None,
        norm: ArrayLike = None,
    ):
        super().__init__(
            compute_variance=compute_variance,
            shape=(size,) if size is not None else None,
            dtype=dtype,
            first=first,
            second=second,
            norm=norm,
        )

    def _expand(self, size: int):

        if size <= self.first.size:
            return

        self.norm = _expand_array1d(self.norm, size)
        self.first = _expand_array1d(self.first, size)

        if self.compute_variance:
            self.second = _expand_array1d(self.second, size)

    def add_sample(self, data: ArrayLike):

        assert data.ndim == 1

        if self.first is None:
            super().add_sample(data)
            return

        self._expand(data.size)
        self.norm[: data.size] += 1
        self.first[: data.size] += data

        if self.compute_variance:
            self.second[: data.size] += data**2

    def add_point(self, datum: float | int, index: int):

        if self.first is None:
            self._allocate(index + 1, type(datum))
        else:
            self._expand(index + 1)

        return super().add_point(datum, index)


if __name__ == "__main__":
    pass
