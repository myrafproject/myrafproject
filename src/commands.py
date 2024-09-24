import argparse
import math
from json import dumps
from pathlib import Path

from astropy.coordinates import SkyCoord

from myraflib import FitsArray, Fits


def imhead(files):
    fits_array = FitsArray.from_pattern(files, verbose=True)
    headers = fits_array.header()
    print(headers.to_json(orient='index', indent=4))


def imhedit(files, keys, values, comments, delete, value_is_key):
    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.hedit(keys=keys, values=values, comments=comments, delete=delete, value_is_key=value_is_key)


def imarith(files, operator, other, output):
    if operator not in ['+', '-', '*', '/', '**', '^']:
        raise ValueError("Operator must be +,-,/,*,**")

    if Path(other).exists():
        other = Fits.from_path(other)
    else:
        try:
            other = float(other)
        except ValueError:
            raise ValueError("Other must be either a path or a number")

    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.imarith(other, operand=operator, output=output)


def imvalue(files, x, y):
    fits_array = FitsArray.from_pattern(files, verbose=True)
    value = fits_array.value(x, y)
    print(value.to_json(orient='index', indent=4))


def imstat(files):
    fits_array = FitsArray.from_pattern(files, verbose=True)
    image_statistics = fits_array.imstat()
    print(image_statistics.to_json(orient='index', indent=4))


def imbin(files, x, y, output):
    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.bin([x, y], output=output)


def imcrop(files, x, y, w, h, output):
    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.crop(x, y, w, h, output=output)


def imrotate(files, angle, degrees, output):
    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    if degrees:
        the_angle = math.radians(angle)
    else:
        the_angle = angle

    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.rotate(the_angle, output=output)


def imshift(files, x, y, output):
    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.shift(x, y, output=output)


def imclean(files, output, sigclip, sigfrac, objlim, gain, readnoise, satlevel, niter, sepmed, cleantype, fsmode,
            psfmodel, psffwhm, psfsize, psfbeta, gain_apply):
    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    fits_array = FitsArray.from_pattern(files, verbose=True)

    fits_array.cosmic_clean(
        output=output, sigclip=sigclip, sigfrac=sigfrac, objlim=objlim, gain=gain, readnoise=readnoise,
        satlevel=satlevel, niter=niter, sepmed=sepmed, cleantype=cleantype, fsmode=fsmode, psfmodel=psfmodel,
        psffwhm=psffwhm, psfsize=psfsize, psfbeta=psfbeta, gain_apply=gain_apply
    )


def imshow(files):
    fits_array = FitsArray.from_pattern(files, verbose=True)
    fits_array.show()


def imalign(files, other, output, max_control_points, min_area):
    if not Path(output).is_dir():
        raise ValueError("Output directory must be an existing directory")

    if Path(other).exists():
        reference = Fits.from_path(other)
    else:
        try:
            reference = other
        except ValueError:
            raise ValueError("Other must be either a path or a number")

    fits_array = FitsArray.from_pattern(files, verbose=True)

    fits_array.align(reference, max_control_points=max_control_points, min_area=min_area, output=output)


def imp2s(files, x, y):
    fits_array = FitsArray.from_pattern(files, verbose=True)

    sky = fits_array.pixels_to_skys(x, y)
    result = {
        index: {"ra": sky.values[0].ra.degree, "dec": sky.values[0].dec.degree}
        for index, sky in sky[["sky"]].iterrows()
    }

    print(dumps(result, indent=4))


def ims2p(files, ra, dec):
    fits_array = FitsArray.from_pattern(files, verbose=True)

    sky = SkyCoord(ra, dec, unit='deg')
    pixels = fits_array.skys_to_pixels(sky)
    print(pixels[["xcentroid", "ycentroid"]].to_json(orient='index', indent=4))


def immap2sky(files):
    fits = Fits.from_path(files)
    sky_map = fits.map_to_sky()
    result = {
        sky["name"]: {"ra": sky["sky"].ra.degree, "dec": sky["sky"].dec.degree, "x": sky["xcentroid"],
                      "y": sky["ycentroid"]}
        for index, sky in sky_map[["name", "sky", "xcentroid", "ycentroid"]].iterrows()
    }

    print(dumps(result, indent=4))


def main():
    parser = argparse.ArgumentParser(description="MYRaf Command Line Tools")
    subparsers = parser.add_subparsers(dest='command', title='Description',
                                       description='MYRaf provides some of its functionalities as command tool.',
                                       help='Subcommand help')

    header = subparsers.add_parser('header', help='Image Header')
    header.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')

    hedit = subparsers.add_parser('hedit', help='Header Edit')
    hedit.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    hedit.add_argument('key', type=str, help='Key for the header card')
    hedit.add_argument('--value', type=str, help='Value for the header card', default=None)
    hedit.add_argument('--comment', type=str, help='Value for the header card', default=None)
    hedit.add_argument('--delete', action='store_true', help='Delete the header card', default=False)
    hedit.add_argument('--value-is-key', action='store_true', help='Copy value form the card',
                       default=False)

    arith = subparsers.add_parser('arith', help='Arithmetic')
    arith.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    arith.add_argument('operator', type=str, help='Operator +, -, /, *, **, ^')
    arith.add_argument('other', help='Fits or Number to Operate')
    arith.add_argument('output', type=str, help='Output directory')

    value = subparsers.add_parser('value', help='Pixel Value')
    value.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    value.add_argument('x', type=int, help='X component of coordinate')
    value.add_argument('y', type=int, help='Y component of coordinate')

    statistics = subparsers.add_parser('stat', help='Image Statistics')
    statistics.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')

    binning = subparsers.add_parser('bin', help='Image Binning')
    binning.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    binning.add_argument('x', type=int, help='X amount')
    binning.add_argument('y', type=int, help='Y amount')
    binning.add_argument('output', type=str, help='Output directory')

    crop = subparsers.add_parser('crop', help='Image Cropping')
    crop.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    crop.add_argument('x', type=int, help='X component of coordinate')
    crop.add_argument('y', type=int, help='Y component of coordinate')
    crop.add_argument('w', type=int, help='Width of bounding box')
    crop.add_argument('h', type=int, help='Height of bounding box')
    crop.add_argument('output', type=str, help='Output directory')

    rotate = subparsers.add_parser('rotate', help='Image Rotate')
    rotate.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    rotate.add_argument('angle', type=int, help='Angle')
    rotate.add_argument('output', type=str, help='Output directory')
    rotate.add_argument('--degrees', action='store_true', help='Angle is in Degrees', default=False)

    shift = subparsers.add_parser('shift', help='Image Shift')
    shift.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    shift.add_argument('x', type=int, help='X amount')
    shift.add_argument('y', type=int, help='Y amount')
    shift.add_argument('output', type=str, help='Output directory')

    clean = subparsers.add_parser('clean', help='Image Cosmic Cleaner')
    clean.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    clean.add_argument('output', type=str, help='Output directory')
    clean.add_argument('--sigclip', type=float, default=4.5,
                       help='Laplacian-to-noise limit for cosmic ray detection. Lower values will flag more pixels as '
                            'cosmic rays.')
    clean.add_argument('--sigfrac', type=float, default=0.3,
                       help='Fractional detection limit for neighboring pixels. For cosmic ray neighbor pixels, a '
                            'Laplacian-to-noise detection limit of sigfrac * sigclip will be used.')
    clean.add_argument('--objlim', type=int, default=5,
                       help='Minimum contrast between Laplacian image and the fine structure image. Increase this '
                            'value if cores of bright stars are flagged as cosmic rays.')
    clean.add_argument('--gain', type=float, default=1.0,
                       help='Gain of the image (electrons / ADU). We always need to work in electrons for cosmic ray '
                            'detection.')
    clean.add_argument('--readnoise', type=float, default=6.5,
                       help='Read noise of the image (electrons). Used to generate the noise model of the image.')
    clean.add_argument('--satlevel', type=float, default=65535.0,
                       help='Saturation level of the image (electrons). This value is used to detect saturated stars '
                            'and pixels at or above this level are added to the mask.')
    clean.add_argument('--niter', type=int, default=4,
                       help='Number of iterations of the LA Cosmic algorithm to perform.')
    clean.add_argument('--sepmed', action='store_true', default=True,
                       help='Use the separable median filter instead of the full median filter. The separable median '
                            'is not identical to the full median filter, but they are approximately the same, the '
                            'separable median filter is significantly faster, and still detects cosmic rays well. '
                            'Note, this is a performance feature, and not part of the original L.A. Cosmic.')
    clean.add_argument('--cleantype', type=str, default='meanmask',
                       help='Set which clean algorithm is used. "median": An unmasked 5x5 median filter. "medmask": A '
                            'masked 5x5 median filter. "meanmask": A masked 5x5 mean filter. "idw": A masked 5x5 '
                            'inverse distance weighted interpolation.')
    clean.add_argument('--fsmode', type=str, default='median',
                       help='Method to build the fine structure image. "median": Use the median filter in the '
                            'standard LA Cosmic algorithm. "convolve": Convolve the image with the psf kernel to '
                            'calculate the fine structure image.')
    clean.add_argument('--psfmodel', type=str, default='gauss',
                       help='Model to use to generate the psf kernel if fsmode == ‘convolve’ and psfk is None. '
                            'The current choices are Gaussian and Moffat profiles. "gauss" and "moffat" produce '
                            'circular PSF kernels. The "gaussx" and "gaussy" produce Gaussian kernels in the x '
                            'and y directions respectively.')
    clean.add_argument('--psffwhm', type=float, default=2.5,
                       help='Full Width Half Maximum of the PSF to use to generate the kernel.')
    clean.add_argument('--psfsize', type=int, default=7,
                       help='ize of the kernel to calculate. Returned kernel will have size psfsize x psfsize. '
                            'psfsize should be odd.')
    clean.add_argument('--psfbeta', type=float, default=4.765,
                       help='Moffat beta parameter. Only used if fsmode=="convolve" and psfmodel=="moffat"')
    clean.add_argument('--gain_apply', action='store_true', default=True,
                       help='If True, return gain-corrected data, with correct units, otherwise do not '
                            'gain-correct the data.')

    show = subparsers.add_parser('show', help='Image Show')
    show.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')

    align = subparsers.add_parser('align', help='Image Align')
    align.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    align.add_argument('other', help='Fits or index of the reference')
    align.add_argument('output', type=str, help='Output directory')
    align.add_argument('--max-control-points', type=int, help='Maximum number of control points',
                       default=50)
    align.add_argument('--min-area', type=int, help='Minimum area', default=5)

    p2s = subparsers.add_parser('p2s', help='Pixel to Sky')
    p2s.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    p2s.add_argument('x', type=int, help='X component of coordinate')
    p2s.add_argument('y', type=int, help='Y component of coordinate')

    s2p = subparsers.add_parser('s2p', help='Sky to Pixel')
    s2p.add_argument('file', type=str, help='A file path or pattern (e.g., "*.fits")')
    s2p.add_argument('ra', type=float, help='Right ascension in degrees')
    s2p.add_argument('dec', type=float, help='Declination in degrees')

    map2sky = subparsers.add_parser('map2sky', help='Map to Sky')
    map2sky.add_argument('file', type=str, help='A file path')

    args = parser.parse_args()
    if args.command == "header":
        imhead(args.file)

    elif args.command == "hedit":
        imhedit(args.file, args.key, args.value, args.comment, args.delete, args.value_is_key)

    elif args.command == "arith":
        imarith(args.file, args.operator, args.other, args.output)

    elif args.command == "value":
        imvalue(args.file, args.x, args.y)

    elif args.command == "stat":
        imstat(args.file)

    elif args.command == "bin":
        imbin(args.file, args.x, args.y, args.output)

    elif args.command == "crop":
        imcrop(args.file, args.x, args.y, args.w, args.h, args.output)

    elif args.command == "rotate":
        imrotate(args.file, args.angle, args.degree, args.output)

    elif args.command == "shift":
        imshift(args.file, args.x, args.y, args.output)

    elif args.command == "clean":
        imclean(args.file, args.output, args.sigclip, args.sigfrac, args.objlim, args.gain, args.readnoise,
                args.satlevel, args.niter, args.sepmed, args.cleantype, args.fsmode, args.psfmodel, args.psffwhm,
                args.psfsize, args.psfbeta, args.gain_apply)

    elif args.command == "show":
        imshow(args.file)

    elif args.command == "align":
        imalign(args.file, args.other, args.output, args.max_control_points, args.min_area)

    elif args.command == "p2s":
        imp2s(args.file, args.x, args.y)

    elif args.command == "s2p":
        ims2p(args.file, args.ra, args.dec)

    elif args.command == "map2sky":
        immap2sky(args.file)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
