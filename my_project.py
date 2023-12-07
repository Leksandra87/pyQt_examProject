from PySide6 import QtWidgets, QtCore
import psutil
import platform


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """
        lableProcessorName = QtWidgets.QLabel("Процессор")
        lableProcessorName.setMinimumWidth(120)
        self.ProcNameLineEdit = QtWidgets.QLineEdit()
        self.ProcNameLineEdit.setReadOnly(True)
        layoutProcessor = QtWidgets.QHBoxLayout()
        layoutProcessor.addWidget(lableProcessorName)
        layoutProcessor.addWidget(self.ProcNameLineEdit)

        lableCores = QtWidgets.QLabel("Количество ядер")
        lableCores.setMinimumWidth(120)
        self.CoresLineEdit = QtWidgets.QLineEdit()
        self.CoresLineEdit.setReadOnly(True)
        layoutCores = QtWidgets.QHBoxLayout()
        layoutCores.addWidget(lableCores)
        layoutCores.addWidget(self.CoresLineEdit)

        lableProcessorLoad = QtWidgets.QLabel("Текущая загрузка")
        lableProcessorLoad.setMinimumWidth(120)
        self.ProcessorLoadLineEdit = QtWidgets.QLineEdit()
        self.ProcessorLoadLineEdit.setReadOnly(True)
        layoutProcessorLoad = QtWidgets.QHBoxLayout()
        layoutProcessorLoad.addWidget(lableProcessorLoad)
        layoutProcessorLoad.addWidget(self.ProcessorLoadLineEdit)

        self.ProcessorLoadPB = QtWidgets.QProgressBar()

        layoutProc = QtWidgets.QVBoxLayout()
        layoutProc.addLayout(layoutProcessor)
        layoutProc.addLayout(layoutCores)
        layoutProc.addLayout(layoutProcessorLoad)
        layoutProc.addWidget(self.ProcessorLoadPB)

        GBprocessor = QtWidgets.QGroupBox("Процессор")
        GBprocessor.setLayout(layoutProc)

# ----------------------------------------------------------------------------------------------------------------------
        lableRAMtotal = QtWidgets.QLabel('Объём памяти')
        lableRAMtotal.setMinimumWidth(120)
        self.RAMtotalLineEdit = QtWidgets.QLineEdit()
        self.RAMtotalLineEdit.setReadOnly(True)
        layoutRAMtotal = QtWidgets.QHBoxLayout()
        layoutRAMtotal.addWidget(lableRAMtotal)
        layoutRAMtotal.addWidget(self.RAMtotalLineEdit)

        lableRAMcurrent = QtWidgets.QLabel('Текущая загрузка ОП')
        lableRAMcurrent.setMinimumWidth(120)
        self.RAMcurrentLineEdit = QtWidgets.QLineEdit()
        self.RAMcurrentLineEdit.setReadOnly(True)
        layoutRAMcurret = QtWidgets.QHBoxLayout()
        layoutRAMcurret.addWidget(lableRAMcurrent)
        layoutRAMcurret.addWidget(self.RAMcurrentLineEdit)

        self.RAMload = QtWidgets.QProgressBar()

        layoutRAM = QtWidgets.QVBoxLayout()
        layoutRAM.addLayout(layoutRAMtotal)
        layoutRAM.addLayout(layoutRAMcurret)
        layoutRAM.addWidget(self.RAMload)

        GBram = QtWidgets.QGroupBox("...")
        GBram.setLayout(layoutRAM)

# ----------------------------------------------------------------------------------------------------------------------
        lableDisk = QtWidgets.QLabel("Количество жестких дисков")
        lableDisk.setMinimumWidth(160)
        self.DiskLineEdit = QtWidgets.QLineEdit()
        self.DiskLineEdit.setReadOnly(True)
        layoutD = QtWidgets.QHBoxLayout()
        layoutD.addWidget(lableDisk)
        layoutD.addWidget(self.DiskLineEdit)
        self.DiskInfoPlaintext = QtWidgets.QPlainTextEdit()
        layoutDisk = QtWidgets.QVBoxLayout()
        layoutDisk.addLayout(layoutD)
        layoutDisk.addWidget(self.DiskInfoPlaintext)

        GBdisk = QtWidgets.QGroupBox("...")
        GBdisk.setLayout(layoutDisk)



        FirstTabLayout = QtWidgets.QVBoxLayout()
        FirstTabLayout.addWidget(GBprocessor)
        FirstTabLayout.addWidget(GBram)
        FirstTabLayout.addWidget(GBdisk)




        # self.systemPlaintextEdit = QtWidgets.QPlainTextEdit()
        # self.systemPlaintextEdit.setReadOnly(True)
        # self.proccesPlaintextEdit = QtWidgets.QPlainTextEdit()
        # self.proccesPlaintextEdit.setReadOnly(True)
        # self.servisePlaintextedit = QtWidgets.QPlainTextEdit()
        # self.servisePlaintextedit.setReadOnly(True)
        # self.tasksPlaintextEdit = QtWidgets.QPlainTextEdit()

        # self.tabWidget = QtWidgets.QTabWidget()
        # self.tabWidget.addTab(self.systemPlaintextEdit, 'Система')
        # self.tabWidget.addTab(self.proccesPlaintextEdit, 'Процессы')
        # self.tabWidget.addTab(self.servisePlaintextedit, 'Службы')
        # self.tabWidget.addTab(self.tasksPlaintextEdit, 'Задачи')
        #
        # self.spinBoxLabel = QtWidgets.QLabel("Чатсота обновления")
        # self.spinBox = QtWidgets.QSpinBox()
        # self.spinBox.setRange(1, 30)
        #
        # spinboxLayout = QtWidgets.QHBoxLayout()
        # spinboxLayout.addWidget(self.spinBoxLabel)
        # spinboxLayout.addWidget(self.spinBox)
        #
        # mainLayout = QtWidgets.QVBoxLayout()
        # mainLayout.addWidget(self.tabWidget)
        # mainLayout.addLayout(spinboxLayout)
        #
        self.setLayout(FirstTabLayout)
        # self.setMinimumSize(500, 400)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
