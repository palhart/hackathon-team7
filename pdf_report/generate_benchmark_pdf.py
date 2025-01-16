import pandas as pd
from fpdf import FPDF
import os
import shutil
import ast
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


dir_name = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(os.path.dirname(dir_name))

# Function 1: Load the data
def load_data(file_path):
    columns = [
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
    df = pd.read_csv(file_path, usecols=columns)

    return df

def generate_benchmark_graphs(company_name, df):
    
    # Convert company name to lowercase for consistency
    company_name = company_name.lower()
    
    # Create directory for graphs
    graph_dir = os.path.join("graphs", company_name)
    if os.path.exists(graph_dir):
        shutil.rmtree(graph_dir)
    os.makedirs(graph_dir, exist_ok=True)

    # Data Cleaning
    df = df.dropna(subset=['display_name', 'number_of_visits'])
    df['number_of_visits'] = pd.to_numeric(df['number_of_visits'], errors='coerce')
    df['quarter'] = df['quarter'].astype(str)
    df_grouped = df.groupby('display_name').first().reset_index()

    # Graphs
    figures = [
        (px.line(df.sort_values(['display_name', 'quarter']), x='quarter', y='number_of_visits', color='display_name',
                 title="Web Traffic Over Time", labels={"number_of_visits": "Number of Visits", "quarter": "Quarter"}),
         "web_traffic_trend.png"),

        (px.bar(df_grouped.sort_values('total_funding_raised', ascending=False), x="display_name", y="total_funding_raised",
                title="Total Funding Raised per Company", labels={"total_funding_raised": "Total Funding (€)"}),
         "total_funding_raised.png"),

        (px.bar(df_grouped.sort_values('employee_count', ascending=False), x="display_name", y="employee_count",
                title="Number of Employees per Company", labels={"employee_count": "Employee Count"}),
         "employee_count.png"),

        (px.pie(df_grouped, names="latest_funding_stage", title="Funding Stage Distribution"), "funding_stage_distribution.png"),

        (px.pie(df_grouped, names="display_name", values="number_of_visits", title="Website Traffic Share"), "website_traffic_share.png"),

        (px.bar(df_grouped.sort_values('number_funding_rounds', ascending=False), x="display_name", y="number_funding_rounds",
                title="Number of Funding Rounds per Company"), "funding_rounds.png"),

        (px.scatter(df_grouped, x="employee_count", y="total_funding_raised", color="display_name",
                    title="Employees vs. Funding Raised", labels={"employee_count": "Employees", "total_funding_raised": "Funding (€)"},
                    log_x=True), "employees_vs_funding.png"),

        (px.bar(df.groupby('display_name').agg({'number_of_visits': 'sum'}).reset_index()
                 .sort_values('number_of_visits', ascending=False), x="display_name", y="number_of_visits",
                 title="Total Web Traffic Growth per Company"), "web_traffic_growth.png"),

        (px.pie(df_grouped, names="display_name", values="employee_count", title="Employee Distribution"), "employee_distribution.png"),

        (px.bar(df, x="quarter", y="number_of_visits", color="display_name", title="Website Traffic Change by Quarter"),
         "web_traffic_quarterly.png"),

        (px.pie(df_grouped[df_grouped['total_funding_raised'] > df_grouped['total_funding_raised'].median()],
                names="latest_funding_stage", title="Funding Stage Breakdown for Top Companies"), "funding_stage_top_companies.png"),

        (px.scatter(df_grouped, x="number_of_visits", y="total_funding_raised", color="latest_funding_stage",
                    title="Funding vs. Web Traffic Growth", labels={"number_of_visits": "Web Traffic", "total_funding_raised": "Funding (€)"}),
         "funding_vs_web_traffic.png"),

        (px.scatter(df_grouped.sort_values('last_funding_date'), x="last_funding_date", y="display_name", color="display_name",
                    title="Most Recent Funding Date per Company", labels={"last_funding_date": "Last Funding Date", "display_name": "Company"},
                    size_max=15), "funding_timeline.png"),

        (px.scatter(df_grouped, x="total_funding_raised", y="employee_count", color="display_name",
                    title="Funding Raised vs. Employee Count", labels={"total_funding_raised": "Total Funding (€)", "employee_count": "Employee Count"},
                    log_x=True, log_y=True), "funding_vs_employees.png"),

        (px.scatter(df_grouped, x="total_funding_raised", y="number_of_visits", color="display_name",
                    title="Web Traffic vs. Funding Raised", labels={"total_funding_raised": "Total Funding (€)", "number_of_visits": "Web Traffic"},
                    log_x=True, log_y=True), "web_traffic_vs_funding.png"),

        (px.scatter(df_grouped, x="number_funding_rounds", y="total_funding_raised", color="display_name",
                    title="Funding Rounds vs. Funding Raised", labels={"number_funding_rounds": "Number of Funding Rounds", "total_funding_raised": "Total Funding (€)"}),
         "funding_rounds_vs_funding.png")
    ]

    # Save each figure to the graph directory
    for fig, filename in figures:
        fig.update_layout(
            legend=dict(
                orientation="h",  # Make the legend horizontal
                yanchor="top",    # Anchor the legend from the top
                y=-0.4,           # Move it further down to avoid overlapping
                xanchor="center", # Center the legend
                x=0.5             # Keep it centered horizontally
            ),
            margin=dict(b=100)  # Add extra bottom margin to avoid overlap
        )
        fig.write_image(os.path.join(graph_dir, filename))

    return graph_dir


def create_pdf_report(company_name, graph_dir):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Report for {company_name}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"This report provides a detailed analysis of {company_name}'s performance metrics.")
    pdf.ln(10)
    
    graph_mappings = {
        "Web Traffic Over Time": "web_traffic_trend.png",
        "Total Funding Raised per Company": "total_funding_raised.png",
        "Number of Employees per Company": "employee_count.png",
        "Funding Stage Distribution": "funding_stage_distribution.png",
        "Website Traffic Share": "website_traffic_share.png",
        "Number of Funding Rounds per Company": "funding_rounds.png",
        "Employees vs. Funding Raised": "employees_vs_funding.png",
        "Total Web Traffic Growth per Company": "web_traffic_growth.png",
        "Employee Distribution": "employee_distribution.png",
        "Website Traffic Change by Quarter": "web_traffic_quarterly.png",
        "Funding Stage Breakdown for Top Companies": "funding_stage_top_companies.png",
        "Funding vs. Web Traffic Growth": "funding_vs_web_traffic.png",
        "Funding Raised vs. Employee Count": "funding_vs_employees.png",
        "Web Traffic vs. Funding Raised": "web_traffic_vs_funding.png",
        "Funding Rounds vs. Funding Raised": "funding_rounds_vs_funding.png"
    }

    
    for title, filename in graph_mappings.items():
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt=title, ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"This graph illustrates {title.lower()}.")
        pdf.image(os.path.join(graph_dir, filename), x=10, y=50, w=190)
        pdf.ln(130)
    
    pdf_dir = os.path.join(root_path, "reports")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"{company_name}_report.pdf")
    pdf.output(pdf_path)
    
    return pdf_path

# Main function to generate report for a single company
def generate_benchmark_report(file_path, company_name):

    data = load_data(file_path)
    graph = generate_benchmark_graphs(company_name, data)
    pdf_path = create_pdf_report(company_name, graph)
    print(f"Report generated: {pdf_path}")
    
    return pdf_path


if __name__ == '__main__':
    #t = generate_report_for_company("dataset/portcos_historical_db.csv", "Databricks")
    t_benchmark = generate_benchmark_report("../dataset/benchmark_db.csv", "Revolut")
