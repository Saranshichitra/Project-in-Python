import tkinter as tk               #importing tkinter library
from pymongo import MongoClient    #Mongo Used to connect to MongoDB database
import pandas as pd                #importing pandas library
import numpy as np                 #importing numpy library
import matplotlib.pyplot as plt    #importing matpotlib library

client = MongoClient("mongodb://localhost:27017/")
db = client["library"]
books = db["books"]

def add_book():                          #function to add book
    name = book_entry.get()              #asking user to enter the book name
    author = author_entry.get()          #asking user to enter the author's name

    if name != "" and author != "":      #checking whether both the blocks are filled or not
        books.insert_one({"name": name, "author": author, "available": True})     #adding the book 
        status_label.config(text="Book Added")   #dispalying message 
        book_entry.delete(0, tk.END)    #deleting the book name after adding
        author_entry.delete(0, tk.END)  #deleting the author name after adding
    else:
        status_label.config(text="Enter all details")   #DispaLying message 

def view_books():                         #function to view all books       
    text.delete("1.0", tk.END)
    for b in books.find():
        if b["available"]:
            status = "Available"
        else:
            status = "Issued"

        line = b["name"] + " - " + b["author"] + " (" + status + ")\n"      #dispalying message as <Book name>-<Author name>"<Status(whether available or not)>"
        text.insert(tk.END, line)          #displaying message in the output box

def issue_book():                         #function to issue book
    name = book_entry.get()               #asking user to enter the book name to issue
    book = books.find_one({"name": name, "available": True})           #to find the book and check whether it is available
    if book:
        books.update_one({"name": name},{"$set": {"available": False}})      
        status_label.config(text="Book Issued") #informing user that book is issued
    else:
         status_label.config(text="Book not available")  #message to be displayed when book is not available
    book_entry.delete(0, tk.END)     #deleting the book name after issueing
    author_entry.delete(0, tk.END)   #deleting the author name after issueing

def return_book():                         #function to return book
    name = book_entry.get()               #asking user to enter the book name to return
    book = books.find_one({"name": name})
    if book and not book["available"]:
        books.update_one({"name": name},{"$set": {"available": True}})       #Assigning availability to the book which was first unavailable
        status_label.config(text="Book Returned")   #displaying message that book is returned successfully
    else:
       status_label.config(text="Invalid Book")  #if the book name is not in the list this will mean that the book was never in the library hence displaying message of invalidity
    book_entry.delete(0, tk.END)     #deleting the book name after returning
    author_entry.delete(0, tk.END)   #deleting the author name after returning

def show_stats():          #function to display stats of all books 
    data = list(books.find())  #storing all books from dataset in the form of list

    if len(data) == 0:  #if their is no book in the list
        status_label.config(text="No data available")   #output statement if condition persists
        return

    df = pd.DataFrame(data)   #converting list in the pandas database for easier manipulations

    total = len(df)  #counting the total no. of books
    available = len(df[df["available"] == True])    #checking the number of available booka
    issued = len(df[df["available"] == False])   #checking the number of unavailable(i.e. issued) books

    arr = np.array([available, issued])   #storing available and issued books in an array using numpy library

    issued_books = df[df["available"] == False]   #getting only issued books

    result = f"Total Books: {total}\nAvailable: {arr[0]}\nIssued: {arr[1]}\n\nIssued Books:\n"  #output format 

    if len(issued_books) == 0:   #condition if no book is issued
        result += "None"  
    else:
        for i, row in issued_books.iterrows():
            result += f"{row['name']} - {row['author']}\n"   #Dispalying all issued books

    text.delete("1.0", tk.END)   #Clearing the old text from screen
    text.insert(tk.END, result)  #Displaying the required output
    
def show_graph():       #function to display graphs
    data = list(books.find())  #storing all books from dataset in the form of list

    if len(data) == 0:  #if their is no book in the list
        status_label.config(text="No data to show")   #output statement if condition persists
        return

    available = 0
    issued = 0

    for b in data:   #going through all books in the list
        if b["available"]:
            available += 1  #if available
        else:
            issued += 1  #if issued

    labels = ["Available", "Issued"]
    values = [available, issued]

    plt.bar(labels, values)   #bar graph plotting
    plt.title("Library Book Status")    #title of the graph
    plt.xlabel("Category")  #x axis label
    plt.ylabel("Number of Books")  #y axis label
    plt.show()  #Displaying the graph

    issued_books = {}   #empty dictionary 

    for b in data:   #going through all books in the dictionary
        if not b["available"]:   # only issued books
            name = b["name"]    #name of the issued book
            if name in issued_books:
                issued_books[name] += 1  
            else:
                issued_books[name] = 1

    if len(issued_books) == 0: #if no book is issued
        status_label.config(text="No issued books to show")  #output statement if condition persists
        return

    names = list(issued_books.keys())  #storing the name of book
    counts = list(issued_books.values())  #storing how many times the book is issued

    plt.figure()   #creating a graph
    plt.bar(names, counts)    #bar graph ploting
    plt.title("Most Issued Books")  #Title of the graph
    plt.xlabel("Book Name")   #x axis label
    plt.ylabel("Times Issued")   # y axis label
    plt.show() #Displaying the graph

# GUI
root = tk.Tk()                     #creating the main window
root.title("Library Management System")         #to display title
root.geometry("450x520")      #deciding the size of display window          
root.configure(bg="#6fb7d8")      #adding background color to the main window


# Heading Display
title = tk.Label(root,text="Library Management System",font=("Arial", 18, "bold"),bg="#e6f2ff",fg="#003366")        #format to display the main heading
title.pack(pady=15)               #locks and displays the changes in the window , pady=10 adds the vertical space

# Input Frame
frame = tk.Frame(root, bg="#e6f2ff")
frame.pack(pady=10)      #creates containers

tk.Label(frame, text="Book Name:", font=("Arial", 12),bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=8)     #displaying book name in the main window and deciding it's spacing
book_entry = tk.Entry(frame, width=28, font=("Arial", 11))              #taking input from user
book_entry.grid(row=0, column=1, padx=10, pady=8)   #deciding the position

tk.Label(frame, text="Author:", font=("Arial", 12),bg="#e6f2ff").grid(row=1, column=0, padx=10, pady=8)     #displaying book name in the main window and deciding it's spacing
author_entry = tk.Entry(frame, width=28, font=("Arial", 11))              #taking input from user
author_entry.grid(row=1, column=1, padx=10, pady=8)   #deciding the position

# Buttons Frame 
btn_frame = tk.Frame(root, bg="#e6f2ff")     #creating a separate frame to display buttons
btn_frame.pack(pady=15)    #locks and displays the changes in the window , pady=10 adds the vertical space

tk.Button(btn_frame, text="Add Book", width=16, command=add_book,bg="#007acc", fg="white").grid(row=0, column=0, padx=8, pady=8)    #displaying button in the main window witn text Add Book and describing it's size 
tk.Button(btn_frame, text="View Books", width=16, command=view_books,bg="#28a745", fg="white").grid(row=0, column=1, padx=8, pady=8)   #displaying button in the main window with text view Book and describing it's size 
tk.Button(btn_frame, text="Issue Book", width=16, command=issue_book,bg="#ffc107", fg="black").grid(row=1, column=0, padx=8, pady=8)  #displaying button in the main window witn\h text issue Book and describing it's size 
tk.Button(btn_frame, text="Return Book", width=16, command=return_book,bg="#6f42c1", fg="white").grid(row=1, column=1, padx=8, pady=8)   #displaying button in the main window with text return Book and describing it's size 
tk.Button(btn_frame, text="Show Stats", width=16, command=show_stats,bg="#17a2b8", fg="white").grid(row=2, column=0, columnspan=2, pady=8)  #displaying button in the main window with text show stats and describing it's size 
tk.Button(btn_frame, text="Show Graph", width=16, command=show_graph,bg="#dc3545", fg="white").grid(row=3, column=0, columnspan=2, pady=8)  #displaying button in the main window with text show graph and describing it's size 

# Output Box
text = tk.Text(root, height=12, width=55,font=("Consolas", 10),bg="white", fg="black", bd=2, relief="solid")                 #creating a large text area(i.e. output box) to view books or to display output
text.pack(pady=10)

# Status
status_label = tk.Label(root, text="", fg="#003366",bg="#e6f2ff",font=("Arial", 11, "bold"))
status_label.pack(pady=5)
root.mainloop()