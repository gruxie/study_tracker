from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

DATA_DIR = 'data'
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
SUBJECTS_FILE = os.path.join(DATA_DIR, 'subjects.json')
OBSERVATIONS_FILE = os.path.join(DATA_DIR, 'observations.json')

# Utility Functions
def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def validate_phone(phone):
    pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    return pattern.match(phone)

def validate_email(email):
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.(net|com|org|edu|gov)$')
    return pattern.match(email)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Project Browser
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    projects = load_data(PROJECTS_FILE)
    if request.method == 'POST':
        try:
            unique_number = int(request.form['unique_number'])
            # Check for uniqueness
            if any(p['unique_number'] == unique_number for p in projects):
                flash('Project number must be unique.', 'error')
                return redirect(url_for('projects'))
            title = request.form['title']
            description = request.form['description']
            tags = request.form['tags'].split(',')  # Assuming tags are comma-separated
            tags = [tag.strip() for tag in tags if tag.strip()]
            if len(tags) > 100:
                flash('A maximum of 100 tags are allowed.', 'error')
                return redirect(url_for('projects'))
            new_project = {
                'unique_number': unique_number,
                'title': title,
                'description': description,
                'tags': tags
            }
            projects.append(new_project)
            save_data(PROJECTS_FILE, projects)
            flash('Project added successfully!', 'success')
        except ValueError:
            flash('Unique number must be an integer.', 'error')
        return redirect(url_for('projects'))
    return render_template('projects.html', projects=projects)

# Subject Browser
@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    subjects = load_data(SUBJECTS_FILE)
    projects = load_data(PROJECTS_FILE)
    if request.method == 'POST':
        try:
            project_number = int(request.form['project_number'])
            # Validate project exists
            if not any(p['unique_number'] == project_number for p in projects):
                flash('Invalid project number.', 'error')
                return redirect(url_for('subjects'))
            subject_number = int(request.form['subject_number'])
            # Check for unique subject number
            if any(s['subject_number'] == subject_number for s in subjects):
                flash('Subject number must be unique.', 'error')
                return redirect(url_for('subjects'))
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            nick_name = request.form['nick_name']
            phone = request.form['phone']
            email = request.form['email']
            url = request.form['url']
            # Validate phone and email
            if not validate_phone(phone):
                flash('Invalid phone number format. Use ###-###-####.', 'error')
                return redirect(url_for('subjects'))
            if not validate_email(email):
                flash('Invalid email format or unsupported domain.', 'error')
                return redirect(url_for('subjects'))
            new_subject = {
                'project_number': project_number,
                'subject_number': subject_number,
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'nick_name': nick_name,
                'phone': phone,
                'email': email,
                'url': url
            }
            subjects.append(new_subject)
            save_data(SUBJECTS_FILE, subjects)
            flash('Subject added successfully!', 'success')
        except ValueError:
            flash('Project and Subject numbers must be integers.', 'error')
        return redirect(url_for('subjects'))
    return render_template('subjects.html', subjects=subjects, projects=projects)

# Observation Browser
@app.route('/observations', methods=['GET', 'POST'])
def observations():
    observations = load_data(OBSERVATIONS_FILE)
    projects = load_data(PROJECTS_FILE)
    subjects = load_data(SUBJECTS_FILE)
    if request.method == 'POST':
        try:
            project_number = int(request.form['project_number'])
            subject_number = int(request.form['subject_number'])
            # Validate project and subject
            if not any(p['unique_number'] == project_number for p in projects):
                flash('Invalid project number.', 'error')
                return redirect(url_for('observations'))
            if not any(s['subject_number'] == subject_number and s['project_number'] == project_number for s in subjects):
                flash('Invalid subject number for the selected project.', 'error')
                return redirect(url_for('observations'))
            observation_text = request.form['observation']
            if len(observation_text) > 1000:
                flash('Observation text cannot exceed 1000 characters.', 'error')
                return redirect(url_for('observations'))
            unique_observation_id = max([o['unique_observation_id'] for o in observations], default=0) + 1
            new_observation = {
                'project_number': project_number,
                'subject_number': subject_number,
                'observation': observation_text,
                'unique_observation_id': unique_observation_id
            }
            observations.append(new_observation)
            save_data(OBSERVATIONS_FILE, observations)
            flash('Observation added successfully!', 'success')
        except ValueError:
            flash('Project and Subject numbers must be integers.', 'error')
        return redirect(url_for('observations'))
    return render_template('observations.html', observations=observations, projects=projects, subjects=subjects)

# View Observations for a Subject
@app.route('/observations/<int:subject_number>')
def view_observations(subject_number):
    observations = load_data(OBSERVATIONS_FILE)
    subjects = load_data(SUBJECTS_FILE)
    subject = next((s for s in subjects if s['subject_number'] == subject_number), None)
    if not subject:
        flash('Subject not found.', 'error')
        return redirect(url_for('observations'))
    subject_observations = [o for o in observations if o['subject_number'] == subject_number]
    return render_template('view_observations.html', subject=subject, observations=subject_observations)

if __name__ == '__main__':
    app.run(debug=True)
