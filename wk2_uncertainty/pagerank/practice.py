pageFrequency = {}
page = 0
for i in range(4):
        if i > 0:
            page = i
        
        if page in pageFrequency:
            pageFrequency[page] += 1
        else:
            pageFrequency[page] = 1

print(len(pageFrequency), pageFrequency)
