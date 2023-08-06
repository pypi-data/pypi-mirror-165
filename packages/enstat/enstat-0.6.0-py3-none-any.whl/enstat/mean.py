import warnings

import numpy as np


class Scalar:
    r"""
    Allocate the ensemble average of a scalar.
    Add samples to it using :py:func:`Scalar.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying:

    :param float first: Sum of the first moment.
    :param float second: Sum of the second moment.
    :param int norm: Number of samples.
    """

    def __init__(self, first=0, second=0, norm=0):

        warnings.warn("Deprecated. Use: enstat.scalar.", DeprecationWarning)

        self.m_first = first
        self.m_second = second
        self.m_norm = norm

    def add_sample(self, data):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param float data: the scalar sample.
        """

        self.m_first += np.sum(data.ravel())
        self.m_second += np.sum(data.ravel() ** 2)
        self.m_norm += data.size

    def mean(self):
        r"""
        Obtain the current mean.
        N.B. samples can be added afterwards without any problems.
        """

        if self.m_norm == 0:
            return np.NaN

        return self.m_first / self.m_norm

    def variance(self):
        r"""
        Obtain the current variance.
        N.B. samples can be added afterwards without any problems.
        """

        if self.m_norm <= 1:
            return np.NaN

        return (
            (self.m_second / self.m_norm - (self.m_first / self.m_norm) ** 2)
            * self.m_norm
            / (self.m_norm - 1)
        )

    def std(self):
        r"""
        Obtain the current standard deviation.
        N.B. samples can be added afterwards without any problems.
        """

        return np.sqrt(self.variance())

    def norm(self):
        r"""
        Return normalisation: the number of samples.

        :return: Scalar.
        """

        return self.m_norm

    def first(self):
        r"""
        Sum of the first statistical moment.

        :return: Scalar.
        """

        return self.m_first

    def second(self):
        r"""
        Sum of the second statistical moment.

        :return: Scalar.
        """

        return self.m_second


class StaticNd:
    r"""
    Allocate the ensemble average of an Nd-array (of same size for all samples).
    Add samples to it using :py:func:`StaticNd.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying ``first``, ``second``, ``norm``.

    :param bool compute_variance:
        If set ``False`` no second moment will be computed.
        The variance an standard deviation will not be available.

    :param list shape, optional:
        The shape of the data.
        If not specified it is determined form the first sample.

    :param type dtype, optional:
        The numpy-type of the data.
        If not specified it is determined form the first sample.

    :param np.array<T> first: Continued computation: Sum of the first moment.
    :param np.array<T> second: Continued computation: Sum of the second moment.
    :param np.array<np.int64> norm: Continued computation: Number of samples.
    """

    def __init__(
        self,
        compute_variance=True,
        shape=None,
        dtype=None,
        first=None,
        second=None,
        norm=None,
    ):

        warnings.warn("Deprecated. Use: enstat.static.", DeprecationWarning)

        self.m_compute_variance = compute_variance
        self.m_first = first
        self.m_second = second
        self.m_norm = norm
        self.m_shape = shape
        self.m_dtype = dtype

    def _allocate(self, data):

        if self.m_first is not None:
            assert data.shape == self.m_shape
            return

        self.m_shape = self.m_shape if self.m_shape is not None else data.shape
        self.m_dtype = self.m_dtype if self.m_dtype is not None else data.dtype

        self.m_norm = np.zeros(self.m_shape, np.int64)
        self.m_first = np.zeros(self.m_shape, self.m_dtype)

        if self.m_compute_variance:
            self.m_second = np.zeros(self.m_shape, self.m_dtype)

    def shape(self):
        r"""
        Return the data's shape.
        """
        return self.m_shape

    def size(self):
        r"""
        Return the data's size.
        """
        return np.prod(self.m_shape)

    def add_sample(self, data, mask=None):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param np.array<T> data: the sample.
        :param np.array<bool> mask: optional, mask entries.
        """

        self._allocate(data)

        # masked data
        if mask is not None:
            incl = np.logical_not(mask)
            self.m_norm[incl] += 1
            self.m_first[incl] += data[incl]
            if self.m_compute_variance:
                self.m_second[incl] += data[incl] ** 2
            return

        # unmasked data
        self.m_norm += 1
        self.m_first += data
        if self.m_compute_variance:
            self.m_second += data**2

    def mean(self):
        r"""
        Obtain the current mean.
        N.B. samples can be added afterwards without any problems.
        """

        if self.m_norm is None:
            return None

        n = np.where(self.m_norm > 0, self.m_norm, 1)
        ret = self.m_first / n
        return np.where(self.m_norm > 0, ret, np.NaN)

    def variance(self):
        r"""
        Obtain the current variance.
        N.B. samples can be added afterwards without any problems.
        """

        if self.m_norm is None:
            return None

        assert self.m_compute_variance
        n = np.where(self.m_norm > 1, self.m_norm, 2)
        ret = (self.m_second / n - (self.m_first / n) ** 2) * n / (n - 1)
        return np.where(self.m_norm > 1, ret, np.NaN)

    def std(self):
        r"""
        Obtain the current standard deviation.
        N.B. samples can be added afterwards without any problems.
        """

        if self.m_norm is None:
            return None

        return np.sqrt(self.variance())

    def norm(self):
        r"""
        Return normalisation: the number of samples.

        :return: Scalar.
        """

        return self.m_norm

    def first(self):
        r"""
        Sum of the first statistical moment.

        :return: Scalar.
        """

        return self.m_first

    def second(self):
        r"""
        Sum of the second statistical moment.

        :return: Scalar.
        """

        assert self.m_compute_variance
        return self.m_second


def _expand_array1d(data, size):

    tmp = np.zeros((size), data.dtype)
    tmp[: data.size] = data
    return tmp


class Dynamic1d(StaticNd):
    r"""
    Allocate the ensemble average of an 1d-array (which grows depending of the size of the samples).
    Add samples to it using :py:func:`Dynamic1d.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying ``first``, ``second``, ``norm``.

    :param bool compute_variance:
        If set ``False`` no second moment will be computed.
        The variance an standard deviation will not be available.

    :param list size, optional:
        The initial size of the data.

    :param type dtype, optional:
        The numpy-type of the data.
        If not specified it is determined form the first sample.

    :param np.array<T> first: Continued computation: Sum of the first moment.
    :param np.array<T> second: Continued computation: Sum of the second moment.
    :param np.array<np.int64> norm: Continued computation: Number of samples.
    """

    def __init__(
        self,
        compute_variance=True,
        size=None,
        dtype=None,
        first=None,
        second=None,
        norm=None,
    ):

        warnings.warn("Deprecated. Use: enstat.dynamic1d.", DeprecationWarning)

        self.m_compute_variance = compute_variance
        self.m_first = first
        self.m_second = second
        self.m_norm = norm
        self.m_size = size
        self.m_shape = [self.m_size]
        self.m_dtype = dtype

    def _allocate(self, data):
        r"""
        Allocate data if necessary.
        """

        if self.m_first is not None:
            return

        self.m_size = self.m_size if self.m_size is not None else data.size
        self.m_dtype = self.m_dtype if self.m_dtype is not None else data.dtype
        self.m_shape = [self.m_size]

        self.m_norm = np.zeros((self.m_size), np.int64)
        self.m_first = np.zeros((self.m_size), self.m_dtype)

        if self.m_compute_variance:
            self.m_second = np.zeros((self.m_size), self.m_dtype)

    def _expand(self, data):

        if data.size <= self.m_size:
            return

        self.m_size = data.size
        self.m_shape = [self.m_size]
        self.m_norm = _expand_array1d(self.m_norm, data.size)
        self.m_first = _expand_array1d(self.m_first, data.size)

        if self.m_compute_variance:
            self.m_second = _expand_array1d(self.m_second, data.size)

    def add_sample(self, data):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param np.array<T> data: the sample.
        """

        assert data.ndim == 1

        self._allocate(data)
        self._expand(data)

        self.m_norm[: data.size] += 1
        self.m_first[: data.size] += data

        if self.m_compute_variance:
            self.m_second[: data.size] += data**2


if __name__ == "__main__":
    pass
