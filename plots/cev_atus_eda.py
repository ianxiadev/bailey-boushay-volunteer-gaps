import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CEV_PATH = 'data/cev_state_level_summary.csv'
ATUS_PATH = 'data/american_time_use_survey.csv'


def load_data(path: str) -> pd.DataFrame:
    """
    Loads the CSV file at the given path and returns it as a
    DataFrame.
    """
    df = pd.read_csv(path)
    return df


def clean_cev(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the full CEV dataset and returns a new DataFrame with a State
    column and one column per survey year (2017, 2019, 2021, 2023)
    holding the formal volunteering rate as a percentage.
    """
    cev_cleaned = df.loc[:, ['State']]

    # 2017-2021 rates are strings like '33.8%'
    rates = df['State 2017 Formal Volunteering Rate']
    cev_cleaned['2017'] = rates.str.strip('%').astype('float')
    rates = df['State 2019 Formal Volunteering Rate']
    cev_cleaned['2019'] = rates.str.strip('%').astype('float')
    rates = df['State 2021 Formal Volunteering Rate']
    cev_cleaned['2021'] = rates.str.strip('%').astype('float')

    # 2023 rates are proportions like 0.328
    rates = df['State 2023 Formal Volunteering Rate']
    cev_cleaned['2023'] = rates * 100

    return cev_cleaned


def clean_atus(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the full ATUS dataset and returns a new DataFrame with an
    Activity column and the average minutes per weekday and per weekend
    day that men and women spend on each activity.
    """
    atus_cleaned = df.loc[:, ['Activity']]

    # the dataset gives hours per day; 60 minutes in an hour
    atus_cleaned['men weekday'] = df['Average per weekday, men'] * 60
    atus_cleaned['women weekday'] = df['Average per weekday, women'] * 60
    atus_cleaned['men weekend'] = df['Average per weekend day, men'] * 60
    atus_cleaned['women weekend'] = df['Average per weekend day, women'] * 60

    return atus_cleaned


def plot_state_trend(df: pd.DataFrame, state: str) -> None:
    """
    Saves a bar chart of the given state's formal volunteering rate in
    each survey year to plots/cev_state_trend.png.
    """
    one_state = df[df['State'] == state]
    rates = one_state.loc[:, ['2017', '2019', '2021', '2023']]
    sns.barplot(data=rates, color='tab:blue')
    plt.title('Formal Volunteering Rate in ' + state)
    plt.xlabel('Survey year')
    plt.ylabel('Formal volunteering rate (%)')
    plt.savefig('plots/cev_state_trend.png', bbox_inches='tight')
    plt.close()


def plot_state_change(df: pd.DataFrame, state: str) -> None:
    """
    Saves a bar chart of how much the given state's formal volunteering
    rate changed between each pair of survey years to
    plots/cev_state_change.png.
    """
    one_state = df[df['State'] == state]
    one_state['2017 to 2019'] = one_state['2019'] - one_state['2017']
    one_state['2019 to 2021'] = one_state['2021'] - one_state['2019']
    one_state['2021 to 2023'] = one_state['2023'] - one_state['2021']
    changes = one_state.loc[:, ['2017 to 2019', '2019 to 2021',
                                '2021 to 2023']]
    sns.barplot(data=changes, color='tab:blue')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title('Change in Formal Volunteering Rate in ' + state)
    plt.xlabel('Survey period')
    plt.ylabel('Change in percentage points')
    plt.savefig('plots/cev_state_change.png', bbox_inches='tight')
    plt.close()


def plot_weekday_volunteering(df: pd.DataFrame, activity: str) -> None:
    """
    Saves a bar chart of average weekday minutes that men and women
    spend in the given activity category to
    plots/atus_weekday_volunteering.png.
    """
    one_activity = df[df['Activity'] == activity]
    minutes = one_activity.loc[:, ['men weekday', 'women weekday']]
    sns.barplot(data=minutes)
    plt.title('Weekday Time in Organizational, Civic,\n'
              'and Religious Activities (ATUS 2025)')
    plt.xlabel('Group')
    plt.ylabel('Average minutes per weekday')
    plt.savefig('plots/atus_weekday_volunteering.png',
                bbox_inches='tight')
    plt.close()


def plot_weekday_vs_weekend(df: pd.DataFrame, activity: str) -> None:
    """
    Saves a bar chart comparing average weekday and weekend minutes that
    men and women spend in the given activity category to
    plots/atus_weekday_vs_weekend.png.
    """
    one_activity = df[df['Activity'] == activity]
    minutes = one_activity.loc[:, ['men weekday', 'women weekday',
                                   'men weekend', 'women weekend']]
    sns.barplot(data=minutes, color='tab:blue')
    plt.title('Weekday vs. Weekend Time in Organizational, Civic,\n'
              'and Religious Activities (ATUS 2025)')
    plt.xlabel('Group and day type')
    plt.ylabel('Average minutes per day')
    plt.savefig('plots/atus_weekday_vs_weekend.png', bbox_inches='tight')
    plt.close()


def main():
    atus_activity = 'Organizational, civic, and religious activities'

    cev_raw = load_data(CEV_PATH)
    # every column's Non-Null Count matches the number of rows, so no
    # data is missing
    cev_raw.info()
    cev = clean_cev(cev_raw)
    plot_state_trend(cev, 'WA')
    plot_state_change(cev, 'WA')

    atus_raw = load_data(ATUS_PATH)
    atus_raw.info()
    atus = clean_atus(atus_raw)
    plot_weekday_volunteering(atus, atus_activity)
    plot_weekday_vs_weekend(atus, atus_activity)


if __name__ == '__main__':
    main()