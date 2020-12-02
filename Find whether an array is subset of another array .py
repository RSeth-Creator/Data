#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import array as arr


# In[97]:


##Initialize main array

main = arr.array('i', [])
s1 = int(input("Enter size of array:"))
for i in range(0, s1):
    n1 = int(input("Enter main array element:"))
    main.append(n1)

print("final main array is:", end="")
for i in main:
    print(i, end=" ")
    


# In[109]:


##Initialize test  array

test = arr.array('i', [])
s2 = int(input("Enter size of array:"))
for j in range(0, s2):
    n2 = int(input("Enter main array element:"))
    test.append(n2)

print("final test array is:", end="")
for j in test:
    print(j, end=" ")
    


# In[110]:


## Check how many element of test present in the main array 

temp=arr.array('i',[])
for k1 in range (0,len(test)):
    for k2 in range (0,len(main)):
        if(test[k1]== main[k2]):
            temp.append(test[k2])


# In[114]:


##Element of test array present in main array is:

print("Element of test array present in main array is:", end=" ")
for k in temp:
    print(k,end=" ")
print("\n") 
##find out subset or not 
if (len(temp)!=len(test)):
    print("Not all the element of test array present in main array. Hence,Test array is not subset of the main array.")
else:
    print("All the element of test array present in main array. Hence,Test array is subset of main array.")


# In[ ]:




