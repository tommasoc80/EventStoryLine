import os
import os.path
import sys
from baseline_OP import check_path
from collections import namedtuple

Result = namedtuple('Result', ['true_positive', 'false_positive', 'false_negative'])
Result_value = namedtuple('Result_value', ['true_positive', 'false_positive', 'false_negative'])

def true_positive(test, gold):
    counter_tp = 0
    for i in test:
        if i in gold:
            counter_tp += 1
    return counter_tp

def false_positives(test, gold):
    counter_fp = 0
    for i in test:
        if i not in gold:
            counter_fp +=1
    return counter_fp


def false_negatives(gold, test):
    counter_fn = 0
    for i in  gold:
        if i not in test:
            counter_fn += 1
    return counter_fn


def process_file(file_name):

    event_pairs = []
    event_pairs_values = []

    if os.path.isfile(file_name):

        with open(file_name) as fileObject:
            for line in fileObject:
                line_stripped = line.strip()
                line_splitted = line_stripped.split("\t")

                pairs = line_splitted[0] + "#" + line_splitted[1]
                pairs_value = line_splitted[0] + "#" + line_splitted[1] + "#" + line_splitted[2]

                event_pairs.append(pairs)
                event_pairs_values.append(pairs_value)

    return event_pairs, event_pairs_values


def compute_eval(goldf, systemf):

    event_pairs_gold, pairs_relation_gold = process_file(goldf)
    event_pairs_sys, pairs_relations_sys = process_file(systemf)


    tp_pairs = true_positive(event_pairs_sys,event_pairs_gold)
    fp_pairs = false_positives(event_pairs_sys,event_pairs_gold)
    fn_pairs = false_negatives(event_pairs_gold,event_pairs_sys)

    tp_pairs_value = true_positive(pairs_relations_sys,pairs_relation_gold)
    fp_pairs_value = false_positives(pairs_relations_sys,pairs_relation_gold)
    fn_pairs_value = false_negatives(pairs_relation_gold,pairs_relations_sys)


    scores = Result(true_positive=tp_pairs,
                   false_positive=fp_pairs,
                   false_negative=fn_pairs)


    scores_value = Result_value(true_positive=tp_pairs_value,
                   false_positive=fp_pairs_value,
                   false_negative=fn_pairs_value)


    return scores, scores_value

# print(result.false_positive)

def eval(golddir, systemdir):

    gold_check = check_path(golddir)
    system_check = check_path(systemdir)

    file_names_ecbplus = [(gold_check, f) for f in os.listdir(gold_check)]

    all_results = []
    for f in file_names_ecbplus:
        if f[1].endswith("plus.xml"):

            systemf = system_check + f[1].split(".xml")[0] + ".base3.out"
            result = compute_eval(gold_check + f[1], systemf)
            all_results.append(result)

    tp_pairs = (sum([i[0].true_positive for i in all_results]))
    fp_pairs = (sum([i[0].false_positive for i in all_results]))
    fn_pairs = (sum([i[0].false_negative for i in all_results]))

    tp_pairs_value = (sum([i[1].true_positive for i in all_results]))
    fp_pairs_value = (sum([i[1].false_positive for i in all_results]))
    fn_pairs_value = (sum([i[0].false_negative for i in all_results]))


    precision_pairs = float(tp_pairs) / (float(tp_pairs) + float(fp_pairs))
    recall_pairs = float(tp_pairs) / (float(tp_pairs) + float(fn_pairs))
    if precision_pairs == 0.0 and recall_pairs == 0.0:
        f1_pairs = 0.0
    else:
        f1_pairs = (2*((precision_pairs * recall_pairs)/(precision_pairs + recall_pairs)))

    print("Precision pairs baseline: " + str(precision_pairs) + "\n"
          + "Recall pairs baseline: " + str(recall_pairs) + "\n"
          + "F1 pairs baseline: " +  str(f1_pairs) + "\n")


    precision_pairs_value = float(tp_pairs_value) / (float(tp_pairs_value) + float(fp_pairs_value))
    recall_pairs_values = float(tp_pairs_value) / (float(tp_pairs_value) + float(fn_pairs_value))

    if precision_pairs_value == 0.0 and recall_pairs_values == 0.0:
        f1_pairs_values = 0.0
    else:
        f1_pairs_values = (2 * ((precision_pairs_value * recall_pairs_values) / (precision_pairs_value + recall_pairs_values)))

    print("Precision pairs-relType baseline: " + str(precision_pairs_value) + "\n"
      + "Recall pairs-relType baseline: " + str(recall_pairs_values) + "\n"
      + "F1 pairs-relType baseline: " + str(f1_pairs_values) + "\n")


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        print("Usage python3 eval_mentions.py gold system")
    else:
        eval(argv[1], argv[2])


if __name__ == '__main__':
    main()
