import time, calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # gets user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data from Chicago, New York City, or Washington?\n').lower()
        if city in (CITY_DATA):
            print('You have selected to view the data of {}\n'.format(city).title())
            break
        else:
            print('\nYou have not selected a valid city. Please try again...')
            continue
    # gets user input for month (all, january, february, ... , june)
    while True:
        month = input('What month would you like to filter by? Enter: January, February, March, April, May, June, or All:\n').lower()
        months = ['all','january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            print('You have selected: {}\n'.format(month).title())
            break
        else:
            print('\nYou have not selected a valid month. Please try again...')
            continue
    # gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day would you like to filter by? Enter: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All:\n').lower()
        days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day not in days:
            print('\nYou have not selected a valid day of the week. Please try again...')
            continue
        else:
            print('You have selected: {}\n'.format(day).title())
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month = calendar.month_name[common_month]
    print('The most popular month is: {}.\n'.format(common_month))
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week is: {}.\n'.format(common_day))
    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most popular start time is: {}.\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most popular used start station is: {}.\n'.format(common_start_station))
    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('The most popular used end station is: {}.\n'.format(common_end_station))
    # display most frequent combination of start station and end station trip
    common_combination_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most popular combination of stations is:\n{}\n'.format(common_combination_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total number of trips
    trip_count = df['Trip Duration'].count()
    print('The total number of trips is: {}.\n'.format(trip_count))
    # display total travel time
    total_trip_duration = df['Trip Duration'].sum() / 60 / 60 / 24
    print('The total time travelled is: {} days.\n'.format(total_trip_duration))
    # display mean travel time
    average_trip_duration = df['Trip Duration'].mean() / 60
    print('The average trip time is: {} minutes.\n'.format(average_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of the user types are:\n', user_types)

    try:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nThe counts per gender are:\n', gender_count)
    except KeyError:
        print('\nNo gender data available for the selected city.')

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest birth year is: {}.\n'.format(earliest_year))
        latest_year = df['Birth Year'].max()
        print('The latest birth year is: {}.\n'.format(latest_year))
        common_year = df['Birth Year'].mode()[0]
        print('The most common birth year is: {}.\n'.format(common_year))
    except KeyError:
        print('\nNo birth year data available for the selected city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks if the user would like to see lines of data from the filtered dataset.
    Displays 5 lines, then asks if they would like to see more.
    Continues asking until they say no."""
    i = 0
    view_data = input('\nWould you like to view individual trip data? Please type yes or no.\n').lower()
    while view_data == 'yes' and i+5 < df.shape[0]:
        if view_data == 'no':
            print('Data viewing ended.')
            break
        five_rows = df.iloc[i:i+5]
        print(five_rows)
        view_data = input('\nWould you like to view the next 5 rows of individual trip data? Please type yes or no.\n').lower()
        i += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()