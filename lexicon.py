'''
Created on Nov 17, 2016

@author: fangyihao
'''
import csv
import tokenizer
import os
class Lexicon:
    _PAD = "_PAD"
    _GO = "_GO"
    _EOS = "_EOS"
    _UNK = "_UNK"
    _START_LEX = [_PAD, _GO, _EOS, _UNK]
    
    tk = tokenizer.Tokenizer()
    processed_dir = "./processed/"
    lex_path = os.path.join(processed_dir, "lexicon.csv")
    lex = {}
    def __init__(self, csv_file_paths):
        
        for file_path in csv_file_paths:
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    context, utterance = row[:2]

                    tokens = context.split() + utterance.split()
                    for word in tokens:
                        
                        if word in self.lex:
                            self.lex[word] += 1
                        else:
                            self.lex[word] = 1
                  
        lex_list = self._START_LEX + sorted(self.lex, key=self.lex.get, reverse=True)  
        
        for word in self._START_LEX:
            self.lex[word] = 0
        
        with open(self.lex_path, "w") as lf:
            writer = csv.writer(lf)
            for word in lex_list:
                writer.writerow([word, self.lex[word]])     
        
