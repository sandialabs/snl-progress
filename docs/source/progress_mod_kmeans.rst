Progress K-Means Module
=======================

mod_kmeans.py
~~~~~~~~~~~~~

``mod_kmeans.py`` provides functionality for **k-means clustering** of solar generation
data. It contains the ``KMeans_Pipeline`` class, which:

- Preprocesses the solar and clear-sky irradiance data.
- Allows evaluation of different cluster sizes using metrics like SSE and silhouette scores.
- Performs cluster probability calculations to facilitate random day selection in the MCS.

.. automodule:: progress.mod_kmeans
   :members:
   :undoc-members:
   :show-inheritance:
