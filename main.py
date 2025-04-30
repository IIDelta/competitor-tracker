# main.py
from api_client import get_studies_for_company, fields
from excel_manager import select_output_file_path, write_studies_to_excel
from data_processor import format_study_data

import tkinter as tk
from tkinter import simpledialog

def get_company_names():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring("Input", "Enter company names separated by commas:")
    if user_input:
        companies = [name.strip() for name in user_input.split(',')]
        return companies
    return []

def main():
    companies = get_company_names()
    output_file_path = select_output_file_path()
    for company in companies:
        response = get_studies_for_company(company, fields)
        formatted_data = format_study_data(response)
        print(f"Data to be written for {company}: {formatted_data}")  # Debugging information
        write_studies_to_excel(output_file_path, company, formatted_data)

if __name__ == "__main__":
    main()
