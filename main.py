#!/usr/bin/env python3
import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickView

from src.gui.bridge import GameBridge


def main():
    app = QApplication(sys.argv)

    # 创建桥接对象
    bridge = GameBridge()

    # 创建视图
    view = QQuickView()
    view.rootContext().setContextProperty("gameBridge", bridge)

    # 加载QML
    qml_path = os.path.join(os.path.dirname(__file__), "src", "gui", "main.qml")
    view.setSource(QUrl.fromLocalFile(qml_path))

    if view.status() == QQuickView.Error:
        print("加载QML失败")
        sys.exit(1)

    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
