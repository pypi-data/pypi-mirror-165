import csv
from os.path import join, splitext, basename

import spacy
import argparse

nlp = spacy.load("de_core_news_lg")


def tokenise(input_text: str):
    doc = nlp(input_text)
    result = []
    for sent_idx, sent in enumerate(doc.sents):
        result.append({"new_sentence": sent_idx})

        for token in sent:
            result.append({"token_id": token.i,
                           "token": token.text.replace("\n", " "),
                           "start_pos": token.idx,
                           "end_pos": token.idx + len(token.text)})
    return result


def main():
    parser = argparse.ArgumentParser("Tokenize text file and create output tsv.")
    parser.add_argument("input_file", help="Path to the input txt file.")
    parser.add_argument("output_folder", help="Path to the output folder where the output tsv will be saved.")

    args = parser.parse_args()
    in_file = open(args.input_file, "rt", encoding="utf-8")
    input_filename = splitext(basename(args.input_file))[0]
    input_text = in_file.read()
    tokens = tokenise(input_text)
    out_file = open(join(args.output_folder, f"{input_filename}_tokenized.tsv"), "wt", encoding="utf-8")
    writer = csv.writer(out_file, delimiter="\t", lineterminator="\n")
    writer.writerow(["id", "token", "start", "end"])
    for token in tokens:
        if 'new_sentence' in token:
            writer.writerow([f"# new sentence id {token['new_sentence']}\n"])
        else:
            writer.writerow(token)

    out_file.close()


if __name__ == "__main__":
    main()
