class Node: 
    def __init__(self, data): 
        self.data = data 
        self.next = next

def insert(root, item):
    temp = Node(0)
    temp.data = item
    temp.next = root
    root = temp
    return root

def arrToList(arr):
    n = len(arr)
    root = None
    for i in range(n - 1, -1, -1):
        root = insert(root, arr[i])
    return root

