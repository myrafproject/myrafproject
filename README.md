![myraf](https://github.com/myrafproject/myrafproject/actions/workflows/python-package.yml/badge.svg)
![myraf](https://img.shields.io/badge/coverage-77%25-31c553)
![myraf](https://img.shields.io/badge/Win-%E2%9C%93-f5f5f5?logo=windows11)
![myraf](https://img.shields.io/badge/Ubuntu-%E2%9C%93-e95420?logo=Ubuntu)
![myraf](https://img.shields.io/badge/MacOS-%E2%9C%93-dadada?logo=macos)
![myraf](https://img.shields.io/badge/Python-%2039,%20310,%20311-3776ab?logo=python)
![myraf](https://img.shields.io/badge/LIC-GNU/GPL%20V3-a32d2a?logo=GNU)

# What is MYRaf?

The MYRaf WAS a practicable astronomical image reduction and photometry software and interfaces for IRAF.

Nowadays MYRaf uses astropy and other python's libraries to achieve its purpose. For this, MYRaf uses IRAF, PyRAF, and
many other python packages with a Qt framework. Also, MYRaf is free software and distributed with a GPLv3 license. You
can use it without restrictive licenses, make copies for your friends, school, or institution.

MYRaf is no longer Operating System depended and can be installed on all Operating Systems.

## Installation

```bash
pip install myraf
  ```

If you have any problems during installation or usage, please contact us or create
an [issue](https://github.com/myrafproject/myrafproject/issues/new). Before reporting an issue, please do not forget to
run MYRaf v3 with DEBUG mode and share the outputs with us with the command below;

Clear skies!

GNOME users might get an error. See: https://stackoverflow.com/a/71402854/2681662
OpenSuse users might get `ImportError: libgthread-2.0.so.0: cannot open shared object file: No such file or directory`. 
```bash
sudo zypper install glib2 glib2-devel python311-devel # If you're using python3.11
```
______

**MYRaf Project Team**

**Yücel KILIÇ** | mailto:ykilic@iaa.es

**Mohammad SHEMUNI** | mailto:niaei@pardus.org.tr

For academic use, please cite the paper:

> Shameoni Niaei, M.; Kilic, Y.; Özeren, F. F.,
> 2015, *MYRaf: An Easy Aperture Photometry GUI for IRAF*, **Astronomical Society of the Pacific (Conference Series)**,
> 496, 299 (2015).

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

- Fits object
    - [Creation](example/fits/create.ipynb)
    - [Visualization](example/fits/visualize.ipynb)
    - [Header](example/fits/header.ipynb)
    - [Data](example/fits/data.ipynb)
    - [Transformation](example/fits/transformation.ipynb)
    - [Arithmetic](example/fits/arithmetic.ipynb)
    - [Calibration](example/fits/calibration.ipynb)
    - [Source Extraction](example/fits/source_extraction.ipynb)
    - [Photometry](example/fits/photometry.ipynb)
    - [Map To Sky](example/fits/map_to_sky.ipynb)
    - [Other](example/fits/other.ipynb)
- FitsArray object
    - [Creation](example/fits_array/create.ipynb)
    - [Video](example/fits_array/video.ipynb)
    - [Visualization](example/fits_array/visualize.ipynb)
    - [Header](example/fits_array/header.ipynb)
    - [Data](example/fits_array/data.ipynb)
    - [Transformation](example/fits_array/transformation.ipynb)
    - [Arithmetic](example/fits_array/arithmetic.ipynb)
    - [Combine](example/fits_array/combine.ipynb)
    - [Calibration](example/fits_array/calibration.ipynb)
    - [Source Extraction](example/fits_array/source_extraction.ipynb)
    - [Photometry](example/fits_array/photometry.ipynb)
    - [Other](example/fits_array/other.ipynb)
- [Command Line Tools](example/command_line/im.md)

## MYRaf Telegram

You need some simple coordinate calculation or even visibility chart?
Check [@myrafproject_bot](https://t.me/myrafproject_bot). 
