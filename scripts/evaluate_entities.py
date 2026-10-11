import ast
import pandas as pd


def parse_spans(value):
    """Convert CSV string representation back into a list of span dictionaries."""
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    return ast.literal_eval(value)


def span_set(spans):
    """
    Convert spans into comparable tuples:
    (start, end, label)
    """
    return {
        (span["start"], span["end"], span["label"])
        for span in spans
    }


def evaluate(true_spans_list, predicted_spans_list):
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for true_spans, predicted_spans in zip(
        true_spans_list,
        predicted_spans_list
    ):
        true_set = span_set(true_spans)
        predicted_set = span_set(predicted_spans)

        true_positives += len(true_set & predicted_set)
        false_positives += len(predicted_set - true_set)
        false_negatives += len(true_set - predicted_set)

    precision = (
        true_positives / (true_positives + false_positives)
        if true_positives + false_positives > 0
        else 0
    )

    recall = (
        true_positives / (true_positives + false_negatives)
        if true_positives + false_negatives > 0
        else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0
    )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


if __name__ == "__main__":
    df = pd.read_csv("data/processed/week3_evaluation_set.csv")

    true_spans = df["true_spans"].apply(parse_spans)
    predicted_spans = df["candidate_spans"].apply(parse_spans)

    results = evaluate(true_spans, predicted_spans)

    print("Entity Extraction Evaluation")
    print("----------------------------")
    print("True Positives:", results["true_positives"])
    print("False Positives:", results["false_positives"])
    print("False Negatives:", results["false_negatives"])
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall:    {results['recall']:.4f}")
    print(f"F1 Score:  {results['f1']:.4f}")
    