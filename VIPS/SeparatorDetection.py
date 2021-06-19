# 4.2 Visual Separator Detection
# 4.2.1 Separator Detection

import sys
from Rule.SeparatorRule import SeparatorRule
from VariationOrder.SeparatorVO import SeparatorVO


class SeparatorDetection:
    width = 0
    height = 0
    typ = 0
    separator_list = None
    count = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.separator_list = []

    def service(self, blocks, typ):
        self.typ = typ
        self.separator_list.clear()
        self.step1()
        self.step2(blocks)
        self.step3()
        print(f'{str(self.typ)}-Size of Separator List: {str(len(self.separator_list))}')
        return self.separator_list

    '''
    Step 1
    Initialize the separator list. The list starts with only one separator (Pbe, Pee) whose start pixel and end pixel 
    are corresponding to the borders of the pool.
    '''

    def step1(self):
        separator = SeparatorVO(0, 0, self.width, self.height, self.typ)
        self.separator_list.append(separator)

    '''
    Step 2
    For every block in the pool, the relation of the block with each separator is evaluated.
    a) If the block is contained in the separator, split the separator.
    b) If the block crosses with the separator, update the separator’s parameters.
    c) If the block covers the separator, remove the separator.
    '''

    def step2(self, given_blocks):
        if len(self.separator_list) > 0:
            if self.typ == SeparatorVO.TYPE_HORIZONTAL:
                self.horizontalDetection(given_blocks)
            else:
                self.verticalDetection(given_blocks)

    '''
    Step 3
    Remove the four separators that stand at the border of the pool.
    '''

    def step3(self):
        temp = [self.separator_list]
        if self.typ == SeparatorVO.TYPE_HORIZONTAL:
            for separator in temp:
                if separator.x == 0 and (separator.y == 0 or separator.y + separator.height == self.height):
                    self.separator_list.remove(separator)
        else:
            for separator in temp:
                if separator.y == 0 and (separator.x == 0 or separator.x + separator.width == self.width):
                    self.separator_list.remove(separator)

    def horizontalDetection(self, given_blocks):
        for block in given_blocks:
            temp = []
            for sep in temp:
                self.count += 1
                print(self.count)

                if SeparatorRule.horizontalRule1(block, sep):
                    y = block.y + block.height
                    separator_y = sep.y + sep.height
                    new_separator = SeparatorVO(0, y, self.width, separator_y, self.typ)

                    if new_separator != 0:
                        new_separator.one_side = block
                        self.separator_list.append(new_separator)

                    separator = sep
                    separator.height = block.y - separator.y
                    if separator.height == 0:
                        self.separator_list.remove(separator)
                    else:
                        separator.other_side(block)

                elif SeparatorRule.horizontalRule2(block, sep):
                    self.separator_list.remove(sep)
                elif SeparatorRule.horizontalRule3(block, sep):
                    separator = sep
                    original_y = separator.y
                    separator.y = block.y + block.height
                    separator.height = separator.height + original_y - separator.y
                    separator.one_side(block)
                elif SeparatorRule.horizontalRule4(block, sep):
                    separator = sep
                    separator.height = block.y - separator.y
                    separator.other_side = block
                else:
                    continue

    def verticalDetection(self, given_blocks):
        self.separator_list.clear()
        for block1 in given_blocks:
            left_min_width = sys.maxsize
            left_x = 0
            left_y = 0
            left_width = 0
            left_height = 0

            right_min_width = sys.maxsize
            right_x = 0
            right_y = 0
            right_width = 0
            right_height = 0

            for block2 in given_blocks:
                if block1 == block2:
                    continue
                # The two blocks have no intersection in the x range, and there is an intersection in the y range
                width_x1 = block1.x + block1.width
                width_x2 = block2.x + block2.width
                height_y1 = block1.y + block1.height
                height_y2 = block2.y + block2.height

                # 2 is on the left hand side of 1
                if width_x2 < block1.x:
                    x = block2.x + block2.width  # width_x2
                    width = block1.x - x

                    sep = SeparatorVO(0, 0, block1.x, block1.height, SeparatorVO.TYPE_HORIZONTAL)
                    if SeparatorRule.horizontalRule1(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block1.y
                            left_width = width
                            left_height = block1.height
                    elif SeparatorRule.horizontalRule2(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block2.y
                            left_width = width
                            left_height = block2.height
                    elif SeparatorRule.horizontalRule3(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block2.y
                            left_width = width
                            left_height = height_y1 - block2.y
                    elif SeparatorRule.horizontalRule4(block2, sep):
                        if width < left_min_width:
                            left_min_width = width
                            left_x = x
                            left_y = block1.y
                            left_width = width
                            left_height = height_y2 - block1.y

                # 2 is on the right hand side of 1
                elif width_x1 < block2.x:
                    x = block1.x + block1.width
                    width = block2.x - x

                    sep = SeparatorVO(x, block1.y, block1.width, block1.height, SeparatorVO.TYPE_HORIZONTAL)
                    if SeparatorRule.horizontalRule1(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block1.y
                            right_width = width
                            right_height = block1.height
                    elif SeparatorRule.horizontalRule2(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block2.y
                            right_width = width
                            right_height = block2.height
                    elif SeparatorRule.horizontalRule3(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block1.y
                            right_width = width
                            right_height = height_y1 - block2.height
                    elif SeparatorRule.horizontalRule4(block2, sep):
                        if width < right_min_width:
                            right_min_width = width
                            right_x = x
                            right_y = block1.y
                            right_width = width
                            right_height = height_y2 - block1.height
            if left_min_width < sys.maxsize:
                separator = SeparatorVO(left_x, left_y, left_width, left_height, SeparatorVO.TYPE_VERTICAL)
                self.separator_list.append(separator)
            if right_min_width < sys.maxsize:
                separator = SeparatorVO(right_x, right_y, right_width, right_height, SeparatorVO.TYPE_HORIZONTAL)
                self.separator_list.append(separator)
        self.mergeSeparator()

    def mergeSeparator(self):
        removed_list = []
        removed_index = []
        temp = [self.separator_list]
        for i in range(len(temp)):
            separator1 = temp[i]
            for j in range(i + 1, len(temp)):
                separator2 = temp[j]
                if separator1 == separator2 and abs(separator1.y - separator2.y) < 100:
                    removed_index.append(j)
                    if separator2.y > separator1.y:
                        separator1.y = separator1.y
                        separator1.height = abs(separator1.y - separator2.y + separator2.height)
                    elif separator2.y < separator1.y:
                        separator1.y = separator2.y
                        separator1.height = abs(separator1.y - separator2.y + separator1.height)

        for index in removed_index:
            removed_list.append(index)

        for sep in removed_list:
            removed_list.remove(sep)
