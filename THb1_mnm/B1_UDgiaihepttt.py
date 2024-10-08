import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

class LinearEquationSolver:
    def __init__(self, A, b):
        self.A = np.array(A)
        self.b = np.array(b)
        self.n = len(b)

    def gaussian_elimination(self):

        Ab = np.concatenate((self.A, self.b.reshape(-1, 1)), axis=1)

        for i in range(self.n):
            pivot = Ab[i, i]

            if pivot == 0:
                for k in range(i + 1, self.n):
                    if Ab[k, i] != 0:
                        Ab[[i, k]] = Ab[[k, i]]
                        pivot = Ab[i, i]
                        break

                if pivot == 0:
                    if Ab[i, self.n] != 0:
                        return "Vô nghiệm"
                    else:
                        return "Vô số nghiệm"

            Ab[i, :] /= pivot

            for j in range(i + 1, self.n):
                factor = Ab[j, i]
                Ab[j, :] -= factor * Ab[i, :]

        x = np.zeros(self.n)
        for i in range(self.n - 1, -1, -1):
            x[i] = Ab[i, self.n]
            for j in range(i + 1, self.n):
                x[i] -= Ab[i, j] * x[j]

        return x

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giải hệ phương trình tuyến tính")
        self.geometry("600x450")

        self.create_widgets()

    def create_widgets(self):
        # Khung nhập số phương trình
        self.frame_n = ttk.Frame(self)
        self.frame_n.pack(pady=10)
        ttk.Label(self.frame_n, text="Số phương trình, số ẩn (n):").pack(side="left")
        self.entry_n = ttk.Entry(self.frame_n, width=5)
        self.entry_n.pack(side="left")

        # Nút tạo ma trận và vector
        self.btn_create = ttk.Button(self, text="Tạo", command=self.create_matrix_vector)
        self.btn_create.pack(pady=10)

        # Khung chứa ma trận, vector và label hệ số
        self.frame_matrix_vector = ttk.Frame(self)
        self.frame_matrix_vector.pack()

        # Khung chứa ma trận A
        self.frame_matrix = ttk.Frame(self.frame_matrix_vector)
        self.frame_matrix.pack(side="left", padx=10)

        # Khung chứa vector b
        self.frame_vector = ttk.Frame(self.frame_matrix_vector)
        self.frame_vector.pack(side="left", padx=10)

        # Nút giải hệ phương trình
        self.btn_solve = ttk.Button(self, text="Giải", command=self.solve, state="disabled")
        self.btn_solve.pack(pady=10)

        # Khung hiển thị kết quả
        self.frame_result = ttk.Frame(self)
        self.frame_result.pack()

        # Ô hướng dẫn sử dụng
        self.instructions = tk.Text(self, wrap="word", height=5)
        self.instructions.pack(pady=10)
        self.instructions.insert(tk.END, "Hướng dẫn sử dụng:\n"
                                          "1. Nhập số phương trình.\n"
                                          "2. Nhấn nút 'Tạo' để hiển thị ra các ô nhập hệ số.\n"
                                          "3. Nhập các hệ số .\n"
                                          "4. Nhấn nút 'Giải' để xem kết quả.")
        self.instructions.config(state="disabled")

    def create_matrix_vector(self):
        """ Tạo ma trận A, vector b và các label hệ số. """
        try:
            n = int(self.entry_n.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên cho số phương trình.")
            return

        # Xóa các widget cũ
        for widget in self.frame_matrix.winfo_children():
            widget.destroy()
        for widget in self.frame_vector.winfo_children():
            widget.destroy()

        # Tạo các entry cho ma trận A và label hệ số phía trên
        self.entries_A = []
        for i in range(n):
            row = []
            for j in range(n):
                # Tạo frame để chứa label và entry
                frame = ttk.Frame(self.frame_matrix)
                frame.grid(row=i, column=j, padx=2, pady=2)

                # Tạo label hệ số
                label = ttk.Label(frame, text=f"a{i+1}{j+1}")
                label.pack()

                entry = ttk.Entry(frame, width=5)
                entry.pack()
                row.append(entry)
            self.entries_A.append(row)

        # Tạo các entry cho vector b và label hệ số phía trên
        self.entries_b = []
        for i in range(n):
            # Tạo frame để chứa label và entry
            frame = ttk.Frame(self.frame_vector)
            frame.grid(row=i, column=0, padx=2, pady=2)

            # Tạo label hệ số
            label = ttk.Label(frame, text=f"b{i+1}")
            label.pack()

            entry = ttk.Entry(frame, width=5)
            entry.pack()
            self.entries_b.append(entry)

        # Kích hoạt nút giải hệ phương trình
        self.btn_solve.config(state="normal")

    def solve(self):
        """ Giải hệ phương trình và hiển thị kết quả. """
        try:
            n = int(self.entry_n.get())

            A = [[float(self.entries_A[i][j].get()) for j in range(n)] for i in range(n)]
            b = [float(self.entries_b[i].get()) for i in range(n)]

            solver = LinearEquationSolver(A, b)
            solution = solver.gaussian_elimination()

            self.show_result(solution)

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số cho tất cả các ô.")

    def show_result(self, solution):
        """ Hiển thị nghiệm của hệ phương trình. """
        for widget in self.frame_result.winfo_children():
            widget.destroy()

        if isinstance(solution, str):
            ttk.Label(self.frame_result, text=solution).pack()
        else:
            for i, value in enumerate(solution):
                ttk.Label(self.frame_result, text=f"x{i + 1} = {value:.2f}").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()