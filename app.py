import tkinter as tk
from tkinter import messagebox
from matrix import Matrix

class MatrixCalculatorApp(tk.Tk):

    def __init__(self):
        super().__init__(None)
        self.title('Linear Algebra Calculator')

        root = tk.Frame(self, padx=10, pady=10)
        root.pack(expand=True, fill='both')


        # Inputs
        input_frame = tk.LabelFrame(root, text='Matrix Input', padx=10, pady=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        instr_lbl = tk.Label(input_frame, text='Columns: comma-separated; Rows: new line.')
        instr_lbl.pack(pady=5)

        self.matrix_inpt = tk.Text(input_frame, height=10, width=40, relief=tk.RIDGE, borderwidth=2, font=('Courier New', 12))
        self.matrix_inpt.pack(padx=5, pady=5)
        self.matrix_inpt.insert(tk.END, '1, 2, 3\n4, 5, 6\n7, 8, 9')


        # Calculation Buttons
        button_frame = tk.LabelFrame(root, text='Choose Calculation to Perform', padx=10, pady=10)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Determinant
        tk.Button(button_frame, text='Calculate Determinant', command=lambda: self.operation('det'), width=25, height=2).pack(pady=5)
        
        # Inverse
        tk.Button(button_frame, text='Calculate Inverse', command=lambda: self.operation('inv'), width=25, height=2).pack(pady=5)

        # RREF
        tk.Button(button_frame, text='Perform RREF', command=lambda: self.operation('rref'), width=25, height=2).pack(pady=5)

        # Transpose
        tk.Button(button_frame, text='Get Transpose', command=lambda: self.operation('tra'), width=25, height=2).pack(pady=5)


        # Output
        output_frame = tk.LabelFrame(root, text='Output', padx=10, pady=10)
        output_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.result_title = tk.Label(output_frame, text='Result:', font=('Roboto', 14, 'bold'))
        self.result_title.pack(pady=5)

        self.result_output = tk.Text(output_frame, height=10, width=80, font=('Courier New', 12), state=tk.DISABLED, relief=tk.SUNKEN, borderwidth=2)
        self.result_output.pack(padx=5, pady=5, expand=True, fill='both')

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def get_matrix_from_input(self) -> Matrix:
        """
        Reads text from the input box, parses it, and returns a Matrix object.
        (This method replaces the static Matrix.from_input class method).
        """
        input_str = self.matrix_inpt.get('1.0', tk.END)
        
        if not input_str.strip():
            raise ValueError("Input cannot be empty.")
        
        row_strings = input_str.strip().split('\n')
        matrix_data = []
        
        for i, row_str in enumerate(row_strings):
            elements = [s.strip() for s in row_str.split(',')]
            elements = [e for e in elements if e]

            try:
                float_row = [float(e) for e in elements]
            except ValueError as e:
                raise ValueError(f"Invalid element in row {i+1}. Ensure all elements are numeric.") from e
            
            if float_row:
                matrix_data.append(float_row)
                
        return Matrix(matrix_data)

    def display_result(self, title: str, content: str):
        self.result_title.config(text=title)
        self.result_output.config(state=tk.NORMAL)
        self.result_output.delete('1.0', tk.END)
        self.result_output.insert(tk.END, content)
        self.result_output.config(state=tk.DISABLED)

    def operation(self, operation: int):
        try: 
            matrix_a = self.get_matrix_from_input()

            result = None
            title = ''

            if operation == 'det':
                result = matrix_a.det()
                title = 'Determinant'
                result_content = f"{result:.6f}"
            elif operation == 'inv':
                result = matrix_a.inverse()
                title = 'Inverse Matrix'
                result_content = str(result)
            elif operation == "rref":
                result = matrix_a.rref()
                title = "Reduced Row Echelon Form (RREF)"
                result_content = str(result)
            elif operation == "tra":
                result = matrix_a.transpose()
                title = "Transpose Matrix (Aᵀ)"
                result_content = str(result)

            self.display_result(title, result_content)
        
        except ValueError as e:
            messagebox.showerror("Input Error / Singular Matrix", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexoected error occurred: {e}")


if __name__ == '__main__':
    app = MatrixCalculatorApp()
    app.mainloop()