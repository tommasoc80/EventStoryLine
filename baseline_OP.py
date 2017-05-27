import sys
import os
import os.path
from lxml import etree
import collections
from create_gold_document import create_folder
from itertools import combinations


"""
Baseline system  V1 for PLOT_LINK detection
- assume that all events are correctly identified and classified
- assume relations only in same sentences
- PLOT_LINK exists between every pair of events in the same sentence, excluding classes (NEG_)ACTION_REPORTING
and (NEG_)ACTION_CAUSTIVE (NEG_)ACTION_ASPECTUAL
"""

d = dict()

def check_path(filepath):
    if os.path.isdir(filepath):
        if filepath[-1] != '/':
            filepath += '/'

    return filepath



def extract_event_CAT(etreeRoot):

    event_dict = collections.defaultdict(list)
    not_good_events = ['ACTION_REPORTING', 'NEG_ACTION_REPORTING', 'ACTION_CAUSATIVE', 'NEG_ACTION_CAUSATIVE', 'ACTION_ASPECTUAL', 'NEG_ACTION_ASPECTUAL']

    for elem in etreeRoot.findall('Markables/'):
        for token_id in elem.findall('token_anchor'):
            if elem.tag.startswith("ACTION") or elem.tag.startswith(("NEG_ACTION")):
                if elem.tag not in  not_good_events:
                    event_mention_id = elem.get('m_id', 'nothing')
                    token_mention_id = token_id.get('t_id', 'nothing')
                    event_dict[event_mention_id].append(token_mention_id)

    return event_dict


def event_sentence(etreeRoot, d):
    """
    Identify events in the same sentence ONLY
    :param etreeRoot: CAT file ECB+
    :param d: dictionary annotated event mentions ECB+; key = markable id; v = token ids
    :return:
    """

    event_sentence_dict = collections.defaultdict(list)

    for elem in etreeRoot.findall('token'):
        sentence_id = elem.attrib.get("sentence", "null")
        token_match = elem.attrib.get("t_id", "null")

        for k, v in d.items():
            token_id = v[0]
            if token_match == token_id:
                event_sentence_dict[sentence_id].append(k)

    return event_sentence_dict


def generate_event_pairs(d):

    same_sentence_event_pairs = {}

    for k, v in d.items():
        if len(v) >= 2:
#            same_sentence_pairs = ["\t".join(map(str, comb)) for comb in combinations(v, 2)]
            same_sentence_pairs = [tuple(map(str, comb)) for comb in combinations(v, 2)]
            same_sentence_event_pairs[k] = same_sentence_pairs

    return same_sentence_event_pairs



def produce_output(inputf, outfile):

    ecbplus = etree.parse(inputf, etree.XMLParser(remove_blank_text=True))
    root_ecbplus = ecbplus.getroot()
    root_ecbplus.getchildren()

    event_mentions = extract_event_CAT(ecbplus)
    event_per_sentence = event_sentence(ecbplus, event_mentions)
    event_pairs = generate_event_pairs(event_per_sentence)

#    print(event_mentions)
    for k, v in event_pairs.items():
        for i in v:
            output = open(outfile, "a")
            output.writelines("_".join(event_mentions[i[0]]) + "\t" + "_".join(event_mentions[i[1]]) + "\tPRECONDITION"  + "\n")
            output.close()


def baseline_v1(input, outdir):

    input_dir = check_path(input)

    ecb_subfolder = os.path.dirname(input_dir).split("/")[-1]
    final_outdir = os.path.join(outdir, ecb_subfolder)

    if final_outdir[-1] != '/':
        final_outdir += '/'

    create_folder(final_outdir)

    output_dir = check_path(final_outdir)

    file_names_ecbplus = [(input_dir, f) for f in os.listdir(input_dir)]

    for f in file_names_ecbplus:
        if f[1].endswith("plus.xml"):
            outfile = output_dir + f[1].split(".xml")[0] + ".base.out"
            produce_output(input_dir + f[1], outfile)


def main(argv = None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        print("Usage python3 baseline_v1.py ECBplus outfolder")
    else:
        baseline_v1(argv[1], argv[2])


if __name__ == '__main__':
    main()