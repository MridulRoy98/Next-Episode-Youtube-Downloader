import glob
import string
import urllib.request
import re
import bs4
import requests
from pytube import YouTube

myString = ""
myinput = input("Enter your favorite youtube show: ")
myString = myinput.replace(" ", "+")
# print(myString)

# Reading the episode number and incrementing it
with open('LatestEpisode\\EpisodeNumber.txt', 'r+') as file:
    line = file.readline()
    episodeNumber = int(line)+1
    stringEpisodeNumber = str(episodeNumber)
    print("Episode Number: ", episodeNumber )

#getting video codes
html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + myString + stringEpisodeNumber)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

#getting list of files in download folder
downloadDirectory = 'LatestEpisode\\*'
filelist = glob.glob(downloadDirectory)
# print(filelist)

#base URL
basicUrl = "https://www.youtube.com/watch?v="
number = 0
while number <= 3:

    #Setting up the full URL
    videoUrl = basicUrl + str(video_ids[number])
    htmlPage = requests.get(videoUrl)
    htmlPage.raise_for_status()

    # converting to BeautifulSoup and finding title
    soup = bs4.BeautifulSoup(htmlPage.text, 'html.parser')
    shortSoup = soup.find('title')
    # print(shortSoup.contents)

    # Checking if file already exists and donwloading
    if shortSoup.contents[0].find(stringEpisodeNumber):
        print(shortSoup.contents[0])
        for file in filelist:
            # print(file)
            if not stringEpisodeNumber in file:
                print(videoUrl)
                downloadURL = YouTube(videoUrl)
                downloadURL = downloadURL.streams.get_highest_resolution()
                downloadURL.download('LatestEpisode')
                break

    #To check if the file is downloaded and if it exists in the downloadDirectory
        fileCheck = glob.glob(downloadDirectory + '*')
        for file in fileCheck:
            if stringEpisodeNumber in file:

                #incrementing the episode number
                with open('LatestEpisode\\EpisodeNumber.txt', 'w+') as writingFile:
                    writingFile.write(stringEpisodeNumber)
                    writingFile.close()

            else:
                print("Latest Episode Downloaded")
                break
        break
    number = number + 1


