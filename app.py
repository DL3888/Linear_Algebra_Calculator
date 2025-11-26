import tkinter as tk
from tkinter import messagebox
from matrix import Matrix

class MatrixCalculatorApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Linear Algebra Calculator')
        
        # State variables for two-step binary operations
        self.current_op = None  # Stores the pending operation ('add', 'sub', 'mul')
        self.matrix_a = None    # Stores the first matrix operand

        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(expand=True, fill='both')

        # Input Section (Single Input Field)
        input_frame_a = tk.LabelFrame(main_frame, text='Matrix Input', padx=10, pady=10)
        input_frame_a.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        main_frame.grid_columnconfigure(0, weight=1)

        instr_lbl_a = tk.Label(input_frame_a, text='Matrix: Columns are comma-separated. Rows are on new lines.', font=('Roboto', 10))
        instr_lbl_a.pack(pady=5)

        self.matrix_inpt_a = tk.Text(input_frame_a, height=10, width=50, relief=tk.RIDGE, borderwidth=2, font=('Courier New', 12))
        self.matrix_inpt_a.pack(padx=5, pady=5, fill='both', expand=True)
        self.matrix_inpt_a.insert(tk.END, '1, 2\n3, 4') 

        # Calculation Buttons
        button_frame = tk.LabelFrame(main_frame, text='Operations', padx=10, pady=10)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        # Container for all buttons
        op_container = tk.Frame(button_frame)
        op_container.pack()

        # Unary Buttons
        tk.Button(op_container, text='Determinant (A)', command=lambda: self.perform_operation('det'), width=20, height=2, font=('Roboto', 12)).grid(row=0, column=0, pady=5, padx=5)
        tk.Button(op_container, text='Inverse (A⁻¹)', command=lambda: self.perform_operation('inv'), width=20, height=2, font=('Roboto', 12)).grid(row=0, column=1, pady=5, padx=5)
        tk.Button(op_container, text='RREF (A)', command=lambda: self.perform_operation('rref'), width=20, height=2, font=('Roboto', 12)).grid(row=0, column=2, pady=5, padx=5)
        tk.Button(op_container, text='Transpose (Aᵀ)', command=lambda: self.perform_operation('tra'), width=20, height=2, font=('Roboto', 12)).grid(row=0, column=3, pady=5, padx=5)

        # Binary Buttons (Triggering the two-step process)
        tk.Button(op_container, text='Add (+)', command=lambda: self.perform_operation('add'), width=20, height=2, font=('Roboto', 12)).grid(row=1, column=0, pady=5, padx=5)
        tk.Button(op_container, text='Subtract (-)', command=lambda: self.perform_operation('sub'), width=20, height=2, font=('Roboto', 12)).grid(row=1, column=1, pady=5, padx=5)
        tk.Button(op_container, text='Multiply (*)', command=lambda: self.perform_operation('mul'), width=20, height=2, font=('Roboto', 12)).grid(row=1, column=2, pady=5, padx=5)
        
        # Clear/Reset Button
        tk.Button(op_container, text='Clear All / Reset State', command=self.reset_state, width=18, height=2, font=('Roboto', 12, 'bold'), bg='#e6e6e6').grid(row=1, column=3, pady=5, padx=5)


        # Output
        output_frame = tk.LabelFrame(main_frame, text='Result', padx=10, pady=10)
        output_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        main_frame.grid_rowconfigure(2, weight=1)

        self.result_title = tk.Label(output_frame, text='Ready to Calculate...', font=('Roboto', 14, 'bold'))
        self.result_title.pack(pady=5)

        self.result_output = tk.Text(output_frame, height=10, width=80, font=('Courier New', 12), state=tk.DISABLED, relief=tk.SUNKEN, borderwidth=2)
        self.result_output.pack(padx=5, pady=5, expand=True, fill='both')

    def reset_state(self):
        """Clears all inputs and resets the state machine."""
        self.current_op = None
        self.matrix_a = None
        self.matrix_inpt_a.delete('1.0', tk.END)
        self.display_result("Ready to Calculate...", "The calculator state has been reset.")

    def get_matrix_from_input(self, matrix_name: str = "Matrix") -> Matrix:
        """
        Reads text from the single input box, parses it, and returns a Matrix object.
        """
        input_str = self.matrix_inpt_a.get('1.0', tk.END)
        
        if not input_str.strip():
            raise ValueError(f"{matrix_name} input cannot be empty.")
        
        row_strings = input_str.strip().split('\n')
        matrix_data = []
        
        for i, row_str in enumerate(row_strings):
            elements = [s.strip() for s in row_str.split(',')]
            elements = [e for e in elements if e]

            try:
                float_row = [float(e) for e in elements]
            except ValueError as e:
                raise ValueError(f"Invalid element in {matrix_name}, row {i+1}. Ensure all elements are numeric.") from e
            
            if float_row:
                matrix_data.append(float_row)
        
        return Matrix(matrix_data)
    
    def display_result(self, title: str, content: str):
        """Helper to update the output area with the result."""
        self.result_title.config(text=title)
        self.result_output.config(state=tk.NORMAL)
        self.result_output.delete('1.0', tk.END)
        self.result_output.insert(tk.END, content)
        self.result_output.config(state=tk.DISABLED)

    def perform_operation(self, operation: str):
        """
        Handles both unary operations (direct calculation) and binary operations 
        (two-step state machine).
        """
        op_map = {'add': 'Addition (+)', 'sub': 'Subtraction (-)', 'mul': 'Multiplication (*)'}

        try: 
            # Unary Operations 
            if operation in ['det', 'inv', 'rref', 'tra']:
                # Prevent unary operations if a binary operation is already in progress
                if self.current_op is not None:
                    messagebox.showwarning("Operation in Progress", f"Please complete the pending binary operation ({op_map[self.current_op]}) or click 'Clear All / Reset State' first.")
                    return

                matrix_a = self.get_matrix_from_input("Matrix A")
                result = None
                title = ''
                
                if operation == 'det':
                    result = matrix_a.det()
                    title = 'Determinant (det(A))'
                    self.display_result(title, f"{result:.6f}")
                elif operation == 'inv':
                    result = matrix_a.inverse()
                    title = 'Inverse Matrix (A⁻¹)'
                    self.display_result(title, str(result))
                elif operation == "rref":
                    result = matrix_a.rref()
                    title = "Reduced Row Echelon Form (RREF)"
                    self.display_result(title, str(result))
                elif operation == "tra":
                    result = matrix_a.transpose()
                    title = "Transpose Matrix (Aᵀ)"
                    self.display_result(title, str(result))
            
            # Binary Operations (Two-Step State Machine)
            elif operation in ['add', 'sub', 'mul']:
                
                # Is a binary operation already in progress (current_op is set)?
                if self.current_op is not None and self.current_op != operation:
                     messagebox.showwarning("Operation in Progress", f"A different operation ({op_map[self.current_op]}) is already pending. Please complete it or click 'Clear All / Reset State' first.")
                     return

                # Calculate Result (self.matrix_a is set, current input is Matrix B)
                if self.matrix_a is not None and self.current_op == operation:
                    
                    matrix_b = self.get_matrix_from_input("Matrix B")
                    
                    if operation == 'add':
                        result = self.matrix_a + matrix_b 
                        title = op_map[operation] + ' (A + B)'
                    elif operation == 'sub':
                        result = self.matrix_a - matrix_b 
                        title = op_map[operation] + ' (A - B)'
                    elif operation == 'mul':
                        result = self.matrix_a * matrix_b 
                        title = op_map[operation] + ' (A * B)'
                        
                    self.display_result(title, str(result))
                    
                    # Reset state for the next calculation
                    self.current_op = None
                    self.matrix_a = None
                    
                # Store A and prompt for B (self.matrix_a is None) 
                else:
                    matrix_a = self.get_matrix_from_input("Matrix A")
                    
                    # Store A and the operation type
                    self.matrix_a = matrix_a
                    self.current_op = operation
                    
                    # Clear input field and prompt the user
                    self.matrix_inpt_a.delete('1.0', tk.END)
                    
                    messagebox.showinfo(
                        "Input Matrix B", 
                        f"Matrix A has been stored for {op_map[operation]}.\n\nPlease enter Matrix B into the input field now.\n\nThen press the {op_map[operation]} button again to complete the calculation."
                    )
                    self.display_result(f"Awaiting Matrix B for {op_map[operation]}...", "Matrix A is stored. Enter Matrix B in the input field above, and click the operation button again.")
        
        except ValueError as e:
            # If an error occurs, and a matrix was stored, we should let the user re-try B input.
            # If the error was from reading A (step 1), we should reset.
            if self.matrix_a is None and operation in ['add', 'sub', 'mul']:
                 self.reset_state() # If A failed, reset everything.
            
            messagebox.showerror("Input Error / Calculation Failed", str(e))
        except Exception as e:
            # Catch all other unexpected errors and reset state for safety
            messagebox.showerror("Error", f"An unexpected error occurred: {e}. State has been reset.")
            self.reset_state()


if __name__ == '__main__':
    app = MatrixCalculatorApp()
    app.mainloop()