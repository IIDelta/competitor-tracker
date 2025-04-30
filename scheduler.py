# scheduler.py
import schedule
import time

def job():
    """The task to run on a schedule."""
    print("Updating data...")
    # Call the appropriate functions to update data

# Example scheduling every day at 10 am
schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
