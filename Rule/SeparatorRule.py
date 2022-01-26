# 4.2 Visual Separator Detection
# 4.2.1 Separator Detection

class SeparatorRule:
    """
    Horizontal Rule 1: If the horizontal block is contained in the separator, split the separator.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.  
    """""
    @staticmethod
    def horizontalRule1(block, separator):
        y = block.y
        block_height_y = block.height + y
        separator_height_y = separator.height + separator.y
        # print(f'y = {y}, bhy = {block_height_y}, sep_y = {separator.y}, shy = {separator_height_y}')

        if y > separator.y and block_height_y < separator_height_y:
            print('Comply Horizontal Rule 1, split the separator')
            return True
        print('Violated Horizontal Rule 1, do not split')
        return False

    '''
    Horizontal Rule 2: If the top of horizontal block crosses with the separator, update the separator’s parameters.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def horizontalRule2(block, separator):
        y = block.y
        block_height_y = block.height + y
        separator_height_y = separator.height + separator.y
        # print(f'y = {y}, bhy = {block_height_y}, sep_y = {separator.y}, shy = {separator_height_y}')

        if separator_height_y > block_height_y > separator.y > y:
            print('Comply Horizontal Rule 2, update the separator')
            return True
        print('Violated Horizontal Rule 2, do not update')
        return False

    '''
    Horizontal Rule 3: If the bottom of horizontal block crosses with the separator, update the separator’s parameters.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def horizontalRule3(block, separator):
        y = block.y
        block_height_y = block.height + y
        separator_height_y = separator.height + separator.y
        # print(f'y = {y}, bhy = {block_height_y}, sep_y = {separator.y}, shy = {separator_height_y}')

        if block_height_y > separator_height_y > y > separator.y:
            print('Comply Horizontal Rule 3, update the separator')
            return True
        print('Violated Horizontal Rule 3, do not update')
        return False

    '''
    Horizontal Rule 4: If the horizontal block covers the separator, remove the separator.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def horizontalRule4(block, separator):
        y = block.y
        block_height_y = block.height + y
        separator_height_y = separator.height + separator.y
        # print(f'y = {y}, bhy = {block_height_y}, sep_y = {separator.y}, shy = {separator_height_y}')

        if y < separator.y and block_height_y > separator_height_y:
            print('Comply Horizontal Rule 4, remove the separator')
            return True
        print('Violated Horizontal Rule 4, do not remove')
        return False

    '''
    Vertical Rule 1: If the vertical block is contained in the separator, split the separator.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def verticalRule1(block,  separator):
        x = block.x
        block_width_x = block.width + x
        separator_width_x = separator.width + separator.x

        if x > separator.x and block_width_x < separator_width_x:
            print('Comply Vertical Rule 1, split the separator')
            return True
        print('Violated Vertical Rule 1, do not split')
        return False

    '''
    Vertical Rule 2: If the left of vertical block crosses with the separator, update the separator’s parameters.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def verticalRule2(block, separator):
        x = block.x
        block_width_x = block.width + x
        separator_width_x = separator.width + separator.x

        if block_width_x > separator_width_x > x > separator.x:
            print('Comply Vertical Rule 3, update the separator')
            return True
        print('Violated Vertical Rule 3, do not update')
        return False

    '''
    Vertical Rule 3: If the right of vertical block crosses with the separator, update the separator’s parameters.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def verticalRule3(block, separator):
        x = block.x
        block_width_x = block.width + x
        separator_width_x = separator.width + separator.x

        if x < separator.x < block_width_x < separator_width_x:
            print('Comply Vertical Rule 4, remove the separator')
            return True
        print('Violated Vertical Rule 4, do not remove')
        return False

    '''
    Vertical Rule 4: If the vertical block covers the separator, remove the separator.
    @param block
    @param separator
    @return True if rule is applied, False otherwise.
    '''
    @staticmethod
    def verticalRule4(block,  separator):
        x = block.x
        y = block.y
        block_width_x = block.width + x
        block_height_y = block.height + y
        separator_width_x = separator.width + separator.x
        separator_height_y = separator.height + separator.y

        if x < separator.x and y > separator.y and block_width_x > separator_width_x and block_height_y < separator_height_y:
            print('Comply Vertical Rule 4, remove the separator')
            return True
        print('Violated Vertical Rule 4, do not remove')
        return False
