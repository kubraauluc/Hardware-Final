İmpelementation


# ==========================================
# MEMORY BLOCK (Linked List Node)
# ==========================================
class Block:
    def __init__(self, start_address, size, is_free=True):
        self.start_address = start_address
        self.size = size
        self.is_free = is_free  # True means Empty, False means Used
        self.next_block = None  # Pointer to the next block


# ==========================================
# MEMORY MANAGER (Linked List Implementation)
# ==========================================
class MemoryManager:
    def __init__(self, total_size):
        # We start with one big empty block covering the whole memory
        self.head = Block(0, total_size, True)

        # For Next Fit, we need to remember where we stopped last time
        self.last_alloc_ptr = self.head

    # --- HELPER: To see what's happening inside ---
    def print_status(self):
        current = self.head
        print("Memory Map: ", end="")
        while current:
            status = "FREE" if current.is_free else "USED"
            print(f"[{status} | Addr:{current.start_address} | Size:{current.size}] -> ", end="")
            current = current.next_block
        print("END")
        print("-" * 50)

    # --- HELPER: Splitting a block (Used by all algorithms) ---
    def split_block(self, block, request_size):
        # We calculate how much space is left after allocation
        remaining_size = block.size - request_size

        # We update the current block to be 'USED'
        block.size = request_size
        block.is_free = False

        # If there is remaining space, we create a new free block next to it
        if remaining_size > 0:
            new_address = block.start_address + request_size
            new_block = Block(new_address, remaining_size, True)

            # We link the new block into the list
            new_block.next_block = block.next_block
            block.next_block = new_block

            # Important for Next Fit: Update pointer if needed
            if self.last_alloc_ptr == block:
                self.last_alloc_ptr = new_block

        print(f"SUCCESS: Allocated {request_size} units at Address {block.start_address}")

    # ==========================================
    # 1. BEST FIT (En İyi Uyan)
    # Strategy: Scan the WHOLE list. Find the SMALLEST free block
    # that is big enough. This minimizes wasted leftover space.
    # ==========================================
    def allocate_best_fit(self, size):
        current = self.head
        best_block = None

        # We search through every block
        while current:
            if current.is_free and current.size >= size:
                # If we haven't found a candidate yet OR this one is smaller (tighter fit)
                if best_block is None or current.size < best_block.size:
                    best_block = current

            current = current.next_block

        # If we found a suitable block, we use it
        if best_block:
            self.split_block(best_block, size)
            return

        print(f"FAIL: Best Fit could not find space for {size}")

    # ==========================================
    # 2. WORST FIT (En Kötü Uyan)
    # Strategy: Scan the WHOLE list. Find the LARGEST free block.
    # Logic: A large leftover hole is more useful than a tiny one.
    # ==========================================
    def allocate_worst_fit(self, size):
        current = self.head
        worst_block = None

        # We search through every block
        while current:
            if current.is_free and current.size >= size:
                # If we haven't found a candidate yet OR this one is bigger
                if worst_block is None or current.size > worst_block.size:
                    worst_block = current

            current = current.next_block

        if worst_block:
            self.split_block(worst_block, size)
            return

        print(f"FAIL: Worst Fit could not find space for {size}")

    # ==========================================
    # 3. NEXT FIT (Sıradaki Uyan)
    # Strategy: Start searching from where we LEFT OFF last time.
    # Use the first one we find. Don't scan from the beginning every time.
    # ==========================================
    def allocate_next_fit(self, size):
        start_node = self.last_alloc_ptr
        current = start_node

        # We loop until we check everything (circular check)
        while True:
            if current.is_free and current.size >= size:
                # We found a spot!
                self.split_block(current, size)
                # We remember this spot for next time
                self.last_alloc_ptr = current
                return

            # Move to next
            current = current.next_block

            # If we reached the end, wrap around to the head
            if current is None:
                current = self.head

            # If we came back to where we started, memory is full
            if current == start_node:
                break

        print(f"FAIL: Next Fit could not find space for {size}")

    # ==========================================
    # 4. FREE & MERGE (Silme ve Birleştirme)
    # Strategy: Find the block, mark it FREE.
    # Then check neighbors: If two FREE blocks are side-by-side, merge them.
    # ==========================================
    def free(self, start_address, size):
        current = self.head
        target_found = False

        # Step 1: Find the block and mark it as free
        while current:
            if current.start_address == start_address:
                current.is_free = True
                target_found = True
                print(f"ACTION: Freed block at Address {start_address}")
                break
            current = current.next_block

        if not target_found:
            print("ERROR: Address not found.")
            return

        # Step 2: Merge adjacent free blocks (Coalescing)
        # We start from the beginning to find neighbors
        merger = self.head
        while merger and merger.next_block:
            # If this block is FREE and the NEXT one is also FREE
            if merger.is_free and merger.next_block.is_free:
                # We combine their sizes
                merger.size += merger.next_block.size
                # We skip the next block (remove it from chain)
                merger.next_block = merger.next_block.next_block
                # We assume the user wants to know we merged them
                # print("  -> Merged two free blocks.")
            else:
                # Move to next only if we didn't merge (because new big block might merge again)
                merger = merger.next_block


# ==========================================
# MAIN TEST AREA
# ==========================================
if __name__ == "__main__":
    print("--- 1. TESTING BEST FIT ---")
    mem1 = MemoryManager(100)
    mem1.allocate_best_fit(20)
    mem1.allocate_best_fit(10)
    mem1.allocate_best_fit(30)
    mem1.free(20, 10)  # Create a hole of size 10 in the middle
    mem1.print_status()
    print("Requesting 9 units... (Should fit in the 10-hole)")
    mem1.allocate_best_fit(9)  # Should take the size 10 hole
    mem1.print_status()

    print("\n--- 2. TESTING WORST FIT ---")
    mem2 = MemoryManager(100)
    mem2.allocate_worst_fit(20)
    mem2.free(0, 20)  # Hole of 20 at start, Hole of 80 at end
    mem2.print_status()
    print("Requesting 15 units... (Should take the 80-hole because it's bigger)")
    mem2.allocate_worst_fit(15)
    mem2.print_status()

    print("\n--- 3. TESTING NEXT FIT ---")
    mem3 = MemoryManager(100)
    mem3.allocate_next_fit(20)
    mem3.allocate_next_fit(30)
    mem3.free(0, 20)  # Free the first part
    mem3.print_status()
    print("Requesting 10 units... (Should skip the first hole and continue from middle)")
    mem3.allocate_next_fit(10)  # Starts searching AFTER the 30 block
    mem3.print_status()
