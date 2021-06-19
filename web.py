import json
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from DomNode import DomNode


class UiMainWindow(object):
    nodeList = []
    web_view = None
    central_widget = None
    grid_layout = None
    status_bar = None

    def convertToDomTree(self, obj, parentNode=None):
        if isinstance(obj, str):
            json_obj = json.loads(obj)  # Use json lib to load our json string
        else:
            json_obj = obj
        node_type = json_obj['nodeType']
        node = DomNode(node_type)
        # Element Node
        if node_type == 1:
            node.createElement(json_obj['tagName'])
            attributes = json_obj['attributes']
            if attributes is not None:
                node.setAttributes(attributes)
            visual_cues = json_obj['visual_cues']
            if visual_cues is not None:
                node.setVisualCues(visual_cues)
        elif node_type == 3:
            node.createTextNode(json_obj['nodeValue'], parentNode)
            if node.parentNode is not None:
                visual_cues = node.parentNode.visual_cues
                if visual_cues is not None:
                    node.setVisualCues(visual_cues)
        else:
            return node

        self.node_list.append(node)
        if node_type == 1:
            child_nodes = json_obj['childNodes']
            for i in range(len(child_nodes)):
                if child_nodes[i]['nodeType'] == 1:
                    node.appendChild(self.convertToDomTree(child_nodes[i], node))
                if child_nodes[i]['nodeType'] == 3:
                    try:
                        if not child_nodes[i]['nodeValue'].isspace():
                            node.appendChild(self.convertToDomTree(child_nodes[i], node))
                    except KeyError:
                        print('Abnormal text node')

        return node

    def getDomTree(self):
        for node in self.nodeList:
            if node.nodeType == 1:
                print(node.tagName, ", ", node.nodeType)
            else:
                print(node.nodeValue, ", ", node.nodeType)

    def someCallback(self, x):
        print("Callback")
        # This callback simply calls convertToDomTree method with x as return value
        self.convertToDomTree(x)

    def runSomeJavaScript(self):
        # Read in our DOM java script file as string
        file = open('DOM.js', 'r')
        java_script = file.read()

        # Add additional javascript code to run our DOM js toJSON method
        java_script += '\nreturn JSON.stringify(toJSON(document.getElementsByTagName("BODY")[0]));'

        # Finally run the javascript, and wait for it to finish and call the someCallback function.
        self.web_view.page().runJavaScript(java_script, self.someCallback)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralwidget")

        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("gridLayout")

        self.web_view = QtWebEngineWidgets.QWebEngineView(self.central_widget)
        self.web_view.setUrl(QtCore.QUrl('https://www.thestar.com.my/'))
        self.web_view.setObjectName("webView")
        self.web_view.loadFinished.connect(self.runSomeJavaScript)
        self.grid_layout.addWidget(self.web_view, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.central_widget)

        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
