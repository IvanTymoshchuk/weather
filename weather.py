import tkinter as tk
import requests
import geocoder
from PIL import Image, ImageTk

# Переводимо код погоди в код зображення на openweathermap.org
wmo_to_icon = {
    0: "01d",  # Ясне небо
    1: "01d",  # Ясне небо
    2: "02d",  # Трохи хмар
    3: "03d",  # Розсіяна хмарність
    4: "04d",  # Розсіяна хмарність
    45: "50d",  # Туман
    48: "50d",  # Туман
    61: "10d",  # Дощ
    71: "13d",  # Сніг
    73: "13d",  # Сніг
    75: "13d",  # Сніг
    77: "13d",  # Сніг
    80: "09d",  # Ливень
    81: "09d",  # Ливень
    82: "09d",  # Ливень
    85: "13d",  # Сніг
    86: "13d",  # Сніг
    95: "11d",  # Гроза
    96: "11d",  # Гроза
    99: "11d"   # Гроза
}

# Переводимо код погоди в назву погоди
wmo_to_weather = {
    0: "Ясне небо",
    1: "Ясне небо",
    2: "Трохи хмар",
    3: "Розсіяна хмарність",
    4: "Розсіяна хмарність",
    45: "Туман",
    48: "Туман",
    61: "Дощ",
    71: "Сніг",
    73: "Сніг",
    75: "Сніг",
    77: "Сніг",
    80: "Ливень",
    81: "Ливень",
    82: "Ливень",
    85: "Сніг",
    86: "Сніг",
    95: "Гроза",
    96: "Гроза",
    99: "Гроза"
}

# Ініціюємо geocoder з поточною ip-адресою користувача
g = geocoder.ip('me')

def get_weather():

    # Отримуємо координати користувача по ip-адресі
    latitude = g.latlng[0]
    longitude = g.latlng[1]

    # Робимо запит на open-meteo.com
    URL = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=EET'
    response = requests.get(URL)
    data = response.json()
    
    result_label.config(text="")
    
    date_index = 0
    for date in data['daily']['time']:
        min_temp = data['daily']['temperature_2m_min'][date_index]
        max_temp = data['daily']['temperature_2m_max'][date_index]

        wmo_code = data['daily']['weathercode'][date_index]
        weather = wmo_to_weather.get(wmo_code, 'Ясне небо') # Якщо такого коду немає, ставимо 'Ясне небо'
        weather_icon = get_weather_icon(wmo_code)           # Отримуємо іконку погоди з openweathermap.org

        daily_weather_info = f"Дата: {date}\n"
        daily_weather_info += f"{weather}\n"
        daily_weather_info += f"Мінімальна температура: {min_temp}°C\n"
        daily_weather_info += f"Максимальна температура: {max_temp}°C\n"

        # Якщо іконка є, додаємо її
        if weather_icon:
            icon_label = tk.Label(window, image=weather_icon)
            icon_label.image = weather_icon
            icon_label.grid(row=date_index + 1, column=0, padx=10, pady=10, sticky="w")

        # Додаємо текст
        label = tk.Label(window, text=daily_weather_info, font=('Helvetica', 12), bg="#3498db", fg="white", wraplength=300)
        label.grid(row=date_index + 1, column=1, padx=10, pady=10, sticky="w")

        date_index += 1

def get_weather_icon(wmo_code):
    icon_code = wmo_to_icon.get(wmo_code, "01d")
    icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
    icon_response = requests.get(icon_url, stream=True)
    
    if icon_response.status_code == 200:
        icon_image = Image.open(icon_response.raw)
        icon_photo = ImageTk.PhotoImage(icon_image)
        return icon_photo
    else:
        return None

# Ініціалізуємо вікно
window = tk.Tk()
window.title("Weather App")
window.geometry("400x900")

window.configure(bg="#3498db")

# Додаємо кнопку для погоди
search_button = tk.Button(window, text="Get Weather", command=get_weather, bg="#2ecc71", fg="white", relief="flat")
search_button.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="n")

result_label = tk.Label(window, font=('Helvetica', 12), bg="#3498db", fg="white")
result_label.grid(row=0, column=2, columnspan=2, pady=10, padx=10, sticky="n")

# Запускаємо програму
window.mainloop()