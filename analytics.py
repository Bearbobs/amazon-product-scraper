import json
import re
import statistics
from scipy.stats import kurtosis

with open('data/data.json') as json_file:
    data = json.load(json_file)

output={}

star_list=[]
price_list=[]
for i in data:
    temp=re.search(r'(.*?)out', i["rating"])
    if temp!=None:
        temp=temp.group(1).strip()
        star_list.append(float(temp))
    temp=i["price"].split("\u20b9\u00a0")[1].strip().replace(',','')
    if temp!=None:
        price_list.append(float(temp))

output["star_min"]=min(star_list)
output["star_max"]=max(star_list)
output["star_mean"]=statistics.mean(star_list)
output["star_median"]=statistics.median(star_list)
output["star_kurtosis"]=kurtosis(star_list)

print(output)
