# 4.2 Visual Separator Detection
# 4.2.2 Setting Weights for Separators

from Rule.WeightRule import WeightRule


class SeparatorWeight:
    '''
    Execution function
    The separators are used to distinguish blocks with different semantics, so the weight of a separator can be 
    assigned based on the visual difference between its neighboring blocks
    '''''
    @staticmethod
    def runner(separator_list, hr_list):
        for separator in separator_list:
            # if separator.top is None or separator.bottom is None:
            #     continue
            WeightRule.rule1(separator)
            WeightRule.rule2(separator, hr_list)
            WeightRule.rule3(separator)
            WeightRule.rule4(separator)
            WeightRule.rule5(separator)
