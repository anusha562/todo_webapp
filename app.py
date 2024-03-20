from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

# Define the Task model
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:anusha%40123@localhost/curd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'my_secret_key'  # a secret key for flashing messages
db= SQLAlchemy(app)

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_description=db.Column(db.String(100))
    day =db.Column(db.String(100))
    done=db.Column(db.Boolean)

@app.route('/')
def home():
        return render_template('home.html')

@app.route('/todo',methods=['GET'])
def index():
        todo_list = Todo.query.all()
        return render_template('todo.html', todo_list=todo_list),200

@app.route('/add',methods=['POST'])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        day = request.form.get("day")
        if not(len(name) <= 0 or len(day)<=0):
            new_task=Todo(task_description=name,day=day,done=False)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("index"))
        elif (len(name) <= 0):
            flash("Task cannot be empty", category='warning')
            return redirect(url_for("index"))
        elif (len(day) <= 0):
            flash("Mention a day for the task", category='warning')
            return redirect(url_for("index"))

@app.route('/update/<int:todo_id>', methods=['PUT','POST'])
def update(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.task_description = request.form.get('task_description')
        todo.day = request.form.get('day')
        todo.done = 'done' in request.form  # Check if 'done' checkbox is checked
        db.session.commit()
        flash("Task updated successfully",category='message')
    else:
        flash("Task not found",category='error')
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>',methods=['GET','DELETE'])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo= Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        flash("Task deleted successfully",category='message')
    else:
        flash("Task cannot be deleted successfully",category='error')
    return redirect(url_for("index"))

if __name__=='__main__':
    app.run(debug=True)