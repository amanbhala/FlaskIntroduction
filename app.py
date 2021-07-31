from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'   #To tell the application where our database is located
#4 forward slashes is absolute path and 3 forward slashes is relative path.
#Make sure that every alphabet in SQLALCHEMY_DATABASE_URI is in capital letters. 
db = SQLAlchemy(app)   #So database will be initialized with the settings of our app.

#To set up our application's database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(length=200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# @app.route('/')
@app.route('/', methods=['GET','POST'])     #Post will help us to send data to the database.
def index():
    # return "Hello, World"
    if request.method == 'POST':
        task_content = request.form['content']   #To get the data that is present present in the form tag from the imdex.html file
        new_task = Todo(content=task_content)  #Make a new task from the content taken from the form tag in index.html

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error or issue creating the task'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)  #We don't need to specify the name of the folder templates it automatically looks into that folder only.


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task.'


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating the task.'
    else:
        return render_template('update.html',task=task)



if __name__ == '__main__':
    app.run(debug=True)