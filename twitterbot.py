
# coding: utf-8

# # Bot Skeleton

# The next cell will authenticate your bot based on your keys and tokens. See the [Tweepy tutorial](https://github.com/comp-journalism/UMD-J479V-J779V-Spring2016/blob/master/Weekly/Week_5/Tweepy-skeleton.ipynb) for more details. 

# In[8]:

import tweepy

#Setup and authenticate Tweepy
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


for status in api.user_timeline('Humans_of_Syria'):
    api.retweet(status.id)

    


#api.update_status(status = "Tweet Test")


# The next cell has a number of essential functions that allow your bot to listen to the twitter stream and then respond. The assignment involves fleshing out the editorial logic of the bot and writing code in the sections marked "TODO".

# In[9]:

import random
import json
import time
import pprint


# If debug_mode is True then the bot won't actually tweet. Set debug_mode = False for it to tweet. 
debug_mode = False


# Functions that allow the bot to tweet or reply to tweets
def tweet(status):
    print ("JUST TWEETED: "), status
    # Only *actually* send the tweet on twitter if we're not in debug mode
    if debug_mode == False:
        api.update_status(status)
        
def tweet_with_probability(status, probability):
    # Change the probability of tweeting variable to affect how often the bot tweets
    rand = random.random()
    if rand <= probability:
        print ("JUST TWEETED: "), status
        # Only *actually* send the tweet on twitter if we're not in debug mode
        if debug_mode == False:
            api.update_status(status)
            
#Tweet when keyword is picked up
        
def tweet_reply(status, tweet_to_reply_to):
    screen_name = tweet_to_reply_to["user"]["screen_name"]
    at = "HT @"+screen_name 
    reply_to_id = tweet_to_reply_to["id"]
    foo = ['http://www.humansofnewyork.com/post/125869847371/i-admired-her-from-afar-for-a-while-and', 'http://www.humansofnewyork.com/post/38640617321/the-ghost-tehran-iran', 'http://www.humansofnewyork.com/post/94159334781/there-were-dozens-of-them-and-only-four-of-us', 'http://www.humansofnewyork.com/post/94167715831/i-would-give-my-soul-if-i-could-fix-her-brain', 'http://www.humansofnewyork.com/post/94211267196/i-worry-about-the-day-they-start-to-want-things']
    status = at + " " + status + (random.choice(foo))
    
    print(random.choice(foo))
    
    #status = at + " " + status + 'http://www.humansofnewyork.com/post/38633154424/seen-in-tehran-iran'
    print ("JUST TWEETED: Hello World"), status
    # To actually have the bot tweet a status message uncomment the next line, it will send the tweet in response to the appropriate tweet. 
    # Only *actually* send the tweet on twitter if we're not in debug mode
    if debug_mode == False:
        api.update_status(status=status, in_reply_to_status_id=reply_to_id)
        
    
    foo = ['http://www.humansofnewyork.com/post/125869847371/i-admired-her-from-afar-for-a-while-and', 'http://www.humansofnewyork.com/post/38640617321/the-ghost-tehran-iran', 'http://www.humansofnewyork.com/post/94159334781/there-were-dozens-of-them-and-only-four-of-us', 'http://www.humansofnewyork.com/post/94167715831/i-would-give-my-soul-if-i-could-fix-her-brain', 'http://www.humansofnewyork.com/post/94211267196/i-worry-about-the-day-they-start-to-want-things']
    print(random.choice(foo))
    
# We derive a class that is used to listen to the twitter stream
class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        super(TwitterStreamListener, self).__init__()
        self.num_tweets = 0 
        self.api_count = 0
        self.old_time = time.time()
    
    # Everytime the listener encounters a tweet that matches its filters it will trigger the on_data function
    def on_data(self, data):
        try:
            print ("a tweet found")
            # Increment out counter of tweets
            self.num_tweets = self.num_tweets + 1
               
            
            # The data variable represents the tweet that was detected by the stream listener
            # Here we just parse it as JSON and put it in another variable. 
            tweet_data = json.loads(data)
            
            print(tweet_data)
            # Make sure the bot never interacts with itself
            user = tweet_data["user"]["screen_name"]
            
            user_mentions = tweet_data['entities']['user_mentions']
            print("got here")
            user_mentions_list = []
            for u in user_mentions:
                print("iterating user mentions")
                print(u)
                user_mentions_list.append(u["screen_name"])
            print("got past loop")
            if user == "taytestbot" or "taytestbot" in user_mentions_list:
                print ("dont talk to me")
                # return without doing anything
                return
      
    

            
            # TODO: Add your editorial logic here, some example filters are below
            
            # Possible filters
            # Maybe you don't want to respond to someone's RT
            #if tweet_data["retweeted"] == True
            #    return
            
            # Maybe you don't want to respond to a tweet without a URL
            #if len(tweet_data["entities"]["urls"]) == 0:
            #    return
            
            # Maybe you only want to do something with every Nth tweet since otherwise the bot is tweeting too frequently
            # e.g. Don't do anything unless this is the 5th tweet you've encountered
            if self.num_tweets == 5:
                print ("5")
                self.bot_action(tweet_data)
            
        except Exception as e:
           
            print ("test exception: ") + e
            
            pass
        
        return True
    
    def api_limit_checker(self):
        # API limits are reset every 15 minutes (900 seconds). This checks if we are outside a 15 min window 
        if time.time() - self.old_time > 900: 
            # Reset the timer of window since new window started & Twitter limits refreshed
            self.old_time = time.time()
            #Reset the api counter to 0 since new window started & Twitter limits refreshed
            self.api_count = 0
        else:
            # The bot cannot tweet more than 140 times every 15 minutes (and you should REALLY consider not ever getting close to that as you may trigger Twitters spam detectors)
            # The threshold below is set much more conservatively. It will only let you tweet 5 times in a 15 minute window
            if self.api_count > 5:
                print ("Taking a break")
                # We put the code to sleep for 15-x minutes where x is the current time - old time (when the window started)... So if within 6 minutes we tweet more than 140 times, then the script will halt for the next 15-6=9 minutes until a new window starts
                time.sleep(900 - (time.time() - self.old_time))
                # Since we have slept through the remainder, a new window has started and we reset the API Count as well
                self.api_count = 0
                #Similarly as above, we reset the timer as well since new window has started 
                self.old_time = time.time()
                
    def bot_action(self, tweet_to_reply_to):
        print ("bot action")
        # NOTE: if you'd like your bot to reply, user the tweet_data variable above as the tweet_to_reply_to parameter for this function
        # invoke the API limit checker code, whcih will put bot to sleep if it's too active
        self.api_limit_checker()
        
        # reset the num_tweets counter
        self.num_tweets = 20
        
        print("got to here in bot action")
        # Actually tweet something, just a dummy output right now
        # TODO: Write code that constructs a text to tweet
        try:
            print(tweet_to_reply_to)
            #api.update_status('Hello World',tweet_to_reply_to["id"]) 
            tweet_reply("",tweet_to_reply_to)
        except Exception as e:
            print("Exception in bot action")
            print(e)
       
        print("we think we did something")
        tweet("Hello world")
        
        # Increment API count
        self.api_count = self.api_count + 1
        
        return 
    
    def on_error(self, status):
        print (status)


def listen():
    print ("listening")
    listener = TwitterStreamListener()
    stream = tweepy.Stream(auth, listener)
    # track_object filters the twitter stream to capture data, can provide a hashtag, word, or screenname amongths other things. See documentation at: https://dev.twitter.com/streaming/overview/request-parameters
    track_object = ["#Syria"]
    
    try:
        # Start filtering the twitter stream
        stream.filter(track=track_object)
        print ("tried")
    except:
        # do nothing in the event of an error
        pass
    return


# The next cell will actually run the bot and set it to listen to Twitter.

# In[10]:

listen()


# In[ ]:




# In[ ]:



