"""
Test setting probe info.
"""

import pytest

from qwilprobe.service.api import (
    DATATYPE_INTEGER,
    DATATYPE_REAL,
    DATATYPE_STRING,
    qwilprobe_set_probe_info
)

good_datatype_paramlist = [
    DATATYPE_INTEGER,
    DATATYPE_REAL,
    DATATYPE_STRING]

good_column_key_paramlist = [
    "col1",
    "col2",
]

good_column_val_paramlist = [
    (DATATYPE_INTEGER, ),
    (DATATYPE_REAL, "column description"),
    DATATYPE_STRING,
    (DATATYPE_STRING, ""),
    (DATATYPE_REAL, None)
]

bad_uid_paramlist = [
    "",  # May not be the empty string
    3129,  # Wrong type
    None,  # Must be set
    False,  # Also wrong type
    {"colname": 0}  # Some more wrong type
]

bad_column_info_paramlist = [
    {},  # May not be empty
    None,  # Must be set
    (1, 2, 3),  # Must be a dict
]

bad_column_key_paramlist = [
    "",  # May not be the empty string
    1,  # Must be a string
    (1, 2, 3),
    None  # Must be set
]

bad_column_val_paramlist = [
    "bad val!",  # Val must be tuple or int
    (False, "descr"),  # First element must be int
    (300000, "descr"),  # First element must be within enum range
]

bad_description_paramlist = [
    (1, 2, 3),  # Wrong type
    1234,  # Also wrong type
]


@pytest.mark.parametrize("datatype", good_datatype_paramlist)
def test_set_probe_info_basic(datatype):
    """Test setting minimal probe info."""
    qwilprobe_set_probe_info("dummy_uid", {"colname": datatype})


@pytest.mark.parametrize("datatype", good_datatype_paramlist)
def test_set_probe_info_basic_onetuple(datatype):
    """Test setting minimal probe info with a 1-tuple."""
    qwilprobe_set_probe_info("dummy_uid", {"colname": (datatype,)})


@pytest.mark.parametrize("datatype", good_datatype_paramlist)
def test_set_probe_info_basic_with_descr(datatype):
    """Test setting minimal probe info with a 2-tuple."""
    qwilprobe_set_probe_info("dummy_uid", {"colname": (datatype, "lalalala")})


@pytest.mark.parametrize("uid", bad_uid_paramlist)
@pytest.mark.parametrize("datatype", good_datatype_paramlist)
def test_set_probe_info_bad_uid(uid, datatype):
    """Test that the proper error is raised when uid is bad."""
    with pytest.raises(ValueError):
        qwilprobe_set_probe_info(uid, {"colname": datatype})


@pytest.mark.parametrize("column_info", bad_column_info_paramlist)
def test_set_probe_info_bad_column_info(column_info):
    """Test that the proper exception is raised when column info is bad."""
    with pytest.raises(ValueError):
        qwilprobe_set_probe_info("dummy_uid", column_info)


@pytest.mark.parametrize("key", bad_column_key_paramlist)
@pytest.mark.parametrize("val", good_column_val_paramlist)
def test_set_probe_info_bad_column_keys(key, val):
    """
    Test that the proper exception is raised when keys are bad.
    """
    with pytest.raises(ValueError):
        qwilprobe_set_probe_info("dummy_uid", {key: val})


@pytest.mark.parametrize("key", good_column_key_paramlist)
@pytest.mark.parametrize("val", bad_column_val_paramlist)
def test_set_probe_info_bad_column_vals(key, val):
    """
    Test that the proper exception is raised when vals are bad.
    """
    with pytest.raises(ValueError):
        qwilprobe_set_probe_info("dummy_uid", {key: val})


@pytest.mark.parametrize("datatype", good_datatype_paramlist)
@pytest.mark.parametrize("description", bad_description_paramlist)
def test_set_probe_info_bad_column_description(datatype, description):
    """
    Test that the proper exception is raised when probe description is bad.
    """
    with pytest.raises(ValueError):
        qwilprobe_set_probe_info("dummy_uid",
                                 {"colname": (datatype, description)})
