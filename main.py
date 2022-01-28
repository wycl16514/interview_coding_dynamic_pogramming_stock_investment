import time
start_time = time.time()

profit_map = {}
stock_selected = []

def  selectStock(saving, index, currentValue, futureValue):
    if saving <= 0: #储蓄额为0，无法进行投资因此收益为0
        return 0
    if index >= len(currentValue): #所有股票都选取完毕，直接返回
        return 0

    #查询当前情况下是否已经处理过
    if (saving, index) in profit_map:
        return profit_map[(saving, index)]

    #分别计算购买或者放弃当前股票的最大收益
    profit_for_buying = 0
    if saving >= currentValue[i]:
        #计算购买当前股票后所可能获得的最大收益
        profit_for_buying = futureValue[index] - currentValue[index] + selectStock(saving - currentValue[index], index + 1, currentValue, futureValue)

    #计算放弃当前股票后所能获得最大收益
    profit_for_ignore = selectStock(saving, index + 1, currentValue, futureValue)
    #选择收益最大的一种可能,并标记当前股票是否被选择
    if  profit_for_buying > profit_for_ignore:
        profit_map[(saving, index)] = profit_for_buying
        stock_selected[index] = 1
    else:
        profit_map[(saving, index+1)] = profit_for_ignore
        stock_selected[index] = 0


    return max(profit_for_buying, profit_for_ignore)

current_value = []
future_value = []
saving = 0

with open("input009.txt") as f:
    saving = int(f.readline())
    element_count = int(f.readline())  #current_value数组元素个数
    for i in range(element_count):
        current_value.append(int(f.readline()))
    f.readline() #future_value数组元素个数，它与current_value一样，所以忽略掉
    for i in range(element_count):
        future_value.append(int(f.readline()))

#saving = 250
#current_value = [175, 133, 109,  210, 97]
#future_value = [200, 125, 128, 228, 133]

print("saving: ", saving)
print("current_value: ", current_value)
print("future_value: ", future_value)
print("len: ", len(current_value))


for i in range(len(current_value)):
    stock_selected.append(0)

max_profit = selectStock(saving, 0, current_value, future_value)
print("--- running time is %s seconds ---" % (time.time() - start_time))
print("max profit is: ",max_profit)

total_profit = 0
for i in range(len(stock_selected)):
    if stock_selected[i] == 1:
        total_profit += future_value[i] - current_value[i]
        print("select stock: {}, with profit: {}".format(i, future_value[i] - current_value[i]))




