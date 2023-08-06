"""
API for writing probes for the qwilfish fuzzer.
"""

import qwilprobe.service.microservice as qpms
import qwilprobe.service.util as util
from qwilprobe.generated.qwilprobe_pb2 import ProbeDataType

#: Pass to :func:`qwilprobe_register_handler` to register handler for this RPC
RPC_GET_PROBE_INFO = "GetProbeInfo"
#: Pass to :func:`qwilprobe_register_handler` to register handler for this RPC
RPC_GET_PROBE_IS_READY = "GetProbeIsReady"
#: Pass to :func:`qwilprobe_register_handler` to register handler for this RPC
RPC_GET_PROBE_DATA = "GetProbeData"
#: Pass to :func:`qwilprobe_register_handler` to register handler for this RPC
RPC_TERMINATE = "Terminate"

#: Used to indicate the datatype of a column in
#: :func:`qwilprobe_set_probe_info`
DATATYPE_INTEGER = ProbeDataType.INTEGER
#: Used to indicate the datatype of a column in
#: :func:`qwilprobe_set_probe_info`
DATATYPE_REAL = ProbeDataType.REAL
#: Used to indicate the datatype of a column in
#: :func:`qwilprobe_set_probe_info`
DATATYPE_STRING = ProbeDataType.STRING


def qwilprobe_register_handler(rpc_name, handler):
    """
    Register a handler for various RPCs.

    :param str rpc_name: Required. RPC name to register a handler for.
        Use :const:`RPC_GET_PROBE_INFO`, :const:`RPC_GET_PROBE_IS_READY`,
        :const:`RPC_GET_PROBE_DATA` or :const:`RPC_TERMINATE` for convenience.
    :param handler: Required. Handler function for the specified RPC. Depending
        on ``rpc_name``, the handler is expected to behave differently:

        - For :const:`RPC_GET_PROBE_INFO` the handler should take no input
          parameters and return a tuple on the form:

          :obj:`(uid, column_info[, description])<tuple>`.

          See the parameters for :func:`qwilprobe_set_probe_info` for details.

          Default handler will return whatever has been set with
          :func:`qwilprobe_set_probe_info` or raise an exception on the client
          side if nothing has been set.

        - For :const:`RPC_GET_PROBE_IS_READY` the handler should take no input
          parameters and return a :obj:`bool`.

          Default handler will always return :obj:`True <bool>`.

        - For :const:`RPC_GET_PROBE_DATA` the handler should take no input
          parameters and return a :obj:`dict` with column names for keys and
          probe data as values. If probe info has been set using
          :func:`qwilprobe_set_probe_info` the returned :obj:`dict` will be
          checked for correctness (e.g. no undefined column names or type
          mismatches).

          Default handler will raise an exception on the client side.

        - For :const:`RPC_TERMINATE` the handler should take no input
          parameters and return nothing. The main idea is to use it for cleanup
          before shutting down.

          Default handler does nothing.

          `The handler being registered does not need to care about the actual
          shutting down of the service, that will happen regardless`.

    :raise ValueError: If handler is not a callable or if an invalid RPC name
        is supplied.
    :return: None
    """
    if not callable(handler):
        raise ValueError(f"Handler {handler} is not callable!")

    if rpc_name == RPC_GET_PROBE_INFO:
        qpms.register_get_probe_info_handler(handler)
    elif rpc_name == RPC_GET_PROBE_IS_READY:
        qpms.register_get_probe_is_ready_handler(handler)
    elif rpc_name == RPC_GET_PROBE_DATA:
        qpms.register_get_probe_data_handler(handler)
    elif rpc_name == RPC_TERMINATE:
        qpms.register_terminate_handler(handler)
    else:
        raise ValueError(f"No RPC named '{rpc_name}'. Handler not registered.")


def qwilprobe_set_probe_info(uid, column_info, description=None):
    if not isinstance(uid, str):
        raise ValueError("Probe UID must be a string!")

    if not uid:
        raise ValueError("Probe UID must be a non-empty string!")

    if description:
        if not isinstance(description, str):
            raise ValueError("Make sure probe description is a string!")

    if not util.check_column_info(column_info):
        raise ValueError("Bad column info provided!")

    qpms.set_probe_info(uid, column_info, description)


def qwilprobe_start(address="localhost", port=30051):
    qpms.start(address, port)


def qwilprobe_stop():
    qpms.stop()
