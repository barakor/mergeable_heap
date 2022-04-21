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
    "Sorted": {"make-heap":SortedMergableHeap, "insert":sorted_insert, "print":print,
               "minimum": sorted_minimum, "extract-min": sorted_ext_min, "union":sorted_merge},
    "Not Sorted":{"make-heap":MergableHeap, "insert":unsorted_insert, "print":print,
                  "minimum":unsorted_minimum , "extract-min": unsorted_ext_min, "union":unsorted_merge},
    "Foreigns":{"make-heap":MergableHeap, "insert":foreign_insert, "print":print, 
                     "minimum":foreign_minimum , "extract-min": foreign_ext_min, "union":foreign_merge}
}