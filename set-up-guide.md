# **BigQuery ML Module - Set-up Guide**

This guide will walk you through the essential steps to set up and run the `bqml_registry` module.

## **Prerequisites**
Before starting with the module setup, ensure you meet the following requirements:

1. **Google Cloud Project with BigQuery**: Ensure that you have a Google Cloud Project with BigQuery enabled. If you are new to BigQuery, you can refer to the official documentation on [how to set up BigQuery]().

2. **Billing Enabled**: BigQuery ML is a paid feature. Ensure that your Google Cloud project has billing enabled. You can enable billing [here](https://cloud.google.com/billing/docs/how-to/modify-project).

3. **Service Account Setup**:
   - Create a service account within your Google Cloud Project.
   - Grant the required permissions to this service account. For detailed instructions, refer to our [permissions class guide](). However, if you want a quick setup, grant the following predefined roles to your service account:
     - BigQuery Data Editor
     - BigQuery Job User
     - BigQuery Read Session User
     - BigQuery Resource Viewer

## **How to run bqml_registry module**

Once you have completed the prerequisites, follow the steps below to run the `bqml_registry` module:

1. **Clone the Repository**:
   ```bash
   git clone [your-github-repo-link]
   ```

2. **Environment Setup**:
   - Before running the module, you need to set up an environment variable to point to the service account credentials. 
   - Depending on your OS, the setup might differ. Below are instructions for common platforms:

     **For Linux/MacOS**:
     ```bash
     export SERVICE_ACCOUNT_CREDENTIALS="/path/to/service-account-file.json"
     ```

     **For Windows** (Using Command Prompt):
     ```cmd
     set SERVICE_ACCOUNT_CREDENTIALS="C:\path\to\service-account-file.json"
     ```

     **For Windows** (Using PowerShell):
     ```powershell
     $env:SERVICE_ACCOUNT_CREDENTIALS="C:\path\to\service-account-file.json"
     ```

---

If you encounter any issues or have feedback, please raise them on our GitHub issues page. Your feedback will help us make improvements!