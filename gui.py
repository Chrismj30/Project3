import tkinter as tk
from tkinter import messagebox, filedialog
from backup_app import BackupApp
import datetime
import os
import time

class BackupAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Backup Application")
        self.root.geometry("400x400")
        self.root.configure(bg="black")  # Set background color to black

        # Welcome message
        self.welcome_label = tk.Label(self.root, text="Welcome to Backup Application", font=("Helvetica", 18, "bold"), fg="white", bg="black")
        self.welcome_label.pack(pady=10)

        # Source directory input
        self.source_label = tk.Label(self.root, text="Source Directory:", font=("Helvetica", 12), fg="white", bg="black")
        self.source_label.pack()
        self.source_entry = tk.Entry(self.root, font=("Helvetica", 12), bg="black", fg="white")  # Set background and foreground color
        self.source_entry.pack()
        self.browse_source_button = tk.Button(self.root, text="Browse", command=self.browse_source)
        self.browse_source_button.pack()

        # Backup directory input
        self.backup_label = tk.Label(self.root, text="Backup Directory:", font=("Helvetica", 12), fg="white", bg="black")
        self.backup_label.pack()
        self.backup_entry = tk.Entry(self.root, font=("Helvetica", 12), bg="black", fg="white")  # Set background and foreground color
        self.backup_entry.pack()
        self.browse_backup_button = tk.Button(self.root, text="Browse", command=self.browse_backup)
        self.browse_backup_button.pack()

        # Backup time input
        self.time_label = tk.Label(self.root, text="Backup Time (HH:MM):", font=("Helvetica", 12), fg="white", bg="black")
        self.time_label.pack()
        self.time_entry = tk.Entry(self.root, font=("Helvetica", 12), bg="black", fg="white")  # Set background and foreground color
        self.time_entry.pack()

        self.maintenance_label = tk.Label(self.root, text="Maintenance Time (HH:MM):", font=("Helvetica", 12), fg="white", bg="black")
        self.maintenance_label.pack()
        self.maintenance_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.maintenance_entry.pack()

        # Run backup button
        self.run_backup_button = tk.Button(self.root, text="Run Backup", font=("Helvetica", 14, "bold"), bg="#3498DB", fg="white", relief="raised", command=self.start_backup)
        self.run_backup_button.pack(pady=15)

        # Run maintenance button
        self.run_maintenance_button = tk.Button(self.root, text="Run Maintenance", font=("Helvetica", 14, "bold"), bg="#3498DB", fg="white", relief="raised", command=self.start_maintenance)
        self.run_maintenance_button.pack(pady=15)

        # Opening time input
        self.opening_time_label = tk.Label(self.root, text="Application Opening Time (HH:MM):", font=("Helvetica", 12), fg="white", bg="black")
        self.opening_time_label.pack()
        self.opening_time_entry = tk.Entry(self.root, font=("Helvetica", 12), bg="black", fg="white")  # Set background and foreground color
        self.opening_time_entry.pack()

        # Run application button
        self.run_app_button = tk.Button(self.root, text="Run Application", font=("Helvetica", 14, "bold"), bg="#3498DB", fg="white", relief="raised", command=self.run_application)
        self.run_app_button.pack(pady=15)

        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 12), fg="white", bg="black")
        self.status_label.pack()

    def browse_source(self):
        source_dir = filedialog.askdirectory()
        if source_dir:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, source_dir)

    def browse_backup(self):
        backup_dir = filedialog.askdirectory()
        if backup_dir:
            self.backup_entry.delete(0, tk.END)
            self.backup_entry.insert(0, backup_dir)

    def start_backup(self):
        source_dir = self.source_entry.get()
        backup_dir = self.backup_entry.get()
        backup_time = self.time_entry.get()

        if not source_dir or not backup_dir or not backup_time:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not self.validate_time_format(backup_time):
            messagebox.showerror("Error", "Invalid backup time format. Please use HH:MM.")
            return

        confirmation = messagebox.askyesno("Confirmation", f"Do you want to start the backup process for '{source_dir}' to '{backup_dir}' at {backup_time}?")
        if confirmation:
            app = BackupApp(source_dir, backup_dir, backup_time)
            app.run_backup()
            self.status_var.set("Backup completed.")
        else:
            self.status_var.set("Backup process cancelled.")

    def validate_time_format(self, time_str):
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def run_application(self):
        application_path = filedialog.askopenfilename(title="Select Application")
        if not application_path:
            return

        opening_time = self.opening_time_entry.get()
        if not self.validate_time_format(opening_time):
            messagebox.showerror("Error", "Invalid opening time format. Please use HH:MM.")
            return

        confirmation = messagebox.askyesno("Confirmation", f"Do you want to open the application '{application_path}' at {opening_time}?")
        if confirmation:
            schedule_opening(application_path, opening_time)
            self.status_var.set(f"Application scheduled to open at {opening_time}.")
        else:
            self.status_var.set("Application opening cancelled.")

    def run(self):
        self.root.mainloop()

    def start_maintenance(self):
        maintenance_time = self.maintenance_entry.get()

        if not maintenance_time:
            messagebox.showerror("Error", "Please enter the maintenance time.")
            return

        if not self.validate_time_format(maintenance_time):
            messagebox.showerror("Error", "Invalid maintenance time format. Please use HH:MM.")
            return

        confirmation = messagebox.askyesno("Confirmation", f"Do you want to perform maintenance at {maintenance_time}?")
        if confirmation:
            schedule_maintenance(maintenance_time)
            self.status_var.set(f"Maintenance scheduled at {maintenance_time}.")
        else:
            self.status_var.set("Maintenance scheduling cancelled.")

    def validate_time_format(self, time_str):
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def run(self):
        self.root.mainloop()

def schedule_opening(application_path, opening_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == opening_time:
            os.system(f'start "" "{application_path}"')
            print(f"Application opened at {opening_time}.")
            break
        time.sleep(60)  # Check every minute if it's time to open the application


def schedule_maintenance(maintenance_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == maintenance_time:
            os.system("cleanmgr")
            print(f"Maintenance performed at {maintenance_time}.")
            break
        time.sleep(60)  # Check every minute if it's time to perform maintenance
