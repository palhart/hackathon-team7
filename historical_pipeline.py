from generator.gpt import GPT
from generator.preprocess import convert_input, get_images_path
from dataset.grub import add_json_to_csv
from pdf_report.generate_historical_pdf import generate_report_for_company
from dotenv import load_dotenv
import os
import json 

# load_dotenv()

# root_path = os.path.dirname(os.path.abspath(__file__))

# api_key = os.getenv('OPENAI_API_KEY')



# if __name__ == '__main__':

#     if not api_key:
#         raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

#     # Convert PDF to images
    
#     pdf_path = os.path.join(root_path, "Private_Comprehensive_Startup_Decks", "Company_test.pdf")
#     image_dir = os.path.join(root_path, "images")
#     convert_input(pdf_path, image_dir)

#     # Extract data from images

#     gpt = GPT(api_key=api_key)
#     deck_images = get_images_path(image_dir) 
#     fields = [
#         # PDF EXTRACTION FIELDS
#         'Company_name', 'companie_website', 'quarter', 'years' 'Headcount_Count', 'Headcount_Growth', 'Fundraising_Total_amount', 'Fundraising_Date_of_last_round', 'Financials_GMV' , 'Financials_Net_Sales' , 'Financials_CAC'
#     ]
#     data = gpt.extract_data(deck_images, fields)

#     print(f"Data extracted: {data}")
    
#     # Add data to CSV

#     csv_file_path = os.path.join(root_path, "dataset", "historical.csv")

#     add_json_to_csv(data, csv_file_path)

#     print(f"Data added to CSV: {csv_file_path}")

#     # Create PDF report

#     company_name = data['Company_name']
#     csv_path = os.path.join(root_path, "dataset", "historical.csv")
#     generate_report_for_company(csv_path, company_name)


def historical_process_data(root_path, api_key, pdf_path):
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    # Convert PDF to images
    pdf_path = os.path.join(root_path, pdf_path)
    image_dir = os.path.join(root_path, "images")
    convert_input(pdf_path, image_dir)

    # Extract data from images
    gpt = GPT(api_key=api_key)
    deck_images = get_images_path(image_dir)
    fields = [
        # PDF EXTRACTION FIELDS
        'Company_name', 'companie_website', 'quarter', 'years', 'Headcount_Count', 'Headcount_Growth', 'Fundraising_Total_amount', 'Fundraising_Date_of_last_round', 'Financials_GMV', 'Financials_Net_Sales', 'Financials_CAC'
    ]
    data = gpt.extract_data(deck_images, fields)

    print(f"Data extracted: {data}")

    # Add data to CSV
    csv_file_path = os.path.join(root_path, "dataset", "historical.csv")
    add_json_to_csv(data, csv_file_path)

    print(f"Data added to CSV: {csv_file_path}")

    data = json.loads(data)


    # Create PDF report
    company_name = data['Company_name']
    csv_path = os.path.join(root_path, "dataset/historical.csv")
    pdf_path = generate_report_for_company(csv_path, company_name)

    return pdf_path