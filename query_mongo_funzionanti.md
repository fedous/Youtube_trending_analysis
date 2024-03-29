# Query mongo per estrarre informazioni interessanti

### Contare quanti video hanno tag coronavirus per paese:

db.videos_march.aggregate(
    [{$match : {
                tags : {$all : ["coronavirus"]}}},
     {$group : {
                _id : "$country_name", 
                count : {$sum : 1}}
     }
    ]
)

### Regular expression Covid (javascript) - 1
/(corona|covid|virus|pandemi[aec]|epidemi[aec]|tampon[ei]|sierologico|mascherin[ae]|코로나 바이러스|fase\s*(2|due)|iorestoacasa|stayathome|lockdown|[qc]uar[ae]nt[ei]n[ea]|कोरोनावाइरस|ਕੋਰੋਨਾਵਾਇਰਸ|massisolation|distanziamento\s*sociale|social\s*distancing|감염병 세계적 유행|パンデミック|コロナウイルス|सर्वव्यापी महामारी|ਸਰਬਵਿਆਪੀ ਮਹਾਂਮਾਰੀ|пандемия|коронавирус|social\s*distancing|distanciamiento\s*social|코로나|कोविड|ਕੋਵਿਡ)/i

### Regular expression Covid (javascript) - 2
/(corona|covid|virus|pandemi[aec]|epidemi[aec]|tampon[ei]*|sierologico|mascherin[ae]|코로나 바이러스|fase\s*(2|due)|iorestoacasa|stayathome|lockdown|[qc]uar[ae]nt[äae]i*n[ea]|कोरोनावाइरस|ਕੋਰੋਨਾਵਾਇਰਸ|massisolation|distanziamento\s*sociale|social\s*distancing|감염병 세계적 유행|パンデミック|コロナウイルス|सर्वव्यापी महामारी|ਸਰਬਵਿਆਪੀ ਮਹਾਂਮਾਰੀ|пандемия|коронавирус|social\s*distancing|distanciamiento\s*social|코로나|कोविड|ਕੋਵਿਡ|vaccin[oe]*|isolamento|intensiv[ao]|assembrament[io]|guant[oi]|dpi|disinfettante|swabs|emergenza|emergency|droplets*|aerosol|isolation|intensive\s*care|crowd|gloves*|disinfectant|감염병 유행|완충기|마스크|나는 집에있어|폐쇄|사회적 거리두기|백신|모임|비상 사태|비말|범 혈증|écouvillon|masques*|restealamaison|confin[ae]mento*|distanciation\s*sociale|soins\s*intensifs|rassemblements|désinfectant|urgence|gouttelettes|飛沫|タンポン|マスケリン|封鎖|人混みを避ける|ワクチン|隔離|集会|集中治療|緊急|बूंदें|फाहे|मास्क|लॉकडाउन|सोशल डिस्टन्सिंग|टीका|गहन देखभाल|समारोहों|आपातकालीन|gotas|cotonetes|m[áa]scaras|ficoemcasa|vac[iu]na|reuni[õo]n*es|emerg[êe]ncia|капли|тампоны|маски|карантин|социальное\s*дистанцирование|вакцина|интенсивная\s*терапия|сходы|чрезвычайное\s*происшествие|hisopos|mequedoencasa|cierre|Tröpfchen|Tupfer|Masken|bleibezuHause|Ausgangssperre|soziale\s*Distanzierung|Impfstoff|Intensivstation|Versammlungen|Notfall|건강\s*격리|検疫|संगरोध|[кК]арантин)/i

### Regular expression Covid - 3
/(corona|covid|virus|pandemi[aec]|epidemi[aec]|tampon[ei]*|sierologico|mascherin[ae]|코로나 바이러스|fase\s*(2|due)|iorestoacasa|stayathome|lockdown|[qc]uar[ae]nt[äae]i*n[ea]|कोरोनावाइरस|ਕੋਰੋਨਾਵਾਇਰਸ|massisolation|distanziamento\s*sociale|social\s*distancing|감염병 세계적 유행|パンデミック|コロナウイルス|सर्वव्यापी महामारी|ਸਰਬਵਿਆਪੀ ਮਹਾਂਮਾਰੀ|пандемия|коронавирус|social\s*distancing|distanciamiento\s*social|코로나|कोविड|ਕੋਵਿਡ|vaccin[oe]*|isolamento|intensiv[ao]|assembrament[io]|guant[oi]|dpi|disinfettante|swabs|emergenza|emergency|droplets*|aerosol|isolation|intensive\s*care|crowd|gloves*|disinfectant|감염병 유행|완충기|마스크|나는 집에있어|폐쇄|사회적 거리두기|백신|모임|비상 사태|비말|범 혈증|écouvillon|masques*|restealamaison|confin[ae]mento*|distanciation\s*sociale|soins\s*intensifs|rassemblements|désinfectant|urgence|gouttelettes|飛沫|タンポン|マスケリン|封鎖|人混みを避ける|ワクチン|隔離|集会|集中治療|緊急|बूंदें|फाहे|मास्क|लॉकडाउन|सोशल डिस्टन्सिंग|टीका|गहन देखभाल|समारोहों|आपातकालीन|gotas|cotonetes|m[áa]scaras|ficoemcasa|vac[iu]na|reuni[õo]n*es|emerg[êe]ncia|капли|тампоны|маски|карантин|социальное\s*дистанцирование|вакцина|интенсивная\s*терапия|сходы|чрезвычайное\s*происшествие|hisopos|mequedoencasa|cierre|Tröpfchen|Tupfer|Masken|bleibezuHause|Ausgangssperre|soziale\s*Distanzierung|Impfstoff|Intensivstation|Versammlungen|Notfall|건강\s*격리|検疫|संगरोध|[кК]арантин|hand|man[io]s*|소유|手|[Рp]уки|Hände|mãos)/i

## query applyed
### Set all videos at false
db.video_merge2.update({},{$set : {covid_tags : false, covid_title : false}},{multi : true})

### Per i tags
db.video_merge2.update({tags : {$in : [REGEX]}}, {$set : {covid_tags: true}}, {multi : true})

### Per il title
db.video_merge2.update({title : {$in : [REGEX]}}, {$set : {covid_title: true}}, {multi : true})

## Query da testare:
### Contare numero video covid per paese
db.videos_march.aggregate(
    [{$match : {
                covid_tags : true,
                covid_title : true},
     {$group : {
                _id : "country_name", 
                count : {$sum : 1}}
     }
    ]
)
### Data con il video con il maggior numero di visualizzazioni in Francia

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
result = client['YT_data']['merge_c'].aggregate([
    {
        '$project': {
            'country_name': '$country_name', 
            'timestamp': '$timestamp', 
            'date': {
                '$dateToParts': {
                    'date': '$timestamp'
                }
            }, 
            'title': '$title', 
            'giorno': '$date.hour', 
            'visualizzazioni': '$statistics.view_count'
        }
    }, {
        '$match': {
            'country_name': 'Francia'
        }
    }, {
        '$group': {
            '_id': {
                'timestamp': '$timestamp', 
                'title': '$title'
            }, 
            'somma': {
                '$sum': '$visualizzazioni'
            }
        }
    }, {
        '$group': {
            '_id': '$_id', 
            'massViz': {
                '$max': '$somma'
            }
        }
    }, {
        '$sort': {
            'massViz': -1
        }
    }, {
        '$limit': 1
    }
])

### Video covid il giorno del massimo aumento giornaliero di casi in Italia
db.video.find(
    {}
)