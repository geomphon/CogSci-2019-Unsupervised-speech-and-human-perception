filename = 'dpgmm_english_kl_results.csv'
f = open(filename, 'r')
ind = f.readline()
total = 0
count = 0
for line in f:
    new_line = line.replace('\n','').split(',')
    res = new_line[-1]
    if res == 'TGT':
        total+=1
    count +=1

print(float(total)/float(count))
    
