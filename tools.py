class Stack(list):
        
    def push(self,l):
        if isinstance(l,list):
            while l:
                self.push(l.pop())
        else:
            self.append(l)
    def isEmpty(self):
        return not self
    def __str__(self):
        return ' '.join(map(str,self))
    
class State:
    def __init__(self,name,initial=False):
        self.name = name
        self.isInitial = initial
        self.isFinal = False
        self.outgoingEdges = list()
        self.ingoingEdges = list()
    
class Edge:
    def __init__(self,head,read,tail,write,di):
        self.head = head
        self.tail = tail
        self.read = read
        self.write = write
        self.di = di
    def __str__(self):
        return '{0}-----------{1},{2}/{3}---->{4}'.format(self.head.name,self.read,self.write,self.di,self.tail.name)

class PDAEdge:
    def __init__(self,head,read,tail,s1,s2,p1,p2):
        self.head = head
        self.read = read
        self.tail = tail
        self.s1 = s1
        self.s2 = s2
        self.p1 = p1
        self.p2 = p2
    def __str__(self):
        return '{0} -----{1},{2}/{3},{4}--------->{5}'.format(self.head.name,self.s1,self.s2,self.p1,self.p2,self.tail.name)
        
class TM:

    def __init__(self,manual = False):
        self.head = 0
        self.tape = ['*']
        self.gamma = []
        self.states = set()
        self.transitions = []
        self.firstState = None
        self.currentState = None
        if not manual:
            self.initiate()
    
    def initiate(self):
        stateNames = raw_input("Enter state names with space as separator\n").split(' ')
        self.states =list(set([State(n) for n in stateNames]))  # states initiated
        self.acceptState = State('ha')
        self.rejectState = State('hr')
        self.states.append(self.acceptState)
        self.states.append(self.rejectState)

        firstStateName = raw_input("What's the name of the first state?\n")
        for s in self.states:
            if s.name == firstStateName:
                s.isInitial = True
                self.firstState = s
                break           # first state determined
            
        self.gamma = raw_input("Enter tape symbols with space as separator\n").split(' ')  # tape symbols got fixed

        print("Ok, Now you should enter transitions one by one. one transition in a row. like this:\n")
        print("Source whatWeRead destination whatWeWrite direction\n")
        print("Blank to continue")
        while True:
            t = raw_input()
            if t == "":
                break
            else:
                t = tuple(t.split(' '))
                self.transitions.append(t)
        self.transitions = set(self.transitions)  # transitions added

        self.createGraph()
            
    def createGraph(self):
        for tr in self.transitions:
            e = Edge(tr[0],tr[1],tr[2],tr[3],tr[4])
            for s in self.states:
                if s.name == tr[0]:
                    e.head = s
                    s.outgoingEdges.append(e)
                if s.name == tr[2]:
                    e.tail = s
                    s.ingoingEdges.append(e)
    def turnOn(self,string):
        self.currentState = self.firstState
        self.tape.extend(list(string))
        self.go()
    def go(self):
        while self.currentState != self.acceptState and self.currentState != self.rejectState:
            for e in self.currentState.outgoingEdges:
                if e.read == self.tape[self.head]:
                    self.currentState = e.tail
                    self.tape[self.head] = e.write
                    self.moveHead(e.di)

        if self.currentState == self.acceptState:
              print 'Accepted'          
                    
    def moveHead(self,d):
        #print 'in moveHead'
        if d == 'r':
            self.head += 1
        if d == 'l':
            self.head -= 1
        if d == 's':
            pass

        if self.head >= len(self.tape):
            self.tape.extend(['*']*(self.head - len(self.tape) + 1))



class PDA:
    def __init__(self):
        self.states = list()
        self.stack1 = Stack()
        self.stack2 = Stack()
        self.sigma = list()
        self.gamma = list()
        self.firstState = None
        self.finalStates= list()
        self.currentState = None
    def turnOn(self,inp):
        self.stack1.push('*')
        self.stack2.push('*')
        self.stack2.push(list(inp))
        self.currentState = self.firstState
        self.go()
    def go(self):
        while not self.currentState.isFinal:
            for e in self.currentState.outgoingEdges:
                s1 = self.stack1.pop()
                if self.stack2.isEmpty():
                    s2 = '*'
                else:
                    s2 = self.stack2.pop()
                if isinstance(e,PDAEdge) and e.s1 == s1:
                    print e
                    assert(isinstance(e,PDAEdge))
                    self.currentState = e.tail
                    if e.p1 != '':
                        self.stack1.push([x if x!='#' else s2 for x in e.p1])
                    if e.p2 != '':
                        self.stack2.push([x if x!='#' else s2 for x in e.p2])
                    print '----------------------------------------'
                    print 'Stack1: '
                    print self.stack1
                    print 'Stack2 '
                    print self.stack2
                    break
                else:
                    self.stack1.push(s1)
                    self.stack2.push(s2)
        print "Accepted"
