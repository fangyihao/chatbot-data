import nltk
import re
class Tokenizer:
    def utter_tokenize(self, utterance):
        words = []
    
        # Extract sentences
        sentences = self.sent_tokenize(utterance)
    
        # We add sentence by sentence until we reach the maximum length
        for i in range(len(sentences)):
            tokens = self.word_tokenize(sentences[i])
            for token in tokens:
                    words.append(token)
        
        return words
    
    def word_tokenize(self, sentence):
        d = {}
        d["'re"] = "are"
        d["n't"] = "not"
        d["'m"] = "am"
        d["'ll"] = "will"
        d["'ve"] = "have"
        tokens = nltk.word_tokenize(sentence)
        words =[]
        for token in tokens:
            token = token.lower()
            if token in d:
                words.append(d[token])
            else:
                words.append(token)
        return words
    
    def sent_tokenize(self, utterance):
        sentences = nltk.sent_tokenize(utterance)
        # correct the last sentence's segmentation
        fragment = ""
        last = len(sentences)
        for i in range(len(sentences)):
            m = re.match(r'^[ ]*["\?!\.\-*0-9]+[ ]*$', sentences[len(sentences) - 1 - i])
            if m:
                fragment = m.group(0) + fragment
                last = len(sentences) - 1 - i
            else:
                break
        if last > 0:
            sentences = sentences[:last]
            if fragment != "":
                sentences[last - 1] += fragment
        else:
            sentences = [fragment]
        
        fragment = ""    
        first = 0
        # correct the first sentence's segmentation
        for j in range(len(sentences)):
            m1 = re.search(r"[ \.]([A-Z]|No|Op|a\.k\.a|Sr)[\.]\s*$", sentences[j])
            if m1:
                fragment += sentences[j]
                first = j + 1
            else:
                break
        if first < len(sentences):
            sentences = sentences[first:]
            if fragment != "":
                sentences[0] = fragment + sentences[0]
        else:
            sentences = [fragment]
        return sentences
    
    def sent_strip(self, sentence):
        sentence = sentence.lstrip('.')
        sentence = sentence.strip('-* ')
        return sentence
    
    def utter_clean(self, utterance):
        utterance = re.sub(r'<[^>]+>([^<]+)</[^>]+>', r'\1', utterance)
        utterance = re.sub(r'&[lg]t;',' ', utterance)
        utterance = re.sub(r'[\+\* ]+', ' ', utterance)
        utterance = utterance.lstrip('. ')
        return utterance


