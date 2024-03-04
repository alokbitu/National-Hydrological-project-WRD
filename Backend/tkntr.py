import csv
import os
import shutil
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd
import datetime

#from PIL import ImageTk
from tkcalendar import DateEntry

# Create the Tkinter window
window = tk.Tk()
window.title("Sunjray Infosystems")
window.geometry("800x980")

# Site information
site_name = "Salia Dam"
site_id = "ORSW_230601_130700_31801040"
name = "Sunjray Infosystem"

# Read the file
file_contents = pd.read_excel('data.xlsx')
all_rows = file_contents.values.tolist()

# Additional data
current_date_time = datetime.datetime.now().strftime("%d-%m-%Y / %H:%M:%S")
solar_voltage = all_rows[1][1]
battery_voltage = all_rows[2][1]
water_depth = all_rows[3][1]
hourly_rainfall = all_rows[4][1]
daily_rainfall = all_rows[5][1]

with open("current_rainfall.txt", "r")as file:
    current_rainfall = file.read().strip()
    file.close()

# Header
header_frame = tk.Frame(window, bg="#34c9eb")
header_frame.pack(fill="x")

'''# Logo
logo_image = Image.open("sunjray _logo.png")
logo_image = logo_image.resize((90, 60), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(header_frame, image=logo_photo, bg="#34c9eb", anchor="w")
logo_label.grid(row=0, column=0, padx=2, pady=2)

# Site Name Label
site_name_label = tk.Label(header_frame, text="Site Name:" + site_name, font=("Arial", 22, "bold"), bg="#34c9eb", fg="black")
site_name_label.grid(side ="top", padx=5, pady=5)

# Site ID Label
site_id_label = tk.Label(header_frame, text="Site ID:" + site_id, font=("Arial", 20, "bold"), bg="#34c9eb", fg="black")
site_id_label.grid(side="top", padx=5, pady=5)

name_label = tk.Label(header_frame, text="" + name, font=("Arial", 20, "bold"), bg="#34c9eb", fg="blue")
name_label.pack(side="top", padx=5, pady=5)'''

site_name_label = tk.Label(header_frame, text="Site Name:" + site_name, font=("Arial", 23, "bold"), bg="#34c9eb",
                           fg="black")
site_name_label.pack(side="top", padx=3, pady=3)

site_id_label = tk.Label(header_frame, text="Site ID:" + site_id, font=("Arial", 22, "bold"), bg="#34c9eb", fg="black")
site_id_label.pack(side="top", padx=3, pady=3)

name_label = tk.Label(header_frame, text="" + name, font=("Arial", 20, "bold"), bg="#34c9eb", fg="blue")
name_label.pack(side="top", padx=3, pady=3)

# Body
body_frame = tk.Frame(window, bg="#cbedf2")
body_frame.pack(padx=10, pady=10)

# Stack to store previous pages
previous_pages = []


def show_initial_content():
    for widget in body_frame.winfo_children():
        widget.destroy()

    date_time_label = tk.Label(body_frame, text="Date & Time: " + current_date_time, font=("Arial", 26), bg="#cbedf2")
    date_time_label.pack(anchor="w")

    solar_voltage_label = tk.Label(body_frame, text="Solar Voltage: " + str(solar_voltage) + "Volt", font=("Arial", 26),
                                   bg="#cbedf2")
    solar_voltage_label.pack(anchor="w")

    battery_voltage_label = tk.Label(body_frame, text="Battery Voltage: " + str(battery_voltage) + "Volt",
                                     font=("Arial", 26), bg="#cbedf2")
    battery_voltage_label.pack(anchor="w")

    water_depth_label = tk.Label(body_frame, text="Water Depth: " + str(water_depth) + "meter", font=("Arial", 26),
                                 bg="#cbedf2")
    water_depth_label.pack(anchor="w")

    current_rainfall_label = tk.Label(body_frame, text="Current Rainfall:" + str(current_rainfall), font=("Arial", 26),
                                      bg="#cbedf2")
    current_rainfall_label.pack(anchor="w")

    hourly_rainfall_label = tk.Label(body_frame, text="Hourly Rainfall: " + str(hourly_rainfall), font=("Arial", 26),
                                     bg="#cbedf2")
    hourly_rainfall_label.pack(anchor="w")

    daily_rainfall_label = tk.Label(body_frame, text="Daily Rainfall: " + str(daily_rainfall), font=("Arial", 26),
                                     bg="#cbedf2")
    daily_rainfall_label.pack(anchor="w")

    # Add the Main Menu button
    main_menu_button = tk.Button(body_frame, text="Main Menu(+)", command=show_main_menu, font=("Arial", 18, "bold"), bg="#34c9eb", fg="black")
    main_menu_button.pack(side="bottom", pady=10)

    # Add the body and header frames to previous_pages
    previous_pages.append(body_frame)
    previous_pages.append(header_frame)

 # Function to handle keypress event
def on_keypress(event):
    key = event.char
    if key == '+':
        show_main_menu()
# Bind the keypress event to the window
window.bind('<KeyPress>', on_keypress)

def enter_key_pressed(event):
    show_main_menu()

window.bind('<Return>', enter_key_pressed)


def show_main_menu():
    for widget in body_frame.winfo_children():
        widget.destroy()

    # You can customize the main menu content here
    main_menu_label = tk.Label(body_frame, text="Main Menu", font=("Arial", 30, "bold"), bg="#cbedf2")
    main_menu_label.grid(row=0, column=0, columnspan=2, pady=10)


    # Add additional text below the back button
    additional1_text = tk.Label(body_frame, text="Press 1: Configuration", font=("Arial", 26),
                               bg="#cbedf2")
    additional1_text.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
    # Add additional text below the back button
    additional2_text = tk.Label(body_frame, text="Press 2: View Data", font=("Arial", 26),
                               bg="#cbedf2")
    additional2_text.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

    # Add a button to go back to the initial content
    back_button = tk.Button(body_frame, text="Back(-)", command=show_initial_content, font=("Arial", 18,"bold"), bg="#34c9eb",
                            fg="black")
    back_button.grid(row=4, column=0, pady=10, sticky="w")

    # Function to handle keypress event
    def on_keypress(event):
        key = event.char
        if key == '1':
            configure_settings()
        elif key == '2':
            display_data_settings()
        elif key == '-':
            show_initial_content()
        elif key == '+':
            show_main_menu()

    # Bind the keypress event to the window
    window.bind('<KeyPress>', on_keypress)

def configure_settings():
    # Remove existing widgets from the body frame
    for widget in body_frame.winfo_children():
        widget.destroy()

    # Add a title for the configuration page
    configuration_title = tk.Label(body_frame, text="Configuration Page", font=("Arial", 30, "bold"), bg="#cbedf2")
    configuration_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Display the instruction label
    instruction_label = tk.Label(body_frame, text="Please select an option:", font=("Arial", 28, "bold"), bg="#cbedf2")
    instruction_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

    # Display the configuration options
    option1_label = tk.Label(body_frame, text="Press 1 - AWLR", font=("Arial",26 ), bg="#cbedf2")
    option1_label.grid(row=2, column=0, pady=5, sticky="w")

    option2_label = tk.Label(body_frame, text="Press 2 - ARG", font=("Arial", 26), bg="#cbedf2")
    option2_label.grid(row=3, column=0, pady=5, sticky="w")

    # Add a button to go back to the main menu
    back_button = tk.Button(body_frame, text="Back(-)", command=show_main_menu, font=("Arial", 18, "bold"), bg="#34c9eb",
                            fg="black")
    back_button.grid(row=5, column=0, pady=10, sticky="w")

    def on_keypress(event):
        key = event.char
        if key == '1':
            handle_option("AWLR")
        elif key == '2':
            handle_option("ARG")
        elif key == '-':
            show_main_menu()

    # Bind the keypress event to the window
    window.bind('<KeyPress>', on_keypress)

def display_data_settings():
    for widget in body_frame.winfo_children():
        widget.destroy()

    # Add a title for the configuration page
    view_data_title = tk.Label(body_frame, text="ViewData Page", font=("Arial", 30, "bold"), bg="#cbedf2")
    view_data_title.grid(row=0, column=0, columnspan=2, pady=10)

    instruction_label = tk.Label(body_frame, text="Please select an option:", font=("Arial", 28,"bold"), bg="#cbedf2")
    instruction_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

    option1_label = tk.Label(body_frame, text="Press 1 - Report download", font=("Arial", 26), bg="#cbedf2")
    option1_label.grid(row=2, column=0, pady=5,sticky="w")

    option2_label = tk.Label(body_frame, text="Press 2 - Display data", font=("Arial", 26), bg="#cbedf2")
    option2_label.grid(row=3, column=0, pady=5, sticky="w")

    # Add a button to go back to the main menu
    back_button = tk.Button(body_frame, text="Back(-)", command=show_main_menu, font=("Arial", 18,"bold"),
                            bg="#34c9eb", fg="black")
    back_button.grid(row=5, column=0, pady=10,sticky="w")

    def on_keypress(event):
        key = event.char
        if key == '1':
            handle_option("Report download")
        elif key == '2':
            view_data_settings()
        elif key == '-':
            show_main_menu()
    # Bind the keypress event to the window
    window.bind('<KeyPress>', on_keypress)

def view_data_settings():
    for widget in body_frame.winfo_children():
        widget.destroy()
    # Add a title for the configuration page
    display_data_title = tk.Label(body_frame, text="DisplayData Page", font=("Arial", 30, "bold"), bg="#cbedf2")
    display_data_title.grid(row=0, column=0, columnspan=2, pady=10)

    instruction_label = tk.Label(body_frame, text="Please select an option:", font=("Arial", 28,"bold"), bg="#cbedf2")
    instruction_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

    option1_label = tk.Label(body_frame, text="Press 1 - AWLR", font=("Arial", 26), bg="#cbedf2")
    option1_label.grid(row=2, column=0, pady=5, sticky="w")

    option2_label = tk.Label(body_frame, text="Press 2 - ARG", font=("Arial", 26), bg="#cbedf2")
    option2_label.grid(row=3, column=0, pady=5, sticky="w")

    # Add a button to go back to the main menu
    back_button = tk.Button(body_frame, text="Back(-)", command=display_data_settings, font=("Arial", 18,"bold"),
                            bg="#34c9eb", fg="black")
    back_button.grid(row=5, column=0, pady=10, sticky="w")

    def on_keypress(event):
        key = event.char
        if key == '1':
            display_data_handle_option("AWLR")
        elif key == '2':
            display_data_handle_option("ARG")
        elif key == '-':
            display_data_settings()
    # Bind the keypress event to the window
    window.bind('<KeyPress>', on_keypress)


def handle_option(option):
    for widget in body_frame.winfo_children():
        widget.destroy()

    # Create new content based on selected option
    option_frame = tk.Frame(window, bg="#cbedf2")
    option_frame.pack(padx=10, pady=10)

    option_label = tk.Label(body_frame, text="Selected Option: " + option, font=("Arial", 28, "bold"), bg="#cbedf2")
    option_label.pack()

    if option == "AWLR":
        try:
            with open("rl_value.txt", "r") as file:
                previous_rl_value = file.read().strip()
        except FileNotFoundError:
            previous_rl_value = ""

        # Create RL Value text field
        rl_label = tk.Label(body_frame, text="RL Value:" + previous_rl_value, font=("Arial", 24), bg="#cbedf2")
        rl_label.pack(anchor="w", pady=5)

        rl_entry = tk.Entry(body_frame, font=("Arial", 28))
        rl_entry.pack(anchor="w", pady=5)
        rl_entry.focus_set()

        try:
            with open("water_height.txt", "r") as file:
                previous_total_height = file.read().strip()
        except FileNotFoundError:
            previous_total_height = ""

        # Create water height text field
        water_label = tk.Label(body_frame, text="TOTAL HEIGHT:"+ previous_total_height, font=("Arial", 24), bg="#cbedf2")
        water_label.pack(anchor="w", pady=5)

        water_entry = tk.Entry(body_frame, font=("Arial", 28))
        water_entry.pack(anchor="w", pady=5)
        # water_entry.insert(0, previous_total_height)

        def handle_key(event):
            if event.keysym == "Return":
                if rl_entry.get():
                    water_entry.focus_set()
                else:
                    save_rl_wtrheight_value()

        def handle_down_key(event):
            current_focus = window.focus_get()
            if current_focus == rl_entry:
                water_entry.focus_set()

        def handle_up_key(event):
            current_focus = window.focus_get()
            if current_focus == water_entry:
                rl_entry.focus_set()


        def save_rl_wtrheight_value():
            rl_value = rl_entry.get()
            water_height = water_entry.get()
            with open("rl_value.txt", "w") as file:
                file.write(rl_value)
            print("RL Value saved:", rl_value)
            with open("water_height.txt", "w") as file:
                file.write(water_height)
            print("Water Height Value saved:", water_height)
            messagebox.showinfo("Value Saved", "The values have been saved successfully!")

        # Bind the Return key press event on rl_entry to handle_key function
        rl_entry.bind("<Return>", handle_key)
        # Bind the Return key press event on water_entry to save_rl_wtrheight_value function
        water_entry.bind("<Return>", lambda event: save_rl_wtrheight_value())
        # Bind the Up and Down arrow key press events on rl_entry and water_entry
        rl_entry.bind("<Down>", handle_down_key)
        water_entry.bind("<Up>", handle_up_key)

        # Create Save button
        save_button = tk.Button(body_frame, text="SAVE(Enter)", command=save_rl_wtrheight_value, font=("Arial", 18,"bold"),
                                bg="#34c9eb")
        save_button.pack(side="left", padx=5, pady=10)

        # Bind the Return key press event on save_button to save_rl_wtrheight_value function
        save_button.bind("<Return>", lambda event: save_rl_wtrheight_value())

        back_button = tk.Button(body_frame, text="BACK(-)", font=("Arial", 18,"bold"), bg="#34c9eb", command=configure_settings)
        back_button.pack(side="left", padx=5, pady=10)

        def on_keypress(event):
            key = event.char
            if key == '-':
                configure_settings()

        # Bind the keypress event to the window
        window.bind('<KeyPress>', on_keypress)

        # Set focus to the window
        window.focus_set()

    elif option == "ARG":

        try:
            with open("resolution_value.txt","r") as file:
                previous_resolution_value  = file.read().strip()
        except FileNotFoundError:
            previous_resolution_value =""

        # Create Resolution text field
        resolution_label = tk.Label(body_frame, text="Resolution:"+ previous_resolution_value, font=("Arial", 24), bg="#cbedf2")
        resolution_label.pack(anchor="w", pady=5)

        resolution_entry = tk.Entry(body_frame, font=("Arial", 28))
        resolution_entry.pack(anchor="w", pady=5)
        resolution_entry.focus_set()

        # Function to handle save button click event
        def save_resolution_value():
            resolution_value = resolution_entry.get()
            # Check if the resolution value is valid
            if resolution_value not in ["0.2", "0.5"]:
                # Display an error message in a popup window
                messagebox.showerror("Invalid Value", "Please insert a correct value (0.2 or 0.5).")
            else:
                with open("resolution_value.txt", "w") as file:
                    file.write(resolution_value)
                print("Resolution Value saved:", resolution_value)  # Replace with your desired feedback or logic
                messagebox.showinfo("Value Saved", "The resolution value has been saved successfully!")
        # Create Save button
        save_button = tk.Button(body_frame, text="SAVE(Enter)", command=save_resolution_value, font=("Arial", 18,"bold"),
                                bg="#34c9eb")
        save_button.pack(side="left", padx=5, pady=10)
        window.bind("<Return>", lambda event: save_resolution_value())

        back_button = tk.Button(body_frame, text="BACK(-)", font=("Arial", 18,"bold"), bg="#34c9eb",command=configure_settings)
        back_button.pack(side="left", padx=5, pady=10)

        def on_keypress(event):
            key = event.char
            if key == '-':
                configure_settings()

        # Bind the keypress event to the window
        window.bind('<KeyPress>', on_keypress)

    elif option == "Report download":
        global from_date_entry, to_date_entry

        # Create widgets and handlers as before
        from_date_label = tk.Label(body_frame, text="FROM_DATE:", font=("Arial", 20), bg="#cbedf2")
        from_date_label.pack(anchor="w", pady=5)
        from_date_entry = DateEntry(body_frame, font=("Arial", 24), date_pattern='dd/mm/yy')
        from_date_entry.pack(anchor="w", padx=3, pady=2)
        from_date_entry.focus_set()

        to_date_label = tk.Label(body_frame, text="TO_DATE:", font=("Arial", 20), bg="#cbedf2")
        to_date_label.pack(anchor="w", pady=5)
        to_date_entry = DateEntry(body_frame, font=("Arial", 24), date_pattern='dd/mm/yy')
        to_date_entry.pack(anchor="w", padx=3, pady=2)

        def download_reports():
            from_date = from_date_entry.get_date().strftime('%y%m%d')  # Format the date as yymmdd
            to_date = to_date_entry.get_date().strftime('%y%m%d')

            if not from_date or not to_date:
                messagebox.showerror("Error", "Please provide both From Date and To Date.")
                return

            usb_drive = find_usb_drive()
            if usb_drive:
                try:
                    copy_files_to_usb(usb_drive, from_date, to_date)
                    messagebox.showinfo("Success", "Files copied to USB successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while copying files: {e}")
            else:
                messagebox.showerror("Error", "Please insert the USB drive.")

        def find_usb_drive():
            # Implement a function to find the USB drive here
            # Return the USB drive path if found, otherwise return None
            usb_drive_path = "E:/"  # Replace with your implementation
            if os.path.exists(usb_drive_path):
                return usb_drive_path
            return None

        def copy_files_to_usb(usb_drive, from_date, to_date):
            source_folder = "E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//Sunjray_Received//"  # Replace with the path to the source folder where files are located

            # Convert from_date and to_date strings to datetime objects
            from_date = datetime.datetime.strptime(from_date, "%y%m%d")
            to_date = datetime.datetime.strptime(to_date, "%y%m%d")

            # Iterate through files in the source folder
            for filename in os.listdir(source_folder):
                file_path = os.path.join(source_folder, filename)

                # Check if the file is within the selected date range
                file_date_str = filename.split("_")[1]  # Extract the date part from the filename
                file_date = datetime.datetime.strptime(file_date_str, "%y%m%d")
                if from_date <= file_date <= to_date:
                    destination_path = os.path.join(usb_drive, filename)
                    shutil.copy(file_path, destination_path)

        # Create Download button
        download_button = tk.Button(body_frame, text="Download(Enter)", font=("Arial", 18,"bold"), bg="#34c9eb",
                                    command=download_reports)
        download_button.pack(side="left", padx=5, pady=10)

        back_button = tk.Button(body_frame, text="BACK(-)", command=display_data_settings, font=("Arial", 18,"bold"), bg="#34c9eb")
        back_button.pack(side="left", padx=5, pady=10)

        def on_keypress(event):
            key = event.char
            if key == '-':
                display_data_settings()

        # Bind the keypress event to the window
        window.bind('<KeyPress>', on_keypress)

        # Bind the Enter key to the Download button's action
        def enter_key_pressed(event):
            download_reports()

        window.bind('<Return>', enter_key_pressed)

        # Bind the Up and Down arrow keys to navigate between date entry fields
        def on_down_arrow_key(event):
            if event.keysym == 'Down':
                to_date_entry.focus_set()

        def on_up_arrow_key(event):
            if event.keysym == 'Up':
                from_date_entry.focus_set()

        # Bind the down arrow key to the on_down_arrow_key function
        from_date_entry.bind('<Down>', on_down_arrow_key)
        to_date_entry.bind('<Up>', on_up_arrow_key)


def display_data_handle_option(option):
    for widget in body_frame.winfo_children():
        widget.destroy()

    if option == 'AWLR':
        source_folder = "E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//WRD_Sent//"

        # Create a table to display the data
        columns = ['Stn_id', 'Date&Time', 'Sim_no', 'Batt_Volt', 'Water_Depth','Solar_Volt']
        data_rows = []
        # Initialize variables for earliest and latest dates
        earliest_date = None
        latest_date = None
        # Iterate through files in the source folder
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            # Check if the file is for the selected date
            file_date_str = filename.split("_")[1]  # Extract the date part from the filename
            file_date = datetime.datetime.strptime(file_date_str, "%y%m%d")

            # Update earliest_date and latest_date
            if earliest_date is None or file_date < earliest_date:
                earliest_date = file_date
            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        # Select only specific columns from the row
                        selected_columns = [row[0], row[1], row[2], row[3], row[4], row[7]]
                        data_rows.append(selected_columns)

        date_range_label = tk.Label(body_frame,
                                    text=f"Data available from: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}",
                                    font=("Arial", 18), bg="#cbedf2")
        date_range_label.pack(anchor="w", pady=10)
        back_button = tk.Button(body_frame, text="BACK(-)", command=view_data_settings, font=("Arial", 18, "bold"),
                                bg="#34c9eb")
        back_button.pack(anchor="w", pady=10)


        # Display the data in a table
        tree = ttk.Treeview(body_frame, columns=columns, show='headings')

        # Create a vertical scrollbar
        tree_scrollbar = ttk.Scrollbar(body_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scrollbar.set)

        for col in columns:
            tree.heading(col, text=col)

            tree.column(col, width=125)  # Adjust the column width as needed

        for row in data_rows:
            tree.insert('', 'end', values=row)

        tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="left", fill="y")

        def on_keypress(event):
            key = event.keysym
            if key == 'Up':
                tree.yview_scroll(-1, "units")
            elif key == 'Down':
                tree.yview_scroll(1, "units")
            elif key == 'minus':
                view_data_settings()

        # Bind the keypress event to the window
        window.bind('<KeyPress>', on_keypress)

    if option == 'ARG':
        source_folder = "E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//WRD_Sent//"

        # Create a table to display the data
        columns = ['Stn_id', 'Date&Time', 'Sim_no', 'Batt_Vol','Hr_Rainfall','Daily_Rainfall', 'Solar_Volt']
        data_rows = []
        # Initialize variables for earliest and latest dates
        earliest_date = None
        latest_date = None
        # Iterate through files in the source folder
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            # Check if the file is for the selected date
            file_date_str = filename.split("_")[1]  # Extract the date part from the filename
            file_date = datetime.datetime.strptime(file_date_str, "%y%m%d")

            # Update earliest_date and latest_date
            if earliest_date is None or file_date < earliest_date:
                earliest_date = file_date
            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        # Select only specific columns from the row
                        selected_columns = [row[0], row[1], row[2], row[3], row[5], row[6], row[7]]
                        data_rows.append(selected_columns)

        date_range_label = tk.Label(body_frame,
                                    text=f"Data available from: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}",
                                    font=("Arial", 18), bg="#cbedf2")
        date_range_label.pack(anchor="w", pady=10)
        
        back_button = tk.Button(body_frame, text="BACK(-)", command=view_data_settings, font=("Arial", 18, "bold"),
                                bg="#34c9eb")
        back_button.pack(anchor="w", pady=10)


        # Display the data in a table
        tree = ttk.Treeview(body_frame, columns=columns, show='headings')

        # Create a vertical scrollbar
        tree_scrollbar = ttk.Scrollbar(body_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scrollbar.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=115)  # Adjust the column width as needed

        for row in data_rows:
            tree.insert('', 'end', values=row)

        # Pack the Treeview widget

        tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="left", fill="y")

        def on_keypress(event):
            key = event.keysym
            if key == 'Up':
                tree.yview_scroll(-1, "units")
            elif key == 'Down':
                tree.yview_scroll(1, "units")
            elif key == 'minus':
                view_data_settings()
        
        window.focus_set()
        # Bind the keypress event to the window
        window.bind('<KeyPress>', on_keypress)


# Initial content
date_time_label = tk.Label(body_frame, text="Date & Time: " + current_date_time, font=("Arial", 26), bg="#cbedf2")
date_time_label.pack(anchor="w")
solar_voltage_label = tk.Label(body_frame, text="Solar Voltage: " + str(solar_voltage) + "Volt", font=("Arial", 26),
                               bg="#cbedf2")
solar_voltage_label.pack(anchor="w")

battery_voltage_label = tk.Label(body_frame, text="Battery Voltage: " + str(battery_voltage) + "Volt",
                                 font=("Arial", 26), bg="#cbedf2")
battery_voltage_label.pack(anchor="w")

water_depth_label = tk.Label(body_frame, text="Water Depth: " + str(water_depth) + "meter", font=("Arial", 26),
                             bg="#cbedf2")
water_depth_label.pack(anchor="w")

current_rainfall_label = tk.Label(body_frame, text="Current Rainfall:"+ str(current_rainfall), font=("Arial",26), bg="#cbedf2")
current_rainfall_label.pack(anchor="w")

hourly_rainfall_label = tk.Label(body_frame, text="Hourly Rainfall: " + str(hourly_rainfall), font=("Arial", 26),
                                 bg="#cbedf2")
hourly_rainfall_label.pack(anchor="w")

daily_rainfall_label = tk.Label(body_frame, text="Daily Rainfall: " + str(daily_rainfall), font=("Arial", 26),
                                bg="#cbedf2")
daily_rainfall_label.pack(anchor="w")

# Main Menu Button
main_menu_button = tk.Button(body_frame, text="Main Menu(+)", command=show_main_menu, font=("Arial", 20, "bold"), bg="#34c9eb", fg="black")
main_menu_button.pack(side="bottom", pady=10)


def update_initial_content():
    # Read the updated values from the Excel sheet
    file_contents = pd.read_excel('data.xlsx')
    all_rows = file_contents.values.tolist()

    # Update the values
    current_date_time = datetime.datetime.now().strftime("%d-%m-%Y / %H:%M:%S")
    solar_voltage = all_rows[1][1]
    battery_voltage = all_rows[2][1]
    water_depth = all_rows[3][1]
    hourly_rainfall = all_rows[4][1]
    daily_rainfall = all_rows[5][1]

    with open("current_rainfall.txt", "r") as file:
        current_rainfall = file.read().strip()
        file.close()

    # Update the labels in the initial content section
    date_time_label.config(text="Date & Time: " + current_date_time)
    solar_voltage_label.config(text="Solar Voltage: " + str(solar_voltage) + " Volt")
    battery_voltage_label.config(text="Battery Voltage: " + str(battery_voltage) + " Volt")
    water_depth_label.config(text="Water Depth: " + str(water_depth) + " meter")
    current_rainfall_label.config(text="Current Rainfall: "+ str(current_rainfall))
    hourly_rainfall_label.config(text="Hourly Rainfall: " + str(hourly_rainfall))
    daily_rainfall_label.config(text="Daily Rainfall: " + str(daily_rainfall))

    # Schedule the next update after 15 minutes
    window.after(60000, update_initial_content)



# Call the update_initial_content function to initiate the first update
update_initial_content()

# Run the Tkinter event loop
window.mainloop()