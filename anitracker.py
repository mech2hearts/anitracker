from tkinter import *
import tkinter.messagebox
import urllib.request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
from requests.exceptions import HTTPError

testfile = urllib.request.URLopener()

root = Tk()

user_url = "https://nyaa.si/user/"
anime_url = "?f=0&c=0_0&q=starlight+revue+1080p&s=id&o=asc"


def seriesPlus(): #dummy command/function
    print("TEST")

def fileRetrieval(url): #dummy file retrieval, might not need anymore
    testfile=urllib.request.URLopener()
    testfile.retrieve(url,"testiscle")

def dlAnime(title, subber, resolution):
    user_url = "https://nyaa.si/user/"+subber  # enter subber name here
    anime_url = "?f=0&c=0_0&q=+"+title.replace(" ","+")  # add title like 'starlight+revue' 1080p added just in case. Remove later
    rest_url = "&s=id&o=asc" #ascending order e.g 1-13
    total_url = user_url +  anime_url
    if resolution == 1:
        total_url += "+480p"
    elif resolution == 2:
        total_url += "+720p"
    elif resolution == 3:
        total_url += "+1080p"
    total_url += '+'+rest_url
    print(total_url) #check url to see if valid


    try:
        uClient = uReq(total_url) #url is opened through program
    except: #specify the error for HTTP 404. Maybe use urllib3 instead
        tkinter.messagebox.showinfo("Alert", "No episodes found. Please alter your search or check at a later time")
        return
    page_html = uClient.read() #html of the page from URL is saved in this variable
    uClient.close() #close the connection to web to save process


    page_soup = soup(page_html, "html.parser") #html is parsed
    containers = page_soup.findAll("tr", {"class": "success"}) #find the all row sections called "success". Each row holds episode title, DL, and etc.

    for container in containers:
        norp = ''
        dlLink = ''
        episode_row = container.find_all("td", {"colspan": "2"}) #variable finds all the episode title sections from each row of episodes
        for episode in episode_row: #takes episode section from an episode row
            if episode.find(class_="comments"): #if there is a comment link in the section
                for title in episode.find_all('a'): #finds all links in the episode section
                    if episode.find(class_="comments"):
                        norp = title["title"] #might be wrong. comment link is taken first but replaced by the episode title link.
                        #WASTE FIX THIS ^
            else:
                norp = episode.a["title"]
            print(norp[0:-4]) #cuts out the .mkv part so it doesn't mess up the file download type

        linker = container.find_all("td", {"class": "text-center"}) #looks for the section holding the torrent DL link
        for link in linker:
            for dl in link.find_all('a'): #all links in the DL section of an episode
                urlChain = dl["href"] #unneeded Maybe. Unnecessarily takes in excess links
                if urlChain[0:2] == "/d": #links starting with /download
                    dlLink = "https://nyaa.si" + urlChain
                    print(dlLink)
        testfile.retrieve(dlLink, norp[0:-4] + ".torrent") #downloads files from link and adds .torrent to file name


def searchAnime(title, subber, resolution):
    user_url = "https://nyaa.si/user/" + subber  # enter subber name here
    anime_url = "?f=0&c=0_0&q=+" + title.replace(" ","+")  # add title like 'starlight+revue' 1080p added just in case. Remove later
    rest_url = "&s=id&o=asc"  # ascending order e.g 1-13
    total_url = user_url + anime_url
    if resolution == 1:
        total_url += "+480p"
    elif resolution == 2:
        total_url += "+720p"
    elif resolution == 3:
        total_url += "+1080p"
    total_url += '+' + rest_url
    print(total_url)  # check url to see if valid

    try:
        uClient = uReq(total_url)  # url is opened through program
    except:  # specify the error for HTTP 404. Maybe use urllib3 instead
        tkinter.messagebox.showinfo("Alert", "No episodes found. Please alter your search or check at a later time")
        return
    page_html = uClient.read()  # html of the page from URL is saved in this variable
    uClient.close()  # close the connection to web to save process


    searchWindow = Toplevel(height=50, width=100)
    results = Listbox(searchWindow, selectmode=MULTIPLE, height=15, width=50)
    searchScroll = Scrollbar(searchWindow, orient=VERTICAL)
    results['yscrollcommand']=searchScroll.set
    searchScroll['command']=results.yview

    page_soup = soup(page_html, "html.parser")  # html is parsed
    containers = page_soup.findAll("tr", {
        "class": "success"})  # find the all row sections called "success". Each row holds episode title, DL, and etc.

    for container in containers:
        norp = ''
        dlLink = ''
        episode_row = container.find_all("td", {
            "colspan": "2"})  # variable finds all the episode title sections from each row of episodes
        for episode in episode_row:  # takes episode section from an episode row
            if episode.find(class_="comments"):  # if there is a comment link in the section
                for title in episode.find_all('a'):  # finds all links in the episode section
                    if episode.find(class_="comments"):
                        norp = title[
                            "title"]  # might be wrong. comment link is taken first but replaced by the episode title link.
                        # WASTE FIX THIS ^
            else:
                norp = episode.a["title"]
            results.insert(END, norp[0:-4])  # cuts out the .mkv part so it doesn't mess up the file download type


    searchScroll.pack(side=RIGHT, fill=Y)

    results.pack()


root.title("AniTracker")

plusImg = PhotoImage(file="addplus.png")

label_1 = Label(root, text='Anime Title')
label_2 = Label(root, text='Subbing Group')

entry_1 = Entry(root)
entry_2 = Entry(root) #input fields

label_1.pack()
entry_1.pack() #anime title
label_2.pack()
entry_2.pack() #subber name



resolutionVar = IntVar()
Radiobutton(root, text="480p", value=1, variable=resolutionVar).pack()
Radiobutton(root, text="720p", value=2, variable=resolutionVar).pack()
Radiobutton(root, text="1080p",value=3, variable=resolutionVar).pack()



toolbar = Frame(root)
addAnime = Button(toolbar, text="Add Series", command=lambda: dlAnime(entry_1.get(),entry_2.get(),resolutionVar.get()), image=plusImg, compound=LEFT)
addAnime.pack(side=LEFT, anchor=E, padx=3)
listAnime = Button(toolbar, text="DL List", command=lambda: searchAnime(entry_1.get(),entry_2.get(),resolutionVar.get()))
listAnime.pack(side=LEFT, padx=3)
folderAnime = Button(toolbar, text="Folder", command=seriesPlus)
folderAnime.pack(side=LEFT, padx=3)


toolbar.pack(side=TOP, fill=X, padx=5, pady=5)
sizer = Frame(root, width=500, height=350)
currency = Label(sizer, text="Currently Watching Anime")
currency.pack()

sizer.pack() #fixed size of window


root.mainloop()