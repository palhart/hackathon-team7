import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os
import shutil
import ast
import numpy as np


dir_name = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(os.path.dirname(dir_name))

# Function 1: Load the data
def load_data(file_path):
    columns = [
        "company_name", "company_website", "quarter", "Headcount_Count",
        "Headcount_Growth",
        "Fundraising_Total_amount", "Fundraising_Date_of_last_round",
        "Financials_GMV", "Financials_Net_Sales", "Financials_CAC", "tech_employee", "sales_employee" ,"admin_employee", 'year'
    ]

    df = pd.read_csv(file_path, usecols=columns)

    return df


# Function 2: Generate graphs for a company
def generate_graphs(company_name, data):
    df = data[data['company_name'] == company_name].copy()
    
    # Create directory for graphs
    graph_dir = os.path.join(root_path, "graphs")
    if os.path.exists(graph_dir):
        shutil.rmtree(graph_dir)
    os.makedirs(graph_dir, exist_ok=True)

    # Set the style
    sns.set_style("whitegrid")
    
    # Data preparation
    df['index'] = df['quarter'].astype(str) + '-' + df['year'].astype(str)
    df.set_index('index', inplace=True)
    
    # Department renaming
    df.rename(columns={
        'tech_employee': 'tech',
        'sales_employee': 'sales',
        'admin_employee': 'admin'
    }, inplace=True)

    # Create figure with adjusted spacing
    fig = plt.figure(figsize=(15, 12))
    plt.subplots_adjust(bottom=0.2, hspace=0.4)

    # 1. Headcount Growth Over Time
    plt.subplot(2, 2, 1)
    plt.plot(df.index, df['Headcount_Growth'], marker='o', linewidth=2)
    plt.title('Headcount Growth Rate Over Time', fontsize=12, pad=15)
    plt.xlabel('Quarter-Year')
    plt.ylabel('Growth Rate (%)')
    plt.xticks(rotation=90)
    plt.grid(True, alpha=0.3)

    # 2. Department Distribution Stacked Area
    plt.subplot(2, 2, 2)
    departments = ['tech', 'sales', 'admin']
    plt.stackplot(df.index, 
                [df[dept] for dept in departments],
                labels=departments,
                alpha=0.7)
    plt.title('Department Distribution Over Time', fontsize=12, pad=15)
    plt.xlabel('Quarter-Year')
    plt.ylabel('Number of Employees')
    plt.xticks(rotation=90)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)

    # 3. GMV vs CAC Scatter
    plt.subplot(2, 2, 3)
    plt.scatter(df['Financials_GMV'], df['Financials_CAC'], alpha=0.6)
    plt.title('Relationship: GMV vs CAC', fontsize=12, pad=15)
    plt.xlabel('Gross Merchandise Value (GMV)')
    plt.ylabel('Customer Acquisition Cost (CAC)')
    z = np.polyfit(df['Financials_GMV'], df['Financials_CAC'], 1)
    p = np.poly1d(z)
    plt.plot(df['Financials_GMV'], p(df['Financials_GMV']), "r--", alpha=0.8)
    plt.grid(True, alpha=0.3)

    # 4. Department Ratio Over Time
    plt.subplot(2, 2, 4)
    ratio_data = df[departments].div(df[departments].sum(axis=1), axis=0)
    plt.stackplot(df.index, 
                [ratio_data[dept] for dept in departments],
                labels=departments,
                alpha=0.7)
    plt.title('Department Ratio Over Time', fontsize=12, pad=15)
    plt.xlabel('Quarter-Year')
    plt.ylabel('Ratio')
    plt.xticks(rotation=90)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.savefig(f"{graph_dir}/report_graph_{company_name}.png", bbox_inches='tight')
    plt.close(fig)

    return graph_dir

# Function 3: Create a single PDF report for a company
def create_pdf_report(company_name, graph_dir):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Report for {company_name}", ln=True, align="C")
    pdf.ln(20)  # Add some space


    pdf.image(f"{graph_dir}/report_graph_{company_name}.png", x=10, y=40, w=190)


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
    t = generate_report_for_company("dataset/portcos_historical_db.csv", "Revolut")
