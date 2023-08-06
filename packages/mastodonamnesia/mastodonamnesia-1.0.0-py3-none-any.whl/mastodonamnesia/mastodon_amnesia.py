"""
    MastodonAmnesia - deletes old Mastodon toots
    Copyright (C) 2021  Mark S Burgunder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import asyncio
import logging
from math import ceil
from typing import Any
from typing import cast
from typing import Dict
from typing import Optional

import arrow
from atoot import MastodonAPI
from atoot import RatelimitError
from outdated import check_outdated
from rich import print as rprint
from rich import traceback
from tqdm import tqdm
from tqdm import trange

from . import __package_name__
from . import __version__
from .control import Configuration

traceback.install(show_locals=True)
logger = logging.getLogger("MastodonAmnesia")


async def main() -> None:
    """Main logic to run MastodonAmnesia."""

    parser = argparse.ArgumentParser(description="Delete old toots.")
    parser.add_argument(
        "-c",
        "--config-file",
        action="store",
        default="config.json",
        dest="config_file",
        help="Name of configuration file to use",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="Only print out which toots would be deleted. No actual deletion occurs",
        action="store_true",
        dest="dry_run",
    )

    args = parser.parse_args()

    config = await Configuration.load_config(config_file_name=args.config_file)

    mastodon = config.mastodon_config.mastodon

    now = arrow.now()
    oldest_to_keep = now.shift(seconds=-config.bot.delete_after)

    rprint(f"Welcome to MastodonAmnesia {__version__}")

    check_updates()

    rprint(
        f"We are removing toots older than {oldest_to_keep} "
        f"from {config.mastodon_config.instance}@"
        f"{config.mastodon_config.user_info.user_name}"
    )

    toots = await mastodon.account_statuses(
        account=config.mastodon_config.user_info.account_id
    )

    total_toots = 0
    toots_to_delete = []
    title = "Finding toots to delete"
    with tqdm(
        desc=f"{title:.<60}",
        ncols=120,
        unit=" toots",
        position=0,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} at {rate_fmt}",
    ) as progress_bar:
        while True:
            total_toots += len(toots)
            progress_bar.total = total_toots
            for toot in toots:
                logger.debug(
                    "Processing toot: %s from %s",
                    toot.get("url"),
                    toot.get("created_at"),
                )

                try:
                    toot_created_at = arrow.get(cast(int, toot.get("created_at")))
                    logger.debug(
                        "Oldest to keep vs toot created at %s > %s (%s)",
                        oldest_to_keep,
                        toot_created_at,
                        bool(oldest_to_keep > toot_created_at),
                    )

                    if toot_created_at < oldest_to_keep:
                        if should_keep(toot, config):
                            logger.info(
                                "Not deleting toot: "
                                "Bookmarked: %s - "
                                "My Fav: %s - "
                                "Pinned: %s - "
                                "Poll: %s - "
                                "Attachements: %s - "
                                "Faved: %s - "
                                "Boosted: %s - "
                                "DM: %s -+- "
                                "%s",
                                toot.get("bookmarked"),
                                toot.get("favourited"),
                                toot.get("pinned"),
                                (toot.get("poll") is not None),
                                len(toot.get("media_attachments")),
                                toot.get("favourites_count"),
                                toot.get("reblogs_count"),
                                (toot.get("visibility") == "direct"),
                                toot.get("url"),
                            )
                            progress_bar.update()
                            continue

                        toots_to_delete.append(toot)

                    else:
                        logger.debug(
                            "Skipping toot: %s from %s",
                            toot.get("url"),
                            toot.get("created_at"),
                        )

                except RatelimitError:
                    await sleep_off_ratelimiting(mastodon=mastodon)

                progress_bar.update()

            # Get More toots if available:
            if toots.next:
                toots = await mastodon.get_next(toots)
            else:
                break

    total_toots_to_delete = len(toots_to_delete)

    # If dry-run has been specified, print out list of toots that would be deleted
    if args.dry_run:
        rprint("\n--dry-run or -d specified. [yellow][bold]No toots will be deleted")
        for toot in toots_to_delete:
            rprint(
                f"[red]Would[/red] delete toot"
                f" {toot.get('url')} from {toot.get('created_at')}"
            )
        rprint(f"Total of {total_toots_to_delete} toots would be deleted.")

    # Dry-run has not been specified... delete toots!
    else:
        await delete_toots(mastodon, toots_to_delete)
        rprint(f"All old toots deleted! Total of {total_toots_to_delete} toots deleted")

    await mastodon.close()


async def delete_toots(
    mastodon: MastodonAPI, toots_to_delete: list[dict[str, Any]]
) -> None:
    """Method to delete all toots that should be deleted."""
    title = "Deleting toots"
    total_toots_to_delete = len(toots_to_delete)
    if total_toots_to_delete > 0:
        with tqdm(
            desc=f"{title:.<60}",
            ncols=120,
            total=total_toots_to_delete,
            unit=" toots",
            position=0,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} at {rate_fmt}",
        ) as progress_bar:

            while len(toots_to_delete) > 0:

                responses = await asyncio.gather(
                    *[delete_single_toot(i, mastodon) for i in toots_to_delete]
                )

                deleted_toots = [toot for toot in responses if toot is not None]
                for toot in deleted_toots:
                    progress_bar.update()
                    toots_to_delete.remove(toot)

                if len(deleted_toots) < len(toots_to_delete):
                    await sleep_off_ratelimiting(mastodon=mastodon)


async def sleep_off_ratelimiting(mastodon: MastodonAPI) -> None:
    """Determines time needed to wait and waits for rate limiting to be
    over."""

    reset_at = arrow.get(mastodon.ratelimit_reset).datetime
    now = arrow.now().datetime
    need_to_wait = ceil((reset_at - now).total_seconds())

    logger.info(
        "Need to wait %s seconds (until %s) to let server 'cool down'",
        need_to_wait,
        arrow.get(mastodon.ratelimit_reset),
    )
    bar_title = "Waiting to let server 'cool-down'"
    for _i in trange(
        need_to_wait,
        desc=f"{bar_title:.<60}",
        unit="s",
        ncols=120,
        bar_format="{desc}: {percentage:3.0f}%|{bar}| Eta: {remaining} - Elapsed: {elapsed}",
        position=1,
    ):
        await asyncio.sleep(1)


async def delete_single_toot(
    toot: dict[str, Any], mastodon: MastodonAPI
) -> Optional[dict[str, Any]]:
    """Deletes a single toot."""
    return_toot: Optional[dict[str, Any]] = toot
    try:
        await mastodon.delete_status(toot)
        logger.info(
            "Deleted toot %s from %s",
            toot.get("url"),
            toot.get("created_at"),
        )
    except RatelimitError:
        return_toot = None

    return return_toot


def check_updates() -> None:
    """Check if there is a newer version of MastodonAmnesia available on
    PyPI."""
    is_outdated = False
    try:
        is_outdated, pypi_version = check_outdated(
            package=__package_name__,
            version=__version__,
        )
        if is_outdated:
            rprint(
                f"[bold][red]!!! New version of MastodonAmnesia ({pypi_version}) "
                f"is available on PyPI.org !!!\n"
            )
    except ValueError:
        rprint(
            "[yellow]Notice - Your version is higher than last published version on PyPI"
        )


def should_keep(toot: Dict[str, Any], config: Configuration) -> bool:
    """Function to determine if toot should be kept even though it might be a
    candidate for deletion."""
    keeping = False
    if config.bot.skip_deleting_bookmarked:
        keeping = bool(toot.get("bookmarked"))

    if not keeping and config.bot.skip_deleting_faved:
        keeping = bool(toot.get("favourited"))

    if not keeping and config.bot.skip_deleting_pinned:
        keeping = bool(toot.get("pinned"))

    if not keeping and config.bot.skip_deleting_poll:
        keeping = bool(toot.get("poll"))

    if not keeping and config.bot.skip_deleting_dm:
        keeping = toot.get("visibility") == "direct"

    if not keeping and config.bot.skip_deleting_media:
        medias = toot.get("media_attachments")
        if isinstance(medias, list):
            keeping = bool(len(medias))

    if not keeping and config.bot.skip_deleting_faved_at_least:
        keeping = bool(
            toot.get("favourites_count", 0) >= config.bot.skip_deleting_faved_at_least
        )

    if not keeping and config.bot.skip_deleting_boost_at_least:
        keeping = bool(
            toot.get("reblogs_count", 0) >= config.bot.skip_deleting_boost_at_least
        )

    return keeping


def start() -> None:
    """Main entry point for app."""
    asyncio.run(main())


# run main programs
if __name__ == "__main__":
    start()
