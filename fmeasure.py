

inputFile = open("assignment5_output.txt")

str1 = inputFile.read()
str2 = str1.replace(":", ",")
str3 = str2.replace("[", "")
str4 = str3.replace("]", "")


for lines in str4.splitlines():
    lines.split()
    print(lines)