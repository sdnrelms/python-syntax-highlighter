# 💻 Python Syntax Highlighter

Bu proje, Python diline özel olarak hazırlanmış bir **sözdizimi vurgulayıcı (syntax highlighter)** ve **ayrıştırıcı (parser)** sistemidir. Kullanıcı arayüzü üzerinde yazılan kodlar anlık olarak analiz edilir, renklendirilir ve AST (Soyut Sözdizim Ağacı) olarak kullanıcıya gösterilir. Programlama Dilleri dersi kapsamında dönem projesidir.

Hiçbir harici kütüphane kullanmadan, sıfırdan bir lexer ve parser geliştirilmiştir.

👉 [Demo videosu için tıklayınız](https://youtu.be/7w5ISfNn26Q)
<br>
📑 [Medium yazısı için tıklayınız](https://medium.com/@sudenurelmas08/python-i%C3%A7in-ger%C3%A7ek-zamanl%C4%B1-s%C3%B6zdizimi-vurgulay%C4%B1c%C4%B1-1bc6307e416a)
<br>
🖊️ [Dokümantasyon için tıklayınız](https://github.com/sdnrelms/python-syntax-highlighter/blob/main/rapor_sudenurelmas.pdf)



## 🎯 Mevcut Özellikler

- ✅ Gerçek zamanlı kod renklendirme (9 farklı token türü)
- ✅ Lexer: Anahtar kelime, sayı, string, yorum, f-string vb. ayrımı
- ✅ Parser: Recursive descent yöntemiyle AST üretimi
- ✅ Tkinter arayüzü ile kullanıcı dostu GUI
- ✅ Hatalı sözdizimlerinde konumlu hata mesajları
- ✅ Karanlık tema desteği (Dark Mode)
- ✅ Satır numarası gösterimi
- ✅ Nokta notasyonu desteği (object.method)
- ✅ F-string tanıma
- ✅ Çok satırlı string desteği
- ✅ Class ve fonksiyon tanımları



## 🗝️ Kullanılan Teknikler

| Bileşen           | Açıklama |
|-------------------|---------|
| **Lexer**         | `class Lexer`: Python kodlarını token’lara ayırır |
| **Parser**        | `class Parser`: Token akışını sözdizimsel olarak çözümler |
| **AST**           | Her ifade için ağaç yapısı üretir |
| **SyntaxHighlighter** | `class SyntaxHighlighter`: Token’lara göre renklendirme yapar |
| **GUI**           | `Tkinter` ile özelleştirilmiş yazı alanı, satır numarası, sonuç paneli |



## 🎨 Renklendirme Şeması

| Token Türü  | Renk (Dark Mode) | Örnekler |
|-------------|------------------|-----------|
| `KEYWORD`   | Mavi (#7ab6e7)   | `if`, `def`, `class`,`return` |
| `BUILTIN`   | Mor (#7c75d6)    |  `print`, `str`, `len`,`self` |
| `IDENTIFIER`| Açık Mor (#bc80d8) | değişken adları |
| `NUMBER`    | Turkuaz (#4ec9b0) |  `42`, `3.1415` |
| `STRING`    | Somon (#ce9178)  | `hello`, `syntax`, `highlighter`|
| `FSTRING`   | Açık Mavi (#caf7f4) |  `f"hello" {name}` |
| `COMMENT`   | Yeşil (#6a9955)  | `#bu yorum satırıdır`  |
| `OPERATOR`  | Sarı (#d5e98f)   | `+`, `-`, `==`, `>`  |
| `DELIMITER` | Sarı (#d5e98f)   |  `[`, `]`, `(`,`)`, `:`|



## 📸 Ekran Görüntüsü

- Başarılı Parsing
![basarili_parse](https://github.com/sdnrelms/python-syntax-highlighter/blob/main/img/image1.png)



- Hatalı Parsing
![basarisiz_parse](https://github.com/sdnrelms/python-syntax-highlighter/blob/main/img/image.png)






## 🚀 Nasıl Çalıştırılır?

#### Gereksinimler

- Python 3.8 veya üzeri
- Tkinter (Python ile birlikte gelir)

#### Kurulum

1. Projeyi indirin:
```bash 
git clone https://github.com/sdnrelms/python-syntax-highlighter.git
cd python-syntax-highlighter
```
2. Terminal veya IDE üzerinden çalıştırın:
```bash
python main.py
```




## 📁 Dosya Yapısı
```
python-syntax-highlighter/
│
├── main.py              # GUI, çalıştırma kodu ve örnek kod yükleme
├── lexer.py             # Tokenizer sınıfı
├── parser.py            # Recursive descent parser
├── highlighter.py       # GUI ve Renklendirme sınıfı
├── img                  # Proje ekran görüntüleri
├── README.md            # Bu dosya
└── rapor_sudenurelmas.pdf # Proje dokümanı
```



## ⚙️ Detaylı Teknik Açıklaması

#### 📝 Lexical Analysis (Lexer)
- Lexer, kaynak kodun en temel bileşeni olan token'lara ayrıştırılmasından sorumludur.

##### Token Türleri
- KEYWORD,     BUILTIN,    IDENTIFIER,   NUMBER,   STRING,     FSTRING,     COMMENT,     OPERATOR,    DELIMITER   

##### Lexer Algoritması

```
def tokenize(self, text):
    """
    Karakter karakter okuyarak token'ları üretir.
    
    Algoritma:
    1. Whitespace karakterleri atla
    2. Yorum satırlarını tanı (#)
    3. String literals tanı (', ", """, f-strings)
    4. Sayıları tanı (integer, float)
    5. Anahtar kelimeleri ve identifier'ları ayırt et
    6. Operatör ve delimiter'ları tanı
    """

```

#### 🌳 Syntax Analysis (Parser)
- Parser, token akışını alarak Abstract Syntax Tree (AST) üretir. Recursive Descent yöntemi kullanılır.


```
# Python Grammar:
<program>       ::= <statement>*

<statement>     ::= <assign_stmt> 
                  | <if_stmt> 
                  | <while_stmt> 
                  | <func_def> 
                  | <return_stmt> 
                  | <print_stmt>
                  | <expr_stmt>

<assign_stmt>   ::= IDENTIFIER "=" <expression>

<if_stmt>       ::= "if" <expression> ":" <block> ["elif" <expression> ":" <block>]* ["else" ":" <block>]

<while_stmt>    ::= "while" <expression> ":" <block>

<func_def>      ::= "def" IDENTIFIER "(" [<param_list>] ")" ":" <block>

<param_list>    ::= IDENTIFIER ("," IDENTIFIER)*

<return_stmt>   ::= "return" [<expression>]

<print_stmt>    ::= "print" "(" [<expression> ("," <expression>)*] ")"

<expr_stmt>     ::= <expression>

<block>         ::= INDENT <statement>+ DEDENT | <statement>

<expression>    ::= <comparison> (("and" | "or") <comparison>)*

<comparison>    ::= <addition> (("==" | "!=" | "<" | ">" | "<=" | ">=") <addition>)*

<addition>      ::= <term> (("+" | "-") <term>)*

<term>          ::= <factor> (("*" | "/") <factor>)*

<factor>        ::= NUMBER 
                  | STRING 
                  | IDENTIFIER 
                  | IDENTIFIER "(" [<arg_list>] ")"
                  | "(" <expression> ")" 
                  | "not" <factor>
                  | "[" [<expression_list>] "]"
                  | "{" [<keyvalue_list>]}"

<arg_list>      ::= <expression> ("," <expression>)*

<expression_list> ::= <expression> ("," <expression>)*

<keyvalue_list> ::= STRING ":" <expression> ("," STRING ":" <expression>)*
```

#### 📜 AST (Abstract Syntax Tree) Yapısı
- AST, kodun semantik yapısını temsil eden ağaç veri yapısıdır.

**Örnek AST Çıktısı:**
- Kod :

```
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
- AST :

```
✅ Parse Başarılı!

AST:
PROGRAM
  FUNC_DEF
    fibonacci
    n
    IF
      if
      BIN_OP
        <=
        IDENTIFIER
          n
        NUMBER
          1
      RETURN
        IDENTIFIER
          n
      None
  RETURN
    BIN_OP
      +
      FUNC_CALL
        fibonacci
        BIN_OP
          -
          IDENTIFIER
            n
          NUMBER
            1
      FUNC_CALL
        fibonacci
        BIN_OP
          -
          IDENTIFIER
            n
          NUMBER
            2
```


#### 🎨 Syntax Highlighting Sistemi
- Real-time highlighting sistemi token-based çalışır:

```
def highlight(self, text):
    """
    1. Lexer ile text'i tokenize et
    2. Her token için Tkinter tag oluştur  
    3. Token pozisyonuna göre renklendirme uygula
    """
    tokens = self.lexer.tokenize(text)
    for token in tokens:
        start_index = f"1.0 + {token.position[0]} chars"
        end_index = f"1.0 + {token.position[1]} chars"
        self.text.tag_add(token.type, start_index, end_index)
```



#### 🖼️ GUI (Tkinter)
- Gerçek zamanlı sözdizim vurgulama (real-time syntax highlighting) işlevini kullanıcı dostu bir arayüz ile sunar. GUI, Python'da Tkinter kütüphanesi kullanılarak geliştirilmiştir.

Temel Özellikler
- AST Görselleştirme:
  - Kod yazıldıkça lexer ve parser çalışır.

  - Başarılıysa AST hiyerarşik şekilde görüntülenir.

  - Hatalıysa hata mesajı ve pozisyon bilgisi gösterilir.


- Satır Numaraları:

  - Kod penceresinin soluna otomatik olarak satır numaraları eklenir.

  - Yazı değiştikçe veya pencere kaydırıldıkça güncellenir.


  ```
  class LineNumbers(tk.Text):
    """
    Satır numaralarını gösteren özel Text widget.
    
    - `text_widget` ile ana kod alanına bağlanır.
    - `<<Change>>` ve `scroll` event’lerine tepki vererek
      satır numaralarını otomatik günceller.
    """
  ```


