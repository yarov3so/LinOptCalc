import streamlit as st
from objrowinputformat_st import objrowinputformat
from constrrowinputformat_st import constrrowinputformat

# Supporting functions
def delete(a):
    return ""

def forall(el, expr, f):
    while el in expr:
        if type(expr) == list:
            for i in range(len(expr)):
                if el == expr[i]:
                    expr = expr[0:i] + [f(el)] + expr[i + 1:]
                    break
        if type(expr) == str:
            j = len(el)
            for i in range(len(expr)):
                if el == expr[i:i + j]:
                    expr = expr[0:i] + f(el) + expr[i + j:]
                    break
        if type(expr) == tuple:
            for i in range(len(expr)):
                if el == expr[i]:
                    expr = expr[0:i] + (f(el),) + expr[i + 1:]
                    break
    return expr

# Main optimization function
def linear_optimization():
    st.title("Linear Optimization Calculator")

    problem = st.radio(
        "Choose problem type:",
        ('max', 'min')
    )
    
    # Ask for input for objective function and constraints
    Nvar = st.number_input("Number of variables:", min_value=1, value=2)
    ConstrRows_tuple = constrrowinputformat()
    ConstrRows = ConstrRows_tuple[0]
    Nconstr = len(ConstrRows)

    # Introduce slack variables
    slackvars = ", ".join([f"x_{i+1}" for i in range(Nvar, Nconstr + Nvar)])
    st.write(f"Introducing slack variables: {slackvars}")

    PreObjList = st.text_input("Please enter the algebraic expression of the objective function:")
    
    if PreObjList == "":
        st.warning("Please enter an objective function.")
        return

    PreObjList = objrowinputformat(PreObjList, Nvar)
    if problem == "max":
        PreObjList = [-x for x in PreObjList]

    ObjRow = PreObjList + [0.0] * Nconstr + [1.0] + [0.0]
    
    # Set up the tableau
    for i in range(Nconstr):
        ConstrRows[i] = ConstrRows[i][0:len(ConstrRows[i])-1] + [1.0 if i == j else 0.0 for j in range(Nconstr)] + [ConstrRows[i][-1]]
    
    # Display the tableau
    st.write("The following tableau was registered:")
    for i in range(Nconstr):
        st.write(f"Constraint Row #{i+1}: {ConstrRows[i][0:len(ConstrRows[i])-1]} | {ConstrRows[i][-1]}")
    
    st.write(f"Objective Row: {ObjRow[0:len(ObjRow)-1]} | {ObjRow[-1]}")

    # Start optimization logic (simplex)
    constants = [ConstrRows[i][-1] for i in range(Nconstr)]
    
    # Check if feasible region exists (simplex steps can go here)
    a, b = neg_entry(constants)
    
    if a:
        st.write("The linear system's feasible region is empty.")
        return
    
    # Begin Simplex iterations 
    while neg_entry(constants)[0]:
        colindex = neg_entry([ConstrRows[b][i] for i in range(len(ConstrRows[0])-1)])[1]
        column_interest = [ConstrRows[i][colindex] for i in range(Nconstr)]
        ratiolist = [constants[i] / column_interest[i] if column_interest[i] != 0 else 0.0 for i in range(Nconstr)]
        
        rowindex = ratiolist.index(min(ratiolist))
        ConstrRows[rowindex] = [x / column_interest[rowindex] for x in ConstrRows[rowindex]]
        
        st.write(f"Pivoting on entry ({rowindex+1}, {colindex+1}):")
        for i in range(Nconstr):
            if i != rowindex:
                ConstrRows[i] = [x - ConstrRows[i][colindex] * y for x, y in zip(ConstrRows[i], ConstrRows[rowindex])]
        
        # Display current tableau
        for i in range(Nconstr):
            st.write(f"Constraint Row #{i+1}: {ConstrRows[i][0:len(ConstrRows[i])-1]} | {ConstrRows[i][-1]}")
        st.write(f"Objective Row: {ConstrRows[-1][0:len(ObjRow)-1]} | {ConstrRows[-1][-1]}")

# Helper functions
def neg_entry(mylist):
    for i in range(len(mylist)):
        if mylist[i] < 0:
            return True, i
    return False, False

# Run the app
if __name__ == "__main__":
    linear_optimization()
