from hash_utils import format_entry

class HashTable:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.item_count = 0
        self.entries = [None] * capacity
        self.entry_values = [None] * capacity
        self.removed_markers = [False] * capacity

    def _calculate_hash(self, entry_key):
        hash_result = 0
        for idx, character in enumerate(str(entry_key)):
            hash_result += (idx + 1) * ord(character)
        return hash_result % self.capacity

    def _find_slot(self, initial_hash, attempt):
        return (initial_hash + attempt) % self.capacity

    def _expand_table(self):
        old_entries = self.entries
        old_values = self.entry_values
        old_markers = self.removed_markers
        self.capacity *= 2
        self.item_count = 0
        self.entries = [None] * self.capacity
        self.entry_values = [None] * self.capacity
        self.removed_markers = [False] * self.capacity
        for key, value, marker in zip(old_entries, old_values, old_markers):
            if key is not None and not marker:
                self.insert(key, value)

    def insert(self, entry_key, entry_value):
        if self.item_count / self.capacity > 0.6:
            self._expand_table()

        hash_idx = self._calculate_hash(entry_key)
        attempt = 0
        step = 1
        while True:
            position = self._find_slot(hash_idx, attempt)
            if self.entries[position] is None or self.removed_markers[position]:
                self.entries[position] = entry_key
                self.entry_values[position] = entry_value
                self.removed_markers[position] = False
                self.item_count += 1
                return
            elif self.entries[position] == entry_key and not self.removed_markers[position]:
                print(f"Entry '{entry_key}' already exists.")
                return
            attempt += step
            step += 1
            if attempt >= self.capacity:
                self._expand_table()
                hash_idx = self._calculate_hash(entry_key)
                attempt = 0
                step = 1

    def retrieve(self, entry_key):
        hash_idx = self._calculate_hash(entry_key)
        attempt = 0
        step = 1
        while True:
            position = self._find_slot(hash_idx, attempt)
            current_key = self.entries[position]
            if current_key is None:
                return None
            if current_key == entry_key and not self.removed_markers[position]:
                return self.entry_values[position]
            attempt += step
            step += 1

    def remove(self, entry_key):
        hash_idx = self._calculate_hash(entry_key)
        attempt = 0
        step = 1
        while self.entries[self._find_slot(hash_idx, attempt)] is not None:
            position = self._find_slot(hash_idx, attempt)
            if self.entries[position] == entry_key and not self.removed_markers[position]:
                self.removed_markers[position] = True
                self.entry_values[position] = None
                self.item_count -= 1
                return True
            attempt += step
            step += 1
        return False

    def __str__(self):
        return '\n'.join([
            format_entry(self, key)
            for key, marker in zip(self.entries, self.removed_markers)
            if key is not None and not marker
        ])

def create_table_from_dict(data_dict):
    table = HashTable()
    for key, value in data_dict.items():
        table.insert(key, value)
    return table