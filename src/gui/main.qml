import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 600
    height: 750
    title: "中国象棋"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        // Turn indicator
        Text {
            id: turnText
            text: gameBridge ? gameBridge.currentTurn : "加载中..."
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        // Game result
        Text {
            id: resultText
            visible: false
            font.pixelSize: 28
            font.bold: true
            color: "red"
            Layout.alignment: Qt.AlignHCenter
        }

        // Chess board
        ChessBoard {
            id: chessBoard
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        // New game button
        Button {
            text: "新游戏"
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                resultText.visible = false;
                if (gameBridge) {
                    gameBridge.newGame();
                }
            }
        }
    }

    // Game over handler
    Connections {
        target: gameBridge
        function onGameOver(message) {
            resultText.text = message;
            resultText.visible = true;
        }
    }
}
