import json

tags_dataset = dict()
with open('data/problems.json') as f:
    data = json.load(f)
    problems = data['problems']
    for problem in problems:
        problem_id = str(problem['contestId']) + problem['index']
        tags = problem['tags']
        tags_dataset[problem_id] = tags

with open("data/tags.json", "w") as outfile:
    json.dump(tags_dataset, outfile)