class LogicalOperations:
    @staticmethod
    def xor_operation(bit_a, bit_b):
        return (not bit_a and bit_b) or (bit_a and not bit_b)

    @staticmethod
    def equivalence_operation(bit_a, bit_b):
        return (bit_a and bit_b) or (not bit_a and not bit_b)

    @staticmethod
    def implication_operation(bit_a, bit_b):
        return not bit_a and bit_b

    @staticmethod
    def disjunction_with_negation(bit_a, bit_b):
        return bit_a or not bit_b