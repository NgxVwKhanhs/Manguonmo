import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

def open_image():
    """Mở hộp thoại chọn tệp và hiển thị ảnh đã chọn."""
    global original_image, image_path
    image_path = filedialog.askopenfilename(
        initialdir="/",
        title="Chọn ảnh",
        filetypes=(("Image files", "*.jpg *.jpeg *.png *.bmp"), ("all files", "*.*")),
    )
    if image_path:
        original_image = Image.open(image_path)
        original_image = original_image.resize((300, 300))
        photo = ImageTk.PhotoImage(original_image)
        image_label.config(image=photo)
        image_label.image = photo

def enhance_image():
    """Tăng cường ảnh đã chọn, hiển thị kết quả và hiển thị thông báo."""
    global original_image, enhanced_image
    if original_image is None:
        return

    # Chuyển đổi ảnh PIL sang OpenCV
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

    # Áp dụng cân bằng biểu đồ thích ứng tương phản giới hạn (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v_eq = clahe.apply(v)
    hsv_eq = cv2.merge((h, s, v_eq))
    enhanced_img = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)

    # Chuyển đổi ảnh OpenCV sang PIL
    enhanced_image = Image.fromarray(enhanced_img)
    enhanced_image = enhanced_image.resize((300, 300))
    photo = ImageTk.PhotoImage(enhanced_image)
    image_label.config(image=photo)
    image_label.image = photo

    # Hiển thị thông báo
    messagebox.showinfo("Thông báo", "Đã tăng cường thành công!")

def save_image():
    """Lưu ảnh đã được tăng cường vào tệp."""
    global enhanced_image
    if enhanced_image is None:
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=(("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png"), ("All files", "*.*")),
    )
    if save_path:
        enhanced_image.save(save_path)

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng tăng cường ảnh")

# Biến toàn cục để lưu trữ ảnh
original_image = None
enhanced_image = None
image_path = None

# Tạo các widget
open_button = tk.Button(root, text="Mở ảnh", command=open_image)
enhance_button = tk.Button(root, text="Tăng cường", command=enhance_image)
save_button = tk.Button(root, text="Lưu ảnh", command=save_image)
image_label = tk.Label(root)

# Đặt vị trí cho các widget
open_button.grid(row=0, column=0, padx=10, pady=10)
enhance_button.grid(row=0, column=1, padx=10, pady=10)
save_button.grid(row=0, column=2, padx=10, pady=10)
image_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()