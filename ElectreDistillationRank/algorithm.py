import copy, math

from copy import deepcopy

class algorithm(object):
    
    def __init__(self, alternatives, downwards, upwards):
        self.alternatives = alternatives
        self.N = len(alternatives)
        self.downwards = downwards
        self.upwards = upwards
        
    def Run(self):   
        # S relation
        s = {}
        rank = (self.downwards, self.upwards)
        
        for a1 in self.alternatives:
            s[a1] = {}
            for a2 in self.alternatives:
                s[a1][a2] = 0
                
        for a1 in self.alternatives:
            for a2 in self.alternatives:
                if a1 == a2:
                    s[a1][a2] = 1
                    continue
                for i in range(2):
                    a = self.isBetter(a1, a2, rank[i])
                    b = self.isBetter(a2, a1, rank[1 - i])
                    if (a == b == 0):
                        s[a1][a2] = 1
                        break
                    if (a == b == 1):
                        s[a1][a2] = 0
                        break
                    if (a == 1) and (b <= 0):
                        s[a1][a2] = 1                   
                        break
        
        # Find Bests and Next
        best = []
        next = {}
        for a1 in self.alternatives:
            dc = 0
            a3 = -1
            for a2 in self.alternatives:
                if a1 == a2: 
                    continue    
                if (s[a2][a1] == 1) and (s[a1][a2] == 0):
                    dc = 1
                if (s[a1][a2] == 1) and (s[a2][a1] == 0):
                    if (a3 == -1) or ((s[a2][a3] == 1) and (s[a3][a2] == 0)):
                        a3 = a2                                    
            next[a1] = a3
            if dc == 0:
                best.append(a1)
        
        # Final rank        
        r = {}
        for a1 in self.alternatives:
            b = self.N
            for root in best:
                c = root
                l = 0
                while (c != a1) and (next[c] != -1):
                    c = next[c]
                    l += 1
                if l < b:
                    b = l
            r[a1] = b
        
        #Median ranking
        mo = []
        for i in range(self.N):
            mo.append(i)
            for j in xrange(i, 0, -1):
                a1 = self.alternatives[mo[j]]
                a2 = self.alternatives[mo[j - 1]]
                if r[a2] < r[a1]:
                    break
                if r[a2] > r[a1]:
                    mo[j - 1], mo[j] = mo[j], mo[j - 1]
                elif r[a2] == r[a1]:
                    d1 = self.downwards[a1] - self.downwards[a2]
                    d2 = self.upwards[a1] - self.upwards[a2]
                    if d1 + d2 < 0:
                        mo[j - 1], mo[j] = mo[j], mo[j - 1]
        
        m = {}
        p = 1
        for i in range(len(mo)):
            if i > 0:
                a1 = self.alternatives[mo[i]]
                a2 = self.alternatives[mo[i - 1]]
                if (r[a2] < r[a1]):
                    p += 1
                elif (r[a2] == r[a1]):
                    d1 = self.downwards[a1] - self.downwards[a2]
                    d2 = self.upwards[a1] - self.upwards[a2]
                    if d1 + d2 > 0:
                        p += 1 
            m[self.alternatives[mo[i]]] = p   
               
                        
        result = (s, r, m)
        return result
     
        
    def isBetter(self, A, B, ranking):
        if ranking[A] < ranking[B]:
            return 1
        elif ranking[A] == ranking[B]:
            return 0
        else:
            return -1