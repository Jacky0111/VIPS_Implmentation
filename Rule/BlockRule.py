# 4.1 Visual Block Extraction
# Heuristic rules in block extraction phase

class BlockRule:
    THRESHOLD = 40000

    @staticmethod
    def initialization(given_node_list):
        node_list = given_node_list

    @staticmethod
    def dividable(given_block):
        box = given_block.boxes[0]

        if box.nodeType == 3:
            return False
        else:
            if box.nodeName == 'img':
                return False
            else:
                if not BlockRule.isInlineNode(box.nodeName):
                    return BlockRule.inlineRules(given_block)
                elif box.nodeName == 'table':
                    return BlockRule.tableRules(given_block)
                elif box.nodeName == 'tr':
                    return BlockRule.trRules(given_block)
                elif box.nodeName == 'td':
                    return BlockRule.tdRules(given_block)
                elif box.nodeName == 'p':
                    return BlockRule.pRules(given_block)
                else:
                    return BlockRule.otherRules(given_block)

    '''
    Different rules for Inline Text Node
    '''
    @staticmethod
    def inlineRules(given_block):
        if BlockRule.rule1(given_block):
            return True
        if BlockRule.rule2(given_block):
            return True
        if BlockRule.rule3(given_block):
            return True
        if BlockRule.rule4(given_block):
            return True
        if BlockRule.rule5(given_block):
            return True
        if BlockRule.rule6(given_block):
            return True
        if BlockRule.rule7(given_block):
            return True
        if BlockRule.rule9(given_block):
            return True
        if BlockRule.rule10(given_block):
            return True
        if BlockRule.rule12():
            return True
        return False

    '''
    Different rules for <TABLE>
    '''
    @staticmethod
    def tableRules(given_block):
        if BlockRule.rule1(given_block):
            return True
        if BlockRule.rule2(given_block):
            return True
        if BlockRule.rule3(given_block):
            return True
        if BlockRule.rule8(given_block):
            return True
        if BlockRule.rule10(given_block):
            return True
        if BlockRule.rule13(given_block):
            return True
        return False

    '''
    Different rules for <TR> node
    '''
    @staticmethod
    def trRules(given_block):
        if BlockRule.rule1(given_block):
            return True
        if BlockRule.rule2(given_block):
            return True
        if BlockRule.rule3(given_block):
            return True
        if BlockRule.rule7(given_block):
            return True
        if BlockRule.rule8(given_block):
            return True
        if BlockRule.rule10(given_block):
            return True
        if BlockRule.rule13(given_block):
            return True
        return False

    '''
    Different rules for <TD> node
    '''
    @staticmethod
    def tdRules(given_block):
        if BlockRule.rule1(given_block):
            return True
        if BlockRule.rule2(given_block):
            return True
        if BlockRule.rule3(given_block):
            return True
        if BlockRule.rule4(given_block):
            return True
        if BlockRule.rule9(given_block):
            return True
        if BlockRule.rule10(given_block):
            return True
        if BlockRule.rule11(given_block):
            return True
        if BlockRule.rule13(given_block):
            return True
        return False

    '''
    Different rules for <P> node
    '''
    @staticmethod
    def pRules(given_block):
        if BlockRule.rule1(given_block):
            return True
        if BlockRule.rule2(given_block):
            return True
        if BlockRule.rule3(given_block):
            return True
        if BlockRule.rule4(given_block):
            return True
        if BlockRule.rule5(given_block):
            return True
        if BlockRule.rule6(given_block):
            return True
        if BlockRule.rule7(given_block):
            return True
        if BlockRule.rule9(given_block):
            return True
        if BlockRule.rule10(given_block):
            return True
        if BlockRule.rule12():
            return True
        return False

    '''
    Different rules for other tags
    '''
    @staticmethod
    def otherRules(given_block):
        if BlockRule.rule1(given_block):
            return True
        if BlockRule.rule2(given_block):
            return True
        if BlockRule.rule3(given_block):
            return True
        if BlockRule.rule4(given_block):
            return True
        if BlockRule.rule6(given_block):
            return True
        if BlockRule.rule7(given_block):
            return True
        if BlockRule.rule9(given_block):
            return True
        if BlockRule.rule10(given_block):
            return True
        if BlockRule.rule12():
            return True
        return False

    '''
    Rule 1: If the DOM node is not a text node and it has no valid children, then this node cannot be
             divided and will be cut.
    '''
    @staticmethod
    def rule1(given_block):
        node = given_block.boxes[0]

        # Return False if DOM node is text node and has valid children, True otherwise
        if BlockRule.isTextNode(node) and BlockRule.hasValidChildren(node):
            print('Violated Rule 1')
            return False
        return True

    @staticmethod
    def hasValidChildren(node):
        subBoxList = node.childNodes

        for box in subBoxList:
            if BlockRule.isValidNode(box):
                return True
        return False

    '''
    Rule 2: If the DOM node has only one valid child and the child is not a text node, then divide this node.
    '''
    @staticmethod
    def rule2(given_block):
        # Check if contains only 1 child
        if len(given_block.children) == 1:
            node = given_block.children[0].boxes[0]
            # Return True if child node is valid and is not text node, False otherwise
            if BlockRule.isValidNode(node) and not BlockRule.isTextNode(node):
                return True
        print('Violated Rule 2')
        return False

    '''
    Rule 3: If the DOM node is the root node of the sub-DOM tree (corresponding to the block),
            and there is only one sub DOM tree corresponding to this block, divide this node.
    '''
    @staticmethod
    def rule3(given_block):
        node = given_block.boxes[0]
        count = 0

        # Return False if DOM node is root node

        # Return True if only 1 sub-tree corresponded, False otherwise
        for block in given_block.children:
            if block.boxes[0].nodeName == node.nodeName:
                result = True
                BlockRule.isOnlyOneDomSubTree(node, block.boxes[0], result)
                if result:
                    count += 1
        return True if count == 1 else False

    @staticmethod
    def isOnlyOneDomSubTree(pattern, node, result):
        if pattern.nodeName != node.nodeName:
            return False
        elif len(pattern.childNodes) != len(node.pattern.childNodes):
            return False
        elif not result:
            return
        else:
            for i in range(len(pattern.childNodes)):
                BlockRule.isOnlyOneDomSubTree(pattern.childNodes[i], node.childNodes[i], result)

    '''
     Rule 4: If all of the child nodes of the DOM node are text nodes or virtual text nodes, do not divide the node.
             * If the font size and font weight of all these child nodes are same, set the DoC of the extracted block
               to 10.
             * Otherwise, set the DoC of this extracted block to 9.
    '''
    @staticmethod
    def rule4(given_block):
        node = given_block.boxes[0]
        subBoxList = node.childNodes
        count = 0

        for box in subBoxList:
            if BlockRule.isTextNode(box) or BlockRule.isVirtualTextNode(box):
                count += 1
        if count == len(subBoxList):
            fontSize = 0
            fontWeight = None
            for box in subBoxList:
                child_font_size = box.visual_cues['font-size']
                child_font_weight = box.visual_cues['font-weight']
                if (fontSize != 0 and fontSize != child_font_size) or (
                        fontWeight is not None and fontWeight != child_font_weight):
                    given_block.DoC(9)
                    print('Violated Rule 4')
                    return False
                else:
                    fontSize = child_font_size
                    fontWeight = child_font_weight
            given_block.DoC(10)
            print('Violated Rule 4')
            return False
        return True

    '''
    Rule 5: If one of the child nodes of the DOM node is line-break node, then divide this DOM node.
    '''
    @staticmethod
    def rule5(given_block):
        node = given_block.boxes[0]
        subBoxList = node.childNodes

        # Return True if line-break node exist, False otherwise
        for box in subBoxList:
            if not BlockRule.isInlineNode(box.nodeName):
                return True
        print('Violated Rule 5')
        return False

    '''
    Rule 6: If one of the child nodes of the DOM node has HTML tag <HR>, then divide this DOM node.
    '''
    @staticmethod
    def rule6(given_block):
        node = given_block.boxes[0]
        subBoxList = node.childNodes

        # Return True if 1 child node has <HR> tag, False otherwise
        for box in subBoxList:
            if box.nodeName == 'hr':
                return True
        print('Violated Rule 6')
        return False

    '''
    Rule 7: If the sum of all the child nodes' size is greater than this DOM node's size, then divide this node.
    '''
    @staticmethod
    def rule7(given_block):
        node = given_block.boxes[0]
        subBoxList = node.childNodes
        x = node.visual_cues['bounds']['x']
        y = node.visual_cues['bounds']['y']
        width = node.visual_cues['bounds']['width']
        height = node.visual_cues['bounds']['height']

        for box in subBoxList:
            if (box.visual_cues['bounds']['x'] > x or
                    box.visual_cues['bounds']['y'] > y or
                    box.visual_cues['bounds']['x'] + box.visual_cues['bounds']['width'] > (x + width) or
                    box.visual_cues['bounds']['y'] + box.visual_cues['bounds']['height'] > (y + height)):
                return True
        print('Violated Rule 7')
        return False

    '''
    Rule 8: If the background color of this node is different from one of its children's, divide this node and at the
            same time, the child node with different background color will not be divided in this round.
            * Set the DoC value (6-8) for the child node based on the html tag of the child node and the size of
              the child node.
    '''
    @staticmethod
    def rule8(given_block):
        node = given_block.boxes[0]
        bgColor = node.visual_cues['background-color']

        for block in given_block.children:
            child = block.boxes[0]
            child_bg_color = child.visual_cues['background-color']
            if bgColor != child_bg_color:
                block.isDividable = False
                block.DoC = BlockRule.getDoCByTagAndSize('', 0)
                return True
        print('Violated Rule 8')
        return False

    # TO BE IMPROVED
    @staticmethod
    def getDoCByTagAndSize(tag, size):
        return 7

    '''
    Rule 9: If the node has at least one text node child or at least one virtual text node child, and the node's
            relative size is smaller than a threshold, then the node cannot be divided.
            * Set the DoC value (from 5-8) based on the html tag of the node.
    '''
    @staticmethod
    def rule9(given_block):
        node = given_block.boxes[0]
        subBoxList = node.childNodes
        count = 0

        for box in subBoxList:
            if BlockRule.isTextNode(box) or BlockRule.isVirtualTextNode(box):
                count += 1
        if count >= 1 and node.visual_cues['bounds']['x'] * node.visual_cues['bounds']['y'] < BlockRule.THRESHOLD:
            given_block.DoC = BlockRule.getDoCByTagAndSize('', 0)
            return False
        return True

    '''
    Rule 10: If the child of the node with maximum size are smaller than a threshold (relative size), do not divide
             this node.
             * Set the DoC based on the html tag and size of this node.
    '''
    @staticmethod
    def rule10(given_block):
        maximum = 0
        node = given_block.boxes[0]
        subBoxList = node.childNodes

        for box in subBoxList:
            child_size = box.visual_cues['bounds']['x'] * box.visual_cues['bounds']['y']
            maximum = child_size if maximum < child_size else maximum
        if maximum < BlockRule.THRESHOLD:
            given_block.DoC = BlockRule.getDoCByTagAndSize('', 0)
            return False
        return True

    '''
    Rule 11: If previous sibling node has not been divided, do not divide this node.
    '''
    @staticmethod
    def rule11(given_block):
        children = given_block.parent.children
        index = children.index(given_block)
        count = 0

        for i in range(index):
            if not children[i].isDividable:
                count += 1
        return False if count == index else True

    '''
    Rule 12: Divide this node.
    '''
    @staticmethod
    def rule12():
        return True

    '''
    Rule 13: Do not divide this node.
             * Set the DoC value based on the html tag and size of this node.
    '''
    @staticmethod
    def rule13(given_block):
        given_block.DoC = BlockRule.getDoCByTagAndSize('', 0)
        return False

    '''
    Here are the inline elements in HTML:
    Reference: https://www.w3schools.com/html/html_blocks.asp#:~:text=An%20inline%20element%20does%20not%20start%20on%20a%20new%20line,span%3E%20element%20inside%20a%20paragraph.
    '''
    @staticmethod
    def isInlineNode(element):
        if (element == 'a' or
                element == 'abbr' or
                element == 'acronym' or
                element == 'b' or
                element == 'bdo' or
                element == 'big' or
                element == 'br' or
                element == 'button' or
                element == 'cite' or
                element == 'code' or
                element == 'dfn' or
                element == 'em' or
                element == 'i' or
                element == 'img' or
                element == 'input' or
                element == 'kbd' or
                element == 'label' or
                element == 'map' or
                element == 'object' or
                element == 'q' or
                element == 'samp' or
                element == 'script' or
                element == 'select' or
                element == 'small' or
                element == 'span' or
                element == 'strong' or
                element == 'sub' or
                element == 'sup' or
                element == 'textarea' or
                element == 'time' or
                element == 'tt' or
                element == 'var'):
            return False
        else:
            return True

    '''
    Valid node: a node that can be seen through the browser. The node’s width and height are not equal to zero.
    '''
    @staticmethod
    def isValidNode(node):
        display = node.visual_cues['display']
        visibility = node.visual_cues['visibility']
        height = node.visual_cues['bounds']['height']
        width = node.visual_cues['bounds']['width']

        if display == 'none' or visibility == 'hidden' or height == '0px' or width == '0px':
            return False
        return True

    '''
    Text node: the DOM node corresponding to free text, which does not have html tag
    '''
    @staticmethod
    def isTextNode(node):
        return node.nodeType == 3

    '''
    Virtual text node (recursive definition):
    * Inline node with only text node children is a virtual text node.
    * Inline node with only text node and virtual text node children is a virtual text node.
    '''
    @staticmethod
    def isVirtualTextNode(node):
        subBoxList = node.childNodes
        count = 0
        for box in subBoxList:
            if BlockRule.isTextNode(box) or BlockRule.isVirtualTextNode(box):
                count += 1
        if count == len(subBoxList):
            return True
        return False
