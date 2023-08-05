from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from server.tasks import run_code

import subprocess
import pandas as pd
import requests


@api_view(['GET'])
def ping(request):
    return Response('pong')


@api_view(['POST'])
def update(request):
    subprocess.run(["/home/ubuntu/parsagon/parsagon-local-server/bin/parsagon-server-update"])
    return Response('OK')


@api_view(['POST'])
def read_db(request):
    db_type = request.data['db_type']
    db_name = request.data['db_name']
    user = request.data['db_user']
    password = request.data['db_password']
    host = request.data['db_host']
    port = request.data['db_port']
    table = request.data['table']
    schema = request.data['schema']

    con = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    df_iter = pd.read_sql_table(table, con=con, schema=schema, chunksize=100)
    df = next(df_iter)
    result = df.to_dict(orient='records')

    return Response(result)


@api_view(['POST'])
def write_db(request):
    db_type = request.data['db_type']
    db_name = request.data['db_name']
    user = request.data['db_user']
    password = request.data['db_password']
    host = request.data['db_host']
    port = request.data['db_port']
    table = request.data['table']
    schema = request.data['schema']

    con = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    return Response('OK')


@api_view(['POST'])
def fetch_web(request):
    r = requests.post('http://localhost:8001/', json={'action': 'fetch-web', 'params': request.data})
    if r.ok:
        output = r.json()
        return Response(output)
    else:
        return Response('ERROR', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def fetch_web_action(request):
    r = requests.post('http://localhost:8001/', json={'action': 'fetch-web-action', 'params': request.data})
    if r.ok:
        output = r.json()
        return Response(output)
    else:
        return Response('ERROR', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def run_pipeline(request):
    run_code.delay(request.data['run_id'])
    return Response('OK')
