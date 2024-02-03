#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 12:02:24 2023

@author: yarov3so
"""

def constrrowinputformat():
    """
    Asks the user to enter all the linear constraints of the optimization problem separated by commas
    Calculates the number of variables in the system and prompts user to make a correction if necessary.
    
    Returns
    -------
    A list of rows in the optimization tableau

    """
    
    from ineqrowinputformat import ineqrowinputformat
    
    def delete(a):
        b=""
        return b
    
    def repl_by_eql_temp(a):
        b='eql'
        return b
    
    def repl_by_eql(a):
        b='eql'
        return b
    
    def repl_by_leq(a):
        b="<="
        return b
    
    def repl_by_geq(a):
        b=">="
        return b
    
    def repl_by_xlow(a):
        b="x"
        return b
    
    
    def forall(el,expr,f): #applies function f to each element of expr. Does NOT change expr. Be careful - if expr is made up of ints, el must be an int. If expr is made up of floats, el must be a float! Also, using forall to replace select pieces of string by ones containing the original pieces will lead to infinite loops!
        while el in expr:
            if type(expr)==list:
                for i in range(len(expr)):
                    if el==expr[i]:
                        expr=expr[0:i]+[f(el)]+expr[i+1:len(expr)]
                        break
            if type(expr)==str: #can remove multiple consecutive characters in a atring!
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
    
    
    allconstraints=input("Please enter all linear constraints, separated by commas. \n\n ---> \"x_i\", \"X_i\", \"xi\" or \"x_i\" denote the i_th variable (starting with i=1). \n ---> \"=\", \"<=\", \">=\", \"=<\" or \"=>\" are used to relate the two sides in each constraint. \n ---> Ensure that constants multiply variables only from the left and not from the right. \n ---> Multiplication signs may be omitted. \n\n      Constraints:  ")
    allconstraints=forall(" ",allconstraints,delete)
    allconstraints=forall(" ",allconstraints,delete)
    allconstraints=forall("*",allconstraints,delete)
    allconstraints=forall("(",allconstraints,delete)
    allconstraints=forall(")",allconstraints,delete)
    allconstraints=forall("X_",allconstraints,repl_by_xlow)
    allconstraints=forall("x_",allconstraints,repl_by_xlow)
    allconstraints=forall("X",allconstraints,repl_by_xlow)
    allconstraintslist=allconstraints.split(",")
    
    ConstrRows=[]
    
    for i in range(len(allconstraintslist)):
        if ("<=" not in allconstraintslist[i]) and ("=>" not in allconstraintslist[i]) and ("=<" not in allconstraintslist[i]) and (">=" not in allconstraintslist[i]):
            allconstraintslist[i]=forall("=",allconstraintslist[i],repl_by_eql_temp)
            ConstrRows=ConstrRows+[forall("eql",allconstraintslist[i],repl_by_geq)]
            ConstrRows=ConstrRows+[forall("eql",allconstraintslist[i],repl_by_leq)]
        else:
            ConstrRows=ConstrRows+[allconstraintslist[i]]
            
    ConstrRows_copy=ConstrRows[:]
    
    def xindex(mystring):
        start=first_char(mystring,"x")[1]+1
        index=mystring[start]
        mystring=mystring[start:]
        for i in range(len(mystring)):
            try: 
                index=int(mystring[0:len(mystring)-i])
                break
            except:
                continue
        return index
    
    xindeces=[]
    for i in range(len(ConstrRows_copy)):
        while first_char(ConstrRows_copy[i],"x")[0]==True:
            xindeces+=[xindex(ConstrRows_copy[i])]
            xindeces=[max(xindeces)]
            ConstrRows_copy[i]=ConstrRows_copy[i][first_char(ConstrRows_copy,"x")[1] + 1:]
            
    Nvar=max(xindeces)
        
    #old way of getting Nvar
    # maxindeces=[]
    # J=[]
    # for i in range(len(ConstrRows)):
    #     for j in range(1,100):
    #         if f"x{j}" in ConstrRows[i] or f"X{j}" in ConstrRows[i] or f"x_{j}" in ConstrRows[i] or f"X_{j}" in ConstrRows[i]:
    #             J=J+[j]
    #     maxindeces=maxindeces+[max(J)]
    # Nvar=max(maxindeces)
    
    
    print("")
    correction=input(f"Your linear optimization problem appears to have {Nvar} variables.\n\n If this number is wrong, input the correct number of variables now and press Enter. \n Otherwise, leave the answer blank and press Enter. \n\n Number of variables correction: ")
    if forall(" ",correction,delete) != "":
        Nvar=int(correction)
        
    for i in range(len(ConstrRows)):
        ConstrRows[i]=ineqrowinputformat(ConstrRows[i],Nvar)
    
    
    return (ConstrRows,Nvar)
