import csv_to_json
import argparse
import os
import json

def list_directory(data):
    '''
    Estrae lista di directories nelle quali ho i files json
    @params:
        data:   - Required   : cartella di sottocartelle di file json
    '''
    l = []
    print(data)
    for x in os.listdir(data + "\\"):
        l.append(x)
        
    return l


if __name__ == '__main__':
    '''
    Conversione dei file csv in input in file json immagazzinati nella cartella 
    "json" (la crea se non presente)
    @params:
        -d: directory di directories dei files csv
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, required=False, help="Inserire la directory da cui prendere i dati", default="data")
    
    args = parser.parse_args()
    
    try:
        l_dir = list_directory(args.data) #lista di directories da inserire
        print(l_dir)
    except:
        print("error import csv" + str(args.data))
        exit()

    # per ogni directory 
    for i in l_dir:
        print(i)
        # concatena i vari csv pulendoli
        df = csv_to_json.conc_dataframe(args.data + '\\' + i)
        print("dataframe cleaned and merged")
        # nel caso in cui non venga generato alcun dataframe
        if df is None:
            print("df none")
            continue
        # trasforma il dataframe in lista di dizionari
        l_dict = csv_to_json.df_to_listdict(df) 
        # salvataggio dei dizionari in un file json nella cartella json
        n_json = i + '.json'
        # se la cartella json non esiste la crea
        if not os.path.exists("json"):
            os.makedirs("json")
        with open('json\\' + n_json, "w") as file_json:
            json.dump(l_dict, file_json, skipkeys = True)

        print("dataframe correctly converted to json")
        