# Python Practice 3: Basic Data Engineering Pipeline

# Background: I've picked up on a couple of key python concepts that I was more unfamiliar with, so I want to learn more data engineering-related concepts and packages. I will be performing
#             all of the basic data engineering responsibilities for this small movies dataset utilizing new concepts and functions that I've learned recently.
#             I've learned about environment files, iteration and string tools, more ways to use the datetime and collections packages, and writing to files in alternative ways, which will
#             all be shown in this file.

# Side note: Package combos I will learn for future package practice: PySpark(high priority), pytest(high priority), pydantic (high priority), requests and beautifulsoup4 (bs4) (mid priority),
#  dlt (mid priority), duckdb and polaris (mid priority), loguru and typer and fire (low priority), ruff (goes hand and hand with rust) (low priority)

# Side note 2: Scala and Java seem to be important as a data engineer too - focus on python first and foremost, but Java and Scala could be languages I learn next


# Goal: Grow more familiar with packages and tools that data engineers use. Know when to use these packages and tools for the future.

# Project: 
#     - Load config from .env instead of hardcoding the dataset URL.
#     - Use try/except when loading the file so the script doesn’t crash on bad URLs.
#     - Clean strings — trim spaces, make consistent casing in country and rating.
#     - Extract month & day from date_added (date handling).
#     - Count content types using collections.Counter.
#     - Filter dataset to only include the top 5 movies with the highest average audience/critic score
#     - Write a summary text file (File I/O) with human-readable results.


# Day 1: Researched each of the new concepts and read up on unfamiliar terms, experimented with the environment files, found appropriate data to use, debugged the file reading method

# Day 2: Python self-study. Before I jumped into further into this project, I explored concepts I was unfamiliar with on YouTube. I went over the logistics of different programming
#        languages that data engineers use and why they would use them (Scala and Java), reading/writing/handling different types of files and learning further about how to differentiate
#        them, finally learning advanced method chaining, and learning more about APIs and data pipelines, among other things. Today, I went over a lot of small things that I was
#        wondering more about and just decided to learn them. 

# Day 3  Practiced cleaning data with fillna, imputing missing data with my own formulas, learned a bunch about datetime functions and how to change the date and time around to
#        different time zones, and dipped my feet into more complex data cleaning with np.where and masks.

# Day 4 (Short day): Learned how to write a file from scratch, learned how to utilize enumerate and zip, reorganized some code, added an extra variable, troubleshooted some issues.

# COMPLETED ON DAY 4



# Step 0: Reading data with help from .env file

# Importing packages and reading in the MCU dataset from my .env file
import sys
import pandas as pd
import os
import numpy as np
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter

# Setting it so that I can see all the data
pd.set_option("display.max_columns", None)
pd.set_option('display.width', 220)

# Find .env file in case it is in a directory in higher directories
dotenv_path = find_dotenv()

# Making it so that environment variables can be found from the .env file
load_dotenv(dotenv_path)

# Getting the file I want from the secret file name
movie_file1 = os.getenv("MOVIE_FILE")

# Reading the data file as a csv if it can be read in correctly, and specifying what went wrong if it cannot be read in
try:
    movie_df = pd.read_csv(movie_file1)
    print(movie_df.head(2))
except Exception as e:
    print(f"Failure reading in dataset due to {e}")
    sys.exit()
finally:
    print("Done!")



# Step 1: Add extra movies with missing data
movie_df.loc[len(movie_df)] = {"movie": "black Widow", "release_date": "9-Jul-21", "release_order": 24.0, "chronological_order": 24.0, "rt_critic_score": 60.0, "rt_audience_score": 65}
movie_df.loc[len(movie_df)] = {"movie": "guardians of the Galaxy Vol. 3", "release_date": "5-May-23", "release_order": 25.0, "chronological_order": 25.0, \
                               "rt_critic_score": 85, "rt_audience_score": 90.0}

# Step 2: Cleaning the data
movie_df = movie_df.dropna(subset = ["movie"])
movie_df["movie"] = movie_df["movie"].str.title().astype(str)

### Step 2.5: Modifying the release date some and utilizing some other datetime functions with newly added columns
movie_df["release_date"] = pd.to_datetime(movie_df["release_date"], format = "%d-%b-%y")
movie_df["release_month"] = movie_df["release_date"].dt.strftime("%b")
movie_df["last_modified_est"] = datetime.now()
movie_df["last_modified_est"] = movie_df["last_modified_est"].dt.tz_localize("America/New_York")
movie_df["last_modified_ist"] = movie_df["last_modified_est"].dt.tz_convert("Asia/Kolkata")

### Back to cleaning the data
movie_df["box_office"] = movie_df["box_office"].str.replace(",", "").astype(float)
mask = movie_df["phase"].isna()
movie_df.loc[mask, "phase"] = np.where(
    movie_df.loc[mask, "release_date"].dt.year < 2020, 3,4
)
movie_df["running_time"] = movie_df["running_time"].fillna(movie_df["running_time"].median()).round(2)
movie_df["budget"] = movie_df["budget"].fillna(movie_df["budget"].mean())
movie_df["box_office"] = movie_df["box_office"].fillna(2.5 * movie_df["budget"] + movie_df["rt_critic_score"] * 0.33 + movie_df["rt_audience_score"] * 0.67).round(2)
movie_df["wikipedia_link"] = movie_df["wikipedia_link"].fillna("https://en.wikipedia.org/wiki/" + movie_df["movie"]).str.replace(" ", "_")
movie_df["rt_average_score"] = (movie_df["rt_critic_score"] + movie_df["rt_audience_score"]) / 2



# Step 3: Counting number of movies per phase types with Counter
counts = Counter(movie_df["phase"]); print(counts)



# Step 4: Filtering and determining top 5 movies based on average audience/critic score
movie_df = movie_df[["movie", "release_date", "release_month", "release_order", "chronological_order", "phase", "running_time", "budget", "box_office", "rt_critic_score", "rt_audience_score", \
                     "rt_average_score", "wikipedia_link", "last_modified_est", "last_modified_ist"]]
top_5_movies = movie_df.sort_values("rt_average_score", ascending = False).head(5)



# Step 5: Writing a human-readable file with the results I want to show
top_5_movies.to_csv("/Users/willhager/Documents/Python Practice/top_5_movies.csv", index = False)
with open("/Users/willhager/Documents/Python Practice/MarvelMovieStats.txt", "w") as f:
    f.write("Marvel Movie Stats (My first handmade txt file!)\n")
    f.write("========================================\n")
    f.write(f"Total movies: {len(movie_df)}\n\n")
    f.write(f"Number of phases tracked: {dict(counts)}\n\n")
    f.write(f"Top 5 movies:\n\n")
    for index, row in enumerate(top_5_movies.itertuples(index = False), start = 1):
        f.write(f"{index}. {row.movie}\n")
        f.write(f"It has an average rotten tomatoes score of {row.rt_average_score}.\n\n")

# Printing the movie dataframe and the top 5 movies so that I can see the results in the terminal when I run the code
print(movie_df)
print(top_5_movies)


# Resetting column width
pd.reset_option("display.max_columns")
pd.reset_option('display.width')

