# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['correlated_ts_ci']
install_requires = \
['arch>=4.16.1,<5.0.0',
 'joblib>=0.17.0',
 'lmfit>=1.0.2,<2.0.0',
 'numpy>=1.2,<2.0']

setup_kwargs = {
    'name': 'correlated-ts-ci',
    'version': '0.1.5',
    'description': 'Estimate confidence intervals in means of correlated time series with a small number of effective samples (like molecular dynamics simulations). If your time series is long enough that the standard error levels off completely as a function of block length, then this method is overkill and simply using a block bootstrap sampling with a sufficiently large block length is probably sufficient.',
    'long_description': "# Correlated timeseries confidence intervals\n\n## Purpose\n\nEstimate confidence intervals in means of correlated time series with a small number of effective samples (like molecular dynamics simulations). If your time series is long enough that the standard error levels off completely as a function of block length, then this method is overkill and simply using a block bootstrap sampling with a sufficiently large block length is probably sufficient.\n\n## Background\n\nThe origin of this method is in the Appendix of [1]. It based on computing standard error as a function of block length, fitting this, then extrapolating to infinite block length. For correlated data, the standard error will increase asymptotically with increasing block length. Some improvements on the original method are implemented here. The first is to give the option to vary the prefactor for the fitted function which can sometimes give a significantly better fit. The second is to give the option to perform stationary block bootstrap sampling for each block size instead of just using a single set of blocks for each block size. This significantly reduces the noise in the data and leads to better fits.\n\n## Installation\n\n```shell\npip install correlated_ts_ci\n```\n\n## Usage\n\n### Command line\n\n```shell\npython -m correlated_ts_ci [-h] [-op OUTPREFIX] [-id INDIR] [-od OUTDIR] [-tu TIME_UNIT] [-eq EQTIME] [-sk SKIP] [-vp] [-sl SIG_LEVEL] [-mb MIN_BLOCKS] [-bsn BLOCK_SIZE_NUMBER] [-cf CUSTOM_FUNC] [-nb NBOOTSTRAP] [-np NPROCS] infile colnum\n```\n\npositional arguments:\n* infile\n  * File with time in the first column and other quantities in subsequent columns.\n* colnum\n  * Column number in the file with the quantity to be analyzed. The first column (time) is numbered 0, so this should be >= 1.\n\noptional arguments:  \n* -h, --help\n  * show this help message and exit\n* -op OUTPREFIX, --outprefix OUTPREFIX\n  * Prefix for output files. Default is the prefix of the input file.\n* -id INDIR, --indir INDIR\n  * Directory input file is located in. Default is current directory.\n* -od OUTDIR, --outdir OUTDIR\n  * Directory to write data to. Default is current directory.\n* -tu TIME_UNIT, --time_unit TIME_UNIT\n  * String to specify time units. 'ns', 'ps', etc. Default is 'ps'.\n* -eq EQTIME, --eqtime EQTIME\n  * Equilibration time in unit of input file. Default is 0.0.\n* -sk SKIP, --skip SKIP\n  * Only use every this many data points from the input file.\n* -vp, --vary_prefac   \n  * Vary the prefactor instead of constraining it to a constant value of 2 times the standard deviation of all data divided by the total time covered by the data. This is a flag.\n* -sl SIG_LEVEL, --sig_level SIG_LEVEL\n  * Significance level for computing confidence intervals. Default is 0.05.\n* -mb MIN_BLOCKS, --min_blocks MIN_BLOCKS\n  * Minimum number of blocks. Default is 30.\n* -bsn BLOCK_SIZE_NUMBER, --block_size_number BLOCK_SIZE_NUMBER\n  * Number of block sizes to consider. Default is 100.\n* -cf CUSTOM_FUNC, --custom_func CUSTOM_FUNC\n  * Custom lambda function taking a single argument. This function contains the definition of the quantities which you wish to obtain the uncertainties for and should return a single value or a numpy row vector. Example -- lambda x: np.hstack((np.mean(x), np.percentile(x, 90))). If not specified, only np.mean is used.\n* -nb NBOOTSTRAP, --nbootstrap NBOOTSTRAP\n  * Number of bootstrap samples. Default is 100.\n* -np NPROCS, --nprocs NPROCS\n  * Number of processors to use for calculation. Default is all available.\n\n#### Example\n\nAnalyze column 1 of the specified file. Use nanoseconds (ns) for the time unit with an equilibration time of 0.5 ns. All other options default.\n\n```shell\npython -m correlated_ts_ci ./velocities/ads_lower_all_velocity.xvg 1 -tu ns -eq 0.5\n```\n\n### Script\n\n```python\nfrom correlated_ts_ci import ConfidenceInterval\n\nget_confidence_interval = ConfidenceInterval(infile, colnum)\nget_confidence_interval(outfile_prefix=OUTPREFIX, eqtime=EQTIME, skip=SKIP,\n                        indir=INDIR, time_unit=TIME_UNIT,\n                        vary_prefactor=VARY_PREFAC, sig_level=SIG_LEVEL,\n                        block_size_number=BLOCK_SIZE_NUMBER, min_blocks=MIN_BLOCKS,\n                        custom_func=CUSTOM_FUNC, nbootstrap=NBOOTSTRAP,\n                        nprocs=NPROCS, outdir=OUTDIR)\n```\n\n## References\n\n(1) Hess, B. Determining the Shear Viscosity of Model Liquids from Molecular Dynamics Simulations. J. Chem. Phys. 2002, 116, 209–217. https://doi.org/10.1063/1.1421362.\n",
    'author': 'Brian Novak',
    'author_email': 'bnovak1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
