# timer 0, 1, ..., 15, 0
from bin_functions import decimal_to_binary
from minimization import bits_to_term, minimize_chart

states_bin = [decimal_to_binary(i).zfill(4) for i in range(0,16)]
clock = [str(i % 2) for i in range(0, 32)]

digit1_excitation = ['1' if i % 2 == 0 else '0' for i in range(1, 33)]
digit2_excitation = ['1' if i % 4 == 0 else '0' for i in range(1, 33)]
digit3_excitation = ['1' if i % 8 == 0 else '0' for i in range(1, 33)]
digit4_excitation = ['1' if i % 16 == 0 else '0' for i in range(1, 33)]


excitation_table_digit4 = {states_bin[i // 2] + clock[i] : digit4_excitation[i] for i in range(0, 32)}
excitation_table_digit3 = {states_bin[i // 2] + clock[i] : digit3_excitation[i] for i in range(0, 32)}
excitation_table_digit2 = {states_bin[i // 2] + clock[i] : digit2_excitation[i] for i in range(0, 32)}
excitation_table_digit1 = {states_bin[i // 2] + clock[i] : digit1_excitation[i] for i in range(0, 32)}


excitation_digit4_terms = [key for key, value in excitation_table_digit4.items() if value == '1']
excitation_digit3_terms = [key for key, value in excitation_table_digit3.items() if value == '1']
excitation_digit2_terms = [key for key, value in excitation_table_digit2.items() if value == '1']
excitation_digit1_terms = [key for key, value in excitation_table_digit1.items() if value == '1']

variables = ['A', 'B', 'C', 'D', 'V']
excitation_digit4_pdnf = ' | '.join(bits_to_term(i, variables) for i in excitation_digit4_terms)
excitation_digit3_pdnf = ' | '.join(bits_to_term(i, variables) for i in excitation_digit3_terms)
excitation_digit2_pdnf = ' | '.join(bits_to_term(i, variables) for i in excitation_digit2_terms)
excitation_digit1_pdnf = ' | '.join(bits_to_term(i, variables) for i in excitation_digit1_terms)

excitation_digit4_minimized = minimize_chart(excitation_digit4_pdnf)
excitation_digit3_minimized = minimize_chart(excitation_digit3_pdnf)
excitation_digit2_minimized = minimize_chart(excitation_digit2_pdnf)
excitation_digit1_minimized = minimize_chart(excitation_digit1_pdnf)

print("СДНФ для таймера (1 цифра, от высшего разряда к низшему):")
print(f"Для разряда 4: {excitation_digit4_minimized}")
print(f"Для разряда 3: {excitation_digit3_minimized}")
print(f"Для разряда 2: {excitation_digit2_minimized}")
print(f"Для разряда 1: {excitation_digit1_minimized}")