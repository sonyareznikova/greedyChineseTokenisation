
# coding: utf-8

# In[1]:

import nltk


# In[2]:

nltk.download()


# In[4]:

from nltk.corpus import gutenberg


# In[5]:

text = gutenberg.raw("carroll-alice.txt")
print("\n".join(gutenberg.fileids()))


# In[6]:

import re


# In[7]:

t = re.split(" | \n | --", text)


# In[8]:

print(len(t))


# In[ ]:

nltk.download()


# In[14]:

len(nltk.word_tokenize(text))


# In[196]:

#reading the phrases
init_text_file = open("1-tok/chinesetext.utf8", "r")
init_text = []
for line in init_text_file:
    init_text.append(line[:len(line)-1])
print("init text")
print(init_text[0:5])
init_text_file.close()


# In[197]:

#reading the wordlist
wordlist_file = open("1-tok/chinesetrad_wordlist.utf8", "r")
wordlist = []
for line in wordlist_file:
    wordlist.append(line[:len(line)-1])
print("word list")
print(wordlist[:40])
wordlist_file.close()


# In[198]:

def greedy_tokenizer_chinese(n, text):
    tokens = []
    #iterating over all phrases
    for sentence in text:
        end_number = n
        #iterating over symbols
        this_sentence_tokens = []
        start_index = 0
        while (start_index < len(sentence)):
            if sentence[start_index:start_index+end_number] in wordlist:
                this_sentence_tokens.append(sentence[start_index:start_index+end_number])
                start_index += end_number
            else:
                while end_number > 0:
                    if sentence[start_index:start_index+end_number] in wordlist or end_number == 1:
                        this_sentence_tokens.append(sentence[start_index:start_index+end_number])
                        start_index += end_number
                        end_number = n
                        break
                    else:
                        end_number -= 1
        tokens.append(this_sentence_tokens)
    return tokens

        
    


# In[200]:

tokens = greedy_tokenizer_chinese(4, init_text)


# In[213]:

output_file = open("segmented.txt", "w")
for t in tokens:
    sentence = " ".join(t)
    output_file.write(sentence + "\n")

        


# In[195]:

#!/usr/bin/env python

from optparse import OptionParser#for command line options allows users to type -h or --help


parser = OptionParser(usage = '''%prog [-v] <your segmented text> <gold standard segmented text>\n
	Chinese Text Segmentation Evaluation Program
		This program compares <your segmented text> to the gold standard and outputs the accuracy.  
		These files should both be one sentence per line with words segmented by white space.\n
	-h option prints help''',version="%prog 0.1")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print differing lines to stdout")
(options, args) = parser.parse_args()

if (len(args)<2): parser.error("*** Must specify a segmented file AND a gold standard segmentaton file as arguments\n\n") 



#open the files
segmented_file=open(args[0])
gold_file=open(args[1])
#read all lines in files into lists
segmented_text=segmented_file.readlines() #read whole files into array
gold_text=gold_file.readlines()



if len(gold_text)!=len(segmented_text):
	exit("\nSorry! Segmentation file (%d) and Gold standard (%d) have different number of lines!  Is your segmented file one sentence per line?\n"%(len(segmented_text),len(gold_text)))

total_correct=0;
total_num_gold_words=0;

for i in range(len(segmented_text)):
	correct=0
	num_gold_words=0
	
	#gold_line=unicode(gold_text[i],'utf8')
	gold_line=gold_text[i]
	gold_words=set()  #create a set and fill it with the correct words
	for w in gold_line.split():
		gold_words.add(w)
		num_gold_words+=1
		
	#segmented_line=unicode(segmented_text[i],'utf8')
	segmented_line=segmented_text[i]
	for w in segmented_line.split():
		if w in gold_words:
			correct+=1;

	
	total_num_gold_words+=num_gold_words
	total_correct+=correct
	if(options.verbose and correct != num_gold_words):
		print("SEG:",segmented_line,"GOLD:",gold_line," line accuracy=%d%%"%(100*correct/num_gold_words))
		
		

print "Total segmentation accuracy is: %d%%"%(100*total_correct/total_num_gold_words)


# In[ ]:



