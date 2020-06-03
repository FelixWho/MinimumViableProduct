import json

path = "./database_with_mayo_and_medline_links.txt"

with open(path) as jsonfile:
    data = json.load(jsonfile)

diseases = data.keys()

new_dict = dict()

for disease in diseases:
    new_dict[disease.lower()] = data[disease]

converted_data = json.dumps(new_dict)

out = open("database_with_mayo_and_medline_links.txt", "w")
out.write(converted_data)
out.close()  