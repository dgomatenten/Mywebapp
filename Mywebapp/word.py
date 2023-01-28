import os
from bs4 import BeautifulSoup
import requests
import re


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

class wordcnt:
    def __init__(self,content):
        self.input = content
        
    def wordcount(self): 

        frequency = {}
        document_text = self.input

        text_string = document_text.lower()

        #Let's write our regular expression that will return all the words with a number of characters in the range [3-15]. 
        #Starting from 3 will help in avoiding words whose frequency we may not be interested in counting, like if, of, in, etc., 
        #and words longer than 15 might not be correct words. The regular expression for such a pattern looks like this:
        #\b[a-z]{3,15}\b
        #\b is related to the word boundary. For more information on the word boundary,

        match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)

        blacklisted =[]
        i = 0
        
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
        f= open('./Mywebapp/sightword.csv', 'r')

        lines = f.readlines()

        for line in lines:
            line = line.replace("\n","")
            blacklisted.append(line)
            i=i+1


        for word in match_pattern:
            if word not in blacklisted:
                count = frequency.get(word,0)
                frequency[word] = count + 1

        #most_frequent = dict(sorted(frequency.items(), key=lambda elem: elem[1], reverse=True))
        #most_frequent_count = most_frequent.keys()

        # return dictionay
        return frequency



class EngDict:
    def __init__(self,word):
        self.word = word
        self.audio_link = ""
        self.Dict_definition = ""
        
    def GetEngDict(self): 
        url = "https://dictionary.com/browse/" + self.word
        
        print(url)
        
        req = requests.get(url)

        soup=BeautifulSoup(req.text, 'lxml')
        
        audio = soup.find_all('source',type='audio/mpeg')

        list_audio = []    
        for link in audio:
            list_audio.append(link.get('src'))
            print(link.get('src'))

        word = soup.find_all('span',attrs={'class': re.compile("one-click-content")})

        worddef = []
        for defw in word:
            worddef.append(defw.getText())
            print(defw.getText())
        
        self.audio_link=list_audio[0]
        self.Dict_definition = worddef[0]

        return self

