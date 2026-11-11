"""
Ian Xia
CSE163 AD

This file contains functions that analyze the data in
nyc_volunteer_opportunities.csv, exploring the size of the data,
checking for missing values, and creating summaries and
visualizations of the variables of interest.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = 'data/nyc_volunteer_opportunities.csv'
COLUMNS = ["title", "summary", "category_desc"]


def load_data(path: str) -> pd.DataFrame:
    """
    Loads the CSV file at the given path and returns it as a
    DataFrame.
    """
    df = pd.read_csv(path)
    return df


def count_missing_data(df: pd.DataFrame) -> int:
    """
    Takes the full dataset and returns the number of rows that are
    missing a value in at least one of title, summary, or
    category_desc.
    """
    info = df[COLUMNS]
    missing_per_row = info.isnull().sum(axis=1)
    has_missing = missing_per_row > 0
    return has_missing.sum()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the full dataset and returns a new DataFrame with only the
    title, summary, and category_desc columns, excluding rows missing
    any of them. Adds a summary_words column holding the number of
    words in each summary.
    """
    cleaned = df[COLUMNS].dropna().copy()
    cleaned["summary_words"] = cleaned["summary"].str.split().str.len()
    return cleaned


def plot_category_counts(df: pd.DataFrame) -> None:
    """
    Saves a bar chart of the number of volunteer opportunities in
    each of the six categories of category_desc to
    plots/category_counts.png.
    """
    sns.catplot(data=df, y="category_desc", kind="count")
    plt.title("Volunteering Opportunities per Category")
    plt.xlabel("Number of opportunities")
    plt.ylabel("Category")
    plt.savefig("plots/category_counts.png", bbox_inches="tight")
    plt.close()


def plot_summary_length(df: pd.DataFrame) -> None:
    """
    Saves a histogram of the number of words in each opportunity's
    summary to plots/summary_length.png.
    """
    sns.histplot(data=df, x="summary_words")
    plt.title("Distribution of Summary Length")
    plt.xlabel("Words in summary")
    plt.ylabel("Number of opportunities")
    plt.savefig("plots/summary_length.png", bbox_inches="tight")
    plt.close()


def main():
    df = load_data(DATA_PATH)

    # Part One: size of the dataset
    row_count, col_count = df.shape
    print(f"Dataset has {row_count} rows and {col_count} columns")

    # Part Two: missing data in the columns of interest
    missing_data = count_missing_data(df)
    print(f"Dataset has {missing_data} rows with relevant missing data")

    # Part Three: summaries of each variable of interest
    cleaned = clean_data(df)
    print(cleaned["category_desc"].value_counts())
    print(cleaned["summary_words"].describe())

    # Part Four: plots
    plot_category_counts(cleaned)
    plot_summary_length(cleaned)

    # Result validity: count repeated postings (independence assumption)
    duplicates = cleaned.duplicated(subset=["title", "summary"]).sum()
    print(f"Dataset has {duplicates} duplicate title and summary pairs")


if __name__ == "__main__":
    main()
