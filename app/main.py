# app/main.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = r.lrange('tasks', 0, -1)
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        r.rpush('tasks', task)
        return jsonify({'message': 'Task added'}), 201
    return jsonify({'error': 'No task provided'}), 400

@app.route('/tasks/<int:index>', methods=['DELETE'])
def delete_task(index):
    tasks = r.lrange('tasks', 0, -1)
    if 0 <= index < len(tasks):
        r.lrem('tasks', 1, tasks[index])
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found....'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
