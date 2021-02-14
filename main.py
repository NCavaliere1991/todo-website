from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)
Bootstrap(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    due = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# db.create_all()


class TodoForm(FlaskForm):
    task = StringField("Write your task here.", validators=[DataRequired()])
    due = StringField("When is your task due?", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
def home():
    all_tasks = db.session.query(Todo).all()
    form = TodoForm()
    if form.validate_on_submit():
        new_task = Todo(
            task=form.task.data,
            due=form.due.data,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html", tasks=all_tasks, form=form)


@app.route('/delete')
def delete_task():
    task_id = request.args.get("id")
    task = Todo.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)