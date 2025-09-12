# Automatic Linguistic Annotation of Large Scale L2 Databases: The EF-Cambridge Open Language Database (EFCamDat)

Jeroen Geertzen, Theodora Alexopoulou, and Anna Korhonen University of Cambridge

# 1. Introduction

Naturalistic learner productions are an important empirical resource for SLA research. Some pioneering works have produced valuable second language (L2) resources supporting SLA research.1 One common limitation of these resources is the absence of individual longitudinal data for numerous speakers with different backgrounds across the proficiency spectrum, which is vital for understanding the nature of individual variation in longitudinal development.2

A second limitation is the relatively restricted amounts of data annotated with linguistic information (e.g., lexical, morphosyntactic, semantic features, etc.) to support investigation of SLA hypotheses and obtain patterns of development for different linguistic phenomena. Where available, annotations tend to be manually obtained, a situation posing immediate limitations to the quantity of data that could be annotated with reasonable human resources and within reasonable time. Natural Language Processing (NLP) tools can provide automatic annotations for parts-of-speech (POS) and syntactic structure and are indeed increasingly applied to learner language in various contexts. Systems in computer-assisted language learning (CALL) have used a parser and other NLP tools to automatically detect learner errors and provide feedback accordingly.3 Some work aimed at adapting annotations provided by parsing tools to accurately describe learner syntax (Dickinson & Lee, 2009) or evaluated parser performance on learner language and the effect of learner errors on the parser. Krivanek and Meurers (2011) compared two parsing methods, one using a hand-crafted lexicon and one trained on a corpus. They found that the former is more successful in recovering the main grammatical dependency relations whereas the latter is more successful in recovering optional, adjunction relations. Ott and Ziai (2010) evaluated the performance of a dependency parser trained on native German (MaltParser; Nivre et al., 2007) on 106 learner answers to a comprehension task in L2 German. Their study indicates that while some errors can be problematic for the parser (e.g., omission of finite verbs) many others (e.g., wrong word order) can be parsed robustly, resulting in overall high performance scores.

In this paper we have two goals. First, we introduce a new English L2 database, the EF Cambridge Open Language Database, henceforth EFCAMDAT. EFCAMDAT was developed by the Department of Theoretical and Applied Linguistics at the University of Cambridge in collaboration with EF Education First, an international educational organization. It contains writings submitted to Englishtown, the online school of EF accessed daily by thousands of learners worldwide. EFCAMDAT stands out for two reasons: its size and rich individual longitudinal data from learners with a wide variety of L1 backgrounds. The magnitude of EF operations has allowed us to build a resource of considerable size, currently containing half a million scripts from 85K learners summing up 33 million words. Crucially, the progress of individual learners can be followed over time. As new data come in, the database will continue to grow allowing investigation of longitudinal development of larger numbers of learners. EFCAMDAT is an open access resource available to the research community via a web-based interface at http://corpus.mml.cam.ac.uk/efcamdat/, subject to a standard user agreement.

Our second goal is to evaluate parser performance on EFCAMDAT data. Our study provides users of EFCAMDAT with information on the accuracy of the automatically obtained morpho-syntactic annotations that accompany EFCAMDAT data. The parser performance is evaluated using a set of manually annotated EFCAMDAT data. We provide information on the effect of different types of errors on parsing as well as aspects of learner language that are challenging for automated linguistic analysis. This article is structured as follows: section 2 elaborates on the nature and characteristics of the learner data. The syntactic annotations are evaluated and discussed in section 3. We conclude in section 4.

# 2. Data characteristics

EFCAMDAT consists of essays submitted to Englishtown, the online school of EF Education First, by language learners all over the world (Education First, 2012). A full course in Englishtown spans 16 proficiency levels aligned with common standards such as TOEFL, IELTS, and the Common European Framework of Reference for languages (CEFR) as shown in Table 1.

Table 1: Englishtown skill levels in relation (indicative) to common standards   

<html><body><table><tr><td>Englishtown</td><td>1-3</td><td>4-6</td><td>7-9</td><td>10-12</td><td>13-15</td><td>16</td></tr><tr><td>Cambridge ESOL</td><td>-</td><td>KET</td><td>PET</td><td>FCE</td><td>CAE</td><td>-</td></tr><tr><td>IELTS</td><td></td><td>&lt;3</td><td>4-5</td><td>5-6</td><td>6-7</td><td>&gt;7</td></tr><tr><td>TOEFL iBT</td><td>-</td><td>-</td><td>57-86</td><td>87-109</td><td>110-120</td><td>-</td></tr><tr><td>TOEIC Listening &amp; Reading</td><td>120-220</td><td>225-545</td><td>550-780</td><td>785-940</td><td>945</td><td>-</td></tr><tr><td>TOEIC Speaking &amp; Writing</td><td>40-70</td><td>80-110</td><td>120-140</td><td>150-190</td><td>200</td><td>-</td></tr><tr><td>CEFR</td><td>A1</td><td>A2</td><td>B1</td><td>B2</td><td>C1</td><td>C2</td></tr></table></body></html>

Learners are allocated to proficiency levels after a placement test when they start a course at $\mathrm { E F ^ { 4 } }$ or through successful progression through coursework. Each of the 16 levels contains eight lessons, offering a variety of receptive and productive tasks. EFCAMDAT consists of scripts of writing tasks at the end of each lesson on topics like those listed in Table 2.

Table 2: Examples of essay topics at various levels. Level and unit number are separated by a colon.   

<html><body><table><tr><td>ID</td><td>Essay topic</td><td>ID</td><td>Essay topic</td></tr><tr><td>1:1</td><td>Introducing yourself by email.</td><td>7:1</td><td>Giving instructions to play a game</td></tr><tr><td>1:3</td><td>Writing an online profile</td><td>8:2</td><td>Reviewing a song for a website.</td></tr><tr><td>2:1</td><td>Describing your favourite day</td><td>9:7</td><td>Writing an apology email</td></tr><tr><td>2:6</td><td>Telling someone what you&#x27;re doing</td><td>11:1</td><td>Writing a movie review</td></tr><tr><td>2:8</td><td>Describing your family&#x27;s eating habits</td><td>12:1</td><td>Turning down an invitation</td></tr><tr><td>3:1</td><td>Replying to a new penpal</td><td>13:4</td><td>Giving advice about budgeting</td></tr><tr><td>4:1</td><td>Writing about what you do</td><td>15:1</td><td>Covering a news story</td></tr><tr><td>6:4</td><td>Writing a resume</td><td>16:8</td><td>Researching a legendary creature</td></tr></table></body></html>

Given 16 proficiency levels and eight units per level a learner who starts at the first level and completes all 16 proficiency levels would produce 128 different essays. Essays are graded by language teachers;

learners may only proceed to the next level upon receiving a passing grade. Teachers provide feedback to learners using a basic set of error markup tags or through free comments on students’ writing. Currently, EFCAMDAT contains teacher feedback for $36 \%$ of scripts.

The data collected for the first release of EFCAMDAT contain 551,036 scripts (with 2,897,788 sentences, and 32,980,407 word tokens) written by 84,864 learners. We currently have no information on the L1 backgrounds of learners.5 Information on nationality is, thus, used as the closest approximation to L1 background. EFCAMDAT contains data from learners from 172 nationalities. Table 3 shows the spread of scripts across the nationalities with most learners.6

Table 3: Percentage and number of scripts per nationality of learners   

<html><body><table><tr><td>Nationality</td><td>Percentage of scripts</td><td>Number of Scripts</td></tr><tr><td>Brazilians</td><td>36.9%</td><td>187,286</td></tr><tr><td>Chinese</td><td>18.7%</td><td>96,843</td></tr><tr><td>Russians</td><td>8.5%</td><td>44,187</td></tr><tr><td>Mexicans</td><td>7.9%</td><td>41,115</td></tr><tr><td>Germans</td><td>5.6%</td><td>29,192</td></tr><tr><td>French</td><td>4.3%</td><td>22,146</td></tr><tr><td>Italians</td><td>4.0%</td><td>20,934</td></tr><tr><td>Saudi Arabians</td><td>3.3%</td><td>16,858</td></tr><tr><td>Taiwanese</td><td>2.6%</td><td>13,596</td></tr><tr><td> Japanese</td><td>2.1%</td><td>10,672</td></tr></table></body></html>

Few learners complete all of the proficiency levels. For many, their start or end of interacting with Englishtown fell outside the scope of the data collection period for the first release of EFCAMDAT. More generally, many learners only complete portions of the program. Nevertheless, around a third of learners (around 28K) have completed three full levels, corresponding to a minimum of 24 scripts.7 Only 500 learners have completed every unit from level one to six (accounting for at least 48 scripts).

Characterizing scripts quantitatively is difficult, because of the variation across topics and proficiency levels. Texts range from a list of words or a few short sentences to short narratives or articles. As learners become more proficient they tend to produce longer scripts. On average, scripts count seven sentences $\mathrm { S D } = 3 . 8$ ). Sample scripts are shown in Figure 1.

# 3. Syntactic annotations

# 3.1. Background and motivation

Many learner corpora have been annotated for errors and more recently for lemmas, parts of speech (POS), and grammatical relations (D´ıaz-Negrillo, Meurers, Valera, & Wunsch, 2010; Granger, 2003; Granger, Kraif, Ponton, Antoniadis, & Zampa, 2007; Ludeling, Walter, Kroymann, & Adolphs,¨ 2005; Meurers, 2009; Nicholls, 2003). Information on POS and grammatical relations allows the investigation of morpho-syntactic and also some semantic patterns. Such annotation typically involves two distinct levels, one providing category information (POS) and a second level providing syntactic structure, typically represented by phrase structure trees or grammatical dependencies between pairs of words.

As mentioned in the introduction, NLP tools can provide annotations automatically. One critical question is how learner errors and untypical learner production patterns affect parsing performance. POS taggers rely on a combination of lexical, morphological, and distributional information to provide the most likely POS annotation for a given word. But in learner language these three sources of information may be pointing to different outcomes (D´ıaz-Negrillo et al., 2010; Meurers, 2009; Ragheb & Dickinson,

![](img/a974cb6a2f8cfe7f3b1ff44b88b933f315511c18794e93d77c7bdcc8f9522e58.jpg)  
Figure 1: Three typical scripts, in which learners are asked to introduce themselves (1), describe their favourite day (2), and review a song for a website (3).

2011). In particular, D´ıaz-Negrillo et al. (2010) discuss a range of mismatches, as for instance between form and distribution (1-a) and stem and distribution (1-b). In (1-a) the verb want lacks 3rd person agreement. Thus, the distributional information corresponds to a 3rd-person verbal form tag (VBZ) while the morphological information is consistent with a bare verb form tag (VB). Similarly, the stem choice is of category noun, but in (1-b), the morphological and distributional information would indicate verbal tags.

(1) a. ...if he want to know this... b. ... to be choiced for a job...

D´ıaz-Negrillo et al., 2010, ex.9,16

Turning to syntax, learners often make syntactic mistakes, e.g., word order mistakes involving misplaced adverbs as in it brings rarely such connotations (Granger et al., 2007).

Results discussed in D´ıaz-Negrillo et al., 2010 and Meurers, 2009 indicate that taggers show robustness to many such mismatches and that good accuracy scores can be obtained for POS tagging. There is, though, the question of whether native annotations are suitable descriptions of learner language. Ragheb and Dickinson (2011) rightly argue that annotating learner language with existing tools is an instance of Bley-Vroman’s comparative fallacy. Bley-Vroman (1989) has argued for the need to analyse learner language in its own right rather than with categories from the target language. In a series of papers, Ragheb and Dickinson (2011) and Dickinson and Ragheb (2009, 2011), propose an annotation model that seeks to capture the properties of learner language rather than to superimpose native tags. They propose a multilayered annotation scheme where distributional and morphological information is annotated separately. For example, the annotation for (1-a) would just record the mismatch. Under this view (a good part of) errors are mismatches between stem, morphological and distributional information. Errors affect not only POS tagging but can also reduce the probability of parses (Wagner & Foster, 2009). At the same time, parsers show robustness to many errors, e.g., word order (Ott & Ziai, 2010).

In the following sections we present results on parser performance for EFCAMDAT data and discuss the effect of learner errors on parsing.

# 3.2. Methodology

To evaluate how parsers for well-formed English perform on learner language, a sample from EFCAMDAT data was annotated with POS tags and syntactic structure. The Penn Treebank Tagset (Marcus, Marcinkiewicz, & Santorini, 1993) was used for POS annotation because it is widely used and offers a relatively simple and straightforward set of tags. It comprises 36 POS tags, as listed in the Appendix, and features a further 12 tags to mark punctuation and currency symbols. Syntactic structure has been annotated in the form of dependency relations between a pair of words, where one word is analyzed as a head (governor) and the other as a dependent (Tesniere & Fourquet, 1959). The main \` feature of this annotation scheme is the absence of constituency and phrasal nodes. Because of its less hierarchical structure, this framework is particularly suitable for manual annotation. An example is illustrated in Figure 2 and compared with a more standard phrase structure annotation.8

![](img/5f3d942b769b43dbdf6c52ef5e94a8fd21dd16a016533e4dd8e2b31f5f802ec3.jpg)  
Figure 2: A sentence in phrase structure (left) and dependency relations (right) with the dependency graph (top right) and corresponding column-based coding (bottom right).

A set of 1,000 sentences (11,067 word tokens) from EFCAMDAT was pseudo-randomly sampled with equal representation from all 16 proficiency levels and five of the best represented nationalities (i.e., Chinese, Russian, Brazilian, German, and Italian). These sentences were then tagged and parsed using Penn Treebank POS tags and a freely available state-of-the-art parser (Stanford parser; Klein & Manning, 2003). Two trained linguists manually corrected the automatically annotated evaluation set (500 sentences each). They used the grammatical relations of the Stanford Dependency scheme (De Marneffe & Manning, 2008) and worked with collapsed representations.9 The annotators marked learner errors tagging/parsing errors manually on words. They used two error tags, L for learner error and $\mathrm { P }$ for POS tagging and parsing errors, and provided a corrected version. Each annotator corrected 500 sentences. Prior to the annotation, they both corrected a set of 100 additional sentences with corresponding parses in order to measure inter-annotator agreement. Inter-annotator agreement turned out to be $9 5 . 3 \%$ on the full combination of POS, attachment to the head, and relation type. All disagreements were subsequently discussed with a third linguist to reduce any incidental mistakes, which increased the final inter-annotator agreement to $9 7 . 1 \%$ .

One of our goals was to evaluate the effect of learner errors on automated annotation, since errors are rather frequent. In our sample of 1,000 sentences, $3 3 . 8 \%$ contains at least one learner error. These learner errors are mostly spelling and capitalization ones, but also involve morphosyntactic and semantic irregularities or missing words. Some characteristic examples are illustrated in (2) and (3), which show learner errors together with corrections suggested by the annotators.

(2) a. I often have meetings ar go on business trips correction: and b. I finally ger an offer as an secretary in a company correction: get, a c. At night i go to bed correction: I d. Because to whome could i talk English in Germany? correction: whom, I e. I can’t swim, sometimes I like take a walk correction: to take f. If you would like to work, like to volunteer, call to number 80000 correction: delete ‘to’

(3) a. To help me with my vocabulary I note down all the words that I cannot recognize in notebook which enclosed with a sentence for reference correction: delete ‘which’ and replace ‘enclosed’ with ‘along’ b. It must be by far the exhilarating experience correction: the most exhilarating c. you must can my house soon correction: be able to d. to motivate people to reaching aims they would not reach theirselves correction: reach, themselves e. I’ll think about change my career correction: changing

Examples in (2) and (3) give a sense of the range of difficulties. Some errors are more likely to affect the parser than others. For instance, the spelling error in (2-b) where we have ger instead of get may not be as damaging as the spelling error in (2-a) where instead of and we have ar. This is because it is easier to recover a verbal category than a conjunction based on distributional evidence. Similarly whome instead of whom in (2-d) may also have an effect on the parser as it may miss a wh-category. The errors in (2-e-f) could be viewed as subcategorization ones and it is conceivable that the parser can still recover the correct dependencies.10

The effect of an error like (3-a) is rather unpredictable. Such cases illustrate how challenging it can be to describe some errors. Under one analysis, this sentence may just have a missing ‘is’ (which is enclosed....). However, our annotator preferred to rephrase. Cases like this require a systematic analysis of the learner’s productions to establish whether such errors are an instance of a more general pattern (e.g., auxiliary BE omission) or not. It is hard to see how such issues can be addressed by error annotation schemes.

The errors in (3-b-c) are semantic. Though interesting from an SLA perspective, they are unlikely to affect the parser. The pair in (3-d-e) both involve an erroneous verbal form. But the effect on the parser can be different. The parser may establish the correct dependency between reaching and motivate in (3-d). But in (3-e) it may analyze change as a noun rather than a verbal category.

Our data also contain many cases of the mismatches discussed by D´ıaz-Negrillo et al. (2010) as illustrated in (4).

(4) a. but the young woman was catched at the hair by a passer-by correction: caught, by b. please find enclose correction: enclosed

c. I am also certificated in cardio kickboxing correction: certified

Figure 3 illustrates a case where a learner error results in a parsing error. The sentence contains what looks like a preposition in place of an article, and the parser analyzes the item as a preposition and postulates the wrong dependency, where the noun sweater is the object of the preposition. The annotator corrects the direct object interpretation for the noun, and provides corrections as shown in Figure 3.

![](img/a7f6e054dc648845bb1bb31bb9161b019196eda1be92a497fc5d9e43a26b7d87.jpg)  
Figure 3: Example of a parsed sentence with learner and parsing errors (above), and manual corrections (below).

To assess the parser’s performance on L2 English and the effect of errors, it is crucial to know if parsing errors occur in the context of well-formed or ungrammatical sentences. Manual annotation of learner errors and parsing errors allows us to identify the following three scenarios:

1. learner error without a pos-tagging/parsing error;   
2. learner error with a pos-tagging/parsing error;   
3. a pos-tagging/parsing error without a learner error.

The first scenario may arise with semantic or morphological errors at word level that are not stron enough to affect the grammatical rule selection during parsing. Such a situation is depicted by Figure 4, in which the surface form of what appears to be intended as the verb get is correctly identified as such.

![](img/25cdb0121ae0001734f233aa3035d6e198ad1a8cee616238c94ea39b57b02989.jpg)  
Figure 4: Learner errors (in black) without a parsing error.

The second scenario is one in which a learner error causes a parsing error, as exemplified in Figure 5. Both ‘mop’ and ‘de’ are identified as foreign words and interpreted to be compound nouns (see also Figure 3).

Finally, parsers are not always accurate even with grammatically correct native English. The third scenario, therefore, involves a parsing error without a learner error as illustrated in Figure 6 where the word ‘loundry’ is misanalysed as a subject of ‘afternoon’ rather than an object of the verb ’does’ and ‘afternoon’ as a clausal complement rather than a modifier of the verb. Our goal here is to evaluate how often each of these scenarios is realized.

![](img/387ef710e575747ea708f122a2a113de7fd6eec3b09a8f536297ffb09d242220.jpg)  
Figure 5: Learner error with a parsing error (both in black).

![](img/cd6ff6be1fc09aca7b7aecce182ab810094f58c8edadbd5ca316368c3c38700f.jpg)  
Figure 6: Parsing error (in black) without learner error.

# 3.3. Results

Parser errors can be measured in various ways. Measurement may focus on errors per sentence or per word. Evaluation can also consider different aspects of annotation, POS tagging, dependency attachment, and dependency relation label. For instance Figure 5 contains POS errors for ‘mop’ and ‘de’ which are tagged as foreign words. This tagging error results in an attachment and labelling error since these two words are misanalysed as dependents of ‘floor’ in a noun compound dependency. This is a case where a POS error has a knock-on effect on the syntactic annotation. But parsing errors may also appear without a POS error. For instance, in Figure 6 the dependency between the verb and ‘afternoon’ is mislabelled as ‘xcomp’ (clausal complement) instead of modification, but this misanalysis is not triggered by a tagging error.

Parsing performance involving dependency relations is typically evaluated using labelled attachment score (LAS) and unlabelled attachment score (UAS). The former metric is the proportion of word tokens that are assigned both the correct head and the correct dependency relation label. The latter is the proportion of word tokens that are assigned the correct head regardless of what dependency relation label is assigned. A correct assignment of a dependency relation has to match the (manually) annotated relation exactly.11 Over all our sentences, the Stanford parser scored $8 9 . 6 \%$ LAS and $9 2 . 1 \%$ UAS as shown in Table 4. This slightly exceeds results on Wall Street Journal (WSJ; Marcus et al., 1993) news text parsing at $8 4 . 2 \%$ LAS, $8 7 . 2 \%$ UAS (Cer, Marneffe, Jurafsky, & Manning, 2010). This measure does not include POS tagging. POS tagging also reaches a high accuracy of $9 6 . 1 \%$ . When POS tagging errors were included in the scoring this yielded $8 8 . 6 \%$ LAS and $9 0 . 3 \%$ UAS.

To get an idea of how parsing errors are distributed across sentences, accuracies were also computed at sentence level. In our sample of 1,000 sentences, $5 4 . 1 \%$ was without any labelled attachment error and $6 3 . 2 \%$ is without any unlabelled attachment error. As for POS tagging, $7 3 . 1 \%$ of sentences was error free.

The high accuracy scores indicate that the parser can recover the correct syntactic structure despite learner errors as long as the likelihood of the overall dependency tree is sufficiently high (see Figure 4). To assess how the presence of learner errors affected parsing performance, we split the 1,000 sentences into two sets, the $3 3 . 8 \%$ that contain at least one learner error and the remaining $6 6 . 2 \%$ without learner errors, and parsed and evaluated them separately. For convenience, we will refer to these sets as the learner error absent (LA) set and learner error present (LP) set, respectively. Scores are shown in Table 4. As expected, the difference in parsing accuracy between sentences with and without learner errors is considerable.

Table 4: Accuracy scores for sentences with and without learner errors   

<html><body><table><tr><td>Sentences</td><td>LAS</td><td>UAS</td></tr><tr><td>All</td><td>89.6%</td><td>92.1%</td></tr><tr><td>Without learner error</td><td>92.6%</td><td>95.0%</td></tr><tr><td>With at least one learner error</td><td>83.8%</td><td>87.4%</td></tr></table></body></html>

In the LP set, 593 words were directly associated to a learner error. Of those words, $4 9 . 2 \%$ received an incorrect POS or syntactic dependency assigned. Note that a small percentage of these $4 9 . 2 \%$ words would also have received erroneous assignments in absence of the learner error. To obtain more detailed information on the effect of learner errors, we assessed the nature of assignment errors to words. To this purpose, we selected in each set of sentences the words with assignment errors, and looked at the error type, which can relate to POS, head attachment, and the relation. Table 5 shows percentages of assignment error types for individual words, with and without learner errors. POS tagging errors represent $2 1 . 6 \%$ for the LP set. Not surprisingly, in $53 \%$ of erroneous assignments, a POS error causes also a head and a relation error, which on themselves occur considerably less frequent. The picture is rather different for the LA set. POS tagging errors in isolation account for only $7 . 3 \%$ while head+relation errors in absence of POS tagging errors are the most challenging category for this set, accounting for $4 1 . 4 \%$ of all assignment errors. In sum, learner errors affect primarily category assignment (POS tagging), and as a consequence, assignment of a dependency head and labelling of the relation. Nonetheless, automatic assignment is still accurate for $5 0 . 8 \%$ words in the LP set, indicating robustness to a significant number of learner errors.

Table 5: Error types of assignment errors in the presence of a learner error (based on 292 words of the LP set) and in the absence of a learner error (based on 572 words of the LA set), where ‘only’ means that all other aspects are correctly assigned.   

<html><body><table><tr><td>Error type</td><td>LA set</td><td>LP set</td></tr><tr><td>POs only</td><td>7.3%</td><td>21.6%</td></tr><tr><td>Head only</td><td>18.7%</td><td>2.4%</td></tr><tr><td>Relation only</td><td>16.3%</td><td>3.4%</td></tr><tr><td>Head + Relation only</td><td>41.4%</td><td>8.6%</td></tr><tr><td>POS + Head + Relation</td><td>9.3%</td><td>53.1%</td></tr></table></body></html>

Our next question was whether proficiency interacts with parser performance. Our sample was balanced for proficiency, but it could have been possible that at lower proficiency levels accuracy scores were significantly lower.12 We, thus, calculated scores for levels 1-6 and 7-16 and 10-16 separately, shown in Table 6. Accuracy scores are higher at higher proficiency levels but the effect seems small.

Table 6: Accuracy scores for different levels of proficiency   

<html><body><table><tr><td>Proficiency level</td><td>LAS</td><td>UAS</td></tr><tr><td>L1-6</td><td>89.0%</td><td>91.5%</td></tr><tr><td>L7-16</td><td>90.2%</td><td>92.4%</td></tr><tr><td>L10-16</td><td>91.4%</td><td>93.2%</td></tr></table></body></html>

As some dependencies are more challenging for the parser to recover than others, we also measured accuracy for individual grammatical dependencies. The evaluation measures used were precision, recall, and $F _ { 1 }$ . Recall measures how many of the annotated instances of a specific grammatical relation are correctly recovered by the parser. Precision measures how many of the instances labelled by the parser as being a specific grammatical relation are actually correct. The $\mathrm { F _ { 1 } }$ -score is the harmonic mean of precision and recall.13 The grammatical relations that occur at least five times in the evaluation data are listed in Table 7, together with the evaluation metrics and the absolute frequency.

![](img/df7734ca17a9ede4db2b63112cdbeb4cb1040af62b61bb16a752c80a43b9fce0.jpg)  
Figure 7: Error matrix containing percentages of the most frequent errors in assigning dependency relation labels.

As can be seen in Table 7, only a few grammatical relations scored below $90 \%$ $\mathrm { F _ { 1 } }$ . Adjectival complements (acomp, $7 3 . 3 \% \mathrm { F _ { 1 } } ,$ ) suffered from a rather low recall, as did clausal subjects (csubj, $5 7 . 1 \% \mathrm { F } _ { 1 , }$ ) and appositional modifiers (appos, $7 5 . 8 \% \mathrm { F _ { 1 } }$ ).

We next examined the most frequent parser ‘confusions’. The erroneous assignment of dependency relation labels is quantified using the error matrix in Figure 7, in which each column represents the assigned label by the parser, while each row represents the actual label. Only the more frequent errors (i.e., occurring at least four times) have been included, and together account for $38 \%$ of all parsing errors. The number at the end of each row is the absolute frequency at which the label on that row was erroneously assigned, with each cell containing the percentage of this number that got erroneously assigned by the corresponding column label.

One prominent parsing error was misanalysis of direct objects (107 cases). In $37 \%$ of these cases, the direct object was mis-analysed as a nominal subject. This case is illustrated with Figure 6, in which the noun laundry is wrongly assigned to the nominal head afternoon as subject. Few errors were expected, such as noun compounds (NN) with (ADJECTIVAL MODIFIER), or a few indirect objects (IOBJ) with direct objects (DOBJ) or nominal subjects (NSUBJ), but there are no clear outliers. Only the DEPENDENT relation (DEP) has been used often as it is the most underspecified category in the dependency scheme.

Table 7: Grammatical relations occurring at least five times. Precision (Prec), recall $( R e c )$ and $F _ { 1 }$ scores are listed for each grammatical relation, together with its absolute frequency $( \# G R s )$ .   

<html><body><table><tr><td colspan="6"></td></tr><tr><td>Relation</td><td>Description</td><td>Prec</td><td>Rec</td><td>F</td><td>#GRs</td></tr><tr><td>root</td><td>root</td><td>95.2</td><td>97.2</td><td>96.2</td><td>999</td></tr><tr><td>dep</td><td>dependent</td><td>92.5</td><td>65.7</td><td>76.8</td><td>210</td></tr><tr><td>aux</td><td>auxiliary</td><td>98.0</td><td>98.9</td><td>98.4</td><td>646</td></tr><tr><td>auxpass</td><td> passive auxiliary</td><td>96.1</td><td>96.1</td><td>96.1</td><td>78</td></tr><tr><td>cop</td><td> copula</td><td>96.6</td><td>98.7</td><td>97.6</td><td>313</td></tr><tr><td>arg</td><td>argument</td><td></td><td></td><td></td><td></td></tr><tr><td>agent</td><td>agent</td><td>100.0</td><td>87.5</td><td>93.3</td><td></td></tr><tr><td>comp</td><td>complement</td><td></td><td></td><td></td><td></td></tr><tr><td>acomp</td><td>adjectival complement</td><td>78.6</td><td>68.8</td><td>73.3</td><td>16</td></tr><tr><td>ccomp</td><td>clausal complement with internal subject</td><td>93.0</td><td>86.0</td><td>89.4</td><td>189</td></tr><tr><td>xcomp</td><td>clausal complement with external subject</td><td>93.8</td><td>94.2</td><td>94.0</td><td>243</td></tr><tr><td>complm</td><td>complementizer</td><td>98.1</td><td>100.0</td><td>99.0</td><td>52</td></tr><tr><td>obj</td><td>object</td><td></td><td></td><td></td><td></td></tr><tr><td>dobj</td><td> direct object</td><td>93.8</td><td>95.7</td><td>94.7</td><td>694</td></tr><tr><td>iobj</td><td>indirect object</td><td>81.8</td><td>100.0</td><td>90.0</td><td>18</td></tr><tr><td>pobj</td><td>object of preposition</td><td>100.0</td><td>85.2</td><td>92.0</td><td>27</td></tr><tr><td>mark</td><td>marker (word introducing an advcl)</td><td>91.9</td><td>97.8</td><td>94.8</td><td>93</td></tr><tr><td>subj</td><td>subject</td><td></td><td></td><td></td><td></td></tr><tr><td>nsubj</td><td>nominal subject</td><td>97.7</td><td>96.4</td><td>97.0</td><td>1343</td></tr><tr><td>nsubjpass</td><td>passive nominal subject</td><td>95.6</td><td>94.2</td><td>94.9</td><td>69</td></tr><tr><td>csubj</td><td>clausal subject</td><td>66.7</td><td>50.0</td><td>57.1</td><td>8</td></tr><tr><td>cC</td><td>coordination</td><td>96.4</td><td>100.0</td><td>98.2</td><td>28</td></tr><tr><td>conj</td><td>conjunct</td><td>93.2</td><td>97.6</td><td>95.3</td><td>463</td></tr><tr><td>exp1 mod</td><td>expletive (expletive &quot;there&quot;)</td><td>100.0</td><td>100.0</td><td>100.0</td><td>40</td></tr><tr><td>amod</td><td>modifier adjectival modifier</td><td></td><td></td><td></td><td></td></tr><tr><td>appos</td><td> appositional modifier</td><td>96.9 89.3</td><td>95.9 65.8</td><td>96.4 75.8</td><td>657 38</td></tr><tr><td>advcl</td><td>adverbial clause modifier</td><td>86.6</td><td>97.0</td><td>91.5</td><td>100</td></tr><tr><td>det</td><td>determiner</td><td>98.3</td><td>99.4</td><td>98.9</td><td>1024</td></tr><tr><td>predet</td><td> predeterminer</td><td>90.0</td><td>100.0</td><td>94.7</td><td></td></tr><tr><td>preconj</td><td>preconjunct</td><td>83.3</td><td>100.0</td><td>90.9</td><td></td></tr><tr><td>infmod</td><td>infinitival modifier</td><td>85.7</td><td>80.0</td><td>82.8</td><td></td></tr><tr><td>partmod</td><td> participial modifier</td><td>93.9</td><td>86.1</td><td>89.9</td><td></td></tr><tr><td>advmod</td><td>adverbial modifier</td><td>95.2</td><td>95.4</td><td>95.3</td><td>36 507</td></tr><tr><td>neg</td><td>negation modifier</td><td></td><td></td><td>99.5</td><td>91</td></tr><tr><td>rcmod</td><td></td><td>98.9</td><td>100.0</td><td></td><td></td></tr><tr><td></td><td>relative clause modifier</td><td>92.9</td><td>89.7</td><td>91.2</td><td>58</td></tr><tr><td>quantmod</td><td>quantifier noun compound modifier</td><td>87.0</td><td>100.0</td><td>93.0</td><td>20</td></tr><tr><td>nn</td><td>noun phrase adverbial modifier</td><td>92.7</td><td>89.9</td><td>91.3</td><td>300</td></tr><tr><td>npadvmod</td><td></td><td>95.7</td><td>91.7</td><td>93.6</td><td>24</td></tr><tr><td>tmod</td><td>temporal modifier</td><td>84.6</td><td>87.3</td><td>85.9</td><td>63</td></tr><tr><td>num</td><td>numeric modifier</td><td>96.9</td><td>95.4</td><td>96.2</td><td>132</td></tr><tr><td>number</td><td>element of compound number</td><td>100.0</td><td>100.0</td><td>100.0</td><td></td></tr><tr><td>prep</td><td> prepositional modifier</td><td>95.7</td><td>96.3</td><td>96.0</td><td>975</td></tr><tr><td>poss</td><td> possession modifier</td><td>99.1 95.2</td><td>98.8</td><td>99.0</td><td>336</td></tr><tr><td>prt</td><td>phrasal verb particle</td><td></td><td>100.0</td><td>97.5</td><td>61</td></tr><tr><td>parataxis</td><td> parataxis</td><td>62.5</td><td>100.0</td><td>76.9</td><td></td></tr></table></body></html>

# 3.4. Discussion

The most striking result of this evaluation is the high accuracy scores of the automated annotation tools which demonstrates that the tools are robust to learner language. These scores are high even for lower proficiency levels (Table 6). There are a number of explanations for this result.

The first relates to the overall simplicity of learner language in comparison to native productions. For instance, learner sentences tend to be shorter and therefore less demanding for the parser. The average word length of sentences in this evaluation set is 11 words, whereas that of sentences in the British National Corpus (BNC; Burnard, 1995) is 16 words, and that of the WSJ is 21 words. It is possible then that the shorter average sentence length of learner productions compensates for the effect of learner errors on the parser.

A second explanation relates to the nature of errors and the finding that automated tools show robustness to at least half the learner errors. Many errors are semantic and do not affect parser performance which targets syntactic structure. Consider for instance the examples in (5) from our sample. The parser has correctly identified the relevant grammatical dependencies, despite the learner errors (this is also true for also examples (3-b) and (3-c)).

(5) a. ... I play all other kind of music.. b. .... the best convenience of the modern technology .... c. .... it is a potential large group... d. ... my older brother is 40 and my littler brother is ... e. ... my wife is wearing a white and pink pants.... f. ....I try to visualise pleasant and restful place ...

Similarly, a good part of what appear to be subcategorization errors or choice of preposition errors do not affect the parser’s ability to obtain the correct dependencies, see examples (2-e) and (2-f) and (6).

(6) a. I encourage you to continue your support in respect of my presidency b. I am looking forward for your feedback... c. The body language in Russia is very similar with American one.

The erroneous patterns we see in (5) and (6) require a systematic investigation to be modelled accurately. At the same time, the robustness of the parser is welcome since it allows us to obtain the main syntactic patterns that are used by learners. Consider for instance, the sentence mentioned earlier with an adverb intervening between the verb and its object it brings rarely such connotations. The parse of this sentence is shown in Figure 8. The parser ‘ignores’ the word order violation and correctly analyzes rarely as an adverbial modifier and such connotations as a nominal direct object. Similarly, the parser identifies a relative clause in (3-a) and analyzes to reaching in (3-d) as a complement of the main verb. The robustness of the parser in these cases is important, because it captures syntactic structures that are used in learner language. In sum, the parser often abstracts away from local morphosyntactic information and word order violations but succeeds with the underlying syntactic dependencies. While this results in an incomplete picture of learner language, it nevertheless reveals an important aspect of the grammar underlying learner language. The current dependency annotations can be used to investigate the range of word order violations and the way different types of dependents (e.g., adverbs vs. indirect objects) may intervene between the verb and the direct object.

![](img/8ad255974a66e8f64cf67962e296771ebb42df9e0df8c82801ace204aee378d7.jpg)  
Figure 8: Sentence with a word order error

Let us briefly consider the mismatches raised by D´ıaz-Negrillo et al. (2010) and Ragheb and Dickinson (2011). In general, the parser has resolved conflicting evidence in favor of morphological information (and our annotators have accepted morphology-based POS tags). Thus, catched in (4-a) and certificated in (4-c) are tagged as VBN (verb, past participle). Similarly, want in (1-a) is tagged as VBP (verb, non-3rd-person form). Such annotations do not reflect the relevant mismatches but enable a systematic investigation of the environments and lexical elements involved in them.

Finally, despite the very high accuracy scores, some patterns have been particularly challenging for the parser. For instance, absence of critical morphological information may lead to a category error in tagging which can then result in the wrong parse. For instance, change in (3-e) has been analyzed as a noun.

In conclusion, the relatively high accuracy scores of the parser can be explained through a combination of the overall simplicity of learner productions and the robustness of the parser that tends to focus on the primary dependency relations ‘ignoring’ local morphosyntactic information, some word order violations as well as semantic violations. Current NLP tools allow us to obtain reliable morphosyntactic annotations for learner language that are vital for investigating a wide range of lexical and morphosyntactic phenomena of L2 grammars.

# 4. Conclusions

EFCAMDAT is a new L2 English database built at the University of Cambridge, in collaboration with EF Education First. It consists of scripts submitted to Englishtown, the online school of EF Education First. It stands out for its size and rich individual longitudinal data from learners with a wide variety of backgrounds. It is an open access resource available to the research community via a web-based interface at http://corpus.mml.cam.ac.uk/efcamdat/, subject to a standard user agreement.

EFCAMDAT is tagged and parsed for POS and dependency relations using Penn Treebank tags and the Stanford parser. The core of this paper presented the results of an evaluation study on parser performance on a sample of 1,000 sentences from EFCAMDAT. The results indicate that parsing English L2 with current NLP tools generally yields performance close to that of parsing well-formed native English text. This is despite the fact that $3 3 . 8 \%$ of our sample of 1,000 learner sentences contains at least one learner error. Our analysis shows that current NLP tools are robust to a significant part of learner errors. This is because a good part of errors involve local morphosyntactic, subcategorization, word order, and semantic errors that do not affect the main dependency relations the parser targets. As a result, the parser can successfully capture syntactic patterns that are used by learners and provide valuable annotations for the investigation of a wide range of phenomena and SLA hypotheses. At the same time, some form errors (spelling, morphosyntactic) can lead to category (POS) errors when the distributional information cannot reliably define a category (e.g., co-ordination) or the form is ambiguous between a noun and verb category.

The robust performance of current NLP tools on L2 English demonstrates that they can be successfully used for automatic annotation of large scale databases like EFCAMDAT. Moreover, they provide a critical starting point for development of tools that can accurately model the erroneous and untypical patterns of learner language.

In this work we have used one particular state-of-the-art parsing algorithm, the Stanford parser, but various others could be used as well, such as the C&J reranking parser (Charniak & Johnson, 2005) and the Berkely parser (Petrov, Barrett, Thibaux, & Klein, 2006). It would be worth exploring other systems, in isolation and by using ensemble models that combine independently-trained models at parsing time to exploit complementary strengths (Sagae & Tsujii, 2007).

# 5. Appendix: The Penn Treebank POS tagset (excl. punctuation tags)

1. CC Coordinating conjunction   
2. CD Cardinal number   
3. DT Determiner   
4. EX Existential there   
5. FW Foreign word   
6. IN Preposition/subord.   
7. JJ Adjective   
8. JJR Adjective, comparative   
9. JJS Adjective, superlative   
10. LS List item marker   
11. MD Modal   
12. NN Noun, singular or mass   
13. NNS Noun, plural   
14. NNP Proper noun, singular   
15. NNPS Proper noun, plural   
16. PDT Predeterminer   
17. POS Possessive ending   
18. PRP Personal pronoun   
19. PP Possessive pronoun   
20. RB Adverb   
21. RBR Adverb, comparative   
22. RBS Adverb, superlative   
23. RP Particle   
24. SYM Symbol   
25. TO to   
26. UH Interjection   
27. VB Verb, base form   
28. VBD Verb, past tense   
29. VBG Verb, gerund/present participle   
30. VBN Verb, past participle   
31. VBP Verb, non-3rd ps. sing. present   
32. VBZ Verb, 3rd ps. sing. present   
33. WDT wh-determiner   
34. WP wh-pronoun   
35. WP Possessive wh-pronoun   
36. WRB wh-adverb

# References

Amaral, Luiz & Meurers, Detmar. (2011). On using intelligent computer-assisted language learning in real-life foreign language teaching and learning. ReCALL, 23(1), 4–24.   
Barchan, Jonathan, Woodmansee, B., & Yazdani, Masoud. (1986). A PROLOG-based tool for French grammar analysis. Instructional Science, 15(1), 21–48.   
Bley-Vroman, Robert. (1989). What is the logical problem of foreign language learning? In S. M. Gass & J. Schachter (Eds.), Linguistic perspectives on second language acquisition (pp. 41–68). New York: Cambridge University Press.   
Burnard, Lou. (1995, May). Users Reference Guide for the British National Corpus. http://info.ox.ac.uk/bn   
Cer, Daniel, Marneffe, Marie-Catherine De, Jurafsky, Daniel, & Manning, Christopher D. (2010). Parsing to Stanford dependencies: trade-offs between speed and accuracy. In Proceedings of the Seventh International Conference on Language Resources and Evaluation (LREC’10) (pp. 1628–1632). Valletta, Malta.   
Charniak, Eugene & Johnson, Mark. (2005). Coarse-to-fine n-best parsing and maxent discriminative reranking. In Proceedings of the 43rd Annual Meeting of the Association for Computational Linguistics (pp. 173–180). Stroudsburg, PA, USA: Association for Computational Linguistics.   
De Marneffe, Marie-Catherine & Manning, Christopher D. (2008). The Stanford typed dependencies representation. In Coling 2008: Proceedings of the workshop on Cross-Framework and CrossDomain Parser Evaluation (pp. 1–8).   
D´ıaz-Negrillo, Ana, Meurers, Detmar, Valera, Salvador, & Wunsch, Holger. (2010). Towards interlanguage POS annotation for effective learner corpora in SLA and FLT. Language Forum, 36(1–2), 139–154. Special Issue on Corpus Linguistics for Teaching and Learning. In Honour of John Sinclair.   
Dickinson, Markus & Lee, Chong Min. (2009). Modifying corpus annotation to support the analysis of learner language. CALICO Journal, 26(3), 545–561.   
Dickinson, Markus & Ragheb, Marwa. (2009). Dependency annotation for learner corpora. In M. Passarotti, A. Przepiorkowski, S. Raynaud, & F. V. Eynde (Eds.), ´ Proceedings of the Eighth International Workshop on Treebanks and Linguistic Theories (pp. 59–70). Milan, Italy.   
Dickinson, Markus & Ragheb, Marwa. (2011). Dependency annotation of coordination for learner language. In K. Gerdes, E. Hajicova, & L. Wanner (Eds.), Proceedings of the International Conference on Dependency Linguistics (Depling) (pp. 135–144). Barcelona, Spain.   
Education First. (2012). Englishtown. http://www.englishtown.com/.   
Feldweg, Helmut. (1991). The European Science Foundation Second Language Database. Nijmegen, Netherlands: Max-Planck-Institute for Psycholinguistics.   
Granger, Sylviane. (2003). Error-tagged learner corpora and CALL: A promising synergy. CALICO, 20(3), 465–480.   
Granger, Sylviane, Kraif, Olivier, Ponton, Claude, Antoniadis, Georges, & Zampa, Virginie. (2007). Integrating learner corpora and natural language processing: a crucial step towards reconciling technological sophistication and pedagogical effectiveness. ReCaLL, 19(3), 252–268.   
Jensen, Karen, Heidorn, George E., Miller, Lance A., & Ravin, Yael. (1983). Parse fitting and prose fixing: Getting a hold on ill-formedness. Computational Linguistics, 9(3-4), 147–160.   
Klein, Dan & Manning, Christopher D. (2003). Accurate unlexicalized parsing. In Proceedings of the 41st Annual Meeting on Association for Computational Linguistics - volume 1 (pp. 423–430). Stroudsburg, PA, USA: Association for Computational Linguistics.   
Krivanek, Julia & Meurers, Detmar. (2011). Comparing rule-based and datadriven dependency parsing of learner language. In Proceedings of the International Conference on Dependency Linguistics (Depling 2011) (pp. 128–132).   
Ludeling, Anke, Walter, Maik, Kroymann, Emil, & Adolphs, Peter. (2005). Multi-level error annotation ¨ in learner corpora. In Proceedings from the Corpus Linguistics Conference Series (Vol. 1, 1). Birmingham, UK.   
Marcus, Mitchell P., Marcinkiewicz, Mary Ann, & Santorini, Beatrice. (1993, June). Building a large annotated corpus of English: The Penn Treebank. Computational Linguistics, 19(2), 313–330.   
Menzel, Wolfgang & Schroder, Ingo. (1999). Error diagnosis for language learning systems. ¨ ReCALL, 11, 20–30.   
Meurers, Detmar. (2009). On the automatic analysis of learner language. CALICO Journal, 26(3), 469– 473.   
Myles, Florence & Mitchell, Rosamond. (2007). French learner language oral corpora. http://www.flloc.soton.ac.uk/. University of Southampton.   
Nicholls, Diane. (2003). The Cambridge Learner Corpus: Error coding and analysis for lexicography and ELT. In Proceedings of the Corpus Linguistics Conference (pp. 572–581). Lancaster University: University Centre for Computer Corpus Research on Language.   
Nivre, Joakim, Hall, Johan, Nilsson, Jens, Chanev, Atanas, Eryigit, Gulsen, Kubler, Sandra, . . . Marsi, ¨ Erwin. (2007). MaltParser: A language-independent system for data-driven dependency parsing. Natural Language Engineering, 13(2), 95.   
Ott, Niels & Ziai, Ramon. (2010). Evaluating dependency parsing performance on German learner language. In Proceedings of the Ninth International Workshop on Treebanks and Linguistic Theories (NEALT 2010) (pp. 175–186).   
Petrov, Slav, Barrett, Leon, Thibaux, Romain, & Klein, Dan. (2006). Learning accurate, compact, and interpretable tree annotation. In Proceedings of the 21st International Conference on Computational Linguistics and the 44th annual meeting of the Association for Computational Linguistics (pp. 433–440). Stroudsburg, PA, USA: Association for Computational Linguistics.   
Ragheb, Marwa & Dickinson, Markus. (2011). Avoiding the comparative fallacy in the annotation of learner corpora. In G. Granena, J. Koeth, S. Lee-Ellis, A. Lukyanchenko, G. P. Botana, & E. Rhoades (Eds.), Selected Proceedings of the 2010 Second Language Research Forum: Reconsidering SLA research, dimensions, and directions (pp. 114–124). Somerville, MA, USA: Cascadilla Proceedings Project.   
Sagae, Kenji & Tsujii, Jun’ichi. (2007). Dependency parsing and domain adaptation with LR models and parser ensembles. In Proceedings of the conll shared task session of emnlp-conll (Vol. 7, pp. 1044–1050).   
Tesniere, Lucien & Fourquet, Jean. (1959). \` Elements de syntaxe structurale ´ . Klincksieck Paris.   
Wagner, Joachim & Foster, Jennifer. (2009). The effect of correcting grammatical errors on parse probabilities. In Proceedings of the 11th International Conference on Parsing Technologies (pp. 176–179). IWPT ’09. Paris, France: Association for Computational Linguistics.