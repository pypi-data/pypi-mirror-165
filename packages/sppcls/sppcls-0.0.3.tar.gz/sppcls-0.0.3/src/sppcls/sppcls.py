#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# A module to access data from the DFG-funded SPP Computational Literary Studies
#
# Usage:
# import cls
# df = cls.DataFrame("judenbuche", ["events", "keypassages"])
#
# Author: rja
#
# Changes:
# 2022-08-25 (rja)
# - initial version

import pandas as pd

# default repository URL
SPP_CLS_GITLAB = "https://cls-gitlab.phil.uni-wuerzburg.de/spp-cls-data-exchange/spp-cls_annotationtables_data/-/raw/main/"


def load_df(work, projects, repository=SPP_CLS_GITLAB, na_values=""):
    """Generates a dataframe with the data of the projects for work."""
    dataframes = [_download(work, p, repository, na_values) for p in projects]
    dataframe = _merge(dataframes, projects)
    _check(dataframe, dataframes)
    return dataframe


def _download(work, project, repository, na_values):
    # FIXME: add proper URL escaping
    url = repository + "/" + work + "/" + project + ".tsv"
    return pd.read_csv(url, sep='\t', na_values=na_values)


def _merge(dataframes, projects):
    """Merge the dataframes using a JOIN."""
    dataframe = dataframes[0]
    for df in dataframes[1:]:
        dataframe = pd.merge(dataframe, df, on=["id", "word"], suffixes=_suffixes(projects))
    return dataframe


def _suffixes(projects, delim="_"):
    l = _shortest_prefix_length(projects)
    return [delim + p[:l] for p in projects]


def _shortest_prefix_length(projects):
    """Find the smallest l such that the first l chars of projects are uniqe."""
    # FIXME: avoid fixed length
    for i in range(1, 10):
        if len(set([p[:i] for p in projects])) == len(projects):
            return i
    return None


def _check(dataframe, dataframes):
    for df in dataframes:
        assert len(df) == len(dataframe)


if __name__ == '__main__':
    pass
