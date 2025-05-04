from datetime import datetime, time
import pytz
from datetime import datetime


# Fuso horário local (UTC-3)
local_tz = pytz.timezone('America/Sao_Paulo')
today_local = datetime.now(local_tz).strftime("%Y-%m-%d")

# Data de hoje no formato YYYYMMDD
actual_date_yyyymmdd = datetime.today().strftime('%Y%m%d')

# Fórmula para eu transformar a data para UTC-03:00 e sempre ás 20:59:59. 
# A chamada do endpoint apenas capturar hábitos até esse horário.
def to_iso8601_21():
    

    brazil_tz = pytz.timezone("America/Sao_Paulo")
    current_date = datetime.now(brazil_tz).date()

    # Combinar a data atual com o horário fixo 20:59:59
    fixed_time = time(20, 59, 59)
    result = datetime.combine(current_date, fixed_time)
    localized_result = brazil_tz.localize(result)
    # Formato ISO 8601
    iso_result = localized_result.isoformat()
    return iso_result




# Fórmula para eu transformar a data para UTC-03:00 e sempre ás 20:59:59. 
# A chamada do endpoint apenas capturar hábitos até esse horário.
def to_iso8601_23():

    brazil_tz = pytz.timezone("America/Sao_Paulo")
    current_date = datetime.now(brazil_tz).date()

    # Combinar a data atual com o horário fixo 22:59:59
    fixed_time = time(22, 59, 59)
    result = datetime.combine(current_date, fixed_time)
    localized_result = brazil_tz.localize(result)
    # Formato ISO 8601
    iso_result = localized_result.isoformat()
    return iso_result