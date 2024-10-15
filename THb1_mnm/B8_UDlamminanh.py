import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import ImageTk, Image

def open_image():
    global image
    # Mở hộp thoại chọn file ảnh
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Chọn ảnh",
        filetypes=(("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png"), ("All files", "*.*"))
    )
    if filepath:
        # Đọc ảnh từ file
        image = cv2.imread(filepath)
        # Hiển thị ảnh gốc
        show_image(image, canvas_original)

def apply_blur():
    global image, blurred_image
    if image is not None:
        # Lấy giá trị kernel size từ thanh trượt
        kernel_size = slider.get()
        # Áp dụng Gaussian Blur
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        # Hiển thị ảnh đã làm mịn
        show_image(blurred_image, canvas_blurred)

def show_image(img, canvas):
    # Chuyển đổi ảnh từ BGR sang RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Chuyển đổi ảnh sang định dạng PhotoImage
    photo = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))
    # Hiển thị ảnh trên canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Ứng dụng Làm Mịn Ảnh")

# Tạo nút chọn ảnh
button_open = tk.Button(root, text="Chọn ảnh", command=open_image)
button_open.pack()

# Tạo canvas hiển thị ảnh gốc
canvas_original = tk.Canvas(root, width=400, height=300)
canvas_original.pack(side=tk.LEFT)

# Tạo canvas hiển thị ảnh đã làm mịn
canvas_blurred = tk.Canvas(root, width=400, height=300)
canvas_blurred.pack(side=tk.RIGHT)

# Tạo thanh trượt điều chỉnh kernel size
slider = tk.Scale(root, from_=1, to=51, orient=tk.HORIZONTAL, label="Kernel Size", length=400)
slider.set(1) # Đặt giá trị ban đầu cho kernel size
slider.pack()

# Tạo nút áp dụng làm mịn
button_blur = tk.Button(root, text="Làm mịn", command=apply_blur)
button_blur.pack()

# Biến lưu trữ ảnh
image = None
blurred_image = None

# Chạy ứng dụng
root.mainloop()