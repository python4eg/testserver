import os

from optparse import OptionParser
import re
from fb import GitLogs
from log2mail import send_mail

qt_links = []

db_link = 'http://hudsonjob/ws/%s/db/%s'

palm_link = 'http://hudsonjob/ws/%s_%s/'

parser = OptionParser()
parser.add_option('-p', '--platform', type='choice', choices=['Win', 'Qt'], dest='platform')
parser.add_option('-b', '--branch', dest='branch')
parser.add_option('-d', '--database', dest='database')
parser.add_option('-v', '--version', dest='version')

(options, args) = parser.parse_args()

version = options.version
branch = options.branch
platform = options.platform
database = os.path.join(os.path.normpath(options.database), '')

print 'Curent platform:%s, branch:%s, workspace:%s' % (platform,branch,database,)

def get_qt_version():
    qt_version = '0.0.0.0'
    rcFile = 'path/to/varion.rc'
    versionTemplate = re.compile('FILEVERSION (\d+),(\d+),(\d+),(\d+)')
    f = open(rcFile)
    try:
        strings = f.read()
        ver = versionTemplate.search(strings)
        temp = list(ver.groups())
        temp[2] = version
        qt_version = '.'.join(temp)
    finally:
        f.close()
    print 'Qt version: %s' % (qt_version,)
    return qt_version

def palm_gen(version):
    pass

def qt_gen(version):
    msg = ''
    notesFileName = 'fogbugzNotes-%s.txt' % (version,)
    attachedFiles = [notesFileName]

    msg = 'Qt Builds:\n'
    for link in qt_links:
        msg += link % (branch, version,)
        msg += '\n'

    msg += '\nCustom database:\n'
    for root, dirs, files in os.walk(database):
        for file in files:
            if file.endswith('sql.db'):
                msg += db_link % (branch, file,)
                print 'Custom database: %s' % db_link % (branch, file,)
                msg += '\n'

    send_mail('Qt installer links', msg, attachedFiles)

def main():
    main_version = get_qt_version()
    gitGen = GitLogs(main_version)
    gitGen.parse_commits()
    gitGen.save_timestamp()
    if platform == 'Win':
        qt_gen(main_version)
    elif platform == 'Qt':
        palm_gen(main_version)
    else:
        print 'Platform non supported'
    

if __name__ == '__main__':
    main()
