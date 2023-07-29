import tkinter
from tkinter import *
from tkinter import messagebox
import pymysql
import time

class ContactBook:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Contact Book")
        self.window.geometry("700x400")
        self.window.configure(bg="black")
        self.labels()
    def labels(self):
        self.window_label = Label(self.window, text="Contact Book Login", font=("times new roman", 22, "bold"), bg="black", fg="white")
        self.window_label.place(x=180, y=50)
        self.username_label = Label(self.window, text="Username :", font=("times new roman", 18, "bold italic"), bg="black", fg="white")
        self.username_label.place(x=100, y=120)
        self.password_label = Label(self.window, text="Password :", font=("times new roman", 18, "bold italic"), bg="black", fg="white")
        self.password_label.place(x=100, y=170)
        self.username_entry = Entry(self.window, width=30)
        self.username_entry.place(x=300, y=130)
        self.password_entry = Entry(self.window, width=30, show="*")
        self.password_entry.place(x=300, y=180)
        self.login_button = Button(self.window, text="Login", command=self.login, font=("times new roman", 18, "bold italic"), bg="sky blue", fg="black")
        self.login_button.place(x=280, y=220)

    def login(self):
        username = "s"
        password = "a"
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        if username == entered_username and password == entered_password:
            self.login_button.config(state=DISABLED)  # Disable the login button during the sleep period
            loading_label = Label(self.window, text="Loading....", font=("ink free", 18, "bold italic"), bg="black", fg="white")
            loading_label.place(x=280, y=310)
            self.window.update()  # Update the window to display the loading label
            time.sleep(2)  # Pause execution for 2 seconds
            loading_label.destroy()  # Remove the loading label
            self.window.update()  # Update the window to remove the loading label
            messagebox.showinfo("Login Successful", "Welcome to Santhosh Contact Book ")
            self.window.destroy()
            self.details()
        else:
            self.login_button.config(state=DISABLED)  # Disable the login button during the sleep period
            messagebox.showerror("Login Failed", "Incorrect username or password.")
            loading_label = Label(self.window, text="Try again...", font=("ink free", 18, "bold italic"), bg="black",
                                  fg="white")
            loading_label.place(x=280, y=310)
            self.window.update()  # Update the window to display the loading label
            time.sleep(3)  # Pause execution for 2 seconds
            loading_label.destroy()  # Remove the loading label
            self.window.update()  # Update the window to remove the loading label


    def details(self):
        self.window2 = tkinter.Tk()
        self.window2.title("Details")
        self.window2.geometry("900x600")
        self.window2.configure(bg="black")

        self.new_button = Button(self.window2, text="New", command=self.insert_data,
                                 font=("times new roman", 18, "bold italic"), bg="black", fg="light green")
        self.new_button.place(x=60, y=80)
        self.load_button = Button(self.window2, text="Load", command=self.load_contacts,
                                  font=("times new roman", 18, "bold italic"), bg="black", fg="yellow")
        self.load_button.place(x=180, y=80)
        self.edit_button = Button(self.window2, text="Edit", command=self.edit_contact,
                                  font=("times new roman", 18, "bold italic"), bg="black", fg="light blue")
        self.edit_button.place(x=300, y=80)
        self.list_contacts = Listbox(self.window2, height=30, width=40)
        self.list_contacts.place(x=590, y=60)
        self.delete_button = Button(self.window2, text="Delete", command=self.delete_contact,
                                    font=("times new roman", 18, "bold italic"), bg="black", fg="red")
        self.delete_button.place(x=420, y=80)
    def load_contacts(self):
        self.list_contacts.delete(0, END)  # Clear the existing contacts in the list
        db_connection = pymysql.connect(
            host="localhost",
            user="root",
            password="santhosh",
            database="contact_book"
        )
        my_database = db_connection.cursor()
        sql_statement = "SELECT * FROM contacts"
        my_database.execute(sql_statement)
        output = my_database.fetchall()
        for contact_book in output:
            self.list_contacts.insert(END, f"Name : {contact_book[0]} | Phone.no : {contact_book[1]}")

    def create_contact(self):
        name = self.Name_entry.get()
        phone_no = self.Phone_no_entry.get()
        db_connection = pymysql.connect(
            host="localhost",
            user="root",
            password="santhosh",
            database="contact_book"
        )
        my_database = db_connection.cursor()
        sql_statement = "INSERT INTO contacts (name, phone_no) VALUES (%s, %s)"
        values = (name, phone_no)
        my_database.execute(sql_statement, values)
        db_connection.commit()
        messagebox.showinfo("Data Inserted", "New contact added successfully!")
        self.load_contacts()

    def edit_contact(self):
        self.Name_label = Label(self.window2, text="Name :", font=("times new roman", 18, "bold italic"), bg="black",
                                fg="white")
        self.Name_label.place(x=100, y=200)
        self.Phone_no_label = Label(self.window2, text="Phone No :", font=("times new roman", 18, "bold italic"), bg="black",
                                    fg="white")
        self.Phone_no_label.place(x=100, y=250)
        self.Name_entry = Entry(self.window2, width=30)
        self.Name_entry.place(x=250, y=205)
        self.Phone_no_entry = Entry(self.window2, width=30)
        self.Phone_no_entry.place(x=250, y=255)
        self.update_button = Button(self.window2, text="Update", command=self.edit_contact_action,
                                    font=("times new roman", 18, "bold italic"), bg="black", fg="light blue")
        self.update_button.place(x=220, y=360)

        selected_contact = self.list_contacts.curselection()
        if selected_contact:
            contact_info = self.list_contacts.get(selected_contact)
            name = contact_info.split(" | ")[0].split(": ")[1]
            phone_no = contact_info.split(" | ")[1].split(": ")[1]
            self.Name_entry.insert(END, name)
            self.Phone_no_entry.insert(END, phone_no)

    def edit_contact_action(self):
        selected_contact = self.list_contacts.curselection()
        if selected_contact:
            contact_info = self.list_contacts.get(selected_contact)
            name = contact_info.split(" | ")[0].split(": ")[1]
            phone_no = contact_info.split(" | ")[1].split(": ")[1]
            new_name = self.Name_entry.get()
            new_phone_no = self.Phone_no_entry.get()

            db_connection = pymysql.connect(
                host="localhost",
                user="root",
                password="santhosh",
                database="contact_book"
            )
            my_database = db_connection.cursor()
            sql_statement = "UPDATE contacts SET name = %s, phone_no = %s WHERE name = %s AND phone_no = %s"
            values = (new_name, new_phone_no, name, phone_no)
            my_database.execute(sql_statement, values)
            db_connection.commit()
            self.load_contacts()
            messagebox.showinfo("Contact Updated", "Contact updated successfully!")
        else:
            messagebox.showerror("Contact not selected", "Please select a contact")

    def delete_contact(self):
        selected_contact = self.list_contacts.curselection()
        if selected_contact:
            contact_info = self.list_contacts.get(selected_contact)
            name = contact_info.split(" | ")[0].split(": ")[1]
            phone_no = contact_info.split(" | ")[1].split(": ")[1]
            db_connection = pymysql.connect(
                host="localhost",
                user="root",
                password="santhosh",
                database="contact_book"
            )
            my_database = db_connection.cursor()
            sql_statement = "DELETE FROM contacts WHERE name = %s AND phone_no = %s"
            values = (name, phone_no)
            my_database.execute(sql_statement, values)
            db_connection.commit()
            self.load_contacts()
            messagebox.showinfo("Contact Deleted", "Contact deleted successfully!")
        else:
            messagebox.showerror("Contact not selected", "Please select a contact")

    def insert_data(self):
        self.Name_label = Label(self.window2, text="Name :", font=("times new roman", 18, "bold italic"), bg="black",
                                fg="white")
        self.Name_label.place(x=100, y=200)
        self.Phone_no_label = Label(self.window2, text="Phone No :", font=("times new roman", 18, "bold italic"), bg="black",
                                    fg="white")
        self.Phone_no_label.place(x=100, y=250)
        self.Name_entry = Entry(self.window2, width=30)
        self.Name_entry.place(x=250, y=205)
        self.Phone_no_entry = Entry(self.window2, width=30)
        self.Phone_no_entry.place(x=250, y=255)
        self.create_button = Button(self.window2, text="Create", command=self.create_contact,
                                    font=("times new roman", 18, "bold italic"), bg="black", fg="light green")
        self.create_button.place(x=220, y=360)

cont_book = ContactBook()
cont_book.window.mainloop()
