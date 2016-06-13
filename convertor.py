from tools import *
from copy import deepcopy

def Convert(tm):
    pda = PDA()
    for s in tm.states:
        if s != tm.acceptState and s != tm.rejectState:
            pda.states.append(deepcopy(s))
    for s in pda.states:
        if s.name == tm.firstState.name:
             pda.firstState = s   
    for s in pda.states:
        newOuts = list()
        #print s.name        # test
        for e in s.outgoingEdges:
            newOuts.append(translation(e))
            s.outgoingEdges = deepcopy(newOuts)
    for s in pda.states:
        for e in s.outgoingEdges:
            if e.tail.name == 'ha':
                s.isFinal = True
            e.head = s
            for end in pda.states:
                if end.name == e.tail.name:
                    e.tail = end
  
    return pda
def translation(e):
    if e.di == 'r':
        out = PDAEdge(e.head,'*',e.tail,e.read,'#','#' + e.write,'')
    if e.di == 'l':
        out = PDAEdge(e.head,'*',e.tail,e.read,'#','',e.write + '#')
    if e.di == 's':
        out = PDAEdge(e.head,'*',e.tail,e.read,'#',e.write,'#')
    return out
#Tests
pda = Convert(TM())
pda.turnOn(raw_input('Input: '))

