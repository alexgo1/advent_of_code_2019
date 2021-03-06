import numpy as np

# parse interactions and put in dict
f = open('input14.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]
txt = [item.split(' => ') for item in txt]
txt = [[item[0].split(', '), item[1]] for item in txt]    

interactions = {}
for item in txt:
    res = item[1].split(' ')[1]
    res_num = int(item[1].split(' ')[0])
    interactions[res] = {'self': res_num}
    for item2 in item[0]:
        cur = item2.split(' ')[1]
        cur_num = int(item2.split(' ')[0])
        interactions[res][cur] = cur_num

spare_elements = {}
for key in interactions:
    spare_elements[key] = 0
spare_elements['ORE'] = 0
spare_elements_start = spare_elements.copy()

def cnt_ore(element, num, spare_elements):
    if num == 0:
        return 0, spare_elements
    elif element == 'ORE':
        return num
    elif spare_elements[element] >= num:
        spare_elements[element] -= num
        return 0
    elif spare_elements[element] > 0:
        tmp = spare_elements[element]
        spare_elements[element] = 0
        return cnt_ore(element, num - tmp, spare_elements)
    else:
        cnt = 0
        if num <= interactions[element]['self']:
            rep = 1
            spare_elements[element] = (interactions[element]['self'] - num)
        else:
            rep = int(np.ceil(num/interactions[element]['self']))
            spare_elements[element] = (rep*interactions[element]['self'] - num)
        for i in range(rep):
            for key in interactions[element]:
                if key == 'self':
                    continue
                cnt += cnt_ore(key, interactions[element][key], spare_elements)
        return cnt
    
    
# Part 1:
print('part 1 answer = ' + str(cnt_ore('FUEL', 1, spare_elements)))


def cnt_ore_exact(element, num):
    if element=='ORE':
        return num
    else:
        cnt = 0
        for key in interactions[element]:
            if key == 'self':
                continue
            cnt += (num/interactions[element]['self'])*cnt_ore_exact(key, interactions[element][key])
        return cnt
        
# Part 2:
        
# calculate the 'exact' OREs needed to produce 1 fuel, and divide
print('part 2 answer = ' + str(int((10**12)/cnt_ore_exact('FUEL', 1))-1))


