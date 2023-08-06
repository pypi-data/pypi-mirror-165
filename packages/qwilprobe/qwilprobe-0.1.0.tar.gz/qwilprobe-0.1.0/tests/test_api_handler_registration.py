"""
Test registering handlers for a qwilprobe microservice.
"""

import pytest

from qwilprobe.service.api import (
    RPC_GET_PROBE_DATA,
    RPC_GET_PROBE_INFO,
    RPC_GET_PROBE_IS_READY,
    RPC_TERMINATE,
    qwilprobe_register_handler,
)

rpc_param_list = [RPC_GET_PROBE_INFO,
                  RPC_GET_PROBE_IS_READY,
                  RPC_GET_PROBE_DATA,
                  RPC_TERMINATE]


def dummy_handler():
    """Dummy handler that does nothing."""
    pass


@pytest.mark.parametrize("rpc_name", rpc_param_list)
def test_register_probe_handler(rpc_name):
    """Register a handler for all available RPCs."""
    qwilprobe_register_handler(rpc_name, dummy_handler)


@pytest.mark.parametrize("rpc_name", rpc_param_list)
def test_register_probe_handler_bad(rpc_name):
    """Register a bad handler for all available RPCs."""
    with pytest.raises(ValueError):
        qwilprobe_register_handler(rpc_name, None)
