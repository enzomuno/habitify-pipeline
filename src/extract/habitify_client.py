import requests
import json
from src.config import get_api_key, upload_to_s3_habitify
from src.extract.utils import to_iso8601_21, to_iso8601_23, today_local, actual_date_yyyymmdd

# Defino os parâmetros da API do Habitify
api_key = get_api_key()
url_base = "https://api.habitify.me/"
headers = {
    "Authorization": api_key
}

# Parâmetros de datas que irei usar no params de alguns endpoints, como notes, moods e etc...
actual_date_23 = to_iso8601_23()
actual_date_21 = to_iso8601_21()
actual_date_yyyymmdd = actual_date_yyyymmdd

# Função para tratar erros em qualquer chamada dos endpoints
def handle_request_errors(response):

    if response.status_code != 200:
        raise Exception(f"Erro ao consultar API: {response.status_code} - {response.text}")

    # Converte a resposta para um dicionário Python e então serializa em formato JSON para envio ao bucket
    data = response.json()['data']
    return json.dumps(data)

# Função para consuma dos dados sobre áreas
def get_areas_habitify():

    url_endpoint = f"{url_base}areas"

    try:
        response = requests.get(url=url_endpoint, headers=headers)
        return handle_request_errors(response)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Função para consuma dos dados sobre humores
def get_moods_habitify():

    url_endpoint = f"{url_base}moods"
    params = {"target_date": actual_date_21}

    try:
        response = requests.get(url=url_endpoint, headers=headers, params=params)
        return handle_request_errors(response)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Auxiliar para função get_notes_habitify. Aqui retorno uma lista com os ids de cada hábito existente.
def get_habits_id():
    habits_id = []
    response = requests.get(url=f"{url_base}habits", headers=headers).json()
    for i in response['data']:
        habits_id.append(i["id"])
    return habits_id


# Função para consuma dos dados sobre notas registradas.
def get_notes_habitify():
    all_notes = []
    habits = get_habits_id()

    for habit_id in habits:
        url_endpoint = f"{url_base}notes/{habit_id}"
        params = {
            "from": f"{today_local}T00:00:01-00:00",
            "to": f"{today_local}T23:59:59-00:00"
        }
        try:
            response = requests.get(url=url_endpoint, headers=headers, params=params)
            notes_json = handle_request_errors(response)  # string JSON
            # Converte para lista para checar se está vazia
            notes_list = json.loads(notes_json)

            if notes_list:  # Só adiciona se a lista tiver conteúdo
                all_notes.extend(notes_list)
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para hábito {habit_id}: {e}")
            continue
    return json.dumps(all_notes)


# Função para consuma dos dados sobre os habitos
def get_habits_habitify():
    url_endpoint = f"{url_base}habits"
    try:
        response = requests.get(url=url_endpoint, headers=headers)
        return handle_request_errors(response)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


# Função para consuma dos dados sobre registros dos hábitos diariamente
def get_journal_habitify():
    url_endpoint = f"{url_base}journal"
    params = {"target_date": actual_date_23}
    try:
        response = requests.get(url=url_endpoint, headers=headers, params=params)
        return handle_request_errors(response)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


# Função para envio dos dados de cada endpoint para o S3.
def fetch_and_upload_data():

    print("Iniciando coleta de dados da API Habitify...")
    areas = get_areas_habitify()
    moods = get_moods_habitify()
    notes = get_notes_habitify()
    habits = get_habits_habitify()
    journal = get_journal_habitify()
    print("Dados coletados:")
    

    # Debug gerado pelo Chat GPT para conferir se os dados foram enviados para o S3 
    print("Iniciando envio de dados para o S3...")
    if areas:
        upload_to_s3_habitify(f"habitify_data/{actual_date_yyyymmdd}/areas.json", areas)
        print("✅ Envio de areas.json concluído.")
    else:
        print("⚠️ Nenhum dado disponível para áreas. Upload não realizado.")

    if moods:
        upload_to_s3_habitify(f"habitify_data/{actual_date_yyyymmdd}/moods.json", moods)
        print("✅ Envio de moods.json concluído.")
    else:
        print("⚠️ Nenhum dado disponível para moods. Upload não realizado.")

    if notes:
        upload_to_s3_habitify(f"habitify_data/{actual_date_yyyymmdd}/notes.json", notes)
        print("✅ Envio de notes.json concluído.")
    else:
        print("⚠️ Nenhum dado disponível para notes. Upload não realizado.")
        
    if habits:
        upload_to_s3_habitify(f"habitify_data/{actual_date_yyyymmdd}/habits.json", habits)
        print("✅ Envio de notes.json concluído.")
    else:
        print("⚠️ Nenhum dado disponível para notes. Upload não realizado.")

    if journal:
        upload_to_s3_habitify(f"habitify_data/{actual_date_yyyymmdd}/journal.json", journal)
        print("✅ Envio de notes.json concluído.")
    else:
        print("⚠️ Nenhum dado disponível para notes. Upload não realizado.")