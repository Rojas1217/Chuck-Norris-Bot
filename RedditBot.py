import praw
import config #Should include a separate python file (config.py) where login info for the bot (username, password, etc.) are defined
import time
import os
import requests

#settting up all the login and developer details for the bot being retrieved from the file named config.py
def bot_login():  
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "AwkwardWalrus' first reddit bot")
    print "Login successful"
    return r

#Checks comment IDs from a text file that keeps IDs of comments that have already been replied to so you don't keep responding to the same comments
def check_saved_comments(): 
    if not os.path.isfile("comments_replied.txt"):
        comments_replied = [] 
    else:
        with open("comments_replied.txt", "r") as f:   #open file to read stored comment IDs 
            comments_replied = f.read()
            comments_replied = comments_replied.split("\n")
            comments_replied = filter(None, comments_replied)

    return comments_replied

#main function that will be running on a continuous loop and checks every 10 seconds
def run_bot(r, comments_replied): 
    print "taking in details from 100 comments..."
    for comment in r.subreddit("test").comments(limit = 100):  #collecting comments from the r/test subreddit
        if "!joke" in comment.body and comment.id not in comments_replied and comment.author != r.user.me():  
            #looking for !joke and that the commentor wasn't already replied to and that the user is not me

            print "String with \"!joke\" found in comment"

            comment_reply = "You requested a Chuck Norris Joke! Here it is:\n\n"  #preparing the text and get request for the reply

            joke = requests.get('http://api.icndb.com/jokes/random').json()['value']['joke'] 

            comment_reply += ">" + joke

            comment.reply(comment_reply) #PRAW reply

            comments_replied.append(comment.id)

            with open ('comments_replied.txt',"a") as f:  #opens txt file to store ID of the comment that was just replied to
                f.write(comment.id + "\n")

    time.sleep(10) #sleep for 10 seconds

r = bot_login() #initializing the bot
comments_replied = check_saved_comments()

while True:
    run_bot(r, comments_replied)  #looping the important bit to continue checking for comments constantly

#code runs indefinitely