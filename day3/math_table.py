import sys

number = int(sys.argv[1])
print( f'user given number is {number}')

for i in range(1,21):
    print('%d * %2d = %3d ' % (number,i, number*i))
    
    
'''
15*1=15

''' 