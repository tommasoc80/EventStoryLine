import sys
import os
import os.path
from lxml import etree
import collections
from create_gold_document import create_folder
from itertools import combinations, permutations, product
from baseline_OP import extract_event_CAT
from baseline_PPMI1 import cross_sentence, sentence_coocc
from collections import Counter



"""
Baseline system  PPMI-tanchor for PLOT_LINK detection
- assume that all events are correctly identified and classified
- assume relations in same TLINK container only for event pairs
- PLOT_LINK exists between every pair of events, excluding classes (NEG_)ACTION_REPORTING
and (NEG_)ACTION_CAUSTIVE (NEG_)ACTION_ASPECTUAL - if the PPMI score computed on the co-occurences per seminal
event is in the range on PPMI for th seed events.
Order of appearence in the pairs is assumed to be BEFORE --> RISING_ACTION
"""

def check_path(filepath):
    if os.path.isdir(filepath):
        if filepath[-1] != '/':
            filepath += '/'

    return filepath


def get_minimun(list_values):
    """
    function to obtain the min. score of ppmi
    :param list_values:
    :return:
    """
    min_score = min(list_values)

    return min_score


def get_maximum(list_values):
    """
    function to obtain the max score of ppmi
    :param list_values:
    :return:
    """

    max_score = max(list_values)
    return max_score


def normalize(value, min, max):
    """
    funtion to normalize ppmi scores
    :param value:
    :param min:
    :param max:
    :return:
    """
    norm_val = (float(value) - float(min))/(float(max) - float(min))

    return norm_val


def get_tanchor_cat(cat_etree):
    """
    Function to extract events which are in CONTAINS relation with time anchor
    - Merge data if different timex ids have same timex value
    :param cat_etree: lxml etree of file in CAT format - to be used only with GOLD events and timexes
    :return:
    """

    contained_events = collections.defaultdict(list)

    for anchored in cat_etree.findall('Relations/TLINK'):
        if anchored.attrib.get('relType', 'null') == "CONTAINS":
            source = "".join([elem.attrib.get('m_id', 'null') for elem in anchored.findall('source')])
            target = "".join([elem.attrib.get('m_id', 'null') for elem in anchored.findall('target')])
            contained_events[source].append(target)

    timex_values = collections.defaultdict(list)
    for timex in cat_etree.findall('Markables/'):
        if timex.tag.startswith("TIME_DA") or timex.tag.startswith(("TIME_OF")):
            timex_id = timex.attrib.get('m_id', 'null')
            timex_value = timex.attrib.get('value', 'null')
            timex_values[timex_value].append(timex_id)

    aggregate_events_per_timex = collections.defaultdict(set)

    for timex, event_list in contained_events.items():
        for timex_val, timex_id_list in timex_values.items():
            if timex in timex_id_list:
                aggregate_events_per_timex[timex_val].update(event_list)


    pairs_contained = set()
    for k, v in aggregate_events_per_timex.items():
        possible_pairs = list(product(v, repeat=2))
        pairs_contained.update(possible_pairs)

    return pairs_contained


def read_cat_naf(cat_etree, naf_etree):
    """
    function which read CAT and NAF data
    :param cat_etree: ecb+ file in CAT - extract eligible annotated events
    :param naf_etree: ecb+ naf file - extract event lemmas, event same sentence
    :return: cat_event, dict_event_lemma, dict_event_same_sentence: 3 dictionaries
    """

    cat_event = extract_event_CAT(cat_etree) # eligible events annotated in CAT; token ids


    dict_event_lemma = collections.defaultdict(list) # event lemmatized; key: eventID CAT; value: lemma(s) composing the event

    for elem in naf_etree.findall("terms/term"):
        for k, v in cat_event.items():
            if elem.attrib.get('id', 'null').replace('t', '') in v:
                dict_event_lemma[k].append(elem.attrib.get('lemma', 'null'))


    dict_event_same_sentence = {} # Events in the same sentence; key: sentence id; value: token id(s) composing the event

    for elem in naf_etree.findall("text/wf"):
        for k, v in cat_event.items():

            if elem.attrib.get('id', 'null').replace('w', '') in v:
                sentence_id = elem.attrib.get('sent', 'null')

                if sentence_id in dict_event_same_sentence:
                    list_value =  dict_event_same_sentence[sentence_id]
                    if k not in list_value:
                        list_value.append(k)
                else:
                    list_value = []
                    list_value.append(k)
                dict_event_same_sentence[sentence_id] = list_value


    return cat_event, dict_event_lemma, dict_event_same_sentence

def candidate_pairs_same_sent(list_ppmi_pairs, dict_pairs_data_same_sent, dict_event_lemmas, dict_event_same_sentence_naf, dict_event_tokes, dic_contains_event):
    """

    :param list_ppmi_pairs: pairs of events obtained using PPMI thresholds
    :param dict_pairs_data: the event pairs in the same sentence obtained from manual/automatically processed data; k = sentence id
    :param dict_event_lemmas: the event trigger lemmas
    :param dict_event_tokes: the event triggers (manual or automatically processed) with corresponding tokens
    :param dict_contains_event: events ids aggregated per tlink containment relation with a timex
    :return: list which contains candidate events (saved as tuple) in plot link relation
    """

    rel_pairs_appo = {}
    rel_pairs_check_contains = {}
    final_pairs = []

    for i in list_ppmi_pairs:
        for k, v in dict_pairs_data_same_sent.items():
            if i in v:
                source = i[0]
                for k1, v1 in dict_event_lemmas.items():
                    match_event = "_".join(v1)
                    if source == match_event: # get event id from lemma
                        eligible_event_id = k1 # event markable id
                        if eligible_event_id in dict_event_same_sentence_naf[k]: # restrict markable to target sentence
                            sentence_pair = i + (k, eligible_event_id,)
                            rel_pairs_appo[sentence_pair] = (dict_event_tokes[eligible_event_id],)

    for k, v in rel_pairs_appo.items():
        target = k[1]
        sentence = k[2]
        for k1, v1 in dict_event_lemmas.items():
            match_event = "_".join(v1)
            if target == match_event: # get event id from lemma
                eligible_target_id = k1
                if eligible_target_id in dict_event_same_sentence_naf[sentence]:
                    rel_pairs = v + (dict_event_tokes[eligible_target_id],)
                    rel_pairs_check_contains[k + (eligible_target_id,)] = rel_pairs

    for k, v in rel_pairs_check_contains.items():
        lemma_source, lemma_target, sentence, source_id, target_id = k
        match = (source_id, target_id,)
        if match in dic_contains_event:
            if v not in final_pairs:
                final_pairs.append(v)

    final_ordered_same = []
    for i in final_pairs:
        start = i[0][0]
        end = i[1][0]
        if int(start) > int(end):
            new_pair = (i[1], i[0],)
            if new_pair not in final_ordered_same:
                final_ordered_same.append(new_pair)
        else:
            new_pair = i
            if new_pair not in final_ordered_same:
                final_ordered_same.append(i)

    return final_ordered_same


def candidate_pairs_cross_sent(list_ppmi_pairs, dict_pairs_data_cross_sentence, dict_event_lemmas, dict_event_tokes, dic_contains_event):
    """

    :param list_ppmi_pairs: pairs of events obtained using PPMI thresholds
    :param dict_pairs_data_cross_sentence: the event pairs in the same sentence obtained from manual/automatically processed data; k = sentence id
    :param dict_event_lemmas: the event trigger lemmas
    :param dict_event_tokes: the event triggers (manual or automatically processed) with corresponding tokens
    :param dict_contains_event: events ids aggregated per tlink containment relation with a timex
    :return: list which contains candidate events (saved as tuple) in plot link relation
    """

    rel_pairs_appo = {}
    rel_pairs_check_contains = {}
    final_pairs_cross = []


    for pairs_id, freq in dict_pairs_data_cross_sentence.items():
        if pairs_id in dic_contains_event:
            source, target = pairs_id
            source_lemma = "_".join(dict_event_lemmas[source])
            target_lemma = "_".join(dict_event_lemmas[target])

            pair_norm = (source_lemma, target_lemma,)
            pair_inv = (target_lemma, source_lemma,)

            if pair_norm in list_ppmi_pairs:
                token_source = dict_event_tokes[source]
                token_target = dict_event_tokes[target]
                pairs_tokens_norm = (token_source, token_target,)
                if pairs_tokens_norm not in final_pairs_cross:
                    final_pairs_cross.append(pairs_tokens_norm)

            if pair_inv in list_ppmi_pairs:
                token_source = dict_event_tokes[source]
                token_target = dict_event_tokes[target]
                pairs_tokens_inv = (token_target, token_source,)
                if pairs_tokens_inv not in final_pairs_cross:
                    final_pairs_cross.append(pairs_tokens_inv)

    final_ordered_cross = []
    for i in final_pairs_cross:
        start = i[0][0]
        end = i[1][0]
        if int(start) > int(end):
            new_pair = (i[1], i[0],)
            if new_pair not in final_ordered_cross:
                final_ordered_cross.append(new_pair)
        else:
            new_pair = i
            if new_pair not in final_ordered_cross:
                final_ordered_cross.append(i)

    return final_ordered_cross


def read_input(catff, naff, pairs_same_sentence_ppmi, pairs_cross_sentence_ppmi):


    ecbplus = etree.parse(catff, etree.XMLParser(remove_blank_text=True))
    root_ecbplus = ecbplus.getroot()
    root_ecbplus.getchildren()

    doc_naf = etree.parse(naff, etree.XMLParser(remove_blank_text=True))
    naf_root = doc_naf.getroot()
    naf_root.getchildren()

    event_tokens, event_lemmas, event_same_sentence = read_cat_naf(ecbplus, naf_root)

    contains_event = get_tanchor_cat(ecbplus)

    event_lemma_pairs_same_sentence = sentence_coocc(event_lemmas, event_same_sentence)
    event_lemma_pairs_cross_sentence = cross_sentence(event_tokens)

    plot_link_same_sent = candidate_pairs_same_sent(pairs_same_sentence_ppmi,event_lemma_pairs_same_sentence,event_lemmas,event_same_sentence,event_tokens,contains_event)
    plot_link_cross_sent = candidate_pairs_cross_sent(pairs_cross_sentence_ppmi, event_lemma_pairs_cross_sentence, event_lemmas, event_tokens, contains_event)

    plot_link = plot_link_same_sent + plot_link_cross_sent

    plot_link_cleaned = []
    plot_link_cleaned = [i for i in plot_link if i not in plot_link_cleaned]

    return plot_link_cleaned

def produce_output(list_pairs, outfile):

    for i in list_pairs:
        output = open(outfile, "a")
        output.writelines("_".join(i[0]) + "\t" + "_".join(i[1]) + "\tPRECONDITION"  + "\n")
        output.close()


def baseline_v3(input_cat, input_naf, same_sentence_pairs, cross_sentence_pairs, outdir):

    input_dir_cat = check_path(input_cat)
    input_dir_naf = check_path(input_naf)

    ecb_subfolder = os.path.dirname(input_dir_cat).split("/")[-1]
    final_outdir = os.path.join(outdir, ecb_subfolder)

    if final_outdir[-1] != '/':
        final_outdir += '/'

    create_folder(final_outdir)
    output_dir = check_path(final_outdir)

    file_names_ecbplus = [(input_dir_cat, f) for f in os.listdir(input_dir_cat)]

    for f in file_names_ecbplus:
        if f[1].endswith("plus.xml.xml"):
            naff = input_dir_naf + f[1].split(".xml.xml")[0] + ".xml.naf.fix.xml"
            outfile = output_dir + f[1].split(".xml.xml")[0] + ".base.out"
            candidate_pairs = read_input(input_dir_cat + f[1], naff, same_sentence_pairs, cross_sentence_pairs)
            produce_output(candidate_pairs, outfile)



def read_ppmi_data(topic_ppmi):
    """
    function which read PPMI score for seminal events, filter pairs per ppmi, provide pairs
    INTERNAL = ppmi score computed using freq from the seminal events ECB+
    EXTERNAL = ppmi score computed using freq from Google Ngram
    :param topic_ppmi:
    :return:
    """

    ppmi_val_same = []
    ppmi_pairs_same = {}
    same_sentence_pairs = []
    same_sentence = topic_ppmi + "same_sentence_ppmi.sm"
    with open(same_sentence, 'r') as ppmi_same:
        for line in ppmi_same:
            line_stripped = line.strip()
            line_splitted = line_stripped.split("\t")

            ppmi_val_same.append(line_splitted[2])
            ppmi_pairs_same[(line_splitted[0], line_splitted[1],)] = line_splitted[2]

    min_ppmi = get_minimun(ppmi_val_same)
    max_ppmi = get_maximum(ppmi_val_same)

    for k, v in ppmi_pairs_same.items():
        ppmi_norm = normalize(v, min_ppmi, max_ppmi)

        if ppmi_norm >= 0.4 and ppmi_norm <= 0.763: # seeds + dev

            same_sentence_pairs.append(k)

    ppmi_val_cross = []
    ppmi_pairs_cross = {}
    cross_sentence_pairs = []
    cross_sentence = topic_ppmi + "full_corpus_ppmi.sm"
    with open(cross_sentence, 'r') as ppmi_cross:
        for line in ppmi_cross:
            line_stripped = line.strip()
            line_splitted = line_stripped.split("\t")

            ppmi_val_cross.append(line_splitted[2])
            ppmi_pairs_cross[(line_splitted[0], line_splitted[1],)] = line_splitted[2]

    min_ppmi_cross = get_minimun(ppmi_val_cross)
    max_ppmi_cross = get_maximum(ppmi_val_cross)

    for k, v in ppmi_pairs_cross.items():
        ppmi_norm = normalize(v, min_ppmi_cross, max_ppmi_cross)

        if ppmi_norm >= 0.4 and ppmi_norm <= 0.763: # seeds + dev

            cross_sentence_pairs.append(k)

    return same_sentence_pairs, cross_sentence_pairs



def main(argv = None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 5:
        print("Usage python3 baseline_v4.py ECB+_CAT ECB+_naf ppmi_topic outfolder")
    else:
        same_sentence, cross_sentence = read_ppmi_data(argv[3])
        baseline_v3(argv[1], argv[2], same_sentence, cross_sentence, argv[4])




if __name__ == '__main__':
    main()