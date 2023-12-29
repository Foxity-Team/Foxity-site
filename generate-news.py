import os
import marko
from os import path
from typing import Iterable
from collections.abc import Callable
from shutil import rmtree

def readDirectory(dirPath: os.PathLike) -> Iterable[str]:
    if not path.exists(dirPath): os.mkdir(dirPath)
    return map(lambda v: dirPath + v, os.listdir(dirPath))

def readDirectoryRec(dirPath: os.PathLike) -> Iterable:
    files = map(lambda v: (path.join(dirPath, v), v), os.listdir(dirPath))
    return map(lambda v: (v[0], readDirectoryRec(v[0])) if path.isdir(v[0]) else v, files)

def filterFiles(pred: Callable[[str, str], bool], dir: Iterable) -> Iterable:
    return filter(lambda v: v is not None, 
                  map(lambda v: (v[0], filterFiles(pred, v[1])) if not isinstance(v[1], str) 
                                else (v if pred(v[0], v[1])
                                      else None), dir))

def mapFiles(pred: Callable[[str, str], str], dir: Iterable) -> Iterable:
    return map(lambda v: (v[0], mapFiles(pred, v[1])) if not isinstance(v[1], str) else (v[0], pred(v[0], v[1])), dir)

def mapFilenames(pred: Callable[[str], str], dir: Iterable) -> Iterable:
    return map(lambda v: (pred(v[0]), mapFilenames(pred, v[1])) if not isinstance(v[1], str) else (pred(v[0]), v[1]), dir)

def collectDict(dir: Iterable) -> dict:
    return {k: collectDict(v) if not isinstance(v, str) else v for k, v in dir}

def readFile(filename: str) -> str:
    with open(filename) as f: return f.read()

def readMarkdown(filename: str) -> str:
    return marko.convert(readFile(filename))

def readAll(filename: str) -> str:
    if os.path.splitext(filename)[1] == '.md': return readMarkdown(filename)
    else: return readFile(filename)

def directoryToHtml(dir: str) -> str:
    listing = ''.join(
                 map(lambda v: f'<li>{path.splitext(v)[0]}</li>', 
                 filter(lambda v: v != 'index.html' and not path.isdir(path.join(dir, v)), os.listdir(dir))))
    return f'<ol>{listing}</ol>'

def wrapWithDirectoryListing(template: str, filename: str) -> str:
    return template.replace('{{ body }}', directoryToHtml(path.dirname(filename)))

def wrapWithTemplate(template: str, filename: str) -> str:
    file = readAll(filename)
    return template.replace('{{ body }}', file if file != '' and file.splitlines()[0] != '<!-- DirList -->' 
                                          else file + directoryToHtml(path.dirname(filename)))

def placeFiles(dir: dict) -> None:
    global counter
    for filename, data in dir.items():
        if path.splitext(filename)[1] == '':
            os.mkdir(filename)
            placeFiles(data)
        else:
            counter += 1
            with open(filename, 'w') as f:
                f.write(data)

pagesPath = 'pages'
distPath = 'test-public'
allowedExts = ['.md', '.html']

template = readAll('templates/index.html')

val = collectDict(
      mapFilenames(lambda f   : f if path.splitext(f)[1] == '' else path.splitext(f)[0] + '.html',
      mapFilenames(lambda f   : distPath + f.removeprefix(pagesPath),
      mapFiles(    lambda f, d: wrapWithTemplate(template, f), 
      filterFiles( lambda f, d: path.splitext(f)[1] in allowedExts, readDirectoryRec(pagesPath))))))

counter = 0

if path.exists(distPath): rmtree(distPath)
os.mkdir(distPath)
placeFiles(val)

print(f'Сгенерировано {counter} файлов')