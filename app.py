from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
#render template renders html

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://harrison.comfort:dreamsmoneycanbuy@localhost:5432/todos'

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

#ensures that tables are created for models we create
#db.create_all()

#controlers
@app.route('/todos/create', methods=['POST'])

def create_todo():
   description = request.get_json()['description']
   todo = Todo(description=description)
   db.session.add(todo)
   db.session.commit();
   return jsonify({
        'description': todo.description
     })

@app.route('/')
#controller->
def index():
    return render_template('index.html', data=Todo.query.all())

#always include this at the bototm of vode
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")


#def create_person():
#    body={}
#    error=FALSE
#    try:
#        name = request.get_json()['name']
#        person = Person(name=name)
#        body['name'] = person.name
#        db.session.add(person)
#        db.session.commit()
#    except:
#        error=True
#        db.session.rollback()
#        print(sys.exc_info())
#    finally:
#        db.session.close()
#        if error == True:
#            abort(400)
#        else:
#            return(jsonify(body))


#route handler
