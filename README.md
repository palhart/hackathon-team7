# VC productivity, TEAM 7 

-- Include the part below --
![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)
> -- Include the part above --

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

The application is designed to:

1. **Process Email Attachments**:
   - It scans incoming emails to a specified Gmail account.
   - Processes attachments such as Excel or CSV files.
2. **Generate Reports**:
   - Creates detailed reports and dashboards using the provided data.
   - Reports include visualizations like graphs and summaries.
3. **Send Reports**:
   - Sends the generated reports and dashboards back to the specified recipients.

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

