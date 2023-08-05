STEMDIFF :: Simple processing of 4D-STEM data
---------------------------------------------

* The **STEMDIFF package** converts... <br>
  ... a 4D-STEM dataset from a SEM microscope (huge and complex) <br>
  ... to a single powder diffraction pattern (simple and easy to work with).
* The STEMDIFF package is a key part of our **4D-STEM/PNBD** method, <br>
  which was described (together with the package) in open-access publications:
	1. *Nanomaterials* 11 (2021) 962.
	   [https://doi.org/10.3390/nano11040962](https://doi.org/10.3390/nano11040962)
	2. *Materials* 14 (2021) 7550.
       [https://doi.org/10.3390/ma14247550](https://doi.org/10.3390/ma14247550)
* If you use STEMDIFF package, **please cite** the 2nd publication (or both :-).

Principle
---------

<img src="https://mirekslouf.github.io/stemdiff/images/principle2.png" alt="STEMDIFF principle" width="500"/>

Quick start
-----------

* Install stemdiff: `pip install stemdiff`
* Download a [demo dataset](https://www.dropbox.com/s/sfqlrzrlexi9i35/STEMDIFF.RUN.SIMPLE.zip?dl=0)
  and follow the instructions in *readme* file.
* Basically, you just run the master script in Spyder like in this
  [printscreen](https://mirekslouf.github.io/stemdiff/images/stemdiff_prtscr.png).

Documentation, help and examples
--------------------------------

More detailed help, demo and source code including documentation are in
[GitHub](https://mirekslouf.github.io/stemdiff).

## Versions of STEMDIFF

* Version 1.0 = Matlab: just simple summation of 4D-dataset
* Version 2.0 = like v1.0 + post-processing in Jupyter
* Version 3.0 = Python scripts: summation + S-filtering
* Version 4.0 = Python package: summation + S-filtering + deconvolution
	* summation = summation of all 2D-diffractograms
	* S-filtering = sum only diffractograms with strong diffractions = high S
	* deconvolution = reduce the effect of primary beam spread
	  &rArr; better resolution 
* Version 4.2 = like v4.0 + a few important improvements, such as:
	* sum just the central region with the strongest diffractions
	  &rArr; higher speed
	* 3 centering types: (0) geometry, (1) weight of 1st, (2) individual weights 
	* better definition of summation and centering parameters
	* better documentation strings + demo data + improved *master script*