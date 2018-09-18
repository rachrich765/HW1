## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
# https://www.reddit.com/r/flask/comments/4krfu0/afconvert_immutablemultidict_to_properly/
# https://www.tutorialspoint.com/python/dictionary_get.htm
# https://www.w3schools.com/tags/att_input_type.asp
# http://www.seanbehan.com/how-to-get-a-dict-from-flask-request-form/
# https://stackoverflow.com/questions/23375606/converting-list-items-from-string-to-intpython/23375633
# I worked alone

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import requests
import json
import sys
from collections import Counter
import string

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def welcome_to_364():
    return "Welcome to SI 364!"

@app.route('/movie/<anytitlesearch>')
def get_itunes_data(anytitlesearch):
    base_url = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction["term"] = anytitlesearch
    params_diction["media"] = "movie"
    resp = requests.get(base_url,params=params_diction)
    text = resp.text
    python_obj = json.loads(text)
    return str(python_obj)

@app.route('/question')
def question():
    return """ <form action="http://localhost:5000/result" method='POST'>
     Enter your favorite number:  <input type="number" name="number_to_be_doubled" value="number">
    <input type="submit" value="Submit">
    </form>"""

@app.route('/result',methods=["POST"])
def result_form1():
    if request.method == "POST":
        results = request.form.to_dict(request.args)
        num_double_1 = results.get('number_to_be_doubled')
        for i in range(len(num_double_1)):
            num_double_1[i] = int(num_double_1[i])
        number_to_be_doubled = (num_double_1[0])*2
        return "Double your favorite number is " + str(number_to_be_doubled)


@app.route('/problem4form',methods=["GET"])
def prob4_form():
    formstring = """<br><br>
    <form action="" method='GET'>
    Enter a tv show: <input type="text" name="tv_name">  <br>
    Select <b> one </b> of the options below: <br>
    <input type="checkbox" name="rating" value="TV-Y"> I think this TV Show should be rated TV-Y <br>
    <input type="checkbox" name="rating" value="TV-Y7"> I think this TV Show should be rated TV-Y7 <br>
    <input type="checkbox" name="rating" value="TV-G"> I think this TV Show should be rated TV-G <br>
    <input type="checkbox" name="rating" value="TV-PG"> I think this TV Show should be rated TV-PG <br>
    <input type="checkbox" name="rating" value="TV-14"> I think this TV Show should be rated TV-14 <br>
    <input type="checkbox" name="rating" value="TV-MA"> I think this TV Show should be rated TV-MA <br>
    <input type="submit" value="Submit">
    </form>"""
    if request.method == "GET":
        tv_name = request.args.get('tv_name', "")
        base_url = "https://itunes.apple.com/search"
        params_diction = {}
        params_diction["term"] = tv_name
        params_diction["media"] = "tvShow"
        ratings = []
        resp = requests.get(base_url,params=params_diction)
        text = resp.text
        python_obj = json.loads(text)
        for item in python_obj["results"]:
            ratings.append(item['contentAdvisoryRating'])
        ratings_counted = Counter(ratings)
        most_common_rating = []
        for rating, count in ratings_counted.most_common(1):
            most_common_rating.append(rating)
        user_rating = str(request.args.get('rating', ''))
        most_common_rating = str(most_common_rating).replace('[','').replace(']','').strip("''")
        if most_common_rating != user_rating:
            return formstring  + "Your rating, " +  str(user_rating) +  "," + " for the TV show, " + "'" + string.capwords(str(tv_name))  + "'"+ ", is <b> different </b> from the most common rating, which is " + str(most_common_rating) + "."
        else:
            return formstring  + "Your rating, " + str(user_rating) +  "," + " for the TV show, " + "'" + string.capwords(str(tv_name))  + "'" + ", is the <b> same </b> as the most common rating, which is " + str(most_common_rating) + "."
    return formstring

if __name__ == '__main__':
    app.run()


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
