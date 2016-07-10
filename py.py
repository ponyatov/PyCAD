import wx
import ply

class AST:
    def __init__(self,V):
        self.tag=self.__class__.__name__ ; self.val=V ; self.nest=[]
    def push(self,o): self.nest.append(o) ; return self
    def head(self): return "<%s:%s>"%(self.tag,self.val)
    def dump(self,depth=0):
        S="\n"+"\t"*depth+self.head()
        for i in self.nest: S+=i.dump(depth+1)
        return S
    def __repr__(self): return self.head()
    def __add__(self,o): return self.push(o)

Z=AST(123)
Z.push ( AST('Z') )

print Z.dump()

