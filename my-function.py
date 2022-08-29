import pyodbc
import pandas as pd
import boto3


s3_client = boto3.client("s3")
S3_BUCKET = 'sample-bucket-1402'

def lambda_handler(event, context):
  
    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server=ip-rds-database.cduzxn55zeqr.us-west-2.rds.amazonaws.com;"
                "Database=recipes_database;"
                "UID=masterUser;"
                "PWD=iprds123;")
                
    cnxn = pyodbc.connect(cnxn_str)
    
    object_key = "lambda_code/query.txt"
    
    response = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)
    response_df = pd.read_csv(response.get("Body"))
    
    for col in response_df.columns:
      query = col
    data = pd.read_sql(query, cnxn)
    print(data)
    data.to_csv('/tmp/recipes1.csv',index=False)
    print('file created')
    s3_client.upload_file(
        Filename="/tmp/recipes1.csv",
        Bucket="sample-bucket-1402",
        Key="recipes1.csv",
    )
