# 4.2 Visual Separator Detection
# 4.2.2 Setting Weights for Separators

# from VariationOrder import SeparatorVO, BlockVO


class WeightRule:
    DISTANCE = 50
    nodeList = []

    @staticmethod
    def initialization(givenNodeList):
        nodeList = givenNodeList

    '''
    Rule 1: The greater the distance between blocks on different side of the separator, the higher the weight.
    '''
    @staticmethod
    def rule1(given_separator):
        side = given_separator.weight + given_separator.height
        if given_separator.typ == given_separator.TYPE_HORIZONTAL:
            given_separator.weight = side / WeightRule.DISTANCE
        elif given_separator.typ == given_separator.TYPE_VERTICAL:
            given_separator.weight = side / WeightRule.DISTANCE

    '''
    Rule 2: If a visual separator is overlapped with some certain HTML tags (e.g., the <HR> HTML tag), its weight is set to be higher.
    '''
    @staticmethod
    def rule2(given_separator, hr_list):
        for block in hr_list:
            box = block.boxes[0]
            separator_x = given_separator.width + given_separator.x
            separator_y = given_separator.height + given_separator.y
            hr_separator_x = box.visual_cues['bounds']['x'] + box.visual_cues['bounds']['width']
            hr_separator_y = box.visual_cues['bounds']['y'] + box.visual_cues['bounds']['height']
            if (given_separator.x <= box.visual_cues['bounds']['x'] and
                    given_separator.y <= box.visual_cues['bounds']['y'] and
                    separator_x > hr_separator_x and
                    separator_y > hr_separator_y):
                given_separator.weight += 1

    '''
    Rule 3: If background colors of the blocks on two sides of the separator are different, the weight will be increased.
    '''
    @staticmethod
    def rule3(given_separator):
        one_box = given_separator.one_side.boxes[0]
        another_box = given_separator.another_side.boxes[0]
        if one_box.nodeType == 1 and another_box.nodeType == 1:
            one_color = one_box.visual_cues['background-color']
            another_color = another_box.visual_cues['background-color']
            if one_color != another_color:
                given_separator.weight += 1

    '''
    Rule 4: For horizontal separators,
            if the differences of font properties such as font size and font weight
            are bigger on two sides of the separator,the weight will be increased.
            Moreover,the weight will be increased if the font size of the block above the
            separator is smaller than the font size of the block below the separator.
    '''
    @staticmethod
    def rule4(given_separator):
        if given_separator.typ == given_separator.TYPE_HORIZONTAL:
            one_box = given_separator.one_side.boxes[0]
            another_box = given_separator.another_side.boxes[0]
            one_size = one_box.visual_cues['font-size']
            another_size = another_box.visual_cues['font-size']
            if one_size < another_size:
                given_separator.weight += 1
            if one_box.nodeType == 1 and another_box.nodeType == 1:
                one_weight = one_box.visual_cues['font-weight']
                another_weight = another_box.visual_cues['font-weight']
                if one_size != another_size and one_weight != another_weight:
                    given_separator.weight += 1

    '''
    Rule 5: For horizontal separators,
            when the structures of the blocks on the two sides of the separator are very similar
            (e.g. both are text), the weight of the separator will be decreased.
    '''
    @staticmethod
    def rule5(given_separator):
        if given_separator.typ == given_separator.TYPE_HORIZONTAL:
            one_box = given_separator.one_side.boxes[0]
            another_box = given_separator.another_side.boxes[0]
            one_name = one_box.nodeName
            another_name = another_box.nodeName
            if one_name == another_name:
                given_separator.weight -= 1
