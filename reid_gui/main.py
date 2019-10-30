# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2019/10/24
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout, \
    QListWidgetItem, QLabel,QMainWindow,QMenu,qApp,QAction

# Created on 2018年5月29日
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: LeftTabWidget
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0
class MainWindow(QMainWindow):
    '''
    方式二: 通过继承类方式创建主窗口
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建动作
        jumpAct = QAction(QIcon('icon.png'), '&Jump to Source', self)  # 图标 / exit标签
        jumpAct.setShortcut('F4')  # 快捷键
        jumpAct.setStatusTip('这是 Jump to Source 的提示信息')  # 状态栏提示信息
        jumpAct.triggered.connect(qApp.quit)  # 触发 quit 事件

        strucAct = QAction(QIcon('icon.png'), '&Structure', self)
        strucAct.setShortcut("Alt+7")

        # 创建子菜单
        impMenu = QMenu('Tool Windows', self)
        impMenu.addAction(strucAct)  # 往子菜单添加一个动作

        # 创建菜单栏
        menubar = self.menuBar()

        # 创建菜单
        viewMenu = menubar.addMenu('&View')  # 添加View菜单
        viewMenu.addMenu(impMenu)  # 添加子菜单
        viewMenu.addSeparator()  # 添加分隔线
        viewMenu.addAction(jumpAct)  # 添加 动作

        self.setGeometry(300, 300, 550, 350)
        self.setWindowTitle('菜单栏')
        self.show()

    def contextMenuEvent(self, event):
        '''
        右键上下文菜单
        '''
        # 创建子菜单, 并添加动作
        cmenu = QMenu(self)
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")

        action = cmenu.exec_(self.mapToGlobal(event.pos()))  # mapToGlobal 将组件相对坐标转为窗口绝对坐标, exec_ 显示菜单

        # 如果触发的动作为 quitAct 则退出应用
        if action == quitAct:
            qApp.quit()


class LeftTabWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(LeftTabWidget, self).__init__(*args, **kwargs)
        self.resize(1024, 768)
        # 左右布局(左边一个QListWidget + 右边QStackedWidget)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        self.listWidget.setIconSize(QSize(32, 32))
        layout.addWidget(self.listWidget)
        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)
        self.initUi()

    def initUi(self):
        # 初始化界面
        font = QFont("雅黑")
        pointsize = font.pointSize()
        font.setPixelSize(pointsize * 95 / 72)
        app.setFont(font)
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 这里就用一般的文本配合图标模式了(也可以直接用Icon模式,setViewMode)
        menu = ["首页", "模块设置", "在线识别", "离线检索", "信息查看", "退出系统"]
        for i, title in enumerate(menu):
            item = QListWidgetItem(QIcon('Data/%d.ico'%i), title, self.listWidget)
            # 设置item的默认宽高(这里只有高度比较有用)
            item.setSizeHint(QSize(16777215, 50))
            # 文字居中
            item.setTextAlignment(Qt.AlignCenter)

        # 再模拟20个右侧的页面(就不和上面一起循环放了)
        for i in range(20):
            w=QWidget()
            label2 = QLabel('我是buy页面 %d' % i, w)
            label2.setAlignment(Qt.AlignCenter)
            # 设置label的背景颜色(这里随机)
            # 这里加了一个margin边距(方便区分QStackedWidget和QLabel的颜色)
            label2.setStyleSheet('background: rgb(%d, %d, %d);margin: 50px;' % (
                randint(0, 120), randint(0, 255), randint(0, 255)))
            self.stackedWidget.addWidget(w)

# 美化样式表
Stylesheet = """
/*去掉item虚线边框*/
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
/*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
QListWidget {
    min-width: 120px;
    max-width: 120px;
    color: white;
    background: #669999;
}
/*被选中时的背景颜色和左边框颜色*/
QListWidget::item:selected {
    background: #6699CC;
    border-left: 2px solid rgb(9, 187, 7);
}
/*鼠标悬停颜色*/
HistoryPanel::item:hover {
    background: #663366;
}

/*右侧的层叠窗口的背景颜色*/
QStackedWidget {
    background: #6699CC;
}
/*模拟的页面*/
QLabel {
    color: white;
}
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    w = LeftTabWidget()
    w.show()
    sys.exit(app.exec_())
