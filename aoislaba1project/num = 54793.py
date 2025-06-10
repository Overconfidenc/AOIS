def sum_add_code (lis1:list,lis2:list):
    lis3=[0,0,0,0,0,0,0,0]
    if lis1[0]==lis2[0]:
        for i in range (7,-1,-1):
            lis3[i]=lis3[i]+lis1[i]+lis2[i]
            if (lis3[i])>1:
                lis3[i] -= 2
                lis3[i-1] += 1
        lis3[0]=lis1[0]
    return lis3
lis1=[0,0,1,1,0,0,0,0]
lis2=[0,0,0,1,0,0,0,0]
print(sum_add_code(lis1,lis2))