"""
Various utilities for internal use.
"""

from qwilprobe.generated.qwilprobe_pb2 import (
    ProbeDataType,
    ProbeInfoResponse,
    ProbeDatapoint,
    ProbeDataResponse
)


def check_column_info(column_info):
    if not isinstance(column_info, dict):
        return False  # Column must be a dict

    if not column_info:
        return False  # Empty dict not allowed

    for k, v in column_info.items():
        if not _check_column_info_elem(k, v):
            return False

    return True


def convert_probe_data(data, probe_info_response=None):
    """
    Convert a dict to a ProbeDataResponse. If a ProbeInfoResponse is supplied,
    it will make sure the data adheres to the model within.
    """
    if (probe_info_response and
       isinstance(probe_info_response, ProbeInfoResponse)):
        model = {c.column_name: c.column_type
                 for c in probe_info_response.data_model.columns}

        datapoints = []
        for k, v in data.items():
            if k not in model.keys():
                return False, None

            datapoint = ProbeDatapoint(key=k)

            if model[k] == ProbeDataType.INTEGER:
                try:
                    datapoint.intval = v
                except Exception:
                    return False, None
            elif model[k] == ProbeDataType.REAL:
                try:
                    datapoint.realval = v
                except Exception:
                    return False, None
            elif model[k] == ProbeDataType.STRING:
                try:
                    datapoint.stringval = v
                except Exception:
                    return False, None
            else:
                return False, None

            datapoints.append(datapoint)

        response = ProbeDataResponse(probe_data=datapoints)

    else:  # No probe info given. Attempt to build a ProbeDataResponse anyway
        datapoints = []
        for k, v in data.items():
            if not isinstance(k, str):
                return False, None

            datapoint = ProbeDatapoint(key=k)

            if isinstance(v, int):
                datapoint.intval = v
            elif isinstance(v, float):
                datapoint.realval = v
            elif isinstance(v, str):
                datapoint.stringval = v
            else:
                return False, None

            datapoints.append(datapoint)

        response = ProbeDataResponse(probe_data=datapoints)

    return True, response


def _check_column_info_elem(key, value):
    if not isinstance(key, str):
        return False  # Key (i.e. column name) must be a string

    if not key:
        return False  # Key must be non-empty string

    if isinstance(value, tuple):
        if len(value) == 1:
            datatype = value[0]
            description = None
        elif len(value) == 2:
            datatype = value[0]
            description = value[1]
        else:
            return False
    elif isinstance(value, int):
        datatype = value
        description = None
    else:
        return False

    # Don't allow sneaky bools to masquerade as ints
    if isinstance(datatype, bool):
        return False

    try:
        # Attempt to access name of enum elem in qwilbrobe.proto by given info.
        ProbeDataType.Name(datatype)
    except (ValueError, TypeError):
        # Fails if given info is not an integer within the enum range
        return False

    # Check that the comment is a string, if present
    if description:
        if not isinstance(description, str):
            return False

    return True
