'''
stemdiff.const
--------------
Constants for package stemdiff.
'''

# Key constants
# (these costants are not expected to change for given microscope
# (they can be adjusted if the program is used for a different microscope

DET_SIZE = 256
'''DET_SIZE = size of pixelated detector (in pixels :-)'''

RESCALE  = 4
'''RESCALE = scaling coefficient: final image size = DET_SIZE * RESCALE'''

# Additional settings
# (these settings/objects must be adjusted acc. to experimental conditions
# (typically, the objects are defined at the beginning of the master script
# centering = parameters for the determination of the center of 4D-STEM images
# summation = parameters for the summation of 2D-STEM images

class centering:
    '''
    Set parameters for determination of center of 4D-STEM datafiles.
    
    Parameters
    ----------
    ctype : integer, values = 0,1,2
        * 0 = intensity center not determined, geometrical center is used
        * 1 = center determined from the first image and kept constant
        * 2 = center is determined for each individual image
    csquare : integer, interval = 10--DET_SIZE
        Size of the central square (in pixels),
        within which the center of intensity is searched for.
    cintensity : float, interval = 0--1
        Intensity fraction, which is used for center determination.
        Example: cintensity=0.9 => take only pixels > 0.9 * max.intensity.

    Returns
    -------
    Centering object

    Notes
    -----
    * Typical values of the arguments
        * `ctype=1` ..fixed center, determined from the 1st file
        * `csquare=50` ..find center in a central square with size 50 pixels 
        * `cintensity=0.8` ..ignore intensities < 0.8 * maximal intensity
    * Typical usage of the class
        * The centering parameters are saved in variable CENTERING.
        * The CENTERING variable is an argument of the following functions.
        * See the code in the description of the whole stemdiff package.
    '''
    
    def __init__(self, ctype=1, csquare=None, cintensity=None):
        '''
        Initialize parameters for center determination.
        The parameters are described above in class definition.
        '''
        self.ctype = ctype
        self.csquare = csquare
        self.cintensity = cintensity
        
class summation:
    '''
    Set parameters for summation of 4D-STEM datafiles.
    
    Parameters
    ----------
    psfize : integer, smaller than DET_SIZE
        Size/edge of central square, from which 2D-PSF is determined.
    imgsize : integer, smaller than DET_SIZE
        Size of array read from the detector is reduced to imgsize.
        If given, we sum only the central square with size = imgsize.
        Smaller area = higher speed;
        outer area = just weak diffractions.   
    iterate : integer  
        Number of iterations during PSF deconvolution.

    Returns
    -------
    Summation object
    
    Notes
    -----
    * Typical values of the parameters
        * `psfsize=130` ..size of a central square for PSF determination
            * (psfsize > imgsize) => minimization of deconvolution artifacts
        * `imgsize=125` ..size of a central square for summation
            * (imgsize < DET_SIZE) => ignore weak diffraction at the edges
        * `iterate=30`  ..number of iterations during deconvolution
            * (iterate=30) => good start; final number is usually higher
    * Typical usage of the class
        * The summation parameters are saved in variable SUMMATION.
        * The SUMMATION variable is an argument of the following functions.
        * See the code in the description of the whole stemdiff package.
    '''

    def __init__(self, psfsize=None, imgsize=None, iterate=None):
        '''
        Initialize parameters for center determination.
        The parameters are described above in class definition.
        '''
        self.psfsize = psfsize
        self.imgsize = imgsize
        self.iterate = iterate
