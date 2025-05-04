from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.config import get_db_conn
from src.extract.utils import to_iso8601_23
import json

# ====FUNCAO PARA REALIZAR INGESTAO DAS AREAS JÁ CADASTRADAS====
def insert_areas_raw(data: list[dict]):
    if not data:
        print("Nenhum dado para inserir.")
        return
    try:
        engine = create_engine(get_db_conn())
        with engine.connect() as conn:
            for item in data:
                query = text("""
                    INSERT INTO raw.areas_habitify (id, name, color, priority, created_at)
                    VALUES (:id, :name, :color, :priority, :created_at)
                    ON CONFLICT (id) DO NOTHING;
                """)
                conn.execute(query, {
                    "id": item["id"],
                    "name": item["name"],
                    "color": item["color"],
                    "priority": item["priority"],
                    "created_at": item["createdAt"]
                })
            conn.commit()
        print(f"{len(data)} registros inseridos com sucesso em raw.areas_habitify.")

    except SQLAlchemyError as e:
        print(f"Erro ao inserir dados no banco: {e}")



# ====FUNCAO PARA REALIZAR INGESTAO DOS 'MOODS' REGISTRADOS NO DIA====
def insert_moods_raw(data: list[dict]):
    if not data:
        print("Nenhum dado para inserir.")
        return
    try:
        engine = create_engine(get_db_conn())
        with engine.connect() as conn:
            for item in data:
                query = text("""
                    INSERT INTO raw.moods_habitify (id, created_at, value)
                    VALUES (:id, :created_at, :value)
                    ON CONFLICT (id) DO NOTHING;
                """)
                conn.execute(query, {
                    "id": item["id"],
                    "created_at": item["created_at"],
                    "value": item["value"]
                })
            conn.commit()
        print(f"{len(data)} registros inseridos com sucesso em raw.moods_habitify.")

    except SQLAlchemyError as e:
        print(f"Erro ao inserir dados no banco: {e}")


# ====FUNCAO PARA REALIZAR INGESTAO DE TODAS 'NOTES' REGISTRADOS PARA CADA HÁBITO NO DIA====
def insert_notes_raw(data: list[dict]):
    if not data:
        print("Nenhum dado para inserir.")
        return
    try:
        engine = create_engine(get_db_conn())
        with engine.connect() as conn:
            for item in data:
                query = text("""
                    INSERT INTO raw.habit_notes_habitify (id, content, created_date, note_type, habit_id)
                    VALUES (:id, :content, :created_date, :note_type, :habit_id)
                    ON CONFLICT (id) DO NOTHING;
                """)
                conn.execute(query, {
                    "id": item["id"],
                    "content": item["content"],
                    "created_date": item["created_date"],
                    "note_type": item["note_type"],
                    "habit_id": item["habit_id"]
                })
            conn.commit()
        print(f"{len(data)} registros inseridos com sucesso em raw.habit_notes_habitify.")

    except SQLAlchemyError as e:
        print(f"Erro ao inserir dados no banco: {e}")



# ====FUNCAO PARA REALIZAR INGESTAO DE TODOS 'HABITS' CADASTRADOS====
def insert_habits_raw(data: list[dict]):
    if not data:
        print("Nenhum dado para inserir.")
        return
    
    try:
        # Estabelece conexão com o banco de dados
        engine = create_engine(get_db_conn())
        with engine.connect() as conn:
            for item in data:
                query = text("""
                    INSERT INTO raw.habits_habitify (
                        id, name, is_archived, start_date, time_of_day, goal, 
                        goal_history_items, log_method, recurrence, remind, 
                        area, created_date, priority
                    ) VALUES (
                        :id, :name, :is_archived, :start_date, :time_of_day, :goal, 
                        :goal_history_items, :log_method, :recurrence, :remind, 
                        :area, :created_date, :priority
                    )
                    ON CONFLICT (id) DO NOTHING;  -- Evita duplicação de dados
                """)

                # Convertendo os campos do tipo dict/list para JSON
                conn.execute(query, {
                    "id": item["id"],
                    "name": item["name"],
                    "is_archived": item["is_archived"],
                    "start_date": item["start_date"],
                    "time_of_day": json.dumps(item["time_of_day"]),  # Convertendo lista para JSON
                    "goal": json.dumps(item["goal"]),  # Convertendo dict para JSON
                    "goal_history_items": json.dumps(item["goal_history_items"]),  # Convertendo lista de dict para JSON
                    "log_method": item["log_method"],
                    "recurrence": item["recurrence"],
                    "remind": json.dumps(item["remind"]),  # Convertendo lista para JSON
                    "area": json.dumps(item["area"]) if item["area"] is not None else None,
                    "created_date": item["created_date"],
                    "priority": item["priority"]
                })
            conn.commit()
        
        print(f"{len(data)} registros inseridos com sucesso em raw.habits_habitify.")

    except SQLAlchemyError as e:
        print(f"Erro ao inserir dados no banco: {e}")

# ====FUNCAO PARA REALIZAR INGESTAO DE TODAS 'JOURNAL' REGISTRADOS PARA CADA HÁBITO NO DIA====
def insert_journal_raw(data: list[dict]):
    if not data:
        print("Nenhum dado para inserir.")
        return
    
    try:
        # Estabelece conexão com o banco de dados
        engine = create_engine(get_db_conn())
        with engine.connect() as conn:
            for item in data:
                query = text("""
                    INSERT INTO raw.journal_habitify (
                        id, progress, created_at
                    ) VALUES (
                        :id, :progress, :created_at
                    )
                """)

                # Convertendo os campos do tipo dict/list para JSON
                conn.execute(query, {
                    "id": item["id"],
                    "progress": json.dumps(item["progress"]),  # Convertendo dict para JSON
                    "created_at": to_iso8601_23()
                })
            conn.commit()
        
        print(f"{len(data)} registros inseridos com sucesso em raw.journal_habitify.")

    except SQLAlchemyError as e:
        print(f"Erro ao inserir dados no banco: {e}")