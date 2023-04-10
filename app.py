from flask import Flask, request, redirect, render_template, url_for
from models import Project, db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db.init_app(app)

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/projectadded')
def projectadded():
    projects = Project.query.all()
    return render_template('projectadded.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    projects = Project.query.all()
    if request.method == 'POST':
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date() 
        skills = request.form['skills']
        short_description = request.form['short_description']
        github_link = request.form['github_link']

        project = Project(title=title, date=date, skills=skills, short_description=short_description, github_link=github_link)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projectadded'))
    return render_template('projectform.html', projects=projects)

@app.route('/project/<int:id>')
def project_detail(id):
    projects = Project.query.all()
    project = Project.query.get(id)
    return render_template('detail.html', project=project, projects=projects)

@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    projects = Project.query.all()
    project = Project.query.get(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        project.skills = request.form['skills']
        project.short_description = request.form['short_description']
        project.github_link = request.form['github_link']
        db.session.commit()
        return redirect(url_for('project_detail', id=project.id))
    return render_template('editproject.html', project=project, projects=projects)

@app.route('/about')
def aboutpage():
    projects = Project.query.all()
    return render_template('about.html', projects=projects)

@app.route('/projectdeleted')
def projectdeleted():
    projects = Project.query.all()
    return render_template('projectdeleted.html', projects=projects)

@app.route('/projects/<int:id>/delete', methods=['GET', 'POST'])
def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projectdeleted'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not Project.query.all(): 
            # My Projects
            first_project = Project('The Number Guessing Game', datetime.strptime('2023-02-28', '%Y-%m-%d').date(), 'Python', 'This small console game is developed using Python only. The goal of the game is to guess random number in a range from 0 to 10.', 'https://github.com/webark-de/Python---The-Number-Guessing-Game')
            second_project = Project('Basketball Team Stats Tool', datetime.strptime('2023-03-07', '%Y-%m-%d').date(), 'Python', 'Simple Python project', 'https://github.com/webark-de/Basketball-Team-Stats-Tool')
            third_project = Project('Phrase Hunter Game', datetime.strptime('2023-03-23', '%Y-%m-%d').date(), 'HTML, CSS, JavaScript', 'This game is a good example of using object-oriented programming principles in Python, including creating classes, defining methods, and managing attributes of objects.', 'https://github.com/webark-de/OOP-phrase-hunter-game')
            fourth_project = Project('Store Invetory', datetime.strptime('2021-03-30', '%Y-%m-%d').date(), 'Python, SQL, sqlalchemy', 'Console application that allows you to easily interact with data for a store inventory.', 'https://github.com/webark-de/store_inventory')
            
            db.session.add_all([first_project, second_project, third_project, fourth_project])
            db.session.commit()
        else:
            print('My projects already added to database')    

    app.run(debug=False, port=8002, host='127.0.0.1')
