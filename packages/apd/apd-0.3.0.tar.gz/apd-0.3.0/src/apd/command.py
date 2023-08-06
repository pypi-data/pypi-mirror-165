###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
#
# The command line tools use the click and click-log packages for easier development
#
import logging
import os
import sys

import click
import click_log

from .analysis_data import AnalysisData
from .ap_info import cache_ap_info, load_ap_info
from .rich_console import console

logger = logging.getLogger("apd")
click_log.basic_config(logger)


def exception_handler(exception_type, exception, _):
    # All your trace are belong to us!
    # your format
    print(f"{exception_type.__name__}: {exception}")


sys.excepthook = exception_handler


def setup_cache(cache_directory, working_group, analysis, ap_date=None):
    """Utility function that checks whether the data for the Analysis
    is cached already and does it if needed."""
    if not cache_directory:
        cache_directory = "/tmp/apd_cache"
        logger.debug("Cache directory not set, using %s", cache_directory)
    try:
        load_ap_info(cache_directory, working_group, analysis, ap_date=ap_date)
    except FileNotFoundError:
        logger.debug(
            "Caching information for %s/%s to %s for time %s",
            working_group,
            analysis,
            cache_directory,
            ap_date,
        )
        cache_ap_info(cache_directory, working_group, analysis, ap_date=ap_date)


@click.command()
@click.argument("cache_directory")
@click.argument("working_group")
@click.argument("analysis")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
def cmd_cache_ap_info(cache_directory, working_group, analysis, date):
    logger.debug(
        "Caching information for %s/%s to %s for time %s",
        working_group,
        analysis,
        cache_directory,
        date,
    )
    cache_ap_info(cache_directory, working_group, analysis, ap_date=date)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_directory",
    default=os.environ.get("APD_METADATA_CACHE_DIR", None),
    help="Specify location of the cached analysis data files",
)
@click.option("--tag", default=None, help="Tag to filter datasets", multiple=True)
@click.option(
    "--value",
    default=None,
    help="Tag value used if the name is specified",
    multiple=True,
)
@click.option(
    "--eventtype", default=None, help="eventtype to filter the datasets", multiple=True
)
@click.option(
    "--datatype", default=None, help="datatype to filter the datasets", multiple=True
)
@click.option(
    "--polarity", default=None, help="polarity to filter the datasets", multiple=True
)
@click.option("--name", default=None, help="dataset name")
@click.option("--version", default=None, help="dataset version")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
def cmd_list_pfns(
    working_group,
    analysis,
    cache_directory,
    tag,
    value,
    eventtype,
    datatype,
    polarity,
    name,
    version,
    date,
):
    """List the PFNs for the analysis, matching the tags specified.
    This command checks that the arguments are not ambiguous."""

    setup_cache(cache_directory, working_group, analysis, date)

    # Loading the data and filtering/displaying
    datasets = AnalysisData(
        working_group, analysis, metadata_cache=cache_directory, ap_date=date
    )
    filter_tags = {}
    if name is not None:
        filter_tags["name"] = name
    if version is not None:
        filter_tags["version"] = version
    if eventtype != ():
        filter_tags["eventtype"] = eventtype
    if datatype != ():
        filter_tags["datatype"] = datatype
    if polarity != ():
        filter_tags["polarity"] = polarity
    filter_tags |= dict(zip(tag, value))
    for f in datasets(**filter_tags):
        click.echo(f)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_directory",
    default=os.environ.get("APD_METADATA_CACHE_DIR", None),
    help="Specify location of the cached analysis data files",
)
@click.option("--tag", default=None, help="Tag to filter datasets", multiple=True)
@click.option(
    "--value",
    default=None,
    help="Tag value used if the name is specified",
    multiple=True,
)
@click.option(
    "--eventtype", default=None, help="eventtype to filter the datasets", multiple=True
)
@click.option(
    "--datatype", default=None, help="datatype to filter the datasets", multiple=True
)
@click.option(
    "--polarity", default=None, help="polarity to filter the datasets", multiple=True
)
@click.option("--name", default=None, help="dataset name")
@click.option("--version", default=None, help="dataset version")
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
def cmd_list_samples(
    working_group,
    analysis,
    cache_directory,
    tag,
    value,
    eventtype,
    datatype,
    polarity,
    name,
    version,
    date,
):
    """List the samples for the analysis, matching the tags specified.
    This command does not check whether the data set in unambiguous"""

    # Dealing with the cache
    setup_cache(cache_directory, working_group, analysis, date)

    # Loading the data and filtering/displaying
    datasets = AnalysisData(
        working_group, analysis, metadata_cache=cache_directory, ap_date=date
    )
    filter_tags = {}
    if name is not None:
        filter_tags["name"] = name
    if version is not None:
        filter_tags["version"] = version
    if eventtype != ():
        filter_tags["eventtype"] = eventtype
    if datatype != ():
        filter_tags["datatype"] = datatype
    if polarity != ():
        filter_tags["polarity"] = polarity
    filter_tags |= dict(zip(tag, value))
    matching = datasets(check_data=False, return_pfns=False, **filter_tags)
    click.echo(matching)


@click.command()
@click.argument("working_group")
@click.argument("analysis")
@click.option(
    "--cache_directory",
    default=os.environ.get("APD_METADATA_CACHE_DIR", None),
    help="Specify location of the cached analysis data files",
)
@click.option(
    "--tag",
    default=None,
    help="Tag for which the values should be listed",
    multiple=True,
)
@click.option("--date", default=None, help="analysis date in ISO 8601 format")
@click_log.simple_verbosity_option(logger)
def cmd_summary(
    working_group,
    analysis,
    cache_directory,
    tag,
    date,
):

    # Dealing with the cache
    setup_cache(cache_directory, working_group, analysis, date)

    # Loading the dataset and displaying its summary
    datasets = AnalysisData(
        working_group, analysis, metadata_cache=cache_directory, ap_date=date
    )
    console.print(datasets.summary(tag))
