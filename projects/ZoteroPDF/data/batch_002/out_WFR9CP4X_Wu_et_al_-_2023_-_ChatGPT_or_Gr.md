# ChatGPT or Grammarly? Evaluating ChatGPT on Grammatical Error Correction Benchmark

Haoran Wu† Wenxuan Wang† Yuxuan Wan † Wenxiang Jiao‡ Michael R. Lyu†   
†Department of Computer Science and Engineering, The Chinese University of Hong Kong 1155157061@link.cuhk.edu.hk {wxwang,yxwan9,lyu}@cse.cuhk.edu.hk ‡Tencent AI Lab joelwxjiao@tencent.com

# Abstract

ChatGPT is a cutting-edge artificial intelligence language model developed by OpenAI, which has attracted a lot of attention due to its surprisingly strong ability in answering follow-up questions. In this report, we aim to evaluate ChatGPT on the Grammatical Error Correction (GEC) task, and compare it with commercial GEC product (e.g., Grammarly) and state-of-the-art models (e.g., GECToR). By testing on the CoNLL2014 benchmark dataset, we find that ChatGPT performs not as well as those baselines in terms of the automatic evaluation metrics (e.g., $F _ { 0 . 5 }$ score), particularly on long sentences. We inspect the outputs and find that ChatGPT goes beyond one-by-one corrections. Specifically, it prefers to change the surface expression of certain phrases or sentence structure while maintaining grammatical correctness. Human evaluation quantitatively confirms this and suggests that ChatGPT produces less undercorrection or mis-correction issues but more over-corrections. These results demonstrate that ChatGPT is severely under-estimated by the automatic evaluation metrics and could be a promising tool for GEC.

# 1 Introduction

ChatGPT1, the current “super-star” in artificial intelligence (AI) area, has attracted millions of registered users within just a week since its launch by OpenAI. One of the reasons for ChatGPT being so popular is its surprisingly strong performance on various natural language processing (NLP) tasks (Bang et al., 2023), including question answering (Omar et al., 2023), text summarization (Yang et al., 2023), machine translation (Jiao et al., 2023), logic reasoning (Frieder et al., 2023), code debugging (Xia and Zhang, 2023), etc. There is also a trend of using ChatGPT as a writing assistant for text polishing.

Despite the widespread use of ChatGPT, it remains unclear to the NLP community that to what extent ChatGPT is capable of revising the text and correcting grammatical errors. To fill this research gap, we empirically study the Grammatical Error Correction (GEC) ability of ChatGPT by evaluating on the CoNLL2014 benchmark dataset $( \mathrm { N g }$ et al., 2014), and comparing its performance to Grammarly, a prevalent cloud-based English typing assistant with 30 million users daily (Grammarly, 2023) and GECToR (Omelianchuk et al., 2020), a state-of-the-art GEC model. With this study, we aim to answer a research question:

Is ChatGPT a good tool for GEC?

To the best of our knowledge, this is the first study on ChatGPT’s ability in GEC.

We present the major insights gained from this evaluation as below:

• ChatGPT performs worse than the baseline systems in terms of the automatic evaluation metrics (e.g., $F _ { 0 . 5 }$ score), particularly on long sentences.   
• ChatGPT goes beyond one-by-one corrections by introducing more changes to the surface expression of certain phrases or sentence structure while maintaining the grammatical correctness.   
• Human evaluation quantitatively demonstrates that ChatGPT produces less undercorrection or mis-correction issues but more over-corrections.

Our evaluation indicates the limitation of relying solely on automatic evaluation metrics to assess the performance of GEC models and suggests that ChatGPT is a promising tool for GEC.

Table 1: Different types of error in GEC.   

<html><body><table><tr><td>Type</td><td>Error</td><td>Correction</td></tr><tr><td>Preposition</td><td>I sat in the talk.</td><td>I sat in on the talk</td></tr><tr><td>Morphology</td><td>dreamed</td><td>dreamt</td></tr><tr><td>Determiner</td><td>I like the ice cream</td><td>I like ice cream</td></tr><tr><td>Tense/Aspect</td><td>I like play basketball</td><td>I like playing basketball</td></tr><tr><td>Syntax</td><td>I have not the book</td><td>I do not have the book</td></tr><tr><td>Punctuation</td><td>We met they talked and left</td><td>We met, they talked and left</td></tr></table></body></html>

# 2 Background

# 2.1 ChatGPT

ChatGPT is an intelligent chatbot powered by large language models developed by OpenAI. It has attracted great attention from industry, academia, and the general public due to its strong ability in answering various follow-up questions, correcting inappropriate questions (Zhong et al., 2023), and even refusing illegal questions. While the technical details of ChatGPT have not been released systematically, it is known to be built upon InstructGPT (Ouyang et al., 2022) which is trained using instruction tuning (Wei et al., 2022a) and reinforcement learning from human feedback (RLHF, Christiano et al., 2017).

# 2.2 Grammatical Error Correction

Grammatical Error Correction (GEC) is a task of correcting different kinds of errors in text such as spelling, punctuation, grammatical, and word choice errors (Ruder, 2022). It is highly demanded as writing plays an important role in academics, work, and daily life. Table 1 presents the illustration of different grammatical errors borrowed from Bryant et al. (2022) in a comprehensive survey on grammatical error correction. In general, grammatical errors can be roughly classified into three categories: omission errors, such as "on" in the first example; replacement errors, such as "dreamed" for "dreamt" in the second example; and insertion errors, such as "the" in the third example.

To evaluate the performance of GEC, researchers have built various benchmark datasets, which include but are not limited to:

• CoNLL-2014: Given the short English texts written by non-native speakers, the task requires a participating system to correct all errors present in each text.

• BEA-2019: It is similar to CoNLL-2014 but introduces a new dataset, namely, the Write&Improve+LOCNESS corpus, which represents a wider range of native and learner English levels and abilities (Bryant et al., 2019).

Table 2: GEC performance of GECToR, Grammarly, and ChatGPT.   

<html><body><table><tr><td>System</td><td>Precision</td><td>Recall</td><td>Fo.5</td></tr><tr><td>GECToR</td><td>71.2</td><td>38.4</td><td>60.8</td></tr><tr><td>Grammarly</td><td>67.3</td><td>51.1</td><td>63.3</td></tr><tr><td>ChatGPT</td><td>51.2</td><td>62.8</td><td>53.1</td></tr></table></body></html>

• JFLEG: It represents a broad range of lan guage proficiency levels and uses holistic fluency edits to not only correct grammatical errors but also make the original text more native sounding (Tetreault et al., 2017).

# 3 ChatGPT for GEC

# 3.1 Experimental Setup

Dataset. We evaluate the ability of ChatGPT in grammatical error correction on the CoNLL2014 task $\mathrm { N g }$ et al., 2014) dataset. The dataset is composed by short paragraphs that are written by nonnative speakers of English, accompanied with the corresponding annotations on the grammatical errors. We pulled 100 sentences from the officialcombined test set in the alternate folder of the dataset sequentially.

Evaluation Metric. To evaluate the performance of GEC, we adopt three metrics that are widely used in literature, namely, Precision, Recall, and $F _ { 0 . 5 }$ score. Among them, $F _ { 0 . 5 }$ score combines both Precision and Recall, where Precision is assigned a higher weight (Wikipedia contributors, 2023a).

<html><body><table><tr><td rowspan="2">System</td><td colspan="3">Short</td><td colspan="3">Medium</td><td colspan="3">Long</td></tr><tr><td>Precision Recall</td><td></td><td>F0.5</td><td>Precision</td><td>Recall</td><td>Fo.5</td><td>Precision Recall</td><td></td><td>Fo.5</td></tr><tr><td>GECToR</td><td>76.9</td><td>38.5</td><td>64.1</td><td>68.8</td><td>37.5</td><td>58.9</td><td>71.8</td><td>38.9</td><td>61.5</td></tr><tr><td>Grammarly</td><td>62.5</td><td>60.6</td><td>62.1</td><td>68.9</td><td>56.0</td><td>65.9</td><td>67.3</td><td>45.3</td><td>61.4</td></tr><tr><td>ChatGPT</td><td>58.5</td><td>66.7</td><td>60.0</td><td>48.7</td><td>60.7</td><td>50.7</td><td>51.0</td><td>62.8</td><td>53.0</td></tr></table></body></html>

Table 3: GEC performance with respect to sentence length.

Specifically, the three metrics are expressed as:

$$
\begin{array} { l } { { \mathrm { P r e c i s i o n } = \displaystyle \frac { T P } { T P + F P } , } } \\ { { \mathrm { R e c a l l } = \displaystyle \frac { T P } { T P + F N } , } } \\ { { \mathrm { F } _ { 0 . 5 } = \displaystyle \frac { 1 . 2 5 \times \mathrm { P r e c i s i o n } \times \mathrm { R e c a l l } } { 0 . 2 5 \times \mathrm { P r e c i s i o n } + \mathrm { R e c a l l } } , } } \end{array}
$$

where $T P , F P$ and $F N$ represent the true positives, false positives and false negatives of the predictions, respectively. We use the scoring program provided by CoNLL2014 official but adapt it to be compatible with the latest Python environment.

Baselines. In this report, we perform the GEC task on three systems, including:

• ChatGPT: We query ChatGPT manually rather than using some API due to the instability of ChatGPT. For example, when a query sentence resembles a question or demand, ChatGPT may stop the process of GEC but respond to the “demand” instead. After a few trials, we find a prompt that works well for ChatGPT:

Do grammatical error correction on all the following sentences I type in the conversation.

We query ChatGPT with this prompt for each test sample.

• Grammarly: Grammarly is a prevalent cloudbased English typing assistant. It reviews spelling, grammar, punctuation, clarity, engagement, and delivery mistakes in English texts, detects plagiarism and suggests replacements for the identified errors (Wikipedia contributors, 2023b). As stated by Grammarly, every day, 30 million people and 50,000 teams around the world use Grammarly with their writing (Grammarly, 2023). When querying Grammarly, we open a text file and paste all the test samples into separate paragraphs. We enable all the grammar correction in the setting and only ask it to correct the ones with correctness problems (red underline), while leaving the clarity (blue underline), engagement (green underline) and delivery (purple underline) unchanged. We iterate this process several times until there is no error detected by Grammarly.

• GECToR: Besides Grammarly, we also compare ChatGPT with GECToR (Omelianchuk et al., 2020), a state-of-the-art model on GEC in research, which also exhibits good performance on the CoNLL2014 task. We adopt the implementation based on the pre-trained RoBERTa model.

# 3.2 Results and Analysis

Overall Performance. Table 2 presents the overall performance of the three systems. As seen, ChatGPT obtains the highest recall value, GECToR obtains the highest precision value, while Grammarly achieves a better balance between the two metrics and results in the highest $F _ { 0 . 5 }$ score. These results suggest that ChatGPT tends to correct as many errors as possible, which may lead to more overcorrections. Instead, GECToR corrects only those it is confident about, which leaves many errors uncorrected. Grammarly combines the advantages of both such that it performs more stably.

# ChatGPT Performs Worse on Long Sentences?

To understand which kind of sentences ChatGPT are good at, we divide the 100 test sentences into three equally sized categories, namely, Short, Medium and Long. Table 3 shows the results with respect to sentence length. As seen, the gap between ChatGPT and Grammarly is significantly bridged on short sentences. In contrast, ChatGPT performs much worse on those longer sentences, at least in terms of the existing evaluation metrics.

ChatGPT Goes Beyond One-by-One Corrections. We inspect the output of the three systems, especially those for long sentences, and find that

Table 4: Comparison of the outputs from different GEC systems.   

<html><body><table><tr><td>System Sentence</td><td></td></tr><tr><td>Source</td><td>For an example , if exercising is helpful for family potential disease , we can always look for more chances for the family to go exercise .</td></tr><tr><td>Reference</td><td>For example , if exercising (OR exercise) is helpful for a potential family disease , we can always look for more chances for the family to do exercise .</td></tr><tr><td>GECToR Grammarly</td><td>For example , if exercising is helpful for family potential disease , we can always look for more chances for the family to go exercise . For example , if exercising is helpful for a family &#x27;s potential disease , we can</td></tr><tr><td>ChatGPT</td><td>always look for more chances for the family to go exercise .</td></tr><tr><td></td><td>For example , if exercise is helpful in preventing potential family diseases , we can always look for more opportunities for the family to exercise .</td></tr></table></body></html>

Table 5: GEC performance with Grammarly for further correction.   

<html><body><table><tr><td>System</td><td>Precision</td><td>Recall</td><td>Fo.5</td></tr><tr><td>GECToR</td><td>71.2</td><td>38.4</td><td>60.8</td></tr><tr><td>+ Grammarly</td><td>-5.9</td><td>+16.5</td><td>+2.1</td></tr><tr><td>ChatGPT</td><td>51.2</td><td>62.8</td><td>53.1</td></tr><tr><td>+ Grammarly</td><td>+0.4</td><td>+0.8</td><td>+0.5</td></tr></table></body></html>

ChatGPT is not limited to correcting the errors in the one-by-one fashion. Instead, it is more willing to change the superficial expression of some phrases or the sentence structure. For example, in Table 4, GECToR and Grammarly make minor changes to the source sentence (i.e., “an example” to “example”, “family potential disease” to “a family ’s potential disease”), while ChatGPT modifies the sentence structure (i.e., “for family potential disease” to “in preventing potential family diseases”) and word choice (i.e., “chances” to “opportunities”). It indicates that the outputs by ChatGPT maintain the grammatical correctness, although they do not follow the original expression of the source sentences.

To validate our hypothesis, we let Grammarly to further correct the grammatical errors in the outputs of GECToR and ChatGPT. Table 5 lists the results. We can observe that Grammarly introduces a negligible improvement to the output of ChatGPT, demonstrating that ChatGPT indeed generates correct sentences. On the contrary, Grammarly further improves the performance of GECToR noticeably (i.e., $+ 2 . 1$ $F _ { 0 . 5 }$ , $+ 1 6 . 5$ Recall), suggesting that there are still many errors in the output of GECToR.

Table 6: Number of under-correction (Under), miscorrection (Mis) and over-correction (Over) produced by different GEC systems.   

<html><body><table><tr><td>System</td><td>#Under</td><td>#Mis</td><td>#Over</td></tr><tr><td>GECToR</td><td>13</td><td>4</td><td>0</td></tr><tr><td>Grammarly</td><td>14</td><td>0</td><td>1</td></tr><tr><td>ChatGPT</td><td>3</td><td>3</td><td>30</td></tr></table></body></html>

Human Evaluation. We conduct a human evaluation to further demonstrate the potential of ChatGPT for the GEC task. Specifically, we follow Wang et al. (2022) to manually annotate the issues in the outputs of the three systems, including 1) Under-correction, which is the grammatical errors that are not found; 2) Mis-correction, which is the grammatical errors that are found but modified incorrectly; it can be either grammatically incorrect or semantically incorrect; 3) Overcorrection, which is the other modifications beyond the changes in the reference. We sample 20 sentences out of the 100 test sentences and ask two annotators to identify the issues. Table 6 shows the results. Obviously, ChatGPT has the least number of under-corrections among the three systems and fewer number of mis-corrections compared with GECToR, which suggests its great potential in grammatical error correction. Meanwhile, ChatGPT produces more over-corrections, which may come from the diverse generation ability as a large language model. While this usually leads to a lower $F _ { 0 . 5 }$ score, it also allows more flexible language expressions in GEC.

Discussions. We have checked the outputs corresponding to the results of Table 5, and observed different behaviors of ChatGPT and Grammarly. The slight improvement (i.e., $+ 0 . 5 \ F _ { 0 . 5 } )$ by Grammarly mainly comes from punctuation problems. ChatGPT is not sensitive to punctuation problems but Grammarly is, though the modifications are not always correct. For example, when we manually undo the corrections on punctuation, the $F _ { 0 . 5 }$ score increases by $+ 0 . 0 0 1 5$ . Other than punctuation problems, Grammarly also corrects a few grammatical errors on articles, prepositions, and plurals. However, these corrections usually require Grammarly to repeat the process twice. Take the following sentence as an example,

constructs of the family and kinship are a social construct,

Grammarly first changes it to constructs of the family and kinship are a social constructs,

Then, changes it to constructs of the family and kinship are social constructs,

Nonetheless, it does correct some errors that ChatGPT fails to correct.

# 4 Conclusion

This paper evaluates ChatGPT on the task of Grammatical Error Correction (GEC). By testing on the CoNLL2014 benchmark dataset, we find that ChatGPT performs worse than a commercial product Grammarly and a state-of-the-art model GECToR in terms of automatic evaluation metrics. By examining the outputs, we find that ChatGPT displays a unique ability to go beyond one-by-one corrections by changing surface expressions and sentence structure while maintaining grammatical correctness. Human evaluation results confirm this finding and reveals that ChatGPT produces fewer under-correction or mis-correction issues but more over-corrections. These results demonstrate the limitation of relying solely on automatic evaluation metrics to assess the performance of GEC models and suggest that ChatGPT has the potential to be a valuable tool for GEC.

# Limitations and Future Works

There are several limitations in this version, which we leave for future work:

• More Datasets: In this version, we only use the CoNLL-2014 test set and only randomly select 100 sentences to conduct the evaluation. In our future work, we will conduct experiments on more datasets.

• More Prompt and In-context Learning: In this version, we only use one prompt to query ChatGPT and do not utilize the advanced technology from the in-context learning field, such as providing demonstration examples (Brown et al., 2020) or providing chain-of-thought (Wei et al., 2022b), which may under-estimate the full potential of ChatGPT. In our future work, we will explore the in-context learning methods for GEC to improve its performance.

• More Evaluation Metrics: In this version, we only adopt Precision, Recall and $F _ { 0 . 5 }$ as evaluation metrics. In our future work, we will utilize more metrics, such as pretraining-based metrics (Gong et al., 2022) to evaluate the performance comprehensively.

# References

Yejin Bang, Samuel Cahyawijaya, Nayeon Lee, Wenliang Dai, Dan Su, Bryan Wilie, Holy Lovenia, Ziwei Ji, Tiezheng Yu, Willy Chung, Quyet V. Do, Yan Xu, and Pascale Fung. 2023. A multitask, multilingual, multimodal evaluation of chatgpt on reasoning, hallucination, and interactivity. ArXiv.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. NeurIPS.

Christopher Bryant, Mariano Felice, Øistein E. Andersen, and Ted Briscoe. 2019. The bea-2019 shared task on grammatical error correction. In $B E A @ A C L$ .

Christopher Bryant, Zheng Yuan, Muhammad Reza Qorib, Hannan Cao, Hwee Tou Ng, and Ted Briscoe. 2022. Grammatical error correction: A survey of the state of the art. ArXiv.

Paul Francis Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei. 2017. Deep reinforcement learning from human preferences. NeruIPS.

Simon Frieder, Luca Pinchetti, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas Lukasiewicz, Philipp Christian Petersen, Alexis Chevalier, and J J Berner. 2023. Mathematical capabilities of chatgpt. ArXiv.

Peiyuan Gong, Xuebo Liu, Heyan Huang, and Min Zhang. 2022. Revisiting grammatical error correction evaluation and beyond. EMNLP.

Grammarly. 2023. Grammarly website about us page.

Wenxiang Jiao, Wenxuan Wang, Jen tse Huang, Xing Wang, and Zhaopeng Tu. 2023. Is ChatGPT a good translator? a preliminary study. In ArXiv.

Hwee Tou Ng, Siew Mei Wu, Ted Briscoe, Christian Hadiwinoto, Raymond Hendy Susanto, and Christopher Bryant. 2014. The conll-2014 shared task on grammatical error correction. In CoNLL.

Reham Omar, Omij Mangukiya, Panos Kalnis, and Essam Mansour. 2023. Chatgpt versus traditional question answering for knowledge graphs: Current status and future directions towards knowledge graph chatbots. ArXiv.

Kostiantyn Omelianchuk, Vitaliy Atrasevych, Artem N. Chernodub, and Oleksandr Skurzhanskyi. 2020. Gector – grammatical error correction: Tag, not rewrite. In Workshop on Innovative Use of NLP for Building Educational Applications.

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. arXiv.

Sebastian Ruder. 2022. NLP-progress.

Joel R. Tetreault, Keisuke Sakaguchi, and Courtney Napoles. 2017. Jfleg: A fluency corpus and benchmark for grammatical error correction. In EACL.

Wenxuan Wang, Wenxiang Jiao, Yongchang Hao, Xing Wang, Shuming Shi, Zhaopeng Tu, and Michael Lyu. 2022. Understanding and improving sequence-tosequence pretraining for neural machine translation. In ACL.

Jason Wei, Maarten Bosma, Vincent Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and Quoc V. Le. 2022a. Finetuned language models are zero-shot learners. ICLR.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Huai hsin Chi, Quoc Le, and Denny Zhou. 2022b. Chain of thought prompting elicits reasoning in large language models. NeurIPS.

Wikipedia contributors. 2023a. F-score — Wikipedia, the free encyclopedia. [Online; accessed 5-March2023].

Wikipedia contributors. 2023b. Grammarly — Wikipedia, the free encyclopedia. [Online; accessed 2-March-2023].

Chun Xia and Lingming Zhang. 2023. Conversational automated program repair. ArXiv.

Xianjun Yang, Yan Li, Xinlu Zhang, Haifeng Chen, and Wei Cheng. 2023. Exploring the limits of chatgpt for query or aspect-based text summarization. ArXiv.

Qihuang Zhong, Liang Ding, Juhua Liu, Bo Du, and Dacheng Tao. 2023. Can chatgpt understand too? a comparative study on chatgpt and fine-tuned bert. ArXiv.