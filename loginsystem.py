import tkinter as tk
import tkinter.font
import json
from firebase import firebase

#Create login screen with tkinter
login_screen=tk.Tk()
login_screen.title("Login")
appFont=tkinter.font.Font(family='Calibri', size=12)

#method to kill login screen
def exitProgram():
    login_screen.destroy()

#method to open app
#def access():
    #insert app content later

#method to create registration window
def register():
    register_screen = tk.Toplevel(login_screen)
    register_screen.title("Register an account")

    #method to register a new user
    def registerNewUser():
        fb_app = firebase.FirebaseApplication('https://naamakirja-dea54-default-rtdb.europe-west1.firebasedatabase.app/',None)
        new_username = reg_input_username_field.get()
        new_password = reg_input_password_field.get()
        new_user_data = {'Username': f'{new_username}',
                    'Password': f'{new_password}'
                    }
        print('updated firebase with given info')
        result = fb_app.post('/users', new_user_data, {'print': 'pretty'})

    #widget for registration label
    register_form_label=tk.Label(register_screen, text='Register a new account',
                                font=appFont,bg='blue',height=2,width=30,fg='white')
    register_form_label.grid(row=0, column=0)

    #widget for username label
    reg_username_label=tk.Label(register_screen, text='Enter username', font=appFont,
                        height=2, width=30)
    reg_username_label.grid(row=1, column=0)

    #widget for username input
    reg_input_username_field=tk.Entry(register_screen, bd=5, width=12)
    reg_input_username_field.grid(row=1, column=1)

    #widget for password label
    reg_password_label=tk.Label(register_screen, text='Enter password', font=appFont,
                        height=2, width=30)
    reg_password_label.grid(row=2, column=0)

    #widget for password input
    reg_input_password_field=tk.Entry(register_screen, bd=5, width=12)
    reg_input_password_field.grid(row=2, column=1)

    #button to send registration info to firebase with method 'registerNewUser'
    new_account_button=tk.Button(register_screen, text='Register', font=appFont,
                          command=registerNewUser, height=2, width=30)
    new_account_button.grid(row=3, column=1, sticky=tk.NSEW)

    #button to quit registration window
    exit_button=tk.Button(register_screen, text='Exit', font=appFont, command=register_screen.destroy, bg='bisque',
                      height=1, width=24)
    exit_button.grid(row=4, column=0, sticky=tk.W)

#label to show instructions
form_label=tk.Label(login_screen, text='Log in or register a new account',
                    font=appFont,bg='blue',height=2, width=30, fg='white')
form_label.grid()

#label for username input
username_label=tk.Label(login_screen, text='Enter username', font=appFont,
                        height=2, width=30)
username_label.grid(row=1, column=0)

#input for username login
input_username_field=tk.Entry(login_screen, bd=5, width=12)
input_username_field.grid(row=1, column=1)

#label for password input
password_label=tk.Label(login_screen, text='Enter password', font=appFont,
                        height=2, width=30)
password_label.grid(row=2, column=0)

#input for password login
input_password_field=tk.Entry(login_screen, bd=5, width=12)
input_password_field.grid(row=2, column=1)

#button to send login information and search firebase for match
login_button=tk.Button(login_screen, text='Log in', font=appFont,
                          height=2, width=30)
login_button.grid(row=3, column=0, sticky=tk.NSEW)

#button to open registration window
register_button=tk.Button(login_screen, text='Register', font=appFont,
                          command=register, height=2, width=30)
register_button.grid(row=3, column=1, sticky=tk.NSEW)

#button to shutdown program
exit_button=tk.Button(login_screen, text='Exit', font=appFont, command=exitProgram, bg='bisque',
                      height=1, width=24)
exit_button.grid(row=4, column=0, sticky=tk.W)

#run tkinter mainloop
tk.mainloop()