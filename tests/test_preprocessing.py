from numpy import nan
from pandas import DataFrame
from nba_rookie.preprocessing import treat_position


def test__treat_position():
    test_data = {"position": ["C", "G", "F-C", "G-F", "F"]}
    test_df = DataFrame(test_data)

    return_df = treat_position(test_df)

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

    return_df = treat_position(test_df)

    print(return_df)

    assert len(return_df) == 1
    assert return_df.position.tolist() == ["C"]
