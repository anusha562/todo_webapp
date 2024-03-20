from flask import Flask,render_template,request,redirect,url_for,flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

# Define the Task model
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:anusha%40123@localhost/curd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "TODO LIST API"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_description=db.Column(db.String(100))
    day =db.Column(db.String(100))
    done=db.Column(db.Boolean)

# @app.route('/')
# def home():
#         return render_template('home.html')

@app.route('/todo',methods=['GET'])
def index():
    todo_list = Todo.query.all()
    tasks = []
    for todo in todo_list:
        tasks.append({
            'task_id': todo.task_id,
            'task_description': todo.task_description,
            'day': todo.day,
            'done': todo.done
        })
    return jsonify(tasks), 200

@app.route('/add',methods=['POST'])
def add():
        data = request.json
        name = data.get("task_description")
        day = data.get("day")
        if not (len(name) <= 0 or len(day) <= 0):
            new_task = Todo(task_description=name, day=day, done=False)
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': 'Task added successfully'}), 201
        else:
            return jsonify({'error': 'Missing required fields'}), 400
        
@app.route('/update/<int:todo_id>', methods=['PUT'])
def update(todo_id):
        todo = Todo.query.get(todo_id)
        if todo:
            data = request.json
            todo.task_description = data.get('task_description')
            todo.day = data.get('day')
            todo.done = data.get('done', False)
            db.session.commit()
            return jsonify({'message': 'Task updated successfully'}), 200
        else:
            return jsonify({'error': 'Invalid task id: Bad request'}), 404

@app.route('/delete/<int:todo_id>', methods=['DELETE', 'GET'])
def delete(todo_id):
        todo = Todo.query.get(todo_id)
        if todo:
            todo = Todo.query.get(todo_id)
            db.session.delete(todo)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'error': 'Invalid task id: Bad request'}), 400
   

if __name__=='__main__':
    app.run(debug=True)