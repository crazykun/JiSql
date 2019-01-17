import sys

from PyQt5.QtWidgets import QMainWindow ,QDesktopWidget,QApplication,QPushButton,QHBoxLayout,QWidget
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.resize(400,200)
        self.center()
        self.status=self.statusBar()
        self.status.showMessage("这是状态了提示",5000)
        self.setWindowTitle("PyQt MainWindow demo")

        self.button1=QPushButton("关闭窗口")
        self.button1.clicked.connect(self.onButtonClick)
        layout=QHBoxLayout()
        layout.addWidget(self.button1)

        main_frame=QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

    def center(self):
        screen =QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

    def onButtonClick(self):
        sender=self.sender()
        print(sender.text()+' 被按下了')
        qApp=QApplication.instance()
        qApp.quit()

if __name__=="__main__":
    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/ji.ico"))
    form=MainWindow()
    form.show()
    sys.exit(app.exec_())