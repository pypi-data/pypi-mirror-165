from transformers import AutoTokenizer, CamembertTokenizer, AutoModelForSequenceClassification, pipeline, AutoModelForTokenClassification
import torch
import torch.nn.functional as F

class SentimentDetection:

    def __init__(self, device):
        #  pretrained "nlptown/bert-base-multilingual-uncased-sentiment" or "cmarkea/distilcamembert-base-sentiment"
        self.model_name = "cmarkea/distilcamembert-base-sentiment"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(device)
        self.tokenizer = CamembertTokenizer.from_pretrained(self.model_name)
        self.device = device

        self.tokenizerForLanguage = AutoTokenizer.from_pretrained("eleldar/language-detection")
        self.modelForLanguage = AutoModelForSequenceClassification.from_pretrained("eleldar/language-detection")

    def detectDominantLanguage(model, text):
        inputs = model.tokenizerForLanguage(text, return_tensors="pt")
        with torch.no_grad():
            logits = model.modelForLanguage(**inputs).logits
            labels = torch.argmax(logits, dim=1)
            result = [model.modelForLanguage.config.id2label[label_id] for label_id in labels.tolist()]     

        return result        

    def detectSentiment(model, text):
        # result2 = sentimentanalyzer(text)[0]
        # result = analyzer(text)[0]
        tokens = model.tokenizer.tokenize(text)
        token_ids = model.tokenizer.convert_tokens_to_ids(tokens)
        input_ids = model.tokenizer(text)

        # print(f'     Tokens: {tokens}')
        # print(f' Tokens IDs: {token_ids}')
        # print(f'  Input IDs: {input_ids}')

        batch = model.tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt').to(model.device)
        # print(batch)

        with torch.no_grad():
            outputs = model.model(**batch)
            # print(outputs)
            predictions = F.softmax(outputs.logits)
            # print(predictions)
            labels = torch.argmax(predictions, dim=1)
            # print(labels)
            result = [model.model.config.id2label[label_id] for label_id in labels.tolist()]

            # datainput.loc[index, "AWSSentiment"] = 'NEUTRAL'
            # datainput.loc[index, "Star"] = '3 stars'
        return result


    def save(model, save_directory):
        model.tokenizer.save_pretrained(save_directory)
        model.model.save_pretrained(save_directory)


class NerDetection:

    def __init__(self, device):
        #  pretrained "nlptown/bert-base-multilingual-uncased-sentiment" or "cmarkea/distilcamembert-base-sentiment"
        self.device = device
        self.model_name = "Jean-Baptiste/camembert-ner"
        self.model_name = "cmarkea/distilcamembert-base-ner"       
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_name).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, device=device)
        self.nlp = pipeline('ner', model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple", device=0)
       
        # dataset =   ("blbooks")
        # len(dataset)


    def detectNer(model, text):
       return model.nlp(text)

    def save(model, save_directory):
        model.tokenizer.save_pretrained(save_directory)
        model.model.save_pretrained(save_directory)