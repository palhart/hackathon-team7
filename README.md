# VC productivity, TEAM 7 

-- Include the part below --
![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)
> -- Include the part above --

## Overview

This project is a comprehensive application designed to process, analyze, and generate reports based on historical data, benchmark datasets, and insights from a Deck PDF file. The application integrates multiple functionalities, including processing email attachments, generating reports, and interacting with cloud-based APIs.

## Prerequisites

Ensure you have the following installed:

1. **Python**: Version 3.8 or higher.
2. **pip**: Python package installer.

---

## Setting up the Environment

### Step 1: Create a `.env` File

In the root directory of your project, create a file named `.env` and include the following environment variables:

```env
OPENAI_API_KEY=<Your OpenAI API Key>
GMAIL_USER=<Your Gmail Address>
GMAIL_PASSWORD=<Your App Password>
```

Replace the placeholders (`<...>`) with your actual values:

- **OPENAI_API_KEY**: Obtain this from OpenAI by signing up and generating an API key.
- **GMAIL_USER**: This is the Gmail address you will use to send emails.
- **GMAIL_PASSWORD**: This is a generated app password. Follow the instructions below to create one.

---

### Step 2: Generate a Gmail App Password

1. **Sign in to Your Google Account**: Go to [Google Account](https://myaccount.google.com/).
2. **Enable 2-Factor Authentication (2FA)**:
   - Navigate to the **Security** section.
   - Under **Signing in to Google**, enable **2-Step Verification** if it’s not already enabled.
3. **Generate an App Password**:
   - In the **Security** section, locate **App Passwords** under the "Signing in to Google" section.
   - You may need to re-enter your password.
   - Click **Generate**. A 16-character app password will be displayed.
   - Copy and use this password as the `GMAIL_PASSWORD` value in your `.env` file.

---

## Application Functionality

### Process Email Attachments:
- Scans incoming emails from a specified Gmail account.
- Processes attachments such as Excel, CSV, and PDF files.

### Generate Reports:
- Produces detailed PDF reports based on the provided data:
  - **Hierarchical PDF Report**: Summarizes insights from the Deck PDF and historical datasets, focusing on trends and organizational data.
  - **Benchmark PDF Report**: Compares the subject company with competitive enterprises using benchmark data.
- Reports include visualizations, graphs, and summaries.

### Send Reports:
- Sends the generated PDF reports back to specified recipients via email.

---

## File Structure
```
.
├── LICENSE
├── README.md
├── apis
│   ├── harmonic_api.py
│   ├── people_data_labs_api.py
│   ├── predict_leads_api.py
│   └── similarweb_api.py
├── backend.py
├── benchmark_pipeline.py
├── csv_file
│   └── harmonic_db.csv
├── dataset
│   ├── benchmark_db.csv
│   ├── grub.py
│   └── portcos_historical_db.csv
├── generator
│   ├── gpt.py
│   └── preprocess.py
├── historical_pipeline.py
├── main.py
├── pdf_report
│   ├── generate_benchmark_pdf.py
│   └── generate_historical_pdf.py
├── requirements.txt
└── utils
    └── preprocessing.py
```

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## Running the Application

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```
--- 

## License
This project is licensed under the terms of the `LICENSE` file.




