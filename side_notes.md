Base assumptions:
Values can appear more than once in the list, When ExtractMin is used only the 1 instance of the Mininmum is exracted

1) Sorted lists:
    INSERT: for every value given, the function iterates over the list to find the right position to place the new value while keeping the list sorted. 
        Best Case: O(1), the values given are lower or equal to the minimum value every time, or lower or equal to the 2nd value in the list (which can be the minimum value as well), or higher than the maximum value (prev to the lowest), resulting in a predifined operation without any input dependant iterations. 
        
        Worst Case: O(n), the values given are in the "middle" of the min and max values and the function iterates over n/2 nodes 

        Mean Case:(largely depending on the input range and intial values, given a total random state, m=max_possible_val, n=min_possible_val, the probabily to get a number x is 1/(m-n), the probabilty of another number being lower is  1/(x-n), higher: 1/(m-x), and equal is 1/(m-n)^2, ) O(lg(n)) - need to prove though....

    MINIMUM: The function returns the first value in the list. 
        Every Case:O(1)

    EXTRACT-MIN: The function takes the first (Which is the minimum) node and removes it from the list, because the list is sorted there is no need to search for a new minimum. 
        Every Case: O(1)

    Extract-Min-Val: The function takes the minimum value and removes all nodes that have that value
        Best Case: O(1), there is only one instance for that value
        Worst Case: O(n), all the values in the list are the same = the minimum value
        Mean case: O(1), the probabilty of the value filling all nodes is 1/(x)^n where x=the range of possible values. assuming x=2 (while for x>2 the case applies even more) (1/2)^x mean that the  

    UNION:In order to merge the lists the function goes over both of them and adds the values one by one, each time the minimum value between the 2 lists, meaning it iterates over n+m (length of the lists) times and uses O(1) function Extract-Min
        Best case:O(1) if either of the lists is empty, the functions returns the other one
        Worst Case:O(n+n = 2n) = O(n), both lists have the same ammount of values
        Mean Case:O(length of the smaller list) = O(n) 


2) lists:
    INSERT: 
        
        Every Case: O(1)

    MINIMUM: The function returns the value in min_node. 
        Every Case:O(1)

    EXTRACT-MIN: The function takes the minimum node and removes it from the list, returning it's child nodes to the main axis, and gathers the values again into "heaps"
        Best Case: O(lg(n))
        Worst Case: O(n),
        Mean case: O(lg(n)), 

    Extract-Min-Val: The function takes the minimum value and removes all nodes that have that value
        Best Case: O(lg(n)),
        Worst Case: O(n), 
        Mean case: O(lg(n)),

    UNION:
        Every case:O(1)

3) foriegn lists:

    INSERT: 
        Given a value place it first if it's the new min, before first (last) if it's the new max, after first otherwise
        also check if it already exists in a different heap using val_in_list, this function is relaiant on the amount of heaps as well as their size and state
        Best Case: O(1), there's only 1 list, or there are 2 and the value is outside the boundries of it resulting in an optimized find
        Worst Case: O(n^2)
        Average Case: O(nlg(n))

    MINIMUM: The function returns the value in min_node. 
        Every Case:O(1)

    EXTRACT-MIN: The function takes the minimum node and removes it from the list, returning it's child nodes to the main axis, and gathers the values again into "heaps"
        Best Case: O(lg(n))
        Worst Case: O(n),
        Mean case: O(lg(n)), 

    Extract-Min-Val: The function takes the minimum value and removes all nodes that have that value
        Best Case: O(lg(n)),
        Worst Case: O(n), 
        Mean case: O(lg(n)),

    UNION:
        Every case:O(1)