import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

def open_image():
    """Mở hộp thoại chọn file và hiển thị ảnh được chọn."""
    global img, file_path

    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Chọn ảnh",
        filetypes=(("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")),
    )
    if file_path:
        img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = resize_image(img)
        show_original_image(img)
        update_image()

def update_image():
    """Cập nhật ảnh sau khi xử lý."""
    global img
    if img is not None:
        lower = int(lower_scale.get())
        upper = int(upper_scale.get())

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, lower, upper)
        show_processed_image(edges)

def show_original_image(img):
    """Hiển thị ảnh gốc trên label bên trái."""
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
    original_image_label.config(image=img_tk)
    original_image_label.image = img_tk

def show_processed_image(img):
    """Hiển thị ảnh đã xử lý trên label bên phải."""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
    processed_image_label.config(image=img_tk)
    processed_image_label.image = img_tk

def resize_image(img, max_width=400, max_height=400):
    """Thay đổi kích thước ảnh nếu cần để vừa với màn hình."""
    height, width = img.shape[:2]
    if width > max_width or height > max_height:
        scale_factor = min(max_width / width, max_height / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = cv2.resize(img, (new_width, new_height))
    return img

def save_image():
    """Lưu ảnh đã xử lý."""
    global img, file_path
    if img is not None:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=(("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png"), ("All files", "*.*")),
        )
        if save_path:
            cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng phát hiện biên")

# Biến toàn cục lưu trữ ảnh
img = None
file_path = None

# Tạo frame chứa 2 ảnh
image_frame = tk.Frame(root)
image_frame.pack()

# Tạo label để hiển thị ảnh gốc
original_image_label = tk.Label(image_frame)
original_image_label.pack(side="left", padx=10)

# Tạo label để hiển thị ảnh đã xử lý
processed_image_label = tk.Label(image_frame)
processed_image_label.pack(side="left", padx=10)

# Tạo nút chọn ảnh
open_button = tk.Button(root, text="Chọn ảnh", command=open_image)
open_button.pack(pady=10)

# Tạo thanh trượt cho ngưỡng dưới
lower_scale = tk.Scale(
    root,
    from_=0,
    to=255,
    orient="horizontal",
    label="Ngưỡng dưới:",
    command=lambda x: update_image(),
)
lower_scale.set(50)
lower_scale.pack()

# Tạo thanh trượt cho ngưỡng trên
upper_scale = tk.Scale(
    root,
    from_=0,
    to=255,
    orient="horizontal",
    label="Ngưỡng trên:",
    command=lambda x: update_image(),
)
upper_scale.set(150)
upper_scale.pack()

# Tạo nút lưu ảnh
save_button = tk.Button(root, text="Lưu ảnh", command=save_image)
save_button.pack(pady=10)

root.mainloop()