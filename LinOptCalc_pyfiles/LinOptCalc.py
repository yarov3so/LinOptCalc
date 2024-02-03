#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 16:15:42 2023

@author: yarov3so
"""

from objrowinputformat import objrowinputformat
from constrrowinputformat import constrrowinputformat

noanswer=False

def delete(a):
    b=""
    return b

def forall(el,expr,f): # Applies function f to each element of expr. Does NOT change expr. Be careful - if expr is made up of ints, el must be an int. If expr is made up of floats, el must be a float! Also, using forall to replace select pieces of string by ones containing the original pieces will lead to infinite loops!
    while el in expr:
        if type(expr)==list:
            for i in range(len(expr)):
                if el==expr[i]:
                    expr=expr[0:i]+[f(el)]+expr[i+1:len(expr)]
                    break
        if type(expr)==str: # Can remove multiple consecutive characters in a string!
            j=len(el)
            for i in range(len(expr)):
                if el==expr[i:i+j]:
                    expr=expr[0:i]+f(el)+expr[i+j:len(expr)]
                    break
        if type(expr)==tuple:
            for i in range(len(expr)):
                if el==expr[i]:
                    expr=expr[0:i]+(f(el),)+expr[i+1:len(expr)]
                    break
    return expr

print("")
print("LINEAR OPTIMIZATION CALCULATOR")
print("Written by yarov3so")
print("")
problem=input(" For maximization, please enter \"max\". \n For minimization, please enter \"min\". \n\n Answer: ")
while problem != "max" and problem != "min":
    problem=input("Your choice was not registered. \n For maximization, please enter \"max\". \n For minimization, please enter \"min\". \n Answer: ")

print("")

ObjRow=[]
slack=[]

ConstrRows_tuple=constrrowinputformat() # Asks user to input all the constraints in the optimization problem
ConstrRows=ConstrRows_tuple[0]
Nconstr=len(ConstrRows)
ConstrRows=ConstrRows+[0]
Nvar=ConstrRows_tuple[1]
zeroone=list(list([] for i in range(Nconstr+1)) for i in range(Nconstr+1))
    
for i in range(Nconstr):
    slack+=[0.0]
    
for i in range(Nconstr+1):
    
    for j in range(Nconstr+1):
        if i==j:
            zeroone[i][j]=1.0
        else:
            zeroone[i][j]=0.0
            
for i in range(Nconstr):
    ConstrRows[i]=ConstrRows[i][0:len(ConstrRows[i])-1] + zeroone[i] + [ConstrRows[i][len(ConstrRows[i])-1]]

slackvars=""
for i in range(Nvar,Nconstr+Nvar):
    slackvars+=f"x_{i+1}, "

print("")
print(f"Introducing slack variables: {slackvars[0:len(slackvars)-2]}")
print("")


if Nvar==1:
    PreObjList=input("Please enter the algebraic expression of the objective function: \n\n f(x_1) = ")
elif Nvar==2:
    PreObjList=input("Please enter the algebraic expression of the objective function: \n\n f(x_1,x_2) = ")
elif Nvar==3:
    PreObjList=input("Please enter the algebraic expression of the objective function: \n\n f(x_1,x_2,x_3) = ")
else:
    PreObjList=input(f"Please enter the algebraic expression of the objective function: \n\n f(x_1, ... ,x_{Nvar}) = ")
if forall(" ",PreObjList,delete)=="0":
    PreObjList="0x1"
PreObjList=objrowinputformat(PreObjList,Nvar)
if problem=="max":
    PreObjList=[-x for x in PreObjList]
ObjRow=PreObjList + slack + [1.0]+[0.0] # Unnecessary label, but will be integrated in the list ConstrRows later

print("")
print("The following tableau was registered: ")
print("")

for i in range(Nconstr):
    print("Constraint Row #"+str(i+1)+":",ConstrRows[i][0:len(ConstrRows[i])-1],"|",ConstrRows[i][len(ConstrRows[i])-1])
    
print("Objective Row:    ", ObjRow[0:len(ObjRow)-1],"|",ObjRow[len(ObjRow)-1])


ConstrRows[Nconstr]=ObjRow #O bjRow has been integrated into ConstrRows. From now on, we work exclusively with ConstrRows. Pheww
ncols=Nconstr+Nvar+2 # Easier to work with these numbers than constantly referencing individual list lengths...
nrows=Nconstr+1 # ditto
init_constants=[ConstrRows[i][ncols-1] for i in range(nrows-1)] # Will be needed at the end


def neg_entry(mylist) : 

    """

    Parameters
    ----------
    mylist : any list
 
    Returns
    -------
    verdict : whether or not the list contains a negative entry
    problem_pos : the FIRST position at which a negative entry occurs, if any. Returns False otherwise 

    """
    verdict=False
    problem_pos=False
    for i in range(len(mylist)):
        if mylist[i] < 0:
            verdict=True 
            problem_pos=i
            break
    return (verdict,problem_pos)

def first_char(myexpr,char) : 

    """

    Parameters
    ----------
    mylist : any list
 
    Returns
    -------
    verdict : whether or not myexpr contains the character char
    problem_pos : the FIRST position at which char occurs, if any. Returns False otherwise 

    """
    verdict=False
    problem_pos=False
    for i in range(len(myexpr)):
        if myexpr[i] == char:
            verdict=True 
            problem_pos=i
            break
    return (verdict,problem_pos)


def negoreq_entry(mylist) : 

    """

    Parameters
    ----------
    mylist : any list
 
    Returns
    -------
    verdict : whether or not the list contains a negative entry OR ZERO
    problem_pos : the FIRST position at which a negative entry occurs, if any. Returns False otherwise 

    """
    verdict=False
    problem_pos=False
    for i in range(len(mylist)):
        if mylist[i] <= 0:
            verdict=True 
            problem_pos=i
            break
    return (verdict,problem_pos)

def all_neg(mylist) :
    
    """

    Parameters
    ----------
    mylist : any list

    Returns
    -------
    verdict : whether or not the list is made up of all negative numbers 

    """
    
    verdict=True
    for i in range(len(mylist)):
        if mylist[i]>0:
            verdict=False
            break
    return verdict

def all_neg0(mylist) :
    
    """

    Parameters
    ----------
    mylist : any list

    Returns
    -------
    verdict : whether or not the list is made up of all negative numbers 

    """
    
    verdict=True
    for i in range(len(mylist)):
        if mylist[i]>0:
            verdict=False
            break
    return verdict


# We now ensure that the starting basic solution of our linear optimization problem is feasible.

constants=[ConstrRows[i][ncols-1] for i in range(nrows-1)]
a=neg_entry(constants)[0]
b=neg_entry(constants)[1]

if (neg_entry(constants))[0]==True and neg_entry(ConstrRows[b][0:ncols-1])[0]==False:
    print("")
    print("The linear system's feasible region is empty.")
    noanswer=True
    
else: 
    while a==True:
        colindex=neg_entry([ConstrRows[b][i] for i in range(ncols-1)])[1]
        column_interest=[ConstrRows[i][colindex] for i in range(nrows-1)]
        ratiolist=[0.0 for i in range(nrows-1)]
        for i in range(nrows-1):
            if column_interest[i] != 0 :
                ratiolist[i]=constants[i] / column_interest[i]
        currentmin=0
        ratiolist_copy=ratiolist[:]
        while currentmin <= 0 and negoreq_entry(ratiolist_copy)[0]==True:
            minpos=ratiolist_copy.index(min(ratiolist_copy))
            ratiolist_copy=ratiolist_copy[0:minpos]+ratiolist_copy[minpos+1:len(ratiolist_copy)]
            currentmin=min(ratiolist_copy)
        rowindex=ratiolist.index(min(ratiolist_copy))
        for i in range(nrows-1):
            if column_interest[i]!=0.0 and constants[i]==0.0:
                rowindex=i
                break
        ConstrRows[rowindex]=[x / column_interest[rowindex] for x in ConstrRows[rowindex]]
        
        print("")
        print("Pivoting on entry ("+str(rowindex+1)+","+str(colindex+1)+"):")
        print("")
    
    
        for i in range(nrows):
            if i != rowindex:
                ConstrRows[i]=[x-(ConstrRows[i][colindex])*y for x, y in zip(ConstrRows[i],ConstrRows[rowindex])]
    
        for i in range(Nconstr):
            print("Constraint Row #"+str(i+1)+":",ConstrRows[i][0:len(ConstrRows[i])-1],"|",ConstrRows[i][len(ConstrRows[i])-1])
        
        print("Objective Row:    ", ConstrRows[nrows-1][0:len(ObjRow)-1],"|",ConstrRows[nrows-1][len(ObjRow)-1])
    
        constants=[ConstrRows[i][ncols-1] for i in range(nrows-1)]
        a=neg_entry(constants)[0]
        b=neg_entry(constants)[1]
        
        if (neg_entry(constants))[0]==True and neg_entry(ConstrRows[b][0:ncols-1])[0]==False:
            print("")
            print("The linear system's feasible region is empty.")
            noanswer=True
            break


# With the tableau prepped (the starting basic solution is feasible), time to apply the simplex method:
    
if a==False:
    print("")
    print ("The basic solution is feasible.")       

while neg_entry(ConstrRows[nrows-1][0:ncols-1])[0]==True and a==False:
    all_negTF=[all_neg([ConstrRows[i][j] for i in range(nrows)]) for j in range(ncols-1)]
    unbvars=""
    for j in range(ncols-2):
        if all_negTF[j]==True and ConstrRows[nrows-1][j] != 0.0:
            i_unb=j + 1
            unbvars+=f"x_{i_unb}, "
    if unbvars!="":
        noanswer=True
        print("")
        print(f"The linear system's feasible region is unbounded due to the presence of unbounded variables: {unbvars[0:len(unbvars)-2]}.")
        break
    colindex = neg_entry(ConstrRows[nrows-1][0:ncols-1])[1] # Finds the horizontal (row) position of the first negative entry in the objective row
    column_interest=[ConstrRows[i][colindex] for i in range(nrows-1)]
    ratiolist=[0.0 for i in range(nrows-1)]
    for i in range(nrows-1):
        if column_interest[i] != 0 :
            ratiolist[i]=constants[i] / column_interest[i]
    currentmin=0
    ratiolist_copy=ratiolist[:]
    while currentmin <= 0 and negoreq_entry(ratiolist_copy)[0]==True:
        minpos=ratiolist_copy.index(min(ratiolist_copy))
        ratiolist_copy=ratiolist_copy[0:minpos]+ratiolist_copy[minpos+1:len(ratiolist_copy)]
        currentmin=min(ratiolist_copy)
    rowindex=ratiolist.index(min(ratiolist_copy)) # Finds the vertical (column) position of the pivot corresponding to the variable we are bringing into the solution.
    for i in range(nrows-1):
        if column_interest[i]!=0.0 and constants[i]==0.0:
            rowindex=i
            break
    ConstrRows[rowindex]=[x / column_interest[rowindex] for x in ConstrRows[rowindex]]
    
    print("")
    print("Pivoting on entry ("+str(rowindex+1)+","+str(colindex+1)+"):")
    print("")
    
    for i in range(nrows):
        if i != rowindex:
            ConstrRows[i]=[x-(ConstrRows[i][colindex])*y for x, y in zip(ConstrRows[i],ConstrRows[rowindex])]
            
    constants=[ConstrRows[i][ncols-1] for i in range(nrows-1)]
    
    for i in range(Nconstr):
        print("Constraint Row #"+str(i+1)+":",ConstrRows[i][0:len(ConstrRows[i])-1],"|",ConstrRows[i][len(ConstrRows[i])-1])
    print("Objective Row:    ", ConstrRows[nrows-1][0:len(ObjRow)-1],"|",ConstrRows[nrows-1][len(ObjRow)-1])
    
def zerocount(mylist):
    i=0
    for j in range(len(mylist)):
        if mylist[j]==0:
            i=i+1
    return i

soln=[0 for i in range(Nvar)]
dist=[0 for i in range(Nconstr)]

constants=[ConstrRows[i][ncols-1] for i in range(nrows-1)]

for j in range(Nvar):
    column_j=[ConstrRows[i][j] for i in range(nrows)]
    if zerocount(column_j)==nrows-1:
        first_1=first_char(column_j,1)[1]
        soln[j]=constants[first_1]
    else:
        soln[j]=0.0
        
for j in range(Nvar,ncols-2):
    column_j=[ConstrRows[i][j] for i in range(nrows)]
    if zerocount(column_j)==nrows-1:
        first_1=first_char(column_j,1)[1]
        dist[j-Nvar]=constants[first_1]
    else:
        dist[j-Nvar]=0.0
        


if problem=="max" and noanswer==False:
    print("")
    print("The maximum value of the objective function is",float(ConstrRows[nrows-1][len(ObjRow)-1]),".")
    print("")
    print(f"The maximum occurs at {soln} and this maximum's inequality constraint deficiencies are: \n")
    for i in range(Nconstr):
        if dist[i]==0.0:
            print(f" Constraint #{i+1} deficiency:",dist[i],"--->","The coordinates of this maximum satisfy the equality version of this constraint." )
        else: 
            print(f" Constraint #{i+1} deficiency:",dist[i],"--->",f"The coordinates of this maximum satisfy the equality version of this constraint if its bounding term {init_constants[i]} is replaced by {init_constants[i]} - {dist[i]} = {init_constants[i]-dist[i]} .")



if problem=="min" and noanswer==False:
    print("")
    print("The minimum value of the objective function is",float(-ConstrRows[nrows-1][len(ObjRow)-1]),".")
    print("")
    print(f"The minimum occurs at {soln} and this minimum's inequality constraint deficiencies are: \n")
    for i in range(Nconstr):
        if dist[i]==0.0:
            print(f" Constraint #{i+1} deficiency:",dist[i],"--->","The coordinates of this minimum satisfy the equality version of this constraint." )
        else: 
            print(f" Constraint #{i+1} deficiency:",dist[i],"--->",f"The coordinates of this minimum satisfy the equality version of this constraint if its bounding term {init_constants[i]} is replaced by {init_constants[i]} - {dist[i]} = {init_constants[i]-dist[i]} .")


print("")

    
                        
                