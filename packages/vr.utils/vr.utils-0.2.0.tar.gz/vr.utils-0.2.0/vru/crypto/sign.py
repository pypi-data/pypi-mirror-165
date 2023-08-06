#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# Classes for security

import os
from hashlib import blake2b
import base64
from hmac import compare_digest

SECRET_KEY = os.environ.get("SECRET_KEY",
                            "pseudo randomly generated server secret key")


def sign(data: str):
    h = blake2b(digest_size=32, key=SECRET_KEY.encode("UTF-8"))
    h.update(data.encode("UTF-8"))
    return base64.b64encode(h.hexdigest().encode("UTF-8")).decode("UTF-8")


def verify(data: str, sig: str):
    good_sig = base64.b64decode(sign(data))
    return compare_digest(good_sig, base64.b64decode(sig))
