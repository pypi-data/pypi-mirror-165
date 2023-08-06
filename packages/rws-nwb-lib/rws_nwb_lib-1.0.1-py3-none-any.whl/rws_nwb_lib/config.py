"""Configuration Module for NWB Lib."""
from typing import List, Optional, Tuple

from pydantic import BaseModel, validator


class NWBConfig(BaseModel):
    """NWB Config class.

    only_state_roads
        Whether to only keep state_roads (much faster when True),
        fewer data of course.
    output_file_path
        The file path to write the downloaded data to.
    keep_road_numbers
        Which road numbers to keep. Keep in mind that this data works with leading zeroes,
        e.g. '009' for A9.
    keep_rpe_codes
        Which RPE codes to keep (i.e. which side of the highway) (default all, valid values
        are "L", "R" and "#").
    bbox
        The bounding box within which to get the data. Shall be of the format 'x0,y0,x1,y1'.
    encoding
        The encoding to store the output in.

    """

    bounding_box: Optional[Tuple[float, float, float, float]] = None
    only_state_roads: bool = True
    keep_road_numbers: Optional[List[str]] = None
    keep_rpe_codes: Optional[List[str]] = None
    encoding: str = "utf-8"

    @validator("keep_rpe_codes")
    @classmethod
    def validate_rpe_codes(cls, value: List[str]) -> List[str]:
        """Validate road RPE codes.

        This method validates the RPE codes that can be specified. Valid
        codes can be "L", "R", and "#".

        Parameters
        ----------
        value
            List of RPE codes.

        Returns
        -------
        List[str]
            Validated input list.

        """
        if not len(value) > 0:
            raise ValueError("Specify at least one RPE code")
        invalid_codes = cls._get_invalid_codes(value)
        if any(invalid_codes):
            raise ValueError(
                f"Invalid RPE code(s) {invalid_codes}, supported are"
                f" {','.join(NWBConfig.valid_rpe_codes())}"
            )
        return value

    @staticmethod
    def valid_rpe_codes() -> List[str]:
        """Return all valid RPE codes.

        Returns
        -------
        List[str]
            Supported RPE codes.

        """
        return ["L", "R", "#"]

    @classmethod
    def _get_invalid_codes(cls, codes_list: List[str]) -> List[str]:
        """Return all invalid RPE codes in a list.

        This method returns the difference between the list of valid RPE
        codes and a supplied input list.

        Parameters
        ----------
        codes_list
            List of strings (RPE codes) to check.

        Returns
        -------
        List[str]
            List of invalid RPE codes.

        """
        invalid_codes = [
            i for i in codes_list if i not in NWBConfig.valid_rpe_codes() or i == ""
        ]
        return invalid_codes

    @validator("bounding_box")
    @classmethod
    def validate_bounding_box(
        cls, value: Tuple[float, float, float, float]
    ) -> Tuple[float, float, float, float]:
        """Validate the optional bounding box.

        This method checks to see if bounding box is correctly specified.

        Rules:

        x1 >x0, y1> y0
        all values must be positive >0

        Parameters
        ----------
        value
            The bounding box in form x0,y0,x1,y1.

        Returns
        -------
        Tuple[float,float,float,float]
            The validated bounding box.

        """
        for i in value:
            if i < 0:
                raise ValueError(f"Coordinate should be of positive value: {i}")
        if value[0] > value[2] or value[1] > value[3]:
            raise ValueError("x1 or y1 should be greater than x0 or y0")
        return value

    @validator("only_state_roads")
    @classmethod
    def validate_state_road_bbox_exclusivity(cls, value: bool, values: dict) -> bool:
        """Validate that only_state_roads/bounding_box are mutually exclusive.

        Parameters
        ----------
        value
            The only_state_roads variable
        values
            Other values from the model.

        Returns
        -------
        bool
            Returns only_state_roads if validated, otherwise raises
            ValidationError.

        """
        if value and "bounding_box" in values and values["bounding_box"] is not None:
            # This is not possible in the same URL params.
            raise AssertionError(
                "only_state_roads and bounding_box are "
                "mutually exclusive for this release"
            )
        return value
