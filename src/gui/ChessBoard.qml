import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    property real cellWidth: width / 9
    property real cellHeight: height / 10

    // Background
    Rectangle {
        anchors.fill: parent
        color: "#DEB887"  // Wood color
    }

    // Grid lines
    Canvas {
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d");
            ctx.strokeStyle = "#8B4513";
            ctx.lineWidth = 2;

            // Horizontal lines
            for (var row = 0; row < 10; row++) {
                var y = row * cellHeight + cellHeight / 2;
                ctx.beginPath();
                ctx.moveTo(cellWidth / 2, y);
                ctx.lineTo(width - cellWidth / 2, y);
                ctx.stroke();
            }

            // Vertical lines (with gap for river)
            for (var col = 0; col < 9; col++) {
                var x = col * cellWidth + cellWidth / 2;
                // Top section
                ctx.beginPath();
                ctx.moveTo(x, cellHeight / 2);
                ctx.lineTo(x, 4.5 * cellHeight);
                ctx.stroke();
                // Bottom section
                ctx.beginPath();
                ctx.moveTo(x, 5.5 * cellHeight);
                ctx.lineTo(x, height - cellHeight / 2);
                ctx.stroke();
            }

            // Palace diagonals - Red side
            ctx.beginPath();
            ctx.moveTo(3 * cellWidth + cellWidth / 2, cellHeight / 2);
            ctx.lineTo(5 * cellWidth + cellWidth / 2, 2.5 * cellHeight);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(5 * cellWidth + cellWidth / 2, cellHeight / 2);
            ctx.lineTo(3 * cellWidth + cellWidth / 2, 2.5 * cellHeight);
            ctx.stroke();

            // Palace diagonals - Black side
            ctx.beginPath();
            ctx.moveTo(3 * cellWidth + cellWidth / 2, 7.5 * cellHeight);
            ctx.lineTo(5 * cellWidth + cellWidth / 2, height - cellHeight / 2);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(5 * cellWidth + cellWidth / 2, 7.5 * cellHeight);
            ctx.lineTo(3 * cellWidth + cellWidth / 2, height - cellHeight / 2);
            ctx.stroke();
        }
    }

    // River text
    Text {
        x: cellWidth
        y: 4.5 * cellHeight
        text: "楚河"
        font.pixelSize: cellHeight * 0.6
        color: "#8B4513"
    }

    Text {
        x: 6 * cellWidth
        y: 4.5 * cellHeight
        text: "汉界"
        font.pixelSize: cellHeight * 0.6
        color: "#8B4513"
    }

    // Pieces
    Repeater {
        model: gameBridge ? gameBridge.boardData : []
        Piece {
            row: modelData.row
            col: modelData.col
            pieceColor: modelData.color
            displayName: modelData.displayName
        }
    }

    // Selection highlight - matches Piece.qml positioning
    Rectangle {
        visible: gameBridge && gameBridge.selectedRow >= 0
        x: gameBridge.selectedCol >= 0 ? gameBridge.selectedCol * cellWidth : 0
        y: gameBridge.selectedRow >= 0 ? gameBridge.selectedRow * cellHeight : 0
        width: cellWidth
        height: cellHeight
        color: "transparent"
        border.color: "yellow"
        border.width: 4

        // Inner circle highlight matching piece size
        Rectangle {
            anchors.centerIn: parent
            width: parent.width * 0.8
            height: parent.height * 0.8
            radius: width / 2
            color: "transparent"
            border.color: "yellow"
            border.width: 3
        }
    }

    // Legal move markers
    Repeater {
        model: gameBridge ? gameBridge.legalMoves : []
        Rectangle {
            x: modelData.col * cellWidth + cellWidth / 2 - width / 2
            y: modelData.row * cellHeight + cellHeight / 2 - height / 2
            width: cellWidth / 3
            height: cellHeight / 3
            radius: width / 2
            color: "#8000FF00"  // Semi-transparent green
        }
    }

    // Mouse area for clicks
    MouseArea {
        anchors.fill: parent
        onClicked: {
            var col = Math.floor(mouse.x / cellWidth);
            var row = Math.floor(mouse.y / cellHeight);
            if (gameBridge) {
                gameBridge.onCellClicked(row, col);
            }
        }
    }
}
