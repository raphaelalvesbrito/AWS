#Este script lê dados de um arquivo CSV armazenado no S3, faz transformações simples e grava os dados em um banco de dados do Redshift.

import sys
import boto3
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame

# Inicialização do contexto Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Definindo parâmetros
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'REDSHIFT_JDBC_URL', 'REDSHIFT_DB', 'REDSHIFT_TABLE'])

# Leitura do arquivo CSV
s3_input_path = args['S3_INPUT_PATH']
df = spark.read.csv(s3_input_path, header=True, inferSchema=True)

# Conversão para DynamicFrame (formato utilizado pelo AWS Glue)
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

# Transformação (Exemplo simples: seleção de colunas)
dynamic_frame_transformed = dynamic_frame.select_fields(['col1', 'col2', 'col3'])

# Configuração de conexão com o Redshift
redshift_options = {
    "url": args['REDSHIFT_JDBC_URL'],
    "dbtable": args['REDSHIFT_TABLE'],
    "database": args['REDSHIFT_DB']
}

# Gravação no Redshift
glueContext.write_dynamic_frame.from_options(dynamic_frame_transformed, connection_type="redshift", connection_options=redshift_options)

#Leitura de dados do Amazon RDS e gravação no Amazon S3
#Neste script, você lê dados de um banco de dados RDS (MySQL) e escreve os dados transformados no S3.

import sys
import boto3
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame

# Inicialização do contexto Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Definindo parâmetros
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'RDS_CONNECTION', 'S3_OUTPUT_PATH'])

# Leitura do banco de dados RDS
rds_connection_options = {
    "url": args['RDS_CONNECTION'],
    "dbtable": "your_table_name",
    "database": "your_database_name"
}

datasource = glueContext.create_dynamic_frame.from_options(connection_type="mysql", connection_options=rds_connection_options)

# Transformações (Exemplo simples de filtragem)
filtered_dynamic_frame = datasource.filter(lambda x: x['column_name'] == 'desired_value')

# Gravação no S3 em formato Parquet
s3_output_path = args['S3_OUTPUT_PATH']
glueContext.write_dynamic_frame.from_options(filtered_dynamic_frame, connection_type="s3", connection_options={"path": s3_output_path}, format="parquet")

#Leitura de dados JSON do S3, transformação e gravação no Amazon Redshift
#Este exemplo mostra como ler dados JSON do S3, fazer uma transformação simples e gravar no Redshift.

import sys
import boto3
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame

# Inicialização do contexto Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Definindo parâmetros
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_JSON_INPUT_PATH', 'REDSHIFT_JDBC_URL', 'REDSHIFT_DB', 'REDSHIFT_TABLE'])

# Leitura do arquivo JSON no S3
s3_json_input_path = args['S3_JSON_INPUT_PATH']
df = spark.read.json(s3_json_input_path)

# Conversão para DynamicFrame
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

# Transformação (Exemplo de mapeamento de campos)
transformed_dynamic_frame = dynamic_frame.apply_mapping([("old_column1", "string", "new_column1", "string"),
                                                        ("old_column2", "string", "new_column2", "string")])

# Configuração de conexão com o Redshift
redshift_options = {
    "url": args['REDSHIFT_JDBC_URL'],
    "dbtable": args['REDSHIFT_TABLE'],
    "database": args['REDSHIFT_DB']
}

# Gravação no Redshift
glueContext.write_dynamic_frame.from_options(transformed_dynamic_frame, connection_type="redshift", connection_options=redshift_options)

