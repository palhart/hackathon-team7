import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os
import shutil
import ast


dir_name = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(os.path.dirname(dir_name))

# Function 1: Load the data
def load_data(file_path):
    columns = [
        "company_name", "company_website", "quarter", "Headcount_Count",
        "Headcount_Growth", "Headcount_Breakdown_of_employees",
        "Fundraising_Total_amount", "Fundraising_Date_of_last_round",
        "Financials_GMV", "Financials_Net_Sales", "Financials_CAC"
    ]

    df = pd.read_csv(file_path, usecols=columns)

    df_breakdown = df['Headcount_Breakdown_of_employees'].apply(ast.literal_eval).apply(pd.Series)

    final_df = pd.concat([df, df_breakdown], axis=1)
    final_df = final_df.drop(['Headcount_Breakdown_of_employees'], axis=1)

    final_df['year'] = final_df['quarter'].str.extract(r'(\d{4})').astype(int)
    
    
    final_df['quarter'] = final_df['quarter'].str.extract(r'Q(\d)').astype(int)

    return final_df


# Function 2: Generate graphs for a company
def generate_graphs(company_name, data):
   
    company_data = data[data['company_name'] == company_name].copy()
    company_data['Year'] = company_data['quarter'].str.extract(r'(\d{4})').astype(int)


    
    # Create directory for graphs
    graph_dir = os.path.join(root_path, "graphs")
    if os.path.exists(graph_dir):
        shutil.rmtree(graph_dir)
    os.makedirs(graph_dir, exist_ok=True)

    sns.set_theme(style="whitegrid")

    # Create a single figure for all graphs
    fig, axes = plt.subplots(4, 1, figsize=(12, 20), sharex=True)

    # Graph 1: Headcount Over Time
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=company_data, x="Year", y="Headcount_Count", marker="o", linewidth=2.5, label="Headcount")
    sns.lineplot(data=company_data, x="Year", y="Headcount_Growth", linestyle="--", label="Growth (%)")
    plt.title("Headcount and Growth Over Time", fontsize=14, weight="bold")
    plt.xlabel("Year")
    plt.ylabel("Headcount / Growth")
    plt.legend(title="Metrics")
    description = "This graph shows the changes in headcount and growth percentage over time."
    plt.figtext(0.5, -0.1, description, wrap=True, horizontalalignment='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{graph_dir}/headcount_graph_{company_name}.png")
    plt.close()

    # Graph 2: Fundraising Total Amount Over Time
    plt.figure(figsize=(8, 6))
    sns.barplot(data=company_data, x="Year", y="Fundraising_Total_amount", hue="quarter", palette="coolwarm", dodge=False)
    plt.title("Fundraising Total Amount Over Time", fontsize=14, weight="bold")
    plt.xlabel("Year")
    plt.ylabel("Fundraising Total Amount ($)")
    plt.legend(title="Quarter")
    description = "This bar graph illustrates the total amount raised by the company, grouped by year and quarter."
    plt.figtext(0.5, -0.1, description, wrap=True, horizontalalignment='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{graph_dir}/fundraising_graph_{company_name}.png")
    plt.close()

    # Graph 3: GMV vs Net Sales Over Time
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=company_data, x="Year", y="Financials_GMV", marker="o", linewidth=2.5, label="GMV")
    sns.lineplot(data=company_data, x="Year", y="Financials_Net_Sales", linestyle="--", label="Net Sales")
    plt.title("GMV vs Net Sales Over Time", fontsize=14, weight="bold")
    plt.xlabel("Year")
    plt.ylabel("Financials ($)")
    plt.legend(title="Metrics")
    description = "This graph compares GMV (Gross Merchandise Value) and net sales performance over time."
    plt.figtext(0.5, -0.1, description, wrap=True, horizontalalignment='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{graph_dir}/gmv_net_sales_graph_{company_name}.png")
    plt.close()

    # Graph 4: Customer Acquisition Cost (CAC) Over Time
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=company_data, x="Year", y="Financials_CAC", marker="o", linewidth=2.5, color="orange", label="CAC")
    plt.title("Customer Acquisition Cost (CAC) Over Time", fontsize=14, weight="bold")
    plt.xlabel("Year")
    plt.ylabel("CAC ($)")
    description = "This graph shows the trend of customer acquisition costs over the years."
    plt.figtext(0.5, -0.1, description, wrap=True, horizontalalignment='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{graph_dir}/cac_graph_{company_name}.png")
    plt.close()

    return graph_dir


# Function 3: Create a single PDF report for a company
def create_pdf_report(company_name, graph_dir):


    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Report for {company_name}", ln=True, align="C")
    pdf.ln(10)  # Add some space

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=(
        f"This report provides a detailed analysis of {company_name}'s performance metrics. "
        f"The following graphs visualize trends in headcount, growth, fundraising, financials, and customer acquisition costs over time."
    ))
    pdf.ln(10)  # Add some space

    # Graph 1: Headcount and Growth Over Time
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Headcount and Growth Over Time", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This graph shows the changes in headcount and growth percentage over time.")
    pdf.image(f"{graph_dir}/headcount_graph_{company_name}.png", x=10, y=50, w=190)
    pdf.ln(130)

    # Graph 2: Fundraising Total Amount Over Time
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Fundraising Total Amount Over Time", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This bar graph illustrates the total amount raised by the company, grouped by year and quarter.")
    pdf.image(f"{graph_dir}/fundraising_graph_{company_name}.png", x=10, y=50, w=190)
    pdf.ln(130)

    # Graph 3: GMV vs Net Sales Over Time
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="GMV vs Net Sales Over Time", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This graph compares GMV (Gross Merchandise Value) and net sales performance over time.")
    pdf.image(f"{graph_dir}/gmv_net_sales_graph_{company_name}.png", x=10, y=50, w=190)
    pdf.ln(130)

    # Graph 4: Customer Acquisition Cost (CAC) Over Time
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Customer Acquisition Cost (CAC) Over Time", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This graph shows the trend of customer acquisition costs over the years.")
    pdf.image(f"{graph_dir}/cac_graph_{company_name}.png", x=10, y=50, w=190)
    pdf.ln(130)



    # Save PDF
    pdf_dir = os.path.join(root_path, "reports")
    pdf_path = f"{pdf_dir}/{company_name}_report.pdf"
    pdf.output(pdf_path)

    return pdf_path


# Main function to generate report for a single company
def generate_report_for_company(file_path, company_name):

    data = load_data(file_path)
    graph = generate_graphs(company_name, data)
    pdf_path = create_pdf_report(company_name, graph)
    print(f"Report generated: {pdf_path}")
    return pdf_path


if __name__ == '__main__':
    t = generate_report_for_company("dataset/portcos_historical_db.csv", "Databricks")
