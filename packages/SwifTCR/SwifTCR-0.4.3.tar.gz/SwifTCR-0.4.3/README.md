# SwiftTCR: A Quick-and-Simple Way to Discover T Cell Repertoire Patterns
SwifTCR is a Python package provides a relatively quick way to find all sequences with shared single-only-replacement, only-deletion or both, creating clusters of CDR3s highly similar and construct a network graph. The tool, designed to enable researchers to quickly identify clusters in a relatively small data-set, is also available for large-scale data collection thanks its implementation of Spark, making it available for big-data immunological analysis.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

``` bash
pip install swiftcr
```

## Usage/Examples

to create a networkX graph:

``` python
from SwifTCR import cluster
data = ["ABC", "AXC", "AC", "XBC"]
clusters_found = cluster(data, deletion=True)
print(clusters_found)
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

