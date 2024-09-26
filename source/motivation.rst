.. _motivation:

Motivation
==================

``MYRaf`` is designed with the needs of the average coder in mind. To support ease of use, it introduces two key classes: ``Fits`` and ``FitsArray``. A ``Fits`` object is expected to perform a variety of operations, including both data and header manipulations on FITS files. The ``Fits`` class encapsulates all necessary data, along with the header and data operations required for astronomical analysis. To achieve this functionality, ``MYRaf`` integrates multiple Python libraries, such as :py:mod:`Astropy` [The_Astropy_Collaboration_2022]_, :py:mod:`Astroquery` [Astroquery]_, :py:mod:`AstroAlign` [beroiz2019]_, :py:mod:`ccdproc` [matt_craig2017]_, :py:mod:`numpy` [harris2020]_, :py:mod:`pandas` [mckinney2010]_, :py:mod:`photutils` [larry_bradley2024]_, :py:mod:`scipy` [2020SciPy-NMeth]_, :py:mod:`sep` [Barbary2016]_, :py:mod:`ginga` [Jeschke15A]_, and others, while shielding users from the complexity of directly interacting with these libraries.

.. [The_Astropy_Collaboration_2022] The Astropy Collaboration. (2022). *Astropy Documentation*. Retrieved from https://www.astropy.org
.. [Astroquery] Astroquery Development Team. (n.d.). *Astroquery Documentation*. Retrieved from https://astroquery.readthedocs.io
.. [beroiz2019] Beroiz, M., & Fitzgerald, M. (2019). *AstroAlign: Pythonic Astronomical Image Registration*. Retrieved from https://github.com/toros-astro/astroalign
.. [matt_craig2017] Craig, M., et al. (2017). *CCDProc: CCD Image Processing in Astronomy*. Retrieved from https://ccdproc.readthedocs.io
.. [harris2020] Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.
.. [mckinney2010] McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*, 51–56.
.. [larry_bradley2024] Bradley, L., et al. (2024). *Photutils: Photometry Tools*. Retrieved from https://photutils.readthedocs.io
.. [2020SciPy-NMeth] Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. *Nature Methods*, 17, 261–272.
.. [Barbary2016] Barbary, K. (2016). SEP: Source Extraction and Photometry. *Journal of Open Source Software*, 1(6), 58.
.. [Jeschke15A] Jeschke, E. (2015). *Ginga: An Astronomical Image Viewer and Toolkit*. Retrieved from https://ginga.readthedocs.io

