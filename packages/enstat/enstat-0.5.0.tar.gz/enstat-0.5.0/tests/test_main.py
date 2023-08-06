import unittest
from collections import defaultdict

import numpy as np

import enstat.mean


class Test_mean(unittest.TestCase):
    """
    tests
    """

    def test_scalar(self):
        """
        Basic test of "mean" and "std" using a random sample.
        """

        average = enstat.scalar()

        average.add_sample(np.array(1.0))

        self.assertFalse(np.isnan(average.mean()))
        self.assertTrue(np.isnan(average.std()))

        average.add_sample(np.array(1.0))

        self.assertFalse(np.isnan(average.mean()))
        self.assertFalse(np.isnan(average.std()))

    def test_scalar_division(self):
        """
        Check for zero division.
        """

        average = enstat.scalar()

        a = np.random.random(50 * 20).reshape(50, 20)

        for i in range(a.shape[0]):
            average.add_sample(a[i, :])

        self.assertTrue(np.isclose(average.mean(), np.mean(a)))
        self.assertTrue(np.isclose(average.std(), np.std(a), rtol=1e-3))

    def test_static(self):
        """
        Basic test of "mean" and "std" using a random sample.
        """

        average = enstat.static()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)

        for i in range(a.shape[0]):
            average.add_sample(a[i, :, :])

        self.assertTrue(np.allclose(average.mean(), np.mean(a, axis=0)))
        self.assertTrue(np.allclose(average.std(), np.std(a, axis=0), rtol=5e-1, atol=1e-3))
        self.assertTrue(average.shape == a.shape[1:])
        self.assertTrue(average.size == np.prod(a.shape[1:]))

    def test_static_ravel(self):
        """
        Like :py:func:`test_static` but with a test of `ravel`.
        """

        arraylike = enstat.static()
        scalar = enstat.scalar()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)

        for i in range(a.shape[0]):
            arraylike.add_sample(a[i, :, :])
            scalar.add_sample(a[i, :, :])

        flat = arraylike.ravel()

        self.assertTrue(np.allclose(flat.mean(), np.mean(a)))
        self.assertTrue(np.allclose(flat.std(), np.std(a), rtol=5e-1, atol=1e-3))
        self.assertTrue(np.allclose(flat.mean(), scalar.mean()))
        self.assertTrue(np.allclose(flat.std(), scalar.std(), rtol=5e-1, atol=1e-3))

    def test_static_division(self):
        """
        Check for zero division.
        """

        average = enstat.static()

        average.add_sample(np.array([1.0]))

        self.assertFalse(np.isnan(average.mean()))
        self.assertTrue(np.isnan(average.std()))

        average.add_sample(np.array([1.0]))

        self.assertFalse(np.isnan(average.mean()))
        self.assertFalse(np.isnan(average.std()))

    def test_static_mask(self):
        """
        Mask part of the data.
        """

        average = enstat.static()

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)
        m = np.random.random(35 * 50 * 20).reshape(35, 50, 20) > 0.8

        for i in range(a.shape[0]):
            average.add_sample(a[i, :, :], m[i, :, :])

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(np.all(np.equal(average.norm, np.sum(np.logical_not(m), axis=0))))

    def test_static_add_point(self):
        """
        Add data point-by-point.
        """

        a = np.random.random(35 * 50).reshape(35, 50)
        m = np.random.random(35 * 50).reshape(35, 50) > 0.8
        average = enstat.static(shape=a.shape[1])

        for i in range(a.shape[0]):
            for j in np.argwhere(~m[i, :]).ravel():
                average.add_point(a[i, j], j)

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(
            np.isclose(
                np.sum(average.first) / np.sum(average.norm),
                np.mean(a[np.logical_not(m)]),
            )
        )

        self.assertTrue(np.all(np.equal(average.norm, np.sum(np.logical_not(m), axis=0))))

    def test_dynamic1d(self):
        """
        Dynamically grow shape.
        """

        average = enstat.dynamic1d()

        average.add_sample(np.array([1, 2, 3]))
        average.add_sample(np.array([1, 2, 3]))
        average.add_sample(np.array([1, 2]))
        average.add_sample(np.array([1]))
        average.add_sample(np.array([1, 2, 3, 4]))
        average.add_sample(np.array([1, 2, 3, 4]))

        self.assertTrue(np.allclose(average.mean(), np.array([1, 2, 3, 4])))
        self.assertTrue(np.allclose(average.std(), np.array([0, 0, 0, 0])))
        self.assertEqual(average.shape, (4,))
        self.assertEqual(average.size, 4)


class Test_defaultdict(unittest.TestCase):
    """
    functionality
    """

    def test_scalar(self):

        average = defaultdict(enstat.scalar)

        a = np.random.random(50 * 20).reshape(50, 20)
        b = np.random.random(52 * 21).reshape(52, 21)

        for i in range(a.shape[0]):
            average["a"].add_sample(a[i, :])

        for i in range(b.shape[0]):
            average["b"].add_sample(b[i, :])

        self.assertTrue(np.isclose(average["a"].mean(), np.mean(a)))
        self.assertTrue(np.isclose(average["b"].mean(), np.mean(b)))

    def test_static(self):

        average = defaultdict(enstat.static)

        a = np.random.random(35 * 50 * 20).reshape(35, 50, 20)
        b = np.random.random(37 * 52 * 21).reshape(37, 52, 21)

        for i in range(a.shape[0]):
            average["a"].add_sample(a[i, :, :])

        for i in range(b.shape[0]):
            average["b"].add_sample(b[i, :, :])

        self.assertTrue(np.allclose(average["a"].mean(), np.mean(a, axis=0)))
        self.assertTrue(np.allclose(average["b"].mean(), np.mean(b, axis=0)))
        self.assertTrue(average["a"].shape == a.shape[1:])
        self.assertTrue(average["b"].shape == b.shape[1:])


if __name__ == "__main__":

    unittest.main()
