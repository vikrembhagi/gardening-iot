import tweepy

def get_api(cfg):
  auth = tweepy.OAuthHandler('Bj8azJ7e93Dz5nmEeNj39LCl6', 'qzcD0dSm44dWStn5DeGonMe5ZdDP74uzpeUi7iaRXD26U2KcFy') # Add your secret Keys here 
  auth.set_access_token('892192619811528704-Jofde1j4UegmvCOWtJg8t2ZtXaMe7pg', 'E2DZmoWqPyqoUT5cHpILYsXNWn2VRf2f5Ty7anSr7v7UA') # Add your Authorization token information here
  return tweepy.API(auth)

def main():
  # Fill in the values noted in previous step here
  cfg = { 
    "consumer_key"        : "VALUE",
    "consumer_secret"     : "VALUE",
    "access_token"        : "VALUE",
    "access_token_secret" : "VALUE" 
    }

  api = get_api(cfg)
  tweet = "@restlessvik Hello master !" # Send Tweet Message
  status = api.update_status(status=tweet) 
  # Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
  main()