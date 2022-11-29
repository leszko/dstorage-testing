import sys
import requests
import os

def suffix(url):
    return url.rsplit("/", 1)[1]

def prefix(url):
    return url.split("/", 1)[0]

def download(url, outputDirectory):
    print("Downloading " + url)
    response = requests.get(url)
    open(outputDirectory + "/" + suffix(url), "wb").write(response.content)

def createResDirectory(res, outputDirectory):
    path = outputDirectory + "/" + res
    if not os.path.exists(path):
        os.mkdir(path)
    return path

if len(sys.argv) < 3:
    print("Not enough arguments")
    print("Usage: download.py <playback-url> <output-directory>")
    exit(1)

playbackUrl = sys.argv[1]
outputDirectory = sys.argv[2]

response = requests.get(playbackUrl)

download(playbackUrl, outputDirectory)
for line in iter(response.text.splitlines()):
    if "index.m3u8" in line:
        resDirectory = createResDirectory(prefix(line), outputDirectory)
        basePlaybackUrl = playbackUrl.replace("index.m3u8", "")
        resPlaybackUrl = basePlaybackUrl + line
        download(resPlaybackUrl, resDirectory)
        resResponse = requests.get(resPlaybackUrl)
        for resLine in iter(resResponse.text.splitlines()):
            if resLine.endswith(".ts"):
                download(basePlaybackUrl + prefix(line) + "/" + resLine, resDirectory)
