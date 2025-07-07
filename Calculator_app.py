import customtkinter as ctk
import math

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("350x600")  # Increased height for history
        self.resizable(True, True)
        self.theme_mode = "dark"
        self._create_widgets()
        self.expression = ""
        self.history = []  # Store calculation history
        self.just_evaluated = False  # Track if last action was '='

    def _create_widgets(self):
        # Configure grid weights for responsive layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        for i in range(9):  # Increased rows for history
            self.grid_rowconfigure(i, weight=1)

        # Theme toggle button
        self.theme_button = ctk.CTkButton(self, text="☀️", width=50, height=30, font=("Arial", 16),
                                          command=self._toggle_theme)
        self.theme_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # History display
        self.history_display = ctk.CTkTextbox(self, height=80, font=("Arial", 12))
        self.history_display.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        self.history_display.configure(state="disabled")  # Read-only

        # Main display
        self.display = ctk.CTkEntry(self, font=("Arial", 24), justify='right', height=50)
        self.display.grid(row=2, column=0, columnspan=4, padx=10, pady=20, sticky="ew")

        buttons = [
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('+', 6, 2), ('=', 6, 3),
            ('C', 7, 0), ('√', 7, 1), ('^', 7, 2), ('log', 7, 3),
            ('exp', 8, 0), ('(', 8, 1), (')', 8, 2), ('DEL', 8, 3)
        ]

        for (text, row, col) in buttons:
            btn = ctk.CTkButton(self, text=text, font=("Helvetica", 18),
                                command=lambda t=text: self._on_button_click(t))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def _toggle_theme(self):
        if self.theme_mode == "light":
            self.theme_mode = "dark"
            self.theme_button.configure(text="☀️")
            ctk.set_appearance_mode("dark")
        else:
            self.theme_mode = "light"
            self.theme_button.configure(text="🌙")
            ctk.set_appearance_mode("light")

    def _on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display.delete(0, ctk.END)
            self._clear_history()  # Clear history when C is pressed
            self.just_evaluated = False
        elif char == 'DEL':
            self.expression = self.expression[:-1]
            self.display.delete(0, ctk.END)
            self.display.insert(0, self.expression)
            self.just_evaluated = False
        elif char == '=':
            try:
                original_expression = self.expression
                result = self._evaluate(self.expression)
                self.display.delete(0, ctk.END)
                self.display.insert(0, str(result))
                self.expression = str(result)
                self._update_history(original_expression, result)  # Add to history
                self.just_evaluated = True
            except Exception:
                self.display.delete(0, ctk.END)
                self.display.insert(0, "Error")
                self.expression = ""
                self.just_evaluated = False
        elif char in ('√', 'log', 'exp', '^'):
            if self.just_evaluated:
                self.expression = ""
                self.display.delete(0, ctk.END)
                self.just_evaluated = False
            if char == '√':
                self.expression += 'sqrt('
                self.display.insert(ctk.END, '√(')
            elif char == 'log':
                self.expression += 'log10('
                self.display.insert(ctk.END, 'log(')
            elif char == 'exp':
                self.expression += 'exp('
                self.display.insert(ctk.END, 'exp(')
            elif char == '^':
                self.expression += '**'
                self.display.insert(ctk.END, '^')
        else:
            if self.just_evaluated:
                self.expression = ""
                self.display.delete(0, ctk.END)
                self.just_evaluated = False
            self.expression += char
            self.display.insert(ctk.END, char)

    def _evaluate(self, expr):
        # Replace user-friendly symbols with Python functions
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('log10', 'math.log10')
        expr = expr.replace('exp', 'math.exp')
        return eval(expr, {"math": math, "__builtins__": {}})

    def _update_history(self, calculation, result):
        """Add calculation to history with fading pattern"""
        # Add new calculation to history
        self.history.append(f"{calculation} = {result}")
        
        # Keep only last 5 calculations for fading effect
        if len(self.history) > 5:
            self.history = self.history[-5:]
        
        # Update history display with fading pattern
        self.history_display.configure(state="normal")
        self.history_display.delete("1.0", ctk.END)
        
        for i, entry in enumerate(self.history):
            # Calculate opacity based on position (newer = more opaque)
            opacity = 1.0 - (i * 0.15)  # Fade by 15% for each older entry
            opacity = max(0.3, opacity)  # Minimum opacity of 30%
            
            # Add entry with appropriate formatting
            if i == 0:  # Most recent
                self.history_display.insert(ctk.END, f"➤ {entry}\n", "recent")
            else:  # Older entries
                self.history_display.insert(ctk.END, f"  {entry}\n", "older")
        
        self.history_display.configure(state="disabled")
        
        # Configure text colors for fading effect
        self.history_display.tag_config("recent", foreground="#FFFFFF")
        self.history_display.tag_config("older", foreground="#CCCCCC")

    def _clear_history(self):
        """Clear the history display"""
        self.history_display.configure(state="normal")
        self.history_display.delete("1.0", ctk.END)
        self.history_display.configure(state="disabled")
        self.history = []

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calculator()
    app.mainloop()
