from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

splash_Screen = Tk()
splash_Width = 700
splash_Height = 350

screen_Width = splash_Screen.winfo_screenwidth()
screen_Height = splash_Screen.winfo_screenheight()

x = (screen_Width/2)-(splash_Width/2)
y = (screen_Height/2)-(splash_Height/2)

splash_Screen.geometry('%dx%d+%d+%d' % (splash_Width, splash_Height, x, y))
splash_Screen.resizable(False, False)
splash_Screen.overrideredirect(True)
splash_Screen.configure(background='#212121')

label = Label(splash_Screen, text="APHAMAX LIBRARY\nMANAGAMENT SYSTEM", font=('times', 35, 'bold'), background='#212121', foreground='white')
label.place(y=90, x=80)

label = Label(splash_Screen, text="Please Wait. Loading...", font=('times', 18, 'bold'), background='#212121', foreground='white')
label.place(y=300, x=240)

# Progress bar

def progressMove():
    current_width = move_Progress_Frame['width']
    move_Progress_Frame.config(width=current_width+10)

    move_Progress_Frame.after(200, progressMove)


progress_Frame = Frame(splash_Screen, width=450, height=15, background='black')
progress_Frame.pack_propagate(False)
progress_Frame.place(y=330, x=125)

move_Progress_Frame = Frame(splash_Screen, width=10, height=15, background='green')
move_Progress_Frame.pack_propagate(False)
move_Progress_Frame.place(y=330, x=125)

move_Progress_Frame.after(200, progressMove)

BG = '#36454F'
FONT = ('times', 15)
LFG = "white"
EBG = "light grey"

# user database connection
user_conn = sqlite3.connect('user_database.db')
user_curs = user_conn.cursor()

# book registation database connection
book_reg_conn = sqlite3.connect('book_reg_database.db')
book_reg_curs = book_reg_conn.cursor()

# Create User DB
def create_user_db():
    # Creating Student Registration Database

    # Table for User Logins
    user_curs.execute("""CREATE TABLE IF NOT EXISTS user_logins (
                                user_id text,
                                username text,
                                user_password text
                )""")

    # Table for user next of kin
    user_curs.execute("""CREATE TABLE IF NOT EXISTS next_Kin (
                                user_id text,
                                kin_relationship text,
                                kin_full_name text,
                                kin_gender text,
                                kin_email text,
                                kin_id_type text,
                                kin_id_no text,
                                kin_contact_no text,
                                kin_location text
                            )""")

    # Table for user registration
    user_curs.execute("""CREATE TABLE IF NOT EXISTS user_registration (
                                user_id text,
                                user_first_name text,
                                user_last_name text,
                                user_gender text,
                                user_email text,
                                user_id_type text,
                                user_id_no text,
                                user_contact text,
                                user_location text,
                                user_join_date text
                            )""")

    # Table for member cancellation
    user_curs.execute("""CREATE TABLE IF NOT EXISTS membership_cancel (
                                user_id text,
                                username text,
                                reason text
                            )""")

    # Table for admins
    user_curs.execute("""CREATE TABLE IF NOT EXISTS admin_lists (
                                user_id text,
                                username text,
                                password text
                            )""")

# Create Book registration database
def create_book_reg_db():
    # Book registration DB
    book_reg_curs.execute("""CREATE TABLE IF NOT EXISTS book_registration (
        book_id text,
        book_name text,
        book_author text,
        publication_year text,
        publishers text,
        academic_year text,
        book_course text,
        book_condition text,
        date_added text,
        registered_by text
    )""")

    # Users issued books
    book_reg_curs.execute("""CREATE TABLE IF NOT EXISTS user_book_detail (
        book_id text,
        user_id text,
        first_name text,
        last_name text,
        user_gender text,
        user_email text,
        user_contact text,
        prev_due text, 
        user_eligibility
    )""")

    # Issued books details
    book_reg_curs.execute("""CREATE TABLE IF NOT EXISTS issue_book_detail (
        user_id text,
        book_id text,
        book_name text,
        book_author text,
        publication_year text,
        book_condition text,
        book_course text,
        issue_date text,
        return_date text,
        book_fine text,
        issued_by text
    )""")

    # Issue tree db
    book_reg_curs.execute("""CREATE TABLE IF NOT EXISTS issue_book_tree (
        user_id text,
        first_name text,
        user_contact text,
        book_id text,
        book_name text,
        book_condition text,
        book_course text,
        issue_date text,
        return_date text,
        book_fine text, 
        issued_by text,
        user_eligibility text
    )""")

    # Report a book
    book_reg_curs.execute("""CREATE TABLE IF NOT EXISTS report_a_book (
        book_id text,
        book_name text,
        user_id text,
        user_name text,
        reasons text
    )""")

    # Request book db
    book_reg_curs.execute("""CREATE TABLE IF NOT EXISTS request_book (
        book_name text,
        book_author text,
        publication_year text,
        book_publishers text,
        book_course text,
        academic_year text
    )""")

# Call Function to create databases
create_user_db()
create_book_reg_db()


class Admin:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1360x690+2+5')
        self.root.resizable(False, False)
        self.root.configure(background=BG)
        self.root.title("ADMIN SECTION")

        def home_section():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.pack_propagate(False)
            general_lbl_frame.pack(pady=3)

            top_frame = LabelFrame(general_lbl_frame, width=1105, height=100, background=BG)
            top_frame.grid_propagate(False)
            top_frame.grid(row=0, column=0, pady=3)

            def requested_books():
                previous_borrowed_lbl_frame = LabelFrame(bottom_frame, width=1095, height=463, background=BG,
                                                         foreground='white', text=":: Requested Books Section :: ",
                                                         font=('times', 18, 'bold'), labelanchor=N)
                previous_borrowed_lbl_frame.grid_propagate(False)
                previous_borrowed_lbl_frame.grid(row=0, column=0, pady=(20, 100), padx=2)

                upper_frame = Frame(previous_borrowed_lbl_frame, width=1095, height=500, background='steel blue')
                upper_frame.grid_propagate(False)
                upper_frame.grid(row=0, column=0)

                def clearTree():
                    for record in treeview.get_children():
                        treeview.delete(record)

                def showAllRecord():
                    clearTree()
                    book_reg_curs.execute(
                        "SELECT book_name, book_author, publication_year, book_publishers, book_course, academic_year FROM request_book")
                    names = book_reg_curs.fetchall()

                    for name in names:
                        treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                             name[4], name[5]))

                tree_frame = Frame(upper_frame, width=1080, height=500)
                tree_frame.place(y=0, x=0)

                treeview = ttk.Treeview(tree_frame)
                showAllRecord()
                # treeview.bind("<ButtonRelease-1>", fillRecord)
                treeview.place(y=0, x=0, height=420, width=1078)

                treeview['columns'] = (
                    'book_name', 'book_author', 'publishers', 'publication_year', 'book_course', 'academic_year')

                treeview.column('#0', width=0, stretch=NO)
                treeview.column('book_name', anchor=N, width=120, minwidth=150)
                treeview.column('book_author', anchor=N, width=120, minwidth=150)
                treeview.column('publishers', anchor=N, width=200, minwidth=230)
                treeview.column('publication_year', anchor=N, width=180, minwidth=200)
                treeview.column('book_course', anchor=N, width=150, minwidth=200)
                treeview.column('academic_year', anchor=N, width=100, minwidth=130)

                treeview.heading('#0', text="", anchor=CENTER)
                treeview.heading('book_name', text="Book Name", anchor=CENTER)
                treeview.heading('book_author', text="Book Author", anchor=CENTER)
                treeview.heading('publishers', text="Publishers", anchor=CENTER)
                treeview.heading('publication_year', text="Publication Year", anchor=CENTER)
                treeview.heading('book_course', text="Book Course", anchor=CENTER)
                treeview.heading('academic_year', text="Academic Year", anchor=CENTER)

                x_scrollbar = ttk.Scrollbar(upper_frame, orient='horizontal', command=treeview.xview)
                x_scrollbar.place(y=420, x=0, width=1095)

                y_scrollbar = ttk.Scrollbar(upper_frame, command=treeview.yview)
                y_scrollbar.place(y=0, x=1078, height=421)

                treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            def reported_books():
                previous_borrowed_lbl_frame = LabelFrame(bottom_frame, width=1095, height=463, background=BG,
                                                         foreground='white', text=":: Reported Books :: ",
                                                         font=('times', 18, 'bold'), labelanchor=N)
                previous_borrowed_lbl_frame.grid_propagate(False)
                previous_borrowed_lbl_frame.grid(row=0, column=0, pady=(20, 100), padx=2)

                upperFrame = Frame(previous_borrowed_lbl_frame, width=1000, height=300, background='steel blue')
                upperFrame.grid_propagate(False)
                upperFrame.grid(row=0, column=0, padx=40)

                def clearTree():
                    for record in treeview.get_children():
                        treeview.delete(record)

                def showAllRecord():
                    clearTree()
                    book_reg_curs.execute(
                        "SELECT user_id, user_name, book_id, book_name, reasons FROM report_a_book")
                    names = book_reg_curs.fetchall()

                    for name in names:
                        treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                             name[4]))

                treeFrame = Frame(upperFrame, width=985, height=285)
                treeFrame.place(y=0, x=0)

                treeview = ttk.Treeview(treeFrame)
                showAllRecord()
                treeview.place(y=0, x=0, height=285, width=985)

                treeview['columns'] = ('user_id', 'user_name', 'book_id', 'book_name', 'reasons')

                treeview.column('#0', width=0, stretch=NO)
                treeview.column('user_id', anchor=N, width=120, minwidth=150)
                treeview.column('user_name', anchor=N, width=230, minwidth=250)
                treeview.column('book_id', anchor=N, width=80, minwidth=150)
                treeview.column('book_name', anchor=N, width=230, minwidth=250)
                treeview.column('reasons', anchor=N, width=300, minwidth=350)

                treeview.heading('#0', text="", anchor=CENTER)
                treeview.heading('user_id', text="User Id", anchor=CENTER)
                treeview.heading('user_name', text="User Name", anchor=CENTER)
                treeview.heading('book_id', text="Book ID", anchor=CENTER)
                treeview.heading('book_name', text="Book Name", anchor=CENTER)
                treeview.heading('reasons', text="Reason For Reporting", anchor=CENTER)

                x_scrollbar = ttk.Scrollbar(upperFrame, orient='horizontal', command=treeview.xview)
                x_scrollbar.place(y=285, x=0, width=1000)

                y_scrollbar = ttk.Scrollbar(upperFrame, command=treeview.yview)
                y_scrollbar.place(y=0, x=985, height=286)

                treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            def register_admin():
                frame = LabelFrame(bottom_frame, width=1000, height=450, background=BG)
                frame.grid_propagate(False)
                frame.grid(row=0, column=0, pady=3)

                user_id_lbl = Label(frame, text='User ID', font=FONT, background=BG)
                user_id_lbl.grid(row=0, column=0, pady=(30, 0))

                user_id_ent = Entry(frame, width=23, background=EBG, font=FONT, foreground='black')
                user_id_ent.grid(row=1, column=0, padx=15, pady=(0, 15))

                username_lbl = Label(frame, text='Username', font=FONT, background=BG)
                username_lbl.grid(row=2, column=0)

                admin_username_ent = Entry(frame, width=23, background=EBG, font=FONT, foreground='black')
                admin_username_ent.grid(row=3, column=0, padx=15, pady=(0, 15))

                admin_password_lbl = Label(frame, text='Password', font=FONT, background=BG)
                admin_password_lbl.grid(row=4, column=0)

                admin_password_ent = Entry(frame, width=23, background=EBG, font=FONT, foreground='black')
                admin_password_ent.grid(row=5, column=0, padx=15, pady=(0, 15))

                def show_one(e):
                    for selected_item in tree.selection():
                        item = tree.item(selected_item)
                        record = item['values']

                        user_id_ent.delete(0, END)
                        admin_username_ent.delete(0, END)
                        admin_password_ent.delete(0, END)

                        user_id_ent.insert(0, record[0])
                        admin_username_ent.insert(0, record[1])
                        admin_password_ent.insert(0, record[2])

                def show_all():
                    user_curs.execute("SELECT * FROM admin_lists")
                    names = user_curs.fetchall()

                    for name in names:
                        tree.insert(parent="", index=0, text="", values=(name[0], name[1], name[2]))
                admin_lbl_frame = LabelFrame(frame, text="LIST OF ADMINS", font=("Courier", 15, 'bold'), labelanchor=N)
                admin_lbl_frame.grid(row=0, column=1, rowspan=5, pady=(35, 0))

                tree = ttk.Treeview(admin_lbl_frame)
                tree.bind("<ButtonRelease-1>", show_one)
                tree.grid(row=0, column=0, pady=20, padx=20)
                tree['columns'] = ('user_id', 'admin_name', 'admin_pass')
                tree.column('#0', width=0, stretch=NO)
                tree.column('user_id', anchor=W, width=90)
                tree.column('admin_name', anchor=W, width=90)
                tree.column('admin_pass', anchor=W, width=90)

                tree.heading('#0', text="", anchor=CENTER)
                tree.heading('user_id', text='User ID', anchor=CENTER)
                tree.heading('admin_name', text='Admin Name', anchor=CENTER)
                tree.heading('admin_pass', text='Admin Pass', anchor=CENTER)
                show_all()

                def add_admin():
                    if user_id_ent.get() == "":
                        messagebox.showerror("ERROR", 'Fill in the details to add user!')
                    else:
                        user_curs.execute("SELECT user_id FROM user_registration")
                        regNo = user_curs.fetchall()
                        names = []
                        for name in regNo:
                            names.append(name[0])

                        if user_id_ent.get() in names:
                            msg = messagebox.askyesno("WARNING", "Are you sure you want to add admin?")
                            if msg > 0:
                                user_curs.execute("""INSERT INTO admin_lists VALUES (
                                                    :user_id, :username, :password)""",
                                                  {
                                                      'user_id': user_id_ent.get(),
                                                      'username': admin_username_ent.get(),
                                                      'password': admin_password_ent.get()
                                                  }
                                                  )
                                user_conn.commit()
                                messagebox.showinfo("SUCCESS", "User successfully made admin!!")
                        else:
                            messagebox.showerror("ERROR", f"User with ID {user_id_ent.get()} does not exists!!")

                def revoke_admin():
                    msg = messagebox.askyesno("WARNING", "Are you sure you want to revoke admin access?")
                    if msg > 0:
                        user_curs.execute("""DELETE FROM admin_lists WHERE user_id =""" + user_id_ent.get())
                        user_conn.commit()
                        messagebox.showerror("SUCCESS", "Admin access successfully revoked!")



                add_admin_button = Button(frame, text='ADD\nADMIN', font=('times', 15, 'bold'),
                                            activebackground='#7393B3', background='#40B5AD', width=15, relief=FLAT,
                                            command=add_admin)
                add_admin_button.grid(row=7, column=0, pady=(10, 10), padx=40)

                revoke_admin_button = Button(frame, text='REVOKE\nADMIN', font=('times', 15, 'bold'),
                                                  activebackground='#7393B3', background='#40B5AD', width=15,
                                                  relief=FLAT, command=revoke_admin)
                revoke_admin_button.grid(row=7, column=1, pady=(10, 10), padx=40)

            def delete_frame():
                for frame in bottom_frame.winfo_children():
                    frame.destroy()

            def show_frame(page):
                delete_frame()
                page()

            modify_user_button = Button(top_frame, text='REGISTER\nADMIN', font=('times', 18, 'bold'),
                                           activebackground='#7393B3', background='#40B5AD', width=15, relief=FLAT,
                                           command=lambda: show_frame(register_admin))
            modify_user_button.grid(row=0, column=0, pady=(10, 10), padx=40)

            cancel_membership_button = Button(top_frame, text='REQUESTED\nBOOKS', font=('times', 18, 'bold'),
                                              activebackground='#7393B3', background='#40B5AD', width=15,
                                              relief=FLAT, command=lambda: show_frame(requested_books))
            cancel_membership_button.grid(row=0, column=1, pady=(10, 10), padx=40)

            cancel_membership_button = Button(top_frame, text='REPORTED\nBOOKS', font=('times', 18, 'bold'),
                                              activebackground='#7393B3', background='#40B5AD', width=15,
                                              relief=FLAT, command=lambda: show_frame(reported_books))
            cancel_membership_button.grid(row=0, column=2, pady=(10, 10), padx=40)

            bottom_frame = LabelFrame(general_lbl_frame, width=1105, height=500, background=BG)
            bottom_frame.grid_propagate(False)
            bottom_frame.grid(row=1, column=0, pady=3)

        def register_users():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.grid_propagate(False)
            general_lbl_frame.pack(pady=3)

            def searchUser():
                top = Tk()
                top.title("::Search User ::")
                top.geometry('1000x380+180+130')
                top.resizable(False, False)

                # top.overrideredirect(True)

                def clearTree():
                    for record in treeview.get_children():
                        treeview.delete(record)

                def fillRecord():
                    for selected_item in treeview.selection():
                        item = treeview.item(selected_item)
                        studentRegNo = item['values']

                        iClear()

                        # fill user details section
                        user_curs.execute("SELECT * FROM user_registration WHERE user_id = " + str(studentRegNo[0]))
                        studentList = user_curs.fetchall()

                        stuDetails = []
                        for item in studentList:
                            stuDetails.append(item)
                        for record in stuDetails:
                            user_id_ent.insert(0, record[0])
                            user_first_name_ent.insert(END, record[1])
                            user_last_name_ent.insert(END, record[2])
                            user_gender_ent.delete(0, END)
                            user_gender_ent.insert(END, record[3])
                            user_email_ent.insert(END, record[4])
                            user_id_type_ent.delete(0, END)
                            user_id_type_ent.insert(END, record[5])
                            id_number_ent.insert(END, record[6])
                            user_contact_no_ent.insert(END, record[7])
                            user_location_ent.insert(END, record[8])
                            user_join_date_ent.insert(END, record[9])

                        # Fill next of kin section
                        user_curs.execute("SELECT * FROM next_Kin WHERE user_id = " + str(studentRegNo[0]))
                        next_kinList = user_curs.fetchall()

                        guardDetails = []
                        for item1 in next_kinList:
                            guardDetails.append(item1)

                        for next_kin in guardDetails:
                            kin_relationship_ent.delete(0, END)
                            kin_relationship_ent.insert(END, next_kin[1])
                            kin_full_name_ent.insert(END, next_kin[2])
                            kin_gender_ent.delete(0, END)
                            kin_gender_ent.insert(END, next_kin[3])
                            kin_email_ent.insert(END, next_kin[4])
                            kin_id_type_ent.delete(0, END)
                            kin_id_type_ent.insert(END, next_kin[5])
                            kin_id_no_ent.insert(END, next_kin[6])
                            kin_contact_no_ent.insert(END, next_kin[7])
                            kin_location_ent.insert(END, next_kin[8])

                        # Fill user login details
                        user_curs.execute("SELECT * FROM user_logins WHERE user_id = " + str(studentRegNo[0]))
                        userLogins = user_curs.fetchall()

                        userDetails = []
                        for item1 in userLogins:
                            userDetails.append(item1)

                        for user_item in userDetails:
                            username_ent.insert(END, user_item[1])
                            userpass_ent.insert(END, user_item[2])
                    top.destroy()

                def showAllRecord():
                    clearTree()
                    user_curs.execute(
                        "SELECT user_id, user_first_name, user_last_name, user_gender, user_id_no, user_contact, user_join_date, user_location FROM user_registration")
                    names = user_curs.fetchall()

                    for name in names:
                        treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                             name[4], name[5], name[6], name[7]))

                def searchRecord():
                    clearTree()
                    if searchByCombo.get() == 'User ID':
                        user_curs.execute("SELECT user_id FROM user_registration")
                        regestration = user_curs.fetchall()
                        studentid = []
                        for name in regestration:
                            studentid.append(name[0])

                        if search_ent.get() not in studentid:
                            messagebox.showerror("ERROR", "Record Not Found!!")

                        else:
                            name = search_ent.get()
                            user_curs.execute(
                                "SELECT user_id, user_first_name, user_last_name, user_gender, user_id_no, user_contact, user_join_date, user_location FROM user_registration WHERE user_id LIKE '%" + name + "%'")
                            names = user_curs.fetchall()
                            for name in names:
                                treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                                     name[4], name[5], name[6],
                                                                                     name[7]))
                    else:
                        messagebox.showerror("ERROR", "Select From The Combobox!!")

                upperFrame = Frame(top, width=1000, height=300, background='steel blue')
                upperFrame.grid_propagate(False)
                upperFrame.grid(row=0, column=0)

                treeFrame = Frame(upperFrame, width=985, height=285)
                treeFrame.place(y=0, x=0)

                lowerFrame = Frame(top, width=1000, height=80, background='steel blue')
                lowerFrame.grid_propagate(False)
                lowerFrame.grid(row=1, column=0)

                treeview = ttk.Treeview(treeFrame)
                treeview.place(y=0, x=0, height=285, width=985)

                treeview['columns'] = (
                'user_id', 'user_first_name', 'user_last_name', 'user_gender', 'user_id_no', 'user_contact',
                'user_join_date', 'user_location')
                treeview.column('#0', width=0, stretch=NO)
                treeview.column('user_id', anchor=N, width=120, minwidth=150)
                treeview.column('user_first_name', anchor=N, width=180, minwidth=200)
                treeview.column('user_last_name', anchor=N, width=80, minwidth=150)
                treeview.column('user_gender', anchor=N, width=130, minwidth=150)
                treeview.column('user_id_no', anchor=N, width=200, minwidth=250)
                treeview.column('user_contact', anchor=N, width=50, minwidth=150)
                treeview.column('user_join_date', anchor=N, width=50, minwidth=150)
                treeview.column('user_location', anchor=N, width=100, minwidth=150)

                treeview.heading('#0', text="", anchor=CENTER)
                treeview.heading('user_id', text="User Id", anchor=CENTER)
                treeview.heading('user_first_name', text="First Name", anchor=CENTER)
                treeview.heading('user_last_name', text="Last Name", anchor=CENTER)
                treeview.heading('user_gender', text="Gender", anchor=CENTER)
                treeview.heading('user_id_no', text="ID Number", anchor=CENTER)
                treeview.heading('user_contact', text="Contact No", anchor=CENTER)
                treeview.heading('user_join_date', text="Joining Date", anchor=CENTER)
                treeview.heading('user_location', text="Location", anchor=CENTER)

                x_scrollbar = ttk.Scrollbar(upperFrame, orient='horizontal', command=treeview.xview)
                x_scrollbar.place(y=285, x=0, width=1000)

                y_scrollbar = ttk.Scrollbar(upperFrame, command=treeview.yview)
                y_scrollbar.place(y=0, x=985, height=286)

                treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

                fillRecordBtn = Button(lowerFrame, text="Insert Record", font=16, width=13, relief=FLAT,
                                       activebackground='light green', command=fillRecord)
                fillRecordBtn.grid(row=0, column=0, pady=15, padx=(20, 10))

                showAllBtn = Button(lowerFrame, text="Display All", font=16, width=13, relief=FLAT,
                                    activebackground='light green', command=showAllRecord)
                showAllBtn.grid(row=0, column=1, pady=15, padx=(10, 10))

                searchByCombo = ttk.Combobox(lowerFrame, width=10, font=16, background='light grey')
                searchByCombo['values'] = ("Search By", 'User ID')
                searchByCombo.current(1)
                searchByCombo.grid(row=0, column=2, pady=15, padx=(10, 10))

                search_ent = Entry(lowerFrame, width=12, font=15, background='light grey', foreground='black')
                search_ent.grid(row=0, column=3, pady=15, padx=(10, 10))

                searchRecordBtn = Button(lowerFrame, text="Search Record", font=16, width=13, relief=FLAT,
                                         activebackground='light green', command=searchRecord)
                searchRecordBtn.grid(row=0, column=4, pady=15, padx=(10, 10))

                def top_kill():
                    top.destroy()

                searchRecordBtn = Button(lowerFrame, text="Close", font=14, width=10, relief=FLAT,
                                         activebackground='maroon', command=top_kill)
                searchRecordBtn.grid(row=0, column=5, pady=15, padx=(10, 10))

                showAllRecord()
                top.mainloop()

            search_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=70, background=BG)
            search_lbl_frame.grid_propagate(False)
            search_lbl_frame.grid(row=0, column=0, pady=(4, 2))

            search_user_button = Button(search_lbl_frame, text='SEARCH USER', font=('times', 18, 'bold'),
                                        relief=FLAT, activebackground='#6082B6', background='light green', width=16,
                                        command=searchUser)
            search_user_button.place(y=15, x=850)

            #####################################################################################################################

            # User Registration Label Frame
            register_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=450, background=BG, fg='white',
                                            text=":: User Registration :: ", font=('times', 20, 'bold'), labelanchor=N)
            register_lbl_frame.grid_propagate(False)
            register_lbl_frame.grid(row=1, column=0, pady=(2, 4))

            user_registration_lbl_frame = LabelFrame(register_lbl_frame, width=540, labelanchor=N, background=BG,
                                                     foreground='white', text=":: User Registration Section :: ",
                                                     height=400,
                                                     font=('times', 15, 'bold'))
            user_registration_lbl_frame.grid_propagate(False)
            user_registration_lbl_frame.grid(row=0, column=0, pady=(2, 4), padx=2, rowspan=2)

            user_id_lbl = Label(user_registration_lbl_frame, text='User ID', font=FONT, background=BG)
            user_id_lbl.grid(row=0, column=0, pady=(30, 0))

            user_id_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            user_id_ent.grid(row=1, column=0, padx=15, pady=(0, 15))

            user_first_name_lbl = Label(user_registration_lbl_frame, text='First Name', font=FONT, background=BG)
            user_first_name_lbl.grid(row=2, column=0)

            user_first_name_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT,
                                        foreground='black')
            user_first_name_ent.grid(row=3, column=0, padx=15, pady=(0, 15))

            user_last_name_lbl = Label(user_registration_lbl_frame, text='Last Name', font=FONT, background=BG)
            user_last_name_lbl.grid(row=4, column=0)

            user_last_name_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT,
                                       foreground='black')
            user_last_name_ent.grid(row=5, column=0, padx=15, pady=(0, 15))

            user_gender_lbl = Label(user_registration_lbl_frame, text='Gender', font=FONT, background=BG)
            user_gender_lbl.grid(row=6, column=0)

            user_gender_ent = ttk.Combobox(user_registration_lbl_frame, width=21, font=FONT, foreground='black',
                                           background='light grey')
            user_gender_ent['values'] = ('Select Gender', 'Male', 'Female', 'Others')
            user_gender_ent.current(0)
            user_gender_ent.grid(row=7, column=0, padx=15, pady=(0, 15))

            user_email_lbl = Label(user_registration_lbl_frame, text='Email Address', font=FONT, background=BG)
            user_email_lbl.grid(row=8, column=0)

            user_email_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            user_email_ent.grid(row=9, column=0, padx=15, pady=(0, 15))

            user_id_type_lbl = Label(user_registration_lbl_frame, text='ID Type', font=FONT, background=BG)
            user_id_type_lbl.grid(row=0, column=1, pady=(30, 0))

            user_id_type_ent = ttk.Combobox(user_registration_lbl_frame, width=21, font=FONT, foreground='black',
                                            background='light grey')
            user_id_type_ent['values'] = (
            'Select ID type', 'National ID', 'Passport', 'Military ID', 'Alien ID', 'Others')
            user_id_type_ent.current(0)
            user_id_type_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

            id_number_lbl = Label(user_registration_lbl_frame, text='ID Number', font=FONT, background=BG)
            id_number_lbl.grid(row=2, column=1)

            id_number_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            id_number_ent.grid(row=3, column=1, padx=15, pady=(0, 15))

            user_contact_no_lbl = Label(user_registration_lbl_frame, text='Contact', font=FONT, background=BG)
            user_contact_no_lbl.grid(row=4, column=1)

            user_contact_no_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT,
                                        foreground='black')
            user_contact_no_ent.grid(row=5, column=1, padx=15, pady=(0, 15))

            user_location_lbl = Label(user_registration_lbl_frame, text='Location', font=FONT, background=BG)
            user_location_lbl.grid(row=6, column=1)

            user_location_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT,
                                      foreground='black')
            user_location_ent.grid(row=7, column=1, padx=15, pady=(0, 15))

            user_join_date_lbl = Label(user_registration_lbl_frame, text='Joining Date', font=FONT, background=BG)
            user_join_date_lbl.grid(row=8, column=1)

            user_join_date_ent = Entry(user_registration_lbl_frame, width=23, background=EBG, font=FONT,
                                       foreground='black')
            user_join_date_ent.grid(row=9, column=1, padx=15, pady=(0, 15))

            # User Logins
            user_logins_lbl_frame = LabelFrame(register_lbl_frame, width=540, height=80, background=BG, fg='white',
                                               text=":: Login Details :: ", font=('times', 14, 'bold'), labelanchor=N)
            user_logins_lbl_frame.grid_propagate(False)
            user_logins_lbl_frame.grid(row=0, column=1, pady=(2, 4), padx=2)

            username_lbl = Label(user_logins_lbl_frame, text='Username', font=14, background=BG)
            username_lbl.grid(row=0, column=0)

            username_ent = Entry(user_logins_lbl_frame, width=23, background=EBG, font=14, foreground='black')
            username_ent.grid(row=1, column=0, padx=15, pady=(0, 15))

            userpass_lbl = Label(user_logins_lbl_frame, text='Password', font=14, background=BG)
            userpass_lbl.grid(row=0, column=1)

            userpass_ent = Entry(user_logins_lbl_frame, width=23, background=EBG, font=14, foreground='black')
            userpass_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

            # Next of Kin Regisrtation

            next_kin_lbl_frame = LabelFrame(register_lbl_frame, width=540, height=318, background=BG, fg='white',
                                            text=":: Next of Kin Section :: ", font=('times', 15, 'bold'),
                                            labelanchor=N)
            next_kin_lbl_frame.grid_propagate(False)
            next_kin_lbl_frame.grid(row=1, column=1, pady=(2, 4), padx=2)

            kin_relationship_lbl = Label(next_kin_lbl_frame, text='Relationship Type', font=FONT, background=BG)
            kin_relationship_lbl.grid(row=0, column=0, pady=(30, 0))

            kin_relationship_ent = ttk.Combobox(next_kin_lbl_frame, width=21, font=FONT, foreground='black',
                                                background='light grey')
            kin_relationship_ent['values'] = (
            'Select Relationship Type', 'Guardian', 'Father', 'Mother', 'Sibling', 'Others')
            kin_relationship_ent.current(0)
            kin_relationship_ent.grid(row=1, column=0, padx=15, pady=(0, 15))

            kin_full_name_lbl = Label(next_kin_lbl_frame, text='Full Name', font=FONT, background=BG)
            kin_full_name_lbl.grid(row=2, column=0)

            kin_full_name_ent = Entry(next_kin_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            kin_full_name_ent.grid(row=3, column=0, padx=15, pady=(0, 15))

            kin_gender_lbl = Label(next_kin_lbl_frame, text="Gender", font=FONT, background=BG)
            kin_gender_lbl.grid(row=4, column=0)

            kin_gender_ent = ttk.Combobox(next_kin_lbl_frame, width=21, font=FONT, foreground='black',
                                          background='light grey')
            kin_gender_ent['values'] = ('Select Gender', 'Male', 'Female', 'Others')
            kin_gender_ent.current(0)
            kin_gender_ent.grid(row=5, column=0, padx=15, pady=(0, 15))

            kin_email_lbl = Label(next_kin_lbl_frame, text='Email Address', font=FONT, background=BG)
            kin_email_lbl.grid(row=6, column=0)

            kin_email_ent = Entry(next_kin_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            kin_email_ent.grid(row=7, column=0, padx=15, pady=(0, 15))

            kin_id_type = Label(next_kin_lbl_frame, text='ID Type', font=FONT, background=BG)
            kin_id_type.grid(row=0, column=1, pady=(30, 0))

            kin_id_type_ent = ttk.Combobox(next_kin_lbl_frame, width=21, font=FONT, foreground='black',
                                           background='light grey')
            kin_id_type_ent['values'] = ('Select ID Type', 'National ID', 'Military ID', 'Alien ID', 'Passport')
            kin_id_type_ent.current(0)
            kin_id_type_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

            kin_id_no_lbl = Label(next_kin_lbl_frame, text='ID Number', font=FONT, background=BG)
            kin_id_no_lbl.grid(row=2, column=1)

            kin_id_no_ent = Entry(next_kin_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            kin_id_no_ent.grid(row=3, column=1, padx=15, pady=(0, 15))

            kin_contact_no_lbl = Label(next_kin_lbl_frame, text='Contact No', font=FONT, background=BG)
            kin_contact_no_lbl.grid(row=4, column=1)

            kin_contact_no_ent = Entry(next_kin_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            kin_contact_no_ent.grid(row=5, column=1, padx=15, pady=(0, 15))

            kin_location_lbl = Label(next_kin_lbl_frame, text='Location', font=FONT, background=BG)
            kin_location_lbl.grid(row=6, column=1)

            kin_location_ent = Entry(next_kin_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            kin_location_ent.grid(row=7, column=1, padx=15, pady=(0, 15))

            def clearFields():
                msg = messagebox.askyesno("Clear Fields!!", "Are you sure you want to clear all fields")
                if msg > 0:
                    iClear()

            def iClear():
                user_id_ent.delete(0, END)
                user_first_name_ent.delete(0, END)
                user_last_name_ent.delete(0, END)
                user_gender_ent.current(0)
                user_email_ent.delete(0, END)
                user_id_type_ent.current(0)
                id_number_ent.delete(0, END)
                user_contact_no_ent.delete(0, END)
                user_location_ent.delete(0, END)
                user_join_date_ent.delete(0, END)
                username_ent.delete(0, END)
                userpass_ent.delete(0, END)

                kin_relationship_ent.current(0)
                kin_full_name_ent.delete(0, END)
                kin_gender_ent.current(0)
                kin_email_ent.delete(0, END)
                kin_id_type_ent.current(0)
                kin_id_no_ent.delete(0, END)
                kin_contact_no_ent.delete(0, END)
                kin_location_ent.delete(0, END)

            def add_new_user():
                # Insert into database next of kin details
                if user_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Fill in the details to add user!')
                else:
                    user_curs.execute("SELECT user_id FROM user_registration")
                    regNo = user_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if user_id_ent.get() in names:
                        messagebox.showerror("ERROR", f"User with ID {user_id_ent.get()} already exists!!")
                    else:
                        # Insert record to userlogins
                        user_curs.execute("""INSERT INTO user_logins VALUES(
                                        :user_id, :username, :user_password )""",
                                          {
                                              'user_id': user_id_ent.get(),
                                              'username': username_ent.get(),
                                              'user_password': userpass_ent.get()
                                          }
                                          )
                        # Insert record to next of kin
                        user_curs.execute("""INSERT INTO next_Kin VALUES (
                                            :user_id, :kin_relationship, :kin_full_name, :kin_gender, :kin_email, :kin_id_type, :kin_id_no, :kin_contact_no, :kin_location)""",
                                          {
                                              'user_id': user_id_ent.get(),
                                              'kin_relationship': kin_relationship_ent.get(),
                                              'kin_full_name': kin_full_name_ent.get(),
                                              'kin_gender': kin_gender_ent.get(),
                                              'kin_email': kin_email_ent.get(),
                                              'kin_id_type': kin_id_type_ent.get(),
                                              'kin_id_no': kin_id_no_ent.get(),
                                              'kin_contact_no': kin_contact_no_ent.get(),
                                              'kin_location': kin_location_ent.get()
                                          }
                                          )
                        # Insert record into student registration
                        user_curs.execute("""INSERT INTO user_registration VALUES (
                                            :user_id, :user_first_name, :user_last_name, :user_gender, :user_email, :user_id_type, :user_id_no, :user_contact, :user_location, :user_join_date)""",
                                          {
                                              'user_id': user_id_ent.get(),
                                              'user_first_name': user_first_name_ent.get(),
                                              'user_last_name': user_last_name_ent.get(),
                                              'user_gender': user_gender_ent.get(),
                                              'user_email': user_email_ent.get(),
                                              'user_id_type': user_id_type_ent.get(),
                                              'user_id_no': id_number_ent.get(),
                                              'user_contact': user_contact_no_ent.get(),
                                              'user_location': user_location_ent.get(),
                                              'user_join_date': user_join_date_ent.get()
                                          }
                                          )
                        messagebox.showinfo("SUCCESS", f"Record for {user_id_ent.get()} Successfully Added!")
                        user_conn.commit()
                        iClear()

            def update_user():
                if user_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Cannot update an empty record!')
                else:
                    user_curs.execute("SELECT user_id FROM user_registration")
                    regNo = user_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if user_id_ent.get() in names:
                        msg = messagebox.askyesno("WARNING", f"Confirm you want to update user {user_id_ent.get()}?")
                        if msg > 0:
                            # Update user registration details
                            user_curs.execute(
                                "UPDATE user_registration SET user_id=?, user_first_name=?, user_last_name=?, user_gender=?, user_email=?, user_id_type=?, user_id_no=?, user_contact=?, user_location=?, user_join_date=? WHERE user_id=?",
                                (
                                    user_id_ent.get(),
                                    user_first_name_ent.get(),
                                    user_last_name_ent.get(),
                                    user_gender_ent.get(),
                                    user_email_ent.get(),
                                    user_id_type_ent.get(),
                                    id_number_ent.get(),
                                    user_contact_no_ent.get(),
                                    user_location_ent.get(),
                                    user_join_date_ent.get(),
                                    user_id_ent.get()
                                )
                                )

                            # Update user next of kin
                            user_curs.execute(
                                "UPDATE next_Kin SET user_id=?, kin_relationship=?, kin_full_name=?, kin_gender=?, kin_email=?, kin_id_type=?, kin_id_no=?, kin_contact_no=?, kin_location=? WHERE user_id =?",
                                (
                                    user_id_ent.get(),
                                    kin_relationship_ent.get(),
                                    kin_full_name_ent.get(),
                                    kin_gender_ent.get(),
                                    kin_email_ent.get(),
                                    kin_id_type_ent.get(),
                                    kin_id_no_ent.get(),
                                    kin_contact_no_ent.get(),
                                    kin_location_ent.get(),
                                    user_id_ent.get()
                                )
                                )

                            # Update user logins
                            user_curs.execute(
                                "UPDATE user_logins SET user_id=?, username=?, user_password=? WHERE user_id =?",
                                (
                                    user_id_ent.get(),
                                    username_ent.get(),
                                    userpass_ent.get(),
                                    user_id_ent.get()
                                )
                                )
                            user_conn.commit()
                            messagebox.showinfo("SUCCESS", f'User {user_id_ent.get()} successfully updated!')
                            iClear()
                    else:
                        messagebox.showerror("ERROR", 'Cannot update a record that does not exist!')

            def delete_user():
                if user_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Cannot delete an empty record!')
                else:
                    user_curs.execute("SELECT user_id FROM user_registration")
                    regNo = user_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if user_id_ent.get() in names:
                        msg = messagebox.askyesno("WARNING",
                                                  f"Are you sure you want to delete record for user {user_id_ent.get()}?")
                        if msg > 0:
                            user_curs.execute("""DELETE FROM user_registration WHERE user_id=""" + user_id_ent.get())
                            user_curs.execute("""DELETE FROM next_Kin WHERE user_id=""" + user_id_ent.get())
                            user_curs.execute("""DELETE FROM user_logins WHERE user_id=""" + user_id_ent.get())
                            user_conn.commit()
                            messagebox.showinfo("SUCCESS", f'Record successfully deleted for user {user_id_ent.get()}.')
                            iClear()
                    else:
                        messagebox.showerror("ERROR", 'Cannot delete a record that does not exist')

            # Button Label Frame
            button_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=130, background=BG)
            button_lbl_frame.grid_propagate(False)
            button_lbl_frame.grid(row=2, column=0, pady=(2, 4))

            add_user_button = Button(button_lbl_frame, text='ADD USER', font=('times', 18, 'bold'),
                                     activebackground='#7393B3', background='#40B5AD', width=15, height=2, relief=FLAT,
                                     command=add_new_user)
            add_user_button.grid(row=0, column=0, padx=(50, 25), pady=35)

            update_user_button = Button(button_lbl_frame, text='UPDATE USER', font=('times', 18, 'bold'),
                                        activebackground='#4F7942', background='#00A36C', width=15, height=2,
                                        relief=FLAT, command=update_user)
            update_user_button.grid(row=0, column=1, padx=(25, 25), pady=35)

            delete_user_button = Button(button_lbl_frame, text='DELETE USER', font=('times', 18, 'bold'), relief=FLAT,
                                        activebackground='red', background='#9A2A2A', foreground='black', width=15,
                                        height=2, command=delete_user)
            delete_user_button.grid(row=0, column=2, padx=(25, 25), pady=35)

            clear_field_button = Button(button_lbl_frame, text='CLEAR FIELDS', font=('times', 18, 'bold'),
                                        activebackground='#6082B6', background='#899499', width=15, height=2,
                                        relief=FLAT, command=clearFields)
            clear_field_button.grid(row=0, column=3, padx=(25, 50), pady=35)

        def register_books():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.grid_propagate(False)
            general_lbl_frame.pack(pady=3)

            search_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=70, background=BG)
            search_lbl_frame.grid_propagate(False)
            search_lbl_frame.grid(row=0, column=0, pady=(4, 2))

            def searchBooks():

                top = Tk()
                top.title("::Search Book ::")
                top.geometry('1000x380+180+130')
                top.resizable(False, False)
                # top.overrideredirect(True)
                top.update_idletasks()

                def clearTree():
                    for record in treeview.get_children():
                        treeview.delete(record)

                def fillRecord():
                    for selected_item in treeview.selection():
                        item = treeview.item(selected_item)
                        studentRegNo = item['values']

                        iClear()

                        # fill book details section
                        book_reg_curs.execute("SELECT * FROM book_registration WHERE book_id=" + str(studentRegNo[0]))
                        studentList = book_reg_curs.fetchall()

                        stuDetails = []
                        for item in studentList:
                            stuDetails.append(item)

                        for record in stuDetails:
                            book_id_ent.insert(0, record[0])
                            book_name_ent.insert(END, record[1])
                            book_author_ent.insert(END, record[2])
                            publication_year_ent.insert(END, record[3])
                            publishers_ent.insert(END, record[4])
                            academic_year_ent.delete(0, END)
                            academic_year_ent.insert(END, record[5])
                            book_course_ent.insert(END, record[6])
                            book_condition_ent.delete(0, END)
                            book_condition_ent.insert(END, record[7])
                            date_added_ent.insert(END, record[8])
                            registered_by_ent.insert(END, record[9])

                    top.destroy()

                def showAllRecord():
                    clearTree()
                    book_reg_curs.execute(
                        "SELECT book_id, book_name, book_author, book_condition, book_course, academic_year, registered_by, date_added FROM book_registration")
                    names = book_reg_curs.fetchall()

                    for name in names:
                        treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                             name[4], name[5], name[6], name[7]))

                def searchRecord():
                    clearTree()
                    if searchByCombo.get() == 'Book ID':
                        if search_ent.get() == "":
                            messagebox.showerror("ERROR", "Enter Book Id to search!")
                        else:
                            book_reg_curs.execute("SELECT book_id FROM book_registration")
                            regestration = book_reg_curs.fetchall()
                            studentid = []
                            for name in regestration:
                                studentid.append(name[0])

                            if search_ent.get() not in studentid:
                                messagebox.showerror("ERROR", "Record Not Found!!")

                            else:
                                name = search_ent.get()
                                book_reg_curs.execute(
                                    "SELECT book_id, book_name, book_author, book_condition, book_course, academic_year, registered_by, date_added FROM book_registration WHERE book_id LIKE '%" + name + "%'")
                                names = book_reg_curs.fetchall()

                                for name in names:
                                    treeview.insert(parent="", index=0, text="",
                                                    values=(name[0], name[1], name[2], name[3],
                                                            name[4], name[5], name[6], name[7]))
                    else:
                        messagebox.showerror("ERROR", "Select From The Combobox!!")

                upperFrame = Frame(top, width=1000, height=300, background='steel blue')
                upperFrame.grid_propagate(False)
                upperFrame.grid(row=0, column=0)

                treeFrame = Frame(upperFrame, width=985, height=285)
                treeFrame.place(y=0, x=0)

                lowerFrame = Frame(top, width=1000, height=80, background='steel blue')
                lowerFrame.grid_propagate(False)
                lowerFrame.grid(row=1, column=0)

                treeview = ttk.Treeview(treeFrame)
                treeview.place(y=0, x=0, height=285, width=985)

                treeview['columns'] = (
                'book_id', 'book_name', 'book_author', 'book_condition', 'book_course', 'academic_year',
                'registered_by', 'date_added')
                treeview.column('#0', width=0, stretch=NO)
                treeview.column('book_id', anchor=N, width=100, minwidth=120)
                treeview.column('book_name', anchor=N, width=180, minwidth=150)
                treeview.column('book_author', anchor=N, width=80, minwidth=120)
                treeview.column('book_condition', anchor=N, width=120, minwidth=130)
                treeview.column('book_course', anchor=N, width=200, minwidth=250)
                treeview.column('academic_year', anchor=N, width=50, minwidth=100)
                treeview.column('registered_by', anchor=N, width=100, minwidth=150)
                treeview.column('date_added', anchor=N, width=80, minwidth=100)

                treeview.heading('#0', text="", anchor=CENTER)
                treeview.heading('book_id', text="Book ID", anchor=CENTER)
                treeview.heading('book_name', text="Book Name", anchor=CENTER)
                treeview.heading('book_author', text="Book Author", anchor=CENTER)
                treeview.heading('book_condition', text="Book Condition", anchor=CENTER)
                treeview.heading('book_course', text="Book Course", anchor=CENTER)
                treeview.heading('academic_year', text="Academic Year", anchor=CENTER)
                treeview.heading('registered_by', text="Registered By", anchor=CENTER)
                treeview.heading('date_added', text="Date Added", anchor=CENTER)

                x_scrollbar = ttk.Scrollbar(upperFrame, orient='horizontal', command=treeview.xview)
                x_scrollbar.place(y=285, x=0, width=1000)

                y_scrollbar = ttk.Scrollbar(upperFrame, command=treeview.yview)
                y_scrollbar.place(y=0, x=985, height=286)

                treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

                fillRecordBtn = Button(lowerFrame, text="Insert Record", font=16, width=13, relief=FLAT,
                                       activebackground='light green', command=fillRecord)
                fillRecordBtn.grid(row=0, column=0, pady=15, padx=(20, 10))

                showAllBtn = Button(lowerFrame, text="Display All", font=16, width=13, relief=FLAT,
                                    activebackground='light green', command=showAllRecord)
                showAllBtn.grid(row=0, column=1, pady=15, padx=(10, 10))

                searchByCombo = ttk.Combobox(lowerFrame, width=10, font=16, background='light grey')
                searchByCombo['values'] = ("Search By", 'Book ID')
                searchByCombo.current(1)
                searchByCombo.grid(row=0, column=2, pady=15, padx=(10, 10))

                search_ent = Entry(lowerFrame, width=12, font=15, background='light grey', foreground='black')
                search_ent.grid(row=0, column=3, pady=15, padx=(10, 10))

                searchRecordBtn = Button(lowerFrame, text="Search Record", font=16, width=13, relief=FLAT,
                                         activebackground='light green', command=searchRecord)
                searchRecordBtn.grid(row=0, column=4, pady=15, padx=(10, 10))

                def top_kill():
                    top.destroy()

                exitBtn = Button(lowerFrame, text="Close", font=14, width=10, relief=FLAT,
                                 activebackground='maroon', command=top_kill)
                exitBtn.grid(row=0, column=5, pady=15, padx=(10, 10))

                showAllRecord()
                top.mainloop()

            search_user_button = Button(search_lbl_frame, text='SEARCH BOOK', font=('times', 18, 'bold'),
                                        relief=FLAT, activebackground='#6082B6', background='light green', width=16,
                                        command=searchBooks)
            search_user_button.place(y=15, x=850)

            register_lbl_frame1 = LabelFrame(general_lbl_frame, width=1100, height=450, background=BG, fg='white',
                                             text=":: Book Registration :: ", font=('times', 20, 'bold'), labelanchor=N)
            register_lbl_frame1.grid_propagate(False)
            register_lbl_frame1.grid(row=1, column=0, pady=(2, 4))

            register_lbl_frame = LabelFrame(register_lbl_frame1, width=1000, height=400, background=BG, fg='white')
            register_lbl_frame.grid_propagate(False)
            register_lbl_frame.grid(row=0, column=0, pady=(2, 4), padx=50)

            book_id_lbl = Label(register_lbl_frame, text='Book ID', font=FONT, background=BG)
            book_id_lbl.grid(row=0, column=0, pady=(30, 5))

            book_id_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            book_id_ent.grid(row=1, column=0, padx=(100, 100), pady=(0, 15))

            book_name_lbl = Label(register_lbl_frame, text='Book Name', font=FONT, background=BG)
            book_name_lbl.grid(row=2, column=0)

            book_name_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            book_name_ent.grid(row=3, column=0, padx=(100, 100), pady=(0, 15))

            book_author_lbl = Label(register_lbl_frame, text='Book Author', font=FONT, background=BG)
            book_author_lbl.grid(row=4, column=0)

            book_author_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            book_author_ent.grid(row=5, column=0, padx=(100, 100), pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Publication Year', font=FONT, background=BG)
            book_id_lbl.grid(row=6, column=0)

            publication_year_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            publication_year_ent.grid(row=7, column=0, padx=(100, 100), pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Publishers', font=FONT, background=BG)
            book_id_lbl.grid(row=8, column=0)

            publishers_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            publishers_ent.grid(row=9, column=0, padx=(100, 100), pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Academic Year', font=FONT, background=BG)
            book_id_lbl.grid(row=0, column=1, pady=(30, 5))

            academic_year_ent = ttk.Combobox(register_lbl_frame, width=28, background=EBG, font=FONT)
            academic_year_ent['values'] = ('Select Academic Year', '1', '2', '3', '4')
            academic_year_ent.current(0)
            academic_year_ent.grid(row=1, column=1, padx=40, pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Course', font=FONT, background=BG)
            book_id_lbl.grid(row=2, column=1)

            book_course_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            book_course_ent.grid(row=3, column=1, padx=40, pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Book Condition', font=FONT, background=BG)
            book_id_lbl.grid(row=4, column=1)

            book_condition_ent = ttk.Combobox(register_lbl_frame, width=28, background=EBG, font=FONT)
            book_condition_ent['values'] = ('Select Book Condition', 'Best', 'Good', 'Avarage', 'Worst')
            book_condition_ent.current(0)
            book_condition_ent.grid(row=5, column=1, padx=40, pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Date Added', font=FONT, background=BG)
            book_id_lbl.grid(row=6, column=1)

            date_added_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            date_added_ent.grid(row=7, column=1, padx=40, pady=(0, 15))

            book_id_lbl = Label(register_lbl_frame, text='Registered By', font=FONT, background=BG)
            book_id_lbl.grid(row=8, column=1)

            registered_by_ent = Entry(register_lbl_frame, width=30, background=EBG, font=FONT, foreground='black')
            registered_by_ent.grid(row=9, column=1, padx=40, pady=(0, 15))

            def clearFields():
                msg = messagebox.askyesno("Clear Fields!!", "Are you sure you want to clear all fields")
                if msg > 0:
                    iClear()

            def iClear():
                book_id_ent.delete(0, END)
                book_name_ent.delete(0, END)
                book_author_ent.delete(0, END)
                publication_year_ent.delete(0, END)
                publishers_ent.delete(0, END)
                academic_year_ent.current(0)
                book_course_ent.delete(0, END)
                book_condition_ent.current(0)
                date_added_ent.delete(0, END)
                registered_by_ent.delete(0, END)

            def add_new_book():
                # Insert into database next of kin details
                if book_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Fill in the details to add user!')
                else:
                    book_reg_curs.execute("SELECT book_id FROM book_registration")
                    regNo = book_reg_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if book_id_ent.get() in names:
                        messagebox.showerror("ERROR", f"Book with ID {book_id_ent.get()} already exists!!")
                    else:
                        # Insert record into book registration
                        book_reg_curs.execute("""INSERT INTO book_registration VALUES (
                                            :book_id, :book_name, :book_author, :publication_year, :publishers, :academic_year, :book_course, :book_condition, :date_added, :registered_by)""",
                                              {
                                                  'book_id': book_id_ent.get(),
                                                  'book_name': book_name_ent.get(),
                                                  'book_author': book_author_ent.get(),
                                                  'publication_year': publication_year_ent.get(),
                                                  'publishers': publishers_ent.get(),
                                                  'academic_year': academic_year_ent.get(),
                                                  'book_course': book_course_ent.get(),
                                                  'book_condition': book_condition_ent.get(),
                                                  'date_added': date_added_ent.get(),
                                                  'registered_by': registered_by_ent.get()
                                              }
                                              )
                        messagebox.showinfo("SUCCESS", f"Record for {book_id_ent.get()} Successfully Added!")
                        book_reg_conn.commit()
                        iClear()

            def update_book():
                if book_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Cannot update an empty record!')
                else:
                    book_reg_curs.execute("SELECT book_id FROM book_registration")
                    regNo = book_reg_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if book_id_ent.get() in names:
                        msg = messagebox.askyesno("WARNING", f"Confirm you want to update Book {book_id_ent.get()}?")
                        if msg > 0:
                            # Update user registration details
                            book_reg_curs.execute(
                                "UPDATE book_registration SET book_id=?, book_name=?, book_author=?, publication_year=?, publishers=?, academic_year=?, book_course=?, book_condition=?, date_added=?, registered_by=? WHERE book_id=?",
                                (
                                    book_id_ent.get(),
                                    book_name_ent.get(),
                                    book_author_ent.get(),
                                    publication_year_ent.get(),
                                    publishers_ent.get(),
                                    academic_year_ent.get(),
                                    book_course_ent.get(),
                                    book_condition_ent.get(),
                                    date_added_ent.get(),
                                    registered_by_ent.get(),
                                    book_id_ent.get()
                                )
                                )

                            messagebox.showinfo("SUCCESS", f'Book {book_id_ent.get()} successfully updated!')

                            book_reg_conn.commit()
                            iClear()
                    else:
                        messagebox.showerror("ERROR", 'Cannot update a record that does not exist!')

            def delete_book():
                if book_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Cannot delete an empty record!')
                else:
                    book_reg_curs.execute("SELECT book_id FROM book_registration")
                    regNo = book_reg_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if book_id_ent.get() in names:
                        msg = messagebox.askyesno("WARNING",
                                                  f"Are you sure you want to delete record for book {book_id_ent.get()}?")
                        if msg > 0:
                            book_reg_curs.execute(
                                """DELETE FROM book_registration WHERE book_id=""" + book_id_ent.get())

                            messagebox.showinfo("SUCCESS", f'Record successfully deleted for book {book_id_ent.get()}.')
                            book_reg_conn.commit()
                            iClear()
                    else:
                        messagebox.showerror("ERROR", 'Cannot delete a record that does not exist')

            # This is the button Section
            button_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=130, background=BG)
            button_lbl_frame.grid_propagate(False)
            button_lbl_frame.grid(row=2, column=0, pady=(2, 4))

            add_book_button = Button(button_lbl_frame, text='ADD BOOK', font=('times', 18, 'bold'), relief=FLAT,
                                     activebackground='#7393B3', background='#40B5AD', width=15, height=2,
                                     command=add_new_book)
            add_book_button.grid(row=0, column=0, padx=(50, 25), pady=35)

            update_book_button = Button(button_lbl_frame, text='UPDATE BOOK', font=('times', 18, 'bold'), relief=FLAT,
                                        activebackground='#4F7942', background='#00A36C', width=15, height=2,
                                        command=update_book)
            update_book_button.grid(row=0, column=1, padx=(25, 25), pady=35)

            delete_book_button = Button(button_lbl_frame, text='DELETE BOOK', font=('times', 18, 'bold'), relief=FLAT,
                                        activebackground='red', background='#9A2A2A', foreground='black', width=15,
                                        height=2, command=delete_book)
            delete_book_button.grid(row=0, column=2, padx=(25, 25), pady=35)

            clear_field_button = Button(button_lbl_frame, text='CLEAR FIELDS', font=('times', 18, 'bold'), relief=FLAT,
                                        activebackground='#6082B6', background='#899499', width=15, height=2,
                                        command=clearFields)
            clear_field_button.grid(row=0, column=3, padx=(25, 50), pady=35)

        def issues_books():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.grid_propagate(False)
            general_lbl_frame.pack(pady=3)

            search_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=70, background=BG)
            search_lbl_frame.grid_propagate(False)
            search_lbl_frame.grid(row=0, column=0, pady=(4, 2))

            # Search and verify student
            def verify_student():
                iClear()
                eligibility_status_ent.delete(0, END)
                previous_due_ent.delete(0, END)
                showtreeRecord()
                if search_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Fill in the details to search user!')
                else:
                    user_curs.execute("SELECT user_id FROM user_registration")
                    regNo = user_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if search_id_ent.get() in names:
                        user_curs.execute(
                            "SELECT user_id, user_first_name, user_last_name, user_gender, user_email, user_contact FROM user_registration WHERE user_id=" + str(
                                search_id_ent.get()))
                        studentList = user_curs.fetchall()

                        book_reg_curs.execute(
                            "SELECT prev_due, user_eligibility FROM user_book_detail WHERE user_id=" + str(
                                search_id_ent.get()))
                        studentList1 = book_reg_curs.fetchall()

                        stuDetails = []
                        for item in studentList:
                            stuDetails.append(item)
                        for record in stuDetails:
                            user_id_ent.insert(0, record[0])
                            first_name_ent.insert(END, record[1])
                            last_name_ent.insert(END, record[2])
                            user_gender_ent.delete(0, END)
                            user_gender_ent.insert(END, record[3])
                            user_email_ent.insert(END, record[4])
                            contact_no_ent.insert(END, record[5])

                        bookDetails = []

                        for item in studentList1:
                            bookDetails.append(item)
                        for record in bookDetails:
                            previous_due_ent.delete(0, END)
                            previous_due_ent.insert(0, record[0])
                            eligibility_status_ent.delete(0, END)
                            eligibility_status_ent.insert(END, record[1])
                    else:
                        messagebox.showerror("ERROR", 'User does not exist!')

            def issue_book():
                # Insert into issue book details
                if book_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Fill in the details to issue book!')
                else:
                    book_reg_curs.execute(
                        "SELECT book_id FROM issue_book_detail WHERE user_id = " + str(user_id_ent.get()))
                    regNo = book_reg_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if book_id_ent.get() in names:
                        messagebox.showerror("ERROR",
                                             f"Book with ID {book_id_ent.get()} is already boorrowed by the user!!")
                    else:
                        # Insert record to issue book detail
                        book_reg_curs.execute("""INSERT INTO issue_book_detail VALUES (
                                            :user_id, :book_id, :book_name, :book_author, :publication_year, :book_condition, :book_course, :issue_date, :return_date, :book_fine, :issued_by)""",
                                              {
                                                  'user_id': user_id_ent.get(),
                                                  'book_id': book_id_ent.get(),
                                                  'book_name': book_name_ent.get(),
                                                  'book_author': book_author_ent.get(),
                                                  'publication_year': publication_year_ent.get(),
                                                  'book_condition': book_condition_ent.get(),
                                                  'book_course': course_ent.get(),
                                                  'issue_date': issue_date_ent.get(),
                                                  'return_date': return_date_ent.get(),
                                                  'book_fine': fine_amount_ent.get(),
                                                  'issued_by': issued_by_ent.get()
                                              }
                                              )
                        # Insert record into user detail section
                        book_reg_curs.execute("""INSERT INTO user_book_detail VALUES (
                                            :book_id, :user_id, :first_name, :last_name, :user_gender, :user_email, :user_contact, :prev_due, :user_eligibility)""",
                                              {
                                                  'book_id': book_id_ent.get(),
                                                  'user_id': user_id_ent.get(),
                                                  'first_name': first_name_ent.get(),
                                                  'last_name': last_name_ent.get(),
                                                  'user_gender': user_gender_ent.get(),
                                                  'user_email': user_email_ent.get(),
                                                  'user_contact': contact_no_ent.get(),
                                                  'prev_due': previous_due_ent.get(),
                                                  'user_eligibility': eligibility_status_ent.get()
                                              }
                                              )

                        # Insert into user tree view
                        book_reg_curs.execute("""INSERT INTO issue_book_tree VALUES (
                                            :user_id, :first_name, :user_contact, :book_id, :book_name, :book_condition, :book_course, :issue_date, :return_date, :book_fine, :issued_by, :user_eligibility)""",
                                              {
                                                  'user_id': user_id_ent.get(),
                                                  'first_name': first_name_ent.get(),
                                                  'user_contact': contact_no_ent.get(),
                                                  'book_id': book_id_ent.get(),
                                                  'book_name': book_name_ent.get(),
                                                  'book_condition': book_condition_ent.get(),
                                                  'book_course': course_ent.get(),
                                                  'issue_date': issue_date_ent.get(),
                                                  'return_date': return_date_ent.get(),
                                                  'book_fine': fine_amount_ent.get(),
                                                  'issued_by': issued_by_ent.get(),
                                                  'user_eligibility': eligibility_status_ent.get()
                                              }
                                              )

                        messagebox.showinfo("SUCCESS", f"Book {book_id_ent.get()} Successfully Issued!")
                        book_reg_conn.commit()
                        iClear()
                        studClear()
                        clearTree()
                        search_id_ent.delete(0, END)

            issue_book_button = Button(search_lbl_frame, text='ISSUE BOOK', font=('times', 18, 'bold'), relief=FLAT,
                                       activebackground='#7393B3', background='#40B5AD', width=15, command=issue_book)
            issue_book_button.grid(row=0, column=4, pady=15, padx=500)

            # Search Book
            def search_book():
                top = Tk()
                top.title(":: Search Book ::")
                top.geometry('1000x380+180+130')
                top.resizable(False, False)
                # top.overrideredirect(True)
                top.update_idletasks()

                def clearTree():
                    for record in treeview.get_children():
                        treeview.delete(record)

                def fillRecord():
                    for selected_item in treeview.selection():
                        item = treeview.item(selected_item)
                        studentRegNo = item['values']

                        iClear()
                        studClear()

                        # fill user details section
                        book_reg_curs.execute(
                            "SELECT book_id, book_name, book_author, publication_year, book_condition, book_course FROM book_registration WHERE book_id=" + str(
                                studentRegNo[0]))
                        studentList = book_reg_curs.fetchall()

                        stuDetails = []
                        for item in studentList:
                            stuDetails.append(item)
                        for record in stuDetails:
                            book_id_ent.insert(0, record[0])
                            book_name_ent.insert(END, record[1])
                            book_author_ent.insert(END, record[2])
                            publication_year_ent.insert(END, record[3])
                            book_condition_ent.insert(END, record[4])
                            course_ent.insert(END, record[5])

                    top.destroy()

                def showAllRecord():
                    clearTree()
                    book_reg_curs.execute(
                        "SELECT book_id, book_name, book_author, publication_year, book_condition, book_course FROM book_registration")
                    names = book_reg_curs.fetchall()

                    for name in names:
                        treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                             name[4], name[5]))

                def searchRecord():
                    clearTree()
                    if searchByCombo.get() == 'Book ID':
                        book_reg_curs.execute("SELECT book_id FROM book_registration")
                        regestration = book_reg_curs.fetchall()
                        studentid = []
                        for name in regestration:
                            studentid.append(name[0])

                        if search_ent.get() not in studentid:
                            messagebox.showerror("ERROR", "Record Not Found!!")

                        else:
                            name = search_ent.get()
                            book_reg_curs.execute(
                                "SELECT book_id, book_name, book_author, publication_year, book_condition, book_course FROM book_registration WHERE book_id LIKE '%" + name + "%'")
                            names = book_reg_curs.fetchall()
                            for name in names:
                                treeview.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                                     name[4], name[5]))
                    else:
                        messagebox.showerror("ERROR", "Select From The Combobox!!")

                upperFrame = Frame(top, width=1000, height=300, background='steel blue')
                upperFrame.grid_propagate(False)
                upperFrame.grid(row=0, column=0)

                treeFrame = Frame(upperFrame, width=985, height=285)
                treeFrame.place(y=0, x=0)

                lowerFrame = Frame(top, width=1000, height=80, background='steel blue')
                lowerFrame.grid_propagate(False)
                lowerFrame.grid(row=1, column=0)

                treeview = ttk.Treeview(treeFrame)
                treeview.place(y=0, x=0, height=285, width=985)

                treeview['columns'] = (
                'book_id', 'book_name', 'book_author', 'publication_year', 'book_condition', 'course')
                treeview.column('#0', width=0, stretch=NO)
                treeview.column('book_id', anchor=N, width=120, minwidth=150)
                treeview.column('book_name', anchor=N, width=180, minwidth=200)
                treeview.column('book_author', anchor=N, width=80, minwidth=150)
                treeview.column('publication_year', anchor=N, width=130, minwidth=150)
                treeview.column('book_condition', anchor=N, width=200, minwidth=250)
                treeview.column('course', anchor=N, width=50, minwidth=150)

                treeview.heading('#0', text="", anchor=CENTER)
                treeview.heading('book_id', text="Book ID", anchor=CENTER)
                treeview.heading('book_name', text="Book Name", anchor=CENTER)
                treeview.heading('book_author', text="Book Author", anchor=CENTER)
                treeview.heading('publication_year', text="Publication Year", anchor=CENTER)
                treeview.heading('book_condition', text="Book Condition", anchor=CENTER)
                treeview.heading('course', text="Course Name", anchor=CENTER)

                x_scrollbar = ttk.Scrollbar(upperFrame, orient='horizontal', command=treeview.xview)
                x_scrollbar.place(y=285, x=0, width=1000)

                y_scrollbar = ttk.Scrollbar(upperFrame, command=treeview.yview)
                y_scrollbar.place(y=0, x=985, height=286)

                treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

                fillRecordBtn = Button(lowerFrame, text="Insert Record", font=16, width=13, relief=FLAT,
                                       activebackground='light green', command=fillRecord)
                fillRecordBtn.grid(row=0, column=0, pady=15, padx=(20, 10))

                showAllBtn = Button(lowerFrame, text="Display All", font=16, width=13, relief=FLAT,
                                    activebackground='light green', command=showAllRecord)
                showAllBtn.grid(row=0, column=1, pady=15, padx=(10, 10))

                searchByCombo = ttk.Combobox(lowerFrame, width=10, font=16, background='light grey')
                searchByCombo['values'] = ("Search By", 'Book ID')
                searchByCombo.current(1)
                searchByCombo.grid(row=0, column=2, pady=15, padx=(10, 10))

                search_ent = ttk.Entry(lowerFrame, width=12, font=15, background='light grey', foreground='black')
                search_ent.grid(row=0, column=3, pady=15, padx=(10, 10))

                searchRecordBtn = Button(lowerFrame, text="Search Record", font=16, width=13, relief=FLAT,
                                         activebackground='light green', command=searchRecord)
                searchRecordBtn.grid(row=0, column=4, pady=15, padx=(10, 10))

                def top_kill():
                    top.destroy()

                searchRecordBtn = Button(lowerFrame, text="Close", font=14, width=10, relief=FLAT,
                                         activebackground='maroon', command=top_kill)
                searchRecordBtn.grid(row=0, column=5, pady=15, padx=(10, 10))

                showAllRecord()
                top.mainloop()

            search_user_button = Button(search_lbl_frame, text='SEARCH BOOK', font=('times', 18, 'bold'),
                                        relief=FLAT, activebackground='#6082B6', background='light green', width=16,
                                        command=search_book)
            search_user_button.grid(row=0, column=0, pady=20, padx=30)

            # Search fot book and issue

            issue_book_lbl_frame = LabelFrame(general_lbl_frame, width=1095, height=600, background=BG, fg='white',
                                              text=":: Issue Book :: ", font=('times', 20, 'bold'), labelanchor=N)
            issue_book_lbl_frame.grid_propagate(False)
            issue_book_lbl_frame.grid(row=1, column=0, pady=(2, 4), padx=3)

            # Student Section

            student_section_lbl_frame = LabelFrame(issue_book_lbl_frame, width=540, labelanchor=N, background=BG,
                                                   foreground='white', text=":: Student Section :: ", height=400,
                                                   font=('times', 15, 'bold'))
            student_section_lbl_frame.grid_propagate(False)
            student_section_lbl_frame.grid(row=0, column=1, pady=(2, 4), padx=2)

            def iClear():
                user_id_ent.delete(0, END)
                first_name_ent.delete(0, END)
                last_name_ent.delete(0, END)
                user_gender_ent.current(0)
                user_email_ent.delete(0, END)
                contact_no_ent.delete(0, END)
                previous_due_ent.delete(0, END)
                eligibility_status_ent.delete(0, END)

            def studClear():
                book_id_ent.delete(0, END)
                book_name_ent.delete(0, END)
                book_author_ent.delete(0, END)
                publication_year_ent.delete(0, END)
                book_condition_ent.delete(0, END)
                course_ent.delete(0, END)
                issue_date_ent.delete(0, END)
                return_date_ent.delete(0, END)
                fine_amount_ent.delete(0, END)
                issued_by_ent.delete(0, END)

            student_verify_lbl_frame = LabelFrame(student_section_lbl_frame, width=520, labelanchor=N, background=BG,
                                                  foreground='white', text="Verify Student", height=80,
                                                  font=('times', 12, 'bold'))
            student_verify_lbl_frame.grid_propagate(False)
            student_verify_lbl_frame.grid(row=0, column=0, columnspan=2, pady=(2, 2), padx=2)

            user_id_lbl = Label(student_verify_lbl_frame, text='User ID', font=16, background=BG)
            user_id_lbl.grid(row=0, column=0, pady=20, padx=20)

            search_id_ent = Entry(student_verify_lbl_frame, width=16, background=EBG, font=FONT, foreground='black')
            search_id_ent.grid(row=0, column=1, padx=5, pady=20)

            verify_button = Button(student_verify_lbl_frame, text='VERIFY...', font=FONT, relief=FLAT, width=16,
                                   activebackground='powder blue', command=verify_student, background='steel blue')
            verify_button.grid(row=0, column=2, padx=20, pady=(5, 10))

            # Student sect
            user_id_lbl = Label(student_section_lbl_frame, text='User ID', font=FONT, background=BG)
            user_id_lbl.grid(row=1, column=0, pady=(20, 0))

            user_id_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            user_id_ent.grid(row=2, column=0, padx=15, pady=(0, 15))

            first_name_lbl = Label(student_section_lbl_frame, text='First Name', font=FONT, background=BG)
            first_name_lbl.grid(row=3, column=0)

            first_name_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            first_name_ent.grid(row=4, column=0, padx=15, pady=(0, 15))

            last_name_lbl = Label(student_section_lbl_frame, text='Last Name', font=FONT, background=BG)
            last_name_lbl.grid(row=5, column=0)

            last_name_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            last_name_ent.grid(row=6, column=0, padx=15, pady=(0, 15))

            user_gender_lbl = Label(student_section_lbl_frame, text='Gender', font=FONT, background=BG)
            user_gender_lbl.grid(row=7, column=0)

            user_gender_ent = ttk.Combobox(student_section_lbl_frame, width=21, background=EBG, font=FONT)
            user_gender_ent['values'] = ('Select Gender', 'Male', 'Female', 'Others')
            user_gender_ent.current(0)
            user_gender_ent.grid(row=8, column=0, padx=15, pady=(0, 15))

            user_email_lbl = Label(student_section_lbl_frame, text='Email Address', font=FONT, background=BG)
            user_email_lbl.grid(row=1, column=1, pady=(20, 0))

            user_email_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            user_email_ent.grid(row=2, column=1, padx=15, pady=(0, 15))

            contact_no_lbl = Label(student_section_lbl_frame, text='Contact', font=FONT, background=BG)
            contact_no_lbl.grid(row=3, column=1)

            contact_no_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            contact_no_ent.grid(row=4, column=1, padx=15, pady=(0, 15))

            previous_due_lbl = Label(student_section_lbl_frame, text='Previous Due', font=FONT, background=BG)
            previous_due_lbl.grid(row=5, column=1)

            previous_due_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            previous_due_ent.grid(row=6, column=1, padx=15, pady=(0, 15))

            eligibility_status_lbl = Label(student_section_lbl_frame, text='Eligibility Status', font=FONT,
                                           background=BG)
            eligibility_status_lbl.grid(row=7, column=1)

            eligibility_status_ent = ttk.Combobox(student_section_lbl_frame, width=21, background=EBG, font=FONT)
            eligibility_status_ent['values'] = ('Select Eligibility Status', 'Eligible', 'Not Eligible')
            eligibility_status_ent.current(0)
            eligibility_status_ent.grid(row=8, column=1, padx=15, pady=(0, 15))

            # Book Section

            book_section_lbl_frame = LabelFrame(issue_book_lbl_frame, width=540, height=400, background=BG, fg='white',
                                                text=":: Book Section :: ", font=('times', 15, 'bold'), labelanchor=N)
            book_section_lbl_frame.grid_propagate(False)
            book_section_lbl_frame.grid(row=0, column=0, pady=(2, 4), padx=2)

            book_id_lbl = Label(book_section_lbl_frame, text='Book ID', font=FONT, background=BG)
            book_id_lbl.grid(row=0, column=0, pady=(30, 0))

            book_id_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_id_ent.grid(row=1, column=0, padx=(15, 0), pady=(3, 15))

            book_name_lbl = Label(book_section_lbl_frame, text='Book Name', font=FONT, background=BG)
            book_name_lbl.grid(row=2, column=0)

            book_name_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_name_ent.grid(row=3, column=0, padx=15, pady=(0, 15))

            book_author_lbl = Label(book_section_lbl_frame, text='Book Author', font=FONT, background=BG)
            book_author_lbl.grid(row=4, column=0)

            book_author_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_author_ent.grid(row=5, column=0, padx=15, pady=(0, 15))

            publication_year_lbl = Label(book_section_lbl_frame, text='Publication Year', font=FONT, background=BG)
            publication_year_lbl.grid(row=6, column=0)

            publication_year_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT,
                                         foreground='black')
            publication_year_ent.grid(row=7, column=0, padx=15, pady=(0, 15))

            book_condition_lbl = Label(book_section_lbl_frame, text='Book Condition', font=FONT, background=BG)
            book_condition_lbl.grid(row=8, column=0)

            book_condition_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_condition_ent.grid(row=9, column=0, padx=15, pady=(0, 15))

            course_lbl = Label(book_section_lbl_frame, text='Course', font=FONT, background=BG)
            course_lbl.grid(row=0, column=2, pady=(30, 0))

            course_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            course_ent.grid(row=1, column=2, padx=15, pady=(0, 15))

            issue_date_lbl = Label(book_section_lbl_frame, text='Issue Date', font=FONT, background=BG)
            issue_date_lbl.grid(row=2, column=2)

            issue_date_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            issue_date_ent.grid(row=3, column=2, padx=15, pady=(0, 15))

            return_date_lbl = Label(book_section_lbl_frame, text='Return Date', font=FONT, background=BG)
            return_date_lbl.grid(row=4, column=2)

            return_date_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            return_date_ent.grid(row=5, column=2, padx=15, pady=(0, 15))

            fine_amount_lbl = Label(book_section_lbl_frame, text='Fine on Book', font=FONT, background=BG)
            fine_amount_lbl.grid(row=6, column=2)

            fine_amount_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            fine_amount_ent.grid(row=7, column=2, padx=15, pady=(0, 15))

            issued_by_lbl = Label(book_section_lbl_frame, text='Issued By', font=FONT, background=BG)
            issued_by_lbl.grid(row=8, column=2)

            issued_by_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            issued_by_ent.grid(row=9, column=2, padx=15, pady=(0, 15))

            # Previously Borrowed Book
            def clearTree():
                for record in treeview.get_children():
                    treeview.delete(record)

            def showtreeRecord():
                clearTree()
                book_reg_curs.execute("SELECT * FROM issue_book_tree WHERE user_id = " + str(search_id_ent.get()))
                names = book_reg_curs.fetchall()

                for name in names:
                    treeview.insert(parent="", index=0, text="", values=(
                    name[0], name[1], name[2], name[3], name[4], name[5], name[6], name[7], name[8], name[9], name[10],
                    name[11]))

            previous_borrowed_lbl_frame = LabelFrame(issue_book_lbl_frame, width=1080, height=155, background=BG,
                                                     foreground='white', text=":: Previously Borrowed Section :: ",
                                                     font=('times', 12, 'bold'), labelanchor=N)
            previous_borrowed_lbl_frame.grid_propagate(False)
            previous_borrowed_lbl_frame.grid(row=2, column=0, pady=(2, 4), padx=2, columnspan=2)

            upper_frame = Frame(previous_borrowed_lbl_frame, width=1080, height=140, background='steel blue')
            upper_frame.grid_propagate(False)
            upper_frame.grid(row=0, column=0)

            tree_frame = Frame(upper_frame, width=1080, height=140)
            tree_frame.place(y=0, x=0)

            treeview = ttk.Treeview(tree_frame)
            treeview.place(y=0, x=0, height=120, width=1063)

            treeview['columns'] = ('user_id', 'first_name', 'contact_no', 'book_id', 'book_name', 'condition', 'course',
                                   'issue_date', 'return_date', 'fine', 'issued_by', 'eligibility_status')

            treeview.column('#0', width=0, stretch=NO)
            treeview.column('user_id', anchor=N, width=120, minwidth=150)
            treeview.column('first_name', anchor=N, width=180, minwidth=200)
            treeview.column('contact_no', anchor=N, width=80, minwidth=150)
            treeview.column('book_id', anchor=N, width=130, minwidth=150)
            treeview.column('book_name', anchor=N, width=200, minwidth=250)
            treeview.column('condition', anchor=N, width=50, minwidth=150)
            treeview.column('course', anchor=N, width=50, minwidth=150)
            treeview.column('issue_date', anchor=N, width=100, minwidth=150)
            treeview.column('return_date', anchor=N, width=100, minwidth=150)
            treeview.column('fine', anchor=N, width=100, minwidth=150)
            treeview.column('issued_by', anchor=N, width=100, minwidth=150)
            treeview.column('eligibility_status', anchor=N, width=100, minwidth=150)

            treeview.heading('#0', text="", anchor=CENTER)
            treeview.heading('user_id', text="User ID", anchor=CENTER)
            treeview.heading('first_name', text="First Name", anchor=CENTER)
            treeview.heading('contact_no', text="Contact No", anchor=CENTER)
            treeview.heading('book_id', text="Book ID", anchor=CENTER)
            treeview.heading('book_name', text="Book Name", anchor=CENTER)
            treeview.heading('condition', text="Condition", anchor=CENTER)
            treeview.heading('course', text="Course", anchor=CENTER)
            treeview.heading('issue_date', text="Issue Date", anchor=CENTER)
            treeview.heading('return_date', text="Return Date", anchor=CENTER)
            treeview.heading('fine', text="Fine on Book", anchor=CENTER)
            treeview.heading('issued_by', text="Issued By", anchor=CENTER)
            treeview.heading('eligibility_status', text="Eligibility Status", anchor=CENTER)

            x_scrollbar = ttk.Scrollbar(upper_frame, orient='horizontal', command=treeview.xview)
            x_scrollbar.place(y=120, x=0, width=1078)

            y_scrollbar = ttk.Scrollbar(upper_frame, command=treeview.yview)
            y_scrollbar.place(y=0, x=1065, height=121)

            treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        def return_books():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.grid_propagate(False)
            general_lbl_frame.pack(pady=3)

            search_lbl_frame = LabelFrame(general_lbl_frame, width=1100, height=70, background=BG)
            search_lbl_frame.grid_propagate(False)
            search_lbl_frame.grid(row=0, column=0, pady=(4, 2))

            def fillRecord(e):
                for selected_item in treeview.selection():
                    item = treeview.item(selected_item)
                    record = item['values']

                    studClear()

                    # fill book details section
                    book_id_ent.insert(0, record[1])
                    book_name_ent.insert(END, record[2])
                    book_author_ent.insert(END, record[3])
                    publication_year_ent.insert(END, record[4])
                    book_condition_ent.insert(END, record[5])
                    course_ent.insert(END, record[6])
                    issue_date_ent.insert(END, record[7])
                    return_date_ent.insert(END, record[8])
                    fine_amount_ent.insert(END, record[9])
                    issued_by_ent.insert(END, record[10])

            def iClear():
                user_id_ent.delete(0, END)
                first_name_ent.delete(0, END)
                last_name_ent.delete(0, END)
                user_gender_ent.current(0)
                user_email_ent.delete(0, END)
                contact_no_ent.delete(0, END)
                eligibility_status_ent.delete(0, END)
                previous_due_ent.delete(0, END)

            def studClear():
                book_id_ent.delete(0, END)
                book_name_ent.delete(0, END)
                book_author_ent.delete(0, END)
                publication_year_ent.delete(0, END)
                book_condition_ent.delete(0, END)
                course_ent.delete(0, END)
                issue_date_ent.delete(0, END)
                return_date_ent.delete(0, END)
                fine_amount_ent.delete(0, END)
                issued_by_ent.delete(0, END)

            def clearTree():
                for record in treeview.get_children():
                    treeview.delete(record)

            # Search and verify student
            def verify_student():
                iClear()
                studClear()
                showtreeRecord()
                if search_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Fill in the details to search user!')
                else:
                    user_curs.execute("SELECT user_id FROM user_registration")
                    regNo = user_curs.fetchall()
                    names = []
                    for name in regNo:
                        names.append(name[0])

                    if search_id_ent.get() in names:
                        user_curs.execute(
                            "SELECT user_id, user_first_name, user_last_name, user_gender, user_email, user_contact FROM user_registration WHERE user_id=" + str(
                                search_id_ent.get()))
                        studentList = user_curs.fetchall()

                        book_reg_curs.execute(
                            "SELECT prev_due, user_eligibility FROM user_book_detail WHERE user_id=" + str(
                                search_id_ent.get()))
                        studentList1 = book_reg_curs.fetchall()

                        stuDetails = []
                        for item in studentList:
                            stuDetails.append(item)
                        for record in stuDetails:
                            user_id_ent.insert(0, record[0])
                            first_name_ent.insert(END, record[1])
                            last_name_ent.insert(END, record[2])
                            user_gender_ent.delete(0, END)
                            user_gender_ent.insert(END, record[3])
                            user_email_ent.insert(END, record[4])
                            contact_no_ent.insert(END, record[5])

                        bookDetails = []

                        for item in studentList1:
                            bookDetails.append(item)
                        for record in bookDetails:
                            previous_due_ent.delete(0, END)
                            previous_due_ent.insert(0, record[0])
                            eligibility_status_ent.delete(0, END)
                            eligibility_status_ent.insert(END, record[1])
                    else:
                        messagebox.showerror("ERROR", 'User does not exist!')

            def return_book():
                if book_id_ent.get() == "":
                    messagebox.showerror("ERROR", 'Insert Book ID to delete!')
                else:
                    msg = messagebox.askyesno("WARNING",
                                              f"Confirm returning book {book_id_ent.get()}?")
                    if msg > 0:
                        book_reg_curs.execute("DELETE FROM issue_book_detail WHERE user_id=? AND book_id=?",
                                              (user_id_ent.get(), book_id_ent.get(),))
                        book_reg_curs.execute("DELETE FROM issue_book_tree WHERE user_id=? AND book_id=?",
                                              (user_id_ent.get(), book_id_ent.get(),))
                        book_reg_curs.execute("DELETE FROM user_book_detail WHERE user_id=? AND book_id=?",
                                              (user_id_ent.get(), book_id_ent.get(),))

                        book_reg_conn.commit()
                        messagebox.showinfo("SUCCESS",
                                            f'Book {book_id_ent.get()} Successfully returned.')
                        iClear()
                        studClear()
                        clearTree()

                    else:
                        messagebox.showerror("ERROR", 'Cannot delete a record that does not exist')

            return_book_button = Button(search_lbl_frame, text='RETURN BOOK', font=('times', 18, 'bold'), relief=FLAT,
                                        activebackground='#7393B3', background='#40B5AD', width=15, command=return_book)
            return_book_button.place(y=15, x=850)

            issue_book_lbl_frame = LabelFrame(general_lbl_frame, width=1095, height=600, background=BG, fg='white',
                                              text=":: Return Book :: ", font=('times', 20, 'bold'), labelanchor=N)
            issue_book_lbl_frame.grid_propagate(False)
            issue_book_lbl_frame.grid(row=1, column=0, pady=(2, 4), padx=3)

            # Student Section

            student_section_lbl_frame = LabelFrame(issue_book_lbl_frame, width=540, labelanchor=N, background=BG,
                                                   foreground='white', text=":: Student Section :: ", height=400,
                                                   font=('times', 15, 'bold'))
            student_section_lbl_frame.grid_propagate(False)
            student_section_lbl_frame.grid(row=0, column=0, pady=(2, 4), padx=2)

            student_verify_lbl_frame = LabelFrame(student_section_lbl_frame, width=520, labelanchor=N, background=BG,
                                                  foreground='white', text="Verify Student", height=80,
                                                  font=('times', 12, 'bold'))
            student_verify_lbl_frame.grid_propagate(False)
            student_verify_lbl_frame.grid(row=0, column=0, columnspan=2, pady=(2, 2), padx=2)

            user_id_lbl = Label(student_verify_lbl_frame, text='User ID', font=16, background=BG)
            user_id_lbl.grid(row=0, column=0, pady=20, padx=20)

            search_id_ent = Entry(student_verify_lbl_frame, width=16, background=EBG, font=FONT, foreground='black')
            search_id_ent.grid(row=0, column=1, padx=5, pady=20)

            verify_button = Button(student_verify_lbl_frame, text='VERIFY...', font=FONT, relief=FLAT, width=16,
                                   activebackground='powder blue', command=verify_student, background='steel blue')
            verify_button.grid(row=0, column=2, padx=20, pady=(5, 10))

            user_id_lbl = Label(student_section_lbl_frame, text='User ID', font=FONT, background=BG)
            user_id_lbl.grid(row=1, column=0, pady=(30, 0))

            user_id_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            user_id_ent.grid(row=2, column=0, padx=15, pady=(0, 15))

            first_name_lbl = Label(student_section_lbl_frame, text='First Name', font=FONT, background=BG)
            first_name_lbl.grid(row=3, column=0)

            first_name_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            first_name_ent.grid(row=4, column=0, padx=15, pady=(0, 15))

            last_name_lbl = Label(student_section_lbl_frame, text='Last Name', font=FONT, background=BG)
            last_name_lbl.grid(row=5, column=0)

            last_name_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            last_name_ent.grid(row=6, column=0, padx=15, pady=(0, 15))

            user_gender_lbl = Label(student_section_lbl_frame, text='Gender', font=FONT, background=BG)
            user_gender_lbl.grid(row=7, column=0)

            user_gender_ent = ttk.Combobox(student_section_lbl_frame, width=21, background=EBG, font=FONT)
            user_gender_ent['values'] = ('Select Gender', 'Male', 'Female', 'Others')
            user_gender_ent.current(0)
            user_gender_ent.grid(row=8, column=0, padx=15, pady=(0, 15))

            user_email_lbl = Label(student_section_lbl_frame, text='Email Address', font=FONT, background=BG)
            user_email_lbl.grid(row=1, column=1, pady=(30, 0))

            user_email_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            user_email_ent.grid(row=2, column=1, padx=15, pady=(0, 15))

            contact_no_lbl = Label(student_section_lbl_frame, text='Contact', font=FONT, background=BG)
            contact_no_lbl.grid(row=3, column=1)

            contact_no_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            contact_no_ent.grid(row=4, column=1, padx=15, pady=(0, 15))

            previous_due_lbl = Label(student_section_lbl_frame, text='Previous Due', font=FONT, background=BG)
            previous_due_lbl.grid(row=5, column=1)

            previous_due_ent = Entry(student_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            previous_due_ent.grid(row=6, column=1, padx=15, pady=(0, 15))

            eligibility_status_lbl = Label(student_section_lbl_frame, text='Eligibility Status', font=FONT,
                                           background=BG)
            eligibility_status_lbl.grid(row=7, column=1)

            eligibility_status_ent = ttk.Combobox(student_section_lbl_frame, width=21, background=EBG, font=FONT)
            eligibility_status_ent['values'] = ('Select Status', 'Eligible', 'Not Eligible')
            eligibility_status_ent.current(0)
            eligibility_status_ent.grid(row=8, column=1, padx=15, pady=(0, 15))

            # Book Section

            book_section_lbl_frame = LabelFrame(issue_book_lbl_frame, width=540, height=400, background=BG, fg='white',
                                                text=":: Book Section :: ", font=('times', 15, 'bold'), labelanchor=N)
            book_section_lbl_frame.grid_propagate(False)
            book_section_lbl_frame.grid(row=0, column=1, pady=(2, 4), padx=2)

            book_id_lbl = Label(book_section_lbl_frame, text='Book ID', font=FONT, background=BG)
            book_id_lbl.grid(row=0, column=0, pady=(20, 0))

            book_id_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_id_ent.grid(row=1, column=0, padx=(15, 0), pady=(3, 15))

            book_name_lbl = Label(book_section_lbl_frame, text='Book Name', font=FONT, background=BG)
            book_name_lbl.grid(row=2, column=0)

            book_name_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_name_ent.grid(row=3, column=0, padx=15, pady=(0, 15))

            book_author_lbl = Label(book_section_lbl_frame, text='Book Author', font=FONT, background=BG)
            book_author_lbl.grid(row=4, column=0)

            book_author_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_author_ent.grid(row=5, column=0, padx=15, pady=(0, 15))

            publication_year_lbl = Label(book_section_lbl_frame, text='Publication Year', font=FONT, background=BG)
            publication_year_lbl.grid(row=6, column=0)

            publication_year_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT,
                                         foreground='black')
            publication_year_ent.grid(row=7, column=0, padx=15, pady=(0, 15))

            book_condition_lbl = Label(book_section_lbl_frame, text='Book Condition', font=FONT, background=BG)
            book_condition_lbl.grid(row=8, column=0)

            book_condition_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            book_condition_ent.grid(row=9, column=0, padx=15, pady=(0, 15))

            course_lbl = Label(book_section_lbl_frame, text='Course', font=FONT, background=BG)
            course_lbl.grid(row=0, column=1, pady=(20, 0))

            course_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            course_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

            issue_date_lbl = Label(book_section_lbl_frame, text='Borrowed Date', font=FONT, background=BG)
            issue_date_lbl.grid(row=2, column=1)

            issue_date_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            issue_date_ent.grid(row=3, column=1, padx=15, pady=(0, 15))

            return_date_lbl = Label(book_section_lbl_frame, text='Due Date', font=FONT, background=BG)
            return_date_lbl.grid(row=4, column=1)

            return_date_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            return_date_ent.grid(row=5, column=1, padx=15, pady=(0, 15))

            fine_amount_lbl = Label(book_section_lbl_frame, text='Fine on Book', font=FONT, background=BG)
            fine_amount_lbl.grid(row=6, column=1)

            fine_amount_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            fine_amount_ent.grid(row=7, column=1, padx=15, pady=(0, 15))

            issued_by_lbl = Label(book_section_lbl_frame, text='Issued By', font=FONT, background=BG)
            issued_by_lbl.grid(row=8, column=1)

            issued_by_ent = Entry(book_section_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            issued_by_ent.grid(row=9, column=1, padx=15, pady=(0, 15))

            def showtreeRecord():
                clearTree()
                book_reg_curs.execute("SELECT * FROM issue_book_detail WHERE user_id = " + str(search_id_ent.get()))
                names = book_reg_curs.fetchall()

                for name in names:
                    treeview.insert(parent="", index=0, text="", values=(
                    name[0], name[1], name[2], name[3], name[4], name[5], name[6], name[7], name[8], name[9], name[10]))

            # Previously Borrowed Book

            previous_borrowed_lbl_frame = LabelFrame(issue_book_lbl_frame, width=1080, height=155, background=BG,
                                                     foreground='white', text=":: Borrowed Book Section :: ",
                                                     font=('times', 12, 'bold'), labelanchor=N)
            previous_borrowed_lbl_frame.grid_propagate(False)
            previous_borrowed_lbl_frame.grid(row=2, column=0, pady=(2, 4), padx=2, columnspan=2)

            upper_frame = Frame(previous_borrowed_lbl_frame, width=1080, height=140, background='steel blue')
            upper_frame.grid_propagate(False)
            upper_frame.grid(row=0, column=0)

            tree_frame = Frame(upper_frame, width=1080, height=140)
            tree_frame.place(y=0, x=0)

            treeview = ttk.Treeview(tree_frame)
            treeview.bind("<ButtonRelease-1>", fillRecord)
            treeview.place(y=0, x=0, height=120, width=1063)

            treeview['columns'] = (
            'user_id', 'book_id', 'book_name', 'book_author', 'publication_year', 'book_condition', 'course',
            'borrowed_date', 'due_date', 'fine', 'issued_by')

            treeview.column('#0', width=0, stretch=NO)
            treeview.column('user_id', anchor=N, width=120, minwidth=150)
            treeview.column('book_id', anchor=N, width=120, minwidth=150)
            treeview.column('book_name', anchor=N, width=200, minwidth=230)
            treeview.column('book_author', anchor=N, width=180, minwidth=200)
            treeview.column('publication_year', anchor=N, width=80, minwidth=100)
            treeview.column('book_condition', anchor=N, width=100, minwidth=130)
            treeview.column('course', anchor=N, width=180, minwidth=200)
            treeview.column('borrowed_date', anchor=N, width=100, minwidth=150)
            treeview.column('due_date', anchor=N, width=100, minwidth=150)
            treeview.column('fine', anchor=N, width=80, minwidth=100)
            treeview.column('issued_by', anchor=N, width=100, minwidth=150)

            treeview.heading('#0', text="", anchor=CENTER)
            treeview.heading('user_id', text="User ID", anchor=CENTER)
            treeview.heading('book_id', text="Book ID", anchor=CENTER)
            treeview.heading('book_name', text="Book Name", anchor=CENTER)
            treeview.heading('book_author', text="Book Author", anchor=CENTER)
            treeview.heading('publication_year', text="Publication Year", anchor=CENTER)
            treeview.heading('book_condition', text="Book Condition", anchor=CENTER)
            treeview.heading('course', text="Course", anchor=CENTER)
            treeview.heading('borrowed_date', text="Borrowed Date", anchor=CENTER)
            treeview.heading('due_date', text="Due Date", anchor=CENTER)
            treeview.heading('fine', text="Fine on Book", anchor=CENTER)
            treeview.heading('issued_by', text="Issued By", anchor=CENTER)

            x_scrollbar = ttk.Scrollbar(upper_frame, orient='horizontal', command=treeview.xview)
            x_scrollbar.place(y=120, x=0, width=1078)

            y_scrollbar = ttk.Scrollbar(upper_frame, command=treeview.yview)
            y_scrollbar.place(y=0, x=1065, height=121)

            treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        def i_logout():
            msg = messagebox.askyesno("WARNING", "Are you sure you want to logout?")
            if msg > 0:
                iLogin()
                self.root.destroy()

        def i_exit():
            msg = messagebox.askyesno("WARNING", "Are sure you want to exit the program?")
            if msg > 0:
                self.root.destroy()

        def report_section():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.grid_propagate(False)
            general_lbl_frame.pack(pady=3)

            def showtreeRecord():
                book_reg_curs.execute("SELECT * FROM issue_book_detail")
                names = book_reg_curs.fetchall()

                for name in names:
                    treeview.insert(parent="", index=0, text="", values=(
                    name[0], name[1], name[2], name[3], name[4], name[5], name[6], name[7], name[8], name[9], name[10]))

            def all_registered_books():
                book_reg_curs.execute(
                    "SELECT book_id, book_name, book_author, book_condition, book_course, academic_year, registered_by, date_added FROM book_registration")
                names = book_reg_curs.fetchall()

                for name in names:
                    treeview1.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                         name[4], name[5], name[6], name[7]))

            def all_reg_users():
                user_curs.execute(
                    "SELECT user_id, user_first_name, user_last_name, user_gender, user_id_no, user_contact, user_join_date, user_location FROM user_registration")
                names = user_curs.fetchall()

                for name in names:
                    treeview2.insert(parent="", index=0, text="", values=(name[0], name[1], name[2], name[3],
                                                                         name[4], name[5], name[6], name[7]))

            # User Report
            upperFrame = LabelFrame(general_lbl_frame, width=1010, height=220, background='steel blue', text="TOTAL REGISTERED USERS", labelanchor=N)
            upperFrame.grid_propagate(False)
            upperFrame.grid(row=0, column=0, pady=5, padx=50)

            treeFrame = Frame(upperFrame, width=985, height=185)
            treeFrame.place(y=0, x=0)

            treeview2 = ttk.Treeview(treeFrame)
            treeview2.place(y=0, x=0, height=185, width=985)

            treeview2['columns'] = (
                'user_id', 'user_first_name', 'user_last_name', 'user_gender', 'user_id_no', 'user_contact',
                'user_join_date', 'user_location')
            treeview2.column('#0', width=0, stretch=NO)
            treeview2.column('user_id', anchor=N, width=120, minwidth=150)
            treeview2.column('user_first_name', anchor=N, width=180, minwidth=200)
            treeview2.column('user_last_name', anchor=N, width=80, minwidth=150)
            treeview2.column('user_gender', anchor=N, width=130, minwidth=150)
            treeview2.column('user_id_no', anchor=N, width=200, minwidth=250)
            treeview2.column('user_contact', anchor=N, width=50, minwidth=150)
            treeview2.column('user_join_date', anchor=N, width=50, minwidth=150)
            treeview2.column('user_location', anchor=N, width=100, minwidth=150)

            treeview2.heading('#0', text="", anchor=CENTER)
            treeview2.heading('user_id', text="User Id", anchor=CENTER)
            treeview2.heading('user_first_name', text="First Name", anchor=CENTER)
            treeview2.heading('user_last_name', text="Last Name", anchor=CENTER)
            treeview2.heading('user_gender', text="Gender", anchor=CENTER)
            treeview2.heading('user_id_no', text="ID Number", anchor=CENTER)
            treeview2.heading('user_contact', text="Contact No", anchor=CENTER)
            treeview2.heading('user_join_date', text="Joining Date", anchor=CENTER)
            treeview2.heading('user_location', text="Location", anchor=CENTER)

            x_scrollbar = ttk.Scrollbar(upperFrame, orient='horizontal', command=treeview2.xview)
            x_scrollbar.place(y=185, x=0, width=1000)

            y_scrollbar = ttk.Scrollbar(upperFrame, command=treeview2.yview)
            y_scrollbar.place(y=0, x=985, height=186)

            treeview2.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            # Book Report
            upperFrame = LabelFrame(general_lbl_frame, width=1010, height=220, background='steel blue', text="TOTAL REGISTERED BOOKS", labelanchor=N)
            upperFrame.grid_propagate(False)
            upperFrame.grid(row=1, column=0, pady=5, padx=10)

            treeFrame = Frame(upperFrame, width=985, height=185)
            treeFrame.place(y=0, x=0)

            treeview1 = ttk.Treeview(treeFrame)
            treeview1.place(y=0, x=0, height=185, width=985)

            treeview1['columns'] = (
                'book_id', 'book_name', 'book_author', 'book_condition', 'book_course', 'academic_year',
                'registered_by', 'date_added')
            treeview1.column('#0', width=0, stretch=NO)
            treeview1.column('book_id', anchor=N, width=100, minwidth=120)
            treeview1.column('book_name', anchor=N, width=180, minwidth=150)
            treeview1.column('book_author', anchor=N, width=80, minwidth=120)
            treeview1.column('book_condition', anchor=N, width=120, minwidth=130)
            treeview1.column('book_course', anchor=N, width=200, minwidth=250)
            treeview1.column('academic_year', anchor=N, width=50, minwidth=100)
            treeview1.column('registered_by', anchor=N, width=100, minwidth=150)
            treeview1.column('date_added', anchor=N, width=80, minwidth=100)

            treeview1.heading('#0', text="", anchor=CENTER)
            treeview1.heading('book_id', text="Book ID", anchor=CENTER)
            treeview1.heading('book_name', text="Book Name", anchor=CENTER)
            treeview1.heading('book_author', text="Book Author", anchor=CENTER)
            treeview1.heading('book_condition', text="Book Condition", anchor=CENTER)
            treeview1.heading('book_course', text="Book Course", anchor=CENTER)
            treeview1.heading('academic_year', text="Academic Year", anchor=CENTER)
            treeview1.heading('registered_by', text="Registered By", anchor=CENTER)
            treeview1.heading('date_added', text="Date Added", anchor=CENTER)

            x_scrollbar = ttk.Scrollbar(upperFrame, orient='horizontal', command=treeview1.xview)
            x_scrollbar.place(y=185, x=0, width=1000)

            y_scrollbar = ttk.Scrollbar(upperFrame, command=treeview1.yview)
            y_scrollbar.place(y=0, x=985, height=186)

            treeview1.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            # Borrowed Book
            upper_frame = LabelFrame(general_lbl_frame, width=1010, height=220, background='steel blue', text="TOTAL BORROWED BOOKS", labelanchor=N)
            upper_frame.grid_propagate(False)
            upper_frame.grid(row=2, column=0, pady=5, padx=10)

            treeFrame = Frame(upper_frame, width=985, height=185)
            treeFrame.place(y=0, x=0)

            treeview = ttk.Treeview(treeFrame)
            treeview.place(y=0, x=0, height=185, width=985)

            treeview['columns'] = (
                'user_id', 'book_id', 'book_name', 'book_author', 'publication_year', 'book_condition', 'course',
                'borrowed_date', 'due_date', 'fine', 'issued_by')

            treeview.column('#0', width=0, stretch=NO)
            treeview.column('user_id', anchor=N, width=120, minwidth=150)
            treeview.column('book_id', anchor=N, width=120, minwidth=150)
            treeview.column('book_name', anchor=N, width=200, minwidth=230)
            treeview.column('book_author', anchor=N, width=180, minwidth=200)
            treeview.column('publication_year', anchor=N, width=80, minwidth=100)
            treeview.column('book_condition', anchor=N, width=100, minwidth=130)
            treeview.column('course', anchor=N, width=180, minwidth=200)
            treeview.column('borrowed_date', anchor=N, width=100, minwidth=150)
            treeview.column('due_date', anchor=N, width=100, minwidth=150)
            treeview.column('fine', anchor=N, width=80, minwidth=100)
            treeview.column('issued_by', anchor=N, width=100, minwidth=150)

            treeview.heading('#0', text="", anchor=CENTER)
            treeview.heading('user_id', text="User ID", anchor=CENTER)
            treeview.heading('book_id', text="Book ID", anchor=CENTER)
            treeview.heading('book_name', text="Book Name", anchor=CENTER)
            treeview.heading('book_author', text="Book Author", anchor=CENTER)
            treeview.heading('publication_year', text="Publication Year", anchor=CENTER)
            treeview.heading('book_condition', text="Book Condition", anchor=CENTER)
            treeview.heading('course', text="Course", anchor=CENTER)
            treeview.heading('borrowed_date', text="Borrowed Date", anchor=CENTER)
            treeview.heading('due_date', text="Due Date", anchor=CENTER)
            treeview.heading('fine', text="Fine on Book", anchor=CENTER)
            treeview.heading('issued_by', text="Issued By", anchor=CENTER)

            x_scrollbar = ttk.Scrollbar(upper_frame, orient='horizontal', command=treeview.xview)
            x_scrollbar.place(y=185, x=0, width=1000)

            y_scrollbar = ttk.Scrollbar(upper_frame, command=treeview.yview)
            y_scrollbar.place(y=0, x=985, height=186)

            treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            showtreeRecord()
            all_reg_users()
            all_registered_books()

        def delete_frame():
            for frame in self.right_frame.winfo_children():
                frame.destroy()

        def show_frame(page):
            delete_frame()
            page()

        self.left_frame = Frame(root, width=250, height=690, background='#212121')
        self.left_frame.grid_propagate(False)
        self.left_frame.grid(row=0, column=0)

        home_section_btn = Button(self.left_frame, text="Home\nSection", font=('times', 17, 'bold'),
                                  activebackground='#40B5AD', width=16, command=lambda: show_frame(home_section))
        home_section_btn.grid(row=1, column=0, padx=12, pady=(10, 10))

        issues_books_btn = Button(self.left_frame, text="Issue\nBooks", font=('times', 17, 'bold'),
                                  activebackground='#40B5AD', width=16, command=lambda: show_frame(issues_books))
        issues_books_btn.grid(row=2, column=0, padx=12, pady=(10, 10))

        return_books_btn = Button(self.left_frame, text="Return\nBooks", font=('times', 17, 'bold'),
                                  activebackground='#40B5AD', width=16, command=lambda: show_frame(return_books))
        return_books_btn.grid(row=3, column=0, padx=12, pady=(10, 10))

        register_books_btn = Button(self.left_frame, text="Book\nRegistration", font=('times', 17, 'bold'),
                                    activebackground='#40B5AD', width=16, command=lambda: show_frame(register_books))
        register_books_btn.grid(row=4, column=0, padx=12, pady=(10, 10))

        register_user_btn = Button(self.left_frame, text="User\nRegistration", font=('times', 17, 'bold'),
                                   activebackground='#40B5AD', width=16, command=lambda: show_frame(register_users))
        register_user_btn.grid(row=5, column=0, padx=12, pady=(10, 10))

        report_books_btn = Button(self.left_frame, text="Report\nSection", font=('times', 17, 'bold'),
                                  activebackground='#40B5AD', width=16, command=lambda: show_frame(report_section))
        report_books_btn.grid(row=6, column=0, padx=12, pady=(10, 10))

        i_logout_button = Button(self.left_frame, text="LOGOUT", font=('times', 17, 'bold'),
                                  activebackground='maroon', width=16, command=i_logout)
        i_logout_button.grid(row=7, column=0, padx=12, pady=(10, 10), ipady=10)
        i_Exit_button = Button(self.left_frame, text="EXIT", font=('times', 17, 'bold'),
                                  activebackground='maroon', width=16, command=i_exit)
        i_Exit_button.grid(row=7, column=0, padx=12, pady=(10, 10), ipady=10)

        self.right_frame = Frame(root, width=1110, height=690, background=BG)
        self.right_frame.pack_propagate(False)
        issues_books()
        self.right_frame.grid(row=0, column=1)


class User:
    def __init__(self, root):
        global user_ids
        global fullName

        self.root = root
        self.root.geometry('1360x690')
        self.root.configure(background="#899499")
        self.root.title(f"USER DASHBOARD :: {fullName}")

        self.left_frame = Frame(root, width=250, height=690, background='#212121')
        self.left_frame.grid_propagate(False)
        self.left_frame.grid(row=0, column=0)

        def user_Profile():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.pack_propagate(False)
            general_lbl_frame.pack(pady=3)

            top_frame = LabelFrame(general_lbl_frame, width=1105, height=100, background=BG)
            top_frame.grid_propagate(False)
            top_frame.grid(row=0, column=0, pady=3)

            def update_profile():
                update_profile_lbl_frame = LabelFrame(bottom_frame, width=1000, height=450, background=BG,
                                                      text=":: UPDATE USER PROFILE ::", labelanchor=N, font=('courier', 18, 'bold'))
                update_profile_lbl_frame.pack_propagate(False)
                update_profile_lbl_frame.pack(pady=(20, 150), padx=(100, 100))

                user_name_lbl = Label(update_profile_lbl_frame, text='Username', font=FONT, background=BG)
                user_name_lbl.grid(row=0, column=0, pady=(30, 0))

                user_name_ent = Entry(update_profile_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
                user_name_ent.grid(row=1, column=0, padx=15, pady=(0, 30))

                user_password_lbl = Label(update_profile_lbl_frame, text='Password', font=FONT, background=BG)
                user_password_lbl.grid(row=2, column=0)

                user_password_ent = Entry(update_profile_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
                user_password_ent.grid(row=3, column=0, padx=15, pady=(0, 30))

                contact_no_lbl = Label(update_profile_lbl_frame, text='Contact No', font=FONT, background=BG)
                contact_no_lbl.grid(row=4, column=0)

                contact_no_ent = Entry(update_profile_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
                contact_no_ent.grid(row=5, column=0, padx=15, pady=(0, 30))

                user_email_lbl = Label(update_profile_lbl_frame, text='Email Address', font=FONT, background=BG)
                user_email_lbl.grid(row=0, column=1, pady=(30, 0))

                user_email_ent = Entry(update_profile_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
                user_email_ent.grid(row=1, column=1, padx=15, pady=(0, 30))

                user_location_lbl = Label(update_profile_lbl_frame, text='User Location', font=FONT, background=BG)
                user_location_lbl.grid(row=2, column=1)

                user_location_ent = Entry(update_profile_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
                user_location_ent.grid(row=3, column=1, padx=15, pady=(0, 30))

                def get_info():
                    # This inserts details into the fields from the database
                    user_curs.execute(
                        "SELECT user_email, user_contact, user_location FROM user_registration WHERE user_id LIKE '%" + user_ids + "%'")
                    names = user_curs.fetchall()

                    list = []
                    for name in names:
                        list.append(name)

                    for n in list:
                        user_email = n[0]
                        user_contact = n[1]
                        user_location = n[2]

                    # fetting the login details
                    user_curs.execute(
                        "SELECT username, user_password FROM user_logins WHERE user_id LIKE '%" + user_ids + "%'")
                    names = user_curs.fetchall()

                    list = []
                    for name in names:
                        list.append(name)

                    for n in list:
                        username = n[0]
                        user_password = n[1]
                    def fill_names():
                        user_email_ent.insert(0, user_email)
                        contact_no_ent.insert(0, user_contact)
                        user_location_ent.insert(0, user_location)
                        user_name_ent.insert(0, username)
                        user_password_ent.insert(0, user_password)

                    fill_names()

                get_info()
                def clear():
                    user_name_ent.delete(0, END)
                    user_password_ent.delete(0, END)
                    contact_no_ent.delete(0, END)
                    user_email_ent.delete(0, END)
                    user_location_ent.delete(0, END)

                def submit_profile():
                    msg = messagebox.askyesno("WARNING", f"Are you sure you want to update profile?")
                    if msg > 0:
                        # Update user registration details
                        user_curs.execute(
                            "UPDATE user_registration SET user_email=?, user_contact=?, user_location=? WHERE user_id=?",
                            (
                                user_email_ent.get(),
                                contact_no_ent.get(),
                                user_location_ent.get(),
                                user_ids
                            )
                        )

                        user_curs.execute(
                            "UPDATE user_logins SET username=?, user_password=? WHERE user_id=?",
                            (
                                user_name_ent.get(),
                                user_password_ent.get(),
                                user_ids
                            )
                        )
                        user_conn.commit()
                        messagebox.showinfo("SUCCESS", 'Profile updated successfully')
                        clear()
                        get_info()

                request_book_button = Button(update_profile_lbl_frame, text='UPDATE PROFILE', font=('times', 14, 'bold'),
                                             activebackground='#7393B3', background='#40B5AD', width=20, relief=FLAT,
                                             command=submit_profile)
                request_book_button.grid(row=4, column=1, rowspan=2, ipady=10)

            def cancel_membership():
                cancel_membership_lbl_frame = LabelFrame(bottom_frame, width=1000, height=450, background=BG,
                                                      text=":: CANCEL MEMBERSHIP ::", labelanchor=N, font=('courier', 18, 'bold'))
                cancel_membership_lbl_frame.pack_propagate(False)
                cancel_membership_lbl_frame.pack(pady=(20, 40), padx=(50, 50))

                user_email_lbl = Label(cancel_membership_lbl_frame, text='User ID', font=FONT, background=BG)
                user_email_lbl.grid(row=0, column=0, pady=(30, 0))

                user_id_ent = Entry(cancel_membership_lbl_frame, width=23, background=EBG, font=FONT,
                                       foreground='black')
                user_id_ent.grid(row=1, column=0, padx=15, pady=(0, 15))

                user_location_lbl = Label(cancel_membership_lbl_frame, text='User Name', font=FONT, background=BG)
                user_location_lbl.grid(row=0, column=1, pady=(30, 0))

                user_name_ent = Entry(cancel_membership_lbl_frame, width=23, background=EBG, font=FONT,
                                          foreground='black')
                user_name_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

                user_email_lbl = Label(cancel_membership_lbl_frame, text='Cancellation Reasons', font=FONT, background=BG)
                user_email_lbl.grid(row=2, column=0, pady=(15, 0), columnspan=2)

                cancellation_reason_ent = Text(cancel_membership_lbl_frame, width=60, background=EBG, font=FONT,
                                       foreground='black', height=10)
                cancellation_reason_ent.grid(row=3, column=0, padx=15, pady=(0, 15), columnspan=2)

                user_curs.execute(
                    "SELECT user_id, user_first_name, user_last_name FROM user_registration WHERE user_id LIKE '%" + user_ids + "%'")
                names = user_curs.fetchall()

                list = []
                for name in names:
                    list.append(name)

                for n in list:
                    user_name1 = n[1] + " " + n[2]
                    user_id1 = n[0]

                def fill_names():
                    user_id_ent.insert(0, user_id1)
                    user_name_ent.insert(0, user_name1)

                fill_names()

                def clear():
                    user_id_ent.delete(0, END)
                    user_name_ent.delete(0, END)
                    cancellation_reason_ent.delete(1.0, END)

                    fill_names()

                def clear_fields():
                    msg = messagebox.askyesno("WARNING",
                                              "All fields will be cleared!\nAre you sure you want to proceed?")
                    if msg > 0:
                        clear()

                def submit_profile():
                    msg = messagebox.askyesno("WARNING", "Are you sure you want to submit the form?")
                    if msg > 0:
                        user_curs.execute("""INSERT INTO membership_cancel VALUES(
                            :user_id, :username, :reason)""",
                        {
                            'user_id': user_id_ent.get(),
                            'username': user_name_ent.get(),
                            'reason': cancellation_reason_ent.get(1.0, END)
                        }
                        )
                        user_conn.commit()
                        messagebox.showinfo("SUCCESS", "Cancellation Request Submitted!")
                        clear()

                request_book_button = Button(cancel_membership_lbl_frame, text='SUBMIT\nREQUEST', font=('times', 14, 'bold'),
                                             activebackground='#7393B3', background='#40B5AD', width=20, relief=FLAT,
                                             command=submit_profile)
                request_book_button.grid(row=4, column=0, columnspan=2, ipady=10, pady=(5, 15))


            def delete_frame():
                for frame in bottom_frame.winfo_children():
                    frame.destroy()

            def show_frame(frame):
                delete_frame()
                frame()

            update_profile_button = Button(top_frame, text='UPDATE PROFILE', font=('times', 18, 'bold'),
                                     activebackground='#7393B3', background='#40B5AD', width=20, relief=FLAT,
                                     command=lambda: show_frame(update_profile))
            update_profile_button.grid(row=0, column=0, pady=(10, 10), padx=40)
            cancel_membership_button = Button(top_frame, text='CANCEL \nMEMBERSHIP', font=('times', 18, 'bold'),
                                        activebackground='#7393B3', background='#40B5AD', width=20,
                                        relief=FLAT, command=lambda: show_frame(cancel_membership))
            cancel_membership_button.grid(row=0, column=1, pady=(10, 10), padx=40)

            bottom_frame = LabelFrame(general_lbl_frame, width=1105, height=500, background=BG)
            update_profile()
            bottom_frame.grid_propagate(False)
            bottom_frame.grid(row=1, column=0, pady=3)

        def borrowed_books():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.grid_propagate(False)
            general_lbl_frame.pack(pady=3)

            def showtreeRecord():
                book_reg_curs.execute("SELECT * FROM issue_book_detail WHERE user_id = " + user_ids)
                names = book_reg_curs.fetchall()

                for name in names:
                    treeview.insert(parent="", index=0, text="", values=(
                    name[0], name[1], name[2], name[3], name[4], name[5], name[6], name[7], name[8], name[9], name[10]))

            # Previously Borrowed Book

            previous_borrowed_lbl_frame = LabelFrame(general_lbl_frame, width=1095, height=463, background=BG,
                                                     foreground='white', text=":: Borrowed Book Section :: ",
                                                     font=('times', 18, 'bold'), labelanchor=N)
            previous_borrowed_lbl_frame.grid_propagate(False)
            previous_borrowed_lbl_frame.grid(row=0, column=0, pady=(100, 100), padx=2)

            upper_frame = Frame(previous_borrowed_lbl_frame, width=1095, height=500, background='steel blue')
            upper_frame.grid_propagate(False)
            upper_frame.grid(row=0, column=0)

            tree_frame = Frame(upper_frame, width=1080, height=500)
            tree_frame.place(y=0, x=0)

            treeview = ttk.Treeview(tree_frame)
            showtreeRecord()
            treeview.place(y=0, x=0, height=420, width=1078)

            treeview['columns'] = (
            'user_id', 'book_id', 'book_name', 'book_author', 'publication_year', 'book_condition', 'course',
            'borrowed_date', 'due_date', 'fine', 'issued_by')

            treeview.column('#0', width=0, stretch=NO)
            treeview.column('user_id', anchor=N, width=120, minwidth=150)
            treeview.column('book_id', anchor=N, width=120, minwidth=150)
            treeview.column('book_name', anchor=N, width=200, minwidth=230)
            treeview.column('book_author', anchor=N, width=180, minwidth=200)
            treeview.column('publication_year', anchor=N, width=150, minwidth=200)
            treeview.column('book_condition', anchor=N, width=100, minwidth=130)
            treeview.column('course', anchor=N, width=180, minwidth=200)
            treeview.column('borrowed_date', anchor=N, width=100, minwidth=150)
            treeview.column('due_date', anchor=N, width=100, minwidth=150)
            treeview.column('fine', anchor=N, width=80, minwidth=100)
            treeview.column('issued_by', anchor=N, width=100, minwidth=150)

            treeview.heading('#0', text="", anchor=CENTER)
            treeview.heading('user_id', text="User ID", anchor=CENTER)
            treeview.heading('book_id', text="Book ID", anchor=CENTER)
            treeview.heading('book_name', text="Book Name", anchor=CENTER)
            treeview.heading('book_author', text="Book Author", anchor=CENTER)
            treeview.heading('publication_year', text="Publication Year", anchor=CENTER)
            treeview.heading('book_condition', text="Book Condition", anchor=CENTER)
            treeview.heading('course', text="Course", anchor=CENTER)
            treeview.heading('borrowed_date', text="Borrowed Date", anchor=CENTER)
            treeview.heading('due_date', text="Due Date", anchor=CENTER)
            treeview.heading('fine', text="Fine on Book", anchor=CENTER)
            treeview.heading('issued_by', text="Issued By", anchor=CENTER)

            x_scrollbar = ttk.Scrollbar(upper_frame, orient='horizontal', command=treeview.xview)
            x_scrollbar.place(y=420, x=0, width=1095)

            y_scrollbar = ttk.Scrollbar(upper_frame, command=treeview.yview)
            y_scrollbar.place(y=0, x=1078, height=421)

            treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        def request_book():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.pack_propagate(False)
            general_lbl_frame.pack(pady=3)

            request_lbl_frame = LabelFrame(general_lbl_frame, width=1000, height=600, background=BG,
                                           text=":: REQUEST BOOK ::", font=("courier", 18, 'bold'), labelanchor=N)
            request_lbl_frame.pack_propagate(False)
            request_lbl_frame.pack(pady=50)

            r_book_name_lbl = Label(request_lbl_frame, text='Book Name', font=FONT, background=BG)
            r_book_name_lbl.grid(row=0, column=0, pady=(30, 0))

            r_book_name_ent = Entry(request_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            r_book_name_ent.grid(row=1, column=0, padx=15, pady=(0, 15))

            r_author_lbl = Label(request_lbl_frame, text='Book Author', font=FONT, background=BG)
            r_author_lbl.grid(row=2, column=0, pady=(30, 0))

            r_author_ent = Entry(request_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            r_author_ent.grid(row=3, column=0, padx=15, pady=(0, 15))

            r_publishers_lbl = Label(request_lbl_frame, text='Publishers', font=FONT, background=BG)
            r_publishers_lbl.grid(row=4, column=0, pady=(30, 0))

            r_publishers_ent = Entry(request_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            r_publishers_ent.grid(row=5, column=0, padx=15, pady=(0, 15))

            r_publication_lbl = Label(request_lbl_frame, text='Publication Year', font=FONT, background=BG)
            r_publication_lbl.grid(row=0, column=1, pady=(30, 0))

            r_publication_ent = Entry(request_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            r_publication_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

            r_book_course_lbl = Label(request_lbl_frame, text='Book Course', font=FONT, background=BG)
            r_book_course_lbl.grid(row=2, column=1, pady=(30, 0))

            r_book_course_ent = Entry(request_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            r_book_course_ent.grid(row=3, column=1, padx=15, pady=(0, 15))

            r_academic_year_lbl = Label(request_lbl_frame, text='Academic Year', font=FONT, background=BG)
            r_academic_year_lbl.grid(row=4, column=1, pady=(30, 0))

            r_academic_ent = Entry(request_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            r_academic_ent.grid(row=5, column=1, padx=15, pady=(0, 15))

            def request_a_book():
                msg = messagebox.askyesno("WARNING", "Are you sure you want to request this book?")
                if msg > 0:
                    book_reg_curs.execute("""INSERT INTO request_book VALUES(
                                                            :book_name, :book_author, :publication_year, :book_publishers, :book_course, :academic_year )""",
                                      {
                                          'book_name': r_book_name_ent.get(),
                                          'book_author': r_author_ent.get(),
                                          'publication_year': r_publication_ent.get(),
                                          'book_publishers': r_publishers_ent.get(),
                                          'book_course': r_book_course_ent.get(),
                                          'academic_year': r_academic_ent.get()
                                      }
                                      )
                    book_reg_conn.commit()
                    messagebox.showinfo("SUCCESS", "Book Successfuly requested!")

            def clear_fields():
                msg = messagebox.askyesno("WARNING", "All Fields will be cleared!\nAre you sure you want to proceed?")
                if msg > 0:
                    r_book_name_ent.delete(0, END)
                    r_author_ent.delete(0, END)
                    r_publication_ent.delete(0, END)
                    r_publishers_ent.delete(0, END)
                    r_book_course_ent.delete(0, END)
                    r_academic_ent.delete(0, END)

            request_book_button = Button(request_lbl_frame, text='REQUEST BOOK', font=('times', 18, 'bold'),
                                     activebackground='#7393B3', background='#40B5AD', width=18, height=2, relief=FLAT,
                                     command=request_a_book)
            request_book_button.grid(row=6, column=0, pady=(50, 100), padx=40)
            clear_field_button = Button(request_lbl_frame, text='CLEAR FIELDS', font=('times', 18, 'bold'),
                                        activebackground='#6082B6', background='#899499', width=18, height=2,
                                        relief=FLAT, command=clear_fields)
            clear_field_button.grid(row=6, column=1, pady=(50, 100), padx=40)

        def report_book():
            general_lbl_frame = LabelFrame(self.right_frame, width=1105, height=685, background=BG)
            general_lbl_frame.pack_propagate(False)
            general_lbl_frame.pack(pady=3)

            report_lbl_frame = LabelFrame(general_lbl_frame, width=1000, height=600, background=BG,
                                           text=":: REPORT BOOK ::", font=("courier", 18, 'bold'), labelanchor=N)
            report_lbl_frame.pack_propagate(False)
            report_lbl_frame.pack(pady=50)

            re_user_id_lbl = Label(report_lbl_frame, text='User ID', font=FONT, background=BG)
            re_user_id_lbl.grid(row=0, column=0, pady=(30, 0))

            re_user_id_ent = Entry(report_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            re_user_id_ent.grid(row=1, column=0, padx=15, pady=(0, 5))

            re_user_name_lbl = Label(report_lbl_frame, text='User Name', font=FONT, background=BG)
            re_user_name_lbl.grid(row=2, column=0, pady=(5, 0))

            re_user_name_ent = Entry(report_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            re_user_name_ent.grid(row=3, column=0, padx=15, pady=(0, 5))

            re_book_id_lbl = Label(report_lbl_frame, text='Book ID', font=FONT, background=BG)
            re_book_id_lbl.grid(row=0, column=1, pady=(30, 0))

            re_book_id_ent = Entry(report_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            re_book_id_ent.grid(row=1, column=1, padx=15, pady=(0, 5))

            re_book_name_lbl = Label(report_lbl_frame, text='Book Name', font=FONT, background=BG)
            re_book_name_lbl.grid(row=2, column=1, pady=(5, 0))

            re_book_name_ent = Entry(report_lbl_frame, width=23, background=EBG, font=FONT, foreground='black')
            re_book_name_ent.grid(row=3, column=1, padx=15, pady=(0, 15))

            re_reasons_lbl = Label(report_lbl_frame, text='Reasons', font=FONT, background=BG)
            re_reasons_lbl.grid(row=4, column=0, pady=(5, 0), columnspan=2)

            re_reasons_ent = Text(report_lbl_frame, width=60, background=EBG, font=FONT, foreground='black', height=10)
            re_reasons_ent.grid(row=5, column=0, padx=15, pady=(5, 15), columnspan=2)

            user_curs.execute("SELECT user_id, user_first_name, user_last_name FROM user_registration WHERE user_id LIKE '%" +user_ids+ "%'")
            names = user_curs.fetchall()

            list = []
            for name in names:
                list.append(name)

            for n in list:
                user_name1 = n[1] + " " + n[2]
                user_id1 = n[0]
            def fill_names():
                re_user_id_ent.insert(0, user_id1)
                re_user_name_ent.insert(0, user_name1)
            fill_names()

            def report_a_book():
                msg = messagebox.askyesno("WARNING", "Are you sure you want to report this book?")
                if msg > 0:
                    book_reg_curs.execute("""INSERT INTO report_a_book VALUES(
                                                    :book_id, :book_name, :user_id, :user_name, :reasons)""",
                                          {
                                              'book_id': re_book_id_ent.get(),
                                              'book_name': re_book_name_ent.get(),
                                              'user_id': re_user_id_ent.get(),
                                              'user_name': re_user_name_ent.get(),
                                              'reasons': re_reasons_ent.get(1.0, END)
                                          }
                                          )
                    book_reg_conn.commit()
                    messagebox.showinfo("SUCCESS", "Book Successfuly reported!")
                    clear_fields()

            def clear_fields():
                msg = messagebox.askyesno("WARNING", "All fields will be cleared!\nAre you sure you want to proceed?")
                if msg > 0:
                    re_book_id_ent.delete(0, END)
                    re_book_name_ent.delete(0, END)
                    re_user_id_ent.delete(0, END)
                    re_user_name_ent.delete(0, END)
                    re_reasons_ent.delete(1.0, END)
                    fill_names()

            report_book_button = Button(report_lbl_frame, text='REPORT BOOK', font=('times', 18, 'bold'),
                                        activebackground='#7393B3', background='#40B5AD', width=18, height=2,
                                        relief=FLAT, command=report_a_book)
            report_book_button.grid(row=6, column=0, pady=(50, 100), padx=40)

            clear_field_button = Button(report_lbl_frame, text='CLEAR FIELDS', font=('times', 18, 'bold'),
                                        activebackground='#6082B6', background='#899499', width=18, height=2,
                                        relief=FLAT, command=clear_fields)
            clear_field_button.grid(row=6, column=1, pady=(50, 100), padx=40)

        def i_logout():
            msg = messagebox.askyesno("WARNING", "Are you sure you want to logout?")
            if msg > 0:
                iLogin()
                self.root.destroy()

        def i_exit():
            msg = messagebox.askyesno("WARNING", "Are sure you want to exit the program?")
            if msg > 0:
                self.root.destroy()


        def delete_frame():
            for frame in self.right_frame.winfo_children():
                frame.destroy()

        def show_frame(page):
            delete_frame()
            page()

        issues_books_btn = Button(self.left_frame, text="User\nProfile", font=('times', 17, 'bold'),
                                  activebackground='#40B5AD', width=16, command=lambda: show_frame(user_Profile))
        issues_books_btn.grid(row=0, column=0, padx=12, pady=(10, 10))

        return_books_btn = Button(self.left_frame, text="Borrowed\nBooks", font=('times', 17, 'bold'),
                                  activebackground='#40B5AD', width=16, command=lambda: show_frame(borrowed_books))
        return_books_btn.grid(row=1, column=0, padx=12, pady=(10, 10))

        register_books_btn = Button(self.left_frame, text="Request\nBook", font=('times', 17, 'bold'),
                                    activebackground='#40B5AD', width=16, command=lambda: show_frame(request_book))
        register_books_btn.grid(row=2, column=0, padx=12, pady=(10, 10))

        register_user_btn = Button(self.left_frame, text="Report\nBook", font=('times', 17, 'bold'),
                                   activebackground='#40B5AD', width=16, command=lambda: show_frame(report_book))
        register_user_btn.grid(row=3, column=0, padx=12, pady=(10, 10))

        i_logout_button = Button(self.left_frame, text="LOGOUT", font=('times', 17, 'bold'), activebackground='maroon',
                                 width=16, command=i_logout)
        i_logout_button.grid(row=4, column=0, padx=12, pady=(10, 10), ipady=10)

        i_exit_button = Button(self.left_frame, text="EXIT", font=('times', 17, 'bold'), activebackground='maroon',
                                 width=16, command=i_exit)
        i_exit_button.grid(row=4, column=0, padx=12, pady=(10, 10), ipady=10)

        self.right_frame = Frame(root, width=1110, height=690, background=BG)
        self.right_frame.pack_propagate(False)
        borrowed_books()
        self.right_frame.grid(row=0, column=1)


def iLogin():
    login_window = Tk()
    login_window.resizable(False, False)
    login_window.title("USER LOGIN")
    login_window.config(background='#36454F')

    login_width = 400
    login_height = 500

    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    x1 = (screen_width / 2) - (login_width / 2)
    y1 = (screen_height / 2) - (login_height / 2)

    login_window.geometry('%dx%d+%d+%d' % (login_width, login_height, x1, y1))

    title_label_frame = LabelFrame(login_window, width=300, height=60, background="#36454F")
    title_label_frame.grid_propagate(False)
    title_label_frame.grid(row=0, column=0, padx=20, pady=(10, 5))

    title_label = Label(title_label_frame, text='USER LOGIN', font=('times', 28, 'bold'), background="#36454F")
    title_label.grid(row=0, column=0, pady=12, padx=25)

    details_label_frame = LabelFrame(login_window, width=350, height=400, background="#36454F")
    details_label_frame.grid_propagate(False)
    details_label_frame.grid(row=1, column=0, padx=25, pady=(5, 5))

    log_as_lbl = Label(details_label_frame, text='Login As:', font=('times', 20, 'bold'), background="#36454F",
                       foreground='white')
    log_as_lbl.grid(row=0, column=0, pady=(50, 5))

    log_as_combo = ttk.Combobox(details_label_frame, width=24, state='readonly', font=('times', 18, 'bold'))
    log_as_combo['values'] = ('login as:', 'Admin', 'User')
    log_as_combo.current(0)
    log_as_combo.grid(row=1, column=0, pady=(0, 15), padx=(15, 15))

    username_lbl = Label(details_label_frame, text='Username', font=('times', 20, 'bold'), background="#36454F",
                         foreground='white')
    username_lbl.grid(row=2, column=0)

    username_ent = Entry(details_label_frame, width=25, font=('times', 18, 'bold'), background='light grey',
                         foreground='black')
    username_ent.grid(row=3, column=0, pady=(0, 15), padx=(15, 15))

    password_lbl = Label(details_label_frame, text='Password', font=('times', 20, 'bold'), background="#36454F",
                         foreground='white')
    password_lbl.grid(row=4, column=0)

    password_ent = Entry(details_label_frame, width=25, show="*", font=('times', 18, 'bold'), background='light grey',
                         foreground='black')
    password_ent.grid(row=5, column=0, pady=(0, 15), padx=(15, 15))

    def clearField():
        username_ent.delete(0, END)
        password_ent.delete(0, END)
        log_as_combo.current(0)
        log_as_combo.focus()

    def credentials_Check():
        if log_as_combo.get() == "Admin":
            user_curs.execute("SELECT username FROM admin_lists")
            names = user_curs.fetchall()

            studentid = []
            for name in names:
                studentid.append(name[0])

            if username_ent.get() in studentid:
                name = username_ent.get()
                user_curs.execute("SELECT password FROM admin_lists WHERE username LIKE '%" + name + "%'")
                password = user_curs.fetchall()

                passwords = []
                for name in password:
                    passwords.append(name[0])
                if password_ent.get() == passwords[0]:
                    win = Tk()
                    Admin(win)
                    login_window.destroy()
                else:
                    messagebox.showerror("ERROR", "Invalid Password!")
            else:
                messagebox.showerror("ERROR", "Admin Not Found!")

        elif log_as_combo.get() == "User":
            user_curs.execute("SELECT username FROM user_logins")
            names = user_curs.fetchall()

            studentid = []
            for name in names:
                studentid.append(name[0])

            if username_ent.get() in studentid:
                name = username_ent.get()
                user_curs.execute("SELECT user_password FROM user_logins WHERE username LIKE '%" + name + "%'")
                password = user_curs.fetchall()

                passwords = []
                for name in password:
                    passwords.append(name[0])
                if password_ent.get() == passwords[0]:
                    name = password_ent.get()

                    # to get the user id and make it global
                    # to be used in respective classes to fetch data in databases
                    user_curs.execute("SELECT user_id FROM user_logins WHERE user_password LIKE '%" + name + "%'")
                    user_id = user_curs.fetchall()

                    list = []
                    for name in user_id:
                        list.append(name[0])
                    global user_ids
                    user_ids = list[0]

                    # To get the first name and last name to form username
                    user_curs.execute(
                        "SELECT user_first_name, user_last_name FROM user_registration WHERE user_id LIKE '%" + user_ids + "%'")
                    names = user_curs.fetchall()

                    list = []
                    for name in names:
                        list.append(name)

                    for n in list:
                        user_name1 = n[0] + " " + n[1]

                    # making the username global
                    global fullName
                    fullName = user_name1


                    win = Tk()
                    User(win)
                    login_window.destroy()
                else:
                    messagebox.showerror("ERROR", "Invalid Password!")
            else:
                messagebox.showerror("ERROR", "User Not Found!")
        else:
            messagebox.showerror("ERROR", "Select From The Dropdown!")
            clearField()

    login_btn = Button(details_label_frame, text="LOGIN", font=('times', 22, 'bold'), relief=FLAT,
                       background='steel blue',
                       activebackground='#40B5AD', width=15, command=credentials_Check)
    login_btn.grid(row=6, column=0, ipady=5, pady=10)


def main():
    splash_Screen.destroy()
    iLogin()


if __name__ == '__main__':
    splash_Screen.after(9000, main)
    splash_Screen.mainloop()
    mainloop()
