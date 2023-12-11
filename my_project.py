from PySide6 import QtWidgets, QtCore
import time
import psutil
import platform


class SystemInfo(QtCore.QThread):
    """
    Получение системной информации

    """
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, timeout=1, parent=None):
        super().__init__(parent)
        self.timeout = timeout
        self.status = True

    def run(self) -> None:
        self.status = True

        while self.status:
            sys_info = [psutil.cpu_percent(), psutil.virtual_memory().percent]
            self.systemInfoReceived.emit(sys_info)
            time.sleep(self.timeout)


class SystemServices(QtCore.QThread):
    """
    Получение информации о службах
    """
    systemServicesReceived = QtCore.Signal(str)

    def __init__(self, timeout=1, parent=None):
        super().__init__(parent)
        self.timeout = timeout

    def run(self) -> None:
        while True:
            services = list(psutil.win_service_iter())
            data = ''
            for value in services:
                data += f'{value.pid()}, {value.name()}, {value.display_name()}, {value.status()}\n'

            self.systemServicesReceived.emit(data)
            time.sleep(self.timeout)


class SystemProces(QtCore.QThread):
    """
    Получение информации о процессах
    """
    SystemProcReceived = QtCore.Signal(str)

    def __init__(self, timeout=1, parent=None):
        super().__init__(parent)
        self.timeout = timeout

    def run(self) -> None:
        while True:
            procs = list(psutil.process_iter())
            data = ''
            for value in procs:
                if psutil.pid_exists(value.ppid()):
                    data += f'{value.ppid()}, {value.name()}, {value.status()}\n'
            self.SystemProcReceived.emit(data)
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
        self.setMinimumSize(500, 600)

        lableProcessorName = QtWidgets.QLabel("Процессор")
        lableProcessorName.setMinimumWidth(120)
        self.ProcNameLineEdit = QtWidgets.QLineEdit()
        self.ProcNameLineEdit.setText(platform.uname().processor)
        self.ProcNameLineEdit.setReadOnly(True)
        layoutProcessor = QtWidgets.QHBoxLayout()
        layoutProcessor.addWidget(lableProcessorName)
        layoutProcessor.addWidget(self.ProcNameLineEdit)

        lableCores = QtWidgets.QLabel("Количество ядер")
        lableCores.setMinimumWidth(120)
        self.CoresLineEdit = QtWidgets.QLineEdit()
        self.CoresLineEdit.setText(str(psutil.cpu_count(logical=True)))
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
        self.RAMtotalLineEdit.setText(f'{psutil.virtual_memory().total / 1024} Kb')
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
        self.DiskLineEdit.setText(str(len(psutil.disk_partitions())))
        layoutD = QtWidgets.QHBoxLayout()
        layoutD.addWidget(lableDisk)
        layoutD.addWidget(self.DiskLineEdit)
        self.DiskInfoPlaintext = QtWidgets.QPlainTextEdit()
        self.DiskInfoPlaintext.setPlainText(self.setDiskInfo())
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

        self.ComboBox.currentTextChanged.connect(self.setTimeoutForSysInfo)
        self.systemInfo.systemInfoReceived.connect(self.setProcInfo)
        self.processInfoThread.SystemProcReceived.connect(self.updateProcessInfo)
        self.serviceInfoThread.systemServicesReceived.connect(self.updateServiseInfo)


    def setProcInfo(self, data):
        """
        Получение информации о текущей загруженности процессора и оперативной памяти
        """

        self.ProcessorLoadLineEdit.setText(str(data[0]))
        self.ProcessorLoadPB.setValue(data[0])
        self.RAMcurrentLineEdit.setText(str(data[1]))
        self.RAMload.setValue(data[1])

    def initThreads(self) -> None:
        """
        Инициализация потоков
        """
        self.systemInfo = SystemInfo()
        self.systemInfo.start()
        self.processInfoThread = SystemProces()
        self.processInfoThread.start()
        self.serviceInfoThread = SystemServices()
        self.serviceInfoThread.start()

    def setTimeoutForSysInfo(self, value):
        """
        Установка частоты обновления информации в потоке
        """

        self.systemInfo.timeout = int(value)
        self.serviceInfoThread.timeout = int(value)
        self.processInfoThread.timeout = int(value)

    def updateServiseInfo(self, data):
        """
        Вывод информации о службах
        """
        self.servisePlaintextedit.setPlainText(data)

    def updateProcessInfo(self, data):
        """
        Вывод информации о процессах
        """
        self.proccesPlaintextEdit.setPlainText(data)

    def setDiskInfo(self) -> str:
        """
        Вывод информации о дисках
        """

        data = ''
        for disc in psutil.disk_partitions():
            usage = psutil.disk_usage(disc.mountpoint)
            data += f'{disc.device}, {disc.fstype}\n' \
                    f'Общий объём памяти: {usage.total / 1024} Kb\n' \
                    f'Используется: {usage.used / 1024} Kb\n' \
                    f'Свободно: {usage.free / 1024} Kb\n' \
                    f'{usage.percent}\n'
        return data


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
