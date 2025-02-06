#Lambda para Processamento de Arquivos no S3
#Processar CSV e Registrar Dados no CloudWatch

import json
import boto3
import logging
import csv
from io import StringIO

# Configuração do cliente do S3
s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Obter informações do evento (como o bucket e o nome do arquivo)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Baixar o arquivo do S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_file = response['Body'].read().decode('utf-8')
        
        # Processar CSV (exemplo simples de contagem de linhas)
        csv_reader = csv.reader(StringIO(csv_file))
        line_count = sum(1 for row in csv_reader)
        
        # Logar o número de linhas no arquivo CSV
        logger.info(f"O arquivo {file_key} contém {line_count} linhas.")
        
    except Exception as e:
        logger.error(f"Erro ao processar o arquivo {file_key}: {str(e)}")
        raise e
#Lambda para Iniciar um Job do Glue
#Este exemplo mostra uma função Lambda que aciona um AWS Glue Job. Ele pode ser usado para iniciar um processo de ETL sempre que necessário.
#Acionar um Job do Glue via Lambda

import json
import boto3

# Configuração do cliente do Glue
glue_client = boto3.client('glue')

def lambda_handler(event, context):
    job_name = 'my-glue-job'  # Nome do seu job do Glue
    
    try:
        # Iniciar o Glue Job
        response = glue_client.start_job_run(JobName=job_name)
        job_run_id = response['JobRunId']
        
        # Retornar o ID do job que foi iniciado
        return {
            'statusCode': 200,
            'body': json.dumps(f'Job iniciado com sucesso. JobRunId: {job_run_id}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao iniciar o Glue Job: {str(e)}')
        }
#Lambda para Gravar em DynamoDB
#Gravar Dados no DynamoDB

import json
import boto3

# Configuração do cliente do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-dynamo-table')

def lambda_handler(event, context):
    # Obter os dados do corpo da solicitação (supondo um POST)
    body = json.loads(event['body'])
    
    # Dados que queremos gravar
    item = {
        'id': body['id'],
        'name': body['name'],
        'age': body['age']
    }
    
    try:
        # Gravar o item na tabela DynamoDB
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Item gravado com sucesso!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao gravar no DynamoDB: {str(e)}')
        }
#Lambda para Enviar Notificação via SNS

import json
import boto3

# Configuração do cliente SNS
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Definir o tópico SNS para onde enviar a notificação
    sns_topic_arn = 'arn:aws:sns:region:account-id:my-topic'
    
    # Mensagem a ser enviada
    message = 'O processo foi concluído com sucesso.'
    
    try:
        # Enviar a mensagem para o SNS
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='Notificação de Processo'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Notificação enviada com sucesso!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao enviar notificação SNS: {str(e)}')
        }
#Lambda para Validar Dados de Entrada

import json

def lambda_handler(event, context):
    # Obter os dados do corpo da solicitação (supondo que seja um JSON)
    body = json.loads(event['body'])
    
    # Validar dados de entrada
    if 'name' not in body or 'age' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps('Erro: os campos "name" e "age" são obrigatórios.')
        }
    
    # Dados válidos
    return {
        'statusCode': 200,
        'body': json.dumps('Dados válidos recebidos.')
    }
