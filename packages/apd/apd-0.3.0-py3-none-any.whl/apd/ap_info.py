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
# Tool to load and interpret information from the AnalysisProductions data endpoint
#
import collections.abc
import json
import logging
import os
from pathlib import Path

import requests

import apd.auth

logger = logging.getLogger("apd")


def iterable(arg):
    """Version of Iterable that excludes str"""
    return isinstance(arg, collections.abc.Iterable) and not isinstance(
        arg, (str, bytes)
    )


def safe_casefold(a):
    """casefold that can be called on any type, does nothing on non str"""
    if isinstance(a, str):
        return a.casefold()
    return a


class APDataDownloader:
    def __init__(self, api_url="https://lbap.app.cern.ch"):
        self.api_url = api_url
        self.token = None

    def _get_kwargs(self):
        token = apd.auth.get_api_token(
            "lhcb-analysis-productions", f"{self.api_url}/user"
        )
        return dict(
            headers={"Authorization": f"Bearer {token}"},
            timeout=120,
        )

    def get_ap_info(self, working_group, analysis, ap_date=None):
        params = {"at_time": ap_date} if ap_date else None
        r = requests.get(
            f"{self.api_url}/stable/v1/{working_group}/{analysis}",
            params=params,
            **self._get_kwargs(),
        )
        r.raise_for_status()
        return r.json()

    def get_ap_tags(self, working_group, analysis, ap_date=None):
        params = {"at_time": ap_date} if ap_date else None
        r = requests.get(
            f"{self.api_url}/stable/v1/{working_group}/{analysis}/tags",
            params=params,
            **self._get_kwargs(),
        )
        r.raise_for_status()
        return r.json()

    def get_user_info(self):
        r = requests.get(f"{self.api_url}/user", **self._get_kwargs())
        r.raise_for_status()
        return r.json()


def fetch_ap_info(
    working_group,
    analysis,
    loader=None,
    api_url="https://lbap.app.cern.ch",
    ap_date=None,
):
    """Fetch the API info from the service"""

    if not loader:
        loader = APDataDownloader(api_url)

    return SampleCollection(
        loader.get_ap_info(working_group, analysis, ap_date),
        loader.get_ap_tags(working_group, analysis, ap_date),
    )


def cache_ap_info(
    cache_dir,
    working_group,
    analysis,
    loader=None,
    api_url="https://lbap.app.cern.ch",
    ap_date=None,
):
    """Fetch the AP info and cache it locally"""
    cache_dir = Path(cache_dir)
    cache_dir = (cache_dir / "archives" / ap_date) if ap_date else cache_dir
    samples = fetch_ap_info(working_group, analysis, loader, api_url, ap_date)
    wgdir = cache_dir / working_group
    anadir = wgdir / analysis
    datafile = wgdir / f"{analysis}.json"
    tagsfile = anadir / "tags.json"
    if not os.path.exists(anadir):
        os.makedirs(anadir)
    datafile.write_text(json.dumps(samples.info))
    tagsfile.write_text(json.dumps(samples.tags))
    return samples


def _find_case_insensitive(mydir, filename):
    for f in os.listdir(mydir):
        if f.casefold() == filename.casefold():
            return f
    raise FileNotFoundError(f"{filename} in {mydir}")


def load_ap_info(cache_dir, working_group, analysis, ap_date=None):
    """Load the API info from a cache file"""
    cache_dir = Path(cache_dir)
    cache_dir = (cache_dir / "archives" / ap_date) if ap_date else cache_dir
    wgdir = cache_dir / _find_case_insensitive(cache_dir, working_group)
    anadir = wgdir / _find_case_insensitive(wgdir, analysis)
    datafile = wgdir / _find_case_insensitive(wgdir, f"{analysis}.json")
    tagsfile = anadir / "tags.json"
    data = json.loads(datafile.read_text())
    tags = json.loads(tagsfile.read_text())
    return SampleCollection(data, tags)


def load_ap_info_from_single_file(filename):
    """Load the API info from a cache file"""
    filename = Path(filename)
    if not filename.is_file():
        raise Exception("Please specify a valid file as metadata cache")
    data = filename.read_text()
    apinfo = json.loads(data)
    info = apinfo["info"]
    tags = apinfo["tags"]
    return SampleCollection(info, tags)


class SampleCollection:
    """Class wrapping the AnalysisProduction metadata."""

    def __init__(self, info=None, tags=None):

        self.info = info if info else []
        self.tags = tags if tags else {}

    def __len__(self):
        return len(self.info)

    def _sampleTags(self, sample):
        """Method exposing the tags for a given sample/dataset
        We take the dictionary passed in the tag list and add the version and name"""
        sid = str(sample["sample_id"])
        tags = self.tags[sid]
        # version and name are mandatory attributes to the sample,
        # allowing to differentiate the samples produced when the
        # AP is rerun
        tags["version"] = sample["version"]
        tags["name"] = sample["name"]
        return tags

    def __repr__(self):
        return "\n".join(
            [
                f"{s['name']} {s['version']} | " + str(self._sampleTags(s))
                for s in self.info
            ]
        )

    def __iter__(self):
        for s in self.info:
            yield s

    def itertags(self):
        for s in self.info:
            yield self._sampleTags(s)

    def filter(self, *args, **tags):
        """
        Filter the requests according to the tag value passed in parameter
        """
        samples = self.info

        if (len(args) != 0) and len(args) != 2:
            raise ValueError(
                "filter method takes two positional arguments or keyword arguments"
            )

        def _compare_tag(sample, ftag, fvalue):
            """Utility method than handles specific tags, but not iterables"""
            return safe_casefold(self._sampleTags(sample).get(ftag)) == safe_casefold(
                fvalue
            )

        def _filter1(samples, ftag, fvalue):
            logger.debug("filtering samples for %s:%s", ftag, fvalue)
            if callable(fvalue):
                matching = [
                    sample
                    for sample in samples
                    if fvalue(safe_casefold(self._sampleTags(sample).get(ftag, None)))
                ]
            elif iterable(fvalue):
                # We join the requests matching in an empty SampleCollection
                matching = []
                for v in fvalue:
                    matching += [
                        sample for sample in samples if _compare_tag(sample, ftag, v)
                    ]
            else:
                matching = [
                    sample for sample in samples if _compare_tag(sample, ftag, fvalue)
                ]
            return matching

        if len(args) == 2:
            samples = _filter1(samples, args[0], args[1])

        for t, v in tags.items():
            samples = _filter1(samples, t, v)
        return SampleCollection(samples, self.tags)

    def PFNs(self):
        """Collects the PFNs"""
        pfns = []
        for sample in self.info:
            for pfnlist in sample["lfns"].values():
                pfns.append(pfnlist[0])
        return pfns

    def __or__(self, samples):
        info = self.info + samples.info
        tags = {**(self.tags), **(samples.tags)}
        return SampleCollection(info, tags)
