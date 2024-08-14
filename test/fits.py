import math
import unittest
from random import choice, choices

from astropy import units
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE
from astropy.nddata import CCDData
from astropy.table import QTable
from scipy.ndimage import rotate
from sep import Background

from myraflib import Fits
import pandas as pd
import numpy as np

from astropy.io.fits.header import Header

from myraflib.error import NothingToDo, OverCorrection, NumberOfElementError, Unsolvable, OperatorError


class TestFits(unittest.TestCase):
    def setUp(self):
        Fits.high_precision = True
        self.SAMPLE = Fits.sample()

    def test_file(self):
        self.assertEquals(self.SAMPLE.file, self.SAMPLE.path.absolute().__str__())

    def test_from_data_header(self):
        new_fits = Fits.from_data_header(self.SAMPLE.data, self.SAMPLE.hdu[0].header)
        self.assertTrue(self.SAMPLE.is_same(new_fits))

    def test_from_data_header_not_equal(self):
        new_fits = Fits.from_data_header(self.SAMPLE.data * 2, self.SAMPLE.hdu[0].header)
        self.assertFalse(self.SAMPLE.is_same(new_fits))

    def test_from_path(self):
        new_fits = Fits.from_path(self.SAMPLE.path.absolute().__str__())
        self.assertTrue(self.SAMPLE.is_same(new_fits))

    def test_ccd(self):
        ccd = self.SAMPLE.ccd
        self.assertIsInstance(ccd, CCDData)

    def test_data(self):
        data = fits.getdata(self.SAMPLE.path.absolute())
        np.testing.assert_array_equal(self.SAMPLE.data, data)

    def test_value(self):
        for x in np.random.randint(0, 20, size=10):
            for y in np.random.randint(0, 20, size=10):
                self.assertEquals(self.SAMPLE.value(x, y), self.SAMPLE.data[x][y])

    def test_header(self):
        header = fits.getheader(self.SAMPLE.path.absolute())
        self.assertEquals(self.SAMPLE.hdu[0].header, header)

    def test_stats(self):
        stats = self.SAMPLE.stats
        self.assertAlmostEquals(stats["size"], self.SAMPLE.data.size)
        self.assertAlmostEquals(stats["width"], self.SAMPLE.data.shape[0])
        self.assertAlmostEquals(stats["height"], self.SAMPLE.data.shape[1])
        self.assertAlmostEquals(stats["min"], self.SAMPLE.data.min())
        self.assertAlmostEquals(stats["max"], self.SAMPLE.data.max())
        self.assertAlmostEquals(stats["mean"], self.SAMPLE.data.mean())
        self.assertAlmostEquals(stats["std"], np.std(self.SAMPLE.data))

    def test_background(self):
        self.assertIsInstance(self.SAMPLE.background(), Background)

    def test_cosmic_cleaner(self):
        data = self.SAMPLE.data.copy()

        self.SAMPLE.cosmic_cleaner()
        mask = data - self.SAMPLE.data
        self.assertNotEquals(mask.sum(), 0)

    def test_hedit_add_single(self):
        self.SAMPLE.hedit("MSH", "TEST", comments="Added for test")
        self.assertEquals(self.SAMPLE.header["MSH"], "TEST")

    def test_hedit_add_multiple(self):
        self.SAMPLE.hedit(
            ["MSH1", "MSH2"],
            ["TEST1", "TEST2"],
            comments=["Added for test", "Added for test"]
        )
        self.assertEquals(self.SAMPLE.header["MSH1"], "TEST1")
        self.assertEquals(self.SAMPLE.header["MSH2"], "TEST2")

    def test_hedit_add_multiple_not_equal(self):
        with self.assertRaises(NumberOfElementError):
            self.SAMPLE.hedit(
                ["MSH1", "MSH2"],
                ["TEST1"],
                comments=["Added for test", "Added for test"]
            )

    def test_hedit_update(self):
        self.SAMPLE.hedit("MSH", "TEST")
        self.SAMPLE.hedit("MSH", "TEST2")
        self.assertEquals(self.SAMPLE.header["MSH"], "TEST2")

    def test_hedit_update_multiple(self):
        self.SAMPLE.hedit("MSH1", "TEST1")
        self.SAMPLE.hedit("MSH2", "TEST2")
        self.SAMPLE.hedit(["MSH1", "MSH2"], ["NEW1", "NEW2"], "comment")
        self.assertEquals(self.SAMPLE.header["MSH1"], "NEW1")
        self.assertEquals(self.SAMPLE.header["MSH2"], "NEW2")

    def test_hedit_update_multiple_not_equal(self):
        self.SAMPLE.hedit("MSH1", "TEST1")
        self.SAMPLE.hedit("MSH2", "TEST2")
        with self.assertRaises(NumberOfElementError):
            self.SAMPLE.hedit(["MSH1", "MSH2"], ["NEW1"])

    def test_hedit_from_other(self):
        header = choice(list(self.SAMPLE.header.keys()))
        self.SAMPLE.hedit("MSH", header, value_is_key=True)
        self.assertEquals(self.SAMPLE.header["MSH"], self.SAMPLE.header[header])

    def test_hedit_from_other_multiple(self):
        k = 5
        headers = choices(list(self.SAMPLE.header.keys()), k=k)
        keys = [f"MSH{i}" for i in range(k)]
        self.SAMPLE.hedit(keys, headers, value_is_key=True)
        for key, other_key in zip(keys, headers):
            self.assertEquals(self.SAMPLE.header[key], self.SAMPLE.header[other_key])

    def test_hedit_from_other_multiple_not_equal(self):
        k = 5
        headers = choices(list(self.SAMPLE.header.keys()), k=k)
        keys = [f"MSH{i}" for i in range(k + 1)]
        with self.assertRaises(NumberOfElementError):
            self.SAMPLE.hedit(keys, headers, value_is_key=True)

    def test_hedit_delete(self):
        self.SAMPLE.hedit("MSH", "TEST")
        self.SAMPLE.hedit("MSH", delete=True)
        self.assertFalse("MSH" in self.SAMPLE.header.keys())

    def test_hedit_delete_multiple(self):
        self.SAMPLE.hedit(["MSH1", "MSH2"], ["NEW1", "NEW2"])
        self.SAMPLE.hedit(["MSH1", "MSH2"], delete=True)
        for each in ["MSH1", "MSH2"]:
            self.assertFalse(each in self.SAMPLE.header.keys())

    def test_hedit_no_value_and_no_delete(self):
        with self.assertRaises(NothingToDo):
            self.SAMPLE.hedit("MSH")

    def test_abs(self):
        new_fits = Fits.from_data_header(self.SAMPLE.data * -1, self.SAMPLE.hdu[0].header)
        new_fits.abs()
        self.assertTrue(new_fits.is_same(self.SAMPLE))

    def test_add(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.add(2)
        np.testing.assert_array_equal(self.SAMPLE.data, data + 2)

    def test_add_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.add(new_fits)
        np.testing.assert_array_equal(self.SAMPLE.data, data + new_fits.data)

    def test_sub(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.sub(2)
        np.testing.assert_array_equal(self.SAMPLE.data, data - 2)

    def test_sub_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.sub(new_fits)
        np.testing.assert_array_equal(self.SAMPLE.data, data - new_fits.data)

    def test_mul(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.mul(2)
        np.testing.assert_array_equal(self.SAMPLE.data, data * 2)

    def test_mul_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.mul(new_fits)
        np.testing.assert_array_equal(self.SAMPLE.data, data * new_fits.data)

    def test_div(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.div(2)
        np.testing.assert_array_equal(self.SAMPLE.data, (data / 2).astype(int))

    def test_div_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.div(new_fits)
        np.testing.assert_array_equal(self.SAMPLE.data, (data / new_fits.data).astype(int))

    def test_pow(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.pow(2)
        np.testing.assert_array_equal(self.SAMPLE.data, data ** 2)

    def test_pow_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.pow(new_fits)
        np.testing.assert_array_equal(self.SAMPLE.data, data ** new_fits.data)

    def test_mod(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.mod(2)
        np.testing.assert_array_equal(self.SAMPLE.data, data % 2)

    def test_mod_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.mod(new_fits)
        np.testing.assert_array_equal(self.SAMPLE.data, data % new_fits.data)

    def test_imarith_add(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.imarith(2, "+")
        np.testing.assert_array_equal(self.SAMPLE.data, data + 2)

    def test_imarith_add_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.imarith(new_fits, "+")
        np.testing.assert_array_equal(self.SAMPLE.data, data + new_fits.data)

    def test_imarith_sub(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.imarith(2, "-")
        np.testing.assert_array_equal(self.SAMPLE.data, data - 2)

    def test_imarith_sub_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.imarith(new_fits, "-")
        np.testing.assert_array_equal(self.SAMPLE.data, data - new_fits.data)

    def test_imarith_mul(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.imarith(2, "*")
        np.testing.assert_array_equal(self.SAMPLE.data, data * 2)

    def test_imarith_mul_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.imarith(new_fits, "*")
        np.testing.assert_array_equal(self.SAMPLE.data, data * new_fits.data)

    def test_imarith_div(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.imarith(2, "/")
        np.testing.assert_array_equal(self.SAMPLE.data, (data / 2).astype(int))

    def test_imarith_div_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.imarith(new_fits, "/")
        np.testing.assert_array_equal(self.SAMPLE.data, (data / new_fits.data).astype(int))

    def test_imarith_pow(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.imarith(2, "^")
        np.testing.assert_array_equal(self.SAMPLE.data, data ** 2)

    def test_imarith_pow_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.imarith(new_fits, "**")
        np.testing.assert_array_equal(self.SAMPLE.data, data ** new_fits.data)

    def test_imarith_mod(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.imarith(2, "%")
        np.testing.assert_array_equal(self.SAMPLE.data, data % 2)

    def test_imarith_mod_fits(self):
        data = self.SAMPLE.data.copy()
        new_fits = Fits.sample()
        self.SAMPLE.imarith(new_fits, "%")
        np.testing.assert_array_equal(self.SAMPLE.data, data % new_fits.data)

    def test_imarith_wrong_operator(self):
        with self.assertRaises(OperatorError):
            self.SAMPLE.imarith(2, "TEST")

    def test_extract(self):
        sources = self.SAMPLE.extract()
        self.assertIsInstance(sources, QTable)

    def test_daofind(self):
        sources = self.SAMPLE.daofind(1)
        self.assertIsInstance(sources, QTable)

    def test_shift(self):
        x, y = 22, 23
        data = self.SAMPLE.data.copy()
        self.SAMPLE.shift(10, 10)
        self.assertEquals(data[x][y], self.SAMPLE.data[x + 10][y + 10])

    def test_rotate(self):
        x, y = 22, 23
        data = self.SAMPLE.data.copy()
        self.SAMPLE.rotate(3.1415 / 2)
        self.assertNotEquals(data[x][y], self.SAMPLE.data[x][y])

    def test_crop(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.crop(10, 10, 10, 10)
        self.assertEquals((10, 10), self.SAMPLE.data.shape)
        self.assertNotEquals(data[9][9], self.SAMPLE.data[0][0])

    def test_bin(self):
        data = self.SAMPLE.data.copy()
        self.SAMPLE.bin(2)
        self.assertEquals((data.shape[0] // 2, data.shape[1] // 2), self.SAMPLE.data.shape)
