# %%
import numpy as np


def blockDesigner(conditions, nRep):
    trialType = []
    for iBlock in range(nRep):
        # randomize the order of conditions (not in place)
        conditions_ = conditions.copy()
        np.random.shuffle(conditions_)
        trialType.extend(conditions_)
    return trialType


class Oracle:
    def __init__(self, nRep):
        self.states = ["00", "01", "10", "11"]
        self.rules = [
            "0001",
            "0010",
            "0011",
            "0100",
            "0101",
            "0110",
            "0111",
            "1000",
            "1001",
            "1010",
            "1011",
            "1100",
            "1101",
            "1110",
        ]
        self.nRep = nRep
        self.createTrial()

    def createTrial(self):
        self.trialType = blockDesigner(self.rules, self.nRep)
        self.nTrials = len(self.trialType)

    def interaction(self, X, iTrial):
        X = "".join([str(int(x)) for x in X])
        iState = self.states.index(X)
        rule = self.trialType[iTrial]
        iRule = self.rules.index(rule)
        return bool(int(self.rules[iRule][iState]))


# class Oracle_temporal_intergral(Oracle):
#     def __init__(self, nRep, wSize=20):
#         super().__init__(nRep)
#         self.wSize = wSize

#     def interaction(self, X, iTrial):
#         X = "".join([str(int(x)) for x in X])
#         iState = self.states.index(X)
#         rule = self.trialType[iTrial]
#         iRule = self.rules.index(rule)
#         return bool(int(self.rules[iRule][iState]))
    
if __name__ == "__main__":
    # test Oracle
    oracle = Oracle(2)
    oracle.createTrial()
    oracle.interaction([True, False], 0)
