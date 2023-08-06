enstat
======

*enstat* allows you to compute the average (and variance) of chunked data,
without the need to load all data at once.
This done by keeping in memory the sum of the first (and second) statistical moment,
as well as the normalisation.
A common practical application is computing the average of an ensemble of realisations.

A simple example:
Suppose that we have 100 realisations each with 1000 blocks, and we want to know the ensemble
average of each block:

.. code-block:: python

   import enstat

   ensemble = enstat.static()

   for realisation in range(100):

      sample = np.random.random(1000)
      ensemble.add_sample(sample)

   mean = ensemble.mean()
   print(mean.shape)

which outputs ``[1000]``.

Note that *enstat* is very much aimed as user friendliness, as it keeps track of shapes
by itself, without the need to pre-specify.

.. toctree::
   :caption: API
   :maxdepth: 1

   module.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
