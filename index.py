from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Person %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        # person_content = request.form['person']
        # new_person = People(name=person_content)
        
        # try:
        #     db.session.add(new_person)
        #     db.session.commit()
        #     return redirect('/settings')
        # except:
        #     return 'There was an issue adding your person'
        return 'Should not happen'

    else:
        people = People.query.order_by(People.date_created).all()
        return render_template('index.html', people=people)
        # return render_template('settings.html', people=people)



@app.route('/settings', methods=['POST','GET'])
def settings():
    if request.method == 'POST':
        person_content = request.form['person']
        new_person = People(name=person_content)
        
        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect('/settings')
        except:
            return 'There was an issue adding your person'

    else:
        people = People.query.order_by(People.date_created).all()
        return render_template('settings.html', people=people)

@app.route('/settings/delete/<int:id>')
def delete(id):
    person_to_delete = People.query.get_or_404(id)
    
    try:
        db.session.delete(person_to_delete)
        db.session.commit()
        return redirect('/settings')
    except:
        return 'There was a problem deleting that person'

@app.route('/settings/update/<int:id>', methods=['GET','POST'])
def update(id):
    person = People.query.get_or_404(id)

    if request.method == 'POST':
        person.name = request.form['person']
        
        try:
            db.session.commit()
            return redirect('/settings')
        except:
            return 'There was an issue updating person'

    else:
        return render_template('update.html', person=person)

if __name__ == "__main__":
    app.run(debug=True)

