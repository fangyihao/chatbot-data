import tokenizer
import os
import csv
import codecs
import re
import math
class Preprocessor:
    tk = tokenizer.Tokenizer()
    raw_dir = "./raw/"
    processed_dir = "./processed/"
    
    def create_csv_iter(self, file_path):
        """
        Returns an iterator over a CSV file. Skips the header.
        """
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            # Skip the header
            next(reader)
            for row in reader:
                yield row
    
    def do_udc(self):
        # udc raw csv file path for training
        trp = os.path.join(self.raw_dir, "udc/train.csv")
        # udc processed csv file path for training
        tpp = os.path.join(self.processed_dir, "udc_train.csv")
        
        with open(tpp, "w") as tpf:
            writer = csv.writer(tpf)
            for i, row in enumerate(self.create_csv_iter(trp)):
                context, utterance = row[:2]
                label = row[2]
                if (label == "1"):
                    writer.writerow([context, utterance])
                    
        # udc raw csv file path for validation
        vrp = os.path.join(self.raw_dir, "udc/valid.csv")
        # udc processed csv file path for validation
        vpp = os.path.join(self.processed_dir, "udc_valid.csv")
        
        with open(vpp, "w") as vpf:
            writer = csv.writer(vpf)
            for i, row in enumerate(self.create_csv_iter(vrp)):
                context, utterance = row[:2]
                writer.writerow([context, utterance])

        return tpp, vpp
    
    def do_cmdc(self):
        # movie line text file path
        mlp = os.path.join(self.raw_dir, "cmdc/movie_lines.txt")
        # movie conversation text file path
        mcp = os.path.join(self.raw_dir, "cmdc/movie_conversations.txt")
        # cmdc processed csv file path for training
        tpp = os.path.join(self.processed_dir, "cmdc_train.csv")
        # cmdc processed csv file path for validation
        vpp = os.path.join(self.processed_dir, "cmdc_valid.csv")

            
        movie_lines = {}
        with codecs.open(mlp, "r", encoding="windows-1252") as mlf:
            for line in mlf:
                m = re.search(r"(L[\d]+) \+\+\+\$\+\+\+ (u[\d]+) \+\+\+\$\+\+\+ (m[\d]+) \+\+\+\$\+\+\+ (.*) \+\+\+\$\+\+\+ (.*)", line)
                # print(m.group(1) + " | " + m.group(2) + " | " + m.group(3) + " | " + m.group(4) + " | " + m.group(5))
                movie_lines[m.group(1)] = m.group(5)
                
        #with codecs.open(mcp, "r", encoding="windows-1252") as mcf:
        #    num_lines = sum(1 for line in mcf)
        
        with open(tpp, "w") as tpf:
            with open(vpp, "w") as vpf: 
                twriter = csv.writer(tpf)
                vwriter = csv.writer(vpf)
                with codecs.open(mcp, "r", encoding="windows-1252") as mcf:
                    for l, line in enumerate(mcf):                   
                        m = re.search(r"(u[\d]+) \+\+\+\$\+\+\+ (u[\d]+) \+\+\+\$\+\+\+ (m[\d]+) \+\+\+\$\+\+\+ (.*)", line)
                        conversation = re.sub("[^L0-9 ]", "", m.group(4)).split()
                        for i, utterance_code in enumerate(conversation):
                            if i > 0:
                                context = ""
                                utterance = movie_lines[utterance_code]
                                j = i - 1
                                while j >= i - 1:
                                    context = movie_lines[conversation[j]] + context
                                    if context.strip() != "" and utterance.strip() != "":
                                        context = self.tk.utter_clean(context)
                                        utterance = self.tk.utter_clean(utterance)
                                        context_sentences = self.tk.sent_tokenize(context)
                                        utterance_sentences = self.tk.sent_tokenize(utterance)
                                        
                                        if re.match(r"^[Oo][Vv][Ee][Rr][\.\?! ]*$", context_sentences[len(context_sentences)-1]) and len(context_sentences) > 2:
                                            context_sentences = context_sentences[:len(context_sentences)-1]                                                    
                                        
                                        context_sentence = ' '.join(self.tk.word_tokenize(self.tk.sent_strip(context_sentences[len(context_sentences)-1])))
                                        utterance_sentence = ' '.join(self.tk.word_tokenize(self.tk.sent_strip(utterance_sentences[0])))
                                        if context_sentence != utterance_sentence:
                                            if math.floor(l % 10) != 1:
                                                twriter.writerow([context_sentence, utterance_sentence])
                                            else:
                                                vwriter.writerow([context_sentence, utterance_sentence])  
                                    j -= 2
    
        return tpp, vpp
    
    def do_wiki(self):
        # wiki dumps raw xml file path
        wrp = os.path.join(self.raw_dir, "wiki/enwiki-20161101-pages-articles.xml")
        # wiki dumps processed csv file path for training
        tpp = os.path.join(self.processed_dir, "wiki_train.csv")
        # wiki dumps processed csv file path for validation
        vpp = os.path.join(self.processed_dir, "wiki_valid.csv")
        
        REGEX_DEF = r"^((?P<article>The|A|An)\s*)?'''(?P<term>[^'\[\]\:\{\}]+?)'''\s*[^\-—_\:].+"
        
        with open(tpp, "w") as tpf:
            with open(vpp, "w") as vpf:
                with codecs.open(wrp, "r", encoding="utf-8") as wrf:
                    twriter = csv.writer(tpf)
                    vwriter = csv.writer(vpf)
                    awake = False
                    count = 0
                    for line in wrf:
                        m0 = re.search(r"\<text[^\>]*?\>", line)
                        if m0:
                            awake = True
                        if awake:
                            m = re.search(REGEX_DEF, line)
                            if m:
                                term = m.group("term")
                                article = m.group("article")
                                # eg. {{IPAc-en|ˈ|aɪ|n|_|ˈ|r|æ|n|d}}
                                line = re.sub(r"\{\{[^\{\}]+?\}\}", "", line)
                                line = re.sub(r"\{\{[^\{\}]+?\}\}", "", line)
                                line = re.sub(r"\{\{[^\{\}]+?\}\}", "", line)
                                # eg. ('''Afro-Asiatic''')
                                line = re.sub(r"\([^\(\)]*?\)", "", line)
                                line = re.sub(r"\([^\(\)]*?\)", "", line)
                                # tackle references
                                line = re.sub(r"\<ref[^\>]*?\>.+?</ref>", "", line)
                                line = re.sub(r"\<ref.*?/\>", "", line)
                                line = re.sub(r"&lt;ref.*?&gt;.+?&lt;/ref&gt;", "", line)
                                line = re.sub(r"&lt;.+?&gt;", "", line)
                                line = re.sub(r"&quot;", '"', line)
                                line = re.sub(r"&amp;nbsp;", ' ', line)
                                line = re.sub(r"&amp;", '&', line)
                                line = re.sub(r"&minus;", '-', line)
                                line = re.sub(r"&nbsp;", ' ', line)
                                # eg. [[veterinary medicine|Veterinary science]]
                                # eg. [[social sciences]]
                                line = re.sub(r"\[\[([^\]]+?\|)?(?P<term>[^\]]+?)\]\]", r"\g<term>", line)
                                line = re.sub(r"\[[^\]]+?\]", "", line)
                                line = re.sub(r"\,\s*\,", ' ', line)
                                line = re.sub(r"'''", "", line)
                                line = re.sub(r"''", "", line)
                                line = self.tk.sent_tokenize(line)[0]
                                
                                m1 = re.search(r"[\.]\s*$", line)
                                if m1:
                                    line = line.strip()
                                    tokens = self.tk.word_tokenize(line)        
                                    if len(tokens) > 5:
                                        utterance = ' '.join(tokens)
                                        context = "tell me the definition of " + ("" if not article else 'the ') + term + " ."
                                        context = ' '.join(self.tk.word_tokenize(context))
                                        if math.floor(count % 20) != 1:
                                            twriter.writerow([context, utterance])
                                        else:
                                            vwriter.writerow([context, utterance])
                                        awake = False
                                        count += 1
                            
        return tpp, vpp
        
    
    def do_bdc(self):
        return

