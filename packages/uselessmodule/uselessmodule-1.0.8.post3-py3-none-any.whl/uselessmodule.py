def deletestr(a,b): #문자열 삭제
    return a.replace(b,'')
    
def deletesymbol(a): #절댓값
    return (a**2)**0.5
    
def add(a,b): #더하기
    if 'str' in str(type(a)) or 'str' in str(type(b)):
        return str(a)+str(b)
    elif 'float' in str(type(a)) or 'float' in str(type(b)):
        return a+b
    elif 'int' in str(type(a)) or 'int' in str(type(b)):
        return a+b
        
def lastdigit(a): #마지막 글자
    return a[len(a)-1]
    
def dellastobj(a): #마지막 항목 삭제(리스트)
    a.remove(a[len(a)-1])
    
def average(a): #평균
    b=0
    for i in range(len(a)):
        b+=a[i]
    b=b/(len(a))
    return b
    
def mode(a): #최빈값
    d=[]
    b=[]
    b.append(a[0])
    for i in range (len(a)):
        c=0
        for j in range (len(b)):
            if a[i]==b[j]:pass
            else:
                c=c+1
        if c==len(b):
            b.append(a[i])
    for i in range (len(b)):
        d.append('')
    for i in range (len(b)):
        hm=0
        for j in range (len(a)):
            if b[i]==a[j]:
                hm=hm+1
        d[i]=hm
    hmm=max(d)
    largest=[]
    h=0
    for i in range (len(d)):
        if d[i]==d[0]:
            h=h+1
    if h==len(d):
        return 'There is no mode.'
    else:
        for i in range (len(d)):
            if max(d)==d[i]:
                largest.append(b[i])
        return largest
        
def median(a): #중앙값
    d=[]
    for i in range (len(a)):
        d.append(a[i])
    d.sort()
    if len(d)%2==0:
        b=(d[int((len(d))/2)]+d[int((len(d))/2-1)])/2
    elif len(d)%2==1:
        b=d[int((len(d)-1)/2)]
    return b
def deviation(a): #편차
    b=0
    for i in range (len(a)):
        b+=a[i]
    b=b/(len(a))
    c=[]
    for i in range (len(a)):
        c.append(a[i]-b)
    return c
def variance(a): #분산
    b=0
    for i in range (len(a)):
        b+=a[i]
    b=b/(len(a))
    c=[]
    for i in range (len(a)):
        c.append(a[i]-b)
    d=0
    for i in range (len(a)):
        d=d+((c[i])**2)
    d=d/5
    return d
def standevia(a): #표준편차
    b=0
    for i in range (len(a)):
        b+=a[i]
    b=b/(len(a))
    c=[]
    for i in range (len(a)):
        c.append(a[i]-b)
    d=0
    for i in range (len(a)):
        d=d+((c[i])**2)
    d=d/5
    d=d**(1/2)
    return d
def triangle(a,b): #삼각형 넓이
    c=a*b/2
    return c
def square(a,b): #사각형 넓이
    c=a*b
    return c
def circle(a): #원 넓이
    c=a*a*3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
    return c
def sphere(a): #구 넓이
    c=a*a*3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/3*4
    return c