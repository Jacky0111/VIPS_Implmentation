class DomNode:
    __slots__ = ('attributes', 'childNodes', 'nodeName', 'nodeType', 'nodeValue', 'parentNode', 'tagName',
                 'visual_cues')

    def __init__(self, nodeType):
        self.attributes = dict()
        self.childNodes = []
        self.nodeType = nodeType
        self.visual_cues = dict()

    # For element nodes, the returned value is the tagname.
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
