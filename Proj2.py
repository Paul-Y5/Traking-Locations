from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

def obter_fuso_horario_gmt(latitude, longitude):
    tf = TimezoneFinder()

    try:
        # Obtém o nome do fuso horário a partir das coordenadas
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)

        if timezone_str:
            # Obtém o objeto de fuso horário usando pytz
            tz = pytz.timezone(timezone_str)
            
            # Obtém o offset atual do fuso horário em relação ao UTC em minutos
            offset_minutes = tz.utcoffset(datetime.now()).seconds // 60

            # Converte o offset para o formato GMT
            offset_hours = offset_minutes // 60
            offset_minutes = offset_minutes % 60
            offset_str = f"{'' if offset_hours >= 0 else '-'}{abs(offset_hours):02d}:{offset_minutes:02d}"

            return offset_str
        else:
            return "Não foi possível determinar o fuso horário para as coordenadas fornecidas."

    except Exception as e:
        return f"Erro ao obter o fuso horário: {str(e)}"

