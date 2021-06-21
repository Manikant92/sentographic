# sentographic

A running version of this app can be found in https://sentographic.herokuapp.com


# Inspiration
It is important for companies/brands to know the voice of their customers/users on how they are feeling about their products/services. Hence, we built an one-stop application, where companies/brands can come here and get to know about the EMOTIONS/SENTIMENTS/VOICE of their users/customers.

#  What it does
As we all know, Social and News Media are the platforms where users voice can be heard aloud today. So, we are fetching the twitter tweets data using tweepy and news articles data using newsapi. We then calculate the sentiment analysis of the data using Expert.ai Sentiment Analysis and leverage few of the Expert.ai services like Main Lemmas and Entities.

# How we built it
Django is the backend server. Using Newsapi and Tweepy, fetching data from news and social media platforms. At frontend, we used JS, Bootstrap and CSS and HTML to represent a beautiful UI with graphs.

# Challenges we ran into
Limitation of Newsapi requests to limit only 1000 requests for one hour per account. Hence, we are limited to display only top 150 when it comes to News Articles data. Having no experience in Django, learnt it and developed and enhanced the application to much better.

# Accomplishments that we're proud of
Connecting all API services of twitter, news, expert.ai and maps to represent the data for brands in a beautiful UI.

# What we learned
Learning Django and connecting to twitter and then newsapi. Learning about various services offered by expert.ai

# What's next for sentographic
Connecting with facebook, instagram API services for getting Social media data.

Further details can be found here: https://devpost.com/software/sentographic
