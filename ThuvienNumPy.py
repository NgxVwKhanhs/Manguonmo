import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Canvas, Text, Scrollbar, RIGHT, Y, BOTTOM, X, TOP, LEFT, Frame, WORD, BOTH 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def forecast_weather(city, country, days):
    api_key = 'e216bfd6782aa9b1732e574c571de0e7' 
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()
    # print(data)
    
    # Trích xuất dữ liệu
    temps = []
    times = []
    weather_descriptions = []
    
    for item in data['list']:
        temps.append(item['main']['temp'])
        times.append(item['dt_txt'])
        weather_descriptions.append(item['weather'][0]['description'])

    # Tạo DataFrame
    df = pd.DataFrame({'Thoi gian': times, 'Nhiet do': temps, 'Dieu kien thoi tiet': weather_descriptions})
    df['Thoi gian'] = pd.to_datetime(df['Thoi gian'])

    # Tính toán các thống kê
    temp_array = np.array(temps)
    avg_temp = np.mean(temp_array)
    max_temp = np.max(temp_array)
    min_temp = np.min(temp_array)
    temp_range = max_temp - min_temp

    # Tạo đặc trưng mới: sự chênh lệch nhiệt độ giữa ngày và đêm
    day_temps = temp_array[::2]
    night_temps = temp_array[1::2]
    temp_diff = np.mean(day_temps) - np.mean(night_temps)

    # Tính toán tỷ lệ ngày nắng, mưa
    sunny_days = df['Dieu kien thoi tiet'].str.contains(r'clear|few clouds', case=False).sum()
    rainy_days = df['Dieu kien thoi tiet'].str.contains(r'rain|shower|thunderstorm', case=False).sum()
    total_days = len(df)
    sunny_ratio = sunny_days / total_days
    rainy_ratio = rainy_days / total_days

    # Thêm tỷ lệ vào DataFrame
    df['Ty le ngay nang'] = sunny_ratio
    df['Ty le ngay mua'] = rainy_ratio

    # Thêm các thống kê vào DataFrame
    df['Nhiet do trung binh'] = avg_temp
    df['Nhiet do cao nhat'] = max_temp
    df['Nhiet do thap nhat'] = min_temp
    df['Bien do nhiet'] = temp_range
    df['Chenh lech nhiet do ngay dem'] = temp_diff

    return df
    
def plot_temperature(data):
    # Vẽ biểu đồ nhiệt độ theo thời gian
    global fig, canvas  # Khai báo fig và canvas global
    fig.clf()  # Xóa biểu đồ cũ
    # Vẽ biểu đồ nhiệt độ theo thời gian
    
    ax = fig.add_subplot(111)  # Thêm subplot vào Figure
    ax.cla()  # Xóa subplot cũ
    ax.plot(data['Thoi gian'], data['Nhiet do'])
    ax.set_xlabel('Thời gian',fontsize=12)
    ax.set_ylabel('Nhiệt độ (°C)', fontsize=12)
    ax.set_title(f'Biểu đồ nhiệt độ tại {city}, {country}')
    ax.tick_params(axis='x', labelsize=8)  # Tùy chỉnh cỡ chữ cho trục x
    ax.tick_params(axis='y', labelsize=8)  # Tùy chỉnh cỡ chữ cho trục y
    ax.grid(True)


def get_forecast():
    global city, country, fig  # Khai báo các biến global
    city = city_entry.get()
    country = country_entry.get()
    days = 5
    # days = int(days_entry.get())

    data = forecast_weather(city, country, days)

    # Vẽ biểu đồ
    plot_temperature(data)

    # Cập nhật Canvas
    canvas.draw()


# Tạo cửa sổ chính
window = Tk()
window.title("Dự Báo Thời Tiết Trong 5 ngày tới")

# Tạo nhãn và ô nhập cho thành phố
city_label = Label(window, text="Tỉnh/Thành phố:")
city_label.grid(row=0, column=0, padx=5, pady=5)
city_entry = Entry(window)
city_entry.grid(row=0, column=1, padx=5, pady=5)

# Tạo nhãn và ô nhập cho quốc gia
country_label = Label(window, text="Quốc gia:")
country_label.grid(row=1, column=0, padx=5, pady=5)
country_entry = Entry(window)
country_entry.grid(row=1, column=1, padx=5, pady=5)

# Tạo nút "Dự báo"
get_forecast_button = Button(window, text="Dự báo", command=get_forecast)
get_forecast_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Tạo khung để vẽ biểu đồ
canvas_frame = Frame(window)
canvas_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
fig = Figure(figsize=(5, 4), dpi=150)  # Tạo Figure mới
canvas = FigureCanvasTkAgg(fig, canvas_frame)
canvas.draw()
canvas_frame.grid(row=5, column=0, columnspan=2)  # Sử dụng grid để sắp xếp
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
# window.state('zoomed')
# Bắt đầu vòng lặp sự kiện
window.mainloop()
print("Khanhs")