
# Example One
This just loops through each folder,starting with the root folder of the library

```
def Scan(path, files, mediaList, subdirs, lang=None, root=None):

    log('Scan', 'path: %s', path)
    log('Scan', 'files: %s', files)
    log('Scan', 'mediaList: %s', mediaList)
    log('Scan', 'subdirs: %s', subdirs)
    log('Scan', 'lang: %s', lang)
    log('Scan', 'root: %s', root)

    for idx, file in enumerate(files):
        log('Scan:file', 'file: %s', file)
```

```
Scan :: path:
Scan :: files: []
Scan :: mediaList: []
Scan :: subdirs: ['/Users/gregory/GitHub/plex-scanner/test/movies/Some Movie (2003)']
Scan :: lang: /Users/gregory/GitHub/plex-scanner/test/movies
Scan :: root: None
GUI: Scanning Some Movie (2003)
Scan :: path: Some Movie (2003)
Scan :: files: []
Scan :: mediaList: []
Scan :: subdirs: ['/Users/gregory/GitHub/plex-scanner/test/movies/Some Movie (2003)/Subs']
Scan :: lang: /Users/gregory/GitHub/plex-scanner/test/movies
Scan :: root: None
GUI: Scanning Some Movie (2003)/Subs
```

# Example 2
