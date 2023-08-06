# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.agent_lib.main import call, initialize
from contrast.agent.agent_lib.semantic_analysis import get_index_of_chained_cmd
from contrast.agent.agent_lib.semantic_analysis import does_file_path_bypass_security
from contrast.agent.agent_lib.semantic_analysis import initialize_semantic_analysis
from contrast.agent.agent_lib.semantic_analysis import (
    does_command_contain_dangerous_path,
)
from contrast.agent.agent_lib.input_tracing import (
    evaluate_header_input,
    evaluate_input_by_type,
    initialize_input_tracing,
    InputType,
)


# For now we just store the reference to the c library here. This file will be
# update to include all initialization of agent lib once SR is completely removed
LIB_CONTRAST = None
