def print(*value,end="\n",sep=" ",times=0):
    import time,sys
    for i in value:
        for j in str(i):
            sys.stdout.write(j)
            time.sleep(float(times))
        if value.index(i)!=len(value)-1:
            sys.stdout.write(sep)
    sys.stdout.write(end)
def input(value="",times=0):
    import time,sys
    for i in str(value):
        sys.stdout.write(i)
        time.sleep(float(times))
    var=sys.stdin.readline()
    return var
def clear():
    print("\033[2J\033[0;0H",end="")
def check(title=None,choice=["选择1","选择2","选择3"],sort=False):
    import keyboard
    index=0
    while True:
        if title!=None:
            print(title)
        for c in choice:
            if c==choice[index]:
                print("\033[7m",end="")
                if sort==True:
                    print(choice.index(c)+1,".",end="",sep="")
                print(str(c)+"\033[0m")
            else:
                if sort==True:
                    print(choice.index(c)+1,".",end="",sep="")
                print(str(c))
        if keyboard.read_key()=="up":
            if index==0:
                index=len(choice)-1
            else:
                index-=1
        elif keyboard.read_key()=="down":
            if index==len(choice)-1:
                index=0
            else:
                index+=1
        elif keyboard.read_key()=="enter":
            return choice[index]
        print("\033[2J\033[00H",end="")
        continue