def objrowinputformat(expr, nvar):
    """
    Parses an algebraic expression into a list of variable coefficients.

    Parameters
    ----------
    expr : str
        Algebraic expression, e.g., "20x1 + 8X_3 -2x_1 - x_4"
    nvar : int
        Number of variables in the optimization problem.

    Returns
    -------
    exprlist : list of floats
        Coefficients sorted by variable index.
    """

    # Clean up and standardize the expression
    expr = expr.replace(" ", "").replace("*", "").replace("(", "").replace(")", "")
    expr = expr.replace("X_", "x").replace("x_", "x").replace("X", "x")
    expr = expr.replace("++", "+").replace("--", "+").replace("+-", "-").replace("-+", "-")
    
    # Insert missing 1 multipliers
    expr = expr.replace("+x", "+1x").replace("-x", "-1x")

    # Ensure the first term has a sign and coefficient
    if expr and expr[0] == "x":
        expr = "+1" + expr
    if expr and expr[0] not in "+-":
        expr = "+" + expr

    # Helper to find first occurrence of a character
    def first_char(s, char):
        for idx, c in enumerate(s):
            if c == char:
                return True, idx
        return False, None

    # Helper to find the next '+' or '-' after the first sign
    def second_sign(s):
        after_first = s[1:]
        plus_pos = after_first.find('+')
        minus_pos = after_first.find('-')

        if plus_pos == -1:
            return minus_pos + 1 if minus_pos != -1 else len(s)
        if minus_pos == -1:
            return plus_pos + 1 if plus_pos != -1 else len(s)
        
        return min(plus_pos, minus_pos) + 1

    # Initialize the list of coefficients
    exprlist = [0.0] * nvar

    # Parse the expression
    while True:
        has_x, x_pos = first_char(expr, "x")
        if not has_x:
            break

        # Get the variable index
        var_start = x_pos + 1
        next_sign = second_sign(expr)

        var_end = next_sign if next_sign > var_start else len(expr)
        var_idx_str = expr[var_start:var_end]
        
        try:
            var_idx = int(var_idx_str) - 1  # Convert to zero-based index
        except ValueError:
            var_idx = None

        # Get the coefficient
        coeff_str = expr[:x_pos]
        coeff = float(eval(coeff_str)) if coeff_str else 0.0

        if var_idx is not None and 0 <= var_idx < nvar:
            exprlist[var_idx] += coeff

        # Move to the rest of the expression
        expr = expr[next_sign:] if next_sign < len(expr) else ""

    return exprlist
