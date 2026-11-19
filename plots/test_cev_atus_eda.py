"""
Dante Johnson
CSE 163
Section AE

Tests the data cleaning and plotting functions in 
cev_atus_eda.py with assert statements. 
"""
from cev_atus_eda import (load_data, clean_cev, clean_volunteering,
                          plot_state_trend, plot_state_change,
                          plot_volunteering_by_period,
                          plot_volunteering_overall)


def test_clean_cev() -> None:
    """
    Checks that clean_cev keeps State and the four years and turns both
    rate formats ('35.7%' and 0.328) into percentages.
    """
    cev = clean_cev(load_data('data/small_cev.csv'))
    assert cev.shape == (3, 5)
    assert cev.columns[0] == 'State'
    assert cev.loc[0, '2017'] == 35.7
    assert round(cev.loc[0, '2023'], 1) == 32.8


def test_clean_volunteering() -> None:
    """
    Checks that clean_volunteering keeps one row per volunteer and gives
    the right start hour, group, and percentages.
    """
    activities = load_data('data/small_atus_act.csv')
    respondents = load_data('data/small_atus_resp.csv')
    vol = clean_volunteering(activities, respondents)
    assert len(vol) == 6
    assert vol[vol['TUCASEID'] == 1]['start_hour'].max() == 7
    assert vol[vol['TUCASEID'] == 2]['group'].max() == 'Employed'
    assert vol[vol['group'] == 'Employed']['percent'].sum() == 100


def test_plot_state_trend() -> None:
    """
    Checks that plot_state_trend runs and does not change the data.
    """
    cev = clean_cev(load_data('data/small_cev.csv'))
    assert plot_state_trend(cev, 'WA') is None
    assert cev.shape == (3, 5)
    assert cev.loc[0, 'State'] == 'WA'
    assert cev.loc[0, '2017'] == 35.7


def test_plot_state_change() -> None:
    """
    Checks that plot_state_change runs and does not add its change
    columns to the data.
    """
    cev = clean_cev(load_data('data/small_cev.csv'))
    assert plot_state_change(cev, 'WA') is None
    assert cev.shape == (3, 5)
    assert '2019 to 2021' not in cev.columns
    assert cev.loc[0, '2021'] == 25.0


def test_plot_volunteering_by_period() -> None:
    """
    Checks that plot_volunteering_by_period runs and does not change the
    data.
    """
    activities = load_data('data/small_atus_act.csv')
    respondents = load_data('data/small_atus_resp.csv')
    vol = clean_volunteering(activities, respondents)
    shape = vol.shape
    assert plot_volunteering_by_period(vol) is None
    assert vol.shape == shape
    assert vol['percent'].sum() == 200
    assert vol[vol['TUCASEID'] == 1]['period'].max() == 'Morning'


def test_plot_volunteering_overall() -> None:
    """
    Checks that plot_volunteering_overall runs and does not change the
    data.
    """
    activities = load_data('data/small_atus_act.csv')
    respondents = load_data('data/small_atus_resp.csv')
    vol = clean_volunteering(activities, respondents)
    shape = vol.shape
    assert plot_volunteering_overall(vol) is None
    assert vol.shape == shape
    assert vol['start_hour'].min() == 0
    assert vol['start_hour'].max() == 19


def main():
    test_clean_cev()
    test_clean_volunteering()
    test_plot_state_trend()
    test_plot_state_change()
    test_plot_volunteering_by_period()
    test_plot_volunteering_overall()
    print('All tests passed')


if __name__ == '__main__':
    main()