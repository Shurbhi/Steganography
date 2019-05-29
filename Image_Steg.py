from PIL import Image

def main():
    print("Press 1 for ENCODE /nPress 2 for DECODE/n")
    option = input()
    if(option=='1'):
        encode()
    elif(option=='2'):
        print("Hidden data "+ decode())
    else:
        print("Enter valid option")

def genData(data):

    newdata = []
    for i in data:
        newdata.append(format(ord(i),'08b'))   
    return newdata

def modPix(data , newimg):
    pixel = newimg.getdata()
    imdata = iter(pixel)
    for i in range(len(data)):
        pix = [value for value in imdata.__next__()[:3]+imdata.__next__()[:3]+imdata.__next__()[:3]]

        for j in range(0,8):
            if((data[i][j]=='0') and (pix[j]%2!=0)):
                pix[j] -=1
            elif((data[i][j]=='1')and(pix[j]%2==0)):
                pix[j] -=1
        if(i==len(data)-1):
            if(pix[-1]%2==0):
                pix[-1] -=1
        else:
            if(pix[-1]%2!=0):
                pix[-1] -=1
        
        pix = tuple(pix)
        yield pix[:3]
        yield pix[3:6]
        yield pix[6:9]


def encode():
    img = input("Enter the name of image with extension : ")
    image = Image.open(img , 'r')

    data = input("Enter the data to be encoded : ")
    if(len(data)==0):
        raise ValueError('Data is Empty')
    data = genData(data)
    newimg = image.copy()
    w = newimg.size[0]
    (x,y)=(0,0)

    for pixel in modPix(data,newimg):
        newimg.putpixel((x,y),pixel)
        if(x==w-1):
            x = 0
            y +=1
        else:
            x +=1
    newimg.save("Output.PNG")
def decode():
    img = input("Enter the name of image with extension : ")
    image = Image.open(img , 'r')
    data=''
    imData= iter(image.getdata())
    while(True):
        pixels = [value for value in imData.__next__()[ :3]+imData.__next__()[ :3]+imData.__next__()[:3]]
        binstr=''
        
        for i in pixels[0:8]:
            if (i%2==0):
                binstr +='0'
            else:
                binstr += '1'
        
        data += chr(int(binstr,2))
        if(pixels[-1]%2!=0):
            return data

if __name__=='__main__':
    main()