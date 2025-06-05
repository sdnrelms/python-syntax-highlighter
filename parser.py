class Parser:
    #tokenları alır ve pos ile takip eder
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    #bir sonraki tokene gecmeyi saglar
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    #gelecek tokene bakmayı saglar
    def peek(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None

    #satır numara takibi
    def get_line_number(self):
        if self.current_token is None:
            return "EOF"
        return f"pos:{self.pos}"

    #sıradaki tokenin type ve valuesine bakar uygunluk durumuna gore error uretir ya da advance ile ilerler
    def expect(self, type_, value=None):
        if self.current_token is None:
            raise SyntaxError(f"Beklenmeyen giriş sonu (beklenen: {type_})")
        if self.current_token.type != type_:
            raise SyntaxError(f"{self.get_line_number()} satırı: Beklenen tür '{type_}', ancak '{self.current_token.type}' bulundu ('{self.current_token.value}')")
        if value is not None and self.current_token.value != value:
            raise SyntaxError(f"{self.get_line_number()} satırı: Beklenen değer '{value}', ancak '{self.current_token.value}' bulundu")
        self.advance()

    def parse(self):
        return self.parse_program()

    #tum satırları sırayla işleyen fonk.
    def parse_program(self):
        statements = []
        while self.current_token is not None:
            stmt = self.parse_statement()
            statements.append(stmt)
        return ("PROGRAM", statements)

    #tokenları ilgili fonksiyona yonlendirme ve tanımlama işlemini yapar
    def parse_statement(self):
        #yorum satırlarını atla
        if self.current_token.type == "COMMENT":
            comment_value = self.current_token.value
            self.advance()
            return ("COMMENT", comment_value)
            
        if self.current_token.type == "KEYWORD":
            if self.current_token.value == "if":
                return self.parse_if_stmt()
            elif self.current_token.value == "while":
                return self.parse_while_stmt()
            elif self.current_token.value == "for":  
                return self.parse_for_stmt()
            elif self.current_token.value == "def":
                return self.parse_func_def()
            elif self.current_token.value == "return":
                return self.parse_return_stmt()
            elif self.current_token.value == "print":
                return self.parse_print_stmt()
            elif self.current_token.value == "class":
                return self.parse_class_def()
            elif self.current_token.value == "elif":
                return self.parse_if_stmt()
            #hata almamak için tanımlamalar, bosta kalan keywordler için
            elif self.current_token.value == "pass":        
                self.advance()
                return ("PASS",)
            elif self.current_token.value == "break":
                self.advance()
                return ("BREAK",)
            elif self.current_token.value == "continue":
                self.advance()
                return ("CONTINUE",)
            else:
                #diğer anahtar kelimeler
                value = self.current_token.value
                self.advance()
                return ("KEYWORD", value)
            
        elif self.current_token.type in ["IDENTIFIER", "BUILTIN"]:
            #atama mı yoksa ifade mi kontrolu ve sonuca gore yonlendirme
            if self.is_assignment():
                return self.parse_assign_stmt()
            else:
                return self.parse_expr_stmt()
        else:
            return self.parse_expr_stmt()

    #bu bi atama mı kontrolu
    def is_assignment(self):
        saved_pos = self.pos
        try:
            #ilk identifier-builtini atla
            if self.current_token.type in ["IDENTIFIER", "BUILTIN"]:
                self.advance()
                
                #nokta notasyonu varsa devam et (self.abc = ... desteği için)
                while self.current_token and self.current_token.value == ".":
                    self.advance()  # . yı atla
                    if self.current_token and self.current_token.type in ["IDENTIFIER", "BUILTIN"]:
                        self.advance()  # identifier atla
                    else:
                        break
                
                # = işareti var mı kontrol et, varsa atamadır
                result = self.current_token and self.current_token.value == "="
                return result
        finally:
            #pozisyonu geriye al
            self.pos = saved_pos
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None


    #class tanımını parse ediyor
    def parse_class_def(self):
        self.expect("KEYWORD", "class")
        class_name = self.current_token.value
        self.expect("IDENTIFIER")
        
        #kalıtım için (class Myclass(a1,b1) gibi)
        bases = []
        if self.current_token and self.current_token.value == "(":
            self.advance()
            while self.current_token and self.current_token.value != ")":
                if self.current_token.type == "IDENTIFIER":
                    bases.append(self.current_token.value)
                    self.advance()
                    if self.current_token and self.current_token.value == ",":
                        self.advance()
            self.expect("DELIMITER", ")")
        
        #sondaki : kontrolu
        self.expect("DELIMITER", ":")
        body = self.parse_block()
        return ("CLASS_DEF", class_name, bases, body)
    

    #fonk. işleme
    def parse_func_def(self):
        self.expect("KEYWORD", "def")
        
        #fonksiyon ad kontrolu (__init__ gibi özel metodlar dahil edildi)
        if self.current_token.type not in ["IDENTIFIER", "BUILTIN"]:
            raise SyntaxError(f"Fonksiyon ismi bekleniyordu, ancak {self.current_token.type} bulundu")
        func_name = self.current_token.value
        self.advance()
        self.expect("DELIMITER", "(")
        
        #parametre listesi parse etme
        params = []
        if self.current_token and self.current_token.value != ")":
            params = self.parse_param_list()
        
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", ":")
        body = self.parse_block()
        return ("FUNC_DEF", func_name, params, body)

    #parametreleri , le ayrılmış okur
    def parse_param_list(self):
        params = []
        if self.current_token and self.current_token.type in ["IDENTIFIER", "BUILTIN"]:
            params.append(self.current_token.value)
            self.advance()
            while self.current_token and self.current_token.value == ",":
                self.advance()
                if self.current_token and self.current_token.type in ["IDENTIFIER", "BUILTIN"]:
                    params.append(self.current_token.value)
                    self.advance()
                else:
                    raise SyntaxError("',' sonrasında parametre ismi bekleniyor")
        return params
    

    #if koşulu ve sonrasının parse işlemini yapar
    def parse_if_stmt(self):
        keyword = self.current_token.value       #if veya elif olabilir
        self.advance()
        condition = self.parse_expression()
        self.expect("DELIMITER", ":")
        if_block = self.parse_block()
        
        elif_blocks = []
        else_block = None
        
        #elif bloklarını işleme
        while self.current_token and self.current_token.type == "KEYWORD" and self.current_token.value == "elif":
            self.advance()
            elif_condition = self.parse_expression()
            self.expect("DELIMITER", ":")
            elif_block = self.parse_block()
            elif_blocks.append(("ELIF", elif_condition, elif_block))
        
        #else bloğunu işleme
        if self.current_token and self.current_token.type == "KEYWORD" and self.current_token.value == "else":
            self.advance()
            self.expect("DELIMITER", ":")
            else_block = self.parse_block()
        
        return ("IF", keyword, condition, if_block, elif_blocks, else_block)

    #while dongusu parse işlemii
    def parse_while_stmt(self):
        self.expect("KEYWORD", "while")
        condition = self.parse_expression()
        self.expect("DELIMITER", ":")
        body = self.parse_block()
        return ("WHILE", condition, body)
    
    #for için parse işlemi ((for i in liste:) gibi bi tanım için "in" ":" vs. kontrolu yapılır)
    def parse_for_stmt(self):
        self.expect("KEYWORD", "for")
        
        if self.current_token.type != "IDENTIFIER":
            raise SyntaxError(f"'for' döngüsü bir değişken gerektirir, ancak {self.current_token.type} bulundu")
        target = self.current_token.value
        self.advance()
        
        if not (self.current_token and self.current_token.type == "KEYWORD" and self.current_token.value == "in"):
            raise SyntaxError(f"'for' döngüsü değişkeninden sonra 'in' anahtar kelimesi bekleniyordu, ancak '{self.current_token.value if self.current_token else 'EOF'}' bulundu")
        self.advance()
        
        iterable = self.parse_expression()
        
        if not (self.current_token and self.current_token.type == "DELIMITER" and self.current_token.value == ":"):
            raise SyntaxError(f"'for' döngüsünden sonra ':' bekleniyordu, ancak '{self.current_token.value if self.current_token else 'EOF'}' bulundu")
        self.advance()
        
        body = self.parse_block()
        return ("FOR", target, iterable, body)
    
    #kod blogunu parse etme, eger uygun tipteyse(if,while ....) parse eder
    def parse_block(self):
        statements = []
        if self.current_token and (
            self.current_token.type in ["KEYWORD", "IDENTIFIER", "BUILTIN", "COMMENT"]
        ):
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements
    
    #ifade baslatır
    def parse_expression(self):
        return self.parse_comparison()

    #karsılastırma ifadeleri için
    def parse_comparison(self):
        left = self.parse_addition()
        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ["==", "!=", "<", ">", "<=", ">="]:
            op = self.current_token.value
            self.advance()
            right = self.parse_addition()
            left = ("BIN_OP", op, left, right)
        return left

    #toplama cıkarma işlemleri için
    def parse_addition(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ["+", "-"]:
            op = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = ("BIN_OP", op, left, right)
        return left

    #çarpma bolme için
    def parse_term(self):
        left = self.parse_factor()
        while self.current_token and self.current_token.type == "OPERATOR" and self.current_token.value in ["*", "/", "%", "//"]:
            op = self.current_token.value
            self.advance()
            right = self.parse_factor()
            left = ("BIN_OP", op, left, right)
        return left

    #aritmetik ifadelerin en minik parcaya kadar cozumleme
    def parse_factor(self):
        token = self.current_token

        #- + varsa unary operator
        if token.type == "OPERATOR" and token.value in ["-", "+"]:
            op = token.value
            self.advance()
            operand = self.parse_factor()
            return ("UNARY_OP", op, operand)
        #sayı varsa sayı parse etme
        if token.type == "NUMBER":
            self.advance()
            return ("NUMBER", token.value)
        #strigse
        elif token.type == "STRING":
            self.advance()
            return ("STRING", token.value)
        #fstringse
        elif token.type == "FSTRING":
            self.advance()
            return ("FSTRING", token.value)
        #degiskenler için ve nokta notasyonnu destekle
        elif token.type in ["IDENTIFIER", "BUILTIN"]:
            name = self.parse_dotted_name()
            #fonk. cag. kontrolü
            if self.current_token and self.current_token.value == "(":
                return self.parse_function_call(name)
            return ("IDENTIFIER", name)
        #parantezli ifadeler için
        elif token.value == "(":
            self.expect("DELIMITER", "(")
            expr = self.parse_expression()
            self.expect("DELIMITER", ")")
            return expr
        #[] ve {} için
        elif token.value == "[":
            self.expect("DELIMITER", "[")
            elements = []
            if self.current_token and self.current_token.value != "]":
                elements.append(self.parse_expression())
                while self.current_token and self.current_token.value == ",":
                    self.advance()
                    if self.current_token and self.current_token.value != "]":
                        elements.append(self.parse_expression())
            self.expect("DELIMITER", "]")
            return ("LIST", elements)
        elif token.value == "{":
            self.expect("DELIMITER", "{")
            elements = []
            if self.current_token and self.current_token.value != "}":
                elements.append(self.parse_expression())
                while self.current_token and self.current_token.value == ",":
                    self.advance()
                    if self.current_token and self.current_token.value != "}":
                        elements.append(self.parse_expression())
            self.expect("DELIMITER", "}")
            return ("SET", elements)
        #tanıyamazsa hata verir
        else:
            raise SyntaxError(f"Beklenmeyen token: {token.value if token else 'EOF'} (tür: {token.type if token else 'None'})")
        

    #self.a.b gibi noktalı ifadeleri tanımlamak için
    def parse_dotted_name(self):
        if self.current_token.type not in ["IDENTIFIER", "BUILTIN"]:
            raise SyntaxError(f"Tanımlayıcı (identifier) bekleniyordu, ancak {self.current_token.type} bulundu")
            
        parts = [self.current_token.value]
        self.advance()
        
        while self.current_token and self.current_token.value == ".":
            self.advance()  # "." yı atla
            if self.current_token and self.current_token.type in ["IDENTIFIER", "BUILTIN"]:
                parts.append(self.current_token.value)
                self.advance()
            else:
                raise SyntaxError("'.' karakterinden sonra tanımlayıcı (identifier) bekleniyordu")
        
        return ".".join(parts)

    #atama işlemleri için fonk (x=0 vb.)
    def parse_assign_stmt(self):
        var_name = self.parse_dotted_name()
        self.expect("OPERATOR", "=")
        expr = self.parse_expression()
        return ("ASSIGN", var_name, expr)

    #sadece ifade parserde else'te cagrılıyor
    def parse_expr_stmt(self):
        expr = self.parse_expression()
        return ("EXPR", expr)

    #fonk. cagrıları işleme (fonk(1,2) vb.)
    def parse_function_call(self, func_name):       #fonk adı cagrıldıgı yerde verilir
        self.expect("DELIMITER", "(")
        args = []
        #fonk cagrısı ıcın gerekli seylerin kontrolu parantez, iki nokta vs.
        if self.current_token and self.current_token.value != ")":
            args.append(self.parse_expression())
            while self.current_token and self.current_token.value == ",":
                self.advance()
                if self.current_token and self.current_token.value != ")":
                    args.append(self.parse_expression())
        self.expect("DELIMITER", ")")
        return ("FUNC_CALL", func_name, args)

    
    #return kelimesi için tanımlama
    def parse_return_stmt(self):
        self.expect("KEYWORD", "return")
        if self.current_token and self.current_token.type not in ["COMMENT"]:
            expr = self.parse_expression()
            return ("RETURN", expr)
        return ("RETURN", None)

    #print parse'i yapılır
    def parse_print_stmt(self):
        self.expect("KEYWORD", "print")
        self.expect("DELIMITER", "(")
        args = []
        if self.current_token and self.current_token.value != ")":
            args.append(self.parse_expression())
            while self.current_token and self.current_token.value == ",":       #içine birden fazla ifade yazabilmek için
                self.advance()
                if self.current_token and self.current_token.value != ")":
                    args.append(self.parse_expression())
        self.expect("DELIMITER", ")")
        return ("PRINT", args)