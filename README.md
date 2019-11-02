# EventStoryLine

This repository contains the following materials to extract storylines using the EventStoryLine Corpus (ESC):

- annotated data in (CAT-)XML format (folder: annotated_data). To visualise the data, you have to use CAT (Content Annotation Tool: http://dh.fbk.eu/resources/cat-content-annotation-tool). Ask for an account, it's free.
- annotated data in evaluation format, extending PLOT_LINK relations to include coreference relations (folder: evaluation_format)
- test data (folder: evaluation_format/test)
- Python3.* scripts for creating the evaluation format of the data, extracting baselines systems, evaluating baselines'output

Version 1.0 is available.

**UPDATES**

We have made available the following extensions to ESC:
- ESC v1.2: all plot link relations annotated using crowdsourcing and evaluated using <a href="http://crowdtruth.org">CrowdTruth</a>. Plot relations have been annotated only for events in the same sentence.
- ESC v1.5: plot link relations annotated by experts (i.e., all data in ESC v1.0) and crowd

ESC v1.2 is available in evaluation format only (folder: evaluation_format). Plot data in the evaluation format have been extended using coreference relations from ECB+. 
Complete documentation about the crowdsourcing experiments to obtain ESC v1.2 is available <a href="https://github.com/CrowdTruth/Crowdsourcing-StoryLines">here</a>.

ESC v1.5 is available in evaluation format (folder: evaluation_format) and (CAT-)XML (folder: annotated_data). Plot data in the evaluation format have been extended using coreference relations from ECB+.
PLOT_LINK relations in (CAT-)XML have been enriched with two new attributes *origin* (values: crowd|experts) and *validated* (values:TRUE|FALSE). 
The *validated* attribute signals if the PLOT_LINK has been validate or not. 

As for experiments, evaluation file format are stored in **/evaluation_format/test**:

1) if you want to evaluate only against the *experts*: use version 1.0
2) if you want to evaluate only against the *crowd*: use version 1.2
3) if you want to evaluate against *experts and crowd*: use version 1.5 



# References

- Caselli, T. and P. Vossen. 2016. <a href="http://aclweb.org/anthology/W/W16/W16-5708.pdf">The Storyline Annotation and Representation Scheme (StaR): A Proposal</a>. In Proceedings of the 2nd Workshop on Computing News Storylines Workshop (CNS 2016). Held in conjunction with EMNLP 2016
```
@inproceedings{caselli-vossen-2016-storyline,
    title = "The Storyline Annotation and Representation Scheme ({S}ta{R}): A Proposal",
    author = "Caselli, Tommaso  and
      Vossen, Piek",
    booktitle = "Proceedings of the 2nd Workshop on Computing News Storylines ({CNS} 2016)",
    month = nov,
    year = "2016",
    address = "Austin, Texas",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W16-5708",
    doi = "10.18653/v1/W16-5708",
    pages = "67--72",
}
```
- Caselli, T. and P. Vossen. 2017. <a href="http://aclweb.org/anthology/W/W17/W17-2711.pdf">The Event StoryLine Corpus: A New Benchmark for Causal and Temporal Relation Extraction</a>. In Proceedings of the Events and Stories in the News Workshop (EventStory 2017). Held in conjunction with ACL 2017
```
@inproceedings{caselli-vossen-2017-event,
    title = "The Event {S}tory{L}ine Corpus: A New Benchmark for Causal and Temporal Relation Extraction",
    author = "Caselli, Tommaso  and
      Vossen, Piek",
    booktitle = "Proceedings of the Events and Stories in the News Workshop",
    month = aug,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-2711",
    doi = "10.18653/v1/W17-2711",
    pages = "77--86",
}
```
- Caselli, T. and O. Inel. 2018. <a href="http://aclweb.org/anthology/W/W17/W17-2711.pdf">Crowdsourcing StoryLines: Harnessing the Crowd for Causal Relation Annotation </a>. In Proceedings of Events and Stories in the News Workshop (EventStory 2018). Held in conjunction with COLING 2018
```
@inproceedings{caselli2018crowdsourcing,
  title={Crowdsourcing StoryLines: Harnessing the Crowd for Causal Relation Annotation},
  author={Caselli, Tommaso and Inel, Oana},
  booktitle={Proceedings of the Workshop Events and Stories in the News 2018},
  pages={44--54},
  year={2018}
}
```

