import logging

import tweepy
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import FormSearchTweeterUser, FormSearchTweet

logger = logging.getLogger(__name__)

# disable the tweepy, requests_oauthlib and oauthlib.oauth1 lib logs
logging.getLogger('tweepy').setLevel(logging.WARNING)
logging.getLogger('requests_oauthlib').setLevel(logging.WARNING)
logging.getLogger('oauthlib.oauth1').setLevel(logging.WARNING)


TWEET_AUTH = tweepy.OAuth1UserHandler(settings.API_KEY,
                                      settings.API_SECRET_KEY,
                                      settings.ACCESS_TOKEN,
                                      settings.ACCESS_TOKEN_SECRET,
                                      )

TWEET_API = tweepy.API(TWEET_AUTH)



class Home(TemplateView):
    template_name = 'home.html'


class RetweetedTweetListView(TemplateView):
    template_name = 'retweeted_tweet_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['get_retweets_of_me'] = TWEET_API.get_retweets_of_me()
        return context


class RetweetedTweetUserListView(TemplateView):
    template_name = 'retweeted_tweet_user_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        tweet_id = self.kwargs.get('tweet_id')
        # print(tweet_id)
        retweets = TWEET_API.get_retweets(tweet_id)
        context['get_retweets'] = retweets
        return context


class ViewSearchTweeterUser(FormView):
    form_class = FormSearchTweeterUser
    template_name = 'form_search_user.html'
    success_url = reverse_lazy('tweetapp:search_user')

    def form_valid(self,form, *args, **kwargs):
        query = form.cleaned_data['query']
        search_users = TWEET_API.search_users(query)
        context = TemplateView.get_context_data(self, **kwargs)
        context['search_users'] = search_users

        if 'form' not in context:
            context['form'] = self.get_form()


        # return FormView.form_valid(self, form, **kwargs)
        return self.render_to_response(context=context)


class ViewSearchTweet(FormView):
    form_class = FormSearchTweet
    template_name = 'form_search_tweet.html'
    success_url = reverse_lazy('tweetapp:search_tweet')

    def form_valid(self,form, *args, **kwargs):
        query = form.cleaned_data['query']
        search_tweets = TWEET_API.search_tweets(query)
        context = TemplateView.get_context_data(self, **kwargs)
        context['search_tweets'] = search_tweets

        if 'form' not in context:
            context['form'] = self.get_form()

        # return FormView.form_valid(self, form, **kwargs)
        return self.render_to_response(context=context)



class ListRetweetedUser(TemplateView):
    template_name = 'retweeted_user.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)

        retweet_user_list = []
        # get my retweeted tweets
        # Returns the 20 most recent Tweets of the authenticated user that have been retweeted by others.
        my_retweets = TWEET_API.get_retweets_of_me()
        # for every retweeted tweets get the retweetd users of my retweeted tweet
        for mt in my_retweets:
            # Returns up to 100 of the first Retweets of the given Tweet.
            retweets = TWEET_API.get_retweets(mt.id)
            retweets_user = [rt.user for rt in retweets]
            retweet_user_list.append(retweets_user)
        # convert list from nested list to one dimensional list
        unique_user_list = [u for u_l in retweet_user_list for u in u_l]

        # make unique user list
        unique_user_list = list(dict.fromkeys(unique_user_list))

        retweeted_user = []
        for current_user in unique_user_list:
            for _user_list in retweet_user_list:
                # if there is break means user is not in every list
                if current_user not in _user_list:
                    break
            else:
                # if no break then user is in every list i.e eligible user
                retweeted_user.append(current_user)
        context['retweeted_user'] = retweeted_user
        return context
