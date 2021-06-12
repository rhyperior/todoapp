from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    addition_Date = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String, nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.description}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        task_name = request.form['taskname']
        description = request.form['description']
        priority = request.form['priority']
        print(task_name+'  '+description+' '+priority)
        todo = ToDo(task_name=task_name, description=description, priority=priority)
        db.session.add(todo)
        db.session.commit()
        
    all_todo = ToDo.query.all()
    return render_template('index.html', alltodo=all_todo)


@app.route('/update/<int:sno>' ,methods=['GET', 'POST'])
def update(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        task_name = request.form['taskname']
        description = request.form['description']
        priority = request.form['priority']
        todo.task_name = task_name
        todo.description = description
        todo.priority = priority
        print('yoooo muthafuckaaaa')
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    # print(list(request.form.keys()))
    print(todo)
    return render_template('updates.html', todo=todo)
    # return 'Hello, User, these are the records that you are looking for.!'

@app.route('/delete/<int:sno>')
def delete(sno):
    record_id = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(record_id)
    db.session.commit()
    return  redirect("/")


if __name__=="__main__":
    app.run(debug=True, port=80, host='0.0.0.0')

