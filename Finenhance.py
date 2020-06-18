"""-------------------------------------------------------------------------------------------
Yousef Yassin                           January 24, 2019           Build 4.0.1

[FINENHANCE] Financial Application - allows users to create an account and manage various
banking accounts with support for transaction history. Also allows users to have a stock
page where they are able to view various NYSE stock exchanges, along with the stocks'
details and buy or sell shares. The accounts save data to an external file which can be
loaded upon startup. Finally, the app also supports various UI themes which can be
accessed and changed from the settings tab.
(There is also load profile notification in the shell upon login).
---------------------------------------------------------------------------------------------"""

"""Import necessary modules"""
#Tkinter: Used to create and mould app GUI
import tkinter as tk
from tkinter import ttk

#OS: Used to create and access files (for login information)
import os

#Datetime: Used to access and format today's and other dates
#to be used as x points for stock plots (domain)
import datetime as dt
from datetime import timedelta

#Pandas: Used to access stock information Yahoo finance API
#and to manipulate it for use in matplotlib graphing
import pandas as pd
import pandas_datareader as web
#from numpy import arange, sin, pi 

#Yahoo Finance: Also used to access stock info from Yahoo finance
#API but namely to acquire current stock price values
from yahoo_fin import stock_info as si #current stock

#Matplotlib: Used to plot, manipulate and style plots of the stock
#information acquired from Yahoo finance.
import matplotlib
import matplotlib.pyplot as pt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Implement the default mpl key bindings and toolbar support (for plot
#manipulation)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


"""Create app default variables"""
#Creates default font used for majority of app
MAIN_FONT= "malgun gothic semilight"
NAV_COL = '#141d26'
FRA_BG = '#99AAB5'
FRA_FG = 'black'

#Tracks colour change
colC=False

#Creates file that will store login credentials upon
#signup to be referenced in login
creds = 'tempfile.temp'

#New default font size for stock plots
matplotlib.rc('xtick', labelsize=6) 
matplotlib.rc('ytick', labelsize=6)

#Creates default for variables to be
#used throughout the program
balance = 50000
stockFg = 'green'
lineC = 'green'
arrow = 'green'
livP = 'Stocks Price (placehold)'
table = 'Stock Table (placehold)'

#For file saving and loading for portfolio
tickerList = [] #stores stock ticker when bough
priceList = [] #stores ticker price when bought
transList = [] #stores transaction history
timeList = [] #stores time at which transaction occured





"""-------------------------------------------

NAVIGATION FUNCTION (MASTER CLASS)

----------------------------------------------"""
#Main function that is used to display pages (Yousef Y).
class Finenhance(tk.Tk):

    def __init__(self):
        #Initializes functions
        tk.Tk.__init__(self)
        #Creates constant container to house navigation buttons
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) #places the container on the bottom 

        #Dictionary that will hold all pages (classes)
        self.frames = {}

        #For loop that will select pages to be displayed
        #upon button click event
        for F in (HomePage, Accounts, Stocks, Settings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)
    

    #Selected frame is raised above other frames (serves as navigation
    #between pages)
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



"""-------------------------------------------

APPLICATION PAGES & SUBPAGES

----------------------------------------------"""
#-------------------------------------
#Creates main, [Homepage - Login] (Yousef Y)

#-------------------------------------
class HomePage(tk.Frame):

    def __init__(self, master, controller):
        #Intiiates the navigational frame (just placeholder until login complete)
        tk.Frame.__init__(self, master, bg=NAV_COL)
        style = ttk.Style() #Allows further styling of widgets using ttk

                
        #Signup definition upon start up - creates signup pages that
        #allows user to create an account        
        def Signup():
            #Creates and places main background frame to place everything on
            self.homeFrame = tk.Frame(self, width = 500, height = 500, bg = FRA_BG)
            self.homeFrame.pack()

            #Creates Finenhance title on homeframe
            labelTitleFIN = tk.Label(self.homeFrame, text="FIN", font=(MAIN_FONT, 35), bg = FRA_BG, fg='#121f1f')
            labelTitleFIN.place(relx=0.315, rely=0.2, anchor='n') #Used to places objects on the frame
            labelTitleEN = tk.Label(self.homeFrame, text="ENHANCE", font=(MAIN_FONT, 35), bg = FRA_BG, fg='green')
            labelTitleEN.place(relx=0.6, rely=0.2, anchor='n')

            #Puts an instruction label in the window telling users to sign up
            instruction = tk.Label(self.homeFrame, text="Please Enter new Credentials\n", bg=FRA_BG, font=(MAIN_FONT, 12))
            instruction.place(relx=0.5, rely=0.45, anchor="n")

            #Labels to tell users where to place username and password for sign up
            self.nameL = tk.Label(self.homeFrame, text="New Username", font=(MAIN_FONT, 15), bg=FRA_BG, fg='green')
            self.pwordL = tk.Label(self.homeFrame, text="New Password", font=(MAIN_FONT, 15), bg=FRA_BG, fg='green')
            self.nameL.place(relx=0.5, rely=0.55, anchor="n")
            self.pwordL.place(relx=0.5, rely=0.7, anchor="n")

            #Places two text boxes under the according labels to accept credentials
            #as an input (Show="*" shows the password characters as *s)
            self.nameE = tk.Entry(self.homeFrame)
            self.pwordE = tk.Entry(self.homeFrame, show="*")
            self.nameE.place(relx=0.5, rely=0.6, anchor="n")
            self.pwordE.place(relx=0.5, rely=0.75, anchor="n")

            #Creates a signup button to call the next definition FSSignup
            signupButton = ttk.Button(self.homeFrame, text="Signup", command=FSSignup)
            signupButton.place(relx=0.5, rely=0.83, anchor="n")        


        #Stores the users credentials entered in entry box of signup
        def FSSignup():
            #Creates document (creds - called 'tempfile')
            with open(creds, 'w') as f: 
                f.write(self.nameE.get()) #Stores username string from entry on first line
                f.write('\n') #Splits to next line
                f.write(self.pwordE.get())#Stores password string from entry on second line
                f.close() #Closes file
                self.homeFrame.destroy()#Destroys the signup page
            Login() #Calls login definition to open login page


        #Creates login window to allow users to login using signup credentials
        def Login():
            global rmuser #more globals - used to delete login and signup return once logged in
            global loginB
            
            #Creates the new login window
            self.homeLFrame = tk.Frame(self, width = 500, height = 500, bg = FRA_BG)
            self.homeLFrame.pack()

            #Creates Finenhance title on new login frame           
            labelTitleFIN = tk.Label(self.homeLFrame, text="FIN", font=(MAIN_FONT, 35), bg = FRA_BG, fg='#121f1f')
            labelTitleFIN.place(relx=0.315, rely=0.2, anchor='n')
            labelTitleEN = tk.Label(self.homeLFrame, text="ENHANCE", font=(MAIN_FONT, 35), bg = FRA_BG, fg='green')
            labelTitleEN.place(relx=0.6, rely=0.2, anchor='n')

            #Puts new instruction label in the window telling users to login
            instruction = tk.Label(self.homeLFrame, text = "Please Login\n", bg=FRA_BG, font=(MAIN_FONT, 12))
            instruction.place(relx=0.5, rely=0.45, anchor="n")

            #More labels to indicate where to enter certain credentials
            self.nameL=tk.Label(self.homeLFrame, text="Username", bg=FRA_BG, font=(MAIN_FONT, 15), fg='green')
            self.pwordL=tk.Label(self.homeLFrame, text="Password", bg=FRA_BG, font=(MAIN_FONT, 15), fg='green')
            self.nameL.place(relx=0.5, rely=0.55, anchor="n")
            self.pwordL.place(relx=0.5, rely=0.7, anchor="n")

            #Two more entry boxes to enter username and password to login
            self.nameEL=tk.Entry(self.homeLFrame)
            self.pwordEL=tk.Entry(self.homeLFrame, show="*")
            self.nameEL.place(relx=0.5, rely=0.6, anchor="n")
            self.pwordEL.place(relx=0.5, rely=0.75, anchor="n")

            #Creates login button, clicked when users have finished entering credentials
            #call checklogin to check input
            loginB = ttk.Button(self.homeLFrame, text="Login", command=CheckLogin)
            loginB.place(relx=0.5, rely=0.8, anchor="n")  

            #Creates remove user button to act as back button to return to signup page
            #to create new credentials if need be
            style.configure("Del.TButton", foreground = 'red', font=(MAIN_FONT, 9)) #styles the button to be red
            rmuser = ttk.Button(self.homeLFrame, text="Delete User", style = 'Del.TButton', command =DelUser)
            rmuser.place(relx=0.5, rely=0.85, anchor="n")



        #Checks input in entry of login window and compares to the tempfile document
        #to validate if the login matches 
        def CheckLogin():
            #Makes username and password global to load and
            #save data in NavAccess() and save() - in stocks
            global uname, pword 
            with open(creds) as f:
                data = f.readlines()    #Takes entire creds document and puts its info into a variable
                uname = data[0].rstrip()    #makes the first line (username in signup) a variable
                pword = data[1].rstrip()    #makes the second line (password in signup) a variable

            #Checks if login data matches signup data
            if self.nameEL.get() == uname and self.pwordEL.get() == pword: #if so..
                #Opens new window to notify user that they have been logged in
                self.r = tk.Tk() 
                self.r.title(":D")
                self.r.iconbitmap('favicon.ico')#sets app icon 
                self.r.geometry("150x50")
                
                #Prints welcome message to user using their inputed username
                rlbl=tk.Label(self.r, text='\n[+] Logged In \n Welcome back ' + self.nameEL.get() + '!')
                rlbl.pack()
                
                #Deletes the remove user and login buttons since no longer needed
                rmuser.destroy()
                loginB.destroy()
                
                #Calls NavAccess to initiate navigational control over app (can open new pages)
                NavAccess()
                self.r.mainloop() #allows the login notification window to remain open

                
            #If input data do not match, creates new window notifying user that
            #this is an invalid login and to try again.
            else:
                self.r = tk.Tk()
                self.r.title("D:")
                self.r.wm_iconbitmap('favicon.ico')#sets app icon 
                self.r.geometry("150x50")
                rlbl = tk.Label(self.r, text="\n[!] Invalid Login")
                rlbl.pack()
                self.r.mainloop()

                
        #If need be, allows user to delete singup credentials, to return to signup page and restart        
        def DelUser():
            os.remove(creds) #deletes the creds file
            self.homeLFrame.destroy() #destroys the login page
            Signup() #calls signup to return to signup page



        #Creates the navigational bar once logged in   
        def NavAccess():
            global balance, tickerList, priceList, timeList, transList
            #Creates a finenhance label on the nav bar
            navLabel = tk.Label(self, text="Finenhance", font=(MAIN_FONT, 12), bg=NAV_COL, fg='#e5dddb')
            navLabel.pack(pady=5,padx=10)

            #Another welcome message (in green) to the user
            welcomeLabel = tk.Label(self, text='Welcome back ' + self.nameEL.get() + '!', font=(MAIN_FONT, 10), bg=NAV_COL, fg='green')
            welcomeLabel.pack(padx=10, pady=10)

            #More styling
            style.configure("TButton", foreground="green", font=(MAIN_FONT, 9))
            style.map("TButton",
                foreground=[('pressed', 'black'), ('active', 'green')],
                background=[('pressed', '!disabled', 'black'), ('active', 'green')]
                )


            #Creates 2 buttons (Stocks (Yousef Y.) and Accounts to navigate to those
            #respective pages
            button = ttk.Button(self, text="Accounts",
                                command=lambda: controller.show_frame(Accounts))
            button.pack()

            button2 = ttk.Button(self, text="Stocks",
                                command=lambda: controller.show_frame(Stocks))
            button2.pack()

            button3 = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
            button3.pack()

            #Will try to load data from file if user has previously
            #saved info
            try:
                #Searches for unqiue file pertaining
                #to user's name and pass 
                f = open(uname + pword + ".txt", "r")
                information = f.readlines() #creates list of file info
                balance = float(information[0]) #balance is the first line

                #sorts through the list and formats it to show stock owned and price bought at
                for i in range(len(information)-1):
                    tickerList.append(information[i+1].partition(" ")[0])
                    priceList.append(float(information[i+1].partition(" ")[-1].strip('\n')))

                #Loads information for transaction history if available
                t = open(uname + pword + "t" + ".txt", "r")
                transactions = t.readlines()
                for i in range(len(transactions)):
                    timeList.append(transactions[i].partition(".")[0])
                    transList.append(transactions[i].partition(".")[2].strip("\n"))
                    

                #Notifies user they have logged before and that their info was found
                #prints the user's saved data
                print("Loaded Profile! Welcome Back " + uname.capitalize() + ".")
                print()
                
                print("Balance: $", balance)
                print()
                
                print("Shares Owned Currently: ") 
                for i in range(len(tickerList)):
                    print(tickerList[i].upper() + "  $" + str(priceList[i]))
                    print()
                    
                print("Transaction History: ")
                for i in range(len(transList)):
                    command = transList[i].partition(".")[0]
                    money = transList[i].partition(".")[2]
                    print(str(i) + ". " + timeList[i] + 5*(" ") + command + " $" + money)
                
                    
                #If file is not found, user has not logged in before and so
            #notifies user
            except FileNotFoundError:
                print("No data found for user")

        #Calls signup to initiate the app
        Signup()




      
#-------------------------------------------------
#Creates [Accounts - Transactions] page (Yousef Y)
        
#-------------------------------------------------
class Accounts(tk.Frame):
    
    def __init__(self, master, controller):
        global balance
        self.i = False #stores configuration of error bar (to destroy)
        
        #Initiates Nav Frame
        tk.Frame.__init__(self, master, bg=NAV_COL)

        #Creates accounts page frame
        accFrame = tk.Frame(self, width = 500, height = 600, bg = FRA_BG)
        accFrame.pack()

        #Creates accounts title on navigation bar
        navLabel = tk.Label(self, text="Accounts", font=(MAIN_FONT, 15), bg=NAV_COL, fg='#e5dddb')
        navLabel.pack(pady=10,padx=10)


        #FRAME
        labelTitle = tk.Label(accFrame, text="Checkings", font=(MAIN_FONT, 20), bg = FRA_BG)
        labelTitle.place(relx=0.5, rely=0.03, anchor='n')

        button = ttk.Button(accFrame, text="Access Account",
                            command=lambda: showLab())
        button.place(relx=0.5, rely=0.9, anchor = 'n')

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Stocks",
                            command=lambda: controller.show_frame(Stocks))
        button2.pack()

        button3 = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
        button3.pack()

        #Refreshes the frame (for background change)
        def refresh():
            global colC
            if colC:
                accFrame.configure(bg=FRA_BG)
                labelTitle.configure(bg=FRA_BG, fg = 'white')

        #Displays widgets on button press for account details
        #(must be on button press so it isnt run on initial startup, when load hasnt yet occured)
        def showLab():
            global balance

            #Updates theme colours
            refresh()

            #Creates balance title lable and displays current checkings balance below along with "CAD" currency
            binstL = tk.Label(accFrame, text="Balance:", font=(MAIN_FONT, 25), bg = FRA_BG, fg=FRA_FG)
            binstL.place(relx=0.25, rely=0.13, anchor='nw')

            bLabel = tk.Label(accFrame, text = "$" + str(round(balance,2)), bg=FRA_BG, fg = FRA_FG, font = (MAIN_FONT, 25, 'bold'))    
            bLabel.place(relx=0.25, rely=0.2, anchor='nw')

            curr = tk.Label(accFrame, text = 'CAD', fg = '#eaeaea', bg=FRA_BG, font=(MAIN_FONT, 25))
            curr.place(relx=0.6, rely=0.2, anchor='nw')

            #Creates deposit and withdraw buttons that go along with money entry box, amount
            #to manipulate is defined by value within entry
            depB = ttk.Button(accFrame, text = 'Deposit',
                              command=lambda: Transaction("Deposit", monEntry.get()))
            withB = ttk.Button(accFrame, text = 'Withdraw',
                              command=lambda: Transaction("Withdrawal", monEntry.get()))

            monEntry = ttk.Entry(accFrame)

            depB.place(relx=0.3, rely=0.296, anchor='n')
            withB.place(relx=0.7, rely=0.296, anchor='n')
            monEntry.place(relx=0.5, rely=0.3, anchor='n')

            #Creates button to save portfolio to new text file (transactions mainly and balance)
            saveB = ttk.Button(accFrame, text="Save Portfolio",
                            command=lambda: Save())
            saveB.place(relx=0.5, rely=0.35, anchor = 'n')

            #Displays name of logged user
            uLabel = tk.Label(accFrame, text = uname, bg = FRA_BG, fg = FRA_FG, font = (MAIN_FONT, 25))
            uLabel.place(relx=0.5, rely=0.4, anchor = 'n')

            #Upon save button press, will save current balance value and ticker/price lists
            #for stock info (must save twice, since balance will load from here - can't have two instances
            #of the same variable as they will diverge)
            def Save():
                #Saves info under unique file pertaining to username and password as the name
                #(if already there will open it, else will create one)
                f=open(uname + pword + ".txt", "w+")
                f.write(str(round(balance,2))) #stores balance value
                f.write('\n') #skips to new line

                #for each item in ticker list, store it and its value beside it (each ticker
                #and its price are in the same index position in their according lists)
                for i in range(len(tickerList)):
                    f.write(tickerList[i] + " " + str(priceList[i]))
                    f.write('\n')
                
                f.close

                #Creates second user defined file to save transaction history (same principle as above)
                t=open(uname + pword + "t" + ".txt", "w+")
                for i in range(len(transList)):
                    t.write(timeList[i] + "." + transList[i])
                    t.write('\n')

                t.close

            #Shows transaction history in scrollable canvas
            def showT():
                def data():
                    #Creates the required number of variable names for frames and buttons
                    for i in range(len(transList)):
                        command = transList[i].partition(".")[0]
                        money = transList[i].partition(".")[2]

                        #Sets colour of money in log if deposit (green) or withdraw (red)
                        if command == 'Deposit':
                            monCol = 'green'
                            money = " " + money
                        else:
                            monCol = 'red'
                            money = "-" + money

                        chars = len(money)-2 #adjusts spaces for formating bigger values
                        #Displays each transaction type, time at which done, number in sequence and money amount in row
                        history = tk.Label(transFrame, text = str(i) + " " + timeList[i] + " ", bg = NAV_COL, fg='white', font = (MAIN_FONT, 12)).grid(row=i, column = 0, sticky = 'w')
                        manip = tk.Label(transFrame, text = command + (13-chars)*(" "), bg=NAV_COL, fg='white', font = (MAIN_FONT, 12, 'bold')).grid(row=i, column = 1, sticky = 'w')
                        amount = tk.Label(transFrame, text = "$" + money, bg = NAV_COL, fg = monCol, font = (MAIN_FONT, 12)).grid(row=i, column = 2, sticky = 'e')
                        
                #Creates scroll bindable canvas to place log within
                def canvasFunction(event):
                    #Creates canvas with defined scroll region
                    canvas.configure(scrollregion=canvas.bbox("all"),width=400,height=200,
                                     bg=FRA_BG, borderwidth = 0, highlightthickness=0)

                #Creates frame to place canvas upon
                canvFrame=tk.Frame(accFrame,relief='groove',width=50,height=100,bd=1)
                canvFrame.place(relx=0.5,rely=0.7, anchor='center')

                #Creates scrollbar for canvas when bigger than defined region initially
                #and designate scroll to y view
                canvas=tk.Canvas(canvFrame, bg = NAV_COL)
                transFrame=tk.Frame(canvas, bg=NAV_COL, width = 200, height = 50)
                myscrollbar=tk.Scrollbar(canvFrame,orient="vertical",command=canvas.yview)
                canvas.configure(yscrollcommand=myscrollbar.set)

                #Displays canvas and scroll region 
                myscrollbar.pack(side="right",fill="y")
                canvas.pack(side="left")
                canvas.create_window((0,0),window=transFrame,anchor='nw')
                transFrame.bind("<Configure>",canvasFunction)

                #acquires and displays transaction data
                data()

            #Creates the transaction
            def Transaction(x, y):
                global transList, timeList, balance

                #stores time at which transaction was created
                time = str(dt.datetime.now()).partition(".")[0]

                #Refreshes any newly created variables (important if returning to
                #accounts page after previous instance)
                refresh()
                binstL.configure(bg=FRA_BG, fg = FRA_FG)
                bLabel.configure(bg=FRA_BG, fg = FRA_FG)
                curr.configure(bg=FRA_BG)
                uLabel.configure(bg=FRA_BG, fg = FRA_FG)

                              
                try:
                    #Error check for positive float value
                    y=float(y)
                    if y<=0:
                        raise ValueError

                    #Destroys error message if present upon valid money entered
                    elif self.i:
                        self.LabelI.destroy()
                        self.i = False

                    #Adds transaction type (withdraw or deposit) along with value to
                    #list to display and save. Also adds time at which created
                    transList.append(str(x) + "." + str(y))
                    timeList.append(time)

                    #Displays transactions log
                    showT()

                    #Updates balance variable and label if deposit (+) or withdraw (-)
                    if x == 'Deposit':
                        balance += y
                        bLabel['text'] = '$' + str(round(balance,2))
                    else:
                        if y <= balance:
                            balance -= y
                            bLabel['text'] = '$' + str(round(balance,2))
                        else:
                            print("Insufficient Funds!")

                #Display error instruction upon non number entered       
                except ValueError:
                    if self.i == False:
                        self.LabelI = tk.Label(accFrame, text="Invalid monetary value, try again." , bg = FRA_BG, fg="red", font = (MAIN_FONT, 8))
                        self.LabelI.place(relx=0.5, rely=0.5, anchor="n")
                        self.i = True #shows error was shown
                    print("Enter valid value.")




                    
#-------------------------------------
#Creates [Settings] page (Yousef Y)
                    
#-------------------------------------
class Settings(tk.Frame):
    
    def __init__(self, master, controller):
        #Initiates nav frame
        tk.Frame.__init__(self, master, bg=NAV_COL)

        #Creates settings page frame
        setFrame = tk.Frame(self, width = 500, height = 600, bg = FRA_BG)
        setFrame.pack()

        #Nav title label
        navLabel = tk.Label(self, text="Settings", font=(MAIN_FONT, 15), bg=NAV_COL, fg='#e5dddb')
        navLabel.pack(pady=10,padx=10)

        #FRAME
        labelTitle = tk.Label(setFrame, text="Settings", font=(MAIN_FONT, 20), bg = FRA_BG)
        labelTitle.place(relx=0.5, rely=0.2, anchor='n')

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Stocks",
                            command=lambda: controller.show_frame(Stocks))
        button2.pack()

        button3 = ttk.Button(self, text="Accounts",
                            command=lambda: controller.show_frame(Accounts))
        button3.pack()

        #Refreshes the frame (for background change)
        def refresh():
            setFrame.configure(bg=FRA_BG)
            labelTitle.configure(bg=FRA_BG, fg = 'white')

        #Changes app main colour theme variables (x bg, y fg)  
        def change(x, y): 
            global FRA_BG, colC, FRA_FG
            #Initiates that colour change was made (for refresh to work)
            colC = True
            
            FRA_BG = x
            FRA_FG = y
            refresh()

        #Nightmode colours button
        darkB = ttk.Button(setFrame, text = 'NightMode', command = lambda: change('#243447', 'white'))
        darkB.place(relx=0.5, rely=0.5, anchor='center')

        #Nightermode colours button
        darkerB = ttk.Button(setFrame, text = 'NighterMode', command = lambda: change('#23272A', 'white'))
        darkerB.place(relx=0.5, rely=0.6, anchor='center')

        #Default colours button
        normalB = ttk.Button(setFrame, text = 'Normal', command = lambda: change('#99AAB5', 'black'))
        normalB.place(relx=0.5, rely=0.7, anchor='center')




        
#-------------------------------------
#Creates [Stocks] page (Yousef Y)
        
#-------------------------------------
class Stocks(tk.Frame):
    
    def __init__(self, master, controller):
        style = ttk.Style()

        #Used in details function for repitition
        self.tickerNameD = 'Ticker Name in details (Placehold)'
        
        #Initiates navigational frame (bottom)
        tk.Frame.__init__(self, master, bg=NAV_COL)

        #Creates actual stock page frame (create first to be ontop)
        stockFrame = tk.Frame(self, width = 500, height = 600, bg = FRA_BG)
        stockFrame.pack()
        
        #Creates stock page title and nav buttons on navigational frame
        navLabel = tk.Label(self, text="Stocks", font=(MAIN_FONT, 15), bg=NAV_COL, fg='#e5dddb')
        navLabel.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Accounts",
                            command=lambda: controller.show_frame(Accounts))
        button2.pack()

        button3 = ttk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(Settings))
        button3.pack()
        
        #Verfification for existing toolbar and invalid text indicator
        #to delete on reexecution if exists.
        self.tool=False
        self.open = False
        self.i = False

        #FRAME Setup 
        labelTitle = tk.Label(stockFrame, text="Stocks", font=(MAIN_FONT, 20), bg = FRA_BG, fg = 'black')
        labelTitle.place(relx=0.5, rely=0.03, anchor='n')

        #Entry widget to enter ticker of stock to be plotted
        tickerEntry = ttk.Entry(stockFrame)
        tickerEntry.place(relx=0.18, rely=0.938, anchor='n')

        #Upon button press, access stock info and plot it (below function)
        tickerButton = ttk.Button(stockFrame, text="Confirm",
                            command=lambda: pressPlot(tickerEntry.get()))
        tickerButton.place(relx=0.38, rely=0.938, anchor='n')

        #Creates radiobuttons to choose length of stock history
        style.configure("TRadiobutton", background = FRA_BG, selectcolor = 'green', font=(MAIN_FONT, 10))
        style.map("TRadiobutton", foreground=[('pressed', 'green')])

        #5 days
        Radio_1=ttk.Radiobutton(stockFrame, text = '5dy', value = 1,
                                command=lambda: setDate(5))
        Radio_1.place(relx=0.05, rely=0.76, anchor='nw')

        #1 month    
        Radio_2=ttk.Radiobutton(stockFrame, text = '1mo', value = 2,
                                command=lambda: setDate(30))
        Radio_2.place(relx=0.15, rely=0.76, anchor='nw')

        #6 months    
        Radio_3=ttk.Radiobutton(stockFrame, text = '6mo', value = 3,
                                command=lambda: setDate(180))
        Radio_3.place(relx=0.25, rely=0.76, anchor='nw')

        #1 year
        Radio_4=ttk.Radiobutton(stockFrame, text = '1yr', value = 4,
                                command=lambda: setDate(365))
        Radio_4.place(relx=0.35, rely=0.76, anchor='nw')

        #5 years
        Radio_5=ttk.Radiobutton(stockFrame, text = '5yr', value = 5,
                                command=lambda: setDate(1826))
        Radio_5.place(relx=0.45, rely=0.76, anchor='nw')
        
        #Refreshes the frame (for background change)
        def refresh():
            global colC
            if colC:
                stockFrame.configure(bg=FRA_BG)
                labelTitle.configure(bg=FRA_BG, fg = 'white')
                style.configure("TRadiobutton", background = FRA_BG, foreground = 'white')

        #Upon call from a radio button, sets various variables to match current date
        #and previous date according to inputed time delta
        def setDate(x):
            #These globals make the variables available to the entrie script
            #usable by any definition that follows
            global year2 
            global month2
            global date2
            global year1
            global month1
            global date1

            #-Current Date-
            #uses datetime to create string of current date (x2)
            now = dt.datetime.now() 
            current = str(now)
            #Sorts through string to store year, month and date which is needed
            #to plot the day and acquire stock data (for pandas and numpy)
            year2 = int(current[0:4])
            month2 = int(current[5:7])
            date2 = int(current[8:10])
            currentList = [year2, month2, date2]

            #Uses timedelta to find the prior date (x1)
            before = dt.datetime.now() - timedelta(days=x)

            #-Prior Date-
            #Creates prior date string which is also sorted to find
            #year, month and date for same reasons
            prior = str(before)
            year1 = int(prior[0:4])
            month1 = int(prior[5:7])
            date1 = int(prior[8:10])
            priorList = [year1, month1, date1]
            
            #Prints both dates in shell (mainly for debug)
            print()
            print('Start Date: ', year1, month1, date1)
            print('End Date: ', year2, month2, date2)

        #-------------------------------------
        #Creates [Investing] Window + Page
            
        #-------------------------------------
        #Opens new sub window that allows user to invest money (from balance)
        #into defined stock at the live price
        #Money made is "simulated" as if the user invested at the open price since there is no
        #simple manner to acquire and update current stock information to find the actual gain
        def Invest(price):
            #price is price of current stock
            global tickerList, priceList
            global stockFg, lineC, arrow

            x=tickerEntry.get() #stores current name of viewed ticker

            #destroys an existing investing window if one is open
            if self.open:
                try:
                    self.r.destroy()
                #In case client closes page first (TCLerror is not supported)
                except Exception:
                    pass

            self.open = True #sets variable to show the invest page was opened

            #Create new investing window    
            self.r = tk.Tk()
            self.r.title("Invest")
            self.r.wm_iconbitmap('favicon.ico')#sets app icon 
            
            #Creates actual stock page frame (create first to be ontop)
            investFrame = tk.Frame(self.r, width = 400, height = 400, bg = FRA_BG)
            investFrame.pack()

            #Creates top label to show current balance
            Binst = tk.Label(investFrame, text = 'Balance', bg=FRA_BG, fg = 'darkgreen', font = (MAIN_FONT, 8))
            Binst.pack()
            BLabel = tk.Label(investFrame, text = '$' + str(round(balance,2)), bg=FRA_BG, fg = FRA_FG, font = (MAIN_FONT, 20, "bold"))
            BLabel.pack()
            
            
            #Creates middle label to show current price of shares to be bought
            #according to slider position
            Pinst = tk.Label(investFrame, text = 'Shares Price', bg=FRA_BG, fg = 'darkgreen', font = (MAIN_FONT, 8))
            Pinst.pack()
            PLabel = tk.Label(investFrame, text = '$' + '0', bg=FRA_BG, fg = FRA_FG, font = (MAIN_FONT, 20))
            PLabel.pack()
            
            #Creates scale bar and displays its value to represent
            #amount of shares to buy
            scalevar = tk.IntVar()
            scalevar.set(0)
                
            #Creates shares label to display number of shares to be bought
            #according to slider
            sharesinst = tk.Label(investFrame, text = 'Number of Shares', bg=FRA_BG, fg = 'darkgreen', font = (MAIN_FONT, 8))
            sharesinst.pack()
            shares = tk.Label(investFrame, textvariable=scalevar, bg=FRA_BG, fg = FRA_FG, font = (MAIN_FONT, 20))
            shares.pack()

            #Updates PLabel
            def showP(x):
                PLabel['text'] = '$' + str(round(x,2))
            
            #Creates slider to select and show number shares to buy and shows their price
            PLabelPrice = scalevar.get()

            slidStock = tk.Scale(investFrame, from_=0, to_=100, length=394, variable = scalevar, orient="horizontal", bg=FRA_BG,
                              command=lambda PLabelPrice: showP(int(PLabelPrice)*price))
            slidStock.pack()
            
            #Function that will show currently owned stocks, their price bought at
            #and how much money made
            def show():
                #Creates second frame to put stock info on
                self.investFrame2 = tk.Frame(self.r, width = 400, height = 50, bg = FRA_BG)
                self.investFrame2.pack()

                #Creates 2 lists to hold required frames and buttons for
                #each stock info frame (each ticker will have one - according to ticker and price lists)
                frameList=[]
                buttonList=[]

                #Creates the required number of variable names for frames and buttons
                for i in range(len(tickerList)):
                    frameList.append('stockFrame' + str(i))
                    buttonList.append('stockB' + str(i))
                    
                #Creates and displays the stock info
                for i in frameList:
                    #Creates an actual frame under the name of each item in frameList
                    frame = i
                    frame = tk.Frame(self.investFrame2, relief = 'groove', bd=3, width = 400, height = 50, bg = NAV_COL)
                    frame.pack()

                    #Calls API for each share bought to display price and money made
                    x = tickerList[frameList.index(i)]
                    
                    table = si.get_quote_table(x)
                    opnP = table['Open']
                    pclP = table['Previous Close']

                    netPrise = opnP - pclP
                    prcntrise = (netPrise/pclP)*10

                    #Sets colour of net gain to red(loss) or green(gain)
                    if netPrise >= 0:
                        stockFg = 'green'
                        lineC = 'g'
                        arrow = '↑'
                    else:
                        stockFg = 'red'
                        lineC = 'r'
                        arrow = '↓'    
                        

                    #Creates the stock label showing the ticker, price the shares were bought at
                    sL = tk.Label(frame, text = tickerList[frameList.index(i)].upper() + " " + str(priceList[frameList.index(i)]), bg = NAV_COL, fg='white', font = (MAIN_FONT, 8))
                    sL.place(relx=0.2, rely=0.5, anchor = 'center')

                    #Creates the net stock profit label to place (different label since needs colour)
                    sP = tk.Label(frame, text = '$' + str(round(priceList[frameList.index(i)]*prcntrise, 2)) + arrow , bg = NAV_COL, fg=stockFg, font = (MAIN_FONT, 8))
                    sP.place(relx=0.6, rely=0.5, anchor = 'center')


                    #Creates unique sell button (with unique sell() call parameter pertaining to stock it is
                    #associated with) for each button in button list
                    button = buttonList[frameList.index(i)]

                    #must use i=i to save the frame (and its index position) at the time the
                    #button was created (so we'll have buttons 0 to n and not just all n)
                    button = ttk.Button(frame, text = "Sell", command=lambda i=i: sell(frameList.index(i))) #i=i to store i at the time
                    button.place(relx=0.8, rely=0.5, anchor = 'center')

            #New function that will sell the shares of the ticker it is
            #associated with upon sell button press
            def sell(x):
                print(x)
                global balance

                table = si.get_quote_table(tickerList[x])
                
                #Creates a sum variable according to the price the shares were bought
                #at in addition to net profit
                summ = priceList[x] + priceList[x]*((table['Open']-table['Previous Close'])/table['Previous Close'])
                
                #Adds the sum to the balance value
                balance += summ
                
                #updates the balance label
                BLabel['text'] = '$' + str(round(balance,2))

                #removes removed stock ticker and price from appropriate lists
                tickerList.remove(tickerList[x])
                priceList.remove(priceList[x])

                #destroys stock info frame and calls show again to update and register changes
                #(more efficient than updating the whole r window)
                self.investFrame2.destroy()
                show()

            #Calls show from r window startup to display currently owned shares
            #from load data (if any).
            show()
        


            #Trans function to show bought stock, amount made and update balance
            def Trans(y):
                global balance
                global stocksDict
                global tickerList, priceList
    
                    
                #Buys stock if balance sufficient and if more than 0 shares bought
                if slidStock.get()*price <= y and slidStock.get()>0:

                    #Updates balance value
                    balance -= slidStock.get()*price
                    #Updates balance on label value
                    BLabel['text'] = '$' + str(round(balance,2))

                    #stores stock and share price in 2 seperate lists to
                    #save and access data

                    #if the ticker is already listed, won't add a new object in the list,
                    #rather just add the value to the current pricelist value at the appropriate
                    #position
                    if x in tickerList:
                        ticker = tickerList.index(x) #stores the position of ticker in tickerlist
                        iPrice = priceList[ticker] #old price

                        #updates to new price at appropriate position in pricelist
                        fPrice = round(iPrice + slidStock.get()*price,2) 
                        priceList[ticker] = fPrice

                    #else creates new objects in both ticker and price lists at the end    
                    else:
                        tickerList.append(x)
                        priceList.append(round(slidStock.get()*price,2))

                    #same as above to update the stock info
                    self.investFrame2.destroy()
                    show()

                #Can't buy without sufficient balance    
                else:
                    print("Insufficient Funds!")
                    
                print(tickerList, priceList)

            #Upon save button press, will save current balance value and ticker/price lists
            #for stock info
            def Save():
                global uname, tickerList, priceList

                #Saves info under unique file pertaining to username and password as the name
                #(if already there will open it, else will create one)
                f=open(uname + pword+ ".txt", "w+")
                f.write(str(round(balance,2))) #stores balance value
                f.write('\n') #skips to new line

                #for each item in ticker list, store it and its value beside it (each ticker
                #and its price are in the same index position in their according lists)
                for i in range(len(tickerList)):
                    f.write(tickerList[i] + " " + str(priceList[i]))
                    f.write('\n')
                
                f.close

    
            #Button to confirm purchase of shares
            iB = ttk.Button(investFrame, text = "Confirm", command=lambda: Trans(balance))
            iB.pack(pady=10)

            #Button to save current portfolio info
            saveB = ttk.Button(investFrame, text = "Save Portfolio", command=lambda: Save())
            saveB.pack()

        #-------------------------------------
        #Creates [Details] Window + Page
            
        #-------------------------------------
        #Displays further details on selected stock(x-table, y-stock ticker)
        def Details(x, y):
            #Checks if this is a repeated tab, in that case, destroy the repeat window.
            if self.tickerNameD == y.upper():
                try:
                    self.d.destroy()
                #In case client closes page first (TCLerror is not supported)
                except Exception:
                    pass
                
            #Creates new window with the "Ticker - More Info" Name
            self.d = tk.Tk()
            self.d.title("Stock Details")
            self.d.wm_iconbitmap('favicon.ico')#sets app icon 

            #Creates details frame
            detailFrame = tk.Frame(self.d, width = 400, height = 400, bg = NAV_COL)
            detailFrame.pack()

            self.tickerNameD = y.upper()
            #Places stock ticker as title label
            titleL = tk.Label(detailFrame, text = y.upper(), bg = NAV_COL, fg='light green', font = (MAIN_FONT, 15))
            titleL.pack()

            #Displays the additional information from the yahoo API table
            for item in x:
                
                infoL = tk.Label(detailFrame, text= item + " :  " + str(x[item]), bg = NAV_COL, fg = 'white', font = (MAIN_FONT, 10), anchor='w')
                infoL.pack(pady=3, fill = 'x')


                
        #---------------------------------
        #Stock Graphing onto matplot graph
                
        #---------------------------------
        def pressPlot(x):
            global stockFg, lineC, arrow

            #Updates UI theme
            refresh()

            #Calls yahoo finance API (slow) to acquire current live stock data
            def acquireData(x):
                global livP, table, lineC
                #Getting stock open price, live price and %netrise
                livP = si.get_live_price(x) #not very live 
                table = si.get_quote_table(x)
                opnP = table['Open']
                pclP = table['Previous Close']

                netPrise = opnP - pclP
                prcntrise = (netPrise/pclP)*100
                
                print("Open {0}, Previous Close {1}, Current {2}" .format(opnP, pclP, round(livP,2)))

                #Sets colour of net gain to red(loss) or green(gain)
                if netPrise >= 0:
                    stockFg = 'green'
                    lineC = 'g'
                    arrow = '↑'
                else:
                    stockFg = 'red'
                    lineC = 'r'
                    arrow = '↓'    
                    
                #destroys any existing toolbars or labels if they already existed
                #prior to a new plot
                if self.tool:
                    self.tickerPriceL.destroy()
                    self.tickerRiseL.destroy()
                    self.tickerprcntL.destroy()
                    self.tickerTitleL.destroy()

                #Plots ticker and ticker Price Live
                self.tickerPrice = round(livP, 2)
                self.tickerPriceL = tk.Label(stockFrame, text=str(self.tickerPrice) + ' USD', font=(MAIN_FONT, 15), bg = FRA_BG, fg = 'white') 
                self.tickerPriceL.place(relx=0.41, rely=0.81, anchor='n')

                self.tickerRiseL = tk.Label(stockFrame, text=round(netPrise, 2), font=(MAIN_FONT, 10, "bold"), bg = FRA_BG, fg = stockFg)
                self.tickerRiseL.place(relx=0.05, rely=0.875, anchor='nw')

                self.tickerprcntL = tk.Label(stockFrame, text='(' + str(round(prcntrise, 2)) + '%) ' + arrow, font=(MAIN_FONT, 10, "bold"), bg = FRA_BG, fg = stockFg)
                self.tickerprcntL.place(relx=0.13, rely=0.875, anchor='nw')

                self.tickerName = x.upper()                             
                self.tickerTitleL = tk.Label(stockFrame, text=self.tickerName, font=(MAIN_FONT, 25), bg = FRA_BG, fg = 'white') 
                self.tickerTitleL.place(relx=0.05, rely=0.8, anchor='nw')
                stockPlot(x, livP, table, lineC)
                

            #Plots actual stock graph from panda stock database (and creates
            #investing button - passes live price as y) and (creates details tab - passes table as z)
            #linC is for plot colour
            def stockPlot(x, livy, tablez, linC):
                
                #Updates label theme incase of settings change
                self.tickerPriceL.configure(bg = FRA_BG, fg = FRA_FG)
                self.tickerRiseL.configure(bg = FRA_BG)
                self.tickerprcntL.configure(bg = FRA_BG)
                self.tickerTitleL.configure(bg = FRA_BG, fg = FRA_FG)
                
                #Plotting the graph of given stock (Ticker)
                pt.style.use("ggplot")
                start = dt.datetime(year1, month1, date1) #Start date, xi on plot
                end = dt.datetime(year2, month2, date2) #End date as today,xf on plot

                #Creates button which opens window for allowing investing
                self.investB = ttk.Button(stockFrame, text="Invest",
                            command=lambda: Invest(livy))
                self.investB.place(relx=0.75, rely=0.938, anchor='n')

                #Creates button which opens window for displaying additional information
                self.infoB = ttk.Button(stockFrame, text="Detailed",
                            command=lambda : Details(tablez, x))
                self.infoB.place(relx=0.75, rely=0.878, anchor='n')

                #Displays user info as logged in (must be in function and not load up, since load up runs at startup of app
                #before a username has been entered)
                logName = tk.Label(stockFrame, text="Logged in as\n " + uname, font=(MAIN_FONT, 15), bg = FRA_BG, fg = '#E8E8E8')
                logName.place(relx=0.75, rely=0.77, anchor='n')


                #Acquires data of given stock (ticker) from
                #Yahoo Finance API
                df = web.get_data_yahoo(str(x), start, end)
                
                #Plots given data, with identifier "Adj Close" on axes
                df["Adj Close"].plot()
                
                #Prints title for Stock graph
                print(x.upper(), "stock price from " +str(start) + " to " + str(end))

                #Graph styling on size
                f = Figure(figsize=(5, 4), dpi=100)
                a = f.add_subplot(111)

                #Makes plot visible on select frame
                f.patch.set_facecolor(FRA_BG)           #sets AXES colour
                a.patch.set_facecolor('xkcd:grey')      #sets actual PLOT colour
                a.set_title(str(x.upper()) + " stock price from " + str(year1) + " " + str(month1) + " " + str(date1) + " \nto "
                            + str(year2) + " " + str(month2) + " " +  str(date2), color=FRA_FG)
                a.set_xlabel('Date')    #sets x axis label to "date"
                a.set_ylabel('Price($)')#sets y axis label to "price"
                a.plot(df["Adj Close"], linC)

    
                #Allocates canvas area to display graph (embeds mtplot graph
                #using FigureCanvasTkAgg function
                canvas = FigureCanvasTkAgg(f, stockFrame)
                canvas.draw()
                canvas.get_tk_widget().place(relx=0.5, rely=0.9, anchor = 'n')
                canvas._tkcanvas.place(relx=0.5, rely=0.1, anchor="n")

                #destroys any existing toolbars
                if self.tool:
                    self.toolbar.destroy()
                    self.tool=False

                #Creates toolbar to manipulate stock graph
                self.toolbar = NavigationToolbar2Tk(canvas, self)
                self.toolbar.configure(bg=NAV_COL)
                self.toolbar.update()
                self.tool=True #holds if a previous stock was viewed

                #destroys invest frame upon changing stocks (avoid confusion)
                if self.open:
                    try:
                        self.r.destroy()
                        #self.d.destroy() #if want to destroy details page, kept for comparing
                        self.open = False
                    #In case client closes page first (TCLerror is not supported)
                    except Exception:
                        pass
                    
                #destroys warning label upon viewing valid stock.
                if self.i:
                    self.LabelI.destroy()
                    self.i=False

            #Code starts here, upon plotting - checks if the entry is just a time change, in that
            #case don't acquire API data, just plot again. Else, acquire data then plot.
            try:
                if self.tool and x.upper() == self.tickerName:
                    global livP, table, lineC
                    print()
                    print('Loading... Plotting...')
                    stockPlot(x, livP, table, lineC)
                    
                else:
                    print()
                    print('Loading... Fetching stock data...')
                    acquireData(x)
                
                
                #Exception handling in case that invalid ticker is entered
            except ValueError:
                #Creates error instructions label to display
                if self.i == False:
                    self.LabelI = tk.Label(stockFrame, text="Invalid ticker or viewing date, try again - must be NYSE.", bg = FRA_BG, fg="red", font = (MAIN_FONT, 7, 'bold'))
                    self.LabelI.place(relx=0.3, rely=0.91, anchor="n")
                    self.i = True #shows error was shown

                #In case of error, destroy buttons since no valid ticker entered
                if self.tool:
                    self.infoB.destroy()
                    self.investB.destroy()
                print("Invalid name or viewing date, try again.")

                
                
              
#Runs the app, sets main title, logo and keeps window open
app = Finenhance()
app.wm_title('Finenhance')      #sets app window title
app.wm_iconbitmap('favicon.ico')#sets app icon 
app.mainloop()
