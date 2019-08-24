# -*- coding: utf-8 -*-
# @Author  : 杨雪源

from PySide2.QtWidgets import *
import hou

# 在这里添加预设**********
user_pref = [(1920, 1080),
             (1280, 720),
             (960, 540),
             (960, 1200),
             (2880, 1200)
             ]
# ************************

class tool(QDialog):
    def __init__(self,allCam):
        super(tool, self).__init__()
        self.allCam = allCam
        self.setWindowTitle("Set Camera Resolution")
        label1 = QLabel("Input the camera resolution")
        label2 = QLabel("Resolution")
        self.resx = QLineEdit('1920')
        self.resy = QLineEdit('1080')
        self.rescb = QComboBox()

        if user_pref:
            for pref in user_pref:
                self.rescb.addItem("%dX%d" % pref)

        self.cbs = []
        for cam in self.allCam:
            cam_info = cam.name() + '\n ' + cam.path()
            self.cbs.append(QCheckBox(cam_info))

        btn = QPushButton('OK', self)
        self.select_all = QCheckBox("Select all")
        self.select_all.toggle()

        resbox = QHBoxLayout()
        resbox.addWidget(label2)
        resbox.addWidget(self.resx)
        resbox.addWidget(self.resy)
        resbox.addWidget(self.rescb)

        okbox = QHBoxLayout()
        okbox.addWidget(self.select_all)
        okbox.addStretch(1)
        okbox.addWidget(btn)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label1)
        vbox.addLayout(resbox)
        vbox.addWidget(QLabel("\nSet the following camera:"))

        cam_list = QWidget()
        cam_list.setMinimumHeight(50)

        vbox1 = QVBoxLayout()
        for cb in self.cbs:
            cb.toggle()
            vbox1.addWidget(cb)
        vbox1.setMargin(10)
        vbox1.setSpacing(10)
        cam_list.setLayout(vbox1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(False)
        scroll.setWidget(cam_list)
        scroll.setAutoFillBackground(True)
        scroll.setStyleSheet(hou.qt.styleSheet())
        scroll.setProperty('houdiniStyle', True)

        vbox.addWidget(scroll)
        vbox.addStretch(1)
        vbox.addLayout(okbox)
        vbox.setMargin(30)

        self.setLayout(vbox)

        self.rescb.currentIndexChanged.connect(self.setResxy)
        self.select_all.stateChanged.connect(self.selectAll)
        btn.clicked.connect(self.doInHou)
        btn.clicked.connect(self.close)

    def setResxy(self):
        slcRes = self.rescb.currentText()
        Resxy = slcRes.split('X')
        self.resx.setText(Resxy[0])
        self.resy.setText(Resxy[1])

    def selectAll(self):
        for cb in self.cbs:
            if self.select_all.isChecked():
                cb.setChecked(True)
            else:
                cb.setChecked(False)

    def doInHou(self):
        for cb in self.cbs:
            if not cb.isChecked():
                camPath = cb.text().split(' ')[1]
                self.allCam.remove(hou.node(camPath))

        for cam in self.allCam:
            x = int(self.resx.text())
            y = int(self.resy.text())
            cam.parm("resx").set(x)
            cam.parm("resy").set(y)


def listNode(node, result=None):
    if result is None:
        result = []

    children = node.children()
    if children:
        for child in children:
            if child.isEditable:
                result.append(child)
                listNode(child, result)
    return result


def set_resolution():
    allNodes = listNode(hou.node('/obj'))
    if allNodes:
        allCam = []
        for node in allNodes:
            if node.type().name() == 'cam':
                allCam.append(node)

        if allCam:
            hou.session.ins = tool(allCam)
            hou.session.ins.setStyleSheet(hou.qt.styleSheet())
            hou.session.ins.setProperty('houdiniStyle', True)
            hou.session.ins.show()
