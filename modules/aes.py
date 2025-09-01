from pwn import *
def cpa(server):
    def sp(s):
        l=[]
        t=""
        c=0
        for i in s: 
            t+=i
            c+=1
            if c==32:
                l.append(t)
                t=""
                c=0
        return l
    ch="  abcdefghijklmnopqrstuvwxyz"
    ch+=ch.upper()
    ch+=".{}_-1234567890"
    f=b"AAAAAAAAAAAAAAAA"
    io = process(server)
    for q in range(4):
      for _ in range(16):
       try:     
        io.sendlineafter(b"Data?",(b"A"*(15-_)).hex().encode())
        l=sp(io.recvline().decode().split()[1])[q]
        for i in ch:
            io.sendlineafter(b"Data?",(f[-15:]+i.encode()).hex().encode())
            t=sp(io.recvline().decode().split()[1])
            if t[0] == l:
                f+=i.encode()
                print(f[16:],i)
                break
       except:
                pass
