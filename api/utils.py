import json


def _open_fixture(file_path):
    try:
        with open(file_path) as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise ValueError("The file %s does not exist" % file_path)
    except json.JSONDecodeError:
        raise ValueError("The file %s contains invalid JSON" % file_path)
