import json

responses = {}

responses['machine_id'] = 'machine id'
responses['ip'] = 'ip'
responses['port'] = 'port'
responses['data'] = "data"

with open(f"response_machine.json", "w") as json_file:
      json.dump(responses, json_file)