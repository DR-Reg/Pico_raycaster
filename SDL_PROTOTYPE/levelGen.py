import sys,os
from PIL import Image
import numpy as np

# using 256-color
def err(*x): print("\033[38;5;196m",end='');print(*x);print("\033[0m",end='');
def war(*x): print("\033[38;5;220m",end='');print(*x);print("\033[0m",end='');
def ok(*x): print("\033[38;5;46m",end='');print(*x);print("\033[0m",end='');

def main(argc,argv):
    if argc < 2:
        err("No file name")
        return 1
    if not os.path.isfile(argv[1]):
        err("Invalid file name")
        return 1
    output_array_data = []
    w,h=0,0
    with Image.open(argv[1]).convert('RGBA') as im:
        im.show()
        w,h = im.size
        for i in range(h):
            for j in range(w):
                pix = im.getpixel((j,i))
                print(pix)
                cnum = ((pix[0]<<24) + (pix[1]<<16) + (pix[2]<<8) +pix[3])
                cnum = hex(cnum)
                print(cnum,end=' ')
                output_array_data.append(cnum)
            print()
    print(w,h)
    filename = argv[1].split('.')[0] + '.cam'
    symbol = filename.replace('.','_')
    arr_name = argv[1].split('.')[0] + '_arr'
    output_level_file = f"""
        #ifndef {symbol}
        #define {symbol}
        #define {arr_name}_W {w}
        #define {arr_name}_H {h} 
        unsigned int {arr_name}[{w}*{h}] =""" "{"+ ','.join(output_array_data) + """};
        #endif
    """
    with open(filename,'w+') as f:
        f.write(output_level_file)
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv),sys.argv))
