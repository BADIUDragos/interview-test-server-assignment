import os


from api.utils import _open_fixture

brackets_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def get_tax_brackets(tax_year):

    file_name = 'tax-brackets--%d.json' % tax_year
    file_path = os.path.join(brackets_dir, file_name)

    return _open_fixture(file_path)

