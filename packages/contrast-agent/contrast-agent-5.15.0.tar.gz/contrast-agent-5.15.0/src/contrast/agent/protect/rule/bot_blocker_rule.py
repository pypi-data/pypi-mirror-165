# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.base_rule import BaseRule


class BotBlocker(BaseRule):

    BITMASK_VALUE = 1 << 6
    RULE_NAME = "bot-blocker"
