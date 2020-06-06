'''
asdf
'''

from kafka import KafkaConsumer
from datetime import datetime, timedelta
from pymongo import MongoClient
import requests, sys, time, os, argparse
import sched
import json

#preparo il code path e il client mongo
def setup(code_path, host, port, user, passw): 
    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]
    
    #definisco il client mongo
    client = MongoClient(host, port, username = user, password = passw)
    
    return country_codes, client

# funzione che sistema il timestamp
def fix_timestamp(timestamp, country_code, c_gmt):
    fuso = c_gmt[str(country_code)]['GMT']
    dt = datetime.strptime(str(timestamp), "%d-%m-%Y %H:%M")
    dt_new = dt + timedelta(hours=fuso)
    return dt_new.strftime("%m-%d-%Y %H:%M")

#restituisce il nome esteso del paese
def find_country_name(country_code, c_gmt):
    return c_gmt[str(country_code)]['name']

# restituisce il nome della categoria per esteso
def find_category_name(category_id, categorys):
    for category in categorys:
        if category['id'] == str(category_id):
            return category['snippet']['title']
    
#rimuovi i caratteri non sicuri
def prepare_feature(feature):
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'

#sistama i tag da inserire in una lista
def get_tags(tags_list):
    return prepare_feature("|".join(tags_list))

#si occupa dell'estrazione dei video in una pagina e li restituisce
def get_videos(items, service):
    lines = []
    
    # carico il file con i dati relativi ai paesi
    with open('country_names.json') as c_names:
        c_gmt = json.load(c_names)
    # carico il file con i dati relativi alle categorie
    with open('category_id.json') as c_names:
        categorys = json.load(c_names)['items']
        
    country_code = service['country']
    country_name = find_country_name(country_code, c_gmt)
    timestamp = fix_timestamp(service['timestamp'], country_code, c_gmt)
    for video in items:

        # se non sono presenti le statistiche saltiamo il video
        if "statistics" not in video:
            continue

        video_id = video['id']
        # Snippet e statistics contengono informazioni interne
        snippet = video['snippet']
        statistics = video['statistics']
        #print(statistics)
        # estraggo da snippet le info che mi servono
        features = [snippet.get(feature, "") for feature in snippet_features]
        # pulisco la description
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        tags = snippet.get("tags", [])
        view_count = statistics.get("viewCount", 0)
        likes = statistics.get("likeCount", 0)
        dislikes = statistics.get("dislikeCount", 0)
        comment_count = statistics.get("commentCount", 0)
        statistics = {
            "view_count" : view_count,
            "likes" : likes,
            "dislikes" : dislikes,
            "comment_count" : comment_count
        }
        # Compiles all of the various bits of info into one consistently formatted line
        line = {}
        line['video_id'] = video_id 
        line['timestamp'] = timestamp
        line['country_code'] = country_code
        line['country_name'] = country_name
        line['title'] = features[0]
        line['publishedAt'] = features[1]
        line['channelId'] = features[2]
        line['channelTitle'] = features[3]
        line['categoryId'] = features[4]
        line['category_name'] = find_category_name(features[4], categorys)
        line['trending_date'] = trending_date
        line['tags'] = tags 
        line['statistics'] = statistics
        line['thumbnail_link'] = thumbnail_link
        line['description'] = description
        
        lines.append(line)
        
    return lines

#si occupa della scrittura su file json
def write_to_file(output_data, pos):
    print(f"Writing data to file...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    subdir = f"{time.strftime('%Y.%m.%d')}_pages"
    if not os.path.exists(f"{output_dir}/{subdir}"):
        os.makedirs(f"{output_dir}/{subdir}")
    with open(f"{output_dir}/{subdir}/{time.strftime('%Y.%m.%d')}_%04i_videos.json" %(pos), "w+", encoding='utf-8') as file:
        json.dump(output_data, file, indent=3)
        
# raccoglie i dati, li scrive su file e su mongoDB
def get_data(clientMongo, database = "yt_data", collection = "videos"):
    global i
    #video è un json fatto con i suoi campi
    for video in consumer:
        #nel caso per qualche errore di rete non arrivassero items
        if "items" not in video.value:
            print("!! ERROR: no items field - " + datetime.today().strftime("%d-%m-%Y %H:%M"))
            continue

        l_video = get_videos(video.value['items'], video.value['service'])
        #salvo i video su file
        write_to_file(l_video, i)
        #inserisco i video in mongoDB
        #db = clientMongo[database]
        #col = db[collection]
        #col.insert_many(l_video)
        #print("inserted in mongo")
        i += 1
        if i > 9999:
            i = 0

def consume(db, col):
    '''
    Esegue tutti i passaggi per leggere da Kafka i dati, salvarli su MongoDB e in json
    '''
    global output_dir
    global country_codes
    global unsafe_characters, i
   
    get_data(clientMongo, db, col)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, required=False, help="Inserire la directory di output", default="output_consumed/")
    parser.add_argument('-co', '--country_path', type=str, required=False, help="Inserire il path del file dove ci sono i country code", default="country_codes.txt")
    parser.add_argument('-ch', '--channel_kafka', type=str, required=False, help="Inserire il nome del canale kafka da consumare", default="yt_video")
    parser.add_argument('-ho', '--host', type=str, required=False, help="Inserire il nome dell'host del server mongoDB", default="localhost")
    parser.add_argument('-p', '--port', type=int, required=False, help="Inserire il numero della porta in cui comunica il server mongoDB", default=27017)
    parser.add_argument('-u', '--user', type=str, required=False, help="Inserire il nome utente del server mongoDB", default="admin")
    parser.add_argument('-pass', '--password', type=str, required=False, help="Inserire la password del server mongoDB", default="DataMan2019!")
    parser.add_argument('-db', '--database', type=str, required=False, help="Inserire il nome del database mongoDB in cui salvare i dati", default="yt_data")
    parser.add_argument('-col', '--collection', type=str, required=False, help="Inserire il nome della collezione mongoDB nella quale inserire i dati", default="videos")
    
    args = parser.parse_args()
    
    # Setting variabili globali
    # scheduler inizializzazione
    scheduler = sched.scheduler(time.time, time.sleep)
    output_dir = args.output
    country_code_path = args.country_path
    channel_kafka = args.channel_kafka
    host = args.host
    port = args.port
    user = args.user
    passw = args.password
    db = args.database
    col = args.collection
    i = 0 #indice per la stampa su file
    country_codes = ""
    # List of simple to collect features
    snippet_features = ["title", "publishedAt", "channelId",
                        "channelTitle", "categoryId"]
    # Elenco ci caratteri problematici
    unsafe_characters = ['\n', '"']

    #Definisco il consumer
    consumer = KafkaConsumer(
    bootstrap_servers=["kafka:9092"],
    auto_offset_reset="latest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")))
    consumer.subscribe([channel_kafka])
    
    # eseguo il setup iniziale
    country_codes, clientMongo = setup(country_code_path, host, port, user, passw)
    
    consume(db, col)