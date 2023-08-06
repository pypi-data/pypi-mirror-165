"""
Some basic sanity checks.
"""

import pytest


# Small import test first...
def test_import():
    """Test that the package can be imported."""
    with pytest.raises(NameError):
        qwilprobe
    import qwilprobe
    qwilprobe


# ...then properly import package and run the rest of the sanity tests
import qwilprobe


def test_has_version():
    """Test that the package has a version."""
    qwilprobe.__version__
