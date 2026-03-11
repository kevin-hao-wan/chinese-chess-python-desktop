import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

Dialog {
    id: colorSelectionDialog
    title: "选择执棋方"
    modal: true
    standardButtons: Dialog.Ok | Dialog.Cancel

    signal colorSelected(int colorValue)
    property int selectedColor: 0  // 0 = 红, 1 = 黑

    ColumnLayout {
        spacing: 20
        Label {
            text: "请选择您要执的棋子："
            font.pixelSize: 16
        }
        RadioButton {
            id: redRadio
            text: "执红先行（先手）"
            checked: colorSelectionDialog.selectedColor === 0
            onClicked: colorSelectionDialog.selectedColor = 0
        }
        RadioButton {
            id: blackRadio
            text: "执黑后行（后手）"
            checked: colorSelectionDialog.selectedColor === 1
            onClicked: colorSelectionDialog.selectedColor = 1
        }
    }

    onAccepted: {
        colorSelected(selectedColor)
        appSettings.lastSelectedColor = selectedColor
    }

    Component.onCompleted: {
        selectedColor = appSettings.lastSelectedColor
    }
}
