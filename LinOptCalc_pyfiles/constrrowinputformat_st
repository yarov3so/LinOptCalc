import streamlit as st
from ineqrowinputformat import ineqrowinputformat  # make sure this module works with Streamlit too!

def constrrowinputformat(allconstraints, correction):
    """
    Parses user-input linear constraints and returns formatted constraint rows and variable count.
    Streamlit adaptation: input fields and correction through Streamlit widgets.
    """
    
    # Helper functions (unchanged in logic)
    def delete(a): return ""

    def repl_by_eql_temp(a): return "eql"
    def repl_by_eql(a): return "eql"
    def repl_by_leq(a): return "<="
    def repl_by_geq(a): return ">="
    def repl_by_xlow(a): return "x"

    def forall(el, expr, f):
        while el in expr:
            if isinstance(expr, list):
                for i in range(len(expr)):
                    if el == expr[i]:
                        expr = expr[0:i] + [f(el)] + expr[i + 1:]
                        break
            if isinstance(expr, str):
                j = len(el)
                for i in range(len(expr)):
                    if el == expr[i:i + j]:
                        expr = expr[0:i] + f(el) + expr[i + j:]
                        break
            if isinstance(expr, tuple):
                for i in range(len(expr)):
                    if el == expr[i]:
                        expr = expr[0:i] + (f(el),) + expr[i + 1:]
                        break
        return expr

    def first_char(myexpr, char):
        verdict = False
        problem_pos = False
        for i in range(len(myexpr)):
            if myexpr[i] == char:
                verdict = True
                problem_pos = i
                break
        return (verdict, problem_pos)

    # Preprocessing user input
    allconstraints = forall(" ", allconstraints, delete)
    allconstraints = forall(" ", allconstraints, delete)
    allconstraints = forall("*", allconstraints, delete)
    allconstraints = forall("(", allconstraints, delete)
    allconstraints = forall(")", allconstraints, delete)
    allconstraints = forall("X_", allconstraints, repl_by_xlow)
    allconstraints = forall("x_", allconstraints, repl_by_xlow)
    allconstraints = forall("X", allconstraints, repl_by_xlow)
    
    allconstraintslist = allconstraints.split(",")

    ConstrRows = []

    for i in range(len(allconstraintslist)):
        if ("<=" not in allconstraintslist[i]) and ("=>" not in allconstraintslist[i]) and ("=<" not in allconstraintslist[i]) and (">=" not in allconstraintslist[i]):
            allconstraintslist[i] = forall("=", allconstraintslist[i], repl_by_eql_temp)
            ConstrRows.append(forall("eql", allconstraintslist[i], repl_by_geq))
            ConstrRows.append(forall("eql", allconstraintslist[i], repl_by_leq))
        else:
            ConstrRows.append(allconstraintslist[i])

    ConstrRows_copy = ConstrRows[:]

    def xindex(mystring):
        start = first_char(mystring, "x")[1] + 1
        index = mystring[start]
        mystring = mystring[start:]
        for i in range(len(mystring)):
            try:
                index = int(mystring[0:len(mystring) - i])
                break
            except:
                continue
        return index

    xindeces = []
    for i in range(len(ConstrRows_copy)):
        while first_char(ConstrRows_copy[i], "x")[0]:
            xindeces.append(xindex(ConstrRows_copy[i]))
            xindeces = [max(xindeces)]
            idx = first_char(ConstrRows_copy[i], "x")[1]
            ConstrRows_copy[i] = ConstrRows_copy[i][idx + 1:]

    Nvar = max(xindeces) if xindeces else 0

    # Apply correction from user input if provided
    correction_cleaned = forall(" ", correction, delete)
    if correction_cleaned != "":
        Nvar = int(correction_cleaned)

    # Process each constraint row with ineqrowinputformat
    for i in range(len(ConstrRows)):
        ConstrRows[i] = ineqrowinputformat(ConstrRows[i], Nvar)

    return ConstrRows, Nvar


# Example Streamlit UI to interact with the function
def main():
    st.title("Linear Constraints Input (Streamlit Version)")

    # Input field for constraints
    allconstraints = st.text_area(
        "Enter all linear constraints, separated by commas.",
        placeholder='e.g. x1 + 2x2 <= 5, 3x1 + x2 = 7',
        height=150
    )

    # Submit button
    if st.button("Process Constraints"):
        if not allconstraints.strip():
            st.warning("Please enter some constraints before proceeding.")
            return
        
        # First process to detect variable count
        temp_constraints, temp_nvars = constrrowinputformat(allconstraints, correction="")

        # Display variable count and request user correction if necessary
        correction = st.text_input(
            f"Detected {temp_nvars} variables. If this is incorrect, specify the correct number:",
            value=str(temp_nvars)
        )

        # Apply correction and finalize
        final_constraints, final_nvars = constrrowinputformat(allconstraints, correction)

        st.subheader("Processed Constraints")
        st.write(final_constraints)

        st.subheader("Number of Variables")
        st.write(final_nvars)


if __name__ == "__main__":
    main()
