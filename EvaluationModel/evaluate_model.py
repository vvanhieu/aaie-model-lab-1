import torch
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score as bert_score_fn
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from typing import List, Dict, Tuple


class EvaluateModel:
    def __init__(self, dataset: dict = None, model=None, tokenizer=None) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.results = {}
        self.device = ("cuda" if torch.cuda.is_available()
                       else "mps" if torch.backends.mps.is_available()
                       else "cpu")
        self.dataset = dataset

    def encode_labels(self, col: str) -> Tuple[List[int], List[int]]:
        try:
            int_labels = [int(x) for x in self.dataset[col]]
            label_names = sorted(set(int_labels))
        except ValueError:
            le = LabelEncoder()
            encoded_labels = le.fit_transform(self.dataset[col])
            int_labels = encoded_labels
            label_names = sorted(set(encoded_labels))
        return int_labels, label_names

    def bleu_score(self, reference_texts: List[str], generated_text: str) -> Dict[str, float]:
        ref_tokens = [ref.split() for ref in reference_texts]
        gen_tokens = generated_text.split()
        smoothie = SmoothingFunction().method1
        bleu = sentence_bleu(ref_tokens, gen_tokens, smoothing_function=smoothie)
        return {'bleu': bleu}

    def rouge_score(self, reference_texts: List[str], generated_text: str) -> Dict[str, float]:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = [scorer.score(ref, generated_text) for ref in reference_texts]
        avg_scores = {k: np.mean([s[k].fmeasure for s in scores]) for k in scores[0]}
        return avg_scores

    def bert_score(self, reference_texts: List[str], generated_text: str, model_type: str = 'bert-base-uncased') -> Dict[str, float]:
        P, R, F1 = bert_score_fn([generated_text], [reference_texts], model_type=model_type)
        return {
            'bertscore_precision': P.mean().item(),
            'bertscore_recall': R.mean().item(),
            'bertscore_f1': F1.mean().item()
        }

    def evaluate_classification_model(self, average: str = 'macro') -> Dict[str, float]:
        targets, label_names_target = self.encode_labels("labels")
        predictions, _ = self.encode_labels("predictions")
        acc = accuracy_score(targets, predictions)
        prec = precision_score(targets, predictions, average=average, zero_division=0)
        rec = recall_score(targets, predictions, average=average, zero_division=0)
        f1 = f1_score(targets, predictions, average=average, zero_division=0)
        cm = confusion_matrix(targets, predictions, labels=label_names_target)

        self.results = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "confusion_matrix": cm.tolist()
        }
        return self.results

    def evaluate_generative_model(self, metrics: List[str] = ['bleu', 'rouge', 'bertscore'],
                                  bert_model: str = 'bert-base-uncased') -> Dict[str, float]:
        refs = self.dataset['reference_texts']
        gens = self.dataset['generated_texts']
        all_scores = {}

        for ref, gen in zip(refs, gens):
            if 'bleu' in metrics:
                all_scores.update(self.bleu_score(ref, gen))
            if 'rouge' in metrics:
                all_scores.update(self.rouge_score(ref, gen))
            if 'bertscore' in metrics:
                all_scores.update(self.bert_score(ref, gen, bert_model))
        self.results = all_scores
        return self.results


def classify_text(model, tokenizer, device: str, text: str, few_shot_prompt: str, max_new_tokens: int = 10) -> str:
    """Run classification inference on a text using a given model + tokenizer + prompt"""
    if not few_shot_prompt:
        raise ValueError("few_shot_prompt cannot be empty")

    prompt = few_shot_prompt.format(text)
    input_ids = tokenizer(prompt, return_tensors="pt").to(device)
    output_ids = model.generate(**input_ids, max_new_tokens=max_new_tokens)
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    label = generated_text.split("Label:")[-1].strip().split()[0]
    return label
