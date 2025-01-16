from backend import get_data_for_domain, gpt_competitor_domains
from pdf_report.generate_benchmark_pdf import generate_benchmark_report
from loguru import logger
import pandas as pd

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

    pdf_path = generate_benchmark_report("dataset/benchmark_db.csv", "Revolut")
    logger.info("Generated Report")

    return pdf_path


