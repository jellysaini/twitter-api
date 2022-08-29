
from django.urls import path
from .views import (Home,RetweetedTweetListView,RetweetedTweetUserListView, 
ListRetweetedUser, ViewSearchTweeterUser, ViewSearchTweet )

urlpatterns = [

    path('',
         Home.as_view(),
         name='home'),
    path('retweets_of_me/',
         RetweetedTweetListView.as_view(),
         name='retweets_of_me'),

    path('retweet_user_list/<int:tweet_id>/',
         RetweetedTweetUserListView.as_view(),
         name='retweet_user_list'),


     path('retweeted_user/',
      ListRetweetedUser.as_view(), 
      name='retweeted_user'),

     path('search_user/',
      ViewSearchTweeterUser.as_view(), 
      name='search_user'),
      
     path('search_tweet/',
      ViewSearchTweet.as_view(), 
      name='search_tweet'),

]