# 4.2 Visual Separator Detection
# 4.2.2 Setting Weights for Separators

from Rule.WeightRule import WeightRule


class SeparatorWeight:
    def __init__(self, node_list):
        WeightRule.initialization(node_list)

    @staticmethod
    def service(separator_list, hr_list):
        for separator in separator_list:
            if separator.one_side is None or separator.another_side is None:
                continue
            WeightRule.rule1(separator)
            WeightRule.rule2(separator, hr_list)
            WeightRule.rule3(separator)
            WeightRule.rule4(separator)
            WeightRule.rule5(separator)
