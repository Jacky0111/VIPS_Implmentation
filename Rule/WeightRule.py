# 4.2 Visual Separator Detection
# 4.2.2 Setting Weights for Separators


class WeightRule:
    """
    Rule 1: The greater the distance between blocks on different side of the separator, the higher the weight.
    @param separator
    @return True if rule is applied, False otherwise.
    """""
    @staticmethod
    def rule1(separator):
        if separator.height > 65:
            separator.weight += 5
        elif 45 < separator.height <= 65:
            separator.weight += 4
        elif 35 < separator.height <= 45:
            separator.weight += 3
        elif 8 < separator.height <= 25:
            separator.weight += 2
        else:
            separator.weight += 1

        print(f'Went through rule 1, current weight is {separator.weight}')

    '''
    Rule 2: If a visual separator is overlapped with some certain HTML tags (e.g., the <HR> HTML tag), its weight is set to be higher.
    @param separator
    @param hr_list is list with <hr> HTML tag.
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def rule2(separator, hr_list):
        if hr_list is None:
            print(f'Went through rule 2, HR list is None, current weight is {separator.weight}')
            return

        for box in hr_list:
            sep_x = separator.width + separator.x
            sep_y = separator.height + separator.y
            hr_sep_x = box.visual_cues['bounds']['x'] + box.visual_cues['bounds']['width']
            hr_sep_y = box.visual_cues['bounds']['y'] + box.visual_cues['bounds']['height']

            if (separator.x <= box.visual_cues['bounds']['x'] and
                    separator.y <= box.visual_cues['bounds']['y'] and
                    sep_x > hr_sep_x and
                    sep_y > hr_sep_y):
                separator.weight += 1

        print(f'Went through rule 2, current weight is {separator.weight}')

    '''
    Rule 3: If background colors of the blocks on two sides of the separator are different, the weight will be increased.
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def rule3(separator):
        if separator.top is None or separator.bottom is None:
            return

        top_box = separator.top.boxes[0]
        bottom_box = separator.bottom.boxes[0]

        if top_box.nodeType == 1 and bottom_box.nodeType == 1:
            top_color = top_box.visual_cues['background-color']
            bottom_color = bottom_box.visual_cues['background-color']
            if top_color != bottom_color:
                separator.weight += 1

        print(f'Went through rule 3, current weight is {separator.weight}')

    '''
    Rule 4: For horizontal separators,
            if the differences of font properties such as font size and font weight
            are bigger on two sides of the separator,the weight will be increased.
            Moreover,the weight will be increased if the font size of the block above the
            separator is smaller than the font size of the block below the separator.
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def rule4(separator):
        if separator.top is None or separator.bottom is None:
            return

        if separator.typ == separator.TYPE_HORIZONTAL:
            top_box = separator.top.boxes[0]
            bottom_box = separator.bottom.boxes[0]
            top_font_size = top_box.visual_cues['font-size']
            bottom_font_size = bottom_box.visual_cues['font-size']
            top_font_weight = top_box.visual_cues['font-weight']
            bottom_font_weight = bottom_box.visual_cues['font-weight']

            if top_font_size < bottom_font_size:
                separator.weight += 1

            if top_font_size != bottom_font_size and top_font_weight != bottom_font_weight:
                separator.weight += 1

        print(f'Went through rule 4, current weight is {separator.weight}')

    '''
    Rule 5: For horizontal separators,
            when the structures of the blocks on the two sides of the separator are very similar
            (e.g. both are text), the weight of the separator will be decreased.
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def rule5(separator):
        if separator.top is None or separator.bottom is None:
            return

        if separator.typ == separator.TYPE_HORIZONTAL:
            top_name = separator.top.boxes[0].nodeName
            bottom_name = separator.bottom.boxes[0].nodeName
            if top_name == bottom_name:
                separator.weight -= 1

        print(f'Went through rule 5, FINAL weight is {separator.weight}')
