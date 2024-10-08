import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MathTool:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.z = sp.Symbol('z')

    def calculate_limit(self, expression, var, point, direction=None):
        f = sp.sympify(expression)
        if direction == '+':
            return sp.limit(f, var, point, dir='+')
        elif direction == '-':
            return sp.limit(f, var, point, dir='-')
        else:
            return sp.limit(f, var, point)

    def calculate_derivative(self, expression, var, order=1):
        f = sp.sympify(expression)
        return sp.diff(f, var, order)

    def calculate_integral(self, expression, var, lower_limit=None, upper_limit=None):
        f = sp.sympify(expression)
        if lower_limit is not None and upper_limit is not None:
            return sp.integrate(f, (var, lower_limit, upper_limit))
        else:
            return sp.integrate(f, var)

    def solve_equation(self, expression):
        try:
            return sp.solve(sp.Eq(sp.sympify(expression), 0), self.x)
        except NotImplementedError:
            return "Phương trình không thể giải được."

    def plot_2d_graph(self, expression, x_range=(-10, 10)):
        f = sp.lambdify(self.x, sp.sympify(expression), 'numpy')
        x_vals = np.linspace(x_range[0], x_range[1], 200)
        y_vals = f(x_vals)
        plt.plot(x_vals, y_vals)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Đồ thị hàm số')
        plt.grid(True)
        plt.show()

    def plot_3d_graph(self, expression, x_range=(-5, 5), y_range=(-5, 5)):
        f = sp.lambdify((self.x, self.y), sp.sympify(expression), 'numpy')
        x_vals, y_vals = np.mgrid[x_range[0]:x_range[1]:0.25, y_range[0]:y_range[1]:0.25]
        z_vals = f(x_vals, y_vals)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_vals, y_vals, z_vals)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.title('Đồ thị hàm số 3D')
        plt.show()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phần mềm hỗ trợ học tập Giải tích")
        self.geometry("800x700")

        self.math_tool = MathTool()
        self.create_widgets()

    def create_widgets(self):
        # Notebook
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        self.create_limit_tab(notebook)
        self.create_derivative_tab(notebook)
        self.create_integral_tab(notebook)
        self.create_equation_tab(notebook)
        self.create_graph_tab(notebook)

        # Ô hướng dẫn
        self.instructions_text = tk.Text(self, wrap="word", height=5)
        self.instructions_text.pack(pady=10, expand=True, fill="both")
        self.update_instructions("Chọn một chức năng từ các tab.")

    def update_instructions(self, text):
        self.instructions_text.config(state="normal")  # Cho phép ghi vào ô text
        self.instructions_text.delete("1.0", tk.END)  # Xóa nội dung cũ
        self.instructions_text.insert(tk.END, text)  # Chèn nội dung mới
        self.instructions_text.config(state="disabled")  # Vô hiệu hóa chỉnh sửa

    def create_limit_tab(self, notebook):
        limit_tab = ttk.Frame(notebook)
        notebook.add(limit_tab, text="Giới hạn")

        # Input
        ttk.Label(limit_tab, text="Nhập hàm số:").grid(row=0, column=0, sticky="w")
        self.limit_expression_entry = ttk.Entry(limit_tab, width=50)
        self.limit_expression_entry.grid(row=0, column=1, columnspan=3)

        ttk.Label(limit_tab, text="Biến số:").grid(row=1, column=0, sticky="w")
        self.limit_var_entry = ttk.Entry(limit_tab, width=10)
        self.limit_var_entry.grid(row=1, column=1)

        ttk.Label(limit_tab, text="Tiệm cận:").grid(row=1, column=2, sticky="w")
        self.limit_point_entry = ttk.Entry(limit_tab, width=10)
        self.limit_point_entry.grid(row=1, column=3)

        ttk.Label(limit_tab, text="Hướng:").grid(row=2, column=0, sticky="w")
        self.limit_direction_var = tk.StringVar(limit_tab)
        self.limit_direction_var.set("Không")
        direction_options = ["Không", "+", "-"]
        ttk.OptionMenu(limit_tab, self.limit_direction_var, *direction_options).grid(row=2, column=1)

        ttk.Button(limit_tab, text="Tính toán", command=self.calculate_limit).grid(row=3, column=0, columnspan=4)

        # Output
        self.limit_result_label = ttk.Label(limit_tab, text="")
        self.limit_result_label.grid(row=4, column=0, columnspan=4)
        # Hướng dẫn sử dụng tab Giới hạn
        limit_tab.bind("<Visibility>", lambda event: self.update_instructions(
            "Hướng dẫn tính giới hạn:\n"
            "1. Nhập hàm số (ví dụ: (x^2 - 1)/(x - 1)).\n"
            "2. Nhập biến số (ví dụ: x).\n"
            "3. Nhập giá trị tiệm cận (ví dụ: 1).\n"
            "4. Chọn hướng (nếu cần) (+, -, hoặc để trống).\n"
            "5. Nhấn nút 'Tính toán'."
        ))

    def create_derivative_tab(self, notebook):
        derivative_tab = ttk.Frame(notebook)
        notebook.add(derivative_tab, text="Đạo hàm")

        # Input
        ttk.Label(derivative_tab, text="Nhập hàm số:").grid(row=0, column=0, sticky="w")
        self.derivative_expression_entry = ttk.Entry(derivative_tab, width=50)
        self.derivative_expression_entry.grid(row=0, column=1, columnspan=3)

        ttk.Label(derivative_tab, text="Biến số:").grid(row=1, column=0, sticky="w")
        self.derivative_var_entry = ttk.Entry(derivative_tab, width=10)
        self.derivative_var_entry.grid(row=1, column=1)

        ttk.Label(derivative_tab, text="Bậc:").grid(row=1, column=2, sticky="w")
        self.derivative_order_entry = ttk.Entry(derivative_tab, width=10)
        self.derivative_order_entry.insert(0, "1")  # Default order is 1
        self.derivative_order_entry.grid(row=1, column=3)

        ttk.Button(derivative_tab, text="Tính toán", command=self.calculate_derivative).grid(row=2, column=0, columnspan=4)

        # Output
        self.derivative_result_label = ttk.Label(derivative_tab, text="")
        self.derivative_result_label.grid(row=3, column=0, columnspan=4)
        # Hướng dẫn sử dụng tab Đạo hàm
        derivative_tab.bind("<Visibility>", lambda event: self.update_instructions(
            "Hướng dẫn tính đạo hàm:\n"
            "1. Nhập hàm số (ví dụ: x^2 - 3*x + 2).\n"
            "2. Nhập biến số (ví dụ: x).\n"
            "3. Nhập bậc đạo hàm (ví dụ: 2 cho đạo hàm bậc 2).\n"
            "4. Nhấn nút 'Tính toán'."
        ))

    def create_integral_tab(self, notebook):
        integral_tab = ttk.Frame(notebook)
        notebook.add(integral_tab, text="Tích phân")

        # Input
        ttk.Label(integral_tab, text="Nhập hàm số:").grid(row=0, column=0, sticky="w")
        self.integral_expression_entry = ttk.Entry(integral_tab, width=50)
        self.integral_expression_entry.grid(row=0, column=1, columnspan=3)

        ttk.Label(integral_tab, text="Biến số:").grid(row=1, column=0, sticky="w")
        self.integral_var_entry = ttk.Entry(integral_tab, width=10)
        self.integral_var_entry.grid(row=1, column=1)

        ttk.Label(integral_tab, text="Giới hạn dưới:").grid(row=2, column=0, sticky="w")
        self.integral_lower_limit_entry = ttk.Entry(integral_tab, width=10)
        self.integral_lower_limit_entry.grid(row=2, column=1)

        ttk.Label(integral_tab, text="Giới hạn trên:").grid(row=2, column=2, sticky="w")
        self.integral_upper_limit_entry = ttk.Entry(integral_tab, width=10)
        self.integral_upper_limit_entry.grid(row=2, column=3)

        ttk.Button(integral_tab, text="Tính toán", command=self.calculate_integral).grid(row=3, column=0, columnspan=4)

        # Output
        self.integral_result_label = ttk.Label(integral_tab, text="")
        self.integral_result_label.grid(row=4, column=0, columnspan=4)
        # Hướng dẫn sử dụng tab Tích phân
        integral_tab.bind("<Visibility>", lambda event: self.update_instructions(
            "Hướng dẫn tính tích phân:\n"
            "1. Nhập hàm số (ví dụ: x^2 - 3*x + 2).\n"
            "2. Nhập biến số (ví dụ: x).\n"
            "3. Nhập giới hạn dưới và giới hạn trên (nếu tính tích phân xác định).\n"
            "4. Nhấn nút 'Tính toán'."
        ))

    def create_equation_tab(self, notebook):
        equation_tab = ttk.Frame(notebook)
        notebook.add(equation_tab, text="Giải phương trình")

        # Input
        ttk.Label(equation_tab, text="Nhập phương trình (vd: x**2 - 1 = 0):").grid(row=0, column=0, sticky="w")
        self.equation_entry = ttk.Entry(equation_tab, width=50)
        self.equation_entry.grid(row=0, column=1)

        ttk.Button(equation_tab, text="Giải", command=self.solve_equation).grid(row=1, column=0, columnspan=2)

        # Output
        self.equation_result_label = ttk.Label(equation_tab, text="")
        self.equation_result_label.grid(row=2, column=0, columnspan=2)
        # Hướng dẫn sử dụng tab Giải phương trình
        equation_tab.bind("<Visibility>", lambda event: self.update_instructions(
            "Hướng dẫn giải phương trình:\n"
            "1. Nhập phương trình (ví dụ: x^2 - 1 = 0).\n"
            "2. Nhấn nút 'Giải'."
        ))

    def create_graph_tab(self, notebook):
        graph_tab = ttk.Frame(notebook)
        notebook.add(graph_tab, text="Vẽ đồ thị")

        # Input
        ttk.Label(graph_tab, text="Nhập hàm số:").grid(row=0, column=0, sticky="w")
        self.graph_expression_entry = ttk.Entry(graph_tab, width=50)
        self.graph_expression_entry.grid(row=0, column=1, columnspan=3)

        ttk.Button(graph_tab, text="Vẽ đồ thị 2D", command=self.plot_2d).grid(row=1, column=0, columnspan=2)
        ttk.Button(graph_tab, text="Vẽ đồ thị 3D", command=self.plot_3d).grid(row=1, column=2, columnspan=2)

        # Output
        self.graph_canvas = None
        graph_tab.bind("<Visibility>", lambda event: self.update_instructions(
            "Hướng dẫn vẽ đồ thị:\n"
            "1. Nhập hàm số (ví dụ: x^2 - 1).\n"
            "2. Nhấn nút 'Vẽ đồ thị 2D' hoặc 'Vẽ đồ thị 3D'."
        ))

    def calculate_limit(self):
        expression = self.limit_expression_entry.get()
        var = self.limit_var_entry.get()
        point = self.limit_point_entry.get()
        direction = self.limit_direction_var.get()
        try:
            result = self.math_tool.calculate_limit(expression, var, float(point), direction)
            self.limit_result_label.config(text=f"Kết quả: {result}")
        except Exception as e:
            self.limit_result_label.config(text=f"Lỗi: {e}")

    def calculate_derivative(self):
        expression = self.derivative_expression_entry.get()
        var = self.derivative_var_entry.get()
        order = self.derivative_order_entry.get()
        try:
            result = self.math_tool.calculate_derivative(expression, var, int(order))
            self.derivative_result_label.config(text=f"Kết quả: {result}")
        except Exception as e:
            self.derivative_result_label.config(text=f"Lỗi: {e}")

    def calculate_integral(self):
        expression = self.integral_expression_entry.get()
        var = self.integral_var_entry.get()
        lower_limit = self.integral_lower_limit_entry.get()
        upper_limit = self.integral_upper_limit_entry.get()
        try:
            if lower_limit and upper_limit:
                result = self.math_tool.calculate_integral(expression, var, float(lower_limit), float(upper_limit))
            else:
                result = self.math_tool.calculate_integral(expression, var)
            self.integral_result_label.config(text=f"Kết quả: {result}")
        except Exception as e:
            self.integral_result_label.config(text=f"Lỗi: {e}")

    def solve_equation(self):
        equation = self.equation_entry.get()
        try:
            result = self.math_tool.solve_equation(equation)
            self.equation_result_label.config(text=f"Nghiệm: {result}")
        except Exception as e:
            self.equation_result_label.config(text=f"Lỗi: {e}")

    def plot_2d(self):
        expression = self.graph_expression_entry.get()
        try:
            self.math_tool.plot_2d_graph(expression)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể vẽ đồ thị. {e}")

    def plot_3d(self):
        expression = self.graph_expression_entry.get()
        try:
            self.math_tool.plot_3d_graph(expression)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể vẽ đồ thị. {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()