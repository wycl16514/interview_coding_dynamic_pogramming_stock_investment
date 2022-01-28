最近有个猎头突然给我推荐一份工作，面试流程是先在网上做几道测试题。我突然发现这类网上测试有一个规律，如果面试的是外企那么通常在HakerRank上做题，例如亚马逊，如果面试的是国内企业，例如华为等，通常在牛客网上做题，无论是哪种情况，考察的题型几乎都遵守同样的规律，通常而言面试时长是90分钟，编程题目大概3道作用，前两道通常考察循环，数组，字符串，栈，队列，第三道最难，同时它在95%以上的情况属于动态规划。

前两道虽然不难，但是题目会给你准备一些特殊的测试用例，因此你必须花不少时间修改代码才能通过所有用例，等到你做到第3题时该概率只有30分钟左右了。如果你不能在十分钟内洞穿第三道题的解法，那你基本不可能完成它。我想把面试算法题中的动态规划作为一个专门课题，通过一系列文章详细剖析其结题套路，原本计划在完成手头几个课题后再处理，但想到过完年后可能有很多同学要换工作，因此必然会面临网上做算法题的挑战，所以提前将这个课题推出来，希望对大家换工作有帮助，如果你因此而赢得心仪的工作，记得苟富贵，莫相忘。

动态规划的算法题虽然难度较大，但却有固定的套路可循，我们通过训练掌握其解题技巧后，在十分钟内找到其解法并不难，同时动态规划难在找到思路，有了解法后编码量往往很小。我们先看我最近在HankerRank做面试题是遇到的一个情况，它的题目如下：

一个投资者想把自己的积蓄投资到股市。他有一系列股票可以选择，但是对任何一只股票它只能买一手，购买股票的前不能超过它的积蓄总额。他有一个股神朋友能非常准确的预测股票当前的价格和一年后的价格，假设预测是完全正确的情况下，请你找出股票的最佳购买方案，使得投资者的收益最大化。例如投资者当前积蓄为saving=250，当前股票价格为current_value=[175, 133, 109, 210, 97],股票一年后价格为future_value=[200, 125, 128, 228, 133], 于是最佳投资方法为购买下标为2和4的两只股票，所得收益为 (128-109) + (133 - 97) = 55，请你设计算法，在给定saving, current_value, future_value的情况下计算最优收益。

我们先看最简单的处理方法那就是遍历所有可能的组合，对于下标为i的股票而言，某个组合要不包含它，要不不包含它，因此暴力遍历的话，对于n只股票而言，时间复杂度是(2^n)，使用暴力遍历法是绝对过不了关，因为它有时间限制，例如我遇到的这道题时间限制为10秒，使用暴力查找所耗费的时间远远超过10秒。

动态规划问题的结题套路一个核心是使用空间换时间，因此遇到这类问题时我们首先要想到构造一张表来存储中间数据；第二个套路是，将问题分解成多个小问题，各个击破后再把小问题的结果结合起来得到当前问题的答案；第3个套路是，在进入递归时，先查表看看是否在当前给定条件下是否已经有了答案，如果有了答案就立即返回，注意这一步是加快速度的关键。

根据上面套路，我们分析一下题目，首先思考如何将问题分解成规模更小但是本质一样的子问题。我们从头开始遍历每只股票，假设当前遍历到第i只股票，在获取最佳收益时针对它只有两种选择，一种是购买它，一种是不购买它，于是问题分解成两种情况，如果购买它，那么将储蓄额减去当前股票价格，然后要用剩余的储蓄在第i只股票之后的股票中中获取最大利润，如果买它，那么我们必须要在当前储蓄额的基础从，从第i只股票之后的股票中找到最大例如。

如果我们用selectStock(saving, index, current_value, future_value)表示储蓄额为saving的情况下，从下标为index开始的股票中所获得的最大收益，于是针对第i只股票，在购买了它的情况下，所能获得的收益就是 future_value[i] - current_value[i] + selectStock(saving - current_value[i], i + 1, current_value, future_value)。
如果不购买第i只股票，那么所得最大收益就是selectStock(saving, i+1, current_value, future_value)，于是我们计算出两个值后，选取最大那个就是针对第i只股票的最好决策。这里的思路针对的是套路2，我们看看套路1，3怎么实现。

我们要使用一个表，用来记录在储蓄额为saving，并且当前可选择股票的下标为i时所能获得的最优例如，于是我们构造一个哈希表profit_map = {}, 键值是一个tuple:(saving, sotck_index)，在计算selectStock时，我们先根据saving 和 i 在profit_map中查找，看看给定情况下是否已经有结果，如果有了结果里面返回，如果没有，那么计算当前条件下的最佳收益后，将对应结果存储到表里，于是代码实现如下：
```
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
#测试数据从文件读取，相关文件从给定github下载
with open("input009.txt") as f:
    saving = int(f.readline())
    element_count = int(f.readline())  #current_value数组元素个数
    for i in range(element_count):
        current_value.append(int(f.readline()))
    f.readline() #future_value数组元素个数，它与current_value一样，所以忽略掉
    for i in range(element_count):
        future_value.append(int(f.readline()))

#则是简单测试用例，反注释后可以运行得到前面说明的结果
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

```
上面代码运行后所得结果如下：
```
saving:  8099
current_value:  [199, 193, 201, 172, 159, 106, 42, 70, 118, 209, 202, 108, 189, 162, 283, 5, 123, 43, 127, 128, 105, 90, 91, 225, 192, 37, 251, 77, 195, 64, 7, 289, 24, 59, 84, 110, 48, 88, 248, 174, 131, 258, 244, 58, 50, 169, 217, 160, 41, 95, 283, 200, 149, 249, 106, 116, 174, 47, 159, 21, 119, 105, 42, 56]
future_value:  [231, 234, 7, 253, 35, 289, 27, 288, 278, 170, 238, 72, 146, 129, 254, 245, 16, 177, 272, 267, 12, 116, 289, 62, 25, 247, 138, 272, 28, 280, 297, 263, 51, 262, 38, 229, 146, 204, 285, 1, 269, 57, 290, 296, 293, 294, 297, 299, 264, 191, 266, 299, 277, 26, 269, 297, 94, 248, 46, 104, 288, 17, 33, 279]
len:  64
--- running time is 0.6094491481781006 seconds ---
max profit is:  5719
select stock: 0, with profit: 32
select stock: 1, with profit: 41
select stock: 3, with profit: 81
select stock: 5, with profit: 183
select stock: 7, with profit: 218
select stock: 8, with profit: 160
select stock: 10, with profit: 36
select stock: 15, with profit: 240
select stock: 17, with profit: 134
select stock: 18, with profit: 145
select stock: 19, with profit: 139
select stock: 21, with profit: 26
select stock: 22, with profit: 198
select stock: 25, with profit: 210
select stock: 27, with profit: 195
select stock: 29, with profit: 216
select stock: 30, with profit: 290
select stock: 32, with profit: 27
select stock: 33, with profit: 203
select stock: 35, with profit: 119
select stock: 36, with profit: 98
select stock: 37, with profit: 116
select stock: 38, with profit: 37
select stock: 40, with profit: 138
select stock: 42, with profit: 46
select stock: 43, with profit: 238
select stock: 44, with profit: 243
select stock: 45, with profit: 125
select stock: 46, with profit: 80
select stock: 47, with profit: 139
select stock: 48, with profit: 223
select stock: 49, with profit: 96
select stock: 51, with profit: 99
select stock: 52, with profit: 128
select stock: 54, with profit: 163
select stock: 55, with profit: 181
select stock: 57, with profit: 201
select stock: 59, with profit: 83
select stock: 60, with profit: 169
select stock: 63, with profit: 223

```
输入的数组有65个数据，运行时间在0.65秒左右，如果使用穷举法遍历所有可能情况的话，所需时间很可能要个把小时，HankRank上这道题的时间上线是10秒，如果不使用动态规划方法的话就很难达到要求。

我们分析一下算法复杂度，可以看到如果profit_map填入的key为(saving, index),其中index取值范围就是输入数组的个数，因此profit_map最会存储的个数为 saving* n，于是算法的时间复杂度为O(saving \* n), 空间复杂度也是O(saving \* n).

后续我会继续推出大厂算法面试中的动态规划问题，希望这个系列能给大家带来真正的实惠。代码和数据文件的下载地址在这里
