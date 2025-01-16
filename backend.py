# main.py
import pandas as pd
from apis.similarweb_api import SimilarWebAPI
from apis.harmonic_api import HarmonicAPI
from apis.people_data_labs_api import PeopleDataLabsAPI
from apis.predict_leads_api import PredictLeadsAPI
import os
from dotenv import load_dotenv
from loguru import logger
import regex as re
from utils.preprocessing import transform_data_to_quarterly, preprocess_pdl_enrichment, preprocess_predict_leads_details, preprocess_financing, preprocess_harmonic
from openai     import OpenAI
from pdf_report.generate_benchmark_pdf import generate_benchmark_report

# Load environment variables
load_dotenv()

SIMILARWEB_API_KEY = os.getenv("SIMILARWEB_API_KEY")
HARMONIC_API_KEY = os.getenv("HARMONIC_API_KEY")
PEOPLE_DATA_LABS_API_KEY = os.getenv("PEOPLE_DATA_LABS_API_KEY")
PREDICT_LEADS_API_KEY = os.getenv("PREDICT_LEADS_API_KEY")
PREDICT_LEADS_API_TOKEN = os.getenv("PREDICT_LEADS_API_TOKEN")

def get_data_for_domain(domain):

    similarweb = SimilarWebAPI(SIMILARWEB_API_KEY)
    harmonic = HarmonicAPI(HARMONIC_API_KEY)
    pdl = PeopleDataLabsAPI(PEOPLE_DATA_LABS_API_KEY)
    predict_leads = PredictLeadsAPI(PREDICT_LEADS_API_KEY, PREDICT_LEADS_API_TOKEN)

    # Collect data from SimilarWeb
    try:
        df_similarweb = pd.DataFrame(transform_data_to_quarterly(similarweb.get_total_traffic_and_engagement_visits(domain, "2024-01", "2024-12")))
    except Exception as e:
        df_similarweb = pd.DataFrame([])
        print(f"Error fetching SimilarWeb data: {e}")

    # Collect data from Harmonic
    try:
        investor_list, _ = preprocess_harmonic(harmonic.post_companies(domain))
    except Exception as e:
        investor_list = []
        print(f"Error fetching Harmonic data: {e}")

    # Collect data from People Data Labs
    try:
        df_pdl_enrich = pd.DataFrame(preprocess_pdl_enrichment(pdl.company_enrichment(domain))) 
    except Exception as e:
        df_pdl_enrich = pd.DataFrame([])
        print(f"Error fetching People Data Labs data: {e}")

    # Collect data from PredictLeads
    try:
        df_predict_leads_details = pd.DataFrame(preprocess_predict_leads_details(predict_leads.get_company_details(domain)))
        list_financing = preprocess_financing(predict_leads.get_financing_events(domain))
    except Exception as e:
        df_predict_leads_details = pd.DataFrame([])
        list_financing = []
        print(f"Error fetching PredictLeads data: {e}")

    # Combine all data into a DataFrame
    #logger.info(df_similarweb.shape)
    #logger.info(df_pdl_enrich.shape)
    #logger.info(df_predict_leads_details.shape)

    df_similarweb['key'] = 0
    df_pdl_enrich['key'] = 0
    df_predict_leads_details['key'] = 0

    combined_data = df_similarweb.merge(df_pdl_enrich, on='key', how='outer')
    combined_data = combined_data.merge(df_predict_leads_details, on='key', how='outer')
    combined_data['invester_list'] = str(investor_list)
    combined_data['financing_list'] = str(list_financing)


    return combined_data


def gpt_competitor_domains(domain):

        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

        prompt = f"""
            You are a structured data extraction assistant. Your task is to return a JSON object containing only the domains of competitors for a given company. Always follow this format strictly.

            ## Guidelines:
            1. Return only JSON output with no additional text.
            2. The JSON structure must always be:
            {{"competitors": ["example.com", "example2.com"]}}
            3. The domain names must not include "www." and must be fully lowercase.
            4. Do not include subdomains, paths, or query parameters.
            5. Ensure the response only contains relevant competitors.
            6. No explanations, summaries, or extra text—just the raw JSON.

            ### Examples:

            #### Example 1:
            **Input:** Give me the competitors of revolut.com  
            **Output:** {{"competitors": ["wise.com", "chime.com", "starlingbank.com", "monzo.com", "n26.com", "monese.com", "bunq.com", "vivid.money", "qonto.com", "finom.co"]}}

            #### Example 2:
            **Input:** List competitors of stripe.com  
            **Output:** {{"competitors": ["paypal.com", "adyen.com", "squareup.com", "checkout.com", "braintreepayments.com", "authorize.net", "worldpay.com", "razorpay.com", "stripe-alternative.com"]}}

            #### Example 3:
            **Input:** Who are the competitors of tesla.com?  
            **Output:** {{"competitors": ["ford.com", "gm.com", "bmw.com", "audi.com", "mercedes-benz.com", "volkswagen.com", "rivian.com", "lucidmotors.com", "nio.com", "xpeng.com"]}}

            #### Example 4:
            **Input:** Give me a list of domains for Airbnb competitors  
            **Output:** {{"competitors": ["vrbo.com", "booking.com", "expedia.com", "hotels.com", "tripadvisor.com", "homestay.com", "onefinestay.com", "sonder.com", "plumguide.com"]}}

            ## Final Instructions:
            - Always respond in JSON format.
            - No extra words, headers, or markdown.
            - Ensure the response contains only valid domains of competitors.
            - If no competitors are found, return an empty list: {{"competitors": []}}

            Now, respond to the following query:  
            [List Competitors] {domain}

        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            max_tokens=1000
        )
        import ast
        comp_dict = ast.literal_eval(response.choices[0].message.content.strip())

        cleaned_urls = []
        
        
        for url in comp_dict['competitors']:
            pattern = r"(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})"
            match = re.search(pattern, url)
            if match:
                domain = match.group(1)
            cleaned_urls.append(domain)


        logger.info(cleaned_urls)
            
        return cleaned_urls

def combined_benchmarking():

    domain = 'revolut.com'
    company_df = get_data_for_domain(domain)

    df_list = [company_df]
    
    benchmark_domains = gpt_competitor_domains(domain)

    for comp_domain in benchmark_domains:
        logger.info(comp_domain)
        benchmark_df = get_data_for_domain(comp_domain)
        df_list.append(benchmark_df)

    results_df = pd.concat(df_list, ignore_index=True)

    fields_sorted = [
        # Company Information
        "display_name",
        "alternative_names",
        "summary",
        "headline",
        "tags",
        "industry",

        # Company Size & Employees
        "size",
        "employee_count",
        "employee_count_by_country",

        # Company Location & Language
        "company_website",
        "country",
        "locality",
        "language",    

        # Traffic & Engagement
        "quarter",
        "number_of_visits",

        # Funding & Investment
        "financing_list",
        "total_funding_raised",
        "latest_funding_stage",
        "last_funding_date",
        "number_funding_rounds",
        "funding_stages",
        "invester_list"
    ]

    filtered_df = results_df[fields_sorted]
    logger.info(filtered_df.shape)
    logger.info("Successfully created csv")
    filtered_df.to_csv('dataset/benchmark_db.csv', index=False) #TODO: Do we want to actually always update this db? Or overwrite

    generate_benchmark_report("dataset/benchmark_db.csv", "Revolut")
    logger.info("Generated Report")


if __name__ == '__main__':
    combined_benchmarking()
