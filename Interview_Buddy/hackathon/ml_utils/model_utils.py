import torch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
device = "cpu"
model_id = "gpt2"
grammar_model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
grammar_tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
max_length = grammar_model.config.n_positions
stride = 512
sid_obj = SentimentIntensityAnalyzer()


def get_ppl(sentence):
    encodings = grammar_tokenizer(sentence, return_tensors="pt")
    nlls = []
    for i in range(0, encodings.input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = min(i + stride, encodings.input_ids.size(1))
        trg_len = end_loc - i
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100
        with torch.no_grad():
            outputs = grammar_model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * trg_len
        nlls.append(neg_log_likelihood)
    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    return ppl.tolist()


def get_grammar_rating(sentence):
    ppl = get_ppl(sentence)
    rating_dict = {(0, 49): 5,
                   (50, 209): 4,
                   (210, 299): 3,
                   (300, 399): 2,
                   (400, 99999): 1}
    return [v for k, v in rating_dict.items() if k[0] <= ppl <= k[1]][0]


def sentiment_scores(sentence):
    sentiment_dict = sid_obj.polarity_scores(sentence)
    neg, new, pos = sentiment_dict['neg']*100, sentiment_dict['neu']*100, sentiment_dict['pos']*100
    if sentiment_dict['compound'] <= -0.05 :
        return 0
    else:
        return 1
