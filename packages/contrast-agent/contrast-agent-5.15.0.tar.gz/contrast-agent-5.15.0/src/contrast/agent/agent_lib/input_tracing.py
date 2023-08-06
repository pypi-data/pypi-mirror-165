# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import ctypes
from enum import IntEnum

from contrast.agent import agent_lib
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


__all__ = [
    "evaluate_header_input",
    "evaluate_input_by_type",
    "initialize_input_tracing",
    "InputType",
]


# These are rules we do not have an implementation for yet
# Other rule IDs where added directly into the protect rule class
SSJS_INJECTION_RULE_ID = 1 << 7


class InputType(IntEnum):
    COOKIE_NAME = 1
    COOKIE_VALUE = 2
    HEADER_KEY = 3
    HEADER_VALUE = 4
    JSON_KEY = 5
    JSON_VALUE = 6
    METHOD = 7
    PARAMETER_KEY = 8
    PARAMETER_VALUE = 9
    URI_PATH = 10
    URL_PARAMETER = 11
    MULTIPART_NAME = 12
    XML_VALUE = 13


class BodyType(IntEnum):
    JSON = 1
    XML = 2


class CEvalResults(ctypes.Structure):
    _fields_ = [
        ("rule_id", ctypes.c_ulonglong),
        ("input_type", ctypes.c_ulonglong),
        ("score", ctypes.c_double),
    ]


class InputAnalysisResult:
    def __init__(self, input_value, value, ceval_results):
        self.rule_id = None
        self.input_type = None
        self.score = None
        self.name = None
        self.value = None

        if (
            isinstance(ceval_results, CEvalResults)
            and input_value is not None
            and isinstance(value, str)
        ):
            self.rule_id = ceval_results.rule_id
            self.input_type = ceval_results.input_type
            self.score = ceval_results.score
            self.name = input_value
            self.value = value


def initialize_input_tracing():
    # This function is necessary for now because we have to conditionally import agent_lib.LIB_CONTRAST
    # When we get to the point where we always use agent lib we would define this outside of a function
    if agent_lib.LIB_CONTRAST is None:
        return

    agent_lib.LIB_CONTRAST.evaluate_header_input.argtypes = (
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_longlong,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(ctypes.POINTER(CEvalResults)),
    )

    agent_lib.LIB_CONTRAST.evaluate_header_input.restype = ctypes.c_int


def evaluate_header_input(header_name, header_value, rules, worth_watching):
    evaluations = []

    if agent_lib.LIB_CONTRAST is None:
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    name = ctypes.c_char_p(bytes(header_name, "utf8"))
    value = ctypes.c_char_p(bytes(header_value, "utf8"))
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(CEvalResults)()

    ret = agent_lib.call(
        agent_lib.LIB_CONTRAST.evaluate_header_input,
        is_valid_return,
        name,
        value,
        rules,
        worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_space(
        ret,
        results,
        results_len,
        header_name,
        header_value,
        is_valid_return,
        evaluations,
    )
    return evaluations


def evaluate_input_by_type(input_type, input_value, rules, worth_watching):
    evaluations = []

    if agent_lib.LIB_CONTRAST is None:
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    name = ctypes.c_char_p(bytes(input_value, "utf8"))
    value = ctypes.c_long(input_type)
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(CEvalResults)()

    ret = agent_lib.call(
        agent_lib.LIB_CONTRAST.evaluate_input,
        is_valid_return,
        name,
        value,
        rules,
        worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_space(
        ret, results, results_len, name, input_value, is_valid_return, evaluations
    )
    return evaluations


def map_result_and_free_space(
    ret, results, results_len, name, value, is_valid_return, evaluations
):
    if ret == 0 and bool(results) and results_len.value > 0:
        for i in range(results_len.value):
            evaluations.append(InputAnalysisResult(name, value, results[i]))

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            agent_lib.LIB_CONTRAST.free_eval_result,
            is_valid_return,
            results,
        )
