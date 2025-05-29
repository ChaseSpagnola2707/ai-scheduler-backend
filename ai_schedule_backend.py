
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    tasks = data.get('tasks', [])
    daily_hours = data.get('daily_hours', 2)
    start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")

    # Sort tasks by due date
    tasks.sort(key=lambda x: x["due"])

    schedule = []
    current_date = start_date
    task_index = 0

    while task_index < len(tasks):
        remaining_time = daily_hours
        day_schedule = []

        while remaining_time > 0 and task_index < len(tasks):
            task = tasks[task_index]
            if task["duration_hrs"] <= remaining_time:
                day_schedule.append({"task": task["title"], "hours": task["duration_hrs"]})
                remaining_time -= task["duration_hrs"]
                task_index += 1
            else:
                task["duration_hrs"] -= remaining_time
                day_schedule.append({"task": task["title"], "hours": remaining_time})
                remaining_time = 0

        schedule.append({"date": current_date.strftime("%Y-%m-%d"), "tasks": day_schedule})
        current_date += timedelta(days=1)

    return jsonify(schedule)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
