#!/usr/bin/env python3
import sys
import os

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine

from src.gui.bridge import GameBridge


def main():
    app = QGuiApplication(sys.argv)

    # 创建桥接对象
    bridge = GameBridge()

    # 创建QML引擎
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("gameBridge", bridge)

    # 加载QML
    qml_path = os.path.join(os.path.dirname(__file__), "src", "gui", "main.qml")
    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        print("加载QML失败")
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
