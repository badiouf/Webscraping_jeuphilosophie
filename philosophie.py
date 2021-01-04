#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, session, request, redirect, flash,url_for
from getpage import getPage
import os


app = Flask(__name__)

app.secret_key = b'012(\xffb\xb4\xd6_\xbe\x16\x10\xb9\x91\x1e\xf1'  #os.urandom(16,seed=2)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')#, message="Bonjour, monde !"

# Si vous définissez de nouvelles routes, faites-le ici

@app.route('/new-game', methods=['POST'])
def new_game():
    session['article']=request.form["start"]
    session['score']=0
    response=getPage(session['article'])
    titre=response[0]
    liens=response[1]
    if len(liens)==0 :
        flash("Le lien demandé n'existe pas.","error")
        return render_template('index.html')
    elif titre=="Philosophie":
        flash("Veuillez saisir un mot différent de Philosophie","error")
        return render_template('index.html')
    return redirect(url_for('game'))

@app.route('/game', methods=['GET','POST'])
def game():
    response=getPage(session['article'])
    titre=response[0]
    liens=response[1]
    if request.form=='GET':
        #if len(liens)==0 or titre=="Philosophie":
        #    flash("Le lien demandé n'existe pas. Veuillez essayer encore")
        return render_template('game.html',page=titre,liens=liens)     
    else:
        if len(liens)==0 :
            flash('Oups! Vous avez perdu: cette page ne contient aucun lien.',"echec")
            return render_template('index.html')   
        else:
            if titre=='Philosophie':
                flash('Félicitation! Vous avez gagné et votre score est  {} '.format(session['score']),'victoire')
                return render_template('index.html')
            session['score']+=1
            return render_template('game.html',page=titre,liens=liens)

#@app.template_filter('page_cible')
#def pagecible(lien):
#    pagecible=getPage(lien)[0]
#    return pagecible 

@app.route('/move', methods=['POST'])
def move():
    session['article']=request.form["destination"]
    return redirect('game')

if __name__ == '__main__':
    app.run(debug=True)

