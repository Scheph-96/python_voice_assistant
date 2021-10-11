import QtQuick 2.14
import QtQuick.Window 2.14
import QtQuick.Layouts 1.0
import QtQuick.Controls 2.15

Window {
    width: 800
    height: 600
    visible: true
    color: "#0a0a0c"
    title: qsTr("Voice Assistant")

    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint

    ColumnLayout {
        x: 15
        y: 21
        spacing: 60

        Image {
            id: image
            source: "../img/girl.png"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.preferredHeight: 147
            Layout.preferredWidth: 147
            fillMode: Image.PreserveAspectFit
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            spacing: 80

            Rectangle {
                id: rectangle
                color: "#e8e8e8"
                Layout.preferredHeight: 60
                Layout.preferredWidth: 65
            }

            Rectangle {
                id: rectangle1
                color: "#00df00"
                Layout.preferredHeight: 60
                Layout.preferredWidth: 65
            }

            Rectangle {
                id: rectangle2
                color: "#e8e8e8"
                Layout.preferredHeight: 60
                Layout.preferredWidth: 65
            }

            Rectangle {
                id: rectangle3
                color: "#00df00"
                Layout.preferredHeight: 60
                Layout.preferredWidth: 65
            }
        }

        Rectangle {
            id: rectangle4
            color: "#00000000"
            border.color: "#00df00"
            border.width: 5
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.preferredHeight: 232
            Layout.preferredWidth: 770

            ScrollView {
                id: scrollView
                x: 13
                y: 12
                width: 200
                height: 200
                anchors.fill: parent
                anchors.bottomMargin: 11
                anchors.rightMargin: 8
                anchors.topMargin: 11
                anchors.leftMargin: 8

                Column {
                    id: column
                    x: 5
                    y: 1
                    width: parent.width
                    height: 209
                    spacing: 10

                    Text {
                        id: text1
                        color: "#ffffff"
                        text: qsTr("Lorem ipsum dolor sit amet")
                        font.pixelSize: 20
                    }

                    Text {
                        id: text2
                        color: "#ffffff"
                        text: qsTr("Lorem ipsum dolor sit amet")
                        font.pixelSize: 20
                    }

                    Text {
                        id: text3
                        color: "#ffffff"
                        text: qsTr("Lorem ipsum dolor sit amet")
                        font.pixelSize: 20
                    }
                }
            }
        }
    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
