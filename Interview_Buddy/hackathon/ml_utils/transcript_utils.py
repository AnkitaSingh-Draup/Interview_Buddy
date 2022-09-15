import nltk

import re
import pickle

model_filename = 'model/query_classifier.pickle'
vec_filename = 'model/query_vectorizer.pickle'

gb = pickle.load(open(model_filename, 'rb'))
vectorizer = pickle.load(open(vec_filename, 'rb'))


def get_questions(text, threshold = 0.75):
    sent_text = nltk.sent_tokenize(text)
    last_index = -1
    questions = []
    
    ques = ''
    for i, sent in enumerate(sent_text):
        if gb.predict_proba(vectorizer.transform([sent]))[0][1] > threshold:
            if i == last_index+1:
                ques += sent
            else:
                questions.append(ques)
                last_index = i
                ques = sent
    questions.append(ques)
    if '' in questions:
        questions.remove('')
    return questions

regex_all = r"""
(^[0-9]{2}[:][0-9]{2}[:][0-9]{2}[.,][0-9]{3})
[ ]-->[ ]
([0-9]{2}[:][0-9]{2}[:][0-9]{2}[.,][0-9]{3})
(?:\n<v\s)(.*?)(?:>)(.*?)(?:</v>)(?:\n\n|\Z)
   """

regex_time = r"(^[0-9]{2})[:]([0-9]{2})[:]([0-9]{2})"


interviewer_name = "Shubhodeep Bhowmick"

with open('Transcript_5e9e8636-c21a-4b65-a83a-495385c63915.vtt') as f:
    vtt_file = f.read()

matches = re.finditer(regex, vtt_file, re.VERBOSE | re.DOTALL | re.MULTILINE)

conversation = []
continual_conv = ''


for matchNum, match in enumerate(matches, start=1):    
    if matchNum < 1000000:
        start, end, name, text = [match.group(group_num) for group_num in range(1,5)]
#         s_hr, s_min, s_sec = [next(re.finditer(regex_time, start, re.VERBOSE | re.DOTALL | re.MULTILINE)).group(group_num) for group_num in range(1,4)]
#         e_hr, e_min, e_sec = [next(re.finditer(regex_time, end, re.VERBOSE | re.DOTALL | re.MULTILINE)).group(group_num) for group_num in range(1,4)]
        
        if matchNum == 1:
            previous_name = name
        
        if name == previous_name:
            continual_conv += text
        else:
            if previous_name == interviewer_name:
                questions = get_questions(continual_conv, 0.6)
                conversation.append({'name': previous_name,
                                         'text': continual_conv,
                                         'questions': questions})
            else:
                conversation.append({'name': previous_name,
                                     'text': continual_conv})

#             sent_text = nltk.sent_tokenize(continual_conv)
#             [print(i,':', sent) for i, sent in enumerate(sent_text) if gb.predict_proba(vectorizer.transform([sent]))[0][1] > 0.6]
#             print()
            
            previous_name = name
            continual_conv = text