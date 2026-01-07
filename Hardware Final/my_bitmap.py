class Bitmap:
    def __init__(self, total_capacity):
        # we give the size of the disk
        self.capacity = total_capacity

        # we create the list and fill every place with 0's
        self.storage_map = [0] * self.capacity

    def show_status(self):
        print(f"Current Disk Bitmap State:")

        # we convert the integer list to a string list to see it visually
        display_str = ''.join(str(bit) for bit in self.storage_map)
        print(f"[{display_str}]")
        print("-" * 40)

    def allocate_memory(self, file_name, required_blocks):
        # variable to keep track of consecutive free blocks found
        consecutive_free_number = 0

        # variable to store the potential starting index of the file
        start_index = -1

        for i in range(self.capacity):
            if self.storage_map[i] == 0:
                if consecutive_free_number == 0:
                    start_index = i

                consecutive_free_number += 1
            else:
                # if we hit an occupied block (1), reset the counter
                consecutive_free_number = 0
                start_index = -1

            # check if we have enough consecutive blocks
            if consecutive_free_number == required_blocks:
                for j in range(required_blocks):
                    self.storage_map[start_index + j] = 1

                # we inform the user
                print(f"SUCCESS: File '{file_name}' allocated. Start: {start_index}, Length: {required_blocks}")
                return

                # if the loop finishes without returning, no space was found
        print(f"ERROR: Not enough contiguous space for '{file_name}'")

    def deallocate_memory(self, start_index, length):
        # we inform the user about the deletion process
        print(f"ACTION: Deleting file at index {start_index} with length {length}...")

        for i in range(length):
            target_pos = start_index + i

            if target_pos < self.capacity:
                self.storage_map[target_pos] = 0
            else:
                print("Warning: Index out of bounds.")

        print("File deleted successfully.")


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Create a disk manager with 20 blocks
    my_disk = BitmapDiskManager(20)

    # Show initial empty state
    my_disk.show_status()

    # Try to save 'File_A' needing 5 blocks
    my_disk.allocate_memory("File_A", 5)
    my_disk.show_status()

    # Try to save 'File_B' needing 3 blocks
    my_disk.allocate_memory("File_B", 3)
    my_disk.show_status()

    # Delete 'File_A' (starting at 0, length 5) to create a hole at the beginning
    my_disk.deallocate_memory(0, 5)
    my_disk.show_status()

    # Try to save 'File_C' into the newly freed space
    my_disk.allocate_memory("File_C", 4)
    my_disk.show_status()
