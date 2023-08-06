#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# Monitoring of various parameters

import humanize
import os
import psutil
import time


# =============================================================================
# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


# =============================================================================
def process_memory_humanize():
    return humanize.naturalsize(process_memory())


# =============================================================================
# decorator function
def profile(func):
    def wrapper(*args, **kwargs):

        time_before = time.perf_counter()
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        time_after = time.perf_counter()
        print(f"{func.__name__}: consumed memory: "
              f"{humanize.naturalsize(mem_before)}, "
              f"{humanize.naturalsize(mem_after)}, "
              f"{humanize.naturalsize(mem_after - mem_before)}; "
              f"time (sec): {time_after-time_before:.3f}")

        return result
    return wrapper
