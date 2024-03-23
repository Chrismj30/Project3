import os
import datetime
import time

def schedule_opening(application_path, opening_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == opening_time:
            os.system(f'start "" "{application_path}"')
            print(f"Application opened at {opening_time}.")
            break
        time.sleep(60)  # Check every minute if it's time to open the application

if __name__ == "__main__":
    application_path = input("Enter the path of the application: ")
    opening_time = input("Enter the opening time (HH:MM): ")
    schedule_opening(application_path, opening_time)
