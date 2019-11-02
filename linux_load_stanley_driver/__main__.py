#!/usr/bin/env python3

# Copyright Claudio Mattera 2019.
# Copyright Center for Energy Informatics 2018.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT


from datetime import datetime
import argparse
import logging
import asyncio
import typing
import os

import iso8601

import pandas as pd

import psutil

from pystanley import StanleyAiohttpInterface


def main() -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_main())
    finally:
        loop.close()


async def async_main() -> None:
    arguments = parse_arguments()
    setup_logging(arguments.verbose)
    logger = logging.getLogger(__name__)

    logger.debug("Using Stanley server %s", arguments.url)
    stanley = StanleyAiohttpInterface(
        arguments.url,
        ca_cert=arguments.ca_cert,
        username=arguments.username,
        password=os.environ["STANLEY_PASSWORD"],
    )

    instant = datetime.utcnow().replace(tzinfo=iso8601.UTC)
    logging.info("Reading values at %s...", instant)
    load_one_minute, _, load_fifteen_minutes = os.getloadavg()
    ratio_used_memory = psutil.virtual_memory().percent / 100
    ratio_used_swap = psutil.swap_memory().percent / 100

    load_one_minute_series = pd.Series(load_one_minute, index=pd.to_datetime([instant]))
    load_fifteen_minutes_series = pd.Series(load_fifteen_minutes, index=pd.to_datetime([instant]))
    ratio_used_memory_series = pd.Series(ratio_used_memory, index=pd.to_datetime([instant]))
    ratio_used_swap_series = pd.Series(ratio_used_swap, index=pd.to_datetime([instant]))

    logging.info("Load average (one minute): %.2f", load_one_minute)
    logging.info("Load average (15 minutes): %.2f", load_fifteen_minutes)
    logging.info("Memory usage: %.0f%%", 100 * ratio_used_memory)
    logging.info("Swap usage: %.0f%%", 100 * ratio_used_swap)

    readings = {
        "/machine/linux/{}/load/one-minute".format(arguments.machine): load_one_minute_series,
        "/machine/linux/{}/load/fifteen-minutes".format(arguments.machine): load_fifteen_minutes_series,
        "/machine/linux/{}/memory/ratio-used".format(arguments.machine): ratio_used_memory_series,
        "/machine/linux/{}/swap/ratio-used".format(arguments.machine): ratio_used_swap_series,
    }

    logging.info("Sending values to Stanley server...")
    await stanley.post_readings(readings)
    logging.info("All done")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record Linux system load to Stanley",
        epilog="Stanley password is read from environment variable STANLEY_PASSWORD",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        help="increase output"
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Stanley archiver URL"
    )
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="Stanley archiver username"
    )
    parser.add_argument(
        "--ca-cert",
        type=str,
        help="Custom certification authority certificate"
    )
    parser.add_argument(
        "--machine",
        type=str,
        required=True,
        help="Name of the current machine"
    )

    return parser.parse_args()


def setup_logging(verbose: typing.Optional[int]) -> None:
    if verbose is None or verbose <= 0:
        level = logging.WARN
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        format="%(levelname)s:%(message)s",
        level=level,
    )


if __name__ == "__main__":
    main()
