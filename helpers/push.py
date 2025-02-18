
from datetime import datetime
from datetime import timedelta
import json
import os
import operator as op
import itertools as it

TOPIC_WORD_LIMIT = 100

tasks_file = 'files/in_progress.json'
backlog_file = 'files/backlog.json'

def roundrobin(*iterables):
    sentinel = object()
    return (a for x in it.zip_longest(*iterables, fillvalue=sentinel) 
            for a in x if a != sentinel)

if not os.path.exists(tasks_file):
    if os.path.exists(backlog_file):
        tasks = json.load(open(backlog_file, "rt", encoding="UTF-8"))
        index_start = max(tasks, key=lambda task: task['index'])['index'] + 1
    else:
        tasks = []
        index_start = 1
    for root, dirs, files in os.walk('files/new'):
        for i, file in enumerate(files):
            input_file = f"{root}/{file}"
            data = json.load(open(input_file, "rt", encoding="UTF-8"))
            for skill in data["skills"]:
                task = { 
                    "index": i + index_start,
                    "topic": data['topic'],
                    "name": skill['name'],
                    "text_prompt": f"Расскажи как {skill['name']}, используй не более {TOPIC_WORD_LIMIT} слов, используй смайлики",
                    "image_prompt": f"Нарисуй рисунок, вдохновлённый темой '{skill['name']}'",
                    "group": skill['group'],
                }
                tasks.append(task)
            processed_file = f"files/processed/{file}"
            os.rename(input_file, processed_file)

    tasks = sorted(tasks, key=lambda task: task['index'])

    x = [list(v) for k, v in it.groupby(tasks, key=op.itemgetter('index'))]
    tasks = list(roundrobin(*x))

    curr_date = datetime.today() + timedelta(days=1)
    for task in tasks:
        task["date"] = curr_date.strftime("%Y-%m-%d")
        curr_date += timedelta(days=1)

    json.dump(tasks, open(tasks_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)
    if os.path.exists(backlog_file):
        os.remove(backlog_file)
    print(f"{len(tasks)} tasks created")
else: 
    print("Tasks already exists, revert before push")