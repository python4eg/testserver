import os

import datetime
import re
import time

from ConfigParser import ConfigParser
from dateutil import parser

msg_template = """
%s
%s
%s
%s
"""

git_message_dict = {'commit' : '',
                    'author' : '',
                    'date' : 0,
                    'msg' : ''}

class GitLogs:

    CONFIG_FILE = 'git.conf'

    def __init__(self, version):
        self.__conf = {}
        self.__get_conf()
        self.__logFile = self.__conf['logfile']
        self.__outputFile = self.__conf['outputfile'] % (version,)
        self.__lastTimestamp = self.__conf['lasttimegrep']
        os.system('git log > %s' % self.__logFile)
        self.regExpGit = re.compile("(^commit\s*(.*)$)?(^Author:\s*(.*)$)?(^Date:\s*(.*)$)?(.*)", re.I+re.M)
        self.regExpFB = re.compile("FB\s*(\d{6})", re.I)


    def __get_text(self):
        strings = ''
        f1 = open(self.__logFile)
        try:
            strings = f1.read()
        finally:
            f1.close()
        return strings

    def __get_log(self):
        f = list()
        temp = ''
        for i in self.regExpGit.findall(self.__get_text()):
            if i[1] is not '':
                f.append(git_message_dict.copy())
                git_message_dict['commit'] = i[1]
                temp = ''
            else:
                if i[3] is not '':
                    git_message_dict['author'] = i[3]
                elif i[5] is not '':
                    git_message_dict['date'] = time.mktime(parser.parse(i[5]).timetuple())
                elif i[6] is not '':
                    temp += i[6]
            git_message_dict['msg'] = temp
        return f

    def __get_conf(self):
        config = ConfigParser()
        config.read(GitLogs.CONFIG_FILE)
        result = {}
        for section in config.sections():
            for option in config.options(section):
                if option == 'lasttimegrep':
                    value = config.getfloat(section, option)
                else:
                    value = config.get(section, option)
                result[option] = value
        self.__conf = result

    def save_timestamp(self):
        config = ConfigParser()
        config.read(GitLogs.CONFIG_FILE)
        config.set('Git', 'lasttimegrep', time.time())
        with open(GitLogs.CONFIG_FILE, 'wb') as configfile:
            config.write(configfile)


    def parse_commits(self):
        list = self.__get_log()
        f1 = open(self.__outputFile, 'w')
        for i in list:
            if i['date'] >= self.__lastTimestamp:
                fb1 = self.regExpFB.findall(i['msg'])
                if fb1:
                    f1.write(msg_template % (i['author'], i['msg'], datetime.datetime.fromtimestamp(i['date']), fb1[0]))
        f1.close()