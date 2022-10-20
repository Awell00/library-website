test_list = [10, 15, 20, 7, 46, 2808]
 
print("Checking if 15 exists in list")
 
# number of times element exists in list
exist_count = test_list.count(15)
 
# checking if it is more than 0
if exist_count > 0:
    print(exist_count)
else:
    print("No, 15 does not exists in list")