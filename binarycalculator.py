import tkinter as tk
from tkinter import messagebox, Toplevel

# Logic gate functions
def AND(a, b): return a & b
def OR(a, b): return a | b
def XOR(a, b): return a ^ b
def NOT(a): return ~a & 1  # ensures 1-bit result

# Helper function to pad binary strings to the same length
def pad_binary(a, b):
    max_len = max(len(a), len(b))
    return a.zfill(max_len), b.zfill(max_len)

# Binary addition using full adders
def binary_adder(a, b):
    a, b = pad_binary(a, b)
    result, carry, steps = "", 0, []
    
    for i in range(len(a) - 1, -1, -1):
        sum_bit, carry = full_adder(int(a[i]), int(b[i]), carry)
        result = str(sum_bit) + result
        steps.append(f"Add {a[i]} + {b[i]} + Carry {carry}: Sum = {sum_bit}, New Carry = {carry}")
    
    if carry:
        result = "1" + result
        steps.append("Final carry: 1")
    
    return result, steps

# Binary subtraction with sign bit handling
def binary_subtractor(a, b):
    a, b = pad_binary(a, b)
    is_negative = int(a, 2) < int(b, 2)
    result, borrow, steps = "", 0, []
    
    for i in range(len(a) - 1, -1, -1):
        diff_bit, borrow = full_subtractor(int(a[i]), int(b[i]), borrow)
        result = str(diff_bit) + result
        steps.append(f"Subtract {a[i]} - {b[i]} - Borrow {borrow}: Difference = {diff_bit}, New Borrow = {borrow}")
    
    result = result.lstrip("0") or "0"
    sign_bit = "1" if is_negative else "0"
    result = sign_bit + result
    
    return result, steps

# Binary multiplication using shift-and-add
def binary_multiplier(a, b):
    product, steps = "0", []
    a, b = a.zfill(len(a) + len(b)), b  # Extend `a` to accommodate larger products
    
    for i in range(len(b) - 1, -1, -1):
        if b[i] == '1':
            partial_product = a + "0" * (len(b) - 1 - i)
            product, add_steps = binary_adder(product, partial_product)
            steps.append(f"Partial Product: {partial_product} + Current Product: {product}")
            steps.extend(add_steps)
        else:
            steps.append(f"Partial Product (skipped as bit is 0): {'0' * len(a)}")
    
    return product.lstrip("0") or "0", steps

# Full Adder for individual bit addition
def full_adder(a, b, carry_in=0):
    sum_ = XOR(XOR(a, b), carry_in)
    carry_out = OR(AND(a, b), AND(carry_in, XOR(a, b)))
    return sum_, carry_out

# Full Subtractor for individual bit subtraction
def full_subtractor(a, b, borrow_in=0):
    difference = XOR(XOR(a, b), borrow_in)
    borrow_out = OR(AND(NOT(a), b), AND(borrow_in, XOR(NOT(a), b)))
    return difference, borrow_out

# GUI functions
def perform_operation():
    try:
        a = entry_a.get()
        b = entry_b.get()
        if not all(c in "01" for c in a) or not all(c in "01" for c in b):
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid binary numbers.")
        return
    
    operation = operation_var.get()
    if operation == "Addition":
        result, steps = binary_adder(a, b)
        result_label.config(text=f"Result (Sum): {result}")
        draw_full_adder(result)
        show_steps("Addition Steps", steps)
    elif operation == "Subtraction":
        result, steps = binary_subtractor(a, b)
        result_label.config(text=f"Result (Difference): {result} (with sign bit)")
        draw_full_subtractor(result)
        show_steps("Subtraction Steps", steps)
    elif operation == "Multiplication":
        result, steps = binary_multiplier(a, b)
        result_label.config(text=f"Result (Product): {result}")
        draw_multiplier(result)
        show_steps("Multiplication Steps", steps)

def show_steps(title, steps):
    steps_window = Toplevel(root)
    steps_window.title(title)
    steps_window.config(bg="beige")
    for i, step in enumerate(steps, start=1):
        tk.Label(steps_window, text=f"Step {i}: {step}", bg="beige", anchor="w", justify="left").pack(fill="both", padx=10, pady=2)

def draw_full_adder(result):
    canvas.delete("all")
    canvas.create_text(150, 20, text="Full Adder Circuit", font=("Arial", 16))
    canvas.create_rectangle(100, 50, 200, 100, fill="lightgrey")
    canvas.create_text(150, 75, text="RESULT")
    canvas.create_text(150, 120, text=f"Sum: {result}")

def draw_full_subtractor(result):
    canvas.delete("all")
    canvas.create_text(150, 20, text="Full Subtractor Circuit", font=("Arial", 16))
    canvas.create_rectangle(100, 50, 200, 100, fill="lightgrey")
    canvas.create_text(150, 75, text="RESULT")
    canvas.create_text(150, 120, text=f"Difference: {result} (with sign bit)")

def draw_multiplier(result):
    canvas.delete("all")
    canvas.create_text(150, 20, text="Multiplier Circuit (Shift and Add)", font=("Arial", 16))
    canvas.create_rectangle(100, 50, 200, 100, fill="lightgrey")
    canvas.create_text(150, 75, text="RESULT")
    canvas.create_text(150, 120, text=f"Product: {result} (Binary)")

# Main GUI setup
root = tk.Tk()
root.title("Logic Gate Simulator for Arithmetic Operations")
root.config(bg="beige")

tk.Label(root, text="Input A (Binary):", bg="beige").grid(row=0, column=0, padx=10, pady=5)
entry_a = tk.Entry(root, bg="#D3D3D3")
entry_a.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Input B (Binary):", bg="beige").grid(row=1, column=0, padx=10, pady=5)
entry_b = tk.Entry(root, bg="#D3D3D3")
entry_b.grid(row=1, column=1, padx=10, pady=5)

operation_var = tk.StringVar(value="Addition")
operation_menu = tk.OptionMenu(root, operation_var, "Addition", "Subtraction", "Multiplication")
operation_menu.grid(row=2, column=1, padx=10, pady=5)

result_label = tk.Label(root, text="Result:", font=("Arial", 12), bg="beige")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

canvas = tk.Canvas(root, width=300, height=150, bg="beige")
canvas.grid(row=4, column=0, columnspan=2, pady=10)

perform_button = tk.Button(root, text="Calculate", command=perform_operation)
perform_button.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
