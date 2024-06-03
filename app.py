from flask import Flask, request, jsonify
from google.cloud import bigquery
import os

# Configure an environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Jakeline\OneDrive\\Área de Trabalho\\GoogleBQ\\newsproject-425223-937f19044577.json"
app = Flask(__name__)

# Set up the BigQuery client
client = bigquery.Client()

# Project name, dataset and table in BigQuery
project_id = "newsproject-425223"
dataset_id = "new_files"
table_id = "articles"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Define the SQL query for BigQuery
    sql_query = f"""
    SELECT title, caption, author, text, url
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE text LIKE @query
    """

    # Set query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("query", "STRING", f"%{query}%")
        ]
    )

    # Run the query
    query_job = client.query(sql_query, job_config=job_config)

    # Collect the results
    results = []
    for row in query_job:
        results.append({
            "title": row.title,
            "caption": row.caption,
            "author": row.author,
            "text": row.text,
            "url": row.url
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
