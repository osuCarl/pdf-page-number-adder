import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QFileDialog, QMessageBox, QHBoxLayout, QListWidgetItem
)
from PyQt5.QtCore import Qt
from core import process_pdfs  # 你的核心处理函数

class PdfListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QListWidget.InternalMove)

class PdfManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 文件顺序管理")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        self.pdf_list_widget = PdfListWidget()
        layout.addWidget(self.pdf_list_widget)

        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ 添加PDF")
        self.btn_add.clicked.connect(self.add_pdf)
        btn_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("➖ 移除最后一个")
        self.btn_remove.clicked.connect(self.remove_pdf)
        btn_layout.addWidget(self.btn_remove)

        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.start_processing)
        btn_layout.addWidget(self.btn_start)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_pdf(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择PDF文件", "", "PDF Files (*.pdf)"
        )
        for file_path in files:
            item = QListWidgetItem(file_path)
            self.pdf_list_widget.addItem(item)

    def remove_pdf(self):
        count = self.pdf_list_widget.count()
        if count > 0:
            self.pdf_list_widget.takeItem(count - 1)

    def start_processing(self):
        pdf_paths = [self.pdf_list_widget.item(i).text() for i in range(self.pdf_list_widget.count())]
        if not pdf_paths:
            QMessageBox.warning(self, "提示", "PDF 列表为空！")
            return
        try:
            process_pdfs(pdf_paths)  # 调用你的核心代码
            QMessageBox.information(self, "完成", "处理完成！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理失败：{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PdfManager()
    win.show()
    sys.exit(app.exec_())