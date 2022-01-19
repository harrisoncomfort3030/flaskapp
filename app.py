from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

#render template renders html

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://harrison.comfort:xxx@localhost:5432/todos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)

def __repr__(self):
    return f'<TodoList {self.id} {self.name}>'

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}, list {self.list_id}>'

#ensures that tables are created for models we create
#db.drop_all()
#db.create_all()

#controlers
@app.route('/todos/create/item', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, list_id=list_id)
        active_list = TodoList.query.get(list_id)
#        todo.list = active_list
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        body['complete'] = todo.complete
        body['id'] = todo.id
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)

@app.route('/todos/create/list', methods=['POST'])
def create_todo_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['name'] = todolist.name
        body['id'] = todolist.id
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/todos/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        for todo in list.todos:
            todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return '', 200

@app.route('/todos/<todo_id>/set-deleted', methods=['DELETE'])
def set_deleted_todo(todo_id):
    try:
        todo=Todo.query.filter_by(id=todo_id)
        todo.delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/todos/<list_id>/list-deleted', methods=['DELETE'])
def set_deleted_list(list_id):
    error = False
    try:
        list=TodoList.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
#controller->
def get_list_todos(list_id):
    return render_template('index.html',
    data=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
    lists=TodoList.query.all(),
    #created a json element by querying a table... this is the key
    active_list=TodoList.query.get(list_id))


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

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
