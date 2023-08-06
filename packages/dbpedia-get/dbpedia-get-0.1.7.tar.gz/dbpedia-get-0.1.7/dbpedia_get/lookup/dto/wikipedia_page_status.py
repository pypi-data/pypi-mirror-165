#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from enum import Enum


class WikipediaPageStatus(Enum):
    PASS = 100
    FROM_CACHE = 110
    FAIL_INVALID_INPUT = 400
    FAIL_PAGE_ERROR = 410
    FAIL_KEY_ERROR = 420
    FAIL_DISAMBIGUATION_ERROR = 430
    FAIL_WIKIPEDIA_ERROR = 440
    FAIL_OS_ERROR = 450
    FAIL_TRANSFORM = 460
    FAIL_OTHER = 500
