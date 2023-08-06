"""rws_nwb_lib.download_nwb simplifies access to the latest NWB data."""
import logging
import warnings
from typing import List, Tuple

import geopandas as gpd
import requests
from requests import Response

from rws_nwb_lib.config import NWBConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Filter out warning thrown by geopandas
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=".*distutils.*classes are deprecated.*",
)
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*imp module is deprecated.*"
)


# These 6 arguments give the user extra functionality
def process_nwb(
    config: NWBConfig,
    output_file_path: str = "nwb.gml",
) -> gpd.GeoDataFrame:
    """Download the latest data from the NWB.

    Parameters
    ----------
    config
        Object holding configuration for downloading and filtering the NWB.
    output_file_path
        The output directory for the NWB shapefile.

    Returns
    -------
    pd.DataFrame
        A Pandas dataframe containing the NWB data for the selected region. For more
        information on this dataset, please refer to
        https://www.pdok.nl/geo-services/-/article/nationaal-wegen-bestand-nwb-
    """
    complete_url = build_nwb_url(config.only_state_roads, config.bounding_box)

    logging.info("Downloading data from NWB using the following URL: %s", complete_url)

    response = download_nwb_shapefile(complete_url, config)

    logging.info("Data downloaded")

    with open(output_file_path, "wb") as out:
        logging.info("Writing response data to file system")
        out.write(response.text.encode(config.encoding))

    logging.info("Reading response into GeoDataFrame")
    result = gpd.read_file(output_file_path)

    float_columns = ["beginkm", "eindkm"]

    for float_column in float_columns:
        result[float_column] = result[float_column].map(float)

    result = apply_filters(
        nwb_data=result,
        keep_road_numbers=config.keep_road_numbers,
        keep_rpe_codes=config.keep_rpe_codes,
    )

    return result


def download_nwb_shapefile(complete_url: str, config: NWBConfig) -> Response:
    """Download the NWB and return the HTTP response.

    Parameters
    ----------
    complete_url
        The complete URL with filter parameters.
    config
        The rest of the NWBConfig.

    Returns
    -------
    Response
        The HTTP Response if successful.

    Raises
    ------
    RuntimeError
        Raises a runtime error if any http exceptions were raised on client
        or server error.

    """
    try:
        response = requests.get(complete_url)
        response.raise_for_status()
        if response.status_code != 200:
            raise RuntimeError(f"Server error, status {response.status_code}")
    except requests.exceptions.RequestException as exception:
        raise RuntimeError(
            f"Unable to process NWB request for config: " f"{config.json()}"
        ) from exception
    return response


def apply_filters(
    nwb_data: gpd.GeoDataFrame,
    keep_road_numbers: List[str] = None,
    keep_rpe_codes: List[str] = None,
) -> gpd.GeoDataFrame:
    """Download the latest data from the NWB.

    Parameters
    ----------
    keep_road_numbers
        Which road numbers to keep. Keep in mind that this data works with leading zeroes,
        e.g. '009' for A9.
    keep_rpe_codes
        Which RPE codes to keep (i.e. which side of the highway) (default all, valid values
        are "L", "R" and "#").

    Returns
    -------
    gpd.GeoDataframe
        The input dataframe containing the NWB data for the selected region, filtered for
        the applicable filters.
    """
    result = nwb_data

    keep_road_numbers = keep_road_numbers or []
    keep_rpe_codes = keep_rpe_codes or ["L", "R", "#"]

    if len(keep_road_numbers) > 0:
        # Unfortunately, the WFS does not support querying for strings with leading zeros.
        result = result.query("wegnummer in @keep_road_numbers")

    result = result.query("rpe_code in @keep_rpe_codes")

    return result.copy()


def build_nwb_url(
    only_state_roads: bool = True, bbox: Tuple[float, float, float, float] = None
) -> str:
    """Download the latest data from the NWB.

    Parameters
    ----------
    only_state_roads
        Whether to only keep rijkswegen (much faster when True), fewer data of course.
    bbox
        The bounding box within which to get the data. Shall be of the format 'x0,y0,x1,y1'.

    Returns
    -------
    str
        The URL containing the applicable filters.
    """
    nwb_url = (
        "https://geodata.nationaalgeoregister.nl/nwbwegen/wfs?request=GetFeature"
        + "&service=WFS&typenames=wegvakken&version=2.0.0"
    )

    if only_state_roads:
        filter_url = (
            "&filter=<Filter><PropertyIsEqualTo><PropertyName>wegbehsrt</PropertyName>"
            + "<Literal>R</Literal></PropertyIsEqualTo></Filter>"
        )
    else:
        filter_url = ""

    if bbox:
        bbox_string = f"&bbox={','.join(str(i) for i in bbox)}"
    else:
        bbox_string = ""

    return nwb_url + filter_url + bbox_string
