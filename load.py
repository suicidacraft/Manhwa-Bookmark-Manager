import json
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import io
import time
import re
import webbrowser

global saved_list 
saved_list = [["" for i in range(5)] for j in range(100)]

manhwa_index = 0

image_url_list = []

current_time = time.time()

#Taking the stuff from the save file
f = open("save.txt", "r")

list_counter = 0


class ScrollableFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
    
        #Create & Display Canvas/Scrollbar
        self.canvas = Canvas(self,bg="lightblue")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview, bg="lightblue")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.scrolling_frame = Frame(self.canvas, bg = "lightblue")
        
        #Connects Canvas and Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        #Add Scrolling Frame to Canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrolling_frame, anchor="nw")
        
        self.scrolling_frame.bind("<Configure>", self.update_scrollregion)
        
        self.canvas.bind("<Configure>", self.resize_frame)
        
        shit1 = self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        shit2 = self.canvas.bind_all("<Down>", self._on_down)
        shit3 = self.canvas.bind_all("<Up>", self._on_up)
        self.canvas.bind("<Enter>", lambda e: (shit1,shit2,shit3))
      
    def _on_down(self, event):
        
        self.canvas.yview_scroll(int(1), "units")
            
    def _on_up(self, event):
        
        self.canvas.yview_scroll(int(-1), "units")
        
    def _on_mousewheel(self, event):
        
        self.canvas.yview_scroll(int(-event.delta/120), "units")

    def update_scrollregion(self, event=None):
        
        #Update Scrollregion when Scrolling Frame size changes
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def resize_frame(self, event=None):
        #Makes Scrolling Frame match Canvas width
        canvas_width = event.width
        
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


class Gui:

    def __init__(self):
    
       
        self.root = tk.Tk()

        self.root.geometry("1600x1600")
        self.root.title("Bookmark Manager")
        self.root.config()
        x_value = 0
        y_value = 0
        
        scr_fr = ScrollableFrame(self.root)
        scr_fr.config()
        scr_fr.pack(fill=BOTH, expand=1)
    
        
        buttons = [None]*1000
        count = 0

        store_image = [None]*1000
        


        for i in image_url_list:
            i = str(i)
            eq = requests.get(i.strip())
            orig = Image.open(io.BytesIO(eq.content))
            orig = orig.resize((200,300),resample=Image.Resampling.LANCZOS)
            store_image[count] = ImageTk.PhotoImage(orig)
            string1 = saved_list[count][0]
            buttons[count] = tk.Button(scr_fr.scrolling_frame, borderwidth = 0,bg = "lightblue",command=lambda count = count: webbrowser.open_new_tab(saved_list[count][1].strip()))
            buttons[count].config(image = store_image[count])
            buttons[count].grid(column=x_value, row = y_value, padx = 20, pady = 10)
            x_value += 1
            
            string2 = saved_list[count][4].strip()
            string3 = saved_list[count][3].strip()
            int2 = float(string2)
            int3 = float(string3)
            string4 = str(int3-int2)
            label = tk.Label(scr_fr.scrolling_frame, text = str(count)+". "+string1+"\n"+string2+"\n"+string3+"\n"+
                  "Available Chapters: "+string4, font=('Sans', 20), bg = "lightblue", wraplength= 400)        
            label.grid(column = x_value, row = y_value)


            x_value += 1
            if(x_value > 2):
                y_value += 1
                x_value = 0  
            count += 1
            print(time.time() - current_time)
            print(saved_list[count][1])
      
        self.root.mainloop()


def sort(papamericano):
    index_sort = 0
    while index_sort < len(image_url_list)-1:
        chap = string_float(papamericano,index_sort)
        index_sort += 1
        chap2 = string_float(papamericano,index_sort)
        if chap < chap2:
            swap(papamericano,index_sort-1,index_sort)
            index_sort = 0
        
        
def string_float(papamericano,index_sort):
    n1 = papamericano[index_sort][4].strip()
    n2 = papamericano[index_sort][3].strip()
    int2 = float(n1)
    int3 = float(n2)
    string4 = (int3-int2)
    return string4

def swap(list,id1,id2):
    copy = [1,2,3,4,5]
    for i in range(5):   
        copy[i] = list[id1][i]
        list[id1][i] = list[id2][i]
        list[id2][i] = copy[i]
    copy[0] = image_url_list[id1]
    image_url_list[id1] = image_url_list[id2]
    image_url_list[id2] = copy[0]



for line in f:
    saved_list[manhwa_index][list_counter] = line
    list_counter += 1
    if(list_counter > 4):
        image_url_list.append(saved_list[manhwa_index][2])
        manhwa_index += 1
        list_counter = 0
    

sort(saved_list)   

Gui()
