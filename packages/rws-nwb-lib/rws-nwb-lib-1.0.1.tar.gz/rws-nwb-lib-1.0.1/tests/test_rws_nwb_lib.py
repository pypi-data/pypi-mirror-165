import os
import pytest
from unittest import mock
from pydantic import ValidationError
from requests import RequestException

from rws_nwb_lib import process_nwb, NWBConfig


def test_nwb_config():
    # default config
    default_conf = NWBConfig()
    assert not any(
        (
            default_conf.bounding_box,
            default_conf.keep_road_numbers,
            default_conf.keep_rpe_codes,
        )
    )
    assert default_conf.only_state_roads

    with pytest.raises(ValidationError):
        NWBConfig(bounding_box=(1, 2, 3))
    with pytest.raises(ValidationError):
        NWBConfig(bounding_box=("test", 1, 2, 3))
    with pytest.raises(ValidationError):
        NWBConfig(keep_rpe_codes=None)
    with pytest.raises(ValidationError):
        NWBConfig(keep_rpe_codes=[])
    with pytest.raises(ValidationError):
        NWBConfig(keep_rpe_codes=["T"])

    conf = NWBConfig(keep_rpe_codes=["L"])
    assert "L" in conf.keep_rpe_codes

    NWBConfig(bounding_box=(0, 0, 1, 1))

    with pytest.raises(ValidationError):
        NWBConfig(bounding_box=(0, 1, 1, 0))
    with pytest.raises(ValidationError):
        NWBConfig(bounding_box=(-1, 0, 1, 1))

    with pytest.raises(ValidationError):
        NWBConfig(bounding_box=(123, 456, 789, 999), only_state_roads=True)


def test_nwb_a9r():
    nwb_a9r = process_nwb(
        NWBConfig(keep_road_numbers=["009"], keep_rpe_codes=["R", "#"])
    )

    # Length as of 2022-07-08
    assert len(nwb_a9r) >= 265
    os.remove("nwb.gml")


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


def mocked_requests_req_exception(*args, **kwargs):
    class ExceptionResponse(MockResponse):
        def raise_for_status(self):
            raise RequestException

    return ExceptionResponse({"body": "maakt niet uit."}, 404)


def mocked_requests_get_404(*args, **kwargs):

    return MockResponse({"body": "maakt niet uit."}, 404)


@mock.patch("requests.get", side_effect=mocked_requests_get_404)
def test_faulty_response(mock_get):
    with pytest.raises(RuntimeError):
        process_nwb(NWBConfig(only_state_roads=True))


@mock.patch("requests.get", side_effect=mocked_requests_req_exception)
def test_other_connection_error(mock_get):
    with pytest.raises(RuntimeError):
        process_nwb(NWBConfig(only_state_roads=True))


def test_rijkswegen_only():
    nl_rijkswegen = process_nwb(NWBConfig(only_state_roads=True))

    # Length as of 2022-07-08
    assert len(nl_rijkswegen) >= 17771

    os.remove("nwb.gml")


def test_bbox():
    nl_all_roads = process_nwb(
        NWBConfig(only_state_roads=False, bounding_box=(52.01, 4.22, 52.05, 4.25))
    )
    os.remove("nwb.gml")


def test_invalid_bbox():
    with pytest.raises(ValidationError):
        process_nwb(config=NWBConfig(bounding_box=(123, 456), only_state_roads=False))
