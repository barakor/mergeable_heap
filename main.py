import os
import sys
import math


class MergableHeap:
    class Node:
        # node class holding actual vals, and acting as the quatrly linked circular list
        # Nodes have next-prev (right-left) and child (down) connections
        # in practice, we iterate [down]-[right] to go over the full list, as it's not sorted, it doesn't really matter
        # The parent is always smaller than the child, thus we keep a min_node value as the main poiner to each child
        
        def __init__(self, val):
            self.val = val
            self.child = None
            self.prev = None
            self.next = None
            self.degree = 0
        def __str__(self, start = None):
            if self is not start:
                if start is None:
                    start = self
                return "{} {} {}".format(self.val, self.child.__str__() if self.child else "", self.next.__str__(start))
            return ""
        
        def __iter__(self, start = None):
            if start is None:
                start = self
            n = self
            yield n.val
            if n.child:
                yield from self.child.__iter__()
            n = n.next
            while n is not start:
                yield n.val
                if n.child:
                    yield from n.child.__iter__()
                n = n.next
                
    # the Mergable_Heap wrapper holds the linked list, it's absolute length and a pointer 
    # to the minimum node
    def __init__(self):
        self.min_node = None #pointer(technically a reference) to the minimum node
        self.nodes_count = 0 #the ammount of nodes in the linked list
    
    def __iter__(self):
        return self.min_node.__iter__()
    def __str__(self):
        return self.min_node.__str__()

    def generate_nodes(self, start):
        # Goes over nodes in the list of the start: by going rightward with .next
        # O(length of start's list)
        yield start
        node = start.next
        while node is not start:
            yield node
            node = node.next

    def minimum(self):
        # return the minimum val in the list
        # O (1)
        return self.min_node


    def remove_node_from_list(self, node):
        # Remove the node from the list it's in, decrease nodes count as well 
        # O(1)
        if node == self.min_node:
            self.min_node = node.next
        node.prev.next = node.next
        node.next.prev = node.prev
        self.nodes_count -= 1

    def insert(self, val):
        # insert val into the the list next after the root node in min_node
        # Time Complexity: no iterations are done and everything is statically used 
        # a function call to insert_node_to_min_node is made which is also O(1)
        # so this function is O(1) for every case  
        n = self.Node(val)
        n.prev = n.next = n
        self.insert_node_to_list(n)
        return n

    def insert_after_node(self, node, n):
        # O(1), just pushes it inside
        n.next = node.next
        n.prev = node
        node.next.prev = n
        node.next = n
        self.nodes_count += 1

    
    def insert_node_to_list(self, node):
        #Insert node into the linked list
        #Time Complexity: no iterations are done and everything is statically used 
        # so this function is O(1)
        if self.min_node is None:
            self.min_node = node
            self.nodes_count += 1
        elif node.val <= self.min_node.val:
            self.insert_after_node(self.min_node.prev, node)
            self.min_node = node
        elif node.val>=self.min_node.prev.val:
            self.insert_after_node(self.min_node.prev, node)
        else:
            self.insert_after_node(self.min_node, node)

    def extract_minimum(self):
        # pop the minimum val from the list
        # Time: Worst case: O(n), Average case: O(lg(n)), Best case: O(1)
        # Memory: 
        min_node = self.min_node
        if min_node is not None:
            if min_node.child is not None:
                # return child nodes to the list
                cmin = min_node.child
                clast = cmin.prev
                min_node.next.prev = clast
                clast.next = min_node.next
                cmin.prev = min_node
                min_node.next = cmin

            self.remove_node_from_list(min_node)
            # if the linked list only contained 1 node
            if min_node is min_node.next:
                self.min_node = None    
            else:
                self.min_node = min_node.next
                self.gather_to_heap()
        return min_node

    def gather_to_heap(self):
        # gathers all nodes in the main axis of the same degree (degree is the amount of nested childs a node has)
        # the inner children are linked lists as well, and they behave the same way as the main axis (first node is the smallest), while the parent is always smaller than all of it's children as well 
        # Best case: O(1), average case: O(lg(n)), worst case: O(n)
        degrees_list = [None] * max(2, int(math.log2(self.nodes_count) * 2))
        nodes = [n for n in self.generate_nodes(self.min_node)]
        for node in nodes:
            degree = node.degree
            while degrees_list[degree] is not None:
                node_of_same_degree = degrees_list[degree]
                # pick the smaller value to be the parent
                if node_of_same_degree.val < node.val:
                    node_of_same_degree, node = node, node_of_same_degree
                self.child_merge(node, node_of_same_degree)

                degrees_list[degree] = None
                degree += 1

            degrees_list[node.degree] = node
        # because of the nature of the way we gather the nodes, the minimum value must be in the main axis
        # so we update the pointer to it
        for i in range(0, len(degrees_list)):
            if degrees_list[i] is not None:
                self.remove_node_from_list(degrees_list[i])
                self.insert_node_to_list(degrees_list[i])

    def child_merge(self, parent, node):
        # merging parent and node
        # O(1)
        self.remove_node_from_list(node)
        node.prev = node.next = node
        self.insert_node_to_child_list(parent, node)
        parent.degree += 1

    # merge a node with the doubly linked child list of a root node
    def insert_node_to_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
            self.nodes_count += 1
        elif node.val <= parent.child.val:
            self.insert_after_node(parent.child.prev, node)
            parent.child = node
        elif node.val>=parent.child.prev.val:
            self.insert_after_node(parent.child.prev, node)
        else:
            self.insert_after_node(parent.child, node)

    def merge(self, heap_to_merge):
        if self.min_node is None:
            return heap_to_merge
        elif heap_to_merge.min_node is None:
            return self
        
        merged_into = MergableHeap()
        merged_into.min_node = self.min_node
        # fix pointers when merging the two heaps
        max_node = heap_to_merge.min_node.prev
        heap_to_merge.min_node.prev = merged_into.min_node.prev
        merged_into.min_node.prev.next = heap_to_merge.min_node
        merged_into.min_node.prev = max_node
        merged_into.min_node.prev.next = merged_into.min_node
        # update min node if needed
        if heap_to_merge.min_node.val < merged_into.min_node.val:
            merged_into.min_node = heap_to_merge.min_node
        # update total nodes
        merged_into.nodes_count = self.nodes_count + heap_to_merge.nodes_count
        return merged_into

    
    def val_in_list(self, val, min_node = None):
        # Best: O(1)
        # Worst: O(n)
        # Average: O(lg(n)) (binary search~ish)

        if min_node is None:
            min_node = self.min_node
        n = min_node
        if val < min_node.val:
            return False
        elif val == min_node.val:
            return True
        elif val == min_node.prev.val:
            return True
        else:
            
            if val>n.val and n.child:
                c = n.child 
                if self.val_in_list(val, min_node=c):
                    return True
            n = n.next
            while n is not min_node:
                if val == n.val:
                    return True
                elif val>n.val and n.child:
                        c = n.child
                        if self.val_in_list(val, min_node=c):
                            return True
                n = n.next
        return False

        

class SortedMergableHeap():
    # Assuming values can only apear once in the heap
    class Node():
        def __init__(self, val=None):
            self.val = val
            self.next = self
            self.prev = self

        def __str__(self, start = None): 
            if self is not start:
                if start is None:
                    start = self
                return "{} {}".format(self.val, self.next.__str__(start))
            return ""

    def __init__(self):
        self.min_node = None  # circular
        self.nodes_count = 0  # keep track of the ammount of nodes

    def __tolist__(self):
        n = self.min_node
        l = [n.val]
        n = n.next
        while n is not self.min_node:
            l.append(n.val)
            n = n.next
        return l

    def __str__(self): return self.min_node.__str__()
    def __len__(self): return self.nodes_count

    def insert_after_node(self, node, n):
        # O(1), just push a new node after the given node
        n.next = node.next
        n.prev = node
        node.next.prev = n
        node.next = n
        self.nodes_count += 1

    def insert_ordered(self, val):
        # in O(n), go over list and insert val into it
        # because we assume we can't have duplicated values (as a base assumption for the task)
        # We must go over the list to validate if it's there or not, so might as well keep it
        # sorted to keep other functions at better time complexities
        n = self.min_node
        node = self.Node(val)
        node.prev = node
        node.next = node
        if n is None:
            self.min_node = node
            self.nodes_count = 1
            return node

        elif val <= n.val:
            # check if it's a new min val
            self.insert_after_node(n.prev, node)
            self.min_node = node
            return node
        elif val >= n.prev.val:
            self.insert_after_node(n.prev, node)
            return node
        else:
            # a naive way to try to cut the mean time assuming normal distribution
            middle = int((n.val+n.next.val)/2)
            if val > middle:
                n = n.prev
                while n is not self.min_node:
                    if val >= n.val:
                        self.insert_after_node(n, node)
                        return node
                    else:
                        n = n.prev
                self.insert_after_node(n, node)
                return node
            else:
                n = n.next
                while n is not self.min_node:
                    if val <= n.val:
                        self.insert_after_node(n.prev, node)
                        return node
                    else:
                        n = n.next
                self.insert_after_node(n.prev, node)
                return node

    # remove a node from the min_node

    def pop(self, node):
        # O(1)
        if node.next is node:
            self.min_node = None
            self.nodes_count = 0
            node.prev = node
            node.next = node
            return node

        if node == self.min_node:
            self.min_node = node.next
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node
        node.next = node

        self.nodes_count -= 1
        return node

    def minimum(self):
        # O(1)
        return self.min_node

    def extract_minimum_val(self):
        # O(n)
        min_val = self.minimum().val
        while self.minimum().val == min_val:
            n = self.pop(self.min_node)
        return min_val

    def extract_minimum(self):
        # O(1)
        return self.pop(self.min_node)

    def merge(self, m):
        # O(n)
        if self.nodes_count == 0:
            return m
        elif m.nodes_count == 0:
            return self
        merge_into = self if self.nodes_count > m.nodes_count else m
        take_from = m if merge_into is self else self

        while take_from.minimum().val <= merge_into.minimum().val:
            # take all the minimum nodes
            n = take_from.extract_minimum()
            merge_into.insert_after_node(merge_into.min_node.prev, n)
            merge_into.min_node = n

        A = merge_into.min_node.next

        while (take_from.nodes_count > 0) and (A is not merge_into.min_node):
            # Go over merge_into and insert into it the values from take_from in the right places
            if take_from.minimum().val <= A.val:
                n = take_from.extract_minimum()
                merge_into.insert_after_node(A.prev, n)
            else:
                A = A.next

        while take_from.nodes_count > 0:
            # The rest of take_from is bigger than merge_into so we iterate over it and add to the end
            n = take_from.extract_minimum()
            merge_into.insert_after_node(merge_into.min_node.prev, n)

        return merge_into


def sorted_insert(sorted_heaps, val):
    return sorted_heaps[-1].insert_ordered(val)


def sorted_minimum(sorted_heaps):
    return sorted_heaps[-1].minimum().val


def sorted_ext_min(sorted_heaps):
    return sorted_heaps[-1].extract_minimum().val


def sorted_merge(sorted_heaps):
    if len(sorted_heaps)<2:
        return sorted_heaps
    else:
        base = sorted_heaps[0]
        for i in range(1,len(sorted_heaps)):
            base = base.merge(sorted_heaps[i])
        return base
    

def unsorted_insert(heaps, val):
    return heaps[-1].insert(val)


def unsorted_minimum(heaps):
    return heaps[-1].minimum().val


def unsorted_ext_min(heaps):
    return heaps[-1].extract_minimum().val


def unsorted_merge(heaps):
    if len(heaps)<2:
        return heaps
    else:
        base = heaps[0]
        for i in range(1,len(heaps)):
            base = base.merge(heaps[i])
        return base
    

def foreign_insert(heaps, val):
    for i in range(len(heaps)-1):
        heap = heaps[i]
        heap.gather_to_heap()
        if heap.val_in_list(val):
            print(f"The value {val} is already in a heap ({i})")
            return False
    return heaps[-1].insert(val)


def foreign_minimum(heaps):
    return heaps[-1].minimum().val


def foreign_ext_min(heaps):
    return heaps[-1].extract_minimum().val


def foreign_merge(heaps):
    if len(heaps)<2:
        return heaps
    else:
        base = heaps[0]
        for i in range(1,len(heaps)):
            base = base.merge(heaps[i])
        return base
    

list_type = {
    "sorted": {"make-heap":SortedMergableHeap, "insert":sorted_insert, "print":print,
               "minimum": sorted_minimum, "extract-min": sorted_ext_min, "union":sorted_merge},
    "not sorted":{"make-heap":MergableHeap, "insert":unsorted_insert, "print":print,
                  "minimum":unsorted_minimum , "extract-min": unsorted_ext_min, "union":unsorted_merge},
    "foreigns":{"make-heap":MergableHeap, "insert":foreign_insert, "print":print, 
                     "minimum":foreign_minimum , "extract-min": foreign_ext_min, "union":foreign_merge}
}


def exec_cmd(heaps,ltf, f, args):
    if f == "make-heap":
            heaps.append(ltf[f]())
            print("There are now {} heaps in memory".format(len(heaps)))
    elif len(heaps)==0:
        print("No heaps in memory, running MAKE-HEAP first")
        heaps.append(ltf["make-heap"]())
    if f in ["minimum", "extract-min"]:
        v = ltf[f](heaps)
        print(f"The minimum value is: {v}")
    elif f == "insert":
        if len(args)!=1:
            print("ERROR, ONLY 1 VALUE IS ALLOWED")
        else:
            v = int(args[0])
            ltf[f](heaps, v)
    elif f == "union":
        h = ltf[f](heaps)
        heaps = [h]
    if f not in ltf:
        print("What was that? please issue a valid command")
    print("list state: ", end = "")
    print(heaps[-1])
    return heaps

# Main 

heaps = []
print(os.getcwd())
if len(sys.argv)==2:
    input_file = sys.argv[1]
    input_file_full_path = os.path.join(os.getcwd(), input_file)
    with open(input_file_full_path, "rt") as ld:
        lines = ld.readlines()
    lt = lines[0].split("\n")[0].lower()
    if lt in ["1","2","3"]:
        lt = {"1":"sorted","2": "not sorted","3":"foreigns"}[lt]
    elif lt not in list_type:
        print(f"INVALID LIST TYPE {lt}, USING Not-Sorted as default")
        lt = "not sorted"
    ltf = list_type[lt]
    for line in lines[1:]:
        cmd = line.split("\n")[0].split(" ")
        f = cmd[0].lower()    
        args = cmd[1:]

        heaps = exec_cmd(heaps,ltf , f, args=args)

else:
    lt = input("Please select list type:\n 1) sorted \n 2) not sorted \n 3) foreigns \n").lower()
    if lt in ["1","2","3"]:
        lt = {"1":"sorted","2": "not sorted","3":"foreigns"}[lt]
    elif lt not in list_type:
        print(f"INVALID LIST TYPE {lt}, USING Not-Sorted as default")
        lt = "Not Sorted"
    ltf = list_type[lt]
    cmd = input("Select an operation:{}".format(list(list_type[lt].keys())))
    while cmd != "exit":
        cmd = cmd.split(" ")
        f = cmd[0]
        args = cmd[1:]

        heaps = exec_cmd(heaps, ltf, f, args=args)
        cmd = input("Select an operation:{}".format(list_type[lt].keys())).lower()
