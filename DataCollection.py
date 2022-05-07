import twint
import nest_asyncio
import time
import schedule
import atexit
import os

nest_asyncio.apply()

emojis = ["😠", "😡", "😤", "😒", "👎", "👀", "💭", "💰", "😬", "✊", "😖", "😣", "😫", "💩", "😷", "😨", "😱", "😰", "😟", "👻",
          "☺", "😆", "😂", "😹", "😊", "😢", "😭", "💔", "😞", "😥", "🙈", "🎉", "😍", "😳", "🙊", "😙", "💕", "🌹", "💋", "😚"
          ]

keywords = ["koronavirus", "koronaviru", "koronavirem", "korona", "korony", "koroně", "koronou"]
keywords2 = ["covid", "covidu", "covidem", "covid 19", "pandemie", "pandemii"]

txt_name = "my_search_id_.txt"
txt_name2 = "my_search_id_2.txt"

tweets_as_objects = []
temporary_count = 0


def createString(array):
    final_string = ""
    for item in array:
        final_string += item + " OR "
    final_string = final_string[:-4]
    return final_string


def getTweets(keywords_array, txt_resume_name):
    global tweets_as_objects
    print("Fetching Tweets")

    config = twint.Config()
    config.Search = "(" + createString(keywords_array) + ") (" + createString(emojis) + ") lang:cs"
    config.Since = "2020-03-01"
    config.Until = "2020-04-30"
    config.Count = 1
    config.Resume = txt_resume_name
    config.Store_object = True
    config.Store_csv = True
    config.Output = "data/brezen_duben.csv"

    twint.run.Search(config)
    tweets_as_objects = twint.run.output.tweets_list


def exitCheck():
    global tweets_as_objects
    global temporary_count
    if temporary_count != len(tweets_as_objects):
        print("****** Count checked. Temporary count: " + str(temporary_count) + " ****** Object count: " + str(
            len(tweets_as_objects)))
        temporary_count = len(tweets_as_objects)
    else:
        print("***** Fetching tweets done! *****")
        raise SystemExit(0)


def exitExecute():
    os.remove(txt_name)
    os.remove(txt_name2)


schedule.every(5).seconds.do(getTweets, keywords, txt_name)
schedule.every(5).seconds.do(getTweets, keywords2, txt_name2)
schedule.every(30).seconds.do(exitCheck)

atexit.register(exitExecute)


while True:
    schedule.run_pending()
    time.sleep(1)





