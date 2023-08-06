#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2021] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
#
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Optional

from IPython.core.magic import Magics, cell_magic, line_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

from ..common.mixins import LoggingMixin
from . import commands

if TYPE_CHECKING:
    from ..kernel.dag import MRXLinkDag
    from .server_connectors import MRXLinkMagicsLicenseChecker


@magics_class
class MRXLinkMagics(LoggingMixin, Magics):
    """A class to manage canvas magic commands"""

    link_license: Optional["MRXLinkMagicsLicenseChecker"] = None
    link_dag: Optional["MRXLinkDag"] = None

    @magic_arguments()
    @argument("var", default=None, help="Configuration variable")
    @argument("value", default=None, help="Configuration set value")
    @line_magic
    def mrxlink_set_config(self, line: str) -> None:
        """Set configuration variable"""
        args = parse_argstring(self.mrxlink_set_config, line)
        commands.mrxlink_set_config(link_magic=self, args=args)

    @magic_arguments()
    @argument("dag", help="name of the symbol that references the MRXLinkDag object")
    @line_magic
    def mrxlink_reference_dag(self, line: str) -> None:
        """Return the MRXLinkDag object."""
        args = parse_argstring(self.mrxlink_reference_dag, line)
        commands.mrxlink_reference_dag(link_magic=self, args=args)

    @magic_arguments()
    @argument("-b", "--base_url", default="http://localhost:8888", help="Base URL for server REST API")
    @argument("-h", "--header", default="", help="Header value to communicate with Jupyter server")
    @argument("-c", "--cookie", default="", help="Cookie value to communicate with Jupyter server")
    @cell_magic
    def mrxlink_update_dag(self, line: str, cell: str) -> None:
        """Update DAG at once

        Args:
            line (str): magic command and arguments
            cell (str): JSON description of the DAG
        """
        args = parse_argstring(self.mrxlink_update_dag, line)
        args.cell = cell
        commands.mrxlink_update_dag(link_magic=self, args=args)

    @magic_arguments()
    @argument("-i", "--ids", required=True, help="The identifiers of cells")
    @line_magic
    def mrxlink_set_nodes_execution_queue(self, line: str) -> None:
        """Set queue."""
        args = parse_argstring(self.mrxlink_set_nodes_execution_queue, line)
        commands.mrxlink_set_nodes_execution_queue(link_magic=self, args=args)

    @magic_arguments()
    @line_magic
    def mrxlink_reset_nodes_execution_queue(self, line: str) -> None:
        """Reset queue."""
        args = parse_argstring(self.mrxlink_reset_nodes_execution_queue, line)
        commands.mrxlink_reset_nodes_execution_queue(link_magic=self, args=args)

    @magic_arguments()
    @argument("-i", "--id", required=True, help="The identifier of this cell")
    @argument("-t", "--type", default="CodeCell", help="Type of the node to add/update")
    @argument("-n", "--name", default="Unknown", help="name of the component")
    @cell_magic
    def mrxlink_execute_node(self, line: str, cell: str) -> Any:
        """Entry points for node add/remove

        Args:
            line (str): magic line
            cell (Optional[str], optional): cell contents. Defaults to None.

        Raises:
            NotImplementedError: is raised when a command other than add/remove is issued.

        Returns:
            Any: returns last evaluated expression if any, otherwise None.
        """
        args = parse_argstring(self.mrxlink_execute_node, line)
        args.cell = cell
        return commands.mrxlink_execute_node(link_magic=self, args=args)

    @magic_arguments()
    @argument("level", default="INFO", help="root logging handler's logging level")
    @line_magic
    def mrxlink_logging_level(self, line: str) -> None:
        """set root logging handler's logging level

        Args:
            line (str): magic command and argument
        """
        args = parse_argstring(self.mrxlink_logging_level, line)
        commands.mrxlink_logging_level(link_magic=self, args=args)

    @magic_arguments()
    @argument("-s", "--set", nargs="?", const="", default=None, help="Set DAG cache directory")
    @line_magic
    def mrxlink_cache_dir(self, line: str) -> str:
        """Set/get the cache directory for DAG

        Args:
            line (str): magic command and argument
        """
        args = parse_argstring(self.mrxlink_cache_dir, line)
        return commands.mrxlink_cache_dir(link_magic=self, args=args)

    @magic_arguments()
    @argument("-i", "--id", required=True, help="The identifier of selected cell to set diskcache option")
    @argument("-u", "--use", action="store_true", help="The option to use diskcache")
    @line_magic
    def mrxlink_use_diskcache(self, line: str) -> None:
        """Set use_diskcache option for a component. it can affect to the related components

        Args:
            line (str): magic command and argument
        """
        args = parse_argstring(self.mrxlink_use_diskcache, line)
        commands.mrxlink_use_diskcache(link_magic=self, args=args)

    @magic_arguments()
    @argument("-i", "--id", required=True, help="The identifier of selected cell")
    @line_magic
    def mrxlink_clear_cache(self, line: str) -> None:
        """Clear in-memory cache and diskcache of child nodes, including itself."""
        args = parse_argstring(self.mrxlink_clear_cache, line)
        commands.mrxlink_clear_cache(link_magic=self, args=args)

    @magic_arguments()
    @line_magic
    def mrxlink_clear_all_cache(self, line: str) -> None:
        """Clear in-memory cache and diskcache of all nodes."""
        args = parse_argstring(self.mrxlink_clear_all_cache, line)
        commands.mrxlink_clear_all_cache(link_magic=self, args=args)

    @magic_arguments()
    @argument("-n", "--no-reply", action="store_true", help="No reply to Websocket channel")
    @argument("-b", "--base_url", default="http://localhost:8888", help="Base URL for server REST API")
    @argument("-h", "--header", default="", help="Header value to communicate with Jupyter server")
    @argument("-c", "--cookie", default="", help="Cookie value to communicate with Jupyter server")
    @cell_magic
    # pylint: disable=unused-argument
    def mrxlink_set_parameters(self, line: str, cell: str) -> None:
        """Set parameters for Link DAG and send updated parameters info to the clients.

        Args:
            line (str): magic command and argument
            cell (Optional[str], optional): cell contents. Defaults to None. It includes parameter list
        """
        args: SimpleNamespace = parse_argstring(self.mrxlink_set_parameters, line)
        args.cell = cell
        commands.mrxlink_set_parameters(link_magic=self, args=args)

    @magic_arguments()
    @argument("filename", default="", help="file logging handler's logging filename")
    @line_magic
    def mrxlink_logging_filename(self, line: str) -> None:
        """Set file logging handler's logging filename

        Args:
            line (str): magic command and argument
        """
        args = parse_argstring(self.mrxlink_logging_filename, line)
        commands.mrxlink_logging_filename(link_magic=self, args=args)

    @magic_arguments()
    @line_magic
    def mrxlink_load_diskcache(self, line: str) -> None:
        """Load completed diskcache on the component."""
        args: SimpleNamespace = parse_argstring(self.mrxlink_load_diskcache, line)
        commands.mrxlink_check_queue_and_load_diskcache(link_magic=self, args=args)

    @magic_arguments()
    @argument(
        "-i",
        "--id",
        required=True,
        help="The id of the component whose last output is to be set as the target value to be optimized",
    )
    @argument("-n", "--n_trials", type=int, required=True, help="Number of trial to tune")
    @argument(
        "-o",
        "--opt_method",
        required=True,
        help="Optimization method to tune (ex. GridSearch, RandomSearch, TPESearch)",
    )
    @argument("-m", "--is_maximized", action="store_true", help="Optimization direction. Maximize when True")
    @argument("-b", "--base_url", default="http://localhost:8888", help="Base URL for server REST API")
    @argument("-h", "--header", default="", help="Header value to communicate with Jupyter server")
    @argument("-c", "--cookie", default="", help="Cookie value to communicate with Jupyter server")
    @cell_magic
    def mrxlink_tune_parameters(self, line: str, cell: str) -> None:
        """Tune parameters.

        Args:
            line (str): magic command and argument
            cell (Optional[str], optional): cell contents. Defaults to None. It includes parameter info to tune
            --------------------------
            cell PROTOCOL
            --------------------------
            {
                "parameter_1": {
                    "type": int,
                    "distribution": str (uniform, loguniform, int, ...)
                    "low": str,
                    "high": str,
                },
                "parameter_2": {
                    "type": float,
                    "distribution": str (uniform, loguniform, int, ...)
                    "low": str,
                    "high": str,
                }
            }

        """
        args: SimpleNamespace = parse_argstring(self.mrxlink_tune_parameters, line)
        args.cell = cell
        commands.mrxlink_tune_parameters(link_magic=self, args=args)
