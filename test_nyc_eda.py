"""
Ian Xia
CSE163 AD

Tests the functions in nyc_eda.py using test_data/small_nyc.csv, a
6-row file whose correct answers were worked out by hand.
"""

import nyc_eda

SMALL_PATH = 'test_data/small_nyc.csv'


def test_load_data() -> None:
    """
    Tests the function load_data.
    """
    df = nyc_eda.load_data(SMALL_PATH)
    assert df.shape == (6, 5)
    assert df.loc[0, "title"] == "Tutor Kids"


def test_count_missing_data() -> None:
    """
    Tests the function count_missing_data.
    """
    df = nyc_eda.load_data(SMALL_PATH)
    assert nyc_eda.count_missing_data(df) == 1


def test_clean_data() -> None:
    """
    Tests the function clean_data.
    """
    df = nyc_eda.load_data(SMALL_PATH)
    cleaned = nyc_eda.clean_data(df)
    assert cleaned.shape == (5, 4)
    assert list(cleaned.columns) == ["title", "summary",
                                     "category_desc", "summary_words"]
    assert "Block Party" not in list(cleaned["title"])
    assert cleaned["category_desc"].isnull().sum() == 0
    assert list(cleaned["summary_words"]) == [5, 6, 5, 5, 2]
    assert df.shape == (6, 5)


def test_summaries() -> None:
    """
    Tests the category counts and word count summary printed in main,
    using the cleaned small dataset.
    """
    cleaned = nyc_eda.clean_data(nyc_eda.load_data(SMALL_PATH))

    counts = cleaned["category_desc"].value_counts()
    assert counts["Education"] == 3
    assert counts["Environment"] == 1
    assert counts["Helping Neighbors in Need"] == 1

    summary = cleaned["summary_words"].describe()
    assert summary["mean"] == 23 / 5
    assert summary["min"] == 2
    assert summary["50%"] == 5
    assert summary["max"] == 6

    duplicates = cleaned.duplicated(subset=["title", "summary"]).sum()
    assert duplicates == 1


def main():
    test_load_data()
    test_count_missing_data()
    test_clean_data()
    test_summaries()
    print("All tests passed!")


if __name__ == "__main__":
    main()
