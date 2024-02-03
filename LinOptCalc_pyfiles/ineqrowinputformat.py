#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:23:57 2023

@author: yarov3so
"""
def ineqrowinputformat(expr,nvar):
    """

    Parameters
    ----------
    expr : And algebraic expression in which the LHS and RHS are 
           related via <= or >= (the function will also take =<,>=). Example of a valid 
           expression for nvar=4:  20x1 + 8X_3 -2x_1 - x_4 >= 10x3 -1 (notationally very liberal...)
    nvar : number of variables in the optimization problem

    Returns
    -------
    exprlist: list with weights of variables sorted into appropriate positions, 
              as well as the constant bound in the last entry. The list is phrased as a <= inequality.

    """

    #Here come a bitch load of tiny functions
    
    def remove(i):
        if type(i)==str:
            i=""
        if type(i)==tuple:
            i=()
        return i
    
    def remove_tup(i):
        i=()
        return i
    
    def repl_by_comma(a):
        b=","
        return b
    def repl_by_xlow(a):
        b="x"
        return b
    
    def repl_by_pl1(a):
        b="+1x"
        return b
    def repl_by_min1(a):
        b="-1x"
        return b
    
    def repl_by_pl(a):
        b="+"
        return b
    def repl_by_min(a):
        b="-"
        return b
    
    def repl_by_geqpl(a):
        b='> =+'
        return b
    
    def repl_by_leqpl(a):
        b='< =+'
        return b
    
    def repl_by_temppls(a):
        b='temppls'
        return b
    
    def repl_by_tempmin(a):
        b='tempmin'
        return b
    
    def repl_by_leq(a):
        b="<="
        return b
    
    def repl_by_geq(a):
        b=">="
        return b
    
    def delete(a):
        b=""
        return b
    
    
    #The functions above will be used in conjunction with the following powerful function:
    
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
    
    
    #initial cleanup
    expr=forall(" ",expr,delete)
    expr=forall("*",expr,delete)
    expr=forall("(",expr,delete)
    expr=forall(")",expr,delete)
    expr=forall("X_",expr,repl_by_xlow)
    expr=forall("x_",expr,repl_by_xlow)
    expr=forall("X",expr,repl_by_xlow)
    expr=forall("++",expr,repl_by_pl)
    expr=forall("--",expr,repl_by_pl)
    expr=forall("+-",expr,repl_by_min)
    expr=forall("-+",expr,repl_by_min)
    expr=forall("++",expr,repl_by_pl)
    expr=forall("--",expr,repl_by_pl)
    expr=forall("=>",expr,repl_by_geq)
    expr=forall("=<",expr,repl_by_leq)
    
    #accounting for the missing sign of the constant term and missing 1 multiples
    if ("<=-" not in expr) and (">=-" not in expr):
        expr=forall("<=",expr,repl_by_leqpl)
        expr=forall(">=",expr,repl_by_geqpl)
    expr=forall(" ",expr,delete)
    expr=forall("+x",expr,repl_by_pl1)
    expr=forall("-x",expr,repl_by_min1)
    
    #accounting for possible missing sign of the first term and possible missing constant multiple 1 of the first term
    if expr[0] == "x":
        expr="+1"+expr
    if expr[0] != "+" and expr[0] != "-" :
        expr="+"+expr
        
    #inverting the inequality
    if ">="  in expr:
        expr=forall("+",expr,repl_by_tempmin)
        expr=forall("-",expr,repl_by_temppls)
        expr=forall("tempmin",expr,repl_by_min)
        expr=forall("temppls",expr,repl_by_pl)
        expr=forall(">=",expr,repl_by_leq)

    
    #Now we populate exprlist with the correct constants plucked from expr
    
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
    
    eqpos=first_char(expr,"=")[1]
    expr_lhs=expr[0:eqpos-1]
    expr_rhs=expr[eqpos+1:]
    exprlist=[0 for i in range(nvar+1)]
    
    def second_sign(expr_lhs):
        
        second_min=first_char(expr_lhs[1:len(expr_lhs)],"-")[1]+1
        second_plus=first_char(expr_lhs[1:len(expr_lhs)],"+")[1]+1
        second_sign=min(second_min,second_plus)
        if second_min==1 and second_plus==1:
            second_sign=1
        if second_min==1 or second_plus==1:
            second_sign=max(second_min,second_plus)
        return second_sign
    
    
    while first_char(expr_lhs,"x")[0]==True and second_sign(expr_lhs)>1:
        if "x" in expr_lhs[0:second_sign(expr_lhs)]:
            exprlist[int(expr_lhs[first_char(expr_lhs,"x")[1] + 1:second_sign(expr_lhs)])-1]+=float(eval(expr_lhs[0:first_char(expr_lhs,"x")[1]]))
            expr_lhs=expr_lhs[second_sign(expr_lhs):]
            
        else:
            exprlist[nvar]+=float(-eval(expr_lhs[0:second_sign(expr_lhs)]))
            expr_lhs=expr_lhs[second_sign(expr_lhs):]
            
    if "x" in expr_lhs:
        exprlist[int(expr_lhs[expr_lhs.index("x")+1:])-1]+=float(eval(expr_lhs[0:expr_lhs.index("x")]))
    else:
        exprlist[nvar]+=float(-eval(expr_lhs))

        
    while first_char(expr_rhs,"x")[0]==True and second_sign(expr_rhs)>1:
        if "x" in expr_rhs[0:second_sign(expr_rhs)]:
            exprlist[int(expr_rhs[first_char(expr_rhs,"x")[1] + 1:second_sign(expr_rhs)])-1]+=float(-eval(expr_rhs[0:first_char(expr_rhs,"x")[1]]))
            expr_rhs=expr_rhs[second_sign(expr_rhs):]
            
        else:
            exprlist[nvar]+=float(eval(expr_rhs[0:second_sign(expr_rhs)]))
            expr_rhs=expr_rhs[second_sign(expr_rhs):]
            
    if "x" in expr_rhs:
        exprlist[int(expr_rhs[expr_rhs.index("x")+1:])-1]+=float(-eval(expr_rhs[0:expr_rhs.index("x")]))
    else:
        exprlist[nvar]+=float(eval(expr_rhs))
    
    
    return exprlist

