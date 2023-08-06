from setuptools import setup, find_packages

VERSION = '0.4.6' 
DESCRIPTION = 'Cluster sequences by distance one.'
LONG_DESCRIPTION = 'Cluster sequences based on edit distance (hamming/levenshtein) equal to one.'
REQUIREMENTS = ["more_itertools", "findspark", "pyspark", "scipy", "numpy"],
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="SwifTCR", 
        version=VERSION,
        author="ido",
        author_email="ido.hasson.5@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=REQUIREMENTS,
        keywords=['cluster', 'TCR', 'edit', 'distance'],
)