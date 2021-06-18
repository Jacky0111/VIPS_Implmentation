# 4.2 Visual Separator Detection
# 4.2.1 Separator Detection

class SeparatorRule:
    """
    Horizontal Rule 1: If the horizontal block is contained in the separator, split the separator.
    """""
    @staticmethod
    def horizontalRule1(given_block, given_separator):
        y = given_block.y
        height_y = given_block.height + y
        separator_y = given_separator.height + given_separator.y

        if y > given_separator.y and height_y < separator_y:
            return True
        return False

    '''
    Horizontal Rule 2: If the horizontal block crosses with the separator, update the separator’s parameters.
    '''
    @staticmethod
    def horizontalRule2(given_block, given_separator):
        y = given_block.y
        height_y = given_block.height + y
        separator_y = given_separator.height + given_separator.y

        if y < given_separator.y and height_y > separator_y:
            return True
        return False

    '''
    Horizontal Rule 3: If the horizontal block covers top of the separator, remove the separator.
    '''
    @staticmethod
    def horizontalRule3(given_block, given_separator):
        y = given_block.y
        height_y = given_block.height + y
        separator_y = given_separator.height + given_separator.y

        if y > given_separator.y > height_y > separator_y:
            return True
        return False

    '''
    Horizontal Rule 4: If the horizontal block covers bottom of the separator, remove the separator.
    '''
    @staticmethod
    def horizontalRule4(given_block, given_separator):
        y = given_block.y
        height_y = given_block.height + y
        separator_y = given_separator.height + given_separator.y

        if y < given_separator.y < height_y < separator_y:
            return True
        return False

    '''
    Vertical Rule 1: If the vertical block is contained in the separator, split the separator.
    '''
    @staticmethod
    def verticalRule1(given_block,  given_separator):
        x = given_block.x
        width_x = given_block.width + x
        separator_x = given_separator.width + given_separator.x

        if x > given_separator.x and width_x < separator_x:
            return True
        return False

    '''
    Vertical Rule 2: If the vertical block crosses with the separator, update the separator’s parameters.
    '''
    @staticmethod
    def verticalRule2(given_block, given_separator):
        x = given_block.x
        y = given_block.y
        width_x = given_block.width + x
        height_y = given_block.height + y
        separator_x = given_separator.width + given_separator.x
        separator_y = given_separator.height + given_separator.y

        if (x < given_separator.x and
                y > given_separator.y and
                width_x > separator_x and
                height_y < separator_y):
            return True
        return False

    '''
    Vertical Rule 3: If the vertical block covers left of the separator, remove the separator.
    '''
    @staticmethod
    def verticalRule3(given_block, given_separator):
        x = given_block.x
        width_x = given_block.width + x
        separator_x = given_separator.width + given_separator.x

        if x < given_separator.x < width_x < separator_x:
            return True
        return False

    '''
    Vertical Rule 4: If the vertical block covers right of the separator, remove the separator.
    '''
    @staticmethod
    def verticalRule4(given_block,  given_separator):
        x = given_block.x
        width_x = given_block.width + x
        separator_x = given_separator.width + given_separator.x

        if given_separator.x < x < separator_x < width_x:
            return True
        return False
