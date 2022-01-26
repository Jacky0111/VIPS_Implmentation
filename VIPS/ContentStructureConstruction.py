#  4.3 Content Structure Construction
import time

from VIPS.VisualBlockExtraction import VisualBlockExtraction


class ContentStructureConstruction:
    '''
    Execution function
    '''''
    @staticmethod
    def runner(separator_list):
        if not separator_list:
            return

        temp = []
        temp.extend(separator_list)
        # Take the last element of temp as the max weight because the list has been sorted
        max_weight = temp[len(temp) - 1].weight

        for separator in temp:
            if max_weight == separator.weight:
                break

            if separator.top is not None and separator.bottom is not None:
                top = separator.top
                bottom = separator.bottom

                new_block = VisualBlockExtraction(False)
                new_block.parent = top.parent
                new_block.boxes.extend(top.boxes)
                new_block.boxes.extend(bottom.boxes)
                new_block.children.extend(top.children)
                new_block.children.extend(bottom.children)
                new_block.DoC = separator.weight

                top.parent.children.append(new_block)

                top.isVisualBlock = False
                bottom.isVisualBlock = False

                total = 0
                for sep in temp:
                    if sep.top == bottom:
                        sep.top = new_block
                        total += 1
                    if sep.bottom == top:
                        sep.bottom = new_block
                        total += 1
                    if total == 2:
                        break
                separator_list.remove(separator)
