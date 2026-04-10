import json
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import io
import time

path = "C:\\Users\\mik\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Bookmarks"

with open(path, "r+", encoding = "utf-8") as file:
    content = json.load(file)

#print(json.dumps(content['roots']['bookmark_bar']['children'], sort_keys=True, indent=2))
blah = content['roots']['bookmark_bar']['children']

chapter = "chapter"

url = ""

current_time = time.time()

image_url_list = []

#List used to output onto save file
saved_list = [["" for i in range(5)] for j in range(100)]

manhwa_index = -1



class Gui:

    def __init__(self):
       
        self.root = tk.Tk()

        self.root.geometry("1200x1200")
        self.root.title("Bookmark Manager")
        self.root.configure(bg='lightblue') 

        x_value = 0
        y_value = 0

        buttons = [None]*1000
        count = 0

        store_image = [None]*1000

        for i in image_url_list:
            eq = requests.get(i)
            orig = Image.open(io.BytesIO(eq.content))
            orig = orig.resize((200,200),resample=Image.Resampling.LANCZOS)
            store_image[count] = ImageTk.PhotoImage(orig)
            buttons[count] = tk.Button(self.root, text = "Left", font=('Sans', 20) , bg = "orange", borderwidth = 0)
            buttons[count].config(image = store_image[count])
            buttons[count].place(x = x_value, y = y_value)
           
            x_value +=  200
            if(x_value > 1000):
                y_value += 200
                x_value = 0  
            count += 1
        self.root.mainloop()





for i in blah:
    if(i['name'] == "New folder"):
        for child in i['children']:
            if(child.get('name') == "Manhwa"):
                for j in child.get('children'):
                    if (j['url'].startswith("https://asura")) or (j['url'].startswith("https://www.asura")):
                        
                        j['url'] = j['url'].replace("0906168628-", "")
                        j['url'] = j['url'].replace("4102803034-", "")
                        j['url'] = j['url'].replace("www.asurascans.com/", "asurascans.com/comics/")
                        j['url'] = j['url'].replace("-chapter-", "-f6174291/chapter/")
                        j['url'] = j['url'].replace("asura.gg/2226495089-", "asurascans.com/comics/")
                        j['url'] = j['url'].replace("asuracomics.gg", "asurascans.com/comics")
                        j['url'] = j['url'].replace("asuracomic.net", "asurascans.com")
                        j['url'] = j['url'].replace("/series/", "/comics/")
                        
                        manhwa_index += 1
                    
                        ##Sets up name and the url of the CURRENT CHAPTER
                        string1 = j['name']
                        saved_list[manhwa_index][0] = string1.replace("�","")
                        saved_list[manhwa_index][1] = j['url']
                        
                        print(manhwa_index)
                    #I Killed an Academy Player Chapter 66 - Asura Scans
                    #SSS-Class Suicide Hunter Chapter 133 - Asura Scans
                    #Star-Embracing Swordmaster Chapter 77 - Asura Scans
                        print(j['name'])
                        index = j['url'].find("chapter")
                        if index != -1:
                            
                            ##Setting up the url of the manhwa home page so you can access it
                            change = j['url'][0:index-10]
                            print("change", change)
                            change_request = requests.get(change)
                            boop = BeautifulSoup(change_request.text, 'html.parser')
                           
                            ##Gets current chapter by removing everything in the link except
                            current_chapter = j['url'][index+8:].replace("/","")
                            saved_list[manhwa_index][4] = current_chapter

                            ##Looks for latest chapter
                            LatestLoc = boop.find(string = 'Latest Chapter')
                            Link_to_latest = LatestLoc.parent.parent['href']
                            index = Link_to_latest.find("chapter")
                            Latest_chapter = Link_to_latest[index+8:]
                            saved_list[manhwa_index][3] = Latest_chapter

                            ##Looks for the url of the image that displays
                            for bink in boop.find_all("title"):
                                if bink is not None:
                                    meta = bink.parent.find("meta", property="og:image")
                                    if meta is not None:
                    
                                        url = meta["content"]
                                        image_url_list.append(url)
                                        saved_list[manhwa_index][2] = url
                                        break
                    else:
                        print("skip")    
                        
                                        
                                        

                                    
                                    

print("manhwa section\n")
f = open("save.txt", "w")
for manhwa_list in range(manhwa_index):
    for manhwa_list_section in range(5):                       
        print(saved_list[manhwa_list][manhwa_list_section])    
        f.write(saved_list[manhwa_list][manhwa_list_section])    
        f.write("\n")
print(time.time() - current_time)
f.close()
Gui()

                        
                      
                    







