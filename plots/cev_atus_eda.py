import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CEV_PATH = 'data/cev_state_2017_2023.csv'
ATUS_PATH = 'data/time_use_2025.csv'


def load_data(path: str) -> pd.DataFrame:
    """
    Loads the CSV file at the given path and returns it as a
    DataFrame.
    """
    df = pd.read_csv(path)
    return df


def count_missing_data(df: pd.DataFrame) -> int:
    """
    Takes a dataset and returns the number of rows that are missing a
    value in at least one column.
    """
    missing_per_row = df.isnull().sum(axis=1)
    has_missing = missing_per_row > 0
    return has_missing.sum()


def clean_cev(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the full CEV dataset and returns a new DataFrame with a State
    column and one column per survey year (2017, 2019, 2021, 2023)
    holding the formal volunteering rate as a percentage.
    """
    cev_cleaned = pd.DataFrame()
    cev_cleaned['State'] = df['State']

    # 2017-2021 rates are strings like '33.8%'
    rates = df['State 2017 Formal Volunteering Rate']
    cev_cleaned['2017'] = rates.str.strip('%').astype(float)
    rates = df['State 2019 Formal Volunteering Rate']
    cev_cleaned['2019'] = rates.str.strip('%').astype(float)
    rates = df['State 2021 Formal Volunteering Rate']
    cev_cleaned['2021'] = rates.str.strip('%').astype(float)

    # 2023 rates are proportions like 0.328
    rates = df['State 2023 Formal Volunteering Rate']
    cev_cleaned['2023'] = rates * 100

    return cev_cleaned


def clean_atus(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the full ATUS dataset and returns a new DataFrame with an
    Activity column and men and women columns holding the average
    minutes per weekday spent on each activity.
    """
    atus_cleaned = pd.DataFrame()
    atus_cleaned['Activity'] = df['Activity']

    # the dataset gives hours per weekday; 60 minutes in an hour
    atus_cleaned['men'] = df['Average per weekday, men'] * 60
    atus_cleaned['women'] = df['Average per weekday, women'] * 60

    return atus_cleaned


def plot_state_trend(df: pd.DataFrame, state: str) -> None:
    """
    Saves a bar chart of the given state's formal volunteering rate in
    each survey year to plots/cev_state_trend.png.
    """
    years = ['2017', '2019', '2021', '2023']
    one_state = df[df['State'] == state]
    sns.barplot(data=one_state[years], color='blue')
    plt.title(f'Formal Volunteering Rate in {state}')
    plt.xlabel('Survey year')
    plt.ylabel('Formal volunteering rate (%)')
    plt.savefig('plots/cev_state_trend.png', bbox_inches='tight')
    plt.close()


def plot_rate_distribution(df: pd.DataFrame) -> None:
    """
    Saves a box plot of the formal volunteering rate across all states
    in each survey year to plots/cev_rate_distribution.png.
    """
    rates = df.drop(columns='State')
    sns.boxplot(data=rates, color='lightgrey')
    plt.title('Formal Volunteering Rate Across States by Year')
    plt.xlabel('Survey year')
    plt.ylabel('Formal volunteering rate (%)')
    plt.savefig('plots/cev_rate_distribution.png', bbox_inches='tight')
    plt.close()


def plot_weekday_volunteering(df: pd.DataFrame, activity: str) -> None:
    """
    Saves a bar chart of average weekday minutes that men and women
    spend in the given activity category to
    plots/atus_weekday_volunteering.png.
    """
    one_activity = df[df['Activity'] == activity]
    minutes = one_activity.drop(columns='Activity')
    sns.barplot(data=minutes)
    plt.title('Weekday Time in Organizational, Civic,\n'
              'and Religious Activities (ATUS 2025)')
    plt.xlabel('Group')
    plt.ylabel('Average minutes per weekday')
    plt.savefig('plots/atus_weekday_volunteering.png',
                bbox_inches='tight')
    plt.close()


def plot_activity_minutes(df: pd.DataFrame) -> None:
    """
    Saves a bar chart of average weekday minutes in every activity
    category for men and women to plots/atus_activity_minutes.png.
    """
    df.plot(x='Activity', kind='barh', figsize=(8, 6))
    plt.title('Average Weekday Minutes by Activity and Sex')
    plt.xlabel('Average minutes per weekday')
    plt.ylabel('Activity')
    plt.legend(title='Group')
    plt.savefig('plots/atus_activity_minutes.png', bbox_inches='tight')
    plt.close()


def main():
    atus_activity = 'Organizational, civic, and religious activities'

    cev_raw = load_data(CEV_PATH)
    print(f'CEV has {count_missing_data(cev_raw)} rows with missing data')
    cev = clean_cev(cev_raw)
    plot_state_trend(cev, 'WA')
    plot_rate_distribution(cev)

    atus_raw = load_data(ATUS_PATH)
    print(f'ATUS has {count_missing_data(atus_raw)} rows with missing '
          'data')
    atus = clean_atus(atus_raw)
    plot_weekday_volunteering(atus, atus_activity)
    plot_activity_minutes(atus)


if __name__ == '__main__':
    main()