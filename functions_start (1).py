import itertools

def solution(A):
    p = str(A)
    lst = []
    for i in p:
        p.append(i)
    perms = list(itertools.permutations(lst))
    fLst = []
    for i in perms:
        strNum = []
        for x in i:
            strNum.append(x)
        b = ''.join(strNum)
        fLst.append(b)
    fLst = list(map(int, fLst)
    return fLst

if __name__ == "__main__":
    print solution(1267)
        
            
        
    

          
    