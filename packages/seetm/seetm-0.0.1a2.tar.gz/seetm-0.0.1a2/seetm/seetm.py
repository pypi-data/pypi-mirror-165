import argparse
import logging
import os
import sys
from typing import NoReturn, Text

from dotenv import load_dotenv

from seetm.cli.seetm_cli import SEETMCLIMapper
from seetm.core.evaluator import SEETMEvaluator
from seetm.core.extractor import SEETMExtractor
from seetm.server.seetm_server import SEETMServer
from seetm.shared.constants import (
    InterfaceType,
    TermColor,
    MappingMethod,
    LoggingLevel,
    Metrics,
    Config,
    PACKAGE_VERSION_LONG,
    EvaluationLevel,
)
from seetm.shared.exceptions.config import (
    InvalidInterfaceException,
    InvalidConfigKeyException,
)
from seetm.shared.exceptions.core import (
    ZeroMappedTokensException,
    EvaluationDatasetExportException,
    ZeroValidTokensException,
    OutDatedEvaluationDatasetException
)
from seetm.utils.config import get_init_configs
from seetm.utils.io import (
    set_cli_color,
    dir_exists,
    update_sys_path,
)
from seetm.utils.scaffold import SEETMInit
from seetm.utils.seetm_logging_formatter import (
    SEETMLoggingFormatter,
    MaxLevelFilter,
)

load_dotenv()
logger = logging.getLogger()
update_sys_path(os.getcwd())

formatter = SEETMLoggingFormatter(format_str='%(asctime)s\t%(levelname)s\t%(name)s - %(message)s')
logging_out = logging.StreamHandler(sys.stdout)
logging_err = logging.StreamHandler(sys.stderr)
logging_out.setFormatter(formatter)
logging_err.setFormatter(formatter)
logging_out.addFilter(MaxLevelFilter(logging.WARNING))
logging_out.setLevel(logging.DEBUG)
logging_err.setLevel(logging.WARNING)
logger.addHandler(logging_out)
logger.addHandler(logging_err)
logger.setLevel(level=logging.INFO)


def create_argument_parser():
    parser = argparse.ArgumentParser(prog="seetm", description="starts SEETM CLI")
    subparsers = parser.add_subparsers(help='desired SEETM interface to run [cli/server]', dest="subparser_name")

    parser.add_argument(
        "-v",
        "--version",
        action='version',
        version=PACKAGE_VERSION_LONG,
        help="prints the SEETM version info.",
    )

    parser_init = subparsers.add_parser(
        name="init",
        help='create init dir structure for a new mapping project.'
    )
    parser_init.add_argument(
        "--debug",
        action="store_true",
        help="sets the SEETM logging level to debug mode from info.",
    )
    parser_init.add_argument(
        "--quiet",
        action="store_true",
        help="initializes a starter SEETM project without prompting the user for a project configs.",
    )

    parser_server = subparsers.add_parser(
        name="server",
        help='run SEETM server, a web-based mapping tool.'
    )
    parser_server.add_argument(
        "-p",
        "--port",
        type=int,
        help="the port to start the SEETM server at.",
    )
    parser_server.add_argument(
        "-c",
        "--config",
        type=str,
        default=Config.DEFAULT_CONFIG_PATH,
        help="custom SEETM config file.",
    )
    parser_server.add_argument(
        "-m",
        "--method",
        type=str,
        choices=[MappingMethod.IPA, MappingMethod.RULE_BASED, MappingMethod.TRANSLATE],
        help="method used to map the instance/token.",
    )
    parser_server.add_argument(
        "--debug",
        action="store_true",
        help="sets the logging level to debug mode from info and flask server debug mode to True.",
    )

    parser_mapper = subparsers.add_parser(
        name="map",
        help='run SEETM CLI mapper, a terminal-based mapper tool.'
    )
    parser_mapper.add_argument(
        "-i",
        "--instance",
        type=str,
        default=None,
        help="data instance to generate mapping.",
    )
    parser_mapper.add_argument(
        "-c",
        "--config",
        type=str,
        default=Config.DEFAULT_CONFIG_PATH,
        help="custom SEETM config file.",
    )
    parser_mapper.add_argument(
        "-m",
        "--method",
        type=str,
        choices=[MappingMethod.IPA, MappingMethod.RULE_BASED],
        help="method used to map the instance/token.",
    )
    parser_mapper.add_argument(
        "--debug",
        action="store_true",
        help="sets the SEETM logging level to debug mode from info.",
    )
    parser_mapper.add_argument(
        "--no-persist",
        action="store_false",
        dest="persist",
        help="states whether to store mapped instance or not.",
    )
    parser_mapper.add_argument(
        "--no-case",
        action="store_false",
        dest="case",
        help="states whether to store mapped instance or not.",
    )
    parser_mapper.add_argument(
        "--quiet",
        action="store_true",
        help="sets the SEETM logging level to off.",
    )

    parser_evaluator = subparsers.add_parser(
        name="evaluate",
        help='run SEETM CLI evaluator.'
    )
    parser_evaluator.add_argument(
        "-c",
        "--config",
        type=str,
        default=Config.DEFAULT_CONFIG_PATH,
        help="custom SEETM config file.",
    )
    parser_evaluator.add_argument(
        "-m",
        "--method",
        type=str,
        choices=[MappingMethod.IPA, MappingMethod.RULE_BASED],
        help="method used to map the instance/token.",
    )
    parser_evaluator.add_argument(
        "--metric",
        type=str,
        choices=[Metrics.EDIT_DISTANCE, Metrics.SEQUENCE_MATCHING],
        help="metric to evaluate mapped tokens or instances.",
    )
    parser_evaluator.add_argument(
        "-l",
        "--level",
        type=str,
        choices=[EvaluationLevel.TOKEN, EvaluationLevel.VECTOR],
        required=True,
        help="sets the evaluation level to token or instance level.",
    )
    parser_evaluator.add_argument(
        "-e",
        "--epochs",
        type=int,
        default=10,
        help="sets the number of epochs to train the word2vec models.",
    )
    parser_evaluator.add_argument(
        "--debug",
        action="store_true",
        help="sets the SEETM logging level to debug mode from info.",
    )
    parser_evaluator.add_argument(
        "--no-persist",
        action="store_false",
        dest="persist",
        help="states whether to store mapped instance or not.",
    )
    parser_evaluator.add_argument(
        "--quiet",
        action="store_true",
        help="sets the SEETM logging level to off.",
    )

    parser_extractor = subparsers.add_parser(
        name="extract",
        help='run SEETM CLI token extractor.'
    )
    parser_extractor.add_argument(
        "-d",
        "--data-path",
        type=str,
        default=None,
        help="data path to find NLU files at.",
    )
    parser_extractor.add_argument(
        "-c",
        "--config",
        type=str,
        default=Config.DEFAULT_CONFIG_PATH,
        help="custom SEETM config file.",
    )
    parser_extractor.add_argument(
        "--clean",
        action="store_true",
        help="informs the extractor to remove existing eval data and maps.",
    )
    parser_extractor.add_argument(
        "--debug",
        action="store_true",
        help="sets the SEETM logging level to debug mode from info.",
    )
    parser_extractor.add_argument(
        "--no-persist",
        action="store_false",
        dest="persist",
        help="states whether to store mapped instance or not.",
    )
    parser_extractor.add_argument(
        "--quiet",
        action="store_true",
        help="sets the SEETM logging level to off.",
    )
    return parser


def _set_logging_level(level: Text = LoggingLevel.INFO) -> NoReturn:
    if level == LoggingLevel.NOTSET:
        logger.setLevel(level=logging.NOTSET)
    elif level == LoggingLevel.DEBUG:
        logger.setLevel(level=logging.DEBUG)
    elif level == LoggingLevel.INFO:
        logger.setLevel(level=logging.INFO)
    elif level == LoggingLevel.WARNING:
        logger.setLevel(level=logging.WARNING)
    elif level == LoggingLevel.ERROR:
        logger.setLevel(level=logging.ERROR)
    elif level == LoggingLevel.CRITICAL:
        logger.setLevel(level=logging.CRITICAL)
    elif level == LoggingLevel.QUIET:
        logging.disable(level=logging.CRITICAL)
    else:
        logger.setLevel(level=logging.INFO)


def run_seetm_cli() -> NoReturn:
    try:
        logger.debug("Running main SEETM CLI.")
        arg_parser = create_argument_parser()
        cmdline_args = arg_parser.parse_args()
        interface = cmdline_args.subparser_name

        if not interface:
            arg_parser.print_help()
            logger.error("Please specify a valid positional arg out of \'map\',\'init\', \'server\', \'evaluate\', "
                         "and \'extract\' to use SEETM CLI.")
            return

        if str.lower(interface) == InterfaceType.INIT:
            quiet = cmdline_args.quiet
            debug_mode = cmdline_args.debug

            if debug_mode:
                _set_logging_level(level=LoggingLevel.DEBUG)
            else:
                _set_logging_level(level=LoggingLevel.INFO)

            try:
                if not quiet:
                    print(set_cli_color(
                        text_content="👋🏽 Hi there! Welcome to SEETM.",
                        color=TermColor.LIGHTGREEN)
                    )
                    dest_dir = input(set_cli_color(
                        text_content="In which directory do you want to "
                                     "initialize SEETM? [Default: Current "
                                     "Directory]: ",
                        color=TermColor.LIGHTGREEN
                    ))
                else:
                    dest_dir = "."

                if dest_dir and not dir_exists(dir_path=dest_dir):
                    logger.error("Directory name or path should be a "
                                 "valid existing directory")
                    return

                seetm_init = SEETMInit()
                seetm_init.build_scaffold(dest_path=dest_dir)
            except KeyboardInterrupt:
                logger.error("Gracefully terminating SEETM init...")

        elif str.lower(interface) == InterfaceType.SERVER:
            port = cmdline_args.port
            config = cmdline_args.config
            method = cmdline_args.method
            debug_mode = cmdline_args.debug

            if debug_mode:
                _set_logging_level(level=LoggingLevel.DEBUG)
            else:
                _set_logging_level(level=LoggingLevel.INFO)

            configs = get_init_configs(
                config_path=config,
                port=port,
                method=method,
                interface=InterfaceType.SERVER,
            )

            seetm_server = SEETMServer(
                configs=configs,
                debug_mode=debug_mode or False,
            )
            seetm_server.run()

        elif str.lower(interface) == InterfaceType.MAPPER:
            instance = cmdline_args.instance
            method = cmdline_args.method
            config = cmdline_args.config
            persist = cmdline_args.persist
            case = cmdline_args.case
            debug_mode = cmdline_args.debug
            quiet_mode = cmdline_args.quiet

            if debug_mode:
                _set_logging_level(level=LoggingLevel.DEBUG)
            elif quiet_mode:
                _set_logging_level(level=LoggingLevel.QUIET)
            else:
                _set_logging_level(level=LoggingLevel.INFO)

            configs = get_init_configs(
                config_path=config,
                instance=instance,
                method=method,
                case=case,
                interface=InterfaceType.MAPPER,
            )
            print(configs)
            exit()
            seetm_cli_mapper = SEETMCLIMapper(
                configs=configs,
                persist=persist,
                quiet_mode=True if quiet_mode else False,
            )
            seetm_cli_mapper.run()

        elif str.lower(interface) == InterfaceType.EVALUATOR:
            metric = cmdline_args.metric
            method = cmdline_args.method
            level = cmdline_args.level
            config = cmdline_args.config
            epochs = cmdline_args.epochs
            persist = cmdline_args.persist
            debug_mode = cmdline_args.debug
            quiet_mode = cmdline_args.quiet

            if debug_mode:
                _set_logging_level(level=LoggingLevel.DEBUG)
            elif quiet_mode:
                _set_logging_level(level=LoggingLevel.QUIET)
            else:
                _set_logging_level(level=LoggingLevel.INFO)

            if metric == Metrics.SEQUENCE_MATCHING:
                logger.warning("sequence-matching metric depends on the order of the "
                               "tokens provided (test_instance, mapped_instance). "
                               "Use edit-distance as it is more precise.")

            configs = get_init_configs(
                config_path=config,
                method=method,
                metric=metric,
                level=level,
                interface=InterfaceType.EVALUATOR,
            )
            seetm_evaluator = SEETMEvaluator(
                configs=configs,
                level=level,
                epochs=epochs,
                persist=persist,
                quiet_mode=True if quiet_mode else False,
            )
            seetm_evaluator.evaluate()

        elif str.lower(interface) == InterfaceType.EXTRACTOR:
            data_path = cmdline_args.data_path
            config = cmdline_args.config
            persist = cmdline_args.persist
            clean = cmdline_args.clean
            debug_mode = cmdline_args.debug
            quiet_mode = cmdline_args.quiet

            if debug_mode:
                _set_logging_level(level=LoggingLevel.DEBUG)
            elif quiet_mode:
                _set_logging_level(level=LoggingLevel.QUIET)
            else:
                _set_logging_level(level=LoggingLevel.INFO)

            configs = get_init_configs(
                config_path=config,
                data_path=data_path,
                interface=InterfaceType.EXTRACTOR,
            )
            seetm_extractor = SEETMExtractor(
                configs=configs,
                persist=persist,
                clean=clean,
                quiet_mode=True if quiet_mode else False,
            )
            seetm_extractor.extract()
        else:
            logger.error('One or more incorrect CLI arguments detected. '
                         'Refer "seetm -h" to view allowed arguments')
            return
    except InvalidInterfaceException as e:
        logger.error(f"Invalid interface specified.")
        logger.debug(e) if e else None
    except InvalidConfigKeyException as e:
        logger.error(f"Found invalid config keys.")
        logger.debug(e) if e else None
    except KeyboardInterrupt:
        logger.info(f"Gracefully terminating SEETM CLI...")

    # new
    except ZeroMappedTokensException as e:
        logger.error(f"Non of the tokens were mapped. Evaluation is terminated. {e}")
    except EvaluationDatasetExportException as e:
        logger.error(f"Exception occurred while exporting the evaluation dataset. {e}")

    except ZeroValidTokensException:
        logger.error(f"Could not find any valid evaluation token pairs. "
                     f"Use `seetm extract` to generate an up-to-date evaluation "
                     f"dataset or manually map them and retry")
    except OutDatedEvaluationDatasetException:
        logger.error(f"Found out-dated evaluation token pairs. "
                     f"Use `seetm extract` to generate an up-to-date evaluation "
                     f"dataset or manually remove them and retry")

    #     # Training data exceptions
    #     except EvalFileNotFoundException:
    #     logger.error("Could not find the eval YAML files")
    #     exit("data not found error") if self.quiet_mode else exit()
    # except YAMLFormatException:
    #     logger.error("Invalid YAML file format in NLU files")
    #     exit("invalid yaml format error") if self.quiet_mode else exit()
    # except InvalidNLUDatasetException:
    #     logger.error("Could not find the data dir specified")
    #     exit("invalid data path error") if self.quiet_mode else exit()
    # except EmptyNLUDatasetException as e:
    #     logger.error(e)
    #     exit("empty nlu data error") if self.quiet_mode else exit()
    # except InvalidFileExtensionException as e:
    #     logger.error(e)
    #     exit("file ext error") if self.quiet_mode else exit()
    # except InvalidDataInstanceException as e:
    #     logger.error(e)
    #     exit("data instance error") if self.quiet_mode else exit()
    # except ExportableInitializationException as e:
    #     logger.error(e)
    #     exit("data instance error") if self.quiet_mode else exit()
    # # SEETM Base exceptions
    # except MapperException as e:
    #     logger.error(e)
    #     exit("mapper error") if self.quiet_mode else exit()
    # except SEETMCoreException as e:
    #     logger.error(f"Unknown Core Exception {e}")
    #     exit("core error") if self.quiet_mode else exit()
    # except SEETMIOException as e:
    #     logger.error(f"Unknown IO Exception {e}")
    #     exit("io error") if self.quiet_mode else exit()
    # except SEETMException as e:
    #     logger.error(f"Unknown Base Exception {e}")
    #     exit("base error") if self.quiet_mode else exit()
    # # Default exceptions
    # except KeyboardInterrupt:
    #     logger.info(f"Gracefully terminating SEETM CLI Mapper...")
    #     exit("keyboard error") if self.quiet_mode else exit()
    # except MemoryError as e:
    #     logger.info(f"Out of memory exception occurred "
    #                 f"while loading the model. {e}")
    #     exit("memory error") if self.quiet_mode else exit()
    # except OSError as e:
    #     logger.info(f"OSError exception occurred "
    #                 f"while loading the model. {e}")
    #     exit("os error") if self.quiet_mode else exit()
    # # except Exception as e:
    # #     logger.error(f"Unknown CLI Exception. {e}")
    # #     exit("generic error") if self.quiet_mode else exit()
    # #
    #     # Training data exceptions
    #     except NLUFileNotFoundException:
    #     logger.error("Could not find the NLU yaml files")
    #     exit("data not found error") if self.quiet_mode else exit()
    # except YAMLFormatException:
    #     logger.error("Invalid YAML file format in NLU files")
    #     exit("invalid yaml format error") if self.quiet_mode else exit()
    # except InvalidNLUDatasetException:
    #     logger.error("Could not find the data dir specified")
    #     exit("invalid data path error") if self.quiet_mode else exit()
    # except EmptyNLUDatasetException as e:
    #     logger.error(e)
    #     exit("empty nlu data error") if self.quiet_mode else exit()
    # except InvalidFileExtensionException as e:
    #     logger.error(e)
    #     exit("file ext error") if self.quiet_mode else exit()
    # except InvalidDataInstanceException as e:
    #     logger.error(e)
    #     exit("data instance error") if self.quiet_mode else exit()
    # except ExportableInitializationException as e:
    #     logger.error(e)
    #     exit("data instance error") if self.quiet_mode else exit()
    # # SEETM Base exceptions
    # except MapperException as e:
    #     logger.error(e)
    #     exit("mapper error") if self.quiet_mode else exit()
    # except SEETMCoreException as e:
    #     logger.error(f"Unknown Core Exception {e}")
    #     exit("core error") if self.quiet_mode else exit()
    # except SEETMIOException as e:
    #     logger.error(f"Unknown IO Exception {e}")
    #     exit("io error") if self.quiet_mode else exit()
    # except SEETMException as e:
    #     logger.error(f"Unknown Base Exception {e}")
    #     exit("base error") if self.quiet_mode else exit()
    # # Default exceptions
    # except KeyboardInterrupt:
    #     logger.info(f"Gracefully terminating SEETM CLI Mapper...")
    #     exit("keyboard error") if self.quiet_mode else exit()
    # except MemoryError as e:
    #     logger.info(f"Out of memory exception occurred "
    #                 f"while loading the model. {e}")
    #     exit("memory error") if self.quiet_mode else exit()
    # except OSError as e:
    #     logger.info(f"OSError exception occurred "
    #                 f"while loading the model. {e}")
    #     exit("os error") if self.quiet_mode else exit()
    # except Exception as e:
    #     logger.error(f"Unknown CLI Exception. {e}")
    #     exit("generic error") if self.quiet_mode else exit()


if __name__ == "__main__":
    logger.error("This script cannot be directly executed. "
                 "please use the 'seetm' CLI tool instead.")
    exit(code=1)
