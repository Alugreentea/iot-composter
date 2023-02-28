import boto3

# Create an IoT Analytics client
client = boto3.client('iotanalytics', 
                      region_name='ap-northeast-1', 
                      aws_access_key_id='YOUR_ACCESS_KEY_ID', 
                      aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')

# specify the name of your Datastore and the SQL query to execute
datastore_name = 'cocostore'
query = 'SELECT * FROM "' + datastore_name + '"'

# execute the query and get the results
response = client.describe_datastore(datastoreName=datastore_name)
s3_bucket = response['datastoreStorage']['customerManagedS3']['bucket']
s3_key_prefix = response['datastoreStorage']['customerManagedS3']['keyPrefix']
s3_location = 's3://' + s3_bucket + '/' + s3_key_prefix

response = client.start_query_execution(
    datasetName=datastore_name,
    sqlQuery=query,
    resultConfiguration={
        'OutputLocation': s3_location
    }
)

query_execution_id = response['queryExecutionId']

response = client.get_query_execution(
    queryExecutionId=query_execution_id
)

query_status = response['queryExecution']['status']['state']

if query_status == 'SUCCEEDED':
    s3_output_location = response['queryExecution']['resultConfiguration']['outputLocation']
    s3_output_bucket = s3_output_location.split('/')[2]
    s3_output_prefix = '/'.join(s3_output_location.split('/')[3:])
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_output_bucket)
    objs = list(bucket.objects.filter(Prefix=s3_output_prefix))
    if len(objs) > 0:
        s3_key = objs[0].key
        s3_object = s3.Object(s3_output_bucket, s3_key)
        csv_data = s3_object.get()['Body'].read().decode('utf-8')
        print(csv_data)
    else:
        print('No data found.')
else:
    print('Query failed.')
