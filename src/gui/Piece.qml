import QtQuick 2.15

Item {
    id: root
    property int row: 0
    property int col: 0
    property string pieceColor: "red"
    property string displayName: ""

    x: col * parent.cellWidth
    y: row * parent.cellHeight
    width: parent.cellWidth
    height: parent.cellHeight

    // Piece circle
    Rectangle {
        anchors.centerIn: parent
        width: parent.width * 0.8
        height: parent.height * 0.8
        radius: width / 2
        color: pieceColor === "red" ? "#FF4444" : "#444444"
        border.color: "#222222"
        border.width: 2

        // Inner highlight
        Rectangle {
            anchors.centerIn: parent
            width: parent.width * 0.7
            height: parent.height * 0.7
            radius: width / 2
            color: pieceColor === "red" ? "#FF6666" : "#666666"
        }
    }

    // Piece text
    Text {
        anchors.centerIn: parent
        text: displayName
        font.pixelSize: parent.height * 0.5
        font.bold: true
        color: pieceColor === "red" ? "#FFFF00" : "#FFFFFF"
    }
}
