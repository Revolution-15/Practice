#from typing import final
import bs4
from bs4 import BeautifulSoup as bs

content = []
# Read the XML file
with open("my_output_file.xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.read()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")

result = list(bs_content.find_all("tripinfo"))
#print(result)
#waiting_time = bs_content.find("tripinfo")
#print(result)
final=[]
for i in result:
    fop= i['waitingtime']
    final.append(float(fop))
    #print(fop)
denom=len(final)
num=sum(final)
ans= num/denom
print(ans)


