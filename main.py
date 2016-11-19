'''
Created on Nov 14, 2016

@author: fangyihao
'''
import preprocessor
import lexicon
def main():
    pp = preprocessor.Preprocessor()
    csvs = []
    csvs.extend(pp.do_udc())
    csvs.extend(pp.do_cmdc())
    csvs.extend(pp.do_wiki())
    csvs.extend(pp.do_bdc())
    lexicon.Lexicon(csvs)

if __name__ == "__main__":
    main()