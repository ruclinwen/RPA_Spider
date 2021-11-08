import json

# with open('./3#球磨机.json', 'r', encoding='utf-8') as f:
# with open('./1#破碎机.json', 'r', encoding='utf-8') as f:
with open('./3-3#成球机.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data = data[0]['ChartElecData'][0]
dataArray = data['DataArray']
# timeArray = data['DataReportTime']
print(dataArray)

index_morning_low = 32 # 8:01
index_morning_high = 48 # 12:01
index_noon_normal = 68 # 17:01
index_night_high = 84 # 21:01
index_night_normal = 95 # 23:46

count_morning_low =0
count_morning_high = 0
count_noon_normal = 0
count_night_high = 0
count_night_normal = 0

# 早低谷
for i in range(0, index_morning_low+1):
    if dataArray[i] == '-':
        continue
    elif float(dataArray[i]) > 10:
        count_morning_low += 15
# 早高峰
for i in range(index_morning_low+1, index_morning_high+1):
    if dataArray[i] == '-':
        continue
    elif float(dataArray[i]) > 10:
        count_morning_high += 15
# 午平时
for i in range(index_morning_high+1, index_noon_normal+1):
    if dataArray[i] == '-':
        continue
    elif float(dataArray[i]) > 10:
        count_noon_normal += 15
# 晚高峰
for i in range(index_noon_normal+1, index_night_high+1):
    if dataArray[i] == '-':
        continue
    elif float(dataArray[i]) > 10:
        count_night_high += 15
# 晚平时
for i in range(index_night_high+1, index_night_normal+1):
    if dataArray[i] == '-':
        continue
    elif float(dataArray[i]) > 10:
        count_night_normal += 15

print(count_morning_low)
print(count_morning_high)
print(count_noon_normal)
print(count_night_high)
print(count_night_normal)



# print(timeArray)


# print("早低谷")
# print(timeArray.index('2021-11-02 08:01'))        # "早低谷":"", 32
# print("早高峰")
# print(timeArray.index('2021-11-02 12:01'))        # "早高峰":"", 48
# print("午平时")
# print(timeArray.index('2021-11-02 17:01'))        # "午平时":"", 68
# print("晚高峰")
# print(timeArray.index('2021-11-02 21:01'))        # "晚高峰":"", 84
# print("晚平时")
# print(timeArray.index('2021-11-02 23:46'))        # "晚平时":""  95


# minutes = 0
# for d in dataArray:
#     if d != '-' and float(d) > 10:
#         minutes += 15
# print(minutes)
# print(dataarray)



