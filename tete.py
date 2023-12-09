from timezonefinder import TimezoneFinder 

latitude = 2
longitude = 48
fuso_horario = TimezoneFinder().timezone_at(lng=latitude, lat=longitude)

print(fuso_horario)