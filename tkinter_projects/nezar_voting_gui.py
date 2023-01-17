"""Nezar AG 12P 01/04/2020 Voting App + Database to store voting results"""
import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict
import sqlite3

voting_db = sqlite3.connect('voting.db')
cursorObj = voting_db.cursor()

class Mainframe(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = MainPage(self)
        self.frame.pack()
        self.candidates = []
        self.id_candidates2 = {}
        self.num_votes = 0
        self.voting = ''

    def change(self, frame):
        self.frame.pack_forget()
        self.frame = frame(self)
        self.frame.pack()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        cursorObj.execute("CREATE TABLE IF NOT EXISTS vote_names (names Text)")
        voting_db.commit()

        data = cursorObj.execute(''' SELECT * FROM vote_names''')
        voting_db.commit()

        self.vn = []

        for record in data:
            self.vn.append(record[0])

        master.title("Main Page")
        master.geometry("300x300")

        About = tk.Button(self, text="About", command=self.about_info, bg="#eb1a22", fg="#0a2a50", font="Lato 18 bold", borderwidth=4, relief="ridge")
        About.pack()

        voting = tk.Label(self, text= "What are you voting for?", bg="#081b67", fg="#bd592a", font="Lato 12 bold",  borderwidth=2, relief="flat")
        voting.pack()

        self.voting_table = tk.Entry(self, text= "Enter the Name of Voting", bg="white", fg="black", font="Lato 12", borderwidth=6, relief="sunken")
        self.voting_table.pack()
        self.master.bind('<Return>', self.on_press_enter)

        close_app = tk.Button(self, text="Close App", command=self.btn_close, bg="#eb1a22", fg="#0a2a50", font="Lato 18 bold", borderwidth=4, relief="ridge")
        close_app.pack()

    def about_info(self):
        messagebox.showinfo("App Info", """This is an application to make votes for a new class captain
The maximum number of candidates is 4 and the class should have at least 2 candidates
The maximum number of voters is 30""")

    def on_press_enter(self, event):
        global table_name
        table_name = self.voting_table.get()

        if table_name not in self.vn and table_name != "":
            cursorObj.execute("Insert INTO vote_names(names) VALUES(?)", (table_name,))
            voting_db.commit()

            self.voting_table.delete(0, tk.END)
            self.master.change(CandidatePage)
        else:
            messagebox.showinfo("White Space Error or Name already existing", "Make sure you give a name for the vote or choose another unique name for the vote.")
            self.voting_table.delete(0, tk.END)

    def btn_close(self):
        self.master.destroy()

class CandidatePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        print(table_name)
        master.title("Candidate Page")
        master.geometry("300x300")

        candidate = tk.Label(self, text= "Enter Candidate Name", bg="#081b67", fg="#bd592a", font="Lato 12 bold",  borderwidth=2, relief="flat")
        candidate.pack()

        self.candidate_entry = tk.Entry(self, text= "Enter Candidate Name", bg="white", fg="black", font="Lato 12", borderwidth=6, relief="sunken")
        self.candidate_entry.pack()
        self.master.bind('<Return>', self.on_press_enter)

    def finalize(self): #key: i+1, value: [name, 0]
        self.master.id_candidates2 = {i+1:[name, 0] for i,name in enumerate(self.master.candidates)} #dictionary comprehension
        self.master.change(VotingPage)

    def on_press_enter(self, event):
        score = 0
        name = self.candidate_entry.get().title().strip()
        if name not in self.master.candidates and name != "": # ensures that there are no duplicate candidate names in the mainframe class
            self.master.candidates.append(name)
            self.candidate_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Candidate Already Nominated or white space error", "If it is a new candidate and by chance they have the same name. Please write the surname of the candidate.")
            self.candidate_entry.delete(0, tk.END)

        if len(self.master.candidates) == 2:
            less_than_4_candidates = tk.Button(self, text="Start Voting", command=self.finalize, bg="#eb1a22", fg="#0a2a50", font="Lato 18 bold", borderwidth=4, relief="ridge")
            less_than_4_candidates.pack()

        if len(self.master.candidates) == 4:
            self.finalize()

class VotingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Voting Page")
        master.geometry("300x400")

        for k,v in self.master.id_candidates2.items(): # creating labels for candidates with their voting number
            candidate = tk.Label(self, text= "Candidate {}: {}".format(k, v[0]), bg="white", fg="#0d5096", font="Lato 16 bold",  borderwidth=20, relief="flat")
            candidate.pack()

        info = tk.Label(self, text= "Only Enter Candidate Number e.g. 2", bg="white", fg="red", font="Lato 10 bold",  borderwidth=10, relief="flat")
        info.pack()

        self.candidate_entry = tk.Entry(self, text= "Enter Candidate Number to make a vote", bg="white", fg="black", font="Lato 12", borderwidth=6, relief="sunken")
        self.candidate_entry.pack()
        self.master.bind('<Return>', self.on_press_enter)

        finish_voting = tk.Button(self, text="Finish Voting", command=self.btn_command, bg="#eb1a22", fg="#0a2a50", font="Lato 18 bold", borderwidth=4, relief="ridge")
        finish_voting.pack()


    def btn_command(self):
        print(self.master.id_candidates2)
        self.master.change(ResultsPage)

    def on_press_enter(self, event):
        if self.master.num_votes < 30:
            #place for catching user input errors
            try: #put every error in this block
                my_bool = int(self.candidate_entry.get()) in range(1,len(self.master.candidates)+1) #if the user inputs letter instead of number, change T/F to int
                try_this = 1/int(my_bool) # if it's 0 it's going to be False
                ce = int(self.candidate_entry.get())
                self.master.id_candidates2[ce][1] += 1
                self.master.num_votes += 1
                messagebox.showinfo("Candidate vote", "Candidate voted for is {}".format(self.master.id_candidates2[ce][0]))
                print(self.master.id_candidates2)
            except: #try throws an error
                messagebox.showinfo("Invalid vote", " Try again and only use candidates' numbers to vote!!!")
            #try doesn't have an error
            self.candidate_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Invalid vote", " Try again and only use candidates' numbers to vote!!!")
            self.master.change(ResultsPage)

class ResultsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        cursorObj.execute("CREATE TABLE IF NOT EXISTS {} (Id INTEGER , Candidate TEXT,  Score INTEGER)".format(table_name))
        voting_db.commit()

        new_list = []
        for k,v in self.master.id_candidates2.items(): # creating a new list to sort the items in descending order
            new_list.append(v)
            cursorObj.execute("Insert INTO {} (Id, Candidate, Score) VALUES(?, ?, ?)".format(table_name), (k, v[0], v[1]))
            voting_db.commit()
        new_list.sort(key = lambda x: x[1], reverse=True) # sorting the items in descending order

        master.title("Results Page")
        master.geometry("300x400")
        for c in new_list:
            candidate_name = tk.Label(self, text= "{}'s total votes: {}".format(c[0], c[1]), bg="white", fg="#40413f", font="Lato 16 bold",  borderwidth=20, relief="flat")
            candidate_name.pack()

        if new_list[0][1] != new_list[1][1]:
            winner = tk.Label(self, text= "NEW CLASS CAPTAIN {}".format(new_list[0][0].upper()), bg="white", fg="#ac1616", font="Lato 18 bold", borderwidth=20, relief="raised")
            winner.pack()
        else:
            draw = tk.Label(self, text= "NO OVERALL WINNER", bg="white", fg="#ac1616", font="Lato 18 bold", borderwidth=20, relief="raised")
            draw.pack()

        Home = tk.Button(self, text="Another Vote", command=self.btn_command, bg="#eb1a22", fg="#0a2a50", font="Lato 18 bold", borderwidth=4, relief="ridge")
        Home.pack()

        close_app = tk.Button(self, text="Close App", command=self.btn_close, bg="#eb1a22", fg="#0a2a50", font="Lato 18 bold", borderwidth=4, relief="ridge")
        close_app.pack()

    def btn_command(self):
        self.master.destroy()
        app = Mainframe()
        app.mainloop()

    def btn_close(self):
        self.master.destroy()

app = Mainframe()
app.mainloop()
print("Program Completed")
cursorObj.close()
voting_db.close()
