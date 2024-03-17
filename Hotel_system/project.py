from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("900x900")
     
        
        # Initialize room configurations and rates
        self.total_rooms = 300
        self.room_config = {
            "Double": {
                "AC": {"available": 75, "rate": 2000},
                "Non-AC": {"available": 75, "rate": 1500}
            },
            "Single": {
                "AC": {"available": 75, "rate": 3000},
                "Non-AC": {"available": 75, "rate": 1000}
            }
        }

        # Variable to store login credentials
        self.username = "admin"
        self.password = "admin123"

        # Font style
        self.font_style = ("Helvetica", 10)

        # Create login page
        self.create_login_page()

    def create_login_page(self):
        # Username and Password Entry Fields
        self.username_label = Label(self.root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = Label(self.root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        self.login_button = Button(self.root, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def login(self):
        # Retrieve username and password entered by the user
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Check if entered credentials match the stored credentials
        if entered_username == self.username and entered_password == self.password:
            messagebox.showinfo("Login Successful", "Welcome to the Hotel Management System!")
            # Once logged in, show the main menu
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")

    def show_main_menu(self):
        # Destroy login frame
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create notebook widget to display tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Add tabs for Rooms, Restaurant, and Hall
        self.create_rooms_tab()
        self.create_restaurant_tab()
        self.create_hall_tab()

    def create_rooms_tab(self):
        room_tab = Frame(self.notebook)
        self.notebook.add(room_tab, text="Rooms")

        # Functionality for managing rooms
        Label(room_tab, text="Room Booking", foreground="blue", font="capri 19", justify=CENTER).grid(row=1, column=3, padx=10, pady=10)

        # Add room booking form, display available rooms
        self.display_available_rooms(room_tab)

    def create_restaurant_tab(self):
        restaurant_tab = tk.Frame(self.notebook)
        self.notebook.add(restaurant_tab, text="Restaurant")
        self.create_restaurant_management_system(restaurant_tab)

    def create_restaurant_management_system(self, root):
        self.customer_name = tk.StringVar()
        self.customer_contact = tk.StringVar()

        self.items = {
            "Burger": 100,
            "Pizza": 200,
            "Pasta": 150,
            "Sandwich": 80,
            "Salad": 90,
            "Mushroom Biriyani": 100,
            "Friend Rice": 100,
            "Noodles":150,
            "Veg Rice":100,
            "Paneer Tikka":250
        }

        self.orders = {}
        self.gst_percentage = 18
        self.total_tables = 10
        self.reserved_tables = 0
        self.remaining_tables = self.total_tables - self.reserved_tables

        details_frame = tk.LabelFrame(root, text="Customer Details")
        details_frame.pack(fill="x", padx=10, pady=10)

        name_label = tk.Label(details_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        contact_label = tk.Label(details_frame, text="Contact:")
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact)
        contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        contact_entry.configure(validate="key")
        contact_entry.configure(validatecommand=(contact_entry.register(self.validate_contact), "%P"))

        menu_frame = tk.LabelFrame(root, text="Menu")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        item_header = tk.Label(menu_frame, text="Items")
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        quantity_header = tk.Label(menu_frame, text="Quantity")
        quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        row = 1
        for item, price in self.items.items():
            item_var = tk.IntVar()
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            quantity_entry = tk.Entry(menu_frame, width=5)
            quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

            self.orders[item] = {"var": item_var, "quantity": quantity_entry}

            row += 1

        buttons_frame = tk.Frame(root)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup)
        print_bill_button.pack(side="left", padx=5)

        clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection)
        clear_selection_button.pack(side="left", padx=5)

        self.sample_bill_text = tk.Text(root, height=10)
        self.sample_bill_text.pack(fill="x", padx=10, pady=10)

        # Update sample bill when quantity or item is selected
        for item, info in self.orders.items():
            info["quantity"].bind("<FocusOut>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<Return>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<KeyRelease>", lambda event, item=item: self.update_sample_bill(item))
            info["var"].trace("w", lambda *args, item=item: self.update_sample_bill(item))

    def show_bill_popup(self):
        # Check if customer name is provided
        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "Please enter customer name.")
            return

        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one item.")
            return

        gst_amount = (total_price * self.gst_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}\n"
        bill += f"Avaliable Table :{self.remaining_tables}"
        self.reserved_tables += 1
        self.update_tables_label()
        with open("bill_details.txt", "a", encoding="utf-8") as file:
            file.write(bill)
            file.write("\n\n")

        messagebox.showinfo("Bill", bill)

    def past_records(self):
        messagebox.showinfo("Past Records", "This feature is not implemented yet.")

    def clear_selection(self):
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, END)

    def update_sample_bill(self, item):
        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        gst_amount = (total_price * self.gst_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}\n"
        bill += f"Avaliable Table :{self.remaining_tables}"

        self.sample_bill_text.delete("1.0", END)  # Clear previous contents
        self.sample_bill_text.insert(END, bill)

    def validate_contact(self, value):
        return value.isdigit() or value == ""

    def convert_to_inr(self, amount):
        return "₹" + str(amount)

    def update_tables_label(self):
        self.remaining_tables = self.total_tables - self.reserved_tables
        tables_label = Label(self.root, text=f"Remaining Tables: {self.remaining_tables}")
        tables_label.pack()
   
        # Number of tables

    def create_hall_tab(self):
        hall_tab = Frame(self.notebook)
        self.notebook.add(hall_tab, text="Hall")

    # Functionality for managing hall
      
        self.create_hall_management(hall_tab)
    def create_hall_management(self,root):
        #
        self.customers_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.time_in = tk.StringVar()
        self.time_out = tk.StringVar()
        self.num_members = tk.IntVar()
        self.food_availability = tk.StringVar()
        self.halls_available = 4
        self.halls_booked = 0
        self.dates = StringVar()
    # Call create_gui method with self as argument
        self.create_gui(root)

    def create_gui(self, root):
        #
        details_frame = tk.LabelFrame(root, text=" Hall Booking Details")
        details_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(details_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(details_frame, textvariable=self.customers_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(details_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(details_frame, textvariable=self.customer_phone).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(details_frame, text="Time In:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(details_frame, textvariable=self.time_in).grid(row=2, column=1, padx=5, pady=5)
       

        tk.Label(details_frame, text="Time Out:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(details_frame, textvariable=self.time_out).grid(row=3, column=1, padx=5, pady=5)
        

        tk.Label(details_frame, text="Number of Members:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(details_frame, textvariable=self.num_members).grid(row=4, column=1, padx=5, pady=5)
        tk.Label(details_frame, text="Date:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(details_frame, textvariable=self.dates).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(details_frame, text="Food Availability:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.food_availability = StringVar()
        self.food_availability.set("0")
        tk.Radiobutton(details_frame, text="Available", variable=self.food_availability, value="Available").grid(row=6, column=1, padx=5, pady=5, sticky="w")
        tk.Radiobutton(details_frame, text="Not Available", variable=self.food_availability, value="Not Available").grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Button(details_frame, text="Book Hall", command=self.book_hall).grid(row=8, columnspan=2, padx=5, pady=10)

    # Display halls availability
        halls_frame = tk.LabelFrame(root, text="Halls Availability")
        halls_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.halls_label = tk.Label(halls_frame, text=f"Halls Available: {self.halls_available}")
        self.halls_label.pack(padx=5, pady=5)

    # Display booked details
        self.booked_frame = tk.LabelFrame(root, text="Hall Booked Details")
        self.booked_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.booked_details_text = scrolledtext.ScrolledText(self.booked_frame, wrap=tk.WORD, width=40, height=10)
        self.booked_details_text.pack(fill="both", expand=True, padx=5, pady=5)


    def book_hall(self):
        if self.halls_available <= 0:
            messagebox.showwarning("Hall Booking", "No halls available for booking.")
            return

        # Validate input fields
        if not self.validate_fields():
            return

        self.halls_booked += 1
        self.halls_available -= 1

        messagebox.showinfo("Hall Booking", "Hall booked successfully.")

        # Update halls availability display
        self.halls_label.config(text=f"Halls Available: {self.halls_available}")

        # Display booked details
        self.display_booked_details()

    def validate_fields(self):
        if not self.customers_name.get().strip():
            messagebox.showerror("Error", "Please enter customer name.")
            return False
        if not self.customer_phone.get().strip():
            messagebox.showerror("Error", "Please enter customer phone.")
            return False
        if not self.time_in.get().strip():
            messagebox.showerror("Error", "Please enter time in.")
            return False
        if not self.time_out.get().strip():
            messagebox.showerror("Error", "Please enter time out.")
            return False
        if not self.dates.get().strip():
            messagebox.showerror("Error", "Please enter correct date.")
            return False
        if self.num_members.get() <= 0:
            messagebox.showerror("Error", "Please enter valid number of members.")
            return False
        return True

    def display_booked_details(self):
        details = f"Name: {self.customers_name.get()}\n"
        details += f"Phone: {self.customer_phone.get()}\n"
        details += f"Time In: {self.time_in.get()}\n"
        details += f"Time Out: {self.time_out.get()}\n"
        details += f"Number of Members: {self.num_members.get()}\n"
        details += f"Food Availability: {self.food_availability.get()}\n"
        details +=f"Date:{self.dates.get()}\n"
        details +="---------------------------------------------------\n"
        with open("hall_book_details.txt", "a", encoding="utf-8") as file:
            file.write(details)
            file.write("\n\n")
        self.booked_details_text.insert(tk.END, details + "\n\n")


    def display_available_rooms(self, parent_frame):
           #
        # Room booking form
           Label(parent_frame, text="First Name:", foreground="blue", font=self.font_style, justify=LEFT).grid(row=2, column=1, padx=10, pady=10, sticky="e")
           self.first_name_entry = Entry(parent_frame, foreground="blue", font=self.font_style)
           self.first_name_entry.grid(row=2, column=2, padx=10, pady=10)

           Label(parent_frame, text="Last Name:", foreground="red", font=self.font_style, justify=LEFT).grid(row=3, column=1, padx=10, pady=10, sticky="e")
           self.last_name_entry = Entry(parent_frame, foreground="red", font=self.font_style)
           self.last_name_entry.grid(row=3, column=2, padx=10, pady=10)

           Label(parent_frame, text="Email:", justify="right", font=self.font_style).grid(row=4, column=1, padx=10, pady=10, sticky="e")
           self.email_entry = Entry(parent_frame, justify="left", font=self.font_style)
           self.email_entry.grid(row=4, column=2, padx=10, pady=10)

           Label(parent_frame, text="Number of Rooms:", font=self.font_style).grid(row=5, column=1, padx=10, pady=10, sticky="e")
           self.num_rooms_entry = Entry(parent_frame, font=self.font_style)
           self.num_rooms_entry.grid(row=5, column=2, padx=10, pady=10)

        # Room type selection
           Label(parent_frame, text="Room Type:", font=self.font_style).grid(row=6, column=1, padx=10, pady=10, sticky="e")
           self.room_type_var = StringVar()
           self.room_type_var.set("0")  # Set initial value to "Double"
           row_index = 6
           for idx, room_type in enumerate(self.room_config.keys()):
                Radiobutton(parent_frame, text=room_type, variable=self.room_type_var, value=room_type, justify=LEFT, font=self.font_style).grid(row=row_index, column=idx+2, padx=10, pady=5)
   

# AC/Non-AC selection
           Label(parent_frame, text="AC/Non-AC:", font=self.font_style).grid(row=row_index+1, column=1, padx=10, pady=10, sticky="e")
           self.ac_var = StringVar()
           self.ac_var.set("0")  # Default selection
           Radiobutton(parent_frame, text="AC", variable=self.ac_var, value="AC", justify=LEFT, font=self.font_style).grid(row=row_index+1, column=2, padx=10, pady=5)
           Radiobutton(parent_frame, text="Non-AC", variable=self.ac_var, value="Non-AC", justify=LEFT, font=self.font_style).grid(row=row_index+1, column=3, padx=10, pady=5)
           row_index += 2  # Increment row index for the next widget

        # Check-in Date entry
           Label(parent_frame, text="Check-in Date:", font=self.font_style).grid(row=row_index, column=1, padx=10, pady=10, sticky="e")
           self.check_in_entry = Entry(parent_frame, font=self.font_style)
           self.check_in_entry.grid(row=row_index, column=2, padx=10, pady=10)

           row_index += 1  # Increment row index for the next widget

        # Check-out Date entry
           Label(parent_frame, text="Check-out Date:", font=self.font_style).grid(row=row_index, column=1, padx=10, pady=10, sticky="e")
           self.check_out_entry = Entry(parent_frame, font=self.font_style)
           self.check_out_entry.grid(row=row_index, column=2, padx=10, pady=10)

           row_index += 1  # Increment row index for the next widget

        # Other fields
           Label(parent_frame, text="Phone Number:", font=self.font_style).grid(row=row_index, column=1, padx=10, pady=10, sticky="e")
           self.phone_entry = Entry(parent_frame, font=self.font_style)
           self.phone_entry.grid(row=row_index, column=2, padx=10, pady=10)
        
           row_index += 1  # Increment row index for the next widget

           Label(parent_frame, text="Upload Aadhar Card Scan:", foreground="red", font=self.font_style).grid(row=row_index, column=1, padx=10, pady=10, sticky="e")
           self.aadhar_button = Button(parent_frame, text="Upload", command=self.upload_aadhar_scan, foreground="red", font=self.font_style)
           self.aadhar_button.grid(row=row_index, column=2, padx=10, pady=10)
           self.aadhar_success_label = Label(parent_frame, text="", fg="green")
           self.aadhar_success_label.grid(row=row_index, column=3, padx=10, pady=10)
           row_index += 1  # Increment row index for the next widget

           self.room_rate_label = Label(parent_frame, text="Room Rate:", font=self.font_style,justify=RIGHT)
           self.room_rate_label.grid(row=row_index, column=1, padx=10, pady=10,sticky="e")
        
           row_index += 1  # Increment row index for the next widget

           Label(parent_frame, text="Address:", font=self.font_style).grid(row=row_index, column=1, padx=10, pady=10, sticky="e")
           self.address_entry = Entry(parent_frame, font=self.font_style)
           self.address_entry.grid(row=row_index, column=2, padx=10, pady=10, sticky="w")

           row_index += 1  # Increment row index for the next widget

        # Submit button
           Button(parent_frame, text="Submit", command=self.book_room, font=("Helvetica", 12)).grid(row=row_index, column=2, padx=10, pady=10, sticky="w")
                # Display available rooms
           self.display_available_rooms_label(parent_frame)

    def display_available_rooms_label(self, parent_frame):
        #
    # Create a frame to contain the available rooms label
        available_rooms_frame = Frame(parent_frame, bd=2, relief="groove")
        available_rooms_frame.grid(row=0, column=5, rowspan=8, padx=10, pady=10)

    # Create a scrolled text widget for displaying available rooms
        available_rooms_text = "Available Rooms:\n"
        for room_type, room_data in self.room_config.items():
            for ac_preference, room_info in room_data.items():
                 available_rooms_text += f"{room_type} {ac_preference}: {room_info['available']}\n"

        available_rooms_text_widget = scrolledtext.ScrolledText(available_rooms_frame, wrap='word', width=30, height=10)
        available_rooms_text_widget.insert('end', available_rooms_text)
        available_rooms_text_widget.config(state='disabled')
        available_rooms_text_widget.pack(fill='both', expand=True)


    def upload_aadhar_scan(self):
         file_path = filedialog.askopenfilename(title="Select Aadhar Card Scan", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
         if file_path:
        # Display success message
               self.aadhar_success_label.config(text="Upload successful", fg="green")
         else:
        # Handle the case where no file was selected or the selection was canceled
              self.aadhar_success_label.config(text="Upload canceled or failed", fg="red")
        # You can store or process the file path as needed

    def book_room(self):
       # Retrieve form data
       first_name = self.first_name_entry.get()
       last_name = self.last_name_entry.get()
       email = self.email_entry.get()
       num_rooms_str = self.num_rooms_entry.get()
       if num_rooms_str:
          num_rooms = int(num_rooms_str)
       else:
    # Handle the case where the entry is empty, e.g., display an error message or set a default value
          num_rooms = 0  
       room_type = self.room_type_var.get()
       ac_preference = self.ac_var.get()
       phone_number = self.phone_entry.get()
       address = self.address_entry.get()  # Retrieve address from Entry widget
       check_in_date=self.check_in_entry.get()
       check_out_date=self.check_out_entry.get()
       # Perform room booking
       room_data = self.room_config.get(room_type)
       if not room_data or room_data[ac_preference]["available"] < num_rooms:
           messagebox.showerror("Booking Failed", f"Not enough {ac_preference} {room_type} rooms unavailable")
           return
        

       # Calculate total cost
       room_rate = room_data[ac_preference]["rate"]
       total_cost = num_rooms * room_rate

       # Display booking confirmation and room rate
       messagebox.showinfo("Booking Successful", f"Booking confirmed for {num_rooms} {ac_preference} {room_type} room(s).\nTotal Cost: ₹{total_cost}")

       # Update total number of rooms
       room_data[ac_preference]["available"] -= num_rooms

       # Display room rate
       self.room_rate_label.config(text=f"Room Rate : {num_rooms} {room_type}  {ac_preference} ₹{total_cost} per room")

       # Update available rooms count
       parent_frame = self.notebook.winfo_children()[0]  # Get the parent frame from the notebook
       self.display_available_rooms_label(parent_frame)
       file_upload_details = self.aadhar_button["text"]
       with open("booking_details.txt", "a",encoding="utf-8") as file:
            file.write(f"Booking Details:\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nNumber of Rooms: {num_rooms}\nRoom Type: {room_type}\nAC Preference: {ac_preference}\nPhone Number: {phone_number}\nAddress: {address}\n")
            file.write(f"Available Rooms: {room_data[ac_preference]['available']}\n")
            file.write(f"Total Cost for {num_rooms} {ac_preference} {room_type} room(s): ₹{total_cost}\n")
            file.write(f"Room Rate: ₹{room_rate}\n")
            file.write(f"File Upload Details: {file_upload_details}\n")
            file.write(f"Check-in Date :{check_in_date}\n")
            file.write(f"Check-out Date ::{check_out_date}\n")
            file.write("\n")
               # Log booking details to scrolled text widget
        # log_message = f"Booking Details:\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nNumber of Rooms: {num_rooms}\nRoom Type: {room_type}\nAC Preference: {ac_preference}\nPhone Number: {phone_number}\nAddress: {address}\n"
        # self.log_scroll_text.insert(END, log_message)

def main():
    root = Tk()
    app = HotelManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
