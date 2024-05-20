import boto3
from datetime import datetime
import time
# https://currentmillis.com/
# unix period was used
# from_unix = 1546308000000 # 2019-01-01 00:00:00 UTC-3
# to_unix = 1715310000000 # 2024-05-10 00:00:00 UTC-3


destination_bucket = 'logs-lambdas-ps'
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_SESSION_TOKEN=""

def list_logs_groups(prefix):
  
   log_groups = []
   paginator = cloudwatch.get_paginator('describe_log_groups')
   for page in paginator.paginate(logGroupNamePrefix = prefix):
       for group in page['logGroups']:
           log_groups.append(group.get('logGroupName'))
  
   return log_groups


CLIENTS = [
   {'client': '', 'from_date': '', 'to_date': '', 'log_groups_prefixes': ['']},
   
]


cloudwatch = boto3.client(
   'logs',
   aws_access_key_id = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   aws_session_token = AWS_SESSION_TOKEN,
   region_name = 'sa-east-1'
)


for client_configs in CLIENTS:
  
   client = client_configs.get('client')
   log_groups_prefixes = client_configs.get('log_groups_prefixes')
  
   from_unix = int(datetime.timestamp(datetime.strptime(client_configs.get('from_date'), '%Y-%m-%d')) * 1000)
   to_unix = int(datetime.timestamp(datetime.strptime(client_configs.get('to_date'), '%Y-%m-%d')) * 1000)
  
   for log_groups_prefix in log_groups_prefixes:
      
       log_groups = list_logs_groups(log_groups_prefix) 
      
         
       for log_group in log_groups:
          
           task_name = f'cloudwatch_s3_logs_{client}_{log_group}_{from_unix}_{to_unix}'.replace('/', '_').replace('-', '_')
 
           while True:
              
               export_tasks_status = []
               for status in ['PENDING_CANCEL', 'PENDING', 'RUNNING']:
                   export_tasks_status.extend(cloudwatch.describe_export_tasks(
                       statusCode = status
                   ).get('exportTasks'))
              
               if not export_tasks_status:
                  
                   print(f'iniciando {task_name}')
          
                   response = cloudwatch.create_export_task(
                       taskName = task_name,
                       logGroupName = log_group,
                       # logStreamNamePrefix = log_group,
                       fromTime = from_unix,
                       to = to_unix,
                       destination = destination_bucket,
                       destinationPrefix = client
                   )
                  
                   break
              
               print(f"Tem task ainda rodando...")
              
               time.sleep(60)



