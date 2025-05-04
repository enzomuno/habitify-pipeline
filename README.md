# 📊 Habitify Data Pipeline

Este repositório contém a pipeline de dados desenvolvida para ingestão, transformação e modelagem dos dados extraídos da API do Habitify. A arquitetura utiliza armazenamento em S3, processamento no Snowflake e transformações com dbt Cloud.

## 🔧 Arquitetura

1. **Coleta (EL)**  
   Os dados são coletados da API do Habitify com um script Python, armazenados em arquivos `.json` no Amazon S3 organizados por data (`YYYYMMDD`).

2. **Ingestão para Snowflake (L)**  
   Uma procedure no Snowflake (`ingest_habitify_data`) é executada diariamente via `TASK`, realizando:
   - **Sobrescrita** das tabelas `areas` e `habits`
   - **Acrescenta dados** nas tabelas `journal`, `moods` e `notes`

3. **Transformação (T)**  
   O dbt Cloud transforma os dados brutos em modelos organizados por camadas:
   - `stg_*`: staging com limpeza e tipagem
   - `core_*`: estruturação de entidades principais
   - `mart_*`: modelos prontos para análise

## ⏱️ Agendamentos

- **GitHub Actions (Python EL)**: roda diariamente às **22:30 BRT** (`01:30 UTC`)
- **Snowflake TASK**: ingestão diária agendada às **01:30 UTC**
- **dbt Cloud Job**: execução diária do pipeline às **02:00 UTC** (23:00 BRT)

## 📦 Tecnologias

- **Python 3.10+**
- **AWS S3**
- **Snowflake**
- **dbt Cloud**
- **GitHub Actions**
