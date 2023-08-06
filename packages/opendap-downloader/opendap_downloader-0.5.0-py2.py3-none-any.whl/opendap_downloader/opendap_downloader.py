#!/usr/bin/env python3

import itertools
import os
import re
from datetime import datetime
from typing import List, Optional, Tuple

import click
import requests
import xarray as xr
import numpy as np
from dask.diagnostics import ProgressBar
from pydap.net import HTTPError
from xarray.backends import PydapDataStore


def __parse_limit(message: str) -> Optional[float]:
    match = re.search(r", max=.+\";", message)
    if match:
        limit = match.group().strip(', max=";')
        return float(limit)
    else:
        return None


def split_by_chunks(dataset):
    chunk_slices = {}
    for dim, chunks in dataset.chunks.items():
        slices = []
        start = 0
        for chunk in chunks:
            if start >= dataset.sizes[dim]:
                break
            stop = start + chunk
            slices.append(slice(start, stop))
            start = stop
        chunk_slices[dim] = slices
    for slices in itertools.product(*chunk_slices.values()):
        selection = dict(zip(chunk_slices.keys(), slices))
        yield dataset[selection]


def find_chunk(ds: xr.Dataset, limit: float) -> Optional[int]:
    N = ds["time"].shape[0]
    for i in range(N, 0, -1):
        ds = ds.chunk({"time": i})
        ts = list(split_by_chunks(ds))
        if (ts[0].nbytes / (1000 * 1000)) < limit:
            return i
    return None


def subset(
    ds,
    variables: List[str],
    geographical_subset: Tuple[float, float, float, float],
    temporal_subset: Tuple[datetime, datetime],
    depth_range: Tuple[float, float],
):

    if variables:
        ds = ds[np.array(variables)]

    if geographical_subset:
        (
            minimal_latitude,
            maximal_latitude,
            minimal_longitude,
            maximal_longitude,
        ) = geographical_subset
        if "latitude" in ds.coords:
            ds = ds.sel(
                latitude=slice(minimal_latitude, maximal_latitude),
                longitude=slice(minimal_longitude, maximal_longitude),
            )
        else:
            ds = ds.sel(
                lat=slice(minimal_latitude, maximal_latitude),
                lon=slice(minimal_longitude, maximal_longitude),
            )

    if temporal_subset:
        (start_datetime, end_datetime) = temporal_subset
        ds = ds.sel(time=slice(start_datetime, end_datetime))

    if ("depth" in ds.dims) and (depth_range is not None):
        (
            minimal_depth,
            maximal_depth,
        ) = depth_range
        ds = ds.sel(depth=slice(minimal_depth, maximal_depth))

    return ds


@click.command(
    help="""Downloads OPeNDAP dataset as NetCDF files taking into account the
server data query limit.

Example:

  opendap-downloader
--dataset-url
https://nrt.cmems-du.eu/thredds/dodsC/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
--variable analysed_sst --variable sea_ice_fraction
--temporal-subset 2021-01-01 2021-01-02
--geographical-subset 0.0 0.1 0.0 0.1

  opendap-downloader
-u https://nrt.cmems-du.eu/thredds/dodsC/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
-v analysed_sst -v sea_ice_fraction
-t 2021-01-01 2021-01-02
-g 0.0 0.1 0.0 0.1
"""
)
@click.option(
    "--dataset-url",
    "-u",
    type=str,
    required=True,
    help="The full OPeNDAP dataset URL",
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help="Specify dataset variables",
    multiple=True,
)
@click.option(
    "--geographical-subset",
    "-g",
    type=(
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-180, max=180),
        click.FloatRange(min=-180, max=180),
    ),
    help="The geographical subset as "
    + "minimal latitude, maximal latitude, "
    + "minimal longitude and maximal longitude",
)
@click.option(
    "--temporal-subset",
    "-t",
    type=(
        click.DateTime(
            ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        ),
        click.DateTime(
            ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        ),
    ),
    help="The temporal subset as start datetime and end datetime",
)
@click.option(
    "--depth-range",
    "-d",
    type=(click.FloatRange(min=0), click.FloatRange(min=0)),
    help="The depth range in meters, if depth is a dataset coordinate",
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(),
    required=True,
    help="The destination path for the downloaded files."
    + " Default is the current directory",
    default="",
)
@click.option(
    "--output-file",
    "-f",
    type=click.Path(),
    help="Concatenate the downloaded data in the given file name"
    + " (under the output path)",
)
@click.option("--login", "-l", prompt="Your login please:")
@click.password_option(confirmation_prompt=False)
def download_dataset(
    dataset_url: str,
    variables: List[str],
    geographical_subset: Tuple[float, float, float, float],
    temporal_subset: Tuple[datetime, datetime],
    depth_range: Tuple[float, float],
    output_path: str,
    output_file: Optional[str],
    login: str,
    password: str,
):
    session = requests.Session()
    session.auth = (login, password)
    store = PydapDataStore.open(dataset_url, session=session)

    ds = xr.open_dataset(store)
    ds = subset(
        ds, variables, geographical_subset, temporal_subset, depth_range
    )

    complete_dataset = os.path.join(
        output_path, dataset_url.rsplit("/", 1)[-1] + ".nc"
    )

    try:
        click.echo("Trying to download as one file...")
        ds.to_netcdf(complete_dataset)
    except HTTPError as e:
        if os.path.exists(complete_dataset):
            try:
                os.remove(complete_dataset)
            except OSError:
                click.echo("Error while deleting file: ", complete_dataset)

        click.echo("Dataset must be chunked.")
        limit = __parse_limit(str(e.comment))
        if limit:
            click.echo(f"Server download limit is {limit} MB")
            i = find_chunk(ds, limit)
            ds = xr.open_dataset(
                store, mask_and_scale=True, chunks={"time": i}
            )

            ds = subset(
                ds,
                variables,
                geographical_subset,
                temporal_subset,
                depth_range,
            )

            ts = list(split_by_chunks(ds))

            p = [
                os.path.join(output_path, str(g) + ".nc")
                for g in range(len(ts))
            ]

            click.echo("Downloading " + str(len(ts)) + " files...")
            delayed = xr.save_mfdataset(datasets=ts, paths=p, compute=False)
            with ProgressBar():
                delayed.compute()
            click.echo("Files downloaded")

            if output_file is not None:
                click.echo(f"Concatenating files into {output_file}...")
                ds = xr.open_mfdataset(p)
                delayed = ds.to_netcdf(
                    os.path.join(output_path, output_file), compute=False
                )
                with ProgressBar():
                    delayed.compute()
                click.echo("Files concatenated")

                click.echo("Removing temporary files")
                for path in p:
                    try:
                        os.remove(path)
                    except OSError:
                        click.echo("Error while deleting file: ", path)
                click.echo("Done")

        else:
            click.echo("No limit found in the returned server error")


if __name__ == "__main__":
    download_dataset()
