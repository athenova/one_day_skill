
from datetime import datetime
from datetime import timedelta
import json
import os

TOPIC_WORD_LIMIT = 300

tasks_file = 'files/in_progress.json'
backlog_file = 'files/backlog.json'

if os.path.exists(tasks_file):
    backlog = []
    in_progress = json.load(open(tasks_file, "rt", encoding="UTF-8"))
    for task in in_progress:
        if task['date'] > datetime.today().strftime('%Y-%m-%d'):
            backlog.append(task)
    json.dump(backlog, open(backlog_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)
    os.remove(tasks_file)
    print(f"{len(backlog)} tasks reverted")
else: 
    print("Nothing to revert")