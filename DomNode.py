class DomNode:
    __slots__ = ('attributes', 'childNodes', 'nodeName', 'nodeType', 'nodeValue', 'parentNode', 'tagName',
                 'visual_cues')

    def __init__(self, nodeName, nodeType, nodeValue, parentNode, tagName):
        self.attributes = dict()
        self.childNodes = []
        self.nodeName = nodeName
        self.nodeType = nodeType
        self.nodeValue = nodeValue
        self.parentNode = parentNode
        self.tagName = tagName
        self.visual_cues = dict()

    def createElement(self, tagName):
        self.nodeName = tagName

    def createTextNode(self, nodeValue, parentNode):
        self.nodeName = '#text'
        self.nodeValue = nodeValue
        self.parentNode = parentNode

    def createComment(self):
        self.nodeName = "#comment"

    def setAttributes(self, attributes):
        self.attributes = attributes

    def setVisualCues(self, visual_cues):
        self.visual_cues = visual_cues

    def appendChild(self, childNode):
        self.childNodes.append(childNode)
