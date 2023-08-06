from setuptools import setup, find_packages

VERSION = '0.4.7' 
DESCRIPTION = 'Cluster sequences by distance one.'
LONG_DESCRIPTION = 'Cluster sequences based on edit distance (hamming/levenshtein) equal to one.'
REQUIREMENTS = ["findspark", "pyspark", "scipy", "numpy", "pandas"],

setup(
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