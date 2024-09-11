# What is MYRaf?

The MYRaf WAS a practicable astronomical image reduction and photometry software and interfaces for IRAF.

Nowadays MYRaf uses astropy and other python's libraries to achieve its purpose. For this, MYRaf uses IRAF, PyRAF, and many other python packages with a Qt framework. Also, MYRaf is free software and distributed with a GPLv3 license. You can use it without restrictive licenses, make copies for your friends, school, or institution.

MYRaf is no longer Operating System depended and can be installed on all Operating Systems.

## Installation

```bash
pip install myraf
  ```

If you have any problems during installation or usage, please contact us or create an [issue](https://github.com/myrafproject/myrafproject/issues/new). Before reporting an issue, please do not forget to run MYRaf v3 with DEBUG mode and share the outputs with us with the command below;

Clear skies!

______

**MYRaf Project Team**

**Yücel KILIÇ** | yucelkilic@myrafproject.org

**Mohammad SHEMUNI** | m.shemuni@myrafproject.org

For academic use, please cite the paper:

> Shameoni Niaei, M.; Kilic, Y.; Özeren, F. F.,
> 2015, *MYRaf: An Easy Aperture Photometry GUI for IRAF*, **Astronomical Society of the Pacific (Conference Series)**, 496, 299 (2015).

[Bibtex@ADS](https://ui.adsabs.harvard.edu/abs/2015ASPC..496..299N/exportcitation) | [ASP](http://articles.adsabs.harvard.edu/pdf/2015ASPC..496..299N)

------------

> Kilic, Y.; Shameoni Niaei, M.; Özeren, F. F.; Yesilyaprak, C.,
> 2016,
> *MYRaf: A new Approach with IRAF for Astronomical Photometric Reduction*,
> **RevMexAA (Serie de Conferencias)**, 48, 38–39 (2016).

[Bibtex@ADS](http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode=2016RMxAC..48...38K&data_type=BIBTEX&db_key=AST&nocookieset=1) | [RevMexAA](http://www.astroscu.unam.mx/rmaa/RMxAC..48/PDF/RMxAC..48_part-2.2.pdf)

## MYRaf as a library
MYRaf has two base objects. `Fits` and `FitsArray`.
Both has almost the same features. Let's explore:

see: [myraf as a library](myraf_fits.md)