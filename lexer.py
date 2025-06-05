#Token'lari oluşturma
class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

#Token sınıfı yardımıyla kodu tokenlara ayıran class 
class Lexer:
    def __init__(self):         #gereklii sabitler tanımlanır
        self.keywords = ["if", "else", "while", "for", "def", "return", "print", 
                        "class", "import", "from", "as", "try", "except", "finally",
                        "with", "lambda", "yield", "async", "await", "None", "True", 
                        "False", "and", "or", "not", "in", "is", "break", "continue",
                        "elif", "pass", "raise", "assert", "del", "global", "nonlocal"]
        
        self.operators = ["+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">=",
                         "+=", "-=", "*=", "/=", "%", "//", "**", "&", "|", "^", "~",
                         "<<", ">>"]
        
        self.delimiters = ["(", ")", "{", "}", "[", "]", ";", ",", ".", ":", "'", '"']
        
        self.builtins = {"print", "len", "str", "int", "float", "list", "dict", "range", 
                        "enumerate", "zip", "map", "filter", "sum", "max", "min", "abs",
                        "round", "type", "isinstance", "hasattr", "getattr", "setattr",
                        "open", "input", "sorted", "reversed", "any", "all", "bool",
                        "set", "tuple", "frozenset", "bytes", "bytearray", "memoryview",
                        "self", "cls", "__init__", "__str__", "__repr__", "__len__",
                        "super", "property", "staticmethod", "classmethod"}
    
    #karakterin ne olduguna bakılır
    
    #boşluk mu 
    def is_whitespace(self, char):
        return char in [' ', '\t', '\n', '\r']
    
    #sayı mı 
    def is_digit(self, char):
        return '0' <= char <= '9'
    
    #harf ya da _ mi
    def is_letter(self, char):
        return ('a' <= char <= 'z') or ('A' <= char <= 'Z') or char == '_'
    
    #metni karakter karakter okur ve token haline getirir
    def tokenize(self, text):
        tokens = []
        i = 0
        
        while i < len(text):
            #bosluklar atlanır
            if self.is_whitespace(text[i]):
                i += 1
                continue
            
            #yorum satırı 
            if text[i] == '#':
                start = i
                i += 1
                while i < len(text) and text[i] != '\n':
                    i += 1
                tokens.append(Token("COMMENT", text[start:i], (start, i)))
                continue

            #f-stringleri tanımlama
            if text[i] == 'f' and i + 1 < len(text) and text[i + 1] in ['"', "'"]:
                start = i
                i += 1  # f'yi atla
                quote_type = text[i]
                i += 1  # tırnağı atla
                while i < len(text) and text[i] != quote_type:
                    if text[i] == '\\' and i + 1 < len(text):
                        i += 2
                    else:
                        i += 1
                if i < len(text):
                    i += 1
                tokens.append(Token("FSTRING", text[start:i], (start, i)))
                continue
            
            #tek tırnaklı string
            if text[i] == "'":
                start = i
                i += 1
                while i < len(text) and text[i] != "'":
                    if text[i] == '\\' and i + 1 < len(text):
                        i += 2
                    else:
                        i += 1
                if i < len(text):
                    i += 1
                tokens.append(Token("STRING", text[start:i], (start, i)))
                continue
            
            #çift tırnaklı string
            if text[i] == '"':
                start = i
                i += 1
                while i < len(text) and text[i] != '"':
                    if text[i] == '\\' and i + 1 < len(text):
                        i += 2
                    else:
                        i += 1
                if i < len(text):
                    i += 1
                tokens.append(Token("STRING", text[start:i], (start, i)))
                continue
            
            #üç tırnaklı string
            if i < len(text) - 2 and text[i:i+3] in ['"""', "'''"]:
                quote_type = text[i:i+3]
                start = i
                i += 3
                while i <= len(text) - 3:
                    if text[i:i+3] == quote_type:
                        i += 3
                        break
                    i += 1
                tokens.append(Token("STRING", text[start:i], (start, i)))
                continue
            
            #sayıları tanımlama
            if self.is_digit(text[i]):
                start = i
                has_dot = False
                while i < len(text) and (self.is_digit(text[i]) or (text[i] == '.' and not has_dot)):
                    if text[i] == '.':
                        has_dot = True
                    i += 1
                tokens.append(Token("NUMBER", text[start:i], (start, i)))
                continue
            
            #tanımlayıcılar ve anahtar kelimeleri tanıma
            if self.is_letter(text[i]):
                start = i
                while i < len(text) and (self.is_letter(text[i]) or self.is_digit(text[i])):
                    i += 1
                word = text[start:i]
                
                if word in self.keywords:
                    tokens.append(Token("KEYWORD", word, (start, i)))
                elif word in self.builtins:
                    tokens.append(Token("BUILTIN", word, (start, i)))
                else:
                    tokens.append(Token("IDENTIFIER", word, (start, i)))
                continue

            #ayraçları tanıma
            if text[i] in self.delimiters:
                tokens.append(Token("DELIMITER", text[i], (i, i+1)))
                i += 1
                continue

            #operatörleri tanımlama
            found_operator = False
            for op_length in [2, 1]:
                if i + op_length <= len(text):
                    op = text[i:i+op_length]
                    if op in self.operators:
                        tokens.append(Token("OPERATOR", op, (i, i+op_length)))
                        i += op_length
                        found_operator = True
                        break
            
            if found_operator:
                continue
            
            #tanımlanamayan bi karakter olursa consola bastırsın
            if i < len(text) and not self.is_whitespace(text[i]):
                print(f"Tanımlanamayan karakter: '{text[i]}' konum: {i}")
                i += 1
        
        return tokens