import tkinter as tk
from parser import Parser

#highlighting ve parse sonuc gosterimi yapılan classımız 
class SyntaxHighlighter:
    def __init__(self, text_widget, lexer, parse_result_widget, dark_mode=False):
        self.text = text_widget
        self.lexer = lexer
        self.parse_result_widget = parse_result_widget
        self.dark_mode = dark_mode

        #renklendirme, her token için bi renk 
        if self.dark_mode:
            self.text.tag_configure("KEYWORD", foreground="#7ab6e7")
            self.text.tag_configure("BUILTIN", foreground="#7c75d6")
            self.text.tag_configure("IDENTIFIER", foreground="#bc80d8")
            self.text.tag_configure("NUMBER", foreground="#4ec9b0")
            self.text.tag_configure("STRING", foreground="#ce9178")
            self.text.tag_configure("FSTRING", foreground="#caf7f4")
            self.text.tag_configure("COMMENT", foreground="#6a9955")
            self.text.tag_configure("OPERATOR", foreground="#d5e98f")
            self.text.tag_configure("DELIMITER", foreground="#d5e98f")
        else:
            self.text.tag_configure("KEYWORD", foreground="blue")
            self.text.tag_configure("BUILTIN", foreground="darkorange")
            self.text.tag_configure("IDENTIFIER", foreground="black")
            self.text.tag_configure("NUMBER", foreground="purple")
            self.text.tag_configure("STRING", foreground="green")
            self.text.tag_configure("FSTRING", foreground="cyan")
            self.text.tag_configure("COMMENT", foreground="gray")
            self.text.tag_configure("OPERATOR", foreground="red")
            self.text.tag_configure("DELIMITER", foreground="brown")

        #yazı değiştikçe highlight yap
        self.text.bind("<KeyRelease>", self.on_modified)
        self.text.bind("<<Paste>>", self.on_modified)
        self.text.bind("<<Cut>>", self.on_modified)

    #kullanıcı kod yazdıkça cagrılıyor
    def on_modified(self, event=None):
        try:
            content = self.text.get("1.0", "end-1c")
            self.highlight(content)
            self.update_parse_result(content)
            #change eventi gönder (satır numaraları için)
            self.text.event_generate("<<Change>>")
        except Exception as e:
            print(f"Error in on_modified: {e}")


    #lexer ile tokenlara ayırır ve renklendirmeyi uygular
    def highlight(self, text):
        #önce tüm tagları kaldır
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", "end")

        try:
            tokens = self.lexer.tokenize(text)      #tokenize et
            for token in tokens:
                start_index = f"1.0 + {token.position[0]} chars"
                end_index = f"1.0 + {token.position[1]} chars"
                self.text.tag_add(token.type, start_index, end_index)
        except Exception as e:
            print(f"Highlighting error: {e}")

    #ast cikarma ve gostermeyi gerceklestırır
    def update_parse_result(self, text):
        self.parse_result_widget.config(state='normal')
        self.parse_result_widget.delete("1.0", "end")
        
        #basarılı ise ast gosterilir degilse hata mesajı ve pos yazılır
        try:
            tokens = self.lexer.tokenize(text)
            parser = Parser(tokens)
            ast = parser.parse()
            
            formatted_ast = self.format_ast(ast, indent=0)
            self.parse_result_widget.insert("1.0", f"✅ Parse Başarılı!\n\nAST:\n{formatted_ast}")
            self.parse_result_widget.config(fg="darkgreen")
            
        except Exception as e:
            error_msg = f"❌ Parse Hatası:\n{str(e)}\n\n"
            if 'parser' in locals() and hasattr(parser, 'current_token') and parser.current_token:
                error_msg += f"Token: {parser.current_token.value}\n"
                error_msg += f"Position: {parser.pos}/{len(tokens) if 'tokens' in locals() else '?'}"
            else:
                error_msg += "Position: EOF"
            self.parse_result_widget.insert("1.0", error_msg)
            self.parse_result_widget.config(fg="red")
        
        self.parse_result_widget.config(state='disabled')


    #ast'yi ekranda guzel gostermek icin girintileme 
    def format_ast(self, node, indent=0):
        if not isinstance(node, tuple):
            return "  " * indent + str(node)
        
        result = "  " * indent + node[0] + "\n"
        for child in node[1:]:
            if isinstance(child, (list, tuple)):
                if isinstance(child, list):
                    for item in child:
                        result += self.format_ast(item, indent + 1) + "\n"
                else:
                    result += self.format_ast(child, indent + 1) + "\n"
            else:
                result += "  " * (indent + 1) + str(child) + "\n"
        
        return result.rstrip()


#guı ye estetik olması için satır numraları ekleme
class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, bg='lightgray', fg='black', **kwargs):
        super().__init__(master, **kwargs)
        self.text_widget = text_widget
        self.config(
            width=4, 
            padx=4, 
            takefocus=0, 
            border=0,
            background=bg,
            foreground=fg,
            state='disabled', 
            wrap='none', 
            font=('Consolas', 12) if text_widget else ('Consolas', 12)
        )
        
        if self.text_widget:
            self.text_widget.bind("<<Change>>", self.on_change)
            self.text_widget.bind("<MouseWheel>", self.on_mousewheel)
            self.text_widget.bind("<Button-4>", self.on_mousewheel)
            self.text_widget.bind("<Button-5>", self.on_mousewheel)
            
        self.update_line_numbers()

    def on_change(self, event=None):
        #degişiklikten sonra satır numaralarını güncelleme
        self.after_idle(self.update_line_numbers) 

    def on_mousewheel(self, event=None):
        #mouse ile scroll edildiğinde line numbersı da scroll et
        self.after_idle(self.sync_scroll)

    def sync_scroll(self):
        if self.text_widget:
            #text widgetın scroll pozisyonunu
            top, bottom = self.text_widget.yview()
            #line numbersı aynı pozisyona scroll etme
            self.yview_moveto(top)

    def update_line_numbers(self):
        if not self.text_widget:
            return
            
        self.config(state='normal')
        self.delete("1.0", "end")

        #text widget'taki gerçek satır sayısı
        last_line = self.text_widget.index("end-1c").split('.')[0]
        line_count = int(last_line)
            
        line_numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self.insert("1.0", line_numbers)
        self.config(state='disabled')
        
        #scroll senkronizasyonu
        self.sync_scroll()


#satır numaraları ve highlighting özellikleri eklemek için oluşturuldu
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
