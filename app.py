import os
from flask import Flask, render_template, url_for, redirect, session, escape, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
import strgen

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Link(db.Model):

    __tablename__ = 'links'
    id = db.Column(db.Integer,primary_key = True)
    olink = db.Column(db.Text)
    slink = db.Column(db.Text)
    views = db.Column(db.Integer)

    def __init__(self,olink,slink,views):
        self.olink = olink
        self.slink = slink
        self.views = views


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST' :
        olink = request.form['olink']
        slink = strgen.StringGenerator("[\d\w]{7}").render()
        check = Link.query.filter_by(slink=slink).first()
        if not check :
            new_link = Link(olink,slink,0)
            db.session.add(new_link)
            db.session.commit()
            return render_template('link.html',link=new_link)
        else :
            return render_template('index.html')
    return render_template('index.html')        

@app.route('/<some_link>')
def link(some_link):
    nlink = Link.query.filter_by(slink=some_link).first()
    if not nlink :
        return render_template('404.html')
    else :
        flink = nlink.olink
        return redirect("https://"+flink)    


if __name__ == '__main__':
    app.run(debug=True)    