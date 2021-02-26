# What is MYRaf?

The MYRaf is a practicable astronomical image reduction and photometry software and interfaces for IRAF. For this purpose, MYRaf uses IRAF, PyRAF, and many other python packages with a Qt framework. Also, MYRaf is free software and distributed with a GPLv3 license. You can use it without restrictive licenses, make copies for your friends, school, or institution.



# Installation

- Clone MYRaf v3.0.0 from git.
  
  ```bash
  $ sudo apt install git
  $ git clone https://github.com/myrafproject/myrafproject.git
  $ cd myrafproject
  ```

- Install IRAF and the required packages with the following series of commands.
  
  ```bash
  $ sudo apt install iraf
  $ sudo apt install python3-dev libx11-dev x11proto-dev libxcb-xinerama0
  $ pip install pyqt5 matplotlib ginga sep ccdproc regions astroalign pyraf mplcursors imexam  
  ```

- If you are using the **bash** terminal;
  
  ```bash
  $ export iraf=/usr/lib/iraf/
  $ export IRAFARCH=linux
  ```

- If you are using **fish** terminal;
  
  ```bash
  $ setenv iraf /usr/lib/iraf/
  $ setenv IRAFARCH linux
  ```

- Finally, run MYRaf v3,
  
  ```bash
  $ python3 main.py
  ```

If you have any problems during installation or usage, please contact us or create an [issue](https://github.com/myrafproject/myrafproject/issues/new). Before reporting an issue, please do not forget to run MYRaf v3 with DEBUG mode and share the outputs with us with the command below;

```bash
$ python3 main.py -ll 10
```

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
