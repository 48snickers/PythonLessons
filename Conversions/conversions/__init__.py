__version__ = '0.1.0'
import json
import os
import sys

def get_json_str_from_file(filename: str) -> str:
  filename = os.path.join(sys.path[0], filename)
  json_file = open(filename, "r")
  json = json_file.read()
  json_file.close()
  return json



ingredients = json.loads(get_json_str_from_file("../Sample/ingredients.json"))
nutrition = json.loads(get_json_str_from_file("../Sample/nutrition.json"))

print(ingredients)
print(nutrition)