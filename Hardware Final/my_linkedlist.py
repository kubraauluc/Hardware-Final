# Helper class to represent a single disk block
class Block:
    def __init__(self):
        self.occupied = 0  # 0 means free
        self.next_block = -1  # -1 means end of file
        self.file_name = None


class LinkedList:
    def __init__(self, total_capacity):
        # we give the size of the disk
        self.capacity = total_capacity

        # we create the list of blocks using the helper class
        self.disk_blocks = [Block() for _ in range(self.capacity)]

    def show_status(self):
        print(f"Current Disk Linked List State:")

        # simple visual map to see occupied blocks
        visual_list = []
        for block in self.disk_blocks:
            if block.occupied == 1:
                # show the first letter of the file name
                visual_list.append(block.file_name[0])
            else:
                visual_list.append(".")

        display_str = ' '.join(visual_list)
        print(f"[{display_str}]")
        print("-" * 40)

    def show_file_chain(self, start_index):
        # method to visualize how blocks are connected
        current = start_index
        chain = []

        while current != -1:
            chain.append(str(current))
            current = self.disk_blocks[current].next_block

        print(f"File Chain: {' -> '.join(chain)}")

    def allocate_memory(self, file_name, required_blocks):
        # check if we have enough total free space first
        free_space_counter = 0
        for block in self.disk_blocks:
            if block.occupied == 0:
                free_space_counter += 1

        if free_space_counter < required_blocks:
            print(f"ERROR: Not enough space for '{file_name}'")
            return

        # variable to keep track of allocated blocks
        allocated_counter = 0
        current_index = -1
        start_index = -1
        previous_index = -1

        for i in range(self.capacity):
            # stop if we allocated enough blocks
            if allocated_counter == required_blocks:
                break

            # if the block is empty
            if self.disk_blocks[i].occupied == 0:
                # fill the block details
                self.disk_blocks[i].occupied = 1
                self.disk_blocks[i].file_name = file_name

                # save start index if it is the first block
                if start_index == -1:
                    start_index = i

                # link the previous block to this one
                if previous_index != -1:
                    self.disk_blocks[previous_index].next_block = i

                # update previous index to current
                previous_index = i
                allocated_counter += 1

        # make sure the last block points to -1 (end)
        if previous_index != -1:
            self.disk_blocks[previous_index].next_block = -1

        # we inform the user
        print(f"SUCCESS: File '{file_name}' allocated. Start Node: {start_index}")

    def deallocate_memory(self, start_index):
        # we inform the user
        print(f"ACTION: Deleting file starting at node {start_index}...")

        current = start_index

        # follow the chain to delete blocks one by one
        while current != -1:
            temp_next = self.disk_blocks[current].next_block

            # reset the block info
            self.disk_blocks[current].occupied = 0
            self.disk_blocks[current].file_name = None
            self.disk_blocks[current].next_block = -1

            # move to the next block in the chain
            current = temp_next

        print("File deleted successfully.")


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Create a linked list disk with 15 blocks
    my_disk = LinkedList(15)

    # Show initial empty state
    my_disk.show_status()

    # Try to save 'Alpha' needing 3 blocks
    my_disk.allocate_memory("Alpha", 3)
    my_disk.show_status()

    # Try to save 'Beta' needing 4 blocks
    my_disk.allocate_memory("Beta", 4)
    my_disk.show_status()

    # Visualizing the chain of Alpha (starts at 0)
    my_disk.show_file_chain(0)

    # Delete 'Alpha' to create holes (fragmentation)
    # linked list handles holes better than bitmap
    my_disk.deallocate_memory(0)
    my_disk.show_status()

    # Try to save 'Gamma' needing 5 blocks
    # It should fill the empty spots left by Alpha
    my_disk.allocate_memory("Gamma", 5)
    my_disk.show_status()

    # Verify Gamma's chain (it should be scattered)
    # Gamma starts at 0 because Alpha freed it
    my_disk.show_file_chain(0)
    4