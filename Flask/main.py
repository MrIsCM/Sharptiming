from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import json

app = Flask(__name__)

# Load saved data
try:
    with open('tracked_time.json', 'r') as f:
        tracked_time = json.load(f)
except FileNotFoundError:
    tracked_time = {}

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Pomodoro session route
@app.route('/start_pomodoro', methods=['POST'])
def start_pomodoro():
    project = request.form.get('project')
    task = request.form.get('task')
    duration = int(request.form.get('duration', 25))  # Default is 25 minutes if not provided
    start_time = time.time()

    # Track session data
    tracked_time[project] = tracked_time.get(project, {})
    tracked_time[project][task] = tracked_time[project].get(task, 0) + duration * 60

    # Save updated tracked time
    with open('tracked_time.json', 'w') as f:
        json.dump(tracked_time, f)

    return jsonify({'message': 'Pomodoro session started', 'project': project, 'task': task})

# Show statistics
@app.route('/statistics')
def statistics():
    return render_template('statistics.html', tracked_time=tracked_time)

if __name__ == '__main__':
    app.run(debug=True)