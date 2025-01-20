# NBADataLake

This repository includes the `setup_nba_data_lake.py` script, designed to automate the creation of a data lake for NBA analytics using AWS services. The script seamlessly integrates Amazon S3, AWS Glue, and Amazon Athena to set up the infrastructure required to store, process, and query NBA-related data.

---

## Overview

The `setup_nba_data_lake.py` script simplifies the creation of a data lake for NBA analytics using AWS services. This script leverages Amazon S3, AWS Glue, and Amazon Athena to establish the necessary infrastructure for storing, processing, and querying NBA-related data. Key functionalities include:

- Creating an Amazon S3 bucket for storing raw and processed data.
- Uploading sample NBA data (in JSON format) to the S3 bucket.
- Setting up an AWS Glue database and an external table for querying the data.
- Configuring Amazon Athena to enable data queries directly from the S3 bucket.
- **`resources.json` file** keeps track of the dynamically generated S3 bucket name for later use.

---

## Prerequisites

Before executing the script, ensure the following requirements are met:

1. **Python Installed**
   - Ensure Python is installed on your system. You can verify this by running:
     ```bash
     python3 --version
     ```

2. **SportsData.io Account**
   - Sign up for a free account at [SportsData.io](https://sportsdata.io).
   - Navigate to the **Developers** section and locate **API Resources**.
   - Opt for the **SportsDataIO API Free Trial**, provide the required information, and select NBA for this tutorial.
   - After receiving the confirmation email, access the **Developer Portal**, switch to the NBA section, and retrieve your API key from the **Standings** section under **Query String Parameters**.
   - Save the API key for later use in the script.

3. **AWS IAM Role/Permissions**
   - The user or role executing the script must have the following AWS permissions:
     - **S3:** `s3:CreateBucket`, `s3:PutObject`, `s3:DeleteBucket`, `s3:ListBucket`
     - **Glue:** `glue:CreateDatabase`, `glue:CreateTable`, `glue:DeleteDatabase`, `glue:DeleteTable`
     - **Athena:** `athena:StartQueryExecution`, `athena:GetQueryResults`

4. **AWS CLI Configuration**
   - Ensure your terminal is configured with AWS credentials for the desired user or role. You can do this by running:
     ```bash
     aws configure
     ```
   - Provide the appropriate access key, secret access key, and default region during configuration.

---

## Steps to Run the Project

1. **Clone the Repository**  
   Clone this repository and navigate to the project directory:  
   ```bash
   git clone https://github.com/hardikgandhi03/NBA-data-lake.git
   cd NBA-data-lake
   ```

## Steps to Set Up the NBA Data Lake

2. **Create `.env` File**  
   Create a `.env` file in the project directory with the following contents:  
   ```bash
    SPORTS_DATA_API_KEY=your_sportsdata_api_key
    NBA_ENDPOINT=https://api.sportsdata.io/v3/nba/scores/json/Players
    AWS_REGION=the_region_you_prefer
    AWS_BUCKET_NAME=sports-analytics-data-lake
    GLUE_DATABASE_NAME=glue_nba_data_lake
   ```

3. **Run the Setup Script** 
    Run the setup script to create the required AWS resources:
    ```bash
    python3 setup_nba_data_lake.py
    ```
After the script completes, the S3 bucket, Glue database, and Athena configuration will be successfully created.


4. **Verify Created Resources**  

    Amazon S3:
    Open the S3 Console in the AWS Management Console. Confirm that a uniquely named bucket has been created. Inside the bucket, you should find a folder named raw-data containing the nba_player_data.json file.

    Amazon Athena:
    Go to the Athena Console and run the following query to confirm that data has been correctly set up:

    ```sql
    SELECT FirstName, LastName, Position, Team
    FROM nba_players
    WHERE Position = 'PG';
    ```

    - Click Run -You should see an output if you scroll down under "Query Results"