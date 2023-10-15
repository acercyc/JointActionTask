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

class Oracle_switcher:
    def __init__(self, wSize=1):
        self.states = ["00", "01", "10", "11"]
        self.wSize = wSize
        self.rules = ['1000', '0100', '0010', '0001']
        self.iRule = None
        self.state_sequence = []
        self.ts = []
        self.ys = []
        self.lastChangeTime = 0
        self.iTrial = None

    # TODO: add trial signal here
    def interaction(self, X, t, iTrial):
        
        # reset if the trial is different
        if self.iTrial != iTrial:
            self.iTrial = iTrial
            self.state_sequence = []
            self.ts = []
            self.ys = []
            self.lastChangeTime = 0
            self.iRule = None
                
        X = "".join([str(int(x)) for x in X])
        iState = self.states.index(X)
        self.state_sequence.append(iState)
        self.ts.append(t)
                
        if len(self.state_sequence) == 1:
            # random sample a rule except the current state
            self.iRule = self.selectDifferentRule(iState)
            self.lastChangeTime = t
            
        y = iState == self.iRule
        self.ys.append(y)
            
        if t - self.lastChangeTime > self.wSize:
            # check if from (t-wSize) to t, the state is the same
            # find index of the first time point within the window of (t-wSize) in ts
            iTime = np.searchsorted(self.ts, t - self.wSize, side='right')
            if all(self.ys[iTime:]):
                # if all the states are the same, switch the rule
                self.iRule = self.selectDifferentRule(iState)
                self.lastChangeTime = t

        return y
        

    def selectDifferentRule(self, iState):
        rules = list(range(len(self.rules)))
        rules.remove(iState)
        return np.random.choice(rules)



# %%    
if __name__ == "__main__":
    # test Oracle
    oracle = Oracle(2)
    oracle.createTrial()
    oracle.interaction([True, False], 0)
