# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=unnecessary-comprehension
"""
profile the imported model.
"""
import logging
import os
import json
import sys

import numpy as np

import tvm
from tvm import relay
from tvm.relay.quantize.quantize_hhb import _bind_params

from core.frontend_manage import import_model
from core.common import hhb_register_parse, HHBException, ensure_dir
from core.common import generate_config_file, ALL_ARGUMENTS_DESC, collect_arguments_info
from core.arguments_manage import (
    add_common_argument,
    add_import_argument,
    add_profiler_argument,
    ArgumentFilter,
)
from core.profiler_manage import convert_tvm_trace2python, aitrace_options
from core.profiler_manage import get_cal_total_info, print_cal_total_info
from core.profiler_manage import get_mem_total_info, print_mem_total_info
from core.profiler_manage import profile_light_trace, dump_profile_result


# pylint: disable=invalid-name
logger = logging.getLogger("HHB")


@hhb_register_parse
def add_profiler_parser(subparsers):
    """ Include parser for 'profiler' subcommand """

    parser = subparsers.add_parser("profiler", help="profile model")
    parser.set_defaults(func=driver_profiler)

    add_import_argument(parser)
    add_profiler_argument(parser)
    add_common_argument(parser)

    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    parser.add_argument(
        "-o",
        "--output",
        default="hhb_out",
        help="The directory that holds the result files.",
    )
    parser.add_argument(
        "-f", "--model-file", nargs="+", help="Path to the input model file, can pass multi files"
    )

    ALL_ARGUMENTS_DESC["profiler"] = collect_arguments_info(parser._actions)


def driver_profiler(args_filter: ArgumentFilter):
    """Driver profiler command"""
    args = args_filter.filtered_args
    args.output = ensure_dir(args.output)

    if args.generate_config:
        generate_config_file(os.path.join(args.output, "cmd_profiler_params.yml"))

    if args.ir_type == "relay":
        # relay ir should do InferType pass before profiling
        from tvm.relay import transform as _transform
        from tvm.ir import transform

        mod, params = import_model(
            args.model_file, args.model_format, args.input_name, args.input_shape, args.output_name
        )

        if "binary" not in args.output_type and "all" not in args.output_type:
            options = aitrace_options(args.indicator, "")
        else:
            options = aitrace_options(args.indicator, os.path.join(args.output, "model.aitrace"))
        logger.debug('profile model with: "%s"', str(options))

        if params:
            mod["main"] = _bind_params(mod["main"], params)
            params = None

        opt_seq = [
            _transform.SimplifyInference(),
            _transform.DynamicToStatic(),
            _transform.FoldConstant(),
            _transform.SimplifyExpr(),
            _transform.InferType(),
        ]
        mod = transform.Sequential(opt_seq, opt_level=3)(mod)

        result = relay.analysis.get_aitrace_data(mod["main"], options)
        result = convert_tvm_trace2python(result)

        dump_profile_result(result, args.output_type, args.indicator, args.ir_type, args.output)
    elif args.ir_type == "light":
        if "cal" in args.indicator:
            logger.error("Unsupport 'cal' for indicator while setting --ir-type light.")
            sys.exit()
        if "binary" in args.output_type:
            logger.error("Unsupport 'binary' for --output-type while setting --ir-type light.")
            sys.exit()
        if not args.model_file or not os.path.exists(args.model_file[0]):
            logger.error("File not exits: %s" % args.model_file[0])
            sys.exit()
        try:
            with open(args.model_file[0], "r") as f:
                trace_data = json.load(f)
        except:
            logger.error("Invalid file for light profiling: %s." % args.model_file)
            sys.exit()

        result = profile_light_trace(trace_data, args.indicator, args.npu_frequency)
        dump_profile_result(result, args.output_type, args.indicator, args.ir_type, args.output)
    else:
        raise HHBException("Unsupport for profiling type: {}\n".format(args.ir_type))
