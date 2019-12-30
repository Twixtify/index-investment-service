import re


class TextParser:
    def __init__(self, texts):
        for text in texts:
            if not isinstance(text, str):
                raise TypeError("Expected '%s', got '%s' " % (str.__name__, type(text).__name__))
        self.texts = texts

    def update(self, new_texts):
        self.texts = new_texts

    def parse_numeric_texts(self):
        text_list = []
        for text in self.texts:
            text_list.append(self.parse_numeric(text))
        return text_list

    def replace_char_texts(self, old_char, new_char):
        text_list = []
        for text in self.texts:
            text_list.append(self.replace_char(text, old_char, new_char))
        return text_list

    @staticmethod
    def replace_char(text, old_char, new_char):
        new_text = text.replace(old_char, new_char)
        return new_text

    @staticmethod
    def parse_numeric(text):
        regex = r'[^\d.]+'
        parser = re.compile(regex)
        return parser.sub('', str(text))


if __name__ == "__main__":
    tp = TextParser(["1,a4", "2,b5"])
    tp.texts = tp.replace_char_texts(",", ".")
    tp.texts = tp.parse_numeric_texts()
    print(tp.texts)
