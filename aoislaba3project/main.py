from functions import *
def main():
    try:
        expr = input("Введите логическую функцию (переменные a,b,c,d,e; операции &,|,!,->): ")
    except EOFError:
        print("Ввод отсутствует. Используется выражение по умолчанию: '!(!a->!b)|c'")
        expr = "!(!a->!b)|c"
    
    variables = sorted(set(c for c in expr if c in 'abcde'))
    if not variables or len(variables) > 5:
        print("Ошибка: должно быть до 5 переменных (a,b,c,d,e).")
        return
    
    table = build_truth_table(expr, variables)
    
    print("\nПолная таблица истинности:")
    print(" ".join(variables + ["F"]))
    for row in table:
        print(" ".join(str(x) for x in row))
    
    sdnf = get_sdnf(table, variables)
    sknf = get_sknf(table, variables)
    print("\nИсходная СДНФ:", sdnf)
    print("Исходная СКНФ:", sknf)
    
    print("\nМинимизация СДНФ расчетным методом:")
    sdnf_terms = [term for term in sdnf.split(" | ") if term != "0"]
    min_terms, stages, coverage = minimize_calculation(sdnf_terms, table, variables, is_dnf=True)
    for i, stage in enumerate(stages, 1):
        if stage:
            print(f"Этап склеивания {i}:")
            for s in stage:
                print(s)
    print("Результат после склеивания:", " | ".join(f"({t})" for t in min_terms) if min_terms else "0")
    min_terms = remove_redundant_implicants(min_terms, table, variables, coverage, is_dnf=True)
    print("Минимизированная СДНФ:", " | ".join(min_terms) if min_terms else "0")
    
    print("\nМинимизация СКНФ расчетным методом:")
    sknf_terms = [term for term in sknf.split(" & ") if term != "1"]
    min_terms, stages, coverage = minimize_calculation(sknf_terms, table, variables, is_dnf=False)
    for i, stage in enumerate(stages, 1):
        if stage:
            print(f"Этап склеивания {i}:")
            for s in stage:
                print(s)
    print("Результат после склеивания:", " & ".join(f"({t})" for t in min_terms) if min_terms else "1")
    min_terms = remove_redundant_implicants(min_terms, table, variables, coverage, is_dnf=False)
    print("Минимизированная СКНФ:", " & ".join(f"({t})" for t in min_terms) if min_terms else "1")
    
    print("\nМинимизация СДНФ расчетно-табличным методом:")
    sdnf_terms = [term for term in sdnf.split(" | ") if term != "0"]
    min_terms, stages, coverage = minimize_calculation(sdnf_terms, table, variables, is_dnf=True)
    for i, stage in enumerate(stages, 1):
        if stage:
            print(f"Этап склеивания {i}:")
            for s in stage:
                print(s)
    print("Результат после склеивания:", " | ".join(f"({t})" for t in min_terms) if min_terms else "0")
    print("Таблица покрытия:")
    print(build_coverage_table(min_terms, table, variables, is_dnf=True))
    min_terms = remove_redundant_implicants(min_terms, table, variables, coverage, is_dnf=True)
    print("Минимизированная СДНФ:", " | ".join(min_terms) if min_terms else "0")
    
    print("\nМинимизация СКНФ расчетно-табличным методом:")
    sknf_terms = [term for term in sknf.split(" & ") if term != "1"]
    min_terms, stages, coverage = minimize_calculation(sknf_terms, table, variables, is_dnf=False)
    for i, stage in enumerate(stages, 1):
        if stage:
            print(f"Этап склеивания {i}:")
            for s in stage:
                print(s)
    print("Результат после склеивания:", " & ".join(f"({t})" for t in min_terms) if min_terms else "1")
    print("Таблица покрытия:")
    print(build_coverage_table(min_terms, table, variables, is_dnf=False))
    min_terms = remove_redundant_implicants(min_terms, table, variables, coverage, is_dnf=False)
    print("Минимизированная СКНФ:", " & ".join(f"({t})" for t in min_terms) if min_terms else "1")
    
    print("\nМинимизация СДНФ табличным методом (карта Карно):")
    karnaugh_map, min_terms = minimize_karnaugh(sdnf_terms,table, variables, is_dnf=True)
    print(karnaugh_map)
    print("Минимизированная СДНФ:", " | ".join(min_terms) if min_terms else "0")

    print("\nМинимизация СКНФ табличным методом (карта Карно):")
    karnaugh_map, min_terms = minimize_karnaugh(sknf_terms,table, variables, is_dnf=False)
    print(karnaugh_map)
    print("Минимизированная СКНФ:", " & ".join(min_terms) if min_terms else "1")

if __name__ == "__main__":
    main()