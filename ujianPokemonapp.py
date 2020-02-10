from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np
import pandas as pd
import requests

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pokeHome.html')

pokemonDf = pd.read_csv('Pokemon.csv')
print(pokemonDf.head(5))

def combine(i):
    return str(i['Type 1'])+ ',' +str(i['Generation'])+','+str(i['Legendary'])

pokemonDf['Attribute']= pokemonDf.apply(combine, axis=1)
pokemonDf['Name']= pokemonDf['Name'].apply(lambda i: i.lower())

ext = CountVectorizer()
exfit = ext.fit_transform(pokemonDf['Attribute'])
ext.get_feature_names()

exfit = exfit.toarray()

cosScore = cosine_similarity(exfit)
cosScore

pokemonName = "bulbasaur"
indexfav = pokemonDf[pokemonDf['Name'] == pokemonName].index[0]
indexfav

recPokemon = list(enumerate(cosScore[indexfav]))
recPokemon = list(filter(lambda x: x[1] > 0.5, recPokemon))
recPokemon = recPokemon[:6]

recList = []
for i in recPokemon:
    recList.append(pokemonDf.iloc[i[0]][:-1])

recommendation = pd.DataFrame(recList)

pokemonIndex = recommendation.index

image = []

for i in pokemonIndex:
    image.append(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png')

recommendation['image'] = image



@app.route('/FindPokemon', methods=['GET','POST'])
def Cari():
    body = request.form
    pokeFav = body['Pokemon'].capitalize()
    pokefav = pokeFav.lower()
    indexFav = pokemonDf[pokemonDf["Name"] == pokeFav].index()
    if pokefav not in list(pokemonDf['Name']):
        return redirect('/NotFound')
    favorit = pokemonDf.iloc[indexFav]['#',"Name",'Type 1','Generation','Legendary']
    url = 'https://pokeapi.co/api/v2/pokemon/'+ pokefav
    url = requests.get(url)
    # imageRecom = url.json()["sprites"]["front_default"]
    pokeSamaSortir = sorted(recPokemon, key= lambda x:x[1], reverse= True)
    Rekom=[]
    for item in pokeSamaSortir[:7]:
        x={}
        if item[0] != indexfav:
            nama = pokemonDf.iloc[item[0]]['Name'].capitalize()
            tipe = pokemonDf.iloc[item[0]]['Type 1']
            legend = pokemonDf.iloc[item[0]]['Legendary']
            gen = pokemonDf.iloc[item[0]]['Generation']
            url = 'https://pokeapi.co/api/v2/pokemon/'+ nama.lower()
            url = requests.get(url)
            # pic = url.json()["sprites"]["front_default"] 
            x['Name']= nama
            x['Type']= tipe
            x['Legend']= legend
            x['Generation']= gen
            # x["gambar"] = pic
            Rekom.append(x)
    return render_template('pokeHasil.html',rekomen= Rekom, favorit= favorit) 


@app.route('/NotFound')
def notFound():
    return render_template('pokeError.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
