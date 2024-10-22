import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from matplotlib.widgets import Slider

# Hàm tạo tín hiệu
def generate_signal(signal_type, frequency, amplitude, time):
    if signal_type == "Sine":
        return amplitude * np.sin(2 * np.pi * frequency * time)
    elif signal_type == "Cosine":
        return amplitude * np.cos(2 * np.pi * frequency * time)
    elif signal_type == "Square":
        return amplitude * signal.square(2 * np.pi * frequency * time)
    else:
        return np.zeros_like(time)

# Hàm biến đổi Fourier
def perform_fourier_transform(signal, sampling_rate):
    frequencies = np.fft.fftfreq(len(signal), 1 / sampling_rate)
    fft_values = np.fft.fft(signal)
    return frequencies, fft_values

# Hàm lọc tín hiệu
def filter_signal(data, filter_type, cutoff_frequency, order, sampling_rate):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_frequency / nyquist
    if filter_type == "Low Pass":
        b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    elif filter_type == "High Pass":
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    else:
        return data
    filtered_signal = signal.lfilter(b, a, data)
    return filtered_signal

# Hàm cập nhật đồ thị
def update_plots(event=None):
    # Lấy thông tin từ các widget
    signal_type = signal_type_var.get()
    frequency = frequency_slider.get()
    amplitude = amplitude_slider.get()
    sampling_rate = 1000  # Tốc độ lấy mẫu cố định
    time = np.arange(0, 1, 1/sampling_rate)

    # Tạo tín hiệu
    signal_data = generate_signal(signal_type, frequency, amplitude, time)

    # Thực hiện biến đổi
    if transform_var.get() == "DFT" or transform_var.get() == "FFT":
        frequencies, transformed_data = perform_fourier_transform(signal_data, sampling_rate)
        transformed_data = np.abs(transformed_data)[:len(frequencies)//2]
        frequencies = frequencies[:len(frequencies)//2]
    else:
        transformed_data = None
        frequencies = None

    # Lọc tín hiệu
    filter_type = filter_type_var.get()
    cutoff_frequency = cutoff_frequency_slider.get()
    order = order_slider.get()
    filtered_signal = filter_signal(signal_data, filter_type, cutoff_frequency, order, sampling_rate)

    # Cập nhật đồ thị tín hiệu
    ax1.clear()
    ax1.plot(time, signal_data, label="Tín hiệu gốc")
    ax1.plot(time, filtered_signal, label="Tín hiệu đã lọc", linestyle='--')
    ax1.set_xlabel("Thời gian (s)")
    ax1.set_ylabel("Biên độ")
    ax1.legend()

    # Cập nhật đồ thị biến đổi Fourier
    ax2.clear()
    if frequencies is not None and transformed_data is not None:
        ax2.plot(frequencies, transformed_data)
        ax2.set_xlabel("Tần số (Hz)")
        ax2.set_ylabel("Biên độ")
    canvas.draw()

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Phần mềm xử lý tín hiệu số")

# Khung nhập tín hiệu
input_frame = tk.LabelFrame(root, text="Tín hiệu đầu vào")
input_frame.grid(row=0, column=0, padx=10, pady=10)

# Loại tín hiệu
signal_type_var = tk.StringVar(value="Sine")
signal_type_label = tk.Label(input_frame, text="Loại tín hiệu:")
signal_type_label.grid(row=0, column=0)
signal_type_dropdown = ttk.Combobox(input_frame, textvariable=signal_type_var,
                                values=["Sine", "Cosine", "Square"])
signal_type_dropdown.grid(row=0, column=1)

# Tần số
frequency_label = tk.Label(input_frame, text="Tần số:")
frequency_label.grid(row=1, column=0)
frequency_slider = tk.Scale(input_frame, from_=1, to=10, orient='horizontal', command=lambda x: update_plots())
frequency_slider.grid(row=1, column=1)

# Biên độ
amplitude_label = tk.Label(input_frame, text="Biên độ:")
amplitude_label.grid(row=2, column=0)
amplitude_slider = tk.Scale(input_frame, from_=0.1, to=1, resolution=0.1, orient='horizontal', command=lambda x: update_plots())
amplitude_slider.grid(row=2, column=1)

# Khung lựa chọn phép biến đổi
transform_frame = tk.LabelFrame(root, text="Biến đổi")
transform_frame.grid(row=1, column=0, padx=10, pady=10)

# Biến đổi
transform_var = tk.StringVar(value="DFT")
dft_radio = tk.Radiobutton(transform_frame, text="DFT", variable=transform_var, value="DFT",
                          command=update_plots)
dft_radio.grid(row=0, column=0)
fft_radio = tk.Radiobutton(transform_frame, text="FFT", variable=transform_var, value="FFT",
                          command=update_plots)
fft_radio.grid(row=0, column=1)

# Khung bộ lọc
filter_frame = tk.LabelFrame(root, text="Bộ lọc")
filter_frame.grid(row=2, column=0, padx=10, pady=10)

# Loại bộ lọc
filter_type_var = tk.StringVar(value="Low Pass")
filter_type_label = tk.Label(filter_frame, text="Loại bộ lọc:")
filter_type_label.grid(row=0, column=0)
filter_type_dropdown = ttk.Combobox(filter_frame, textvariable=filter_type_var,
                                     values=["Low Pass", "High Pass", "None"])
filter_type_dropdown.grid(row=0, column=1)

# Tần số cắt
cutoff_frequency_label = tk.Label(filter_frame, text="Tần số cắt:")
cutoff_frequency_label.grid(row=1, column=0)
cutoff_frequency_slider = tk.Scale(filter_frame, from_=1, to=50, orient='horizontal', command=lambda x: update_plots())
cutoff_frequency_slider.grid(row=1, column=1)

# Bậc
order_label = tk.Label(filter_frame, text="Bậc:")
order_label.grid(row=2, column=0)
order_slider = tk.Scale(filter_frame, from_=1, to=10, orient='horizontal', command=lambda x: update_plots())
order_slider.grid(row=2, column=1)

# Khung đồ thị
plot_frame = tk.Frame(root)
plot_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

# Tạo hình và trục matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

# Cập nhật đồ thị lần đầu
update_plots()

# Chạy giao diện
root.mainloop()
