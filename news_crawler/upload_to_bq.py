from google.cloud import bigquery
import os

# Configure an environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Jakeline\OneDrive\\Área de Trabalho\\GoogleBQ\\newsproject-425223-937f19044577.json"

def upload_to_bigquery(json_file_path, project_id, dataset_id, table_id):
    # Set up the BigQuery client
    client = bigquery.Client()

    # Define the table ID
    table_id = f"{project_id}.{dataset_id}.{table_id}"
    
    # Define the schema
    schema = [
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("caption", "STRING"),
        bigquery.SchemaField("author", "STRING"),
        bigquery.SchemaField("text", "STRING"),
        bigquery.SchemaField("url", "STRING"),
    ]

    # Define the job configuration
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=False,   # Disable autodetect since we are providing the schema
    )

    # Open the JSON file and load it into BigQuery
    with open(json_file_path, "rb") as source_file:
        load_job = client.load_table_from_file(
            source_file, table_id, job_config=job_config
        )

    # Wait for the load job to complete
    load_job.result()

    print(f"Loaded {load_job.output_rows} rows into {table_id}")

if __name__ == "__main__":
    json_file_path = "articles_utf8.json"
    project_id = "newsproject-425223"
    dataset_id = "new_files"
    table_id = "articles"
    
    upload_to_bigquery(json_file_path, project_id, dataset_id, table_id)
