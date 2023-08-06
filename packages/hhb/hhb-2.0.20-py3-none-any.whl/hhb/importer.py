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
"""
Import networks into relay IR.
"""
import logging
import os

from core.common import hhb_register_parse
from core.common import ensure_dir
from core.common import generate_config_file
from core.common import ALL_ARGUMENTS_DESC
from core.common import collect_arguments_info
from core.arguments_manage import add_import_argument
from core.arguments_manage import add_optimize_argument
from core.arguments_manage import add_common_argument
from core.frontend_manage import import_model
from core.hhbir_manage import HHBRelayIR


# pylint: disable=invalid-name
logger = logging.getLogger("HHB")


@hhb_register_parse
def add_import_parser(subparsers):
    """ Include parser for 'import' subcommand """

    parser = subparsers.add_parser("import", help="Import a model into relay ir")
    parser.set_defaults(func=driver_import)

    add_import_argument(parser)
    # add_optimize_argument(parser)
    add_common_argument(parser)

    parser.add_argument(
        "-o",
        "--output",
        metavar="",
        default="hhb_out",
        help="The directory that holds the relay ir.",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    parser.add_argument(
        "FILE", nargs="+", help="Path to the input model file, can pass multi files"
    )

    ALL_ARGUMENTS_DESC["import"] = collect_arguments_info(parser._actions)


def driver_import(args_filter):
    """Driver import command"""
    args = args_filter.filtered_args
    mod, params = import_model(
        args.FILE,
        args.model_format,
        args.input_name,
        args.input_shape,
        args.output_name,
    )

    relay_ir = HHBRelayIR()
    relay_ir.set_model(mod, params)
    args.output = ensure_dir(args.output)

    if args.generate_config:
        generate_config_file(os.path.join(args.output, "cmd_import_params.yml"))

    relay_ir.save_model(args.output)
    # if args.opt_level != -1:
    #     target = get_target(args.board)
    #     with tvm.transform.PassContext(opt_level=args.opt_level):
    #         mod, params = relay.optimize(mod, target=target, params=params)

    return 0
