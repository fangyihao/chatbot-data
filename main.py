'''
Created on Nov 14, 2016

@author: ubuntu
'''
import preprocessor

def main():
    pp = preprocessor.Preprocessor()
    
    #pp.do_udc()
    #pp.do_cmdc()
    pp.do_wiki()
    pp.do_bdc()
    

if __name__ == "__main__":
    main()