from xml.etree.ElementPath import find


def findlength( head):
  
    curr = head
    cnt = 0
    while (curr != None):
      
        cnt = cnt + 1
        curr = curr.next
      
    return cnt

def listToArr(head):
    len1 = findlength(head)
    arr = []
    index = 0
    curr = head
    while( curr != None):
        arr.apend(curr.data)
        curr = curr.next
    
    return arr
