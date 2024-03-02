# importing GUI modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# importing directory path module
from pathlib import Path
# importing date module
import datetime as dt
# importing csv module
import csv
import os
import pandas


#Set window settings
root = Tk()
root.title('Utility Billing Payment Agent System')
root.iconbitmap()
root.geometry("450x400")
root.resizable(False, False)


# Create clear event function
def btn_clear():
    Receiptnum_Entry.delete(0, END)
    Receiptnum_Entry.config(state="disabled")
    accnum_Entry.delete(0, END)
    Receiptnum_Entry.insert(END, f"{dt.datetime.now():%Y%m%d%H%M%S}")
    Receiptnum_Entry.config(state="disabled")
    Date_Entry.insert(END, f"{dt.datetime.now():%b %d %Y}")
    Date_Entry.config(state="disabled")
    BillingCompany_DropDown.delete(0, END)
    CustomerFirstname_Entry.delete(0, END)
    CustomerLastname_Entry.delete(0, END)
    PaymentMethod_DropDown.delete(0, END)
    PayAmount_Entry.delete(0, END)
    PayAmount_Entry.insert(END, '0.00')
    Tendered_Entry.delete(0, END)
    Tendered_Entry.insert(END, '0.00')
    Tendered_Entry.config(state="disabled")
    Change_Entry.delete(0, END)
    Change_Entry.insert(END, '0.00')
    Change_Entry.config(state="disabled")

    accnum_Entry.focus_set()

# Create cancel event function
def btn_cancel():
    btn_clear()

# Create save event function
def btn_save():


    saveError = False
    saveError = Validate()
    if saveError == True:
        return
    else:
        saveError = False
        saveError = ChangeCalculation()
        if saveError == True:
            return
        else:
            myFile = BillingCompany_DropDown.get() + f"_BillPayLog-{dt.datetime.now():%Y%m%d}" + ".CSV"
            #FileWriter(myFile)
            #FileWriter(f"BillPayment_Log-{dt.datetime.now():%Y%m%d}" + ".CSV"
            PrintReceipt()


    #btn_clear()


def Validate():
    vErr = False
    if len(accnum_Entry.get()) == 0:
        messagebox.showerror("Validation Error", "Please enter an Account number!")
        accnum_Entry.focus_set()
        vErr = True


    try:
        int(accnum_Entry.get())
        vErr = False
        #currency/float value entered
    except ValueError:
        messagebox.showerror("Validation Error", "Please enter a number value in account#!")
        accnum_Entry.focus_set()
        vErr = True

    if len(BillingCompany_DropDown.get()) == 0:
        messagebox.showerror("Validation Error", "Please select a billing company!")
        BillingCompany_DropDown.focus_set()
        vErr = True

    if len(CustomerFirstname_Entry.get()) == 0:
        messagebox.showerror("Validation Error", "Please enter customer's first name!")
        CustomerFirstname_Entry.focus_set()
        vErr = True

    if len(CustomerLastname_Entry.get()) == 0:
        messagebox.showerror("Validation Error", "Please enter customer's last name!")
        CustomerLastname_Entry.focus_set()
        vErr = True

    if len(PaymentMethod_DropDown.get()) == 0:
        messagebox.showerror("Validation Error", "Please select a payment method!")
        PaymentMethod_DropDown.focus_set()
        vErr = True

    if (PaymentMethod_DropDown.get() == "Cash"):
        if len(Tendered_Entry.get()) == 0:
            messagebox.showerror("Validation Error", "Please enter cash amount tendered!")
            Tendered_Entry.focus_set()
            vErr = True

    if len(PayAmount_Entry.get()) == 0:
        messagebox.showerror("Validation Error", "Please enter customer's payment amount!")
        PayAmount_Entry.focus_set()
        vErr = True

    try:
        float(PayAmount_Entry.get())
        vErr = False
        #currency/float value entered
    except ValueError:
        messagebox.showerror("Validation Error", "Please enter a currency/float value in payment amount!")
        PayAmount_Entry.focus_set()
        vErr = True

    varAmount = float(PayAmount_Entry.get())
    PayAmount_Entry.delete(0, END)
    PayAmount_Entry.insert(END, '%0.2f' % varAmount)

    if len(Tendered_Entry.get()) == 0:
        messagebox.showerror("Validation Error", "Please enter customer's tendered amount!")
        Tendered_Entry.focus_set()
        vErr = True

    try:
        float(Tendered_Entry.get())
        vErr = False
        #currency/float value entered
    except ValueError:
        messagebox.showerror("Validation Error", "Please enter a currency/float value in tendered amount!")
        Tendered_Entry.focus_set()
        vErr = True

    varAmount = float(Tendered_Entry.get())
    Tendered_Entry.delete(0, END)
    Tendered_Entry.insert(END, '%0.2f' % varAmount)

    return vErr

def ChangeCalculation():
    err = False
    varAmount = float(PayAmount_Entry.get())
    varTender = float(Tendered_Entry.get())
    varChange = float(Change_Entry.get())
    if varTender >= varAmount:
        varChange = varTender - varAmount

        print(f" Amount:  {varAmount}")
        print(f" Tender:  {varTender}")
        print(f" Change:  {varChange}")

        #varAmount = float(PayAmount_Entry.get())
        PayAmount_Entry.delete(0, END)
        PayAmount_Entry.insert(END, '%0.2f' % varAmount)

        #varTender = float(Tendered_Entry.get())
        Tendered_Entry.delete(0, END)
        Tendered_Entry.insert(END, '%0.2f' % varTender)

        #varChange = float(Change_Entry.get())
        Change_Entry.config(state="normal")
        Change_Entry.delete(0, END)
        Change_Entry.insert(END, '%0.2f' % varChange)
        Change_Entry.config(state="disabled")
        print(" varChange:  ", '%0.2f' % float(Change_Entry.get()))

    else:
        messagebox.showerror("Calculation Error", "Cash tendered cannot be less than payment amount")
        err = True


    return err

def onChange_PayAmount_Entry():
    if len(PayAmount_Entry.get()) == 0:
        messagebox.showerror("Validation Error", "Please enter customer's payment amount!")
        PayAmount_Entry.focus_set()
        return

    try:
        float(PayAmount_Entry.get())
        #currency/float value entered
    except ValueError:
        messagebox.showerror("Validation Error", "Please enter a currency/float value in payment amount!")
        PayAmount_Entry.focus_set()
        return

    varAmount = float(PayAmount_Entry.get())
    PayAmount_Entry.delete(0, END)
    PayAmount_Entry.insert(END, '%0.2f' % varAmount)


# Create report window
def btn_report():
    filename = f"BillPayment_Log-{dt.datetime.now():%Y%m%d}" + ".LOG"


    RPTwin = Toplevel(root)
    RPTwin.title("Print Report")
    RPTwin.geometry("1100x480")

    textReport = Text(RPTwin, width=150, height=30, font=("New Courier", 12))
    textReport.pack(pady=20)

    rf = open(filename, "r")
    #f_Report = rf.read()
    rf = csv.reader(rf)
    for row in rf:
        print('{:<20}  {:<15}  {:<20} {:<25} {:<15}  {:<15}  {:<20} {:>7}'.format(*row))
        textReport.insert(INSERT,'{:<20}  {:<15}  {:<20} {:<25} {:<15}  {:<15}  {:<20} {:>7}\n'.format(*row))

    #column_names = ["Receipt #", "Account #", "Payment Date", "Company", "Fname", "Lname", "Method", "Amount"]
    #df = pandas.read_csv(filename, names=column_names)
    #df = pandas.read_csv('hrdata.csv', index_col='Name')
    #print(df)

    #textReport.delete(0, END)
    #textReport.insert(END, df)
    #rf.close()


def PrintReceipt():

    filename = "receipt.txt"
    path = Path(filename)
    # check if file already exist and determine the method of opening file
    if path.is_file():
        os.remove(filename)

    # create file to write to
    f = open(filename, "w")

    f.write("\n--------------------------------------------------------------------------------------")
    f.write("\n          Utility Billing Payment Agent System                  ")
    f.write("\n--------------------------------------------------------------------------------------")
    f.write("\n-------------------------Bill Payment Receipt-------------------------------")
    f.write("\n")
    f.write("\nReceipt#:\t\t\t\t" + Receiptnum_Entry.get())
    f.write("\nReceipt Date#:\t\t\t\t" + Date_Entry.get())
    f.write("\nAccount#:\t\t\t\t" + accnum_Entry.get())
    f.write("\nCompany:\t\t\t\t" + BillingCompany_DropDown.get())
    f.write("\nCustomer's Firstname:\t\t\t\t" + CustomerFirstname_Entry.get())
    f.write("\nCustomer's Lastname:\t\t\t\t" + CustomerLastname_Entry.get())
    f.write("\nPayment Method:\t\t\t\t" + PaymentMethod_DropDown.get())
    f.write("\n")
    f.write("\n--------------------------------------------------------------------------------------")
    f.write("\nPaid:\t\t\t\t" + PayAmount_Entry.get())
    f.write("\nCash Tendered:\t\t\t\t" + Tendered_Entry.get())
    f.write("\nChange:\t\t\t\t" + Change_Entry.get())


    f.write("\n--------------------------------------------------------------------------------------")
    f.write("\n---------------Thank You Please Come Again!-------------------------\n\n")
    f.close()

    win = Toplevel(root)
    win.title("Print Receipt")
    win.geometry("600x380")

    textReceipt = Text(win,width=70,height=20,font=("New Courier",10))
    textReceipt.pack(pady=20)

    tf = open(filename, "r")
    f_receipt = tf.read()

    textReceipt.insert(END, f_receipt)
    tf.close()





# Create exit windows event function
def btn_exit():
    root.destroy()


def PaymentMethod_DropDown_onChange(event):

    #messagebox.showinfo("onChange Event")
    if (PaymentMethod_DropDown.get() == "Cash"):
        Tendered_Entry.config(state="normal")
        Tendered_Entry.delete(0, END)
        Tendered_Entry.insert(END, '0.00')
        PayAmount_Entry.focus_set()
    else:
        Tendered_Entry.config(state="disabled")
        Tendered_Entry.delete(0, END)
        Tendered_Entry.insert(END, '0.00')


def disable_event():
   pass

def FileWriter(filename):
    path = Path(filename)
    # check if file already exist and determine the method of opening file
    if path.is_file():
        # write new record to file
        f = open(filename, "a")
        f.write(f"{Receiptnum_Entry.get()},{accnum_Entry.get()},{Date_Entry.get()},{BillingCompany_DropDown.get()},{CustomerFirstname_Entry.get()},{CustomerLastname_Entry.get()},{PaymentMethod_DropDown.get()},{PayAmount_Entry.get()}")
        f.write("\n")
        f.close()

        #print(f'The file {path_to_file} exists')
    else:
        # create file to write to
        f = open(filename, "w")
        f.write("ReceiptNumber,AccountNumber,PaymentDate,BillingCompany,CustomerFname,CustomerLname,PaymentMethod,Amount\n")
        f.write(f"{Receiptnum_Entry.get()},{accnum_Entry.get()},{Date_Entry.get()},{BillingCompany_DropDown.get()},{CustomerFirstname_Entry.get()},{CustomerLastname_Entry.get()},{PaymentMethod_DropDown.get()},{PayAmount_Entry.get()}")
        f.write("\n")
        f.close()

def FileReader(filename):
    path = Path(filename)
    # check if file already exist, read file, or send error message to user
    if path.is_file():
        # read file
        print(f'The file {path_to_file} exists')
    else:
        # send message to user
        print(f'The file {path_to_file} does not exist')




# Setup for labels and fields with variables
Receiptnum_label = Label(root, text='Receipt #: ')
Receiptnum_label.pack()
Receiptnum_label.place(x=1, y=20)

Receiptnum_Entry = Entry(root, width=20)
Receiptnum_Entry.place(x=200, y=20)
Receiptnum_Entry.insert(END, f"{dt.datetime.now():%Y%m%d%H%M%S}")
Receiptnum_Entry.config(state="disabled")

accnum_label = Label(root, text='Account #: ')
accnum_label.place(x=1, y=50)

accnum_Entry = Entry(root, width=20)
accnum_Entry.place(x=200, y=50)

Date_label = Label(root, text='Date: ')
Date_label.place(x=1, y=80)

Date_Entry = Entry(root, width=15)
Date_Entry.place(x=200, y=80)
Date_Entry.insert(END, f"{dt.datetime.now():%b %d %Y}")
Date_Entry.config(state="disabled")


BillingCompany_label = Label(root, text='Billing Company: ')
BillingCompany_label.place(x=1, y=120)

options = [
    "Rogers",
    "Telus",
    "Electricity",
    "Gas"]

BillingCompany_DropDown = ttk.Combobox(root, value=options)
#BillingCompany_DropDown.current(0)
BillingCompany_DropDown.place(x=200, y=120)

CustomerFirstname_label = Label(root, text='Customer Firstname: ')
CustomerFirstname_label.place(x=1, y=150)

CustomerFirstname_Entry = Entry(root, width=20)
CustomerFirstname_Entry.place(x=200, y=150)

CustomerLastname_label = Label(root, text='Customer Lastname: ')
CustomerLastname_label.place(x=1, y=180)

CustomerLastname_Entry = Entry(root, width=20)
CustomerLastname_Entry.place(x=200, y=180)

PaymentMethod_label = Label(root, text='Payment Method: ')
PaymentMethod_label.place(x=1, y=210)

pay_options = [
    "Cash",
    "Debit Card",
    "Credit Card",
    "Credit Note"]

PaymentMethod_DropDown = ttk.Combobox(root, value=pay_options)
PaymentMethod_DropDown.place(x=200, y=210)
PaymentMethod_DropDown.bind("<<ComboboxSelected>>", PaymentMethod_DropDown_onChange)

PayAmount_label = Label(root, text='Payment Amount:                              $')
PayAmount_label.place(x=1, y=240)

PayAmount_Entry = Entry(root, width=20, justify=RIGHT)
PayAmount_Entry.insert(END, '0.00')
PayAmount_Entry.place(x=200, y=240)

Tendered_label = Label(root, text='Tendered:                                             $')
Tendered_label.place(x=1, y=270)

Tendered_Entry = Entry(root, width=20, justify=RIGHT)
Tendered_Entry.insert(END, '0.00')
Tendered_Entry.place(x=200, y=270)
Tendered_Entry.config(state="disabled")

Change_label = Label(root, text='Change:                                                $')
Change_label.place(x=1, y=300)

Change_Entry = Entry(root, width=20, justify=RIGHT)
Change_Entry.insert(END, '0.00')
Change_Entry.place(x=200, y=300)
Change_Entry.config(state="disabled")


# Buttons
clear_button = Button(root, text="Clear", justify = CENTER, width=10, height=1, command=btn_clear)
#clear_button.pack()
clear_button.place(x=10, y=350)

cancel_button = Button(root, text="Cancel", justify = CENTER, width=10, height=1, command=btn_cancel)
#cancel_button.pack()
cancel_button.place(x=100, y=350)

save_button = Button(root, text="Save", justify = CENTER, width=10, height=1, command=btn_save)
#save_button.pack()
save_button.place(x=185, y=350)

Report_button = Button(root, text="Report...", justify = CENTER, width=10, height=1, command=btn_report)
Report_button.place(x=275, y=350)

exit_button = Button(root, text="Exit", justify = CENTER, width=10, height=1, command=btn_exit)
exit_button.place(x=360, y=350)

root.protocol("WM_DELETE_WINDOW", disable_event)
root.mainloop()


