# -*- coding: utf-8 -*-
from __future__ import annotations

import time

from msgspec.json import encode
from pioreactor.background_jobs.led_control import LEDController
from pioreactor.utils import local_intermittent_storage
from pioreactor.utils import local_persistant_storage
from pioreactor.utils.timing import current_utc_timestamp
from pioreactor.whoami import get_unit_name

from .relay import Relay

def test_relay_runs() -> None:
    rl = Relay.set_on()
    assert 
    rl.clean_up()

