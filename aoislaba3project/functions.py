def parse_expression(expr):
    expr = expr.replace(' ', '')
    expr = expr.replace('->', '>')
    expr = expr.replace('~', '=')
    return expr

def apply_operator(op, stack):
    if op == '!':
        val = stack.pop()
        stack.append(1 - val)
    else:
        b, a = stack.pop(), stack.pop()
        if op == '&':
            stack.append(a & b)
        elif op == '|':
            stack.append(a | b)
        elif op == '>':
            stack.append((1 - a) | b)
        elif op == '=':
            stack.append(1 if a == b else 0)

def get_operator_precedence(op):
    if op == '!':
        return 3
    elif op in '&|':
        return 2
    elif op in '>=':
        return 1
    return 0

def process_pending_operators(current_op, stack, op_stack):
    while (op_stack and op_stack[-1] != '(' and
           get_operator_precedence(op_stack[-1]) >= get_operator_precedence(current_op)):
        op = op_stack.pop()
        apply_operator(op, stack)

def process_closing_parenthesis(stack, op_stack):
    while op_stack and op_stack[-1] != '(':
        op = op_stack.pop()
        apply_operator(op, stack)
    if op_stack and op_stack[-1] == '(':
        op_stack.pop()

def evaluate_expression(expr, values):
    if not expr:
        return 0
    stack = []
    op_stack = []
    i = 0
    while i < len(expr):
        if expr[i] in 'abcde':
            stack.append(values.get(expr[i], 0))
        elif expr[i] == '(':
            op_stack.append(expr[i])
        elif expr[i] == ')':
            process_closing_parenthesis(stack, op_stack)
        elif expr[i] in '!&|>=':
            process_pending_operators(expr[i], stack, op_stack)
            op_stack.append(expr[i])
        i += 1
    while op_stack:
        op = op_stack.pop()
        if op != '(':
            apply_operator(op, stack)
    return stack[0] if stack else 0

def generate_combinations(variables):
    n = len(variables)
    return [[(i >> j) & 1 for j in range(n-1, -1, -1)] for i in range(2**n)]

def build_truth_table(expr, variables):
    expr = parse_expression(expr)
    if not expr and not variables:
        return [[]]
    table = []
    combinations = generate_combinations(variables)
    for comb in combinations:
        values = {var: val for var, val in zip(variables, comb)}
        result = evaluate_expression(expr, values)
        table.append(comb + [result])
    return table

def get_sdnf(table, variables):
    sdnf_terms = []
    for row in table:
        if row[-1] == 1:
            term = []
            for i, var in enumerate(variables):
                term.append(var if row[i] == 1 else f"¬{var}")
            sdnf_terms.append("(" + "&".join(term) + ")")
    return " | ".join(sdnf_terms) if sdnf_terms else "0"

def get_sknf(table, variables):
    sknf_terms = []
    for row in table:
        if row[-1] == 0:
            term = []
            for i, var in enumerate(variables):
                term.append(f"¬{var}" if row[i] == 1 else var)
            sknf_terms.append("(" + "|".join(term) + ")")
    sknf_terms.sort()
    return " & ".join(sknf_terms) if sknf_terms else "1"

def get_numeric_form_sdnf(table):
    return [i for i, row in enumerate(table) if row[-1] == 1]

def get_numeric_form_sknf(table):
    return [i for i, row in enumerate(table) if row[-1] == 0]

def get_index_form(table):
    return ''.join(str(row[-1]) for row in table)

def glue_terms(term1, term2, variables="abcde", is_dnf=True):
    bin1 = ""
    bin2 = ""
    for var in variables:
        if f"¬{var}" in term1:
            bin1 += "0"
        elif var in term1:
            bin1 += "1"
        else:
            bin1 += "X"
        if f"¬{var}" in term2:
            bin2 += "0"
        elif var in term2:
            bin2 += "1"
        else:
            bin2 += "X"

    diff = 0
    result_bin = ""
    for b1, b2 in zip(bin1, bin2):
        if b1 == b2:
            result_bin += b1
        else:
            diff += 1
            result_bin += "X"
        if diff > 1:
            return None

    if diff != 1:
        return None

    result = []
    for i, val in enumerate(result_bin):
        if val == "1":
            result.append(variables[i])
        elif val == "0":
            result.append(f"¬{variables[i]}")
    separator = "&" if is_dnf else "|"
    return separator.join(result) if result else None

def evaluate_term(term, row, variables, is_dnf=True):
    if term == "1" and is_dnf:
        return row[-1] == 1
    if term == "0" and not is_dnf:
        return row[-1] == 0
    separator = "&" if is_dnf else "|"
    term_vars = term.strip("()").split(separator)
    if is_dnf:
        for var in term_vars:
            var_name = var[1:] if var.startswith("¬") else var
            var_val = 0 if var.startswith("¬") else 1
            try:
                var_idx = variables.index(var_name)
            except ValueError:
                return False
            if row[var_idx] != var_val:
                return False
        return True
    else:
        for var in term_vars:
            var_name = var[1:] if var.startswith("¬") else var
            var_val = 0 if var.startswith("¬") else 1
            try:
                var_idx = variables.index(var_name)
            except ValueError:
                continue
            if row[var_idx] == var_val:
                return True
        return False

def minimize_calculation(terms, table, variables, is_dnf=True):
    stages = []
    current_terms = [t.strip("()") for t in terms]
    if is_dnf:
        term_coverage = {t: set(i for i, row in enumerate(table) if evaluate_term(t, row, variables, is_dnf)) for t in current_terms}
        target_rows = set(i for i, row in enumerate(table) if row[-1] == 1)
    else:
        term_coverage = {t: set(i for i, row in enumerate(table) if not evaluate_term(t, row, variables, is_dnf)) for t in current_terms}
        target_rows = set(i for i, row in enumerate(table) if row[-1] == 0)
    
    while True:
        new_terms = []
        new_coverage = {}
        used = set()
        stage = []
        
        for i, term1 in enumerate(current_terms):
            for term2 in current_terms[i+1:]:
                glued = glue_terms(term1, term2, variables="".join(variables), is_dnf=is_dnf)
                if glued:
                    if is_dnf:
                        glued_coverage = set(i for i, row in enumerate(table) if evaluate_term(glued, row, variables, is_dnf))
                    else:
                        glued_coverage = set(i for i, row in enumerate(table) if not evaluate_term(glued, row, variables, is_dnf))
                    if glued_coverage.issubset(target_rows):
                        stage.append(f"({term1}) ∨ ({term2}) => ({glued})")
                        if glued not in new_terms:
                            new_terms.append(glued)
                        used.add(term1)
                        used.add(term2)
                        new_coverage[glued] = glued_coverage
        
        for term in current_terms:
            if term not in used:
                new_terms.append(term)
                new_coverage[term] = term_coverage[term]
        
        stages.append(stage)
        if not stage:
            break
        current_terms = new_terms
        term_coverage = new_coverage
    
    essential_terms = []
    covered_rows = set()
    for term in current_terms:
        unique_rows = term_coverage[term] - covered_rows
        if unique_rows:
            essential_terms.append(term)
            covered_rows.update(term_coverage[term])
    
    return essential_terms, stages, term_coverage

def remove_redundant_implicants(terms, table, variables, coverage, is_dnf=True):
    target_rows = set(i for i, row in enumerate(table) if row[-1] == (1 if is_dnf else 0))
    essential = []
    covered_rows = set()
    
    for row in target_rows:
        covering_terms = [t for t in terms if row in coverage[t]]
        if len(covering_terms) == 1:
            term = covering_terms[0]
            if term not in essential:
                essential.append(term)
                covered_rows.update(coverage[term])
    
    remaining_rows = target_rows - covered_rows
    while remaining_rows:
        best_term = None
        max_coverage = 0
        min_size = float('inf')
        for term in terms:
            if term not in essential:
                coverage_count = len(coverage[term].intersection(remaining_rows))
                term_size = len(term.split("&" if is_dnf else "|"))
                if coverage_count > max_coverage or (coverage_count == max_coverage and term_size < min_size):
                    max_coverage = coverage_count
                    min_size = term_size
                    best_term = term
        if best_term:
            essential.append(best_term)
            covered_rows.update(coverage[best_term])
            remaining_rows = target_rows - covered_rows
        else:
            break
    
    return sorted(essential, key=lambda x: len(x))

def build_coverage_table(terms, table, variables, is_dnf=True):
    target_rows = [i for i, row in enumerate(table) if row[-1] == (1 if is_dnf else 0)]
    # Header row with tuples like (0,1)
    table_str = ["  " + " ".join(f"({','.join(str(x) for x in table[i][:-1])})" for i in target_rows)]
    # Find the maximum term length for padding
    max_term_length = max(len(term) for term in terms) if terms else 1
    for term in terms:
        row = [f"{term:<{max_term_length}}"]  # Left-align term with padding
        for row_idx in target_rows:
            match = evaluate_term(term, table[row_idx], variables, is_dnf)
            # Pad each cell to 4 characters to match header tuple width
            row.append("  X  " if match else "     ")
        table_str.append(" ".join(row))
    return "\n".join(table_str)

def build_karnaugh_map(table, variables):
    n = len(variables)
    if n not in [2, 3, 4]:
        return f"Карта Карно поддерживается только для 2-4 переменных, получено {n}."
    
    if n == 2:
        map_str = [f"{variables[1]}\\{variables[0]} 0 1"]
        for a in [0, 1]:
            row = [f"{a}   "]
            for b in [0, 1]:
                rows = [r for r in table if r[:2] == [a, b]]
                idx = rows[0][-1] if rows else 0
                row.append(str(idx))
            map_str.append(" ".join(row))
        return "\n".join(map_str)
    
    elif n == 3:
        map_str = [f"{variables[1]}{variables[2]}\\{variables[0]} 00 01 11 10"]
        for a in [0, 1]:
            row = [f"{a}   "]
            for b, c in [(0, 0), (0, 1), (1, 1), (1, 0)]:
                rows = [r for r in table if r[:3] == [a, b, c]]
                idx = rows[0][-1] if rows else 0
                row.append(str(idx))
            map_str.append(" ".join(row))
        return "\n".join(map_str)
    
    elif n == 4:
        map_str = [f"{variables[2]}{variables[3]}\\{variables[0]}{variables[1]} 00 01 11 10"]
        for a, b in [(0, 0), (0, 1), (1, 1), (1, 0)]:
            row = [f"{a}{b} "]
            for c, d in [(0, 0), (0, 1), (1, 1), (1, 0)]:
                rows = [r for r in table if r[:4] == [a, b, c, d]]
                idx = rows[0][-1] if rows else 0
                row.append(str(idx))
            map_str.append(" ".join(row))
        return "\n".join(map_str)
    

def minimize_karnaugh(term, table, variables, is_dnf=True):
    n = len(variables)
    if n not in [2, 3, 4]:
        return f"Карта Карно реализована только для 2-4 переменных, получено {n}.", []
    
    target_val = 1 if is_dnf else 0
    terms = []
    target_rows = set(i for i, row in enumerate(table) if row[-1] == target_val)
    
    def is_target(vals):
        for row in table:
            if row[:-1] == vals:
                return row[-1] == target_val
        return False
    
    def get_coverage(term):
        if is_dnf:
            return set(i for i, row in enumerate(table) if evaluate_term(term, row, variables, is_dnf))
        else:
            return set(i for i, row in enumerate(table) if not evaluate_term(term, row, variables, is_dnf))
    
    if n == 3:
        if not is_dnf:  # SKNF: group 0s
            # Group of 4: all cells where c=0
            if all(is_target([a, b, 0]) for a in [0, 1] for b in [0, 1]):
                terms.append("(c)")
            
            # Groups of 2
            # a=1, b=0 (covers [1,0,0] and [1,0,1])
            if all(is_target([1, 0, c]) for c in [0, 1]):
                terms.append("(¬a|b)")
            # a=0, c=0 (covers [0,0,0] and [0,1,0])
            if all(is_target([0, b, 0]) for b in [0, 1]):
                terms.append("(a|c)")
            # b=1, c=0 (covers [0,1,0] and [1,1,0])
            if all(is_target([a, 1, 0]) for a in [0, 1]):
                terms.append("(¬b|c)")
            # b=0, c=1 (covers [0,0,1] and [1,0,1]) - not a group here, as [0,0,1]=1
            
        else:  # SDNF: group 1s (unchanged)
            for a in [0, 1]:
                if all(is_target([a, b, c]) for b in [0, 1] for c in [0, 1]):
                    terms.append(f"{'¬' if a == 0 else ''}{variables[0]}")
            for b in [0, 1]:
                if all(is_target([a, b, c]) for a in [0, 1] for c in [0, 1]):
                    terms.append(f"{'¬' if b == 0 else ''}{variables[1]}")
            for c in [0, 1]:
                if all(is_target([a, b, c]) for a in [0, 1] for b in [0, 1]):
                    terms.append(f"{'¬' if c == 0 else ''}{variables[2]}")
            for a, b in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if all(is_target([a, b, c]) for c in [0, 1]):
                    terms.append(f"{'¬' if a == 0 else ''}{variables[0]}&{'¬' if b == 0 else ''}{variables[1]}")
            for a, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if all(is_target([a, b, c]) for b in [0, 1]):
                    terms.append(f"{'¬' if a == 0 else ''}{variables[0]}&{'¬' if c == 0 else ''}{variables[2]}")
            for b, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if all(is_target([a, b, c]) for a in [0, 1]):
                    terms.append(f"{'¬' if b == 0 else ''}{variables[1]}&{'¬' if c == 0 else ''}{variables[2]}")
    
    # Select minimal terms
    term_coverage = {t: get_coverage(t) for t in terms}
    essential_terms = []
    covered_rows = set()
    
    # Essential prime implicants
    for row in target_rows:
        covering_terms = [t for t, cov in term_coverage.items() if row in cov]
        if len(covering_terms) == 1:
            term = covering_terms[0]
            if term not in essential_terms:
                essential_terms.append(term)
                covered_rows.update(term_coverage[term])
    
    # Cover remaining rows
    remaining_rows = target_rows - covered_rows
    while remaining_rows:
        best_term = None
        max_coverage = 0
        for term, cov in term_coverage.items():
            if term not in essential_terms:
                coverage_count = len(cov & remaining_rows)
                if coverage_count > max_coverage:
                    max_coverage = coverage_count
                    best_term = term
        if best_term:
            essential_terms.append(best_term)
            covered_rows.update(term_coverage[best_term])
            remaining_rows = target_rows - covered_rows
        else:
            break
    essential_terms,a,b = minimize_calculation(term, table,variables,is_dnf)
    return build_karnaugh_map(table, variables), essential_terms

