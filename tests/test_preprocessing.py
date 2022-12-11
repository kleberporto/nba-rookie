from math import isclose
from pandas import DataFrame
from numpy import nan

from nba_rookie.env import HEIGHT
from nba_rookie.preprocessing import Preprocessor

preprocessor = Preprocessor()


def test__treat_position():
    test_data = {"position": ["C", "G", "F-C", "G-F", "F"]}
    test_df = DataFrame(test_data)

    return_df = preprocessor._treat_position(test_df)

    for position in return_df.position.to_list():
        assert len(position) < 2

    assert return_df["has_second_position"].tolist() == [
        False,
        False,
        True,
        True,
        False,
    ]
    assert return_df.position.tolist() == ["C", "G", "F", "G", "F"]


def test__treat_position_with_nan():
    test_data = {"position": ["C", nan]}
    test_df = DataFrame(test_data)

    return_df = preprocessor._treat_position(test_df)

    assert len(return_df) == 1
    assert return_df.position.tolist() == ["C"]


def test__inches_to_meters():
    assert isclose(preprocessor._inches_to_meters(1.0), 0.0254)
    assert isclose(preprocessor._inches_to_meters(2.0), 0.0508)
    assert isclose(preprocessor._inches_to_meters(3.0), 0.0762)
    assert isclose(preprocessor._inches_to_meters(4.0), 0.1016)


def test__feet_to_meters():
    assert isclose(preprocessor._feet_to_meters(1.0), 0.3048)
    assert isclose(preprocessor._feet_to_meters(2.0), 0.6096)
    assert isclose(preprocessor._feet_to_meters(3.0), 0.9144)
    assert isclose(preprocessor._feet_to_meters(4.0), 1.2192)


def test__convert_height():
    test_data = {HEIGHT: ["6-4", "7-0", "5-8"]}
    test_df = DataFrame(test_data)

    return_df = preprocessor._treat_height(test_df)
    return_data = return_df[HEIGHT].tolist()

    assert isclose(return_data[0], 1.9304)
    assert isclose(return_data[1], 2.1336)
    assert isclose(return_data[2], 1.7272)
