#!/usr/bin/env python3
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the database and read the data into a DataFrame
conn = sqlite3.connect('/Users/danipan/Desktop/Friendship-Reserve/chat.db')
df = pd.read_sql_query("SELECT date, text, phone_number FROM merged_egg_2023_q1", conn)

# Convert the date column to a pandas datetime format and adjust timezone
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')


# Extract hour and weekday from the date column
df['hour'] = df['date'].dt.hour
df['weekday'] = df['date'].dt.strftime('%A')

# Define the order of weekdays
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Convert the 'weekday' column to a categorical variable with the defined order
df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True)


# Sort the DataFrame by the weekday order
df = df.sort_values('weekday')


# Group the data by hour and weekday and count the number of texts
df = df.groupby(['hour', 'weekday']).count()


# Pivot the data to create a matrix of hours vs. weekdays
df = df.pivot_table(index='hour', columns='weekday', values='text')

# Create a heatmap of the data using seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(df, cmap='coolwarm', square=True, cbar_kws={'label': 'Number of texts'}, center=df.values.min())
plt.title('Activity heatmap')
plt.xlabel('Weekday')
plt.ylabel('Hour (EST) ')
plt.show()

