num = int(input("enetr a no"))
sum = 0
count =0
while num>0:
    last_digit = num%10
    count = count+1
    sum = sum+last_digit
    num = num//10
    avg = sum/count
print(count)
print(sum)
print(avg)