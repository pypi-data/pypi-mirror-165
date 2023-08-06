"""
Test starting a qwilprobe microservice
"""

import threading

import pytest

from qwilprobe.service.api import qwilprobe_start, qwilprobe_stop


@pytest.fixture
def stop_after_timeout(request):
    stop_thread = threading.Timer(request.param, qwilprobe_stop)
    stop_thread.start()


@pytest.mark.parametrize("stop_after_timeout", [3.0], indirect=True)
def test_start_microservice_nosetup(stop_after_timeout):
    """Test starting/stopping the microservice without any setup."""
    qwilprobe_start()
