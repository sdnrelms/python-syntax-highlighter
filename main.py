from highlighter import CustomText, LineNumbers, SyntaxHighlighter
from lexer import Lexer
import tkinter as tk
        
def main():
    #dark mode renk paleti
    DARK_BG = "#2d2d2d"
    DARK_FG = "#e0e0e0"
    DARK_TEXT_BG = "#3d3d3d"
    DARK_SELECTION = "#4d4d4d"
    DARK_LINE_NUMBERS = "#5d5d5d"
    DARK_RESULT_BG = "#252525"

    #tk pencere oluşturma
    root = tk.Tk()
    root.title("Python Syntax Highlighter - Anlık Parse Sonucu")
    root.geometry("1200x800")
    root.configure(bg=DARK_BG)

    #ana frame
    main_frame = tk.Frame(root, bg=DARK_BG)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    #kodun yazıldığı üst kısım
    editor_frame = tk.Frame(main_frame, bg=DARK_BG)
    editor_frame.pack(fill="both", expand=True)

    #satır numaraları
    line_numbers = LineNumbers(
        editor_frame, 
        None,  
        bg=DARK_LINE_NUMBERS,
        fg=DARK_FG
    )
    line_numbers.pack(side="left", fill="y")

    #text widget ve scrollbar için frame
    text_frame = tk.Frame(editor_frame, bg=DARK_BG)
    text_frame.pack(side="right", fill="both", expand=True)
    
    #text widget için scrollbar
    text_scrollbar = tk.Scrollbar(text_frame)
    text_scrollbar.pack(side="right", fill="y")

    #text widget
    text = CustomText(
        text_frame, 
        width=80, 
        height=20, 
        font=("Consolas", 12), 
        wrap="none",
        bg=DARK_TEXT_BG,
        fg=DARK_FG,
        insertbackground=DARK_FG,
        selectbackground=DARK_SELECTION,
        yscrollcommand=lambda *args: on_scroll(*args)
    )
    text.pack(side="left", fill="both", expand=True)
    
    #simdi line_numbersa text widgetini ata
    line_numbers.text_widget = text
    
    #scroll fonksiyonu - hem text hem line_numbers
    def on_scroll(*args):
        text_scrollbar.set(*args)
        line_numbers.yview_moveto(args[0])
    
    #scrollbari text widget ile bağla ve line_numbersi de scroll et
    def on_scrollbar(*args):
        text.yview(*args)
        line_numbers.yview(*args)
    
    text_scrollbar.config(command=on_scrollbar)

    #parse sonucu gösterme alt kısım
    result_label = tk.Label(
        main_frame, 
        text="Parse Sonucu:", 
        font=("Arial", 12, "bold"),
        bg=DARK_BG,
        fg=DARK_FG
    )
    result_label.pack(anchor="w", pady=(10, 5))

    #parse result için frame
    result_frame = tk.Frame(main_frame, bg=DARK_BG)
    result_frame.pack(fill="both", expand=True)
    
    #parse result için scrollbar
    result_scrollbar = tk.Scrollbar(result_frame)
    result_scrollbar.pack(side="right", fill="y")

    #parse result text widget
    parse_result = tk.Text(
        result_frame, 
        height=15, 
        width=80, 
        font=("Consolas", 10), 
        wrap="word", 
        state='disabled', 
        bg=DARK_RESULT_BG,
        fg=DARK_FG,
        insertbackground=DARK_FG,
        selectbackground=DARK_SELECTION,
        yscrollcommand=result_scrollbar.set
    )
    parse_result.pack(side="left", fill="both", expand=True)
    result_scrollbar.config(command=parse_result.yview)

    #lexer ve highlighter oluşturma
    lexer = Lexer()
    highlighter = SyntaxHighlighter(text, lexer, parse_result, dark_mode=True)

    #satır numaralarının güncellenmesi için
    def on_text_change(event=None):
        line_numbers.update_line_numbers()
    
    text.bind("<<Change>>", on_text_change)

    #frame açılınca örnek kod
    sample_code = '''# Python Syntax Highlighter Example
def calculate_fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Test the function
numbers = [0, 1, 2, 3, 5, 8, 13]
for num in numbers:
    result = calculate_fibonacci(num)
    print(f"Fibonacci({num}) = {result}")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name} and I'm {self.age} years old!"

# Create person instance
person = Person("Alice", 25)
message = person.greet()
print(message)

# Number examples
integer = 42
floating = 3.14159
'''
    
    text.insert("1.0", sample_code)
    highlighter.highlight(sample_code)
    highlighter.update_parse_result(sample_code)
    line_numbers.update_line_numbers()

    root.mainloop()

#maini başlat
if __name__ == "__main__":
    main()