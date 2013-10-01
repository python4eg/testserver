import os
import sys

import re


def ignore_folder(folder, ignoreFolders):
    for ignoreFold in ignoreFolders:
        if folder.startswith(os.path.join(ignoreFold, '')) or folder == ignoreFold:
            return True
    return False

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print "Usage: "+ sys.argv[0]+" <Path to project folder> <Project name> [<Ignore folders>]"
        sys.exit(1)

    mainPath = sys.argv[1]
    projectName = sys.argv[2]
    ignoreFolders = []
    if len(sys.argv) == 4:
        ignoreFolders = sys.argv[3].split(',')

    if not os.path.exists(mainPath):
        print 'Path %s not exists' % mainPath
        return False

    typesPattern = re.compile('.*\.(cpp|h|ui|xml|qrc|ts|txt)$')
    dirsList = ''
    filesList = ''
    for root, dirs, files in os.walk(mainPath):
        temp = ''
        relPath = os.path.relpath(root, mainPath)
        if not ignore_folder(relPath, ignoreFolders):
            for name in files:
                if typesPattern.search(name):
                    temp += os.path.join(relPath, name) + '\n'
            if temp != '':
                dirsList += relPath + '\n'
                filesList += temp

    try:
        filesInclude = open(mainPath+projectName+'.files', 'w')
        dirsInclude = open(mainPath+projectName+'.includes', 'w')
        filesInclude.write(filesList)
        dirsInclude.write(dirsList)
    finally:
        filesInclude.close()
        dirsInclude.close()


if __name__ == '__main__' :
    main()
