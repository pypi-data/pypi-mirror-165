import json 

class JSON():
    def __init__(self, path):
        self.path = path

    def get(self, key, key2=None):
        with open(self.path) as json_file:
            data = json.load(json_file)
            for keys, values in data.items():
                if keys == key:
                    if key2 != None:
                        return values[key2]
                    else:
                        return values

    def get_all_keys(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
            list = []
            for keys in data:
                list.append(keys)
            return list

    def get_all(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
            return data
    
    def exist(self, key, key2=None):
        with open(self.path) as json_file:
            data = json.load(json_file)
            if key2 != None:
                all_data = self.get(key)
                if key2 not in all_data:
                    return False
                else:
                    return True
            else:
                if key not in data:
                    return False
                else:
                    return True
    
    def add_key(self, data):
        with open(self.path) as json_file:
            json_decoded = json.load(json_file)
            for key, value in data.items():
                json_decoded[key] = value
                with open(self.path, 'w') as json_file:
                    json.dump(json_decoded, json_file, indent=4)

    def detele_key(self, key):
        with open(self.path) as json_file:
            data = json.load(json_file)
            del data[key]
            with open(self.path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def add_value(self, key, value):
        with open(self.path) as json_file:
            data = json.load(json_file)
            for keys, values in value.items():
                data[key][keys] = values
            with open(self.path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def set_value(self, key, data):
        with open(self.path) as json_file:
            json_decoded = json.load(json_file)
            json_decoded[key] = data
            with open(self.path, 'w') as json_file:
                json.dump(json_decoded, json_file, indent=4)
