import boto3
import json
from botocore.exceptions import ClientError

# Define the names of resources to delete
def load_bucket_name():
    """Load the dynamically generated bucket name from a file."""
    try:
        with open("resources.json", "r") as file:
            data = json.load(file)
        return data.get("bucket_name", None)
    except FileNotFoundError:
        print("resources.json file not found. Ensure the bucket was created and saved correctly.")
        return None

def delete_athena_query_results(bucket_name):
    """Delete Athena query results stored in the specified S3 bucket."""
    s3 = boto3.client("s3")
    try:
        print(f"Deleting Athena query results in bucket: {bucket_name}")
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix="athena-results/")
        if "Contents" in objects:
            for obj in objects["Contents"]:
                s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                print(f"Deleted Athena query result: {obj['Key']}")
    except ClientError as e:
        print(f"Error deleting Athena query results in bucket {bucket_name}: {e}")

def delete_s3_bucket(bucket_name):
    """Delete a specific S3 bucket and its contents."""
    s3 = boto3.client("s3")
    try:
        print(f"Deleting bucket: {bucket_name}")
        # Delete all objects in the bucket
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in objects:
            for obj in objects["Contents"]:
                s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                print(f"Deleted object: {obj['Key']}")
        # Delete the bucket
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Deleted bucket: {bucket_name}")
    except ClientError as e:
        print(f"Error deleting bucket {bucket_name}: {e}")

def delete_glue_resources(database_name):
    """Delete Glue database and associated tables."""
    glue = boto3.client("glue")
    try:
        print(f"Deleting Glue database: {database_name}")
        # Get tables in the database
        tables = glue.get_tables(DatabaseName=database_name)["TableList"]
        for table in tables:
            table_name = table["Name"]
            print(f"Deleting Glue table: {table_name} in database {database_name}")
            glue.delete_table(DatabaseName=database_name, Name=table_name)
        # Delete the database
        glue.delete_database(Name=database_name)
        print(f"Deleted Glue database: {database_name}")
    except ClientError as e:
        print(f"Error deleting Glue resources for database {database_name}: {e}")

def main():
    print("Deleting resources created during data lake setup...")
    # Load bucket name
    bucket_name = load_bucket_name()
    if not bucket_name:
        print("Bucket name not found. Cannot proceed with cleanup.")
        return

    # Define Glue database name
    glue_database_name = "glue_nba_data_lake"  # This can also be dynamically fetched if needed

    # Delete the S3 bucket
    delete_s3_bucket(bucket_name)
    # Delete Glue resources
    delete_glue_resources(glue_database_name)
    # Delete Athena query results
    delete_athena_query_results(bucket_name)

    print("All specified resources deleted successfully.")

if __name__ == "__main__":
    main()
