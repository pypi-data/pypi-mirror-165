"""
Validate the length and format of the version string.
"""

import sodapy


def test_version():
    version = sodapy.__version__
    components = version.split(".")
    assert len(components) == 3
    for component in components:
        assert component.isnumeric()
