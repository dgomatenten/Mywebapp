
from flask import Blueprint
from flask import Flask, render_template, request, redirect,jsonify
from flask import url_for
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import orm 

from . import db1
from Mywebapp.word import EngDict


bp = Blueprint("Flashcards", __name__)

flc = [
    {'word': 'What is the capital of France?', 'definition': 'Paris'},
    {'word': 'What is the capital of Spain?', 'definition': 'Madrid'},
    {'word': 'What is the capital of Italy?', 'definition': 'Rome'},
]

#Base = declarative_base()

#class Flashcard(Base):
class Flashcard(db1.Model):
    __tablename__ = "FLASHCARDS"
    id = Column(Integer, primary_key=True)
    word = Column(String)
    definition = Column(String)
    JpDef = Column(String)
    status = Column(String)
    audio_link = Column(String)
    Dict_definition = Column(String)

    def to_json(self):
        return {'id': self.id, 'word': self.word, 'definition': self.definition,'JpDef':self.JpDef,'status':self.status,'audio_link':self.audio_link,'Dict_definition':self.Dict_definition}
 
@bp.route('/flashcards',methods=['GET', 'POST'])
def flashcards():
    data = Flashcard.query.all()
    #conver Json 
    flashcards= jsonify([d.to_json() for d in data])
    return render_template('/flashcards/flashcards.html', flashcards=flashcards.get_json())


@bp.route('/flashcards/update_status', methods=['POST'])
def update_status():
    flashcard_id = request.form['flashcard_id']
    status = request.form['status']
    flashcard = Flashcard.query.get(flashcard_id)
    flashcard.status = status
    db1.session.commit()
    return "Success"

@bp.route('/flashcards/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        word = request.form['words']
        definition = request.form['definitions']
        JpDef = request.form['JpDef']
        status = ""
       
        EngDictword = EngDict(word)
        eng = EngDictword.GetEngDict()

        flashcard = Flashcard(word=word,definition=definition,JpDef=JpDef, status=status,audio_link=eng.audio_link,Dict_definition=eng.Dict_definition)
        
        db1.session.add(flashcard)
        db1.session.commit()
    
        return redirect(url_for('Flashcards.index'))
    
    return render_template('/flashcards/register.html')

@bp.route('/flashcards/index',methods=['GET', 'POST'])
def index():
    data = Flashcard.query.all()
    #conver Json 
    return render_template('/flashcards/wordindex.html', flashcards=data)

@bp.route('/flashcards/<int:id>/wordupdate',methods=['GET', 'POST'])
def wordupdate(id):

    key = id
    flashcard = Flashcard.query.filter_by(id = key).first()
    
    if request.method == 'POST':
        id = request.form['id']
        word = request.form['words']
        definition = request.form['definitions']
        JpDef = request.form['JpDef']
        status = ""
        
        EngDictword = EngDict(word)
        eng = EngDictword.GetEngDict()


        flashcard = Flashcard(word=word,definition=definition,JpDef=JpDef, status=status,audio_link=eng.audio_link,Dict_definition=eng.Dict_definition)
        
        db1.session.merge(flashcard)
        db1.session.commit()

        return redirect(url_for('Flashcards.index'))
    
    
    return render_template('/flashcards/wordupdate.html',flashcard=flashcard,id=key,word=flashcard.word)


@bp.route('/flashcards/flcajax', methods=['GET'])
def flcajax():
    index = (request.args.get('index'))
    print(index)
    if index:
        print('index was set from ajax')
        #flashcard = Flashcard.query.filter_by(id = index).first()
        data = Flashcard.query.all()
        #rows = data.statement.execute().fetchall()

        flc_new=[]
        for row in data:
            flc_new.append(row.to_json())
            #flc_new['id'] = i
            #i=i+1    
           # print(flc_new)

        print(flc_new)
        return jsonify(flc_new[int(index)])
    else:
        
        print('index was NOT set from ajax')
        
        return render_template('/flashcards/flashtest.html')
    
