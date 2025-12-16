# File: bq_csv_loader.py
import argparse
import os
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError

def load_csv_to_bigquery(
    client: bigquery.Client,
    csv_path: str,
    dataset_id: str,
    write_mode: str = "WRITE_APPEND",
) -> bool:
    """
    Parses a CSV file with pandas and loads it into a BigQuery table.

    The target table name is derived from the CSV filename.

    Args:
        client: An authenticated BigQuery client instance.
        csv_path: The full path to the .csv file.
        dataset_id: The BigQuery dataset ID to load the data into.
        write_mode: The write disposition ('WRITE_TRUNCATE', 'WRITE_APPEND', 'WRITE_EMPTY').

    Returns:
        True if the load job was successful, False otherwise.
    """
    # Derive table_id from the CSV filename (e.g., 'customers.csv' -> 'customers')
    table_id = os.path.splitext(os.path.basename(csv_path))[0]
    full_table_id = f"{client.project}.{dataset_id}.{table_id}"

    print(f"-> Processing '{csv_path}' for table '{full_table_id}'...")

    try:
        # 1. EXTRACT & TRANSFORM: Use pandas to read and clean the CSV
        # This is where you can add powerful data transformations.
        df = pd.read_csv(csv_path)

        # --- Data Cleaning & Transformation (Optional but Recommended) ---
        # Example: Convert date columns to the correct pandas dtype
        if 'signup_date' in df.columns:
            df['signup_date'] = pd.to_datetime(df['signup_date'])
        
        # Example: Clean up column names (remove spaces, convert to lowercase)
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        if df.empty:
            print("   [SKIP] CSV file is empty. No data to load.")
            return True

        # 2. LOAD: Configure and run the BigQuery Load Job
        # This configuration gives you control over the loading process.
        job_config = bigquery.LoadJobConfig(
            # Overwrite the table if it exists
            write_disposition=write_mode,
            # The source format is inferred from the dataframe, but can be set
            # source_format=bigquery.SourceFormat.CSV, 
            
            # Let BigQuery automatically detect the schema from the dataframe
            autodetect=True, 
            # Or, for production, explicitly define the schema for reliability
            # schema=[
            #     bigquery.SchemaField("customer_id", "INTEGER"),
            #     bigquery.SchemaField("first_name", "STRING"),
            #     ...
            # ]
        )

        # The load_table_from_dataframe method handles creating the job
        # and waiting for it to complete.
        load_job = client.load_table_from_dataframe(
            df, full_table_id, job_config=job_config
        )

        # Wait for the job to complete
        load_job.result()

        # 3. VERIFY: Check the results and report
        destination_table = client.get_table(full_table_id)
        print(
            f"   [SUCCESS] Loaded {destination_table.num_rows} rows into '{full_table_id}'."
        )
        return True

    except FileNotFoundError:
        print(f"   [ERROR] File not found: {csv_path}")
        return False
    except GoogleCloudError as e:
        print(f"   [ERROR] BigQuery API error for '{table_id}': {e}")
        return False
    except Exception as e:
        print(f"   [ERROR] An unexpected error occurred with '{csv_path}': {e}")
        return False

def main():
    """Main function to parse arguments and start the CSV loading process."""
    parser = argparse.ArgumentParser(description="Load CSV files from a directory into BigQuery.")
    parser.add_argument("--project-id", required=True, help="The Google Cloud Project ID.")
    parser.add_argument("--dataset-id", required=True, help="The target BigQuery Dataset ID.")
    parser.add_argument("--data-dir", required=True, help="The directory containing the .csv files.")
    parser.add_argument(
        "--write-mode",
        choices=["WRITE_APPEND", "WRITE_TRUNCATE"],
        default="WRITE_APPEND",
        help=(
            "WRITE_APPEND to add to the table, "
            "WRITE_TRUNCATE to overwrite the table. Defaults to APPEND."
        ),
    )
    args = parser.parse_args()

    try:
        client = bigquery.Client(project=args.project_id)
        print(f"Authenticated to BigQuery project '{args.project_id}'.\n")
    except Exception as e:
        print(f"Could not create BigQuery client. Check authentication. Error: {e}")
        return

    csv_files = [
        os.path.join(args.data_dir, f)
        for f in os.listdir(args.data_dir)
        if f.endswith('.csv')
    ]

    if not csv_files:
        print(f"No .csv files found in '{args.data_dir}'.")
        return

    success_count = 0
    failure_count = 0
    for file_path in sorted(csv_files):
        if load_csv_to_bigquery(client, file_path, args.dataset_id, args.write_mode):
            success_count += 1
        else:
            failure_count += 1
    
    print("\n--- Summary ---")
    print(f"Total files processed: {len(csv_files)}")
    print(f"Successful loads: {success_count}")
    print(f"Failed loads: {failure_count}")
    print("---------------")

    if failure_count > 0:
        exit(1) # Exit with an error code for CI/CD pipelines

if __name__ == "__main__":
    main()

