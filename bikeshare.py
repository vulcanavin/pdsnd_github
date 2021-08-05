import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Args:
        None.
    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Initializing an empty city variable to store city choice from user
    #You will see this repeat throughout the program
    city = ''
    #Running this loop to ensure the correct user input gets selected else repeat
    while city not in CITY_DATA.keys():
        print("\nWelcome! Please choose your city:")
        #Taking user input and converting into lower to standardize them
        #You will find this happening at every stage of input throughout this
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nPlease check input, it doesn\'t appear to be conforming to any of the accepted input formats.")


    print(f"\nYou have chosen {city.title()} as your city.")

    #Creating a dictionary to store all the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nEnter month, between January to June, for which you're seeking the data:")
        print("\nAccepted input:\nFull month name")
        print("\n(You may also opt to view data for all months, please type 'all'.)")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid . Please try again in the accepted input format.")


    print(f"\nYou chose {month.title()} as your month.")

    #Creating a list to store all the days including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice for which you're seeking the data:")
        print("\n(You can also put 'all' or 'All' to view data for all days in a week.)")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please try again in one of the accepted input formats.")


    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*40)
    #Returning the city, month and day selections
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
    df = pd.read_csv(CITY_DATA[city])

#Convert the start tme column to date time
    df['Start Time']=pd.to_datetime(df['Start Time'])

    #Get month and day of week from Start time to create new columns named month and day_of_week respectively
    #month
    df['month']=df['Start Time'].dt.month
    #day of week
    df['day_of_week']=df['Start Time'].dt.day_name

    #filter by month
    if month != 'all':
        months=['january','february','march','april','may','june']
        month = months.index(month)+1

        df= df[df['month']==month]

    #filter by day of week
    if day != 'all':
        df=df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print('Most popular Day Of Week:', popular_day_of_week)

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_common_start_hour = df['hour'].mode()[0]

    print('Most Common Start Hour:', popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"the most common start station is {common_start_station}")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"the most common end station is {common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    df['Start to End']= df['Start Station'].str.cat(df['End Station'], sep=' to ')
    freq_combo=df['Start to End'].mode()[0]
    print(f"\n the most frequent combination of start and end station trip are from {freq_combo}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    average_duration=round(df['Trip Duration'].mean())
    print("avergae travel time", average_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"there are {user_type} user types")
    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print(f"there are {gender_count} counts of gender in the database")
    except:
        print("\n there is no gender column in this table")
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print(f"the earliest is {earliest}, the most recent is {recent}, the most common is {common}.")
    except:
        print("the Birth Year column is not present in the table")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")



    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*40)

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
