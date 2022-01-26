class DomNode:
    __slots__ = ('attributes', 'childNodes', 'nodeName', 'nodeType', 'nodeValue', 'parentNode', 'tagName',
                 'visual_cues')

    def __init__(self, nodeType):
        self.attributes = dict()
        self.childNodes = []
        self.nodeType = nodeType
        self.visual_cues = dict()

    '''
    Specify the node that contains HTML tag. For element nodes, the returned value is the tagName
    @param tagName 
    '''
    def createElement(self, tagName):
        self.nodeName = tagName

    '''
    Specify the node that contains only text without any HTML tag. For text nodes, the returned value is "#text"
    @param nodeValue 
    @param parentNode
    '''
    def createTextNode(self, nodeValue, parentNode):
        self.nodeName = '#text'
        self.nodeValue = nodeValue
        self.parentNode = parentNode

    '''
    Set the attributes to Dom node
    @param attributes 
    '''
    def setAttributes(self, attributes):
        self.attributes = attributes

    '''
    Set Set the visual information of web page to Dom Node.
    @param visual_cues 
    '''
    def setVisualCues(self, visual_cues):
        self.visual_cues = visual_cues

    '''
    Append the child nodes to its parent node
    @param childNode
    '''
    def appendChild(self, childNode):
        self.childNodes.append(childNode)

    def __str__(self):
        return f'Node Type: {self.nodeType} \
            \nNode Name: {self.nodeName} \
            \nAttributes: {self.attributes} \
            \nVisual Cues: {self.visual_cues} \
            \nChild Nodes: {self.childNodes}'
