# final code
# read all bad labels
file1 = open('bad_label.list', 'r') 
lines = file1.readlines() 

n_labels = 8 # 0-7

for line in lines:
    bad_label = line.split(' ')[0]
    file2 = open(bad_label, 'r') 
    lines2 = file2.readlines() 
    file2.close()
    
    file2 = open(bad_label, 'w') 
    
    L = []
    for line2 in lines2:
        lab = line2.split(' ')[0]
        if (int(lab) >= 0) and (int(lab) < n_labels): # valid
            L.append(line2)
        else:
            print('failed')
            
    file2.writelines(L)
    file2.close()
    
file1.close()