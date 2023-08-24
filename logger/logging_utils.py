import sys
import io

class FileWriter:
    def __init__(self, filename):
        self.file = io.open(filename, 'w', encoding='utf-8')
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, text):
        self.file.write(text)
        self.stdout.write(text)

    def flush(self):
        self.file.flush()

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            sys.stdout = self.stdout

# 用于在其他文件中引用
text_writer = FileWriter('./logger/log.txt')