import random

import nltk
import re
import pickle

model_filename = 'hackathon/ml_utils/model/query_classifier_v4.pickle'
vec_filename = 'hackathon/ml_utils/model/query_vectorizer_v4.pickle'

gb = pickle.load(open(model_filename, 'rb'))
vectorizer = pickle.load(open(vec_filename, 'rb'))


def get_questions(text, threshold=0.75):
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


def process_transcript(interviewer_name):
    data_list = [('1.vtt', 'Sushant Gundla')]
    file_name, interviewer_name = random.choice(data_list)
    regex_all = r"""
(^[0-9]{2}[:][0-9]{2}[:][0-9]{2}[.,][0-9]{3})
[ ]-->[ ]
([0-9]{2}[:][0-9]{2}[:][0-9]{2}[.,][0-9]{3})
(?:\n<v\s)(.*?)(?:>)(.*?)(?:</v>)(?:\n\n|\Z)"""

    with open(f'hackathon/ml_utils/{file_name}') as f:
        transcript_text = f.read()

    matches = re.finditer(regex_all, transcript_text, re.VERBOSE | re.DOTALL | re.MULTILINE)

    conversation = []
    continual_conv = ''
    candidate_text = ''
    interviewer_text = ''
    questions_list = list()

    for matchNum, match in enumerate(matches, start=1):
        start, end, name, text = [match.group(group_num) for group_num in range(1, 5)]
        if matchNum == 1:
            previous_name = name

        if name == previous_name:
            continual_conv += text
        else:
            if previous_name == interviewer_name:
                questions = get_questions(continual_conv, 0.6)
                questions_list.extend(questions)
                interviewer_text += continual_conv
                conversation.append({'name': previous_name,
                                     'text': continual_conv,
                                     'questions': questions})
            else:
                conversation.append({'name': previous_name,
                                     'text': continual_conv})
                candidate_text += continual_conv
            previous_name = name
            continual_conv = text

    return questions_list, interviewer_text, candidate_text
