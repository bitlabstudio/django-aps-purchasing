import os
import re

from fabric.api import lcd, local
from fabric.colors import green, red
from fabric.utils import abort


def dumpdata():
    local('python2.7 ./manage.py dumpdata --indent 4 --natural auth --exclude auth.permission > aps_purchasing/fixtures/bootstrap_auth.json')  # NOPEP8


def loaddata():
    local('python2.7 manage.py loaddata aps_purchasing/fixtures/bootstrap_auth.json')  # NOPEP8


def check_coverage():
    """Checks if the coverage is 100%."""
    coverage_path = os.path.join(
        os.path.dirname(__file__), 'aps_purchasing/tests/coverage/')

    with lcd(coverage_path):
        total_line = local('grep -n Total index.html', capture=True)
        match = re.search(r'^(\d+):', total_line)
        total_line_number = int(match.groups()[0])
        percentage_line_number = total_line_number + 4
        percentage_line = local(
            'awk NR=={0} index.html'.format(percentage_line_number),
            capture=True)
        match = re.search(r'<td>(\d.+)%</td>', percentage_line)
        percentage = float(match.groups()[0])
    if percentage < 100:
        abort(red('Coverage is {0}%'.format(percentage)))
    print(green('Coverage is {0}%'.format(percentage)))


def test():
    local('./aps_purchasing/tests/runtests.py')
    check_coverage()
