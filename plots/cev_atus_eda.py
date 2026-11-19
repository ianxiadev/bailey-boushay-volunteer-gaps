"""
Dante Johnson
CSE 163
Section AE

These are the exploratory data analysis functions used
for analyzing CEV and ATUS data. The functions load the 
data, clean it, and create visualizations to explore the data.
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CEV_PATH = 'data/cev_state_level_summary.csv'
ACTIVITY_PATH = 'data/atusact_2025.dat'
RESPONDENT_PATH = 'data/atusresp_2025.dat'


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

    rates = df['State 2017 Formal Volunteering Rate']
    cev_cleaned['2017'] = rates.str.strip('%').astype('float')
    rates = df['State 2019 Formal Volunteering Rate']
    cev_cleaned['2019'] = rates.str.strip('%').astype('float')
    rates = df['State 2021 Formal Volunteering Rate']
    cev_cleaned['2021'] = rates.str.strip('%').astype('float')

    rates = df['State 2023 Formal Volunteering Rate']
    cev_cleaned['2023'] = rates * 100

    return cev_cleaned


def clean_volunteering(activities: pd.DataFrame,
                       respondents: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the ATUS activity and respondent files and returns one row per
    person who volunteered, holding their first volunteering activity of
    the diary day with its start hour, time period (Morning, Noon, or
    Night), the person's employment group (Employed or Not employed),
    and the activity's weighted percentage within that group.
    """
    people = respondents.loc[:, ['TUCASEID', 'TUFINLWGT', 'TELFS']]
    merged = activities.merge(people, left_on='TUCASEID',
                              right_on='TUCASEID')

    volunteering = merged[merged['TUTIER1CODE'] == 15]

    volunteering = volunteering.drop_duplicates('TUCASEID')

    start_minutes = volunteering['TUCUMDUR24'] - volunteering['TUACTDUR24']
    volunteering['start_hour'] = (4 + start_minutes // 60) % 24

    hour = volunteering['start_hour']
    is_morning = (hour >= 5) & (hour <= 13)
    is_noon = (hour >= 14) & (hour <= 18)
    volunteering['period'] = 'Night'
    volunteering.loc[is_morning, 'period'] = 'Morning'
    volunteering.loc[is_noon, 'period'] = 'Noon'

    is_employed = volunteering['TELFS'] <= 2
    volunteering['group'] = 'Not employed'
    volunteering.loc[is_employed, 'group'] = 'Employed'

    weights = volunteering['TUFINLWGT']
    employed_total = weights[is_employed].sum()
    not_employed_total = weights[~is_employed].sum()
    volunteering['percent'] = weights / not_employed_total * 100
    volunteering.loc[is_employed, 'percent'] = (
        weights[is_employed] / employed_total * 100)
    return volunteering


def plot_state_trend(df: pd.DataFrame, state: str) -> None:
    """
    Saves a bar graph of the given state's formal volunteering rate in
    each survey year to plots/cev_state_trend.png.
    """
    one_state = df[df['State'] == state]
    rates = one_state.loc[:, ['2017', '2019', '2021', '2023']]
    sns.barplot(data=rates, color='skyblue')
    plt.title('Formal Volunteering Rate in ' + state)
    plt.xlabel('Survey year')
    plt.ylabel('Formal volunteering rate (%)')
    plt.savefig('plots/cev_state_trend.png', bbox_inches='tight')
    plt.close()


def plot_state_change(df: pd.DataFrame, state: str) -> None:
    """
    Saves a bar graph of how much the given state's formal volunteering
    rate changed between each pair of survey years to
    plots/cev_state_change.png.
    """
    one_state = df[df['State'] == state]
    one_state['2017 to 2019'] = one_state['2019'] - one_state['2017']
    one_state['2019 to 2021'] = one_state['2021'] - one_state['2019']
    one_state['2021 to 2023'] = one_state['2023'] - one_state['2021']
    changes = one_state.loc[:, ['2017 to 2019', '2019 to 2021',
                                '2021 to 2023']]
    sns.barplot(data=changes, color='lightgreen')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title('Change in Formal Volunteering Rate in ' + state)
    plt.xlabel('Survey period')
    plt.ylabel('Change in percentage points')
    plt.savefig('plots/cev_state_change.png', bbox_inches='tight')
    plt.close()


def plot_volunteering_by_period(volunteering: pd.DataFrame) -> None:
    """
    Saves a bar graph comparing the percentage of employed and not
    employed volunteers whose volunteering started in the morning,
    noon, or night to plots/atus_volunteering_by_period.png.
    """
    sns.barplot(data=volunteering, x='period', y='percent', hue='group',
                estimator='sum', errorbar=None,
                order=['Morning', 'Noon', 'Night'])
    plt.title('When Volunteering Starts, by Employment')
    plt.xticks(range(3), ['5am-1pm', '2pm-6pm', '7pm-12am'])
    plt.xlabel('Start time')
    plt.ylabel('Volunteers in group (%)')
    plt.legend(title='Group')
    plt.savefig('plots/atus_volunteering_by_period.png',
                bbox_inches='tight')
    plt.close()


def plot_volunteering_overall(volunteering: pd.DataFrame) -> None:
    """
    Saves a histogram of the weighted percentage of all volunteers whose
    volunteering started in each hour of the day to
    plots/atus_volunteering_overall.png.
    """
    sns.histplot(data=volunteering, x='start_hour', weights='TUFINLWGT',
                 stat='percent', discrete=True)
    plt.xticks(range(0, 24, 2), ['12am', '2am', '4am', '6am', '8am',
                                 '10am', '12pm', '2pm', '4pm', '6pm',
                                 '8pm', '10pm'])
    plt.xlim(-0.5, 23.5)
    plt.title('When Volunteering Starts, All Volunteers')
    plt.xlabel('Start time')
    plt.ylabel('Volunteers (%)')
    plt.savefig('plots/atus_volunteering_overall.png', bbox_inches='tight')
    plt.close()


def main():
    cev_raw = load_data(CEV_PATH)
    # every column's Non-Null Count matches the number of rows, so no
    # data is missing
    cev_raw.info()
    cev = clean_cev(cev_raw)
    plot_state_trend(cev, 'WA')
    plot_state_change(cev, 'WA')

    activities = load_data(ACTIVITY_PATH)
    respondents = load_data(RESPONDENT_PATH)
    activities.loc[:, ['TUCASEID', 'TUTIER1CODE', 'TUCUMDUR24',
                       'TUACTDUR24']].info()
    respondents.loc[:, ['TUCASEID', 'TUFINLWGT', 'TELFS']].info()
    volunteering = clean_volunteering(activities, respondents)
    plot_volunteering_by_period(volunteering)
    plot_volunteering_overall(volunteering)


if __name__ == '__main__':
    main()