import sys
import os
import os.path
from lxml import etree
import collections



def create_folder(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)



def check_entry_dict(event_tokens, d):

    if event_tokens in d:
        return " ".join(d[event_tokens])
    else:
        return event_tokens


def extract_event_CAT(etreeRoot):
    """
    :param etreeRoot: ECB+/ESC XML root
    :return: dictionary with annotaed events in ECB+
    """

    event_dict = collections.defaultdict(list)

    for elem in etreeRoot.findall('Markables/'):
        for token_id in elem.findall('token_anchor'):
            if elem.tag.startswith("ACTION") or elem.tag.startswith(("NEG_ACTION")):
                event_mention_id = elem.get('m_id', 'nothing')
                token_mention_id = token_id.get('t_id', 'nothing')
                event_dict[event_mention_id].append(token_mention_id)

    return event_dict


def extract_corefRelations(etreeRoot, d):
    """
    :param etreeRoot: ECB+ XML root
    :return: dictionary with annotaed events in ECB+ (event_dict)
    :return:
    """

    relations_dict_appo = collections.defaultdict(list)
    relations_dict = {}

    for elem in etreeRoot.findall('Relations/'):
        target_element = elem.find('target').get('m_id', 'null')
        for source in elem.findall('source'):
            source_elem = source.get('m_id', 'null')
            if source_elem in d:
                val = "_".join(d[source_elem])
                relations_dict_appo[target_element].append(val) # coreferential sets of events

    for k, v in relations_dict_appo.items():
        for i in v:
            relations_dict[i] = v

    return relations_dict


def extract_plotLink(etreeRoot, d):
    """

    :param etreeRoot: ESC XML root
    :param d: dictionary with annotaed events in ESC (event_dict)
    :return:
    """

    plot_dict = collections.defaultdict(list)

    for elem in etreeRoot.findall('Relations/'):
        if elem.tag == "PLOT_LINK":
            source_pl = elem.find('source').get('m_id', 'null')
            target_pl = elem.find('target').get('m_id', 'null')
            relvalu = elem.get('relType', 'null')

            if source_pl in d:
                val1 =  "_".join(d[source_pl])
                if target_pl in d:
                    val2 = "_".join(d[target_pl])
                    plot_dict[(val1, val2)] = relvalu

    return plot_dict

def create_merged_files(ecbplus_original, ecbstart_new, outfile1, outfile2):

    """

    :param ecbplus_original: ECB+ CAT data
    :param ecbstart_new: ESC CAT data
    :param outfile1: event mention extended
    :param outfile2: event extended coref chain
    :return:
    """

    ecbplus = etree.parse(ecbplus_original, etree.XMLParser(remove_blank_text=True))
    root_ecbplus = ecbplus.getroot()
    root_ecbplus.getchildren()

    ecb_event_mentions = extract_event_CAT(root_ecbplus)
    ecb_coref_relations = extract_corefRelations(root_ecbplus, ecb_event_mentions)

    """
    ecbstar data
    """

    ecbstar = etree.parse(ecbstart_new, etree.XMLParser(remove_blank_text=True))
    ecbstar_root = ecbstar.getroot()
    ecbstar_root.getchildren()

    ecb_star_events = extract_event_CAT(ecbstar_root)
    ecbstar_events_plotLink = extract_plotLink(ecbstar_root, ecb_star_events)

    get_extended_mention = {}

    for k, v in ecbstar_events_plotLink.items():
        source = check_entry_dict(k[0], ecb_coref_relations).split(" ")
        target = check_entry_dict(k[1], ecb_coref_relations).split(" ")

        output = open(outfile1, "a")
        output.writelines(check_entry_dict(k[0], ecb_coref_relations) + "\t" + check_entry_dict(k[1], ecb_coref_relations) + "\t" + v + "\n")
        output.close()

        mention_pairs = [(x, y) for x in source for y in target]
        for i in mention_pairs:
            get_extended_mention[(k, i)] = v


    mention_elem = {}

    for k, v in get_extended_mention.items():
        first_elem = k[1][0].split("_")[0]
        second_elem = k[1][1].split("_")[0]
        if int(first_elem) < int(second_elem):
            mention_elem[k[1]] = v
        if int(first_elem) > int(second_elem):
            if v == "FALLING_ACTION":
                new_key = (k[1][1], k[1][0],)
                mention_elem[new_key] = "PRECONDITION"
            if v == "PRECONDITION":
                new_key = (k[1][1], k[1][0],)
                mention_elem[new_key] = "FALLING_ACTION"


    for k, v in mention_elem.items():
        output2 = open(outfile2, "a")
        output2.writelines(k[0] + "\t" + k[1] + "\t" + v + "\n")
        output2.close()


def merge_annotations(ecbtopic, ecbstartopic, outdir):

    """

    :param ecbtopic: ECB+ topic folder in CAT format
    :param ecbstartopic: ESC topic folder in CAT format
    :param outdir: output folder for evaluation data format
    :return:
    """

    if os.path.isdir(ecbtopic) and os.path.isdir(ecbstartopic) and os.path.isdir(outdir):
        if ecbtopic[-1] != '/':
            ecbtopic += '/'
        if ecbstartopic[-1] != '/':
            ecbstartopic += '/'
        if outdir[-1] != '/':
            outdir += '/'

        ecb_subfolder = os.path.dirname(ecbtopic).split("/")[-1]
        subfolder_coref = "coref_chain/"
        subfolder_mentions = "event_mentions_extended/"
        final_outdir_fullcoref = os.path.join(outdir, subfolder_coref, ecb_subfolder)
        final_outdir_mention = os.path.join(outdir, subfolder_mentions, ecb_subfolder)


        if final_outdir_fullcoref[-1] != '/':
            final_outdir_fullcoref += '/'

        if final_outdir_mention[-1] != '/':
            final_outdir_mention += '/'


        create_folder(final_outdir_fullcoref)
        create_folder(final_outdir_mention)


        for f in os.listdir(ecbtopic):
            if f.endswith('plus.xml'):
                ecb_file = f
                star_file = ecbstartopic + f + ".xml"

                outfile_coref = final_outdir_fullcoref + f
                outfile_mention = final_outdir_mention + f

                create_merged_files(ecbtopic + ecb_file, star_file, outfile_coref, outfile_mention)

            elif f.endswith('ecb.xml'):
                pass
            else:
                print("Missing file" + f)



def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 4:
        print("Usage python3 create_gold_document.py ECBplusTopic ECBstarTopic outfolder")
    else:
        merge_annotations(argv[1], argv[2], argv[3])


if __name__ == '__main__':
    main()
