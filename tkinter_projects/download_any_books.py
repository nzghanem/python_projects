from bs4 import BeautifulSoup
import requests
import os
import tkinter as tk


"""
If you change the range in line 52 and 64 to more than 3. It will download more books but it will take a while.
The available file fomrats are:
1.    EPUB (with images)
2.    EPUB (no images)
3.    Kindle (no images)
4.    Kindle (with images)
5.    Plain Text UTF-8
There is no pdf format in the website. EPUB as far as I know can only work in Mac. But you probably can use the Kindle file format. You can download Kindle for free.
"""
# You can type in the name of the books you want to download. Try type for example in the GUI window 'Money' hit return on the keyboard


class Main:
    def __init__(self):
        self.book_names = []
        self.s1 = []
        self.s2 = []
        self.GUI()

    def GUI(self):
        root = tk.Tk()
        root.title("Books in an instant with one click")
        root.geometry('800x300')
        root.configure(bg='#082255')
        info = tk.Label(root, text="Time to read some books",
                        bg="#081b67", fg="#bd592a", font="Lato 24 bold",  borderwidth=2, relief="flat")
        info.pack()
        search = tk.Label(root, text="What books do you fancy to read today? 😍",
                          bg="#081b67", fg="cyan", font="Lato 18 italic",  borderwidth=2, relief="ridge")
        search.pack()
        self.queryEntry = tk.Entry(root, bg="#081b67", fg="#bd592a",
                                   font="Lato 24 bold",  borderwidth=2, relief="sunken")
        self.queryEntry.pack()
        root.bind('<Return>', self.killGUI)
        root.mainloop()

    def killGUI(self, event):
        self.query = self.queryEntry.get()
        self.queryEntry.delete(0, tk.END)
        path = '/Users/NezarAG/Desktop/{}'.format(self.query)
        os.mkdir(path)
        os.chdir(path)
        self.bookNames()

    def bookNames(self):
        for i in range(1, 3):
            soup = BeautifulSoup(requests.get(
                'https://www.gutenberg.org/ebooks/search/?query={}&start_index={}'.format(self.query, i)).content, 'html.parser')
            items = soup.find_all(class_='cell content')
            book_names = [item.find(class_='title').get_text()
                          for item in items]
            self.book_names.append(book_names)
        self.book_names = sum(self.book_names, [])
        del self.book_names[0:4]
        self.bookURL()

    def bookURL(self):
        for i in range(1, 3):
            soup = BeautifulSoup(requests.get(
                'https://www.gutenberg.org/ebooks/search/?query={}&start_index={}'.format(self.query, i)).content, 'html.parser')
            for a in soup.find_all(class_='link', href=True):
                self.s1.append('https://www.gutenberg.org/' + a['href'])
        del self.s1[0:4]
        self.bookDownloadPage()

    def bookDownloadPage(self):
        for i in range((len(self.s1))):
            soup = BeautifulSoup(requests.get(
                self.s1[i]).content, 'html.parser')
            for a in soup.find_all(class_='link', href=True):
                if a.get_text() == 'Kindle (with images)':
                    self.s2.append('https://www.gutenberg.org/' + a['href'])
        self.downloadBoook()

    def downloadBoook(self):
        for i in range((len(self.s2))):
            r = requests.get(self.s2[i])
            with open("Book: {} {} .mobi".format(i + 1, self.book_names[i]), 'wb') as f:
                f.write(r.content)


main = Main()
