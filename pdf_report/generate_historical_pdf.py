import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os
import shutil


# Function 1: Load the data
def load_data(file_path):
    return pd.read_csv(file_path)

# Function 2: Generate graphs for a company
def generate_graphs(company_name, data):
    company_data = data[data['Company_name'] == company_name]
    
    # Create directory for graphs
    graph_dir = f"graphs"
    if os.path.exists(graph_dir):
        shutil.rmtree(graph_dir)
    os.makedirs(graph_dir, exist_ok=True)

    sns.set_theme(style="whitegrid")

     # Create a single figure for all graphs
    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    # Plot 1: Headcount over time
    sns.lineplot(ax=axes[0], data=company_data, x="years", y="Headcount_Count", hue="quarter", marker="o", linewidth=2.5, palette="tab10")
    axes[0].set_title(f"Headcount Over Time - {company_name}", fontsize=14, weight="bold")
    axes[0].set_xlabel("Year", fontsize=12)
    axes[0].set_ylabel("Headcount Count", fontsize=12)
    axes[0].legend(title="Quarter", fontsize=10, title_fontsize=12, loc="upper left")

    # Plot 2: Fundraising total amount over years
    sns.barplot(ax=axes[1], data=company_data, x="years", y="Fundraising_Total_amount", hue="quarter", palette="coolwarm")
    axes[1].set_title(f"Fundraising Total Amount - {company_name}", fontsize=14, weight="bold")
    axes[1].set_xlabel("Year", fontsize=12)
    axes[1].set_ylabel("Fundraising Total Amount ($)", fontsize=12)
    axes[1].legend(title="Quarter", fontsize=10, title_fontsize=12, loc="upper left")

    # Plot 3: Financials GMV over years
    sns.lineplot(ax=axes[2], data=company_data, x="years", y="Financials_GMV", hue="quarter", marker="o", linewidth=2.5, palette="viridis")
    axes[2].set_title(f"GMV Over Time - {company_name}", fontsize=14, weight="bold")
    axes[2].set_xlabel("Year", fontsize=12)
    axes[2].set_ylabel("GMV ($)", fontsize=12)
    axes[2].legend(title="Quarter", fontsize=10, title_fontsize=12, loc="upper left")

    plt.tight_layout()
    graph_path = f"combined_graphs_{company_name}.png"
    graph_path = os.path.join(graph_dir, graph_path)
    plt.savefig(graph_path)
    plt.close()

    return graph_path

# Function 3: Create a single PDF report for a company
def create_pdf_report(company_name, graph, data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 5, txt=f"Report for {company_name}", ln=True, align="C")

    pdf.image(graph, x=10, y=15, w=190)

    # Save PDF
    pdf_dir = "reports"
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"{company_name}_report.pdf")
    pdf.output(pdf_path)

    return pdf_path

# Main function to generate report for a single company
def generate_report_for_company(file_path, company_name):
    data = load_data(file_path)
    graph = generate_graphs(company_name, data)
    pdf_path = create_pdf_report(company_name, graph, data)
    print(f"Report generated: {pdf_path}")
    return pdf_path