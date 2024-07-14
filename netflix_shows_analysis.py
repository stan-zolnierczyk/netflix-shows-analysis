# Importing pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Read in the Netflix CSV as a DataFrame
netflix_df = pd.read_csv("netflix_data.csv")

# Check the shape of the dataframe. The result is (number fo rows, number of columns)
netflix_df.shape

# Print the first 10 rows of the dataframe to see names of the headers and what kind of data is stored in each column
netflix_df.head(10)

#Other health checks
netflix_df.describe()
netflix_df.columns
print(netflix_df.isna().sum())

# Check how many shows are there in the database by type of show
types_sum = netflix_df.groupby('type').count()
print(types_sum['show_id'])

# Create a pie chart out of these data
type_counts = types_sum['show_id']
plt.figure(figsize=(8, 8))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=100)

plt.title('Distribution of Netflix shows by Type')
plt.show()

# Check how many shows are there in the database by genre
genres_sum = netflix_df.groupby('genre').size().reset_index(name='count')
# Sort the results with most frequent on top
genres_sum_sorted = genres_sum.sort_values(by='count', ascending=False)

print(genres_sum_sorted.to_string(index=False))
# Count the number of genres
number_of_genres = len(genres_sum)
print('Total number of genres: ' + str(number_of_genres))

#check how many shows are there in the database by country of origin. Display in alphabetical order
coutries_sum = netflix_df.groupby('country').count()
print(coutries_sum['show_id'])

#check how many shows are there in the database by year of release
years_sum = netflix_df.groupby('release_year').count()

# Build a bar plot for the data.
plt.figure(figsize=(14, 11))
graph = plt.barh(years_sum.index, years_sum['show_id'], color='blue')

# Add value-as-text next to each bar
for bar in graph:
    xval = bar.get_width()
    plt.text(xval + 1, bar.get_y() + bar.get_height()/2, int(xval), ha='left', va='center')

# Strings
xlab = 'Number of shows'
ylab = 'Year of release'
title = 'Number of shows released on Netflix each year'

# Add axis labels
plt.xlabel(xlab)
plt.ylabel(ylab)
# Add title
plt.title(title)

# display the plot after customizing
plt.show()

# Extract Movies only (drop TV shows)
movies_only = netflix_df[netflix_df['type'] == 'Movie']

# Further subset the data: select movies from the nineties
movies_1990s = movies_only[(movies_only['release_year'] >= 1990) & (movies_only['release_year'] <= 1999)]

# calculate the mean duration of the above subset
duration1 = round(movies_1990s['duration'].mean())
print('The mean duration of all movies released between 1990 and 1999 is ' + str(duration1) + ' min')

#Group movies form 1990s by duration and count occurrences
movies_1990s_duration = movies_1990s.groupby('duration').count()

# Get the index name (so the duration) of the row with the most counts. (all the colums are the same, so take one of them)
# Convert the result to regular integer
duration = int(movies_1990s_duration['show_id'].idxmax())
print('The most frequent movie duration released between 1990 and 1999 is ' + str(duration) + ' min')

# Build a bar plot for the data.
plt.figure(figsize=(15, 6))
graph = plt.bar(movies_1990s_duration.index, movies_1990s_duration['show_id'], color='green')

# Add value-as-text above a bar which represents max value
maxval = 0
for bar in graph:
    yval = bar.get_height()
    if yval > maxval:
        xval = bar.get_x() + bar.get_width()/2
        maxval = yval
plt.text(xval, maxval, int(xval), ha='center', va='bottom')

# Strings
xlab = 'Duration [min]'
ylab = 'Number of movies'
title = 'Most frequent movie duration in the 1990s'

# Add axis labels
plt.xlabel(xlab)
plt.ylabel(ylab)
# Add title
plt.title(title)

# display the plot after customizing
plt.show()

# Calculate the mean duration of the shows released in a given year.
mean_duration_by_year = netflix_df.groupby('release_year')['duration'].mean()

# Build a bar plot for the data.
plt.figure(figsize=(15, 6))
graph = plt.bar(mean_duration_by_year.index, mean_duration_by_year, color='pink')

# Add axis labels
plt.xlabel('Release year')
plt.ylabel('Duration [min]')
# Add title
plt.title('Average duration of Netflix shows released in a given year')

# Extract Action Movies only (drop TV shows)
action_movies = netflix_df[(netflix_df['type'] == 'Movie') & (netflix_df['genre'] == 'Action')]

# Further subset data: select movies from the nineties
action_movies_1990s = action_movies[(action_movies['release_year'] >= 1990) & (action_movies['release_year'] <= 1999)]

# Declare the counter for the task
short_movie_count = 0
#count the movies which are shorter than 90min
for index, row in action_movies_1990s.iterrows():
    if row['duration'] < 90:
        short_movie_count += 1

print('Asnwer: In the given database there are ' + str(short_movie_count) + ' action movies made in the 1990s which are shorter than 90 minutes.')

# Group data by release year and genre, count the number of occurrences
genre_counts_by_year = netflix_df.groupby(['release_year', 'genre']).size().reset_index(name='count')

# Group by release year and calculate the total number of occurrences in each year
total_counts_by_year = netflix_df.groupby('release_year').size().reset_index(name='total_count')

# Merge both tables to get the total number of occurrences in each year
merged_df = pd.merge(genre_counts_by_year, total_counts_by_year, on='release_year')

# Calculate the percentage share of each genre in a given year
merged_df['percentage'] = (merged_df['count'] / merged_df['total_count']) * 100

# Pivot the data to a wide format for the bar chart
pivot_df = merged_df.pivot(index='release_year', columns='genre', values='percentage')

# Fill missing values with zeros
pivot_df = pivot_df.fillna(0)

# Create the bar chart
pivot_df.plot(kind='bar', stacked=True, figsize=(14, 8))

# Add title and axis labels
plt.title('Percentage Share of Genres by Year')
plt.xlabel('Release Year')
plt.ylabel('Percentage Share')

# Add legend
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the chart
plt.tight_layout()
plt.show()

# Based on previos querries, we already know that 4 most frequently released genres are: Dramas, Comedies, Action and Children
popular_genres_percentage = pivot_df[['Dramas', 'Comedies', 'Action', 'Children']]

# And we are interested in analyzing the last 30 years only
recent_popular_genres_percentage = popular_genres_percentage[(popular_genres_percentage.index >= 1990) & (popular_genres_percentage.index <= 2020)]

# Let's build a graph out of that data frame
plt.figure(figsize=(15, 6))
plt.plot(recent_popular_genres_percentage.index, recent_popular_genres_percentage['Dramas'], label='Dramas', color='green')
plt.plot(recent_popular_genres_percentage.index, recent_popular_genres_percentage['Comedies'], label='Comedies', color='grey')
plt.plot(recent_popular_genres_percentage.index, recent_popular_genres_percentage['Action'], label='Action', color='blue')
plt.plot(recent_popular_genres_percentage.index, recent_popular_genres_percentage['Children'], label='Children', color='purple')

# Add Labels and title
plt.xlabel('Release Year')
plt.ylabel('Percentage (%)')
plt.title('Genre Distribution Over the Years')
# Add legend
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# I already have genre_counts_by_year calculated before
# Pivot the data to a wide format for the chart. Fill missing values with zeros
pivot_2 = genre_counts_by_year.pivot(index='release_year', columns='genre', values='count').fillna(0)
# Calculate cumulative sum of each genre
cum_genre_counts_by_year = pivot_2.cumsum()

# Take that 4 most frequently released genres
cum_popular_genres = cum_genre_counts_by_year[['Dramas', 'Comedies', 'Action', 'Children']]

# Take the last 30 years only
recent_cum_popular_genres = cum_popular_genres[(cum_popular_genres.index >= 2010) & (cum_popular_genres.index <= 2020)]

# A graph out of that data frame
plt.figure(figsize=(15, 6))
plt.plot(recent_cum_popular_genres.index, recent_cum_popular_genres['Dramas'], label='Dramas', color='green')
plt.plot(recent_cum_popular_genres.index, recent_cum_popular_genres['Comedies'], label='Comedies', color='grey')
plt.plot(recent_cum_popular_genres.index, recent_cum_popular_genres['Action'], label='Action', color='blue')
plt.plot(recent_cum_popular_genres.index, recent_cum_popular_genres['Children'], label='Children', color='purple')

# Add Labels and title
plt.xlabel('Release Year')
plt.ylabel('Cumulative Sum')
plt.title('Cumulative Sum: 4 most frequently released genres 2010-2020')
# Add legend
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Take that 4 most frequently released genres
popular_genres = pivot_2[['Dramas', 'Comedies', 'Action', 'Children']]

# Take the last 30 years only
recent_popular_genres = popular_genres[(popular_genres.index >= 2010) & (popular_genres.index <= 2020)]

# A graph out of that data frame
plt.figure(figsize=(15, 6))
plt.plot(recent_popular_genres.index, recent_popular_genres['Dramas'], label='Dramas', color='green')
plt.plot(recent_popular_genres.index, recent_popular_genres['Comedies'], label='Comedies', color='grey')
plt.plot(recent_popular_genres.index, recent_popular_genres['Action'], label='Action', color='blue')
plt.plot(recent_popular_genres.index, recent_popular_genres['Children'], label='Children', color='purple')

# Add Labels and title
plt.xlabel('Release Year')
plt.ylabel('Number of shows released')
plt.title('Number of shows released Over the Years')
# Add legend
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()