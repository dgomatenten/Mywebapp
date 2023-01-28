
from flask import Blueprint
from flask import Flask, render_template, request, redirect,jsonify
from flask import url_for
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import orm 

from . import db1
from Mywebapp.word import wordcnt



bp = Blueprint("eng", __name__)


#Base = declarative_base()

#class Flashcard(Base):
class EngContent(db1.Model):
    __tablename__ = "EN_CONTENTS"
    id = Column(Integer, primary_key=True)
    Type = Column(String)       # Reading, Listening, Speaking, Writing
    Content = Column(String)
    Title = Column(String)

#class Flashcard(Base):
class EngWord(db1.Model):
    __tablename__ = "EN_CONT_WORDS"
    id = Column(Integer, primary_key=True)
    cont_id = Column(Integer)
    word = Column(String)
    count = Column(Integer)
    
    
#@bp.route('/lab',methods=['GET', 'POST'])

@bp.route('/eng/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        type = request.form['type']
        title = request.form['title']
        content = request.form['content']
        
        contents = EngContent(Type=type,Title=title,Content=content)

        db1.session.add(contents)
        db1.session.commit()
    
    return render_template('/eng/register.html')


@bp.route('/eng/engindex',methods=['GET', 'POST'])
def engindex():
    data = EngContent.query.all()
    #conver Json 
    return render_template('/eng/contindex.html', contents=data)

@bp.route('/eng/<int:id>/contupdate',methods=['GET', 'POST'])
def contupdate(id):

    key = id
    contents = EngContent.query.filter_by(id = key).first()

    
    
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        content = request.form['content']
        contents = EngContent(id=id,Title=title,Content=content)

        db1.session.merge(contents)
        db1.session.commit()

        return redirect(url_for('eng.index'))
    
    
    return render_template('/eng/contupdate.html',content=contents,id=key,title=contents.Title)

@bp.route('/eng/<int:id>/wordcount',methods=['GET', 'POST'])
def wordcount(id):

    key = id

    contents = EngContent.query.filter_by(id = key).first()
    content = contents.Content

    engcont = wordcnt(content)
    engconts=engcont.wordcount()
  
    for x, y in engconts.items():
        print(x, y)
        contents = EngWord(cont_id = key,word = x, count=y)
        db1.session.merge(contents)
        db1.session.commit()
 
    # loop to set word data to model EngWord
    # load data to DB 
    #return redirect(url_for('lab.index'))
    return render_template('/eng/test.html',content=engconts)
