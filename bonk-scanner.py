import re, os, os.path
import Media, VideoFiles, Stack, Utils

# Series date format regular expression (Show Title - 2012-09-19 - Episode Title)
SERIES_DATE_REGEX_1 = r'^(?P<baseDir>.*)[\\/](?P<dirShow>[^\\]+)[\\/](?P<dirSeason>[^\\]+)[\\/](?P<show>.*)[ ]*[-\.][ ]*(?P<year>[0-9]{4})[-\. ](?P<month>[0-9]{1,2})[-\. ](?P<day>[0-9]{1,2})[ ]*[-\.][ ]*(?P<title>.*)\.(?P<ext>.*)$'
# Series date format regular expression (Show Title - 09-19-2013 - Episode Title)
SERIES_DATE_REGEX_2 = r'^(?P<baseDir>.*)[\\/](?P<dirShow>[^\\]+)[\\/](?P<dirSeason>[^\\]+)[\\/](?P<show>.*)[ ]*[-\.][ ]*(?P<month>[0-9]{1,2})[-\. ](?P<day>[0-9]{1,2})[-\. ](?P<year>[0-9]{4})[ ]*[-\.][ ]*(?P<title>.*)\.(?P<ext>.*)$'
# Series episode format regular expression (Show title - s2012e0919 - Episode Title)
SERIES_EPISODE_REGEX = r'^(?P<baseDir>.*)[\\/](?P<dirShow>[^\\]+)[\\/](?P<dirSeason>[^\\]+)[\\/](?P<show>.*)[ ]*[-\.][ ]*[sS](?P<season>[0-9]*)[eE](?P<episode>[0-9]*)[ ]*[-\.][ ]*(?P<title>.*)\.(?P<ext>.*)$'
# Simple Series episode format
SERIES_SIMPLE_EPISODE_REGEX = r'^(?P<baseDir>.*)[\\/](?P<dirShow>[^\\]+)[\\/](?P<dirSeason>[^\\]+)[\\/](?P<episode>[0-9]*)[ ]*[-\.][ ]*(?P<title>.*)\.(?P<ext>.*)$'
SERIES_SIMPLE_REGEX = r'^(?P<baseDir>.*)[\\/](?P<dirShow>[^\\]+)[\\/](?P<dirSeason>[^\\]+)[\\/](?P<title>.*)\.(?P<ext>.*)$'
# Episode name REGEX
SERIES_EPISODE_TITLE_PART_REGEX = r'(?P<title>.*)[ ]*part|pt[0-9]'

def log(methodName, message, *args):
    '''
        Create a log message given the message and arguments
    '''
    Log(methodName + ' :: ' + message, *args)

# Only use unicode if it's supported, which it is on Windows and OS X,
# but not Linux. This allows things to work with non-ASCII characters
# without having to go through a bunch of work to ensure the Linux
# filesystem is UTF-8 "clean".
#
def unicodize(s):
    filename = s

    log('unicodize', 'before unicodizing: %s', str(filename))
    if os.path.supports_unicode_filenames:
        try: filename = unicode(s.decode('utf-8'))
        except: pass
    log('unicodize', 'after unicodizing: %s', str(filename))
    return filename

class BaseMediaParser(object):
    '''
        Parses the file name and determines the type of tile that was found
    '''
    def setValues(self, match):
        pass

    def getSupportedRegexes(self):
        return []

    def containsMatch(self, mediaFile):
        retVal = False
        # Iterate over the list of regular expressions
        for regex in self.getSupportedRegexes():
            # Find out what file format is being used
            match = re.search(regex, mediaFile)
            if match:
                retVal = True
                break

        return retVal


    def parse(self, mediaFile, lang):
        self.mediaFile = mediaFile
        self.lang = lang

        # Iterate over the list of regular expressions
        for regex in self.getSupportedRegexes():
            # Find out what file format is being used
            match = re.search(regex, mediaFile)
            log('parse', 'matches: %s', match)
            if match:
                log('parse', 'found matches')
                self.setValues(match)
                break

    def stripPart(self, s):
        retVal = s
        # Test whether it contains part
        match = re.search(SERIES_EPISODE_TITLE_PART_REGEX, retVal)
        if match:
            log('stripPart', 'title matched')
            retVal = match.group('title').strip()

        log('stripPart', 'parsed episode title: %s', retVal)
        return retVal

    def getShowTitle(self):
        return self.showTitle

    def getSeasonTitle(self):
        return self.seasonTitle

    def getEpisodeTitle(self):
        return self.episodeTitle

    def getEpisodeNumber(self):
        return self.episodeNumber

    def getEpisodeReleaseDate(self):
        return self.episodeReleaseDate


class SeriesDateBasedMediaParser(BaseMediaParser):

    def getSupportedRegexes(self):
        return [SERIES_DATE_REGEX_1, SERIES_DATE_REGEX_2]

    def setValues(self, match):
        self.showTitle = match.group('dirShow').strip()
        self.seasonTitle = match.group('dirSeason').strip()
        self.episodeYear = match.group('year').strip()
        self.episodeMonth = match.group('month').strip()
        self.episodeDay = match.group('day').strip()
        self.episodeTitle = self.stripPart(match.group('title').strip())
        # Create the date
        self.episodeReleaseDate = datetime.datetime(int(self.episodeYear), int(self.episodeMonth), int(self.episodeDay))
        log('parse', 'episode date: %s', str(self.episodeReleaseDate))

class SeriesEpisodeMediaParser(BaseMediaParser):

    def getSupportedRegexes(self):
        return [SERIES_EPISODE_REGEX]

    def setValues(self, match):
        self.showTitle = match.group('show').strip()
        self.episodeSeason = match.group('season').strip()
        self.episodeNumber = match.group('episode').strip()
        self.episodeTitle = self.stripPart(match.group('title').strip())

class SeriesSimpleMediaParser(BaseMediaParser):

    def getSupportedRegexes(self):
        return [SERIES_SIMPLE_EPISODE_REGEX, SERIES_SIMPLE_REGEX]

    def setValues(self, match):
        self.parsedEpisodeTitle = self.stripPart(match.group('title').strip())

# List of series parsers
SERIES_PARSERS = [SeriesDateBasedMediaParser(), SeriesEpisodeMediaParser(), SeriesSimpleMediaParser()]


# Look for episodes.
def Scan(path, files, mediaList, subdirs, language=None, root=None):

    # Scan for video files.
    VideoFiles.Scan(path, files, mediaList, subdirs, root)

    for idx, file in enumerate(files):
        log('Scan', 'file: %s', file)

        absFilePath = os.path.abspath(unicodize(file))
        log('Scan', 'absolute file path: %s', absFilePath)

        # Iterate over the list of parsers and parse the file path
        for parser in SERIES_PARSERS:
            if parser.containsMatch(absFilePath) is True:
                log('Scan', 'parser %s contains match - parsing file path', parser)
                parser.parse(absFilePath, lang)

                showTitle = parser.getShowTitle()
                Log('Scan', 'show title %s', showTitle)
                seasonTitle = parser.getSeasonTitle()
                Log('Scan', 'season title %s', seasonTitle)
                episodeNumber = parser.getEpisodeNumber()
                Log('Scan', 'episode number %s', episodeNumber)
                episodeTitle = parser.getEpisodeTitle()
                Log('Scan', 'episode title %s', episodeTitle)

                vid = Media.Episode(showTitle, seasonTitle, episodeNumber, episodeTitle, None)
                if parser.getEpisodeReleaseDate() is not None:
                    vid.released_at = parser.getEpisodeReleaseDate()
                vid.parts.append(file)
                mediaList.append(vid)
                print mediaList
