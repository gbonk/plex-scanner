#
#  This was about the simplest Scanner I could figure out.
#  see the README for more details on how to install and run
#
#
#

def log(methodName, message, *args):
    '''
        Create a log message given the message and arguments
    '''
    logMsg = ''
    # Replace the arguments in the string
    if args:
        logMsg = message % args

    logMsg = methodName + ' :: ' + logMsg
    print logMsg

# Scanner Entry point, where plex will call after finding changes in the library directory
# a PSM list will get you the library Id you want to use
# Then for example `pms --scan --section <<id>>`  will cause Plex to dump out some logging
def Scan(path, files, mediaList, subdirs, lang=None, root=None):

    log('Scan', 'path: %s', path)
    log('Scan', 'files: %s', files)
    log('Scan', 'mediaList: %s', mediaList)
    log('Scan', 'subdirs: %s', subdirs)
    log('Scan', 'lang: %s', lang)
    log('Scan', 'root: %s', root)

    for idx, file in enumerate(files):
        log('Scan:file', 'file: %s', file)
