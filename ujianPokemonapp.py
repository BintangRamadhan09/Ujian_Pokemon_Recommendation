from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

poke = pd.read_csv("Pokemon.csv")
def combination(i):
    return str(i['Type 1'])+ 'space' +str(i['Generation'])+'space'+str(i['Legendary'])
poke['poke']= poke.apply(combination,axis=1)
poke['Name']= poke['Name'].apply(lambda i: i.lower())

ext = CountVectorizer(tokenizer=lambda poke: poke.split('space'))
pokemon = ext.fit_transform(poke['poke'])
skorPoke = cosine_similarity(pokemon)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('pokeHome.html')

@app.route('/hasil', methods=['GET','POST'])
def Cari():
    body = request.form
    pokefav = body['pokemon']
    pokefav = pokefav.lower()
    if pokefav not in list(poke['Name']):
        return redirect('/NotFound')
    indexfav = poke[poke["Name"] == pokefav].index[0]
    favorit = poke.iloc[indexfav][["Name",'Type 1','Generation','Legendary']]
    url = 'https://pokeapi.co/api/v2/pokemon/'+ pokefav
    url = requests.get(url)
    picRecom = url.json()["sprites"]["front_default"]
    pokeRecom = list(enumerate(skorPoke[indexfav]))
    pokeSort = sorted(pokeRecom, key= lambda x:x[1], reverse= True)
    Recom=[]
    for item in pokeSort[:7]:
        x={}
        if item[0] != indexfav:
            nama = poke.iloc[item[0]]['Name'].capitalize()
            type = poke.iloc[item[0]]['Type 1']
            legend = poke.iloc[item[0]]['Legendary']
            gen = poke.iloc[item[0]]['Generation']
            url = 'https://pokeapi.co/api/v2/pokemon/'+ nama.lower()
            url = requests.get(url)
            pic = url.json()["sprites"]["front_default"] 
            x['Name']= nama
            x['Type']= type
            x['Legend']= legend
            x['Generation']= gen
            x["gambar"] = pic
            Recom.append(x)
    return render_template('pokeHasil.html',rekomendasi= Recom, favorit= favorit, pic=picRecom)


@app.route('/NotFound')
def notFound():
    return render_template('pokeError.html')


if __name__=='__main__':
    app.run(debug=True)
