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
Optimize the imported model.
"""
import logging
import os

from core.common import (
    hhb_register_parse,
    HHBException,
    AttributeDict,
    ensure_dir,
    generate_config_file,
    ALL_ARGUMENTS_DESC,
    collect_arguments_info,
)
from core.arguments_manage import (
    add_preprocess_argument,
    add_quantize_argument,
    add_hardware_argument,
    add_codegen_argument,
    add_common_argument,
    add_optimize_argument,
    ArgumentFilter,
)
from core.hhbir_manage import (
    HHBRelayIR,
    HHBQNNIR,
    get_input_info_from_relay,
    get_output_info_from_relay,
)
from core.quantization_manage import (
    collect_quantization_config,
    set_quantize_params_by_board,
    get_config_dict,
)
from core.codegen_manage import (
    collect_codegen_config,
    set_codegen_config,
)
from core.preprocess_manage import collect_preprocess_config, set_preprocess_params, DatasetLoader


# pylint: disable=invalid-name
logger = logging.getLogger("HHB")


@hhb_register_parse
def add_quantize_parser(subparsers):
    """ Include parser for 'quantize' subcommand """

    parser = subparsers.add_parser("quantize", help="Quantize the imported model")
    parser.set_defaults(func=driver_quantize)

    add_preprocess_argument(parser)
    add_quantize_argument(parser)
    add_hardware_argument(parser)
    add_optimize_argument(parser)
    add_codegen_argument(parser)
    add_common_argument(parser)

    parser.add_argument(
        "-o",
        "--output",
        metavar="",
        default="hhb_out",
        help="The directory that holds the quantized relay ir.",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    parser.add_argument("FILE", help="Directory to the model file")

    ALL_ARGUMENTS_DESC["quantize"] = collect_arguments_info(parser._actions)


def driver_quantize(args_filter: ArgumentFilter):
    """Driver quantize command"""
    args = args_filter.filtered_args
    if not os.path.exists(args.FILE) or not os.path.isdir(args.FILE):
        raise HHBException("The directory is not exists: {}".format(args.FILE))
    relay_ir = HHBRelayIR()
    relay_ir.load_model(args.FILE)
    input_mod, input_params = relay_ir.get_model()
    input_name_list, input_shape_list, _ = get_input_info_from_relay(input_mod, input_params)
    output_shape_list, _ = get_output_info_from_relay(input_mod, input_params)

    # filter arguments and prepare all needed args
    all_filters = [
        collect_preprocess_config,
        set_preprocess_params,
        collect_quantization_config,
        set_quantize_params_by_board,
        collect_codegen_config,
        set_codegen_config,
    ]
    extra_args = AttributeDict()
    extra_args.input_shape = input_shape_list
    extra_args.input_num = len(input_shape_list)
    extra_args.output_num = len(output_shape_list)
    extra_args.model_save = "save_and_run"  # default value
    args_filter.filter_argument(all_filters, extra=extra_args)
    args = args_filter.filtered_args

    # add preprocess node into mod
    if args.preprocess_config.add_preprocess_node:
        from tvm.relay.quantize.quantize_hhb import _bind_params
        from tvm.relay import transform

        if input_params:
            input_mod["main"] = _bind_params(input_mod["main"], input_params)
            input_params = None
        input_mod = transform.AddPreprocessNode(
            args.preprocess_config.data_mean, args.preprocess_config.data_scale
        )(input_mod)
        logger.debug("Insert preprocess node into model successfully!")

    # get calibrate dataset
    dataset_list = []
    if args.calibrate_dataset:
        logger.info("get calibrate dataset from %s", args.calibrate_dataset)
        dl = DatasetLoader(
            args.calibrate_dataset, args.preprocess_config, input_shape_list, input_name_list
        )
        dataset = dl.get_data()
        for d in dataset:
            dataset_list.append(d)

    config_dict = get_config_dict(args)

    qnn_ir = HHBQNNIR()
    qnn_ir.convert((input_mod, input_params), config_dict, dataset_list, args.board)
    args.output = ensure_dir(args.output)

    if args.generate_config:
        generate_config_file(os.path.join(args.output, "cmd_quantizer_params.yml"))

    pre_params = args.preprocess_config
    qnn_ir.save_model(args.output, pre_params, config_dict)
