"""
Created on Thu Jan 25 09:16:27 2024
Author: Jakub Trušina
Name: code_aster_Monitoring_GUI.py
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from code_aster_Monitoring import code_aster_monitoring

open_file = 0   ;   file_auto = 0   ;   print_files = 0   ;   mode = 0

directory_name = "directory: "
file_name_name = "file_name: "
file_number_name = "file_number: "
application_name = "application: "
message_file_name = "message_file: "
probe_position_name = "probe_position: "
update_after_name = "update_after: "

open_file_name = "open_file: "
file_auto_name = "file_auto: "
print_files_name = "print_files: "
mode_name = "mode: "

Unit_name = "Unit: "

user_data = "code_aster_Monitoring_Data/code_aster_Monitoring_User_Data.txt"

def save_user_data(directory, file_name, file_number, application, open_file, file_auto, message_file, probe_position, update_after, print_files, mode, Unit, ):
    with open(user_data, "w") as file:
        directory_all = directory_name + (directory)
        file_name_all = file_name_name + (file_name)
        file_number_all = file_number_name + str(file_number)
        application_all = application_name + (application)
        message_file_all = message_file_name + (message_file)
        probe_position_all = probe_position_name + str(probe_position)
        update_after_all = update_after_name + str(update_after)
        
        open_file_all = open_file_name + str(open_file)
        file_auto_all = file_auto_name + str(file_auto)
        print_files_all = print_files_name + str(print_files)
        mode_all = mode_name + str(mode)
        
        Unit_all = Unit_name + str(Unit)
        
        enterances = [directory_all,
                      file_name_all,
                      file_number_all,
                      application_all,
                      message_file_all,
                      probe_position_all,
                      update_after_all,
                                                                  
                      open_file_all,
                      file_auto_all,
                      print_files_all,
                      mode_all,
                      
                      Unit_all, ]
        
        names = "\n".join(enterances)
        file.write(names)
        return names

def read_user_data():
    try:
        with open(user_data, "r") as file:
            data = file.read()
            return data
    except FileNotFoundError:
        pass
    return ""

def set_open_file(type):
    open_file_var.set(type)
def set_open_file_1(type):
    file_auto_var.set(type)
def set_open_file_2(type):
    print_files_var.set(type)
def set_open_file_3(type):
    mode_var.set(type)

def run_program():
    directory = str(directory_entry.get())
    file_name = str(file_name_entry.get())
    file_number = int(file_number_entry.get())
    application = str(application_entry.get())
    message_file = str(message_file_entry.get())
    probe_position = int(probe_position_entry.get())
    update_after = int(update_after_entry.get())
    
    open_file = int(open_file_var.get())
    file_auto = int(file_auto_var.get())
    print_files = int(print_files_var.get())
    mode = int(mode_var.get())
    
    Unit = Unit_var.get()
    
    names = save_user_data(directory, file_name, file_number, application, open_file, file_auto, message_file, probe_position, update_after, print_files, mode, Unit, )
    # result_label.config(text=names)
    print()
    print(names)
    print()

    code_aster_monitoring(directory,file_name,file_number,open_file,application,file_auto,message_file,probe_position,print_files,mode,Unit)
    
    open_file_var.set(0)
    
    window.after( (update_after*1000) , run_program )
    
def close_window(event=None):
    plt.close("all")
    window.destroy()

# Create the main Tkinter window
window = tk.Tk()
window.title("code_aster_Monitoring")

fnt_size = 13
# fnt = "Comic Sans MS"
# fnt = "Segoe UI"
fnt = "Century Gothic"
# fnt = "Helvetica"
# fnt = "Calibri Light"
# fnt = "Abadi"
# fnt ="Arial"
wdth = 10
pdx = 0
row = 1
directory_label = ttk.Label(window, text="Search directory:", font=(fnt,fnt_size)  )
directory_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
directory_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
directory_entry.grid(row=row, column=1, columnspan=5, sticky="we", padx=pdx, pady=10)

row = row + 1
file_name_label = ttk.Label(window, text="Search file name:", font=(fnt,fnt_size))
file_name_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
file_name_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
file_name_entry.grid(row=row, column=1, sticky="w", padx=pdx, pady=10)

row = row + 1
file_number_label = ttk.Label(window, text="File number:", font=(fnt,fnt_size))
file_number_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
file_number_entry = ttk.Spinbox(window, width=wdth, font=(fnt,fnt_size-3), from_=0, to=100, increment=1)
file_number_entry.grid(row=row, column=1, sticky="w", padx=pdx, pady=10)

update_after_label = ttk.Label(window, text="Update:", font=(fnt,fnt_size))
update_after_label.grid(row=row, column=2, padx=10, pady=10, sticky="we")
update_after_label = ttk.Label(window, text="[s]", font=(fnt,fnt_size))
update_after_label.grid(row=row, column=3, padx=10, pady=10, sticky="w")
update_after_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
update_after_entry.grid(row=row, column=2, sticky="e", padx=10, pady=10)

row = row + 1
application_label = ttk.Label(window, text="Application:", font=(fnt,fnt_size))
application_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
application_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
application_entry.grid(row=row, column=1, columnspan=5, sticky="we", padx=pdx, pady=10)

row = row + 1
message_file_label = ttk.Label(window, text="Message file:", font=(fnt,fnt_size))
message_file_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
message_file_entry = ttk.Entry(window, width=105, font=(fnt,fnt_size-3))
message_file_entry.grid(row=row, column=1, columnspan=5, sticky="we", padx=pdx, pady=10)

# row = row + 1
# probe_position_label = ttk.Label(window, text="Probe column:", font=(fnt,fnt_size))
# probe_position_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
# probe_position_entry = ttk.Entry(window, width=wdth, font=(fnt,fnt_size-3))
# probe_position_entry.grid(row=row, column=1, sticky="w", padx=pdx, pady=10)

row = row + 1
probe_position_label = ttk.Label(window, text="Probe column:", font=(fnt,fnt_size))
probe_position_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
probe_position_entry = ttk.Spinbox(window, width=wdth, font=(fnt,fnt_size-3), from_=-100, to=100, increment=1)
probe_position_entry.grid(row=row, column=1, sticky="w", padx=pdx, pady=10)

row = row + 1
open_file_var = tk.StringVar(value=0)  
constant_radio = ttk.Checkbutton(window, text="Open file", variable=open_file_var)
constant_radio.grid(row=row, column=1, padx=10, pady=10, sticky="we")

file_auto_var = tk.StringVar(value=0) 
constant_radio_1 = ttk.Checkbutton(window, text="Automatic file search", variable=file_auto_var)
constant_radio_1.grid(row=row, column=2, padx=10, pady=10, sticky="we")

print_files_var = tk.StringVar(value=0) 
constant_radio_2 = ttk.Checkbutton(window, text="Print files",  variable=print_files_var)
constant_radio_2.grid(row=row, column=3, padx=10, pady=10, sticky="we")

mode_var = tk.StringVar(value=0)  
constant_radio_3 = ttk.Checkbutton(window, text="Dark Theme", style="Switch.TCheckbutton", variable=mode_var )
constant_radio_3.grid(row=row, column=5, padx=0, pady=10, sticky="w")
constant_radio_4 = ttk.Label(window, text="Light Theme"  )
constant_radio_4.grid(row=row, column=4, padx=0, pady=10, sticky="e")

row = row + 1
Unit_label = tk.Label(window, text="Probe unit:", font=(fnt,fnt_size))
Unit_label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
Unit_var = tk.StringVar(value="[-]")
Unit_combobox = ttk.Combobox(window, textvariable=Unit_var, width=10, values=[ "[-]", "[mm]", "[rad]", "[N]", "[MPa]", ])
Unit_combobox.grid(row=row, column=1, sticky="w", padx=pdx, pady=10)

# Button 
row = row + 1
style = ttk.Style()
# style.configure('TButton', background='#1171FF', foreground='black' , font=(fnt,fnt_size))
run_button = ttk.Button(window, text="Update", width=30, style="Accent.TButton", command=lambda: run_program())
run_button.grid(row=row, column=2, columnspan=2, sticky="we", padx=pdx, pady=10)
# style.theme_use('vista')
# style.map('TButton', background=[('active', '#1171FF')])

row = row + 1
result_label = tk.Label(window, text="")
result_label.grid(row=row, column=0, columnspan=3, padx=10, pady=10)

window.bind("<Return>", lambda event: run_program())
window.bind("<Escape>", close_window)
window.protocol("WM_DELETE_WINDOW", close_window)
# window.geometry("900x580")

class RightClicker:
    def __init__(self, e):
        menu = tk.Menu(None, tearoff=0, takefocus=0)
        commands = ["Cut", "Copy", "Paste", "Delete"]
        for cmd in commands:
            menu.add_command(label=cmd, font=(fnt,fnt_size-2), command=lambda cmd=cmd: self.execute_command(e, cmd))
        menu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")
    def execute_command(self, e, cmd):
        if cmd == "Delete":
            e.widget.delete("sel.first", "sel.last")
        else:
            e.widget.event_generate(f'<<{cmd}>>')

directory_entry.bind("<Button-3>", RightClicker)
file_name_entry.bind("<Button-3>", RightClicker)
file_number_entry.bind("<Button-3>", RightClicker)
application_entry.bind("<Button-3>", RightClicker)
message_file_entry.bind("<Button-3>", RightClicker)
probe_position_entry.bind("<Button-3>", RightClicker)

# Load saved user info from file
saved_data = read_user_data()
lines = saved_data.split("\n")
for line in lines:
    if line.startswith("directory: "):
        directory_entry.insert(0, line[len(directory_name):])
        
    elif line.startswith("file_name: "):
        file_name_entry.insert(0, line[len(file_name_name):])
        
    elif line.startswith("file_number: "):
        file_number_entry.insert(0, line[len(file_number_name):])

    elif line.startswith("application: "):
        application_entry.insert(0, line[len(application_name):])
        
    elif line.startswith("message_file: "):
        message_file_entry.insert(0, line[len(message_file_name):])
        
    elif line.startswith("probe_position: "):
        probe_position_entry.insert(0, line[len(probe_position_name):])
    
    elif line.startswith("update_after: "):
        update_after_entry.insert(0, line[len(update_after_name):])
        
    # elif line.startswith("open_file: "):
    #     set_open_file(line[len(open_file_name):])
        
    elif line.startswith("file_auto: "):
        set_open_file_1(line[len(file_auto_name):])

    elif line.startswith("print_files: "):
        set_open_file_2(line[len(print_files_name):])
        
    elif line.startswith("mode: "):
        set_open_file_3(line[len(mode_name):])
        
    elif line.startswith("Unit: "):
        Unit_var.set(line[len(Unit_name):])

window.tk.call("source", "Azure-ttk-theme-main/azure.tcl")
window.tk.call("set_theme", "dark")
window.mainloop()



















