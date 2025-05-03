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
                term.append(var if row[i] == 1 else f"!{var}")
            sdnf_terms.append("(" + "&".join(term) + ")")
    return " | ".join(sdnf_terms) if sdnf_terms else "0"

def get_sknf(table, variables):
    sknf_terms = []
    for row in table:
        if row[-1] == 0:
            term = []
            for i, var in enumerate(variables):
                term.append(f"!{var}" if row[i] == 1 else var)
            sknf_terms.append("(" + "|".join(term) + ")")
    sknf_terms.sort()  # Сортировка терминов для предсказуемого порядка
    return " & ".join(sknf_terms) if sknf_terms else "1"

def get_numeric_form_sdnf(table):
    return [i for i, row in enumerate(table) if row[-1] == 1]

def get_numeric_form_sknf(table):
    return [i for i, row in enumerate(table) if row[-1] == 0]

def get_index_form(table):
    return ''.join(str(row[-1]) for row in table)

def main():
    try:
        expr = input("Введите логическую функцию (переменные a,b,c,d,e; операции &,|,!,->,~): ")
    except EOFError:
        print("Ввод отсутствует. Используется выражение по умолчанию: '!a & b'")
        expr = "!a & b"
    
    variables = sorted(set(c for c in expr if c in 'abcde'))
    if not variables or len(variables) > 5:
        print("Ошибка: должно быть до 5 переменных (a,b,c,d,e).")
        return
    
    table = build_truth_table(expr, variables)
    
    print("\nПолная таблица истинности:")
    print(" ".join(variables + ["F"]))
    for row in table:
        print(" ".join(str(x) for x in row))
    
    print("\nСДНФ:", get_sdnf(table, variables))
    print("СКНФ:", get_sknf(table, variables))
    
    print("\nЧисловая форма СДНФ:", get_numeric_form_sdnf(table))
    print("Числовая форма СКНФ:", get_numeric_form_sknf(table))
    
    print("Индексная форма:", get_index_form(table))

if __name__ == "__main__":
    main()