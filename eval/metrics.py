"""Metrics: pass@k estimator (HumanEval) and binary classification metrics."""
from __future__ import annotations

from dataclasses import dataclass


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased pass@k estimator (Chen et al., 2021 / HumanEval).

    n = total number of generated samples; c = number of correct samples; k = parameter.
    Probability that at least one of k samples (drawn from the n) is correct.
    """
    if k > n:
        raise ValueError(f"k ({k}) cannot be greater than n ({n})")
    if n - c < k:
        return 1.0
    prob_all_fail = 1.0
    for i in range(n - c + 1, n + 1):
        prob_all_fail *= 1.0 - k / i
    return 1.0 - prob_all_fail


@dataclass
class ClassificationMetrics:
    tp: int  # expected buggy, predicted buggy
    fp: int  # expected correct, predicted buggy
    tn: int  # expected correct, predicted correct
    fn: int  # expected buggy, predicted correct
    unknown: int  # unclassifiable responses

    @property
    def total(self) -> int:
        return self.tp + self.fp + self.tn + self.fn + self.unknown

    @property
    def accuracy(self) -> float:
        return (self.tp + self.tn) / self.total if self.total else 0.0

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return self.tp / denom if denom else 0.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return self.tp / denom if denom else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0

    def as_dict(self) -> dict:
        return {
            "tp": self.tp,
            "fp": self.fp,
            "tn": self.tn,
            "fn": self.fn,
            "unknown": self.unknown,
            "accuracy": round(self.accuracy, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1": round(self.f1, 4),
        }


def classification_metrics(pairs: list[tuple[str, str]]) -> ClassificationMetrics:
    """Computes metrics from (expected, predicted) pairs, values in {buggy, correct}.

    Positive class = "buggy". "unknown" predictions are counted as errors.
    """
    tp = fp = tn = fn = unknown = 0
    for expected, predicted in pairs:
        if predicted == "unknown":
            unknown += 1
        elif expected == "buggy" and predicted == "buggy":
            tp += 1
        elif expected == "correct" and predicted == "buggy":
            fp += 1
        elif expected == "correct" and predicted == "correct":
            tn += 1
        elif expected == "buggy" and predicted == "correct":
            fn += 1
    return ClassificationMetrics(tp, fp, tn, fn, unknown)
