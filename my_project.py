from PySide6 import QtWidgets, QtCore
import time
import psutil
import platform


class SystemInfo(QtCore.QThread):
    """
    поток для получения системной информации

    """
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, timeout=1, parent=None):
        super().__init__(parent)
        self.timeout = timeout
        self.status = True

    def run(self) -> None:
        self.status = True

        while self.status:
            sys_info = []
            print(psutil.cpu_percent())
            sys_info.append(psutil.cpu_percent())  # загрузка процессора
            # print(psutil.virtual_memory().percent)
            sys_info.append(psutil.virtual_memory().percent)  # загрузка оперативной памяти

            self.systemInfoReceived.emit(sys_info)

            time.sleep(self.timeout)


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initThreads()
        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """
        self.setWindowTitle('Мониторинг системы')

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

        GBram = QtWidgets.QGroupBox("Оперативная память")
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

        GBdisk = QtWidgets.QGroupBox("Жесткий диск")
        GBdisk.setLayout(layoutDisk)

        FirstTabLayout = QtWidgets.QVBoxLayout()
        FirstTabLayout.addWidget(GBprocessor)
        FirstTabLayout.addWidget(GBram)
        FirstTabLayout.addWidget(GBdisk)

        frame = QtWidgets.QFrame()
        frame.setLayout(FirstTabLayout)

        # ----------------------------------------------------------------------------------------------------------------------

        self.proccesPlaintextEdit = QtWidgets.QPlainTextEdit()
        self.proccesPlaintextEdit.setReadOnly(True)
        self.servisePlaintextedit = QtWidgets.QPlainTextEdit()
        self.servisePlaintextedit.setReadOnly(True)
        self.tasksPlaintextEdit = QtWidgets.QPlainTextEdit()
        self.tasksPlaintextEdit.setReadOnly(True)

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(frame, 'Система')
        self.tabWidget.addTab(self.proccesPlaintextEdit, 'Процессы')
        self.tabWidget.addTab(self.servisePlaintextedit, 'Службы')
        self.tabWidget.addTab(self.tasksPlaintextEdit, 'Задачи')

        ComboBoxLabel = QtWidgets.QLabel("Чатсота обновления, сек.")
        self.ComboBox = QtWidgets.QComboBox()
        self.ComboBox.addItems(['1', '5', '10', '30'])

        comboboxLayout = QtWidgets.QHBoxLayout()
        comboboxLayout.addWidget(ComboBoxLabel)
        comboboxLayout.addWidget(self.ComboBox)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addLayout(comboboxLayout)

        self.setLayout(mainLayout)
        # self.setMinimumSize(500, 400)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        """

        self.ComboBox.currentTextChanged.connect(self.setTimeoutForSysInfo(int(self.ComboBox.currentText())))
        self.ProcNameLineEdit.setText(platform.uname().processor)
        self.CoresLineEdit.setText(str(psutil.cpu_count(logical=True)))
        self.systemInfo.systemInfoReceived.connect(self.setProcInfo)

    def setProcInfo(self, data):
        self.ProcessorLoadLineEdit.setText(str(data[0]))
        self.ProcessorLoadPB.setValue(data[0])




    def initThreads(self) -> None:
        """
        Инициализация потока

        :return:
        """
        self.systemInfo = SystemInfo()
        self.systemInfo.start()

    def setTimeoutForSysInfo(self, value):
        """
        Установка частоты обновления информации в потоке

        """

        self.systemInfo.timeout = value




if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
