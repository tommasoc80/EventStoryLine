README - Event Storyline Corpus v1.0

DIFFERENCES WRT v0.9: 
- data curation: consistency check of timex3 normalisation
- data curation: consistency check of TLINK annotation
- data curation: removal of wrong event tokens
- data curation: consistency check annotation of event extent



The corpus is structured in folders. Each folder corresponds to a topic from the ECB+ corpus. Only the files from the + portion of each topic/seminal event have been annotated.

Files are in CAT-XML labelled annotation format.

*Annotation Format and Layers*

ECB+ Annotation:
1) <token>: token of the document

2) <token> attributes: 
- t_id : token unique id; starts at 1
- sentence : sentence id; starts at 0
- number : token id per sentence; starts at 0

3) <ACTION_*> :event annotation layer from ECB+; tags contains the label of the event type. Father node: <Markables>

4) <NEG_ACTION_*> : event annotation layer from ECB+ for negated events; tags contains the label of the event type. Father node: <Markables>

5) <ACTION_*> and <NEG_ACTION_*> attributes:
- m_id : unique markable id

6) <TIME_*> : temporal expressions annotation layer; tags contain the label of the type of the temporal expression (DATE; SET; DURATION; OF_THE_DAY). Father node: <Markables>


7) <TIME_*> attributes:
- m_id : unique markable id
- DCT [TRUE|FALSE] : identify document creation time (DCT) temporal expressions; if a temporal expression is a DCT value is TRUE
- value : the normalized value of the temporal expressions; possible formats: YYYY-MM-DDThh:mm for dates, and time_of_the_date expressions: P*[granularity_of_timex] for durations and sets
- anchorTimeID : markable id of the anchor timex used to normalise the value/resolve the current temporal expressions

8) <token anchor> : identify the corresponding token(s) which compose the markable. Father nodes: <ACTION_*>, <NEG_ACTION_*>, <TIME_*>

9) <token anchor> attribute:
- t_id : id corresponding to the t_id attribute of the <token> tag


ESC Annotations:

1) <TLINK> : link tag used to annotate temporal relations. Father node: <Relations>

2) <TLINK> attributes:
- r_id : unique id of the link tag
- contextualModality : factuality value of the TLINK - not annotated at the momement. 
- relType : temporal relation value of the TLINK tag
 
3) <PLOT_LINK> link tag used to annotate explanatory relations. Father node: <Relations>


4) attributes:
- r_id : unique id of the link tag
- relType [PRECONDITION | FALLING_ACTION] : explanatory relation value of the TLINK tag
- SIGNAL : markable id of the event markable introducing an explicit causal relation
- CAUSES [TRUE|FALSE] : identify if the event source CAUSES the event target
- CAUSED_BY [TRUE|FALSE] : identify if the event source IS_CAUSED the event target

5) <source> : it identifies the event/temporal expression markable from which a link tag originates. Father node: <TLINK> <PLOT_LINK> 

6) <source> attribute:
- m_id : the markable id of the element from which the link originates

7) <target>: it identifies the event/temporal expression markable towards which a link tag lands

8) <target> attribute:
- m_id : the markable id of the element towards which the link lands

*Additional Notes on TLINK and PLOT_LINK*

The annotation of the TLINK value has been limited in this phase to relations between temporal expressions and events. The <source> of a TLINK is always a temporal expression; the <target> of a TLINK is always an event markable. The <value> of the link is complaint to this directionality; e.g.:

<TLINK relType=CONTAINS>: the temporal expressions CONTAINS the event markable
<TLINK relType=BEFORE>: the temporal expressions is BEFORE the event markable

*To select valid TLINK, check if the relType attribute is NOT empty.* 


The annotation of PLOT_LINK follows the order of presentation of events in the document. The <source> event is always mentioned before the <target> event in the text (i.e. the t_id of <source> event is smaller than the t_id of the <target> event). The value of the relType attribute is always assigned by assuming the directionality from <source> to <target>

<PLOT_LINK relType=PRECONDITION> the source is the PRECONDITION (RISING_ACTION) of the target: 
<PLOT_LINK relType=FALLING_ACTION> the source is the FALLING_ACTION/ of the target

Example of PLOT_LINK:

“Building collapsed after the earthquake”

source: collapsed
target: earthquake
<PLOT_LINK relType=FALLING_ACTION>

