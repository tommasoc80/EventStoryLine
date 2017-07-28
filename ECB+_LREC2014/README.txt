========================================
README file for the LREC-2014 release of:
(1) a new corpus component augmenting the EventCorefBank (ECB, Bejan and Harabagiu, 2010)
(2) annotation of the new corpus component and 
(3) new version of annotation on top of the ECB corpus.

Release: 1.0 (12/10/2014)
Created: December 10, 2014

===================
ECB+ corpus release
===================

Overview
--------
The ECB+ corpus is an extension to the EventCorefBank (ECB). A newly added corpus component consists of 502 documents that belong to the 43 topics of the ECB but that describe different seminal events than those already captured in the ECB. All corpus texts were found through Google Search and were annotated with mentions of events and their times, locations, human and non-human participants as well as with within- and cross-document event and entity coreference information. 
The 2012 version of annotation of the ECB corpus (Lee et al., 2012) was used as a starting point for re-annotation of the ECB according to the ECB+ annotation guideline.

The major differences with respect to the 2012 version of annotation of the ECB are: 
(a) five event components are annotated in text: 
- actions (annotation tags starting with ACTION and NEG)
- times (annotation tags starting with TIME)
- locations (annotation tags starting with LOC)
- human participants (annotation tags starting with HUMAN)
- non-human participants (annotation tags starting with NON_HUMAN)

(b) specific action classes and entity subtypes are distinguished for each of the five main event components resulting in a total tagset of 30 annotation tags based on ACE annotation guidelines (LDC 2008), TimeML (Pustejovsky et al., 2003 and Sauri et al., 2005)

(c) intra- and cross-document coreference relations between mentions of the five event components were established: 
- INTRA_DOC_COREF tag captures within document coreference chains that do not participate in cross-document relations; within document coreference was annotated by means of the CAT tool (Bartalesi et al., 2012)
- CROSS_DOC_COREF tag indicates cross-document coreference relations created in the CROMER tool (Girardi et al., 2014); all coreference branches refer by means of relation target IDs to the so called TAG_DESCRIPTORS, pointing to human friendly instance names (assigned by coders) and also to instance_id-s

(d) events are annotated from an "event-centric" perspective, i.e. annotation tags are assigned depending on the role a mention plays in an event (for more information see ECB+ references).

Important note on coreference annotation
----------------------------------------------
During the first stage of the annotation task the annotators marked mentions of event components and intra-document coreference between them. This phase resulted in annotation of a significant amount of events in text. The final stage of the annotation process in which cross-document coreference relations were established, was focused on annotation of two layers of seminal events captured in ECB+ (for an overview see the guideline document). 
In principle the annotation of mentions and coreference was aimed at a selection of sentences per document. Considering that some mentions outside of the selections were additionally annotated, we provide a list of selected sentences so that one can restrict the evaluation to the gold standard of only those sentences. This is to prevent skewed evaluation results due to system output for mentions that might not be annotated properly. A file with a list of selected sentences: ECBplus_coreference_sentences.csv is included in this release.

ECB+ 1.0 statistics
-------------------

Nr of topics: 43
Nr of texts: 982
Nr of annotated action mentions: 15003
Nr of annotated location mentions: 2205
Nr of annotated time mentions: 2412
Nr of annotated human participant mentions: 9621
Nr of annotated non human participant mentions: 3056
Nr of unique intra-document chains: 185
Nr of unique cross-document chains: 2319 intra-topic instances

The numbers reported here differ slightly from those presented in Cybulska and Vossen (2014). For the purpose of this release a final clean up round was performed on the data. 
1) We removed a number of mentions that were annotated twice (once in the CAT tool and then again in CROMER; at the time when the ECB+ annotation was performed the coders were not given a warning message in CROMER when annotating the same token for the second time, whether accidentally or to correct an earlier annotated mention). 
2) In the first version of the CROMER export format cross-document coreference chains were simply appended on top of the within document relations established during the intra-document round of the annotation. We removed any intra-document coreference links from the output that also make part of cross-document coreference chains hence the number of intra document relations went down significantly.
3) If a mention was linked to an instance that was assigned a different annotation tag than the linked mention, the assumption was made that it was a conscious choice of a coder to correct the annotation tag of a mention annotated wrongly. For this reason the annotation tag assigned to a cross-document instance, in case of tag disagreement, was assigned to mentions linked to the instance, replacing the annotation tags originally assigned during mention annotation.

ECB+ FORMAT
-----------
The ECB+ corpus is distributed in an XML format starting with tokenized corpus texts and  followed by stand-off annotations of event and entity mentions (linked to token IDs) succeeded by coreference annotations (operating on mention IDs). The ECB+ XML files follow the structure employed by the CAT and CROMER annotation tools (for details see CAT and CROMER tool user manuals). 
Note that the newly collected 'ecbplus' files contain links to pages where the corpus texts were found, tokenized as sentence zero. 

CONTENTS
--------
(-) 982 ECB+ corpus texts in the XML format: ECB+.zip
(-) ECB+ annotation guideline: NWR-2014-1.pdf
(-) Index of sentences annotated with coreference: ECBplus_coreference_sentences.csv
(-) LICENSEDATA.TXT
(-) COPYING-CC.TXT
(-) README.TXT
     
Acknowledgments
---------------
We are grateful for the contribution of the annotators Elisa Wubs and Melissa Dabbs.
Many thanks to Christian Girardi for his help in arranging the cross-document annotation by means of the CROMER tool.

The ECB+ corpus is described in:
--------------------------------
Agata Cybulska and Piek Vossen. 2014. Using a sledgehammer to crack a nut? Lexical diversity and event coreference resolution. In Proceedings of LREC 2014.

Agata Cybulska and Piek Vossen. Guidelines for ECB+ Annotation of Events and their Coreference. 2014. (http://www.newsreader-project.eu/files/2013/01/NWR-2014-1.pdf)

References 
----------
Linguistic Data Consortium. 2008. Ace (automatic content extraction) english annotation guidelines for entities, version 6.6 2008.06.13. Technical report, June. http://projects.ldc.upenn.edu/ace/docs/English-Entities-Guidelines v6.6.pdf.

Bartalesi Lenzi, Valentina, Moretti, Giovanni, and Sprugnoli, Rachele. 2012. CAT: the CELCT Annotation Tool. In Proceedings of LREC 2012.

Cosmin Bejan and Sanda Harabagiu. 2010. Unsupervised Event Coreference Resolution with Rich Linguistic Features. In Proceedings of ACL 2010, pages 1412–1422.

Agata Cybulska and Piek Vossen. 2014. Using a sledgehammer to crack a nut? Lexical diversity and event coreference resolution. In Proceedings of the 9th international conference on Language Resources and Evaluation (LREC2014)

Christian Girardi, Manuela Speranza, Rachele Sprugnoli and Sara Tonelli, 2014. CROMER: a Tool for Cross-Document Event and Entity Coreference. In Proceedings of the International Conference on Language Resources and Evaluation LREC 2014

Heeyoung Lee, Marta Recasens, Angel Chang, Mihai Surdeanu and Dan Jurafsky. 2012. Joint Entity and Event Coreference Resolution across Documents. In Proceedings of EMNLP 2012.

Pustejovsky, James, Castano, Jose, Ingria, Bob, Sauri, Roser, Gaizauskas, Rob, Setzer, Andrea, and Katz, Graham. 2003. Timeml: Robust specification of event and temporal expressions in text. In Proceedings of Computational Semantics Workshop (IWCS-5).

Saur´ı, Roser, Littman, Jessica, Knippen, Robert, Gaizauskas, Robert, Setzer, Andrea, and Pustejovsky, James. (2005). Timeml 1.2.1 annotation guidelines, October. http://timeml.org/site/publications/timeMLdocs/annguide 1.2.1.pdf.

LICENSE
-------
The annotation of the ECB+ corpus is made available under a Creative Commons Attribution 3.0 Unported License: http://creativecommons.org/licenses/by/3.0/legalcode
href="http://creativecommons.org/licenses/by/3.0/deed.en_US". See the file LICENSEDATA.TXT and COPYING-CC.TXT both available in the top-directory of this distribution.

The annotated content of this corpus is distributed without any warranty, express or implied. As the annotations were created for research purposes only, they have not been tested to the degree that would be advisable in any important application. All use of these annotations is entirely at the user's own risk.

Permission is granted for anyone to copy, use, or modify the annotations in this document collection for purposes of research or education, provided this copyright notice is retained, and note is made of any changes that have been made.

When using this resource in publications please cite:
Agata Cybulska and Piek Vossen. 2014. Using a sledgehammer to crack a nut? Lexical diversity and event coreference resolution. In Proceedings of the 9th international conference on Language Resources and Evaluation (LREC2014)

Note: The textual news documents annotated in this corpus are not copyrighted. Only the annotated content is subject to copyright.
====
