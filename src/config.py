import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Função para obter a chave da API Habitify
def get_api_key():
    return os.getenv('API_KEY')

# Função para obter o cliente S3
def get_s3_client():

    # Aqui codamos para inicializar o cliente do serviço S3 e posteriomente usar nos uploads para os buckets. eg: upload_to_s3_habitify
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )
    return s3


# Função para realizar o upload dos arquivos para o bucket habitify-data
def upload_to_s3_habitify(s3_key: str, data: dict):

    # Nome do bucket que quero enviar os dados
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME_HABITIFY")
    if not bucket_name:
        print("Nome do bucket não encontrado. Verifique seu arquivo .env.")
        return

    # Inicializa o cliente utilizando a função defina lá em cima
    s3 = get_s3_client()

    # Requisição para enviar os dados
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=data,
            ContentType="application/json"
        )
        print(f"Envio de {s3_key} concluído.")
    except Exception as e:
        print(f"Falha no upload para o S3 ({s3_key}): {e}")