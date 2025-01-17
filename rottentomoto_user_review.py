from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


action_movie = ['hacksaw_ridge', 'blood_father', 'deepwater_horizon',
                'in_a_valley_of_violence', 'the_magnificent_seven_2016', 'dont_mess_with_texas_2014',
                'last_airbender', 'gigli', 'babylon_ad']


romance_movie = ['perfect_man', 'everything_everything_2017']

mystery_movie = ['paranoia_2013', 'mobsters', 'the_book_of_henry']

comedy_movie = ['baywatch_2017', 'the_house_2017', 'snatched_2017']

horror_movie = ['the_dark_tower_2017', 'the_mummy_2017', 'wish_upon']

movie_book = [action_movie, romance_movie,
              mystery_movie, comedy_movie, horror_movie]

# The target movie reviews from the user
# url = 'https://www.rottentomatoes.com/m/iron_man/reviews/'

# Build pd dataframe
recorder = pd.DataFrame()

for movies in movie_book:
    for movie in movies:

        url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews/'

        

        # Set max length of the review
        MAX_LENGTH = 300

        # Choose the range of the pages
        for i in range(1, 50):

            page_number = str(i)

            print("Start at page: ", page_number)

            # Adjust the url for every loop
            url_link = url + "/?page=" + page_number + "&type=user" + "&sort="
            print('The url address is: ', url_link)

            # Open and get the html content
            try:
                html = urlopen(url_link)
            except Exception as e:
                print("Reach the end, break.")
                break
            # html = urlopen(url_link)
            url_content = BeautifulSoup(html, 'html.parser')

            # Get the framework for every user's review
            for review_box in url_content.find_all('div', class_='col-xs-16'):

                # The content of the review
                review = review_box.find(
                    'div', class_='user_review').get_text().lstrip()
                review_length = len(review)

                # Count the length of stars (0-5)
                star_counter = len(review_box.find_all(
                    'span', class_='glyphicon glyphicon-star'))

                # Take 5-star-review as a positive review
                if(star_counter == 5 and review_length <= MAX_LENGTH):
                    print("Positive review!")

                    # Add the positive entry to df
                    recorder = recorder.append(
                        {'review': review, 'label': 1}, ignore_index=True)

                # Count the 1/2 rating benchmark (0/1)
                half_rate_counter = len(review_box.find_all(text="½"))
                if(half_rate_counter == 0):
                    half_rate_counter = len(review_box.find_all(text=" ½"))

                print(star_counter, half_rate_counter)

                # Take 1/2 or 1 star as a negative review
                if((star_counter == 0 and half_rate_counter == 1 or
                        (star_counter == 1 and half_rate_counter == 0)) and
                   review_length <= MAX_LENGTH):
                    print("Negative review!")

                    # Add the negative entry to df
                    recorder = recorder.append(
                        {'review': review, 'label': 0}, ignore_index=True)

                    # print(review)

                # print("________________THIS REVIEW FINISHED__________________")
        print(recorder.head(5))

        # recorder.to_csv(movie + ".csv", index=False)

recorder.to_csv("Movie_reviews.csv",index=False)
