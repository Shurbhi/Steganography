import wave as w
import math
import numpy 
def main():
    print("Press 1 for ENCODE"+"\n"+"Press 2 for DECODE")
    option = input()
    if(option=='1'):
        encode()
    elif(option=='2'):
        print("Message : "+decode())
    else:
        print("Enter valid option")

def genData(data):

    newdata = []
    for i in data:
        newdata.append(format(ord(i),'08b'))   
    return newdata

def bin2dec(a):
    k=0
    for i in range(3):
        k=k*10+a[i]
    k=str(k)
    n= int(k,2)
    return n

def modFrames(arr,data):
    n = bin2dec(arr)
    n = 15-n
    if(data=='0'and arr[n]==1):
        arr[n]=0
    elif(data=='1'and arr[n]==0):
        arr[n]=1
    return arr

def decodeData(arr):
    n = bin2dec(arr)
    n = 15-n
    return str(arr[n])

def encode():
    audio = input("Enter the name of audio file(with extension) : ")
    data = input("Enter the message to be encoded : ")
    if(len(data)==0):
        raise ValueError("Data is empty")

    data = genData(data+'#')
    lenData = len(data)

    aud = w.open(audio,'r')    
    numFrames = aud.getnframes()

    if(lenData>numFrames):
        raise ValueError("Size of audio file is small")
    
    readFrames = aud.readframes(numFrames)
    frameArr = bytearray(readFrames)
    bitsArr = numpy.unpackbits(frameArr)
    
    count = 0
    newFrame = []
    for j in data:
        for i in j:
            l  = modFrames(bitsArr[count:count+16],i)
            for k in l:
                newFrame.append(k)
            count=count+16

    for i in bitsArr[count: ]:
        newFrame.append(i)
    newFrame=numpy.packbits(newFrame)
    finalFrames=bytearray(newFrame)
    
    newAud = w.open("output.wav",'w')
    newAud.setparams(aud.getparams())
    newAud.writeframes(finalFrames)
    newAud.close()
    aud.close()

def decode():
    audio = input("Enter the name of audio file(with extension) : ")
    
    aud = w.open(audio)
    numFrames = aud.getnframes()
    readFrames = aud.readframes(numFrames)
    frameArr = bytearray(readFrames)
    bitsArr = numpy.unpackbits(frameArr)
    
    count = 0
    data = ''
    while(True):
        binstr = ''
        for i in range(8):
            binstr += decodeData(bitsArr[count:count+16])
            count = count+16
        
        char = chr(int(binstr,2))
        print(binstr)
        print(char)
        if(char=='#'):
            return data       
        data +=char
        i=0

if __name__ == "__main__":
    main()

