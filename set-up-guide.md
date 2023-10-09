# **BigQuery ML Module - Set-up Guide**

This guide will walk you through the essential steps to set up and run the `bqml_registry` module.

## **Prerequisites**
Before starting with the module setup, ensure you meet the following requirements:

1. **Google Cloud Project with BigQuery**: Ensure that you have a Google Cloud Project with BigQuery enabled. If you are new to BigQuery, you can refer to the official documentation on [how to set up BigQuery](https://cloud.google.com/bigquery/docs/quickstarts).

2. **Billing Enabled**: BigQuery ML is a paid feature. Ensure that your Google Cloud project has billing enabled. You can enable billing [here](https://cloud.google.com/billing/docs/how-to/modify-project).

3. **Service Account Setup**:
   - Create a service account within your Google Cloud Project.
   - Grant the required permissions to this service account. For detailed instructions, refer to the [permissions class](bqml_registry/permissions.py). However, if you want a quick setup, grant the following predefined roles to your service account:
     - BigQuery Data Editor
     - BigQuery Job User
     - BigQuery Read Session User
     - BigQuery Resource Viewer

## **How to run bqml_registry module**

Once you have completed the prerequisites, follow the steps below to run the `bqml_registry` module:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/chrisbudnik/bigquery-ml-model-registry
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

## Testing Permissions with `BigQueryConnector`

Once you have set up your environment and ensured all prerequisites are in place, you can easily verify if your service account has the necessary permissions. To do this, simply initialize the `BigQueryConnector` from the `bqml_registry` module. 

```python
from bqml_registry import BigQueryConnector
connector = BigQueryConnector()
```

Upon initialization, the `BigQueryConnector` automatically checks for the required permissions. If there are any missing permissions or issues, it will notify you, ensuring that all criteria are met before you proceed with further operations.

---

If you encounter any issues or have feedback, please raise them on our GitHub issues page. Your feedback will help us make improvements!