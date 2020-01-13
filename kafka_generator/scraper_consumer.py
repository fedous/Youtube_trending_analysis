from kafka import KafkaConsumer
from datetime import datetime
from mongoFunctions import insert_video_mongo
import requests, sys, time, os, argparse
import sched
import json

# Set time scheduler
scheduler = sched.scheduler(time.time, time.sleep)
#set global variables
output_dir = "output/"
api_key = ""
country_codes = ""
format_date = "%d-%m-%Y %H:%M"
dt = datetime.now()

snippet_features = ["title",
                   "publishedAt",
                   "channelId",
                   "channelTitle",
                   "categoryId"]

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

######################
# Definisco il consumer
consumer = KafkaConsumer(
  bootstrap_servers=["kafka:9092"],
  auto_offset_reset="latest",
  value_deserializer=lambda v: json.loads(v.decode("utf-8")))
# sottoscrive un determinato topic
consumer.subscribe(["youtube_video"])

def setup(code_path):
    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return country_codes

def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'

#def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
 #   return prepare_feature("|".join(tags_list))

def get_videos(videos):
    lines = []
    items = videos.value['items']
    service = videos.value['service']
    country = service['country']
    timestamp = service['timestamp']
    
    for video in items:
        comments_disabled = False
        ratings_disabled = False

        # We can assume something is wrong with the video if it has no statistics, often this means it has been deleted
        # so we can just skip it
        if "statistics" not in video:
            continue
            
        video_id = video['id']
        snippet = video['snippet']
        statistics = video['statistics']
        features = [snippet.get(feature, "") for feature in snippet_features]

        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        tags = snippet.get("tags", [])

        # Compiles all of the various bits of info into one consistently formatted line
        line = {}
        line['video_id'] = video_id 
        line['timestamp'] = timestamp
        line['country_code'] = country
        line['title'] = features[0]
        line['publishedAt'] = features[1]
        line['channelId'] = features[2]
        line['channelTitle'] = features[3]
        line['categoryId'] = features[4]
        line['trending_date'] = trending_date
        line['tags'] = tags 
        line['statistics'] = statistics
        line['thumbnail_link'] = thumbnail_link
        line['description'] = description
        
        # inserisco il dizionario appena trovato nella lista di output
        lines.append(line)
        
    return lines

def get_data():
    #video è un json fatto con i suoi campi
    for video in consumer:
        #qua va fatto il parser del consumer
        l_video = get_videos(video)
        #inserisco i documenti in mongo
        insert_video_mongo(l_video)
        #stampo i json nella cartella output_consumed
        #write_to_file(l_video, i)

def consume():
    global output_dir
    global country_codes
    global dt
    
    country_code_path = "country_codes.txt"

    country_codes = setup(country_code_path)
   
    get_data()

#fa partire il consume
consume()