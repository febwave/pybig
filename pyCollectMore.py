# -*- coding:utf-8 -*-
import os
import sys
import traceback
import pyScanner
    
 

    

if __name__ == '__main__':
    try:
        if (len(sys.argv)  != 2 ):
            raise Exception("parameter must include path")
        
        inputFolder = sys.argv[1]
        
        address = "192.168.237.144"
        port=27017
        
        scanner = pyScanner.InfoScanner(address,port)
        scanner.ClearCache()
        
        scanner.Scan(inputFolder)
        scanner.Close()
                        
    except Exception as exc:           
        print("app catch: %s\n" % ( exc));   
        info = traceback.format_exc()
        print(info)
    print("done"); 
          