import math
import unittest
from unittest import skip

from astropy import units
from astropy.coordinates import SkyCoord
from astropy.nddata import CCDData
from scipy.ndimage import rotate
from sep import Background

from myraflib import Fits
import pandas as pd
import numpy as np

from astropy.io.fits.header import Header

from myraflib.error import NothingToDo, OverCorrection, NumberOfElementError, Unsolvable


class TestFits(unittest.TestCase):
    def setUp(self):
        Fits.high_precision = True
        self.SAMPLE = Fits.sample()

    def test___str__(self):
        string = str(self.SAMPLE)

        self.assertTrue(string.endswith("')"))
        self.assertTrue(string.startswith(f"{self.SAMPLE.__class__.__name__}"))

    def test___repr__(self):
        string = repr(self.SAMPLE)

        self.assertTrue(string.endswith("')"))
        self.assertTrue(string.startswith(f"{self.SAMPLE.__class__.__name__}"))

    def test___add__(self):
        new_fits = self.SAMPLE + self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test___add___numeric_int(self):
        new_fits = self.SAMPLE + 2
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() + 2)

    def test___add___numeric_float(self):
        new_fits = self.SAMPLE + 2.5
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() + 2.5)

    def test___add___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE + "2"

    def test___radd__(self):
        new_fits = self.SAMPLE + self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test___radd___numeric_int(self):
        new_fits = 2 + self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() + 2)

    def test___radd___numeric_float(self):
        new_fits = 2.5 + self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() + 2.5)

    def test___radd___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" + self.SAMPLE

    def test___sub__(self):
        new_fits = self.SAMPLE - self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 0)

    def test___sub___numeric_int(self):
        new_fits = self.SAMPLE - 2
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() - 2)

    def test___sub___numeric_float(self):
        new_fits = self.SAMPLE - 2.5
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() - 2.5)

    def test___sub___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE - "2"

    def test___rsub__(self):
        new_fits = self.SAMPLE - self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 0)

    def test___rsub___numeric_int(self):
        new_fits = 2 - self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), 2 - self.SAMPLE.data())

    def test___rsub___numeric_float(self):
        new_fits = 2.5 - self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(),
                                      2.5 - self.SAMPLE.data())

    def test___rsub___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" - self.SAMPLE

    def test___mul__(self):
        new_fits = self.SAMPLE * self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test___mul___numeric_int(self):
        new_fits = self.SAMPLE * 2
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test___mul___numeric_float(self):
        new_fits = self.SAMPLE * 2.5
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() * 2.5)

    def test___mul___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE * "2"

    def test___rmul__(self):
        new_fits = self.SAMPLE * self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test___rmul___numeric_int(self):
        new_fits = 2 * self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), 2 * self.SAMPLE.data())

    def test___rmul___numeric_float(self):
        new_fits = 2.5 * self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(),
                                      2.5 * self.SAMPLE.data())

    def test___rmul___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" * self.SAMPLE

    def test___div__(self):
        new_fits = self.SAMPLE / self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / self.SAMPLE.data())

    def test___div___numeric_int(self):
        new_fits = self.SAMPLE / 2
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() / 2)

    def test___div___numeric_float(self):
        new_fits = self.SAMPLE / 2.5
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / 2.5)

    def test___div___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE / "2"

    def test___rdiv__(self):
        new_fits = self.SAMPLE / self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / self.SAMPLE.data())

    def test___rdiv___numeric_int(self):
        new_fits = 2 / self.SAMPLE
        np.testing.assert_array_equal(new_fits.data(), 2 / self.SAMPLE.data())

    def test___rdiv___numeric_float(self):
        new_fits = 2.5 / self.SAMPLE
        np.testing.assert_array_equal(new_fits.data().round(6),
                                      (2.5 / self.SAMPLE.data()).round(6))

    def test___rdiv___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" / self.SAMPLE

    def test_file_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            _ = Fits.from_path("TEST")

    def test_header(self):
        headers = self.SAMPLE.header()
        self.assertIsInstance(headers, pd.DataFrame)

        for each in [
            "SIMPLE", "BITPIX", "NAXIS",
            "NAXIS1", "NAXIS2"
        ]:
            self.assertIn(each, headers.columns)

    def test_data(self):
        data = self.SAMPLE.data()
        self.assertIsInstance(data, np.ndarray)

    def test_value(self):
        data = self.SAMPLE.value(20, 20)
        self.assertIsInstance(data, float)
        self.assertEqual(data, self.SAMPLE.data()[20][20])

    def test_value_out_of_boundaries(self):
        with self.assertRaises(IndexError):
            _ = self.SAMPLE.value(65535, 65535)

    def test_pure_header(self):
        pure_header = self.SAMPLE.pure_header()
        self.assertIsInstance(pure_header, Header)

        for each in [
            "SIMPLE", "BITPIX", "NAXIS",
            "NAXIS1", "NAXIS2"
        ]:
            self.assertIn(each, pure_header)

    def test_ccd(self):
        ccd = self.SAMPLE.ccd()
        self.assertIsInstance(ccd, CCDData)
        np.testing.assert_array_equal(ccd.data, self.SAMPLE.data())

    def test_imstat(self):
        imstat = self.SAMPLE.imstat()
        self.assertIsInstance(imstat, pd.DataFrame)

        for each in ["npix", "mean", "stddev", "min", "max"]:
            self.assertIn(each, imstat.columns)

    def test_cosmic_clean(self):
        cleaned = self.SAMPLE.cosmic_clean()
        self.assertIsInstance(cleaned, Fits)

    def test_hedit(self):
        self.SAMPLE.hedit("MSH", "TEST")
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)
        self.assertEqual(header["MSH"].values, ["TEST"])

    def test_hedit_integer(self):
        self.SAMPLE.hedit("MSH", 44)
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)
        self.assertEqual(header["MSH"].values, 44)

    def test_hedit_float(self):
        self.SAMPLE.hedit("MSH", 4.4)
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)
        self.assertEqual(header["MSH"].values, 4.4)

    def test_hedit_bool(self):
        self.SAMPLE.hedit("MSH", True)
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)
        self.assertTrue(header["MSH"].values)

    def test_hedit_list(self):
        self.SAMPLE.hedit(["MSH1", "MSH2"], ["TEST1", "TEST2"])
        header = self.SAMPLE.header()

        for each in ["MSH1", "MSH2"]:
            self.assertIn(each, header.columns)

        for key, value in zip(["MSH1", "MSH2"], ["TEST1", "TEST2"]):
            self.assertEqual(header[key].values, [value])

    def test_hedit_list_different(self):
        self.SAMPLE.hedit(["MSH1", "MSH2", "MSH3", "MSH4"], ["TEST1", 44, 4.4, True])
        header = self.SAMPLE.header()

        for each in ["MSH1", "MSH2", "MSH3", "MSH4"]:
            self.assertIn(each, header.columns)

        for key, value in zip(["MSH1", "MSH2", "MSH3", "MSH4"], ["TEST1", 44, 4.4, True]):
            self.assertEqual(header[key].values, [value])

    def test_hedit_no_value(self):
        with self.assertRaises(NothingToDo):
            self.SAMPLE.hedit("MSH")

    def test_hedit_no_value_list(self):
        with self.assertRaises(NothingToDo):
            self.SAMPLE.hedit(["MSH1", "MSH2"])

    def test_hedit_value_key_different(self):
        with self.assertRaises(ValueError):
            self.SAMPLE.hedit(["MSH1", "MSH2"], "TEST")

    def test_hedit_key_value_different(self):
        with self.assertRaises(ValueError):
            self.SAMPLE.hedit("MSH", ["TEST1", "TEST2"])

    def test_hedit_key_value_different_length(self):
        with self.assertRaises(ValueError):
            self.SAMPLE.hedit(
                ["MSH1", "MSH2", "MSH3"],
                ["TEST1", "TEST2"]
            )

    def test_hedit_value_key_different_length(self):
        with self.assertRaises(ValueError):
            self.SAMPLE.hedit(
                ["MSH1", "MSH2"],
                ["TEST1", "TEST2", "TEST3"]
            )

    def test_hedit_delete(self):
        self.SAMPLE.hedit("MSH", "TEST")
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)
        self.assertEqual(header["MSH"].values, ["TEST"])

        self.SAMPLE.hedit("MSH", delete=True)
        new_header = self.SAMPLE.header()
        self.assertNotIn("MSH", new_header.columns)
        self.assertEqual(header["MSH"].values, ["TEST"])

    def test_save_as(self):
        new_file = self.SAMPLE.save_as("TEST.fits")
        self.assertIsInstance(new_file, Fits)
        new_file.file.unlink()

    def test_save_as_already_exist(self):
        new_file = self.SAMPLE.save_as("TEST.fits")
        self.assertIsInstance(new_file, Fits)
        with self.assertRaises(FileExistsError):
            _ = self.SAMPLE.save_as("TEST.fits")
        new_file.file.unlink()

    def test_add(self):
        new_fits = self.SAMPLE.add(self.SAMPLE)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test_add_numeric_int(self):
        new_fits = self.SAMPLE.add(2)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() + 2)

    def test_add_numeric_float(self):
        new_fits = self.SAMPLE.add(2.5)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() + 2.5)

    def test_add_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.add("2")

    def test_sub(self):
        new_fits = self.SAMPLE.sub(self.SAMPLE)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 0)

    def test_sub_numeric_int(self):
        new_fits = self.SAMPLE.sub(2)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() - 2)

    def test_sub_numeric_float(self):
        new_fits = self.SAMPLE.sub(2.5)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() - 2.5)

    def test_sub_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.sub("2")

    def test_mul(self):
        new_fits = self.SAMPLE.mul(self.SAMPLE)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test_mul_numeric_int(self):
        new_fits = self.SAMPLE.mul(2)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test_mul_numeric_float(self):
        new_fits = self.SAMPLE.mul(2.5)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() * 2.5)

    def test_mul_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.mul("2")

    def test_div(self):
        new_fits = self.SAMPLE.div(self.SAMPLE)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / self.SAMPLE.data())

    def test_div_numeric_int(self):
        new_fits = self.SAMPLE.div(2)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() / 2)

    def test_div_numeric_float(self):
        new_fits = self.SAMPLE.div(2.5)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / 2.5)

    def test_pow(self):
        new_fits = self.SAMPLE.pow(self.SAMPLE)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() ** self.SAMPLE.data())

    def test_pow_numeric_int(self):
        new_fits = self.SAMPLE.pow(2)
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test_pow_numeric_float(self):
        new_fits = self.SAMPLE.pow(2.5)
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() ** 2.5)

    def test_imarith_add(self):
        new_fits = self.SAMPLE.imarith(self.SAMPLE, "+")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test_imarith_add_numeric_int(self):
        new_fits = self.SAMPLE.imarith(2, "+")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() + 2)

    def test_imarith_add_numeric_float(self):
        new_fits = self.SAMPLE.imarith(2.5, "+")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() + 2.5)

    def test_imarith_sub(self):
        new_fits = self.SAMPLE.imarith(self.SAMPLE, "-")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 0)

    def test_imarith_sub_numeric_int(self):
        new_fits = self.SAMPLE.imarith(2, "-")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() - 2)

    def test_imarith_sub_numeric_float(self):
        new_fits = self.SAMPLE.imarith(2.5, "-")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() - 2.5)

    def test_imarith_mul(self):
        new_fits = self.SAMPLE.imarith(self.SAMPLE, "*")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test_imarith_mul_numeric_int(self):
        new_fits = self.SAMPLE.imarith(2, "*")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() * 2)

    def test_imarith_mul_numeric_float(self):
        new_fits = self.SAMPLE.imarith(2.5, "*")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() * 2.5)

    def test_imarith_div(self):
        new_fits = self.SAMPLE.imarith(self.SAMPLE, "/")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / self.SAMPLE.data())

    def test_imarith_div_numeric_int(self):
        new_fits = self.SAMPLE.imarith(2, "/")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() / 2)

    def test_imarith_div_numeric_float(self):
        new_fits = self.SAMPLE.imarith(2.5, "/")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() / 2.5)

    def test_imarith_pow(self):
        new_fits = self.SAMPLE.imarith(self.SAMPLE, "**")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() ** self.SAMPLE.data())

    def test_imarith_pow_numeric_int(self):
        new_fits = self.SAMPLE.imarith(2, "**")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test_imarith_pow_numeric_float(self):
        new_fits = self.SAMPLE.imarith(2.5, "**")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() ** 2.5)

    def test_imarith_pow2(self):
        new_fits = self.SAMPLE.imarith(self.SAMPLE, "^")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() ** self.SAMPLE.data())

    def test_imarith_pow_numeric_int2(self):
        new_fits = self.SAMPLE.imarith(2, "^")
        np.testing.assert_array_equal(new_fits.data(), self.SAMPLE.data() ** 2)

    def test_imarith_pow_numeric_float2(self):
        new_fits = self.SAMPLE.imarith(2.5, "^")
        np.testing.assert_array_equal(new_fits.data(),
                                      self.SAMPLE.data() ** 2.5)

    def test_imarith_bad_operand(self):
        with self.assertRaises(ValueError):
            self.SAMPLE.imarith(self.SAMPLE, "?")

    def test_shift(self):
        shifted = self.SAMPLE.shift(20, 10)
        self.assertEqual(
            self.SAMPLE.data()[123, 123],
            shifted.data()[133, 143],
        )

    def test_rotate(self):
        rotated = self.SAMPLE.rotate(math.pi)
        rotated_data = rotate(self.SAMPLE.data(), 180, reshape=False)

        np.testing.assert_array_equal(
            rotated.data(), rotated_data
        )

    def test_crop(self):
        cropped = self.SAMPLE.crop(20, 12, 220, 200)

        cropped_data = self.SAMPLE.data()[12:212, 20:240]
        np.testing.assert_array_equal(
            cropped.data(), cropped_data
        )

    def test_crop_out_of_boundaries(self):
        with self.assertRaises(IndexError):
            _ = self.SAMPLE.crop(1000, 1000, 10, 10)

    def test_align(self):
        shifted = self.SAMPLE.shift(10, 10)
        aligned = self.SAMPLE.align(shifted)
        self.assertIsInstance(aligned, Fits)

    def test_zero_correction(self):
        zero_corrected = self.SAMPLE.zero_correction(self.SAMPLE)
        self.assertIn("MY-ZERO", zero_corrected.header().columns)
        self.assertTrue(np.all(zero_corrected.data() == 0))

    def test_zero_correction_over_correction(self):
        zero_corrected = self.SAMPLE.zero_correction(self.SAMPLE)
        with self.assertRaises(OverCorrection):
            _ = zero_corrected.zero_correction(self.SAMPLE)

    def test_zero_correction_over_correction_force(self):
        zero_corrected = self.SAMPLE.zero_correction(self.SAMPLE)
        double_zero_corrected = zero_corrected.zero_correction(
            self.SAMPLE, force=True
        )
        np.testing.assert_array_equal(
            double_zero_corrected.data(), self.SAMPLE.mul(-1).data()
        )

    def test_dark_correction(self):
        dark_corrected = self.SAMPLE.dark_correction(self.SAMPLE)
        self.assertIn("MY-DARK", dark_corrected.header().columns)
        self.assertTrue(np.all(dark_corrected.data() == 0))

    def test_dark_correction_over_correction(self):
        dark_corrected = self.SAMPLE.dark_correction(self.SAMPLE)
        with self.assertRaises(OverCorrection):
            _ = dark_corrected.dark_correction(self.SAMPLE)

    def test_dark_correction_over_correction_force(self):
        dark_corrected = self.SAMPLE.dark_correction(self.SAMPLE)
        double_dark_corrected = dark_corrected.zero_correction(
            self.SAMPLE, force=True
        )
        np.testing.assert_array_equal(
            double_dark_corrected.data(), self.SAMPLE.mul(-1).data()
        )

    def test_flat_correction(self):
        flat_corrected = self.SAMPLE.flat_correction(self.SAMPLE)
        self.assertIn("MY-FLAT", flat_corrected.header().columns)
        flat_corrected_numpy = self.SAMPLE.data() / self.SAMPLE.data()
        division = np.round(flat_corrected.data() / flat_corrected_numpy, 5)
        self.assertTrue(np.all(division == division[0]))

    def test_flat_correction_over_correction(self):
        flat_corrected = self.SAMPLE.flat_correction(self.SAMPLE)
        with self.assertRaises(OverCorrection):
            _ = flat_corrected.flat_correction(self.SAMPLE)

    def test_flat_correction_over_correction_force(self):
        flat_corrected = self.SAMPLE.flat_correction(self.SAMPLE)
        double_flat_corrected = flat_corrected.flat_correction(
            self.SAMPLE, force=True
        )

        flat_corrected_numpy = self.SAMPLE.data() / self.SAMPLE.data() / self.SAMPLE.data()
        division = np.round(
            double_flat_corrected.data() / flat_corrected_numpy, 5)
        self.assertTrue(np.all(division == division[0]))

    def test_background(self):
        background = self.SAMPLE.background()
        self.assertIsInstance(background, Background)

    def test_daofind(self):
        sources = self.SAMPLE.daofind()
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["id", "xcentroid", "ycentroid", "sharpness", "roundness1",
                     "roundness2", "npix", "sky", "peak", "flux", "mag"]:
            self.assertIn(each, sources)

    def test_extract(self):
        sources = self.SAMPLE.extract()
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["xcentroid", "ycentroid"]:
            self.assertIn(each, sources)

    def test_phot_sep(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
        )
        self.assertIsInstance(ph, pd.DataFrame)

    def test_phot_sep_exposure(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure="EXPOSURE"
        )
        self.assertIsInstance(ph, pd.DataFrame)

    def test_phot_sep_exposure_does_not_exist(self):
        sources = self.SAMPLE.extract()
        with self.assertRaises(KeyError):
            _ = self.SAMPLE.photometry_sep(
                sources["xcentroid"], sources["ycentroid"], 10,
                exposure="DOESNOTEXIST"
            )

    def test_phot_sep_exposure_numeric(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure=22
        )
        self.assertIsInstance(ph, pd.DataFrame)

    def test_phot_sep_exposure_numeric_same_as_header(self):
        sources = self.SAMPLE.extract()
        ph_exptime = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure="EXPOSURE"
        )
        ph_65 = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure=65
        )
        pd.testing.assert_frame_equal(ph_exptime, ph_65)

    def test_phot_sep_exposure_same_as_zero(self):
        sources = self.SAMPLE.extract()
        ph_exptime = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
        )
        ph_0 = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure=0
        )
        pd.testing.assert_frame_equal(ph_exptime, ph_0)

    def test_phot_sep_coordinates_same_as_numeric(self):
        ph_list = self.SAMPLE.photometry_sep(
            [1], [2], 10,
        )
        ph_numeric = self.SAMPLE.photometry_sep(
            1, 2, 10,
        )
        pd.testing.assert_frame_equal(ph_list, ph_numeric)

    def test_phot_sep_coordinates_same_as_numeric_mixed(self):
        ph_list = self.SAMPLE.photometry_sep(
            [1], 2, 10,
        )
        ph_numeric = self.SAMPLE.photometry_sep(
            1, [2], 10,
        )
        pd.testing.assert_frame_equal(ph_list, ph_numeric)

    def test_phot_sep_coordinates_not_equal(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.photometry_sep(
                [1, 2], [2], 10,
            )

    def test_phot_sep_coordinates_not_equal_numeric(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.photometry_sep(
                [1, 2], 1, 10,
            )

    def test_phot_sep_header(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers=["NAXIS1", "NAXIS2"]
        )
        self.assertIsInstance(ph, pd.DataFrame)
        for each in ["NAXIS1", "NAXIS2"]:
            self.assertIn(each, ph.columns)

    def test_phot_sep_single(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers="NAXIS1"
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertIn("NAXIS1", ph.columns)

    def test_phot_sep_does_not_exits(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers=["DOESNOTEXIST1", "DOESNOTEXIST2"]
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST1"]))
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST2"]))

    def test_phot_sep_does_not_exits_single(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers="DOESNOTEXIST"
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST"]))

    def test_phot_sep_one_does_not_exits(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers=["NAXIS", "DOESNOTEXIST1"]
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST1"]))
        self.assertTrue(all(each is not None for each in ph["NAXIS"]))

    def test_phot_phu(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
        )
        self.assertIsInstance(ph, pd.DataFrame)

    def test_phot_phu_exposure(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure="EXPOSURE"
        )
        self.assertIsInstance(ph, pd.DataFrame)

    def test_phot_phu_exposure_does_not_exist(self):
        sources = self.SAMPLE.extract()
        with self.assertRaises(KeyError):
            _ = self.SAMPLE.photometry_phu(
                sources["xcentroid"], sources["ycentroid"], 10,
                exposure="DOESNOTEXIST"
            )

    def test_phot_phu_exposure_numeric(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure=22
        )
        self.assertIsInstance(ph, pd.DataFrame)

    def test_phot_phu_exposure_numeric_same_as_header(self):
        sources = self.SAMPLE.extract()
        ph_exptime = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure="EXPOSURE"
        )
        ph_65 = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure=65
        )
        pd.testing.assert_frame_equal(ph_exptime, ph_65)

    def test_phot_phu_exposure_same_as_zero(self):
        sources = self.SAMPLE.extract()
        ph_exptime = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
        )
        ph_0 = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure=0
        )
        pd.testing.assert_frame_equal(ph_exptime, ph_0)

    def test_phot_phu_coordinates_same_as_numeric(self):
        ph_list = self.SAMPLE.photometry_phu(
            [1], [2], 10,
        )
        ph_numeric = self.SAMPLE.photometry_phu(
            1, 2, 10,
        )
        pd.testing.assert_frame_equal(ph_list, ph_numeric)

    def test_phot_phu_coordinates_same_as_numeric_mixed(self):
        ph_list = self.SAMPLE.photometry_phu(
            [1], 2, 10,
        )
        ph_numeric = self.SAMPLE.photometry_phu(
            1, [2], 10,
        )
        pd.testing.assert_frame_equal(ph_list, ph_numeric)

    def test_phot_phu_coordinates_not_equal(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.photometry_phu(
                [1, 2], [2], 10,
            )

    def test_phot_phu_coordinates_not_equal_numeric(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.photometry_phu(
                [1, 2], 1, 10,
            )

    def test_phot_phu_header(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers=["NAXIS1", "NAXIS2"]
        )
        self.assertIsInstance(ph, pd.DataFrame)
        for each in ["NAXIS1", "NAXIS2"]:
            self.assertIn(each, ph.columns)

    def test_phot_phu_single(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers="NAXIS1"
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertIn("NAXIS1", ph.columns)

    def test_phot_phu_does_not_exits(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers=["DOESNOTEXIST1", "DOESNOTEXIST2"]
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST1"]))
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST2"]))

    def test_phot_phu_does_not_exits_single(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers="DOESNOTEXIST"
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST"]))

    def test_phot_phu_one_does_not_exits(self):
        sources = self.SAMPLE.extract()
        ph = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            headers=["NAXIS", "DOESNOTEXIST1"]
        )
        self.assertIsInstance(ph, pd.DataFrame)
        self.assertTrue(all(each is None for each in ph["DOESNOTEXIST1"]))
        self.assertTrue(all(each is not None for each in ph["NAXIS"]))

    def test_pixels_to_skys(self):
        sky = self.SAMPLE.pixels_to_skys(2, 2)
        self.assertAlmostEquals(
            sky.iloc[0].sky.ra.value, 85.39916173
        )
        self.assertAlmostEquals(
            sky.iloc[0].sky.dec.value, -2.58265558
        )

    def test_pixels_to_skys_list(self):
        sky = self.SAMPLE.pixels_to_skys([2, 200], [2, 200])
        self.assertAlmostEquals(
            sky.iloc[0].sky.ra.value, 85.39916173
        )
        self.assertAlmostEquals(
            sky.iloc[0].sky.dec.value, -2.58265558
        )

        self.assertAlmostEquals(
            sky.iloc[1].sky.ra.value, 85.34366079
        )
        self.assertAlmostEquals(
            sky.iloc[1].sky.dec.value, -2.52720021
        )

    def test_pixels_to_skys_not_equal(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.pixels_to_skys([2, 200, 300], [2, 200])

        with self.assertRaises(ValueError):
            _ = self.SAMPLE.pixels_to_skys(2, [2, 200])

    def test_pixels_to_skys_unsolvable(self):
        sample = Fits.from_data_header(self.SAMPLE.data())
        with self.assertRaises(Unsolvable):
            _ = sample.pixels_to_skys(2, 2)

    def test_skys_to_pixels(self):
        sc = SkyCoord(ra=85.39916173 * units.degree, dec=-2.58265558 * units.degree)
        pixel = self.SAMPLE.skys_to_pixels(sc)
        self.assertAlmostEquals(
            pixel.iloc[0].xcentroid, 2, places=3
        )
        self.assertAlmostEquals(
            pixel.iloc[0].ycentroid, 2, places=3
        )

    def test_sky_to_pixel_list(self):
        sc = [
            SkyCoord(ra=85.39916173 * units.degree, dec=-2.58265558 * units.degree),
            SkyCoord(ra=85.34366079 * units.degree, dec=-2.52720021 * units.degree)
        ]
        pixel = self.SAMPLE.skys_to_pixels(sc)
        self.assertAlmostEquals(
            pixel.iloc[0].xcentroid, 2, places=3
        )
        self.assertAlmostEquals(
            pixel.iloc[0].ycentroid, 2, places=3
        )

        self.assertAlmostEquals(
            pixel.iloc[1].xcentroid, 200, places=3
        )
        self.assertAlmostEquals(
            pixel.iloc[1].ycentroid, 200, places=3
        )

    def test_skys_to_pixels_unsolvable(self):
        sc = SkyCoord(ra=85.39916173 * units.hourangle, dec=-2.58265558 * units.hourangle)
        with self.assertRaises(Unsolvable):
            _ = self.SAMPLE.skys_to_pixels(sc)

    def test_skys_to_pixels_unsolvable_no_header(self):
        sample = Fits.from_data_header(self.SAMPLE.data())
        sc = SkyCoord(ra=85.39916173 * units.degree, dec=-2.58265558 * units.degree)
        with self.assertRaises(Unsolvable):
            _ = sample.skys_to_pixels(sc)

    def test_bin(self):
        binned = self.SAMPLE.bin(4)
        self.assertEqual(
            self.SAMPLE.data().shape[0] // 4, binned.data().shape[0]
        )
        self.assertEqual(
            self.SAMPLE.data().shape[1] // 4, binned.data().shape[1]
        )

    def test_bin_asymmetric(self):
        binned = self.SAMPLE.bin([4, 10])
        self.assertEqual(
            self.SAMPLE.data().shape[0] // 4, binned.data().shape[0]
        )
        self.assertEqual(
            self.SAMPLE.data().shape[1] // 10, binned.data().shape[1]
        )

    def test_ccdproc(self):
        corrected = self.SAMPLE.ccdproc(
            master_zero=self.SAMPLE,
            master_dark=self.SAMPLE,
            master_flat=self.SAMPLE
        )
        self.assertIsInstance(corrected, Fits)

    def test_ccdproc_only_zero(self):
        corrected = self.SAMPLE.ccdproc(
            master_zero=self.SAMPLE
        )
        self.assertIsInstance(corrected, Fits)

    def test_ccdproc_only_dark(self):
        corrected = self.SAMPLE.ccdproc(
            master_dark=self.SAMPLE
        )
        self.assertIsInstance(corrected, Fits)

    def test_ccdproc_only_flat(self):
        corrected = self.SAMPLE.ccdproc(
            master_flat=self.SAMPLE
        )
        self.assertIsInstance(corrected, Fits)

    def test_ccdproc_nothing_to_do(self):
        with self.assertRaises(NothingToDo):
            _ = self.SAMPLE.ccdproc()

    @skip("Cannot test since it requires an API key")
    def test_solve_field(self):
        """Cannot test"""

    def test_map_to_sky(self):
        sky_map = self.SAMPLE.map_to_sky()
        self.assertListEqual(
            list(sky_map.columns.to_list()),
            ['name', 'sky', 'xcentroid', 'ycentroid']
        )


if __name__ == '__main__':
    unittest.main()
