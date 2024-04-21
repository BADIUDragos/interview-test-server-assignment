import os
import json
brackets_dir = os.path.join(os.path.dirname(__file__), '../api/tax_calculator/fixtures')


def _get_brackets(tax_year):
    filename = 'tax-brackets--%d.json' % tax_year
    file_with_path = os.path.join(brackets_dir, filename)

    with open(file_with_path) as config_file:
        json_contents = json.load(config_file)
        config_file.close()

    return json_contents

