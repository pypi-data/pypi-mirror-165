# Python package initialization file.

'''
STEMDIFF package
----------------
Conversion of 4D-STEM dataset to single 2D-powder diffration pattern.

* 4D-STEM dataset
    - A set of datafiles from 2D-array STEM detector (aka pixelated detector).
    - Each datafile is a monocrystalline-like nanobeam diffraction pattern.
* STEMDIFF processing of 4D-STEM dataset
    - The 4D-STEM dataset is huge, complex, and hard to process...
    - STEMDIFF reduces the 4D-dataset to 2D powder diffraction patern.
    - The 2D difractogram is then readily converted to a 1D diffractogram.
    - Both 2D and 1D powder diffraction patterns are quite easy to process.
    - This is called **4D-STEM/PNBD method**:
      <https://doi.org/10.3390/ma14247550>

Typical usage of STEMDIFF package is shown in the code block below.

* The code may look complex at first sight...
* but it is quite simple, well-commented, and universal template...
* which can be used (with minor modifications) to arbitrary 4D-STEM dataset.
    
>>> # STEMDIFF = convert a 4D-STEM datacube to a powder electron diffractogram
>>> # Usage: edit input parameters in section [0] and run the script
>>> # Help (in Spyder): place cursor on a keyword below and press Ctrl+I
>>> 
>>> from pathlib import Path
>>> import stemdiff.const, stemdiff.io
>>> import stemdiff.dbase, stemdiff.psf, stemdiff.sum, stemdiff.radial
>>> 
>>> print('[0] Define parameters')
>>> # Data directory and datafiles (this must be adjusted)
>>> DATAFILES = Path(r'../DATA').glob('*.dat')
>>> # Calculation parameters (arguments can be adjusted/optimized)
>>> CENTERING = stemdiff.const.centering(ctype=1, csquare=30, cintensity=0.8)
>>> SUMMATION = stemdiff.const.summation(psfsize=130, imgsize=125, iterate=10)
>>> # Basic output files (other outputs are specified in the functions below)
>>> DBASE = '1_database.zip'
>>> PSF   = '2_psf.npy'
>>> 
>>> print('[1] Prepare database')
>>> df = stemdiff.dbase.calc_database(DATAFILES,CENTERING)
>>> stemdiff.dbase.plot_entropy_histogram(df, bins=100)
>>> stemdiff.dbase.save_database(df, output_file = DBASE)
>>> 
>>> print('[2] Calculate 2D-PSF = point spread function')
>>> psf = stemdiff.psf.psf_from_lowS_files(DBASE,SUMMATION, P=5)
>>> stemdiff.psf.plot_psf(psf, plt_type='3D', plt_size=40)
>>> stemdiff.psf.save_psf(psf, output_file = PSF)
>>> 
>>> print('[3a] Sum all files')
>>> arr1 = stemdiff.sum.sum_all(DBASE,SUMMATION)
>>> stemdiff.sum.save_results(arr1, icut=300, itype='8bit', output='3_sum_all')
>>> print('[3b] Sum high entropy files')
>>> arr2 = stemdiff.sum.sum_highS(DBASE,SUMMATION, P=20)
>>> stemdiff.sum.save_results(arr2, icut=300, itype='8bit', output='3_sum_hs')
>>> print('[3c] Sum high entropy files with deconvolution')
>>> arr3 = stemdiff.sum.sum_highS_deconv(DBASE,SUMMATION,PSF, P=20)
>>> stemdiff.sum.save_results(arr3, icut=300, itype='8bit', output='3_sum_hsd')
>>> 
>>> print('[4] Plot radial distributions')
>>> stemdiff.radial.plot_radial_distributions([
>>>     ['3_sum_all.txt', 'k:',  'All data'],
>>>     ['3_sum_hs.txt',  'b--', 'S-filtering'],
>>>     ['3_sum_hsd.txt', 'r-',  'S-filtering + deconv']],
>>>     xlimit=250, ylimit=300, output='4_radial_dist.png')

'''
__version__ = "4.2.11"
