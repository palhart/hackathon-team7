from generator.gpt import GPT
from generator.preprocess import convert_input, get_images_path
from dataset.grub import add_json_to_csv
from pdf_report.generate_historical_pdf import generate_report_for_company
from dotenv import load_dotenv
import os
import json 


def historical_process_data(root_path, api_key, pdf_path):
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    # Convert PDF to images
    pdf_path = os.path.join(root_path, pdf_path)
    image_dir = os.path.join(root_path, "images")
    convert_input(pdf_path, image_dir)

    print(f"PDF converted to images: {image_dir}")

    # Extract data from images
    gpt = GPT(api_key=api_key)
    deck_images = get_images_path(image_dir)
    fields = [
        "company_name",
        "company_website",
        "quarter",
        "Headcount_Count",
        "Headcount_Growth",
        "Fundraising_Total_amount",
        "Fundraising_Date_of_last_round",
        "Financials_GMV",
        "Financials_Net_Sales",
        "Financials_CAC",
        "tech_employee (convert from % to number)",
        "sales_employee (convert from % to number)",
        "admin_employee (convert from % to number)"
        ]
    data = gpt.extract_data(deck_images, fields)

    print(f"Data extracted: {data}")

    # Add data to CSV
    csv_file_path = os.path.join(root_path, "dataset/portcos_historical_db.csv")
    add_json_to_csv(data, csv_file_path)

    print(f"Data added to CSV: {csv_file_path}")

    data = json.loads(data)


    # Create PDF report
    company_name = data['company_name']
    csv_path = os.path.join(root_path, "dataset/portcos_historical_db.csv")
    pdf_path = generate_report_for_company(csv_path, company_name)

    return pdf_path