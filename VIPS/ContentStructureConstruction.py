#  4.3 Content Structure Construction

from VariationOrder.SeparatorVO import SeparatorVO
from VariationOrder.BlockVO import BlockVO


class ContentStructureConstruction:
    @staticmethod
    def service(separator_list, given_block):
        if len(separator_list) > 0:
            temp = [separator_list]
            max_weight = temp[len(temp) - 1].weight
            print(f'Maximum Weight: {max_weight}')
            for separator in temp:
                if max_weight == separator.weight:
                    break
                if separator.one_side is not None and separator.another_side is not None:
                    one = separator.one_side
                    another = separator.another_side

                    newBlock = BlockVO()
                    newBlock.parent = one.parent
                    newBlock.boxes.extend(one.boxes)
                    newBlock.boxes.extend(another.boxes)
                    newBlock.children.extend(one.children)
                    newBlock.children.extend(another.children)
                    newBlock.DoC = separator.weight
                    newBlock.refresh()

                    one.parent.children.append(newBlock)
                    one.isVisualBlock = False
                    another.isVisualBlock = False

                    total = 0
                    for sep in temp:
                        if sep.one_side == another:
                            sep.one_side = newBlock
                            total += 1
                        if sep.another_side == one:
                            sep.another_side = newBlock
                            total += 1
                        if total == 2:
                            break
                    separator_list.remove(separator)
