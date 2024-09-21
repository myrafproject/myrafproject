import math
import unittest
from unittest import skip

from astropy import units
from astropy.coordinates import SkyCoord
from astropy.nddata import CCDData
from scipy.ndimage import rotate
from sep import Background

from myraflib import FitsArray, Fits
import pandas as pd
import numpy as np

from astropy.io.fits.header import Header

from myraflib.error import NumberOfElementError, Unsolvable, NothingToDo


class TestFitsArray(unittest.TestCase):
    def setUp(self):
        FitsArray.high_precision = True
        self.SAMPLE = FitsArray.sample()
        self.SAMPLE.hedit("EXPOSURE", 65)

    def test___str__(self):
        string = str(self.SAMPLE)

        self.assertTrue(string.endswith("')"))
        self.assertTrue(string.startswith(f"{self.SAMPLE.__class__.__name__}"))

    def test___repr__(self):
        string = repr(self.SAMPLE)

        self.assertTrue(string.endswith("')"))
        self.assertTrue(string.startswith(f"{self.SAMPLE.__class__.__name__}"))

    def test___add__(self):
        new_fits_array = self.SAMPLE + self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test___add___single(self):
        new_fits_array = self.SAMPLE + self.SAMPLE[0]
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + self.SAMPLE[0].data()
            )

    def test___add___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE + to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test___add___numeric_int_single(self):
        new_fits_array = self.SAMPLE + 2
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2
            )

    def test___add___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE + to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test___add___numeric_float_single(self):
        new_fits_array = self.SAMPLE + 2.5
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2.5
            )

    def test___add___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE + "2"

    def test___add___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE + ["2"] * len(self.SAMPLE)

    def test___radd__(self):
        new_fits_array = self.SAMPLE + self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test___radd___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = to_add + self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test___radd___numeric_int_single(self):
        new_fits_array = 2 + self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2
            )

    def test___radd___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = to_add + self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test___radd___numeric_float_single(self):
        new_fits_array = 2.5 + self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2.5
            )

    def test___radd___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" + self.SAMPLE

    def test___radd___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = ["2"] * len(self.SAMPLE) + self.SAMPLE

    def test___sub__(self):
        new_fits_array = self.SAMPLE - self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 0
            )

    def test___sub___single(self):
        new_fits_array = self.SAMPLE - self.SAMPLE[0]
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - self.SAMPLE[0].data()
            )

    def test___sub___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE - to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - added
            )

    def test___sub___numeric_int_single(self):
        new_fits_array = self.SAMPLE - 2
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - 2
            )

    def test___sub___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE - to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - added
            )

    def test___sub___numeric_float_single(self):
        new_fits_array = self.SAMPLE - 2.5
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - 2.5
            )

    def test___sub___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE - "2"

    def test___sub___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE - ["2"] * len(self.SAMPLE)

    def test___rsub__(self):
        new_fits_array = self.SAMPLE - self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 0
            )

    def test___rsub___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = to_add - self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                added - fits.data()
            )

    def test___rsub___numeric_int_single(self):
        new_fits_array = 2 - self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                2 - fits.data()
            )

    def test___rsub___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = to_add - self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                added - fits.data()
            )

    def test___rsub___numeric_float_single(self):
        new_fits_array = 2.5 - self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                2.5 - fits.data()
            )

    def test___rsub___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" - self.SAMPLE

    def test___rsub___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = ["2"] * len(self.SAMPLE) - self.SAMPLE

    def test___mul__(self):
        new_fits_array = self.SAMPLE * self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2
            )

    def test___mul___single(self):
        new_fits_array = self.SAMPLE * self.SAMPLE[0]
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * self.SAMPLE[0].data()
            )

    def test___mul___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE * to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * added
            )

    def test___mul___numeric_int_single(self):
        new_fits_array = self.SAMPLE * 2
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test___mul___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE * to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * added
            )

    def test___mul___numeric_float_single(self):
        new_fits_array = self.SAMPLE * 2.5
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2.5
            )

    def test___mul___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE * "2"

    def test___mul___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE * ["2"] * len(self.SAMPLE)

    def test___rmul__(self):
        new_fits_array = self.SAMPLE * self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2
            )

    def test___rmul___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = to_add * self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                added * fits.data()
            )

    def test___rmul___numeric_int_single(self):
        new_fits_array = 2 * self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                2 * fits.data()
            )

    def test___rmul___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = to_add * self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                added * fits.data()
            )

    def test___rmul___numeric_float_single(self):
        new_fits_array = 2.5 * self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                2.5 * fits.data()
            )

    def test___rmul___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" * self.SAMPLE

    def test___rmul___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = ["2"] * len(self.SAMPLE) * self.SAMPLE

    def test___div__(self):
        new_fits_array = self.SAMPLE / self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / fits.data()
            )

    def test___div___single(self):
        new_fits_array = self.SAMPLE / self.SAMPLE[0]
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / self.SAMPLE[0].data()
            )

    def test___div___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE / to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / added
            )

    def test___div___numeric_int_single(self):
        new_fits_array = self.SAMPLE / 2
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / 2
            )

    def test___div___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE / to_add
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / added
            )

    def test___div___numeric_float_single(self):
        new_fits_array = self.SAMPLE / 2.5
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / 2.5
            )

    def test___div___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = self.SAMPLE / "2"

    def test___div___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE / ["2"] * len(self.SAMPLE)

    def test___rdiv__(self):
        new_fits_array = self.SAMPLE / self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / fits.data()
            )

    def test___rdiv___numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = to_add / self.SAMPLE

        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data().round(6),
                (added / fits.data()).round(6)
            )

    def test___rdiv___numeric_int_single(self):
        new_fits_array = 2 / self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                2 / fits.data()
            )

    def test___rdiv___numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = to_add / self.SAMPLE
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data().round(6),
                (added / fits.data()).round(6)
            )

    def test___rdiv___numeric_float_single(self):
        new_fits_array = 2.5 / self.SAMPLE
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data().round(6),
                (2.5 / fits.data()).round(6)
            )

    def test___rdiv___value_error(self):
        with self.assertRaises(NotImplementedError):
            _ = "2" / self.SAMPLE

    def test___rdiv___list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = ["2"] * len(self.SAMPLE) / self.SAMPLE

    def test_file_does_not_exist(self):
        files = ["a", "b", "c"]
        with self.assertRaises(NumberOfElementError):
            _ = FitsArray.from_paths(files)

    def test_header(self):
        headers = self.SAMPLE.header()
        self.assertIsInstance(headers, pd.DataFrame)

        for each in [
            "SIMPLE", "BITPIX", "NAXIS",
            "NAXIS1", "NAXIS2"
        ]:
            self.assertIn(each, headers.columns)

    def test_data(self):
        list_of_data = self.SAMPLE.data()
        self.assertIsInstance(list_of_data, list)
        for data in list_of_data:
            self.assertIsInstance(data, np.ndarray)

    def test_value(self):
        data = self.SAMPLE.value(200, 200)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertListEqual(data["value"].tolist(), [each.data()[200][200] for each in self.SAMPLE])

    def test_pure_header(self):
        list_of_pure_headers = self.SAMPLE.pure_header()
        self.assertIsInstance(list_of_pure_headers, list)
        for pure_header in list_of_pure_headers:
            self.assertIsInstance(pure_header, Header)
            for each in [
                "SIMPLE", "BITPIX", "NAXIS",
                "NAXIS1", "NAXIS2"
            ]:
                self.assertIn(each, pure_header)

    def test_ccd(self):
        list_of_ccds = self.SAMPLE.ccd()
        self.assertIsInstance(list_of_ccds, list)
        for ccd, fits in zip(list_of_ccds, self.SAMPLE):
            self.assertIsInstance(ccd, CCDData)
            np.testing.assert_array_equal(ccd.data, fits.data())

    def test_imstat(self):
        imstat = self.SAMPLE.imstat()
        self.assertIsInstance(imstat, pd.DataFrame)

        for each in ["npix", "mean", "stddev", "min", "max"]:
            self.assertIn(each, imstat.columns)

    def test_cosmic_clean(self):
        cleaned = self.SAMPLE.cosmic_clean()
        self.assertIsInstance(cleaned, FitsArray)

    def test_hedit(self):
        self.SAMPLE.hedit("MSH", "TEST")
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)

        self.assertListEqual(
            header["MSH"].values.tolist(),
            ["TEST"] * len(self.SAMPLE)
        )

    def test_hedit_integer(self):
        self.SAMPLE.hedit("MSH", 44)
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)

        self.assertListEqual(
            header["MSH"].values.tolist(),
            [44] * len(self.SAMPLE)
        )

    def test_hedit_float(self):
        self.SAMPLE.hedit("MSH", 4.4)
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)

        self.assertListEqual(
            header["MSH"].values.tolist(),
            [4.4] * len(self.SAMPLE)
        )

    def test_hedit_bool(self):
        self.SAMPLE.hedit("MSH", False)
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)

        self.assertListEqual(
            header["MSH"].values.tolist(),
            [False] * len(self.SAMPLE)
        )

    def test_hedit_list(self):
        self.SAMPLE.hedit(["MSH1", "MSH2"], ["TEST1", "TEST2"])
        header = self.SAMPLE.header()

        for each in ["MSH1", "MSH2"]:
            self.assertIn(each, header.columns)

        for key, value in zip(["MSH1", "MSH2"], ["TEST1", "TEST2"]):
            self.assertEqual(header[key].values.tolist(),
                             [value] * len(self.SAMPLE))

    def test_hedit_list_different(self):
        self.SAMPLE.hedit(["MSH1", "MSH2", "MSH3", "MSH4"], ["TEST1", 44, 4.4, True])
        header = self.SAMPLE.header()

        for each in ["MSH1", "MSH2", "MSH3", "MSH4"]:
            self.assertIn(each, header.columns)

        for key, value in zip(["MSH1", "MSH2", "MSH3", "MSH4"], ["TEST1", 44, 4.4, True]):
            self.assertEqual(header[key].values.tolist(),
                             [value] * len(self.SAMPLE))

    def test_hedit_no_value(self):
        self.SAMPLE.hedit("MSH")

    def test_hedit_no_value_list(self):
        self.SAMPLE.hedit(["MSH1", "MSH2"])

    def test_hedit_value_key_different(self):
        self.SAMPLE.hedit(["MSH1", "MSH2"], "TEST")

    def test_hedit_key_value_different(self):
        self.SAMPLE.hedit("MSH", ["TEST1", "TEST2"])

    def test_hedit_key_value_different_length(self):
        self.SAMPLE.hedit(
            ["MSH1", "MSH2", "MSH3"],
            ["TEST1", "TEST2"]
        )

    def test_hedit_value_key_different_length(self):
        self.SAMPLE.hedit(
            ["MSH1", "MSH2"],
            ["TEST1", "TEST2", "TEST3"]
        )

    def test_hedit_delete(self):
        self.SAMPLE.hedit("MSH", "TEST")
        header = self.SAMPLE.header()
        self.assertIn("MSH", header.columns)
        self.assertEqual(
            header["MSH"].values.tolist(),
            ["TEST"] * len(self.SAMPLE)
        )

        self.SAMPLE.hedit("MSH", delete=True)
        new_header = self.SAMPLE.header()
        self.assertNotIn("MSH", new_header.columns)
        self.assertEqual(
            header["MSH"].values.tolist(),
            ["TEST"] * len(self.SAMPLE)
        )

    def test_hselect(self):
        selected = self.SAMPLE.hselect("NAXIS")
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), len(self.SAMPLE))

    def test_hselect_does_not_exits(self):
        selected = self.SAMPLE.hselect("DOESNOTEXIST")
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), 0)

    def test_hselect_list(self):
        selected = self.SAMPLE.hselect(["NAXIS"])
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), len(self.SAMPLE))

    def test_hselect_list_does_not_exits(self):
        selected = self.SAMPLE.hselect(["DOESNOTEXIST"])
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), 0)

    def test_hselect_list_multiple(self):
        selected = self.SAMPLE.hselect(["NAXIS", "NAXIS1"])
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), len(self.SAMPLE))

    def test_hselect_list_multiple_does_not_exits(self):
        selected = self.SAMPLE.hselect(["DOESNOTEXIST", "DOESNOTEXIST2"])
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), 0)

    def test_hselect_list_multiple_at_least_one_exist(self):
        selected = self.SAMPLE.hselect(["NAXIS", "DOESNOTEXIST2"])
        self.assertIsInstance(selected, pd.DataFrame)
        self.assertEqual(len(selected), len(self.SAMPLE))

    def test_add(self):
        new_fits_array = self.SAMPLE.add(self.SAMPLE)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test_add_single(self):
        new_fits_array = self.SAMPLE.add(self.SAMPLE[0])
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + self.SAMPLE[0].data()
            )

    def test_add_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.add(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test_add_numeric_int_single(self):
        new_fits_array = self.SAMPLE.add(2)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2
            )

    def test_add_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.add(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test_add_numeric_float_single(self):
        new_fits_array = self.SAMPLE.add(2.5)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2.5
            )

    def test_add_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.add("2")

    def test_add_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.add(["2"] * len(self.SAMPLE))

    def test_sub(self):
        new_fits_array = self.SAMPLE.sub(self.SAMPLE)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 0
            )

    def test_sub_single(self):
        new_fits_array = self.SAMPLE.sub(self.SAMPLE[0])
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - self.SAMPLE[0].data()
            )

    def test_sub_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.sub(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - added
            )

    def test_sub_numeric_int_single(self):
        new_fits_array = self.SAMPLE.sub(2)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - 2
            )

    def test_sub_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.sub(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - added
            )

    def test_sub_numeric_float_single(self):
        new_fits_array = self.SAMPLE.sub(2.5)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - 2.5
            )

    def test_sub_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.add("2")

    def test_sub_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.add(["2"] * len(self.SAMPLE))

    def test_mul(self):
        new_fits_array = self.SAMPLE.mul(self.SAMPLE)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * fits.data()
            )

    def test_mul_single(self):
        new_fits_array = self.SAMPLE.mul(self.SAMPLE[0])
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * self.SAMPLE[0].data()
            )

    def test_mul_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.mul(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * added
            )

    def test_mul_numeric_int_single(self):
        new_fits_array = self.SAMPLE.mul(2)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test_mul_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.mul(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * added
            )

    def test_mul_numeric_float_single(self):
        new_fits_array = self.SAMPLE.mul(2.5)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2.5
            )

    def test_mul_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.add("2")

    def test_mul_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.add(["2"] * len(self.SAMPLE))

    def test_div(self):
        new_fits_array = self.SAMPLE.div(self.SAMPLE)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / fits.data()
            )

    def test_div_single(self):
        new_fits_array = self.SAMPLE.div(self.SAMPLE[0])
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / self.SAMPLE[0].data()
            )

    def test_div_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.div(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / added
            )

    def test_div_numeric_int_single(self):
        new_fits_array = self.SAMPLE.div(2)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / 2
            )

    def test_div_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.div(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / added
            )

    def test_div_numeric_float_single(self):
        new_fits_array = self.SAMPLE.div(2.5)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / 2.5
            )

    def test_div_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.add("2")

    def test_div_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.add(["2"] * len(self.SAMPLE))

    def test_pow(self):
        new_fits_array = self.SAMPLE.pow(self.SAMPLE)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** fits.data()
            )

    def test_pow_single(self):
        new_fits_array = self.SAMPLE.pow(self.SAMPLE[0])
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** self.SAMPLE[0].data()
            )

    def test_pow_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.pow(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** added
            )

    def test_pow_numeric_int_single(self):
        new_fits_array = self.SAMPLE.pow(2)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2
            )

    def test_pow_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.pow(to_add)
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** added
            )

    def test_pow_numeric_float_single(self):
        new_fits_array = self.SAMPLE.pow(2.5)
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2.5
            )

    def test_pow_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.pow("2")

    def test_pow_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.pow(["2"] * len(self.SAMPLE))

    def test_imarith_add(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE, "+")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test_imarith_add_single(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE[0], "+")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + self.SAMPLE[0].data()
            )

    def test_imarith_add_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.imarith(to_add, "+")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test_imarith_add_numeric_int_single(self):
        new_fits_array = self.SAMPLE.imarith(2, "+")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2
            )

    def test_imarith_add_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.imarith(to_add, "+")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + added
            )

    def test_imarith_add_numeric_float_single(self):
        new_fits_array = self.SAMPLE.imarith(2.5, "+")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() + 2.5
            )

    def test_imarith_add_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.imarith("2", '+')

    def test_imarith_add_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.imarith(["2"] * len(self.SAMPLE), '+')

    def test_imarith_sub(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE, "-")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 0
            )

    def test_imarith_sub_single(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE[0], "-")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - self.SAMPLE[0].data()
            )

    def test_imarith_sub_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.imarith(to_add, "-")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - added
            )

    def test_imarith_sub_numeric_int_single(self):
        new_fits_array = self.SAMPLE.imarith(2, "-")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - 2
            )

    def test_imarith_sub_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.imarith(to_add, "-")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - added
            )

    def test_imarith_sub_numeric_float_single(self):
        new_fits_array = self.SAMPLE.imarith(2.5, "-")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() - 2.5
            )

    def test_imarith_sub_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.imarith("2", "-")

    def test_imarith_sub_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.imarith(["2"] * len(self.SAMPLE), "-")

    def test_imarith_mul(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE, "*")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * fits.data()
            )

    def test_imarith_mul_single(self):
        new_fits_array = self.SAMPLE.mul(self.SAMPLE[0], "*")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * self.SAMPLE[0].data()
            )

    def test_imarith_mul_numeric_int(self):
        to_add = list(range(len(self.SAMPLE)))
        new_fits_array = self.SAMPLE.imarith(to_add, "*")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * added
            )

    def test_imarith_mul_numeric_int_single(self):
        new_fits_array = self.SAMPLE.imarith(2, "*")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2
            )

    def test_imarith_mul_numeric_float(self):
        to_add = np.linspace(1, 0, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.imarith(to_add, "*")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * added
            )

    def test_imarith_mul_numeric_float_single(self):
        new_fits_array = self.SAMPLE.imarith(2.5, "*")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() * 2.5
            )

    def test_imarith_mul_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.imarith("2", "*")

    def test_imarith_mul_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.imarith(["2"] * len(self.SAMPLE), "*")

    def test_imarith_div(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE, "/")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / fits.data()
            )

    def test_imarith_div_single(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE[0], "/")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / self.SAMPLE[0].data()
            )

    def test_imarith_div_numeric_int(self):
        to_add = list(range(1, len(self.SAMPLE) + 1))
        new_fits_array = self.SAMPLE.imarith(to_add, "/")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / added
            )

    def test_imarith_div_numeric_int_single(self):
        new_fits_array = self.SAMPLE.imarith(2, "/")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / 2
            )

    def test_imarith_div_numeric_float(self):
        to_add = np.linspace(2, 1, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.imarith(to_add, "/")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / added
            )

    def test_imarith_div_numeric_float_single(self):
        new_fits_array = self.SAMPLE.imarith(2.5, "/")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() / 2.5
            )

    def test_imarith_div_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.imarith("2", "/")

    def test_imarith_div_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.imarith(["2"] * len(self.SAMPLE), "/")

    def test_imarith_pow(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE, "**")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** fits.data()
            )

    def test_imarith_pow_single(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE[0], "**")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** self.SAMPLE[0].data()
            )

    def test_imarith_pow_numeric_int(self):
        to_add = list(range(1, len(self.SAMPLE) + 1))
        new_fits_array = self.SAMPLE.imarith(to_add, "**")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** added
            )

    def test_imarith_pow_numeric_int_single(self):
        new_fits_array = self.SAMPLE.imarith(2, "**")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2
            )

    def test_imarith_pow_numeric_float(self):
        to_add = np.linspace(2, 1, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.imarith(to_add, "**")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** added
            )

    def test_imarith_pow_numeric_float_single(self):
        new_fits_array = self.SAMPLE.imarith(2.5, "**")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2.5
            )

    def test_imarith_pow_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.imarith("2", "**")

    def test_imarith_pow_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.imarith(["2"] * len(self.SAMPLE), "**")

    def test_imarith_pow2(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE, "^")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** fits.data()
            )

    def test_imarith_pow2_single(self):
        new_fits_array = self.SAMPLE.imarith(self.SAMPLE[0], "^")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** self.SAMPLE[0].data()
            )

    def test_imarith_pow2_numeric_int(self):
        to_add = list(range(1, len(self.SAMPLE) + 1))
        new_fits_array = self.SAMPLE.imarith(to_add, "^")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** added
            )

    def test_imarith_pow2_numeric_int_single(self):
        new_fits_array = self.SAMPLE.imarith(2, "^")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2
            )

    def test_imarith_pow2_numeric_float(self):
        to_add = np.linspace(2, 1, len(self.SAMPLE)).tolist()
        new_fits_array = self.SAMPLE.imarith(to_add, "^")
        for fits, new_fits, added in zip(self.SAMPLE, new_fits_array, to_add):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** added
            )

    def test_imarith_pow2_numeric_float_single(self):
        new_fits_array = self.SAMPLE.imarith(2.5, "^")
        for fits, new_fits in zip(self.SAMPLE, new_fits_array):
            np.testing.assert_array_equal(
                new_fits.data(),
                fits.data() ** 2.5
            )

    def test_imarith_pow2_value_error(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.imarith("2", "^")

    def test_imarith_pow2_list_value_error(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.imarith(["2"] * len(self.SAMPLE), "^")

    def test_imarith_bad_operand(self):
        with self.assertRaises(NumberOfElementError):
            self.SAMPLE.imarith(self.SAMPLE, "?")

    def test_shift_numeric(self):
        new_fits_array = self.SAMPLE.shift(20, 10)
        for fits, shifted in zip(self.SAMPLE, new_fits_array):
            self.assertEqual(
                fits.data()[123, 123],
                shifted.data()[133, 143],
            )

    def test_shift_list(self):
        xs = list(range(10, 110, 10))
        ys = list(range(20, 120, 10))
        new_fits_array = self.SAMPLE.shift(xs, ys)
        for fits, shifted, x, y in zip(self.SAMPLE, new_fits_array, xs, ys):
            self.assertEqual(
                fits.data()[123, 123],
                shifted.data()[123 + y, 123 + x],
            )

    def test_shift_list_number_of_elements(self):
        xs = list(range(10, 110))
        ys = list(range(20, 120))
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.shift(xs, ys)

    def test_rotate(self):
        new_fits_array = self.SAMPLE.rotate(math.pi)
        for fits, rotated in zip(self.SAMPLE, new_fits_array):
            rotated_data = rotate(fits.data(), 180, reshape=False)
            np.testing.assert_array_equal(
                rotated.data(), rotated_data
            )

    @skip("Cannot test because couldn't find a way to do so")
    def test_rotate_individual(self):
        angles = list(math.radians(each) for each in range(0, 180, 18))
        new_fits_array = self.SAMPLE.rotate(angles)
        for fits, rotated, angle in zip(self.SAMPLE, new_fits_array, angles):
            rotated_data = rotate(fits.data(), math.degrees(angle), reshape=False)
            np.testing.assert_array_equal(
                rotated.data(), rotated_data
            )

    def test_rotate_number_of_elements(self):
        angles = list(each * math.pi / 180 for each in range(0, 180))
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.rotate(angles)

    def test_shift_not_equal(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.shift(
                [20] * len(self.SAMPLE),
                [10] * (len(self.SAMPLE) - 2)
            )

    def test_shift_bad_data_type(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.shift("20", "10")

    def test_shift_bad_data_type_listed(self):
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.shift(
                ["20"] * len(self.SAMPLE),
                ["10"] * len(self.SAMPLE)
            )

    def test_crop(self):
        new_fits_array = self.SAMPLE.crop(20, 12, 220, 200)
        for fits, cropped in zip(self.SAMPLE, new_fits_array):
            cropped_data = fits.data()[12:212, 20:240]
            np.testing.assert_array_equal(
                cropped.data(), cropped_data
            )

    def test_crop_list(self):
        xs = list(range(0, 100, 10))
        ys = list(range(100, 200, 10))
        widths = list(range(10, 110, 10))
        heights = list(range(110, 210, 10))
        new_fits_array = self.SAMPLE.crop(xs, ys, widths, heights)
        for fits, cropped, x, y, w, h in zip(self.SAMPLE, new_fits_array, xs, ys, widths, heights):
            cropped_data = fits.data()[y:y + h, x:x + w]
            np.testing.assert_array_equal(
                cropped.data(), cropped_data
            )

    def test_crop_list_number_of_elements(self):
        xs = list(range(0, 100))
        ys = list(range(100, 200))
        widths = list(range(10, 110))
        heights = list(range(110, 210))
        with self.assertRaises(NumberOfElementError):
            _ = self.SAMPLE.crop(xs, ys, widths, heights)

    def test_align(self):
        aligned = self.SAMPLE.align()
        self.assertIsInstance(aligned, FitsArray)

    def test_align_numeric(self):
        aligned = self.SAMPLE.align(4)
        self.assertIsInstance(aligned, FitsArray)

    def test_align_numeric_negative(self):
        aligned = self.SAMPLE.align(-1)
        self.assertIsInstance(aligned, FitsArray)

    def test_align_another_fits(self):
        aligned = self.SAMPLE.align(self.SAMPLE[0])
        self.assertIsInstance(aligned, FitsArray)

    def test_zero_correction(self):
        new_fits_array = self.SAMPLE.zero_correction(self.SAMPLE[0])
        self.assertIn("MY-ZERO", new_fits_array.header().columns)

        for fits, zero_corrected in zip(self.SAMPLE, new_fits_array):
            self.assertTrue(
                np.all(
                    zero_corrected.data() ==
                    fits.data() - self.SAMPLE[0].data()
                )
            )

    def test_zero_correction_over_correction(self):
        zero_corrected = self.SAMPLE.zero_correction(self.SAMPLE[0])
        double_new_fits_array = zero_corrected.zero_correction(self.SAMPLE[0])

        for fits, double_zero_corrected in zip(
                self.SAMPLE, double_new_fits_array
        ):
            self.assertTrue(
                np.all(
                    double_zero_corrected.data() ==
                    fits.data() - self.SAMPLE[0].data()
                )
            )

    def test_zero_correction_over_correction_force(self):
        new_fits_array = self.SAMPLE.zero_correction(self.SAMPLE[0])
        double_new_fits_array = new_fits_array.zero_correction(
            self.SAMPLE[0], force=True
        )
        for fits, double_zero_corrected in zip(
                self.SAMPLE, double_new_fits_array
        ):
            self.assertTrue(
                np.all(
                    double_zero_corrected.data() ==
                    fits.data() - 2 * self.SAMPLE[0].data()
                )
            )

    def test_dark_correction(self):
        new_fits_array = self.SAMPLE.dark_correction(self.SAMPLE[0])
        self.assertIn("MY-DARK", new_fits_array.header().columns)
        for fits, dark_corrected in zip(self.SAMPLE, new_fits_array):
            self.assertTrue(
                np.all(
                    dark_corrected.data() ==
                    fits.data() - self.SAMPLE[0].data()
                )
            )

    def test_dark_correction_over_correction(self):
        new_fits_array = self.SAMPLE.dark_correction(self.SAMPLE[0])
        double_new_fits_array = new_fits_array.dark_correction(self.SAMPLE[0])

        for fits, double_dark_corrected in zip(
                self.SAMPLE, double_new_fits_array
        ):
            self.assertTrue(
                np.all(
                    double_dark_corrected.data() ==
                    fits.data() - self.SAMPLE[0].data()
                )
            )

    def test_dark_correction_over_correction_force(self):
        new_fits_array = self.SAMPLE.dark_correction(self.SAMPLE[0])
        double_new_fits_array = new_fits_array.dark_correction(
            self.SAMPLE[0],
            force=True
        )

        for fits, double_dark_corrected in zip(
                self.SAMPLE, double_new_fits_array
        ):
            self.assertTrue(
                np.all(
                    double_dark_corrected.data() ==
                    fits.data() - 2 * self.SAMPLE[0].data()
                )
            )

    def test_flat_correction(self):
        new_fits_array = self.SAMPLE.flat_correction(self.SAMPLE[0])
        self.assertIn("MY-FLAT", new_fits_array.header().columns)
        for fits, flat_corrected in zip(self.SAMPLE, new_fits_array):
            flat_corrected_numpy = fits.data() / self.SAMPLE[0].data()
            division = np.round(flat_corrected.data() / flat_corrected_numpy,
                                5)
            self.assertTrue(
                np.all(
                    division[~np.isnan(division)] ==
                    division[~np.isnan(division)][0]
                )
            )

    def test_flat_correction_over_correction(self):
        new_fits_array = self.SAMPLE.flat_correction(self.SAMPLE[0])
        double_new_fits_array = new_fits_array.flat_correction(self.SAMPLE[0])

        for fits, double_new_fits_array in zip(
                self.SAMPLE, double_new_fits_array
        ):
            flat_corrected_numpy = fits.data() / self.SAMPLE[0].data()
            division = np.round(
                double_new_fits_array.data() / flat_corrected_numpy,
                5
            )
            self.assertTrue(
                np.all(
                    division[~np.isnan(division)] ==
                    division[~np.isnan(division)][0]
                )
            )

    def test_flat_correction_over_correction_force(self):
        new_fits_array = self.SAMPLE.flat_correction(self.SAMPLE[0])
        double_new_fits_array = new_fits_array.flat_correction(
            self.SAMPLE[0],
            force=True
        )

        for fits, double_new_fits_array in zip(
                self.SAMPLE, double_new_fits_array
        ):
            flat_corrected_numpy = fits.data() / (
                    self.SAMPLE[0].data() * self.SAMPLE[0].data()
            )
            division = np.round(
                double_new_fits_array.data() / flat_corrected_numpy,
                5
            )
            self.assertTrue(
                np.all(
                    division[~np.isnan(division)] ==
                    division[~np.isnan(division)][0]
                )
            )

    def test_ccdproc(self):
        new_fits_array = self.SAMPLE.ccdproc(
            master_zero=self.SAMPLE[0],
            master_dark=self.SAMPLE[0],
            master_flat=self.SAMPLE[0]
        )
        self.assertIsInstance(new_fits_array, FitsArray)

    def test_ccdproc_only_zero(self):
        new_fits_array = self.SAMPLE.ccdproc(
            master_zero=self.SAMPLE[0]
        )
        self.assertIsInstance(new_fits_array, FitsArray)

    def test_ccdproc_only_dark(self):
        new_fits_array = self.SAMPLE.ccdproc(
            master_dark=self.SAMPLE[0]
        )
        self.assertIsInstance(new_fits_array, FitsArray)

    def test_ccdproc_only_flat(self):
        new_fits_array = self.SAMPLE.ccdproc(
            master_flat=self.SAMPLE[0]
        )
        self.assertIsInstance(new_fits_array, FitsArray)

    def test_ccdproc_nothing_to_do(self):
        with self.assertRaises(NothingToDo):
            _ = self.SAMPLE.ccdproc()

    def test_background(self):
        list_of_background = self.SAMPLE.background()
        self.assertIsInstance(list_of_background, list)
        for background in list_of_background:
            self.assertIsInstance(background, Background)

    def test_daofind(self):
        sources = self.SAMPLE.daofind()
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["id", "xcentroid", "ycentroid", "sharpness", "roundness1",
                     "roundness2", "npix", "sky", "peak", "flux", "mag"]:
            self.assertIn(each, sources)

    def test_daofind_indexed(self):
        sources = self.SAMPLE.daofind(1)
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["id", "xcentroid", "ycentroid", "sharpness", "roundness1",
                     "roundness2", "npix", "sky", "peak", "flux", "mag"]:
            self.assertIn(each, sources)

    def test_daofind_indexed_negative(self):
        sources = self.SAMPLE.daofind(-1)
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["id", "xcentroid", "ycentroid", "sharpness", "roundness1",
                     "roundness2", "npix", "sky", "peak", "flux", "mag"]:
            self.assertIn(each, sources)

    def test_extract(self):
        sources = self.SAMPLE.extract()
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["xcentroid", "ycentroid"]:
            self.assertIn(each, sources)

    def test_extract_indexed(self):
        sources = self.SAMPLE.extract(1)
        self.assertIsInstance(sources, pd.DataFrame)
        for each in ["xcentroid", "ycentroid"]:
            self.assertIn(each, sources)

    def test_extract_indexed_negative(self):
        sources = self.SAMPLE.extract(-1)
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
        empty = self.SAMPLE.photometry_sep(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure="DOESNOTEXIST"
        )
        self.assertEqual(
            len(empty), 0
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
        empty = self.SAMPLE.photometry_phu(
            sources["xcentroid"], sources["ycentroid"], 10,
            exposure="DOESNOTEXIST"
        )

        self.assertEqual(
            len(empty), 0
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
        print()
        print(ph_exptime)
        print(ph_65)

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

    def test_merge(self):
        sample = FitsArray.sample()
        sample.merge(self.SAMPLE)
        self.assertEqual(len(sample), 20)

    def test_merge_not_fits_array(self):
        sample = FitsArray.sample()
        with self.assertRaises(ValueError):
            sample.merge(1)

    def test_append(self):
        sample = FitsArray.sample()
        fits = Fits.sample()
        sample.append(fits)
        self.assertEqual(len(sample), 11)

    def test_append_not_fits(self):
        sample = FitsArray.sample()
        with self.assertRaises(ValueError):
            sample.append(1)

    def test_combine_average(self):
        combined = self.SAMPLE.combine(method="average")
        self.assertIsInstance(combined, Fits)
        np.testing.assert_array_equal(
            combined.data(),
            np.mean([each.data() for each in self.SAMPLE], axis=0),
        )

    def test_combine_mean(self):
        combined = self.SAMPLE.combine(method="mean")
        self.assertIsInstance(combined, Fits)
        np.testing.assert_array_equal(
            combined.data(),
            np.mean([each.data() for each in self.SAMPLE], axis=0),
        )

    def test_combine_median(self):
        combined = self.SAMPLE.combine(method="median")
        self.assertIsInstance(combined, Fits)
        np.testing.assert_array_equal(
            combined.data(),
            np.median([each.data() for each in self.SAMPLE], axis=0),
        )

    def test_pixels_to_skys(self):
        ra_decs = [
            [85.39915825, -2.58265742],
            [85.40195947, -2.58545664],
            [85.40476344, -2.58825915],
            [85.40756595, -2.59105989],
            [85.41036992, -2.5938613],
            [85.41317306, -2.59666108],
            [85.41597842, -2.59946113],
            [85.41877975, -2.60226092],
            [85.42158183, -2.60506119],
            [85.42438693, -2.60786386],
        ]
        skys = self.SAMPLE.pixels_to_skys(2, 2)
        for sky, ra_dec in zip(skys.sky.tolist(), ra_decs):
            self.assertAlmostEquals(
                sky.ra.value, ra_dec[0], places=3
            )
            self.assertAlmostEquals(
                sky.dec.value, ra_dec[1], places=3
            )

    def test_pixels_to_skys_list(self):
        sky = self.SAMPLE.pixels_to_skys([2, 200], [2, 200])
        self.assertIsInstance(sky, pd.DataFrame)

    def test_pixels_to_skys_not_equal(self):
        with self.assertRaises(ValueError):
            _ = self.SAMPLE.pixels_to_skys([2, 200, 300], [2, 200])

        with self.assertRaises(ValueError):
            _ = self.SAMPLE.pixels_to_skys(2, [2, 200])

    def test_pixels_to_skys_unsolvable(self):
        sample = FitsArray(
            [
                Fits.from_data_header(fits.data())
                for fits in self.SAMPLE
            ]
        )
        with self.assertRaises(Unsolvable):
            _ = sample.pixels_to_skys(2, 2)

    def test_skys_to_pixels(self):
        sc = SkyCoord(ra=85.39916173 * units.degree, dec=-2.58265558 * units.degree)
        pixel = self.SAMPLE.skys_to_pixels(sc)
        self.assertIsInstance(pixel, pd.DataFrame)

    def test_sky_to_pixel_list(self):
        sc = [
            SkyCoord(ra=85.39916173 * units.degree, dec=-2.58265558 * units.degree),
            SkyCoord(ra=85.34366079 * units.degree, dec=-2.52720021 * units.degree)
        ]
        pixel = self.SAMPLE.skys_to_pixels(sc)

        self.assertIsInstance(pixel, pd.DataFrame)

    def test_skys_to_pixels_unsolvable(self):
        sc = SkyCoord(ra=85.39916173 * units.hourangle, dec=-2.58265558 * units.hourangle)

        with self.assertRaises(Unsolvable):
            _ = self.SAMPLE.skys_to_pixels(sc)

    def test_skys_to_pixels_unsolvable_no_header(self):
        sc = SkyCoord(ra=85.39916173 * units.degree, dec=-2.58265558 * units.degree)

        sample = FitsArray(
            [
                Fits.from_data_header(fits.data())
                for fits in self.SAMPLE
            ]
        )

        with self.assertRaises(Unsolvable):
            _ = sample.skys_to_pixels(sc)

    def test_bin(self):
        new_fits_array = self.SAMPLE.bin(4)
        for fits, binned in zip(self.SAMPLE, new_fits_array):
            self.assertEqual(
                fits.data().shape[0] // 4, binned.data().shape[0]
            )
            self.assertEqual(
                fits.data().shape[1] // 4, binned.data().shape[1]
            )

    def test_bin_asymmetric(self):
        new_fits_array = self.SAMPLE.bin([4, 10])
        for fits, binned in zip(self.SAMPLE, new_fits_array):
            self.assertEqual(
                fits.data().shape[0] // 4, binned.data().shape[0]
            )
            self.assertEqual(
                fits.data().shape[1] // 10, binned.data().shape[1]
            )

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
