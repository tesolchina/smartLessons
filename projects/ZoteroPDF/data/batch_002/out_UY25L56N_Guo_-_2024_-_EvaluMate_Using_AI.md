# EvaluMate: Using AI to support students' feedback provision in peer assessment for writing

Kai Guo

Faculty of Education, The University of Hong Kong, Hong Kong, China

# ARTICLEINFO

# ABSTRACT

Keywords:   
Peer feedback   
Peer assessment   
Large language models   
Artificial intelligence   
Writing

Peer feedback plays an important role in promoting learning in the writing classroom. However, providing high-quality feedback can be demanding for student reviewers. To address this challenge, this article proposes an AI-enhanced approach to peer feedback provision. I introduce EvaluMate, a newly developed online peer review system that leverages ChatGPT, a large language model (LLM), to scaffold student reviewers' feedback generation. I discuss the design and functionality of EvaluMate, highlighting its affordances in supporting student reviewers' provision of comments on peers' essays. I also address the system's limitations and propose potential solutions. Furthermore, I recommend future research on students' engagement with this learning approach and its impact on learning outcomes. By presenting EvaluMate, I aim to inspire researchers and practitioners to explore the potential of AI technology in the teaching, learning, and assessment of writing.

# 1. Introduction

Peer feedback has gained significant recognition in the writing classroom as n invaluable supplement toteacher feedack It offers advantages to both the providers and recipients of feedback (Cho & MacArthur, 2011; Huisman et al, 2018; Wu & Schunn, 2021; Yu, 2019). However, the effectiveness of peer feedback largely depends on the quality of feedback delivered by student reviewers. Insufficient feedback quality can impede the recipients uptake of feedback and hinder their growth and development in the learning process (Deng et al., 2023; Yu, 2021). Consequently, previous studies have focused on monitoring students peer feedback processes and improving their feedback rovision skill (Chang, 2015; Guo et al., 2022; Han & Xu, 2020). To ensure the validity and reliabilit of peer assesment, some reearchers have turned to artificil intelligence (Al) technologiesto evaluate students per assessments El Alaoui, 2023; Hernandez-Gonzalez & Herrera, 2023). Nonetheless, these studies have predominantly concentrated on monitoring students quanttativ ratings of p essays. Thers a paucity of reearch exploring methos to supervise the qulttive comments made by student reviewers on peer esays, which play a crucial role in assing peers in improving thir drafs (Chen et al., 2020; Hsi t al. 2016). In this article, I propose an AI-enhanced approach to peer fedback provision that specifically emphasises the generation of qualitative comments. Furthermore, Iintroduce a newly developed online peer review system named EvaluMate, which applies this proposed approach It is anticipated that this approach can be integrated into the writing classroom to facilitate peer asessment and enrich students' feedback literacy and writing skills.

# 2. Enhancing peer feedback provision in the writing classroom

Peer assessment holds significant value in the teaching and learning of writing. It not only alleviates the burden of reviewing and evaluating students essays for writing teachers, but also fosters student-centred lerning and promotes learner autonomy (Shen et al., 2020). Numerous studies have demonstrated that engaging in peer fedback activities enhances the writing skill of both feedback providers and recipients (Wu & Schunn, 2021). In particular, on the side of feedack providers, engaging in the processof offering feedback on peers written work encourages critical thinking and provide opportunities for self-reflection on their own writing (Cho & MacArthur, 2011; Yu, 2019).

However, studies have identified challenges faced by student reviewers in providing high-quality feedback, including limited language proficiency, lack of motivation, and concerns about interpersonal relations (Deng et al., 2023; Yu, 2021). To address these issues researchers have explored effective methods for improving students feedback provision skils, such as teacher modelling (Chang, 2015) and collaborative peer feedack (Guo et al., 2022). One notable aproach, which I term as feedback on feedback, involves teachers providing feedback on student reviewers feedback on their peers writing. This approach has been found to enhance students' engagement with the learning activity and improve the quality of their peer feedback (Han & Xu, 2020). Nonetheles, providing prompt and comprehensive feedback on students' peer feedback can be time-consuming for teachers, especiall in large classes. To tackle this challenge, researchers have suggested integrating AI technologies into students' peer feedack generation processes to monitor and evaluate the quality of their fedback (El Alaoui, 2023; Hernandez-Gonzalez & Herrera, 2023). However, most of these studies have primaril focused on ensuring the accuracy of student asessors' scoring of peer essays, neglecting the equally important aspect of qualitative comments in peer assessment.

Ensuring the quality of student reviewers qualitative comments is of great importance as these comments serve a crucial role in assisting peers in revising thir drafts and enhancing their writing skil. Merely receiving a score without accompanying qualitative feedback fails to provide peers with a comprehensive understanding of their writing (Chen et al., 2020; Hsia et al., 2016). Previous studies may have overlooked the qualitative comment aspect of peer feedback due to technological limitations. Typicall, numerical data processing is ofen perceived as more straighforward in comparison to analysing textual information. Nevertheles, recent advancements in AI technology, particularly in the development of large language models (LLMs) capable of understanding and generating human languages, have potentially made i feasible to monitor and evaluate student reviewers' qualitative comments on peer essays.

As a pioneering research endeavour, this article proposes an Al-enhanced approach to support students' pee feedback generation. As depicted in Fig. 1, this approach entail a student reviewer reading, evaluating, and composing qualitative comments on their peers work. These comments are then sent to an LM-based tool for evaluation, and the fedback generated by the tool is returned to the student reviewer for revision and improvement of thir original comments. This iterative process can be repeated as neded until the student reviewer fels satistied with their comments. Finally, the refined comments are shared with the peer, enabling them to revise and enhance their work based on the feedback received.

To implement this aproach, I have developed an online peer review system named EvaluMate. This platform allows students to assume two distinct roles: authors and reviewers. AI technologies are employed to support both the writing and reviewing activities within the system. However, in this artice,I primarily concentrate on the reviewing component toalign with the limited space and the specific focus of this article.

# 3. EvaluMate, an AI-supported peer review system

Fig. 2 showcases the interface design of the reviewing component within EvaluMate. The interface displays the task requirements in the top-left coner, the essy being evaluated in the bottom-left corner, and the rating rubrics in the top-right corner. Anonymity is preserved between authors and reviewers, meaning they do not have knowledge of each other's identities. This feature would help foster objectivity in the evaluation process, encourage citical and constructive comments, and address potential face-rlated concerns (Kobayashi, 2020; Lin, 2018; Velamazan et al., 2023).

![](img/4b5f5911629ebd76ea543cc30615a5ed0e8f43849f72acb84a50924efc775512.jpg)  
Fig. 1. An AI-enhanced approach to peer feedback provision.

![](img/30ff902dfcf61e00497bea529a0f511a94b41e84f788574759612ccee6ceae65.jpg)  
Fig. 2. Peer review interface within EvaluMate.

Student reviewers are tasked with providing both scores for the esy and comments on it (Fig. 3). They are prompted to offer feedback on three aspects of writing: content, organisation, and language. These three dimensions have been commonly employed in previous research (e.g., Golparvar & Abolhasani, 2022; Zhang & Lu, 2022) to comprehensively assesstudents' writing abilities.

To aid them in generating comments, a chatbot named Eva is incorporated, which utilises ChatGPT, a popular LLM. During the interaction, the chatbot frstlyoffers prompts on how to writ effctive comments Fig. 3). Additionall, once student reiewers hae completed their comment draft, they can click on the "Check my comments' button to request the chatbot to evaluate and provide feedback on their comments (Fig. 4).

This action activates a researcher-designed prompt that elicits output from the ChatGPT-powered chatbot. The prompt used is as follows:

I am providing feedback on a per's essy. You provide comments and sugestios on my feedback in terms of the five aspects s follows:

1. Affect: Good feedback includes encouraging and positive emotions such as praise or compliments.   
2. Description: Good feedback includes a summary statement such as description of content or taken action to a large extent   
3. Identification: Good feedback includes explicit and localised identification of problems.   
4. Justification: Good feedback includes elaborations and justifications of identified problems.   
5. Constructiveness: Good feedback includes recommendations and action plans for further improvements.

Below is my feedback: [The student's comments typed into the Comment box].

The prompt has been designed based on prior research on per feedback evaluation (Banihashem et al., 2024; Kerman et al., 2022). The evaluation of students' peer feedback encompasses five dimensions:

1) Affect reviewers are encouraged to provide positive and supportive comments that acknowledge the author's achievements. This would foster a friendly and conducive atmosphere while motivating the author to embrace the feedback given.

2) Description: reviewers are expected to provide a summary statement that demonstrates their comprehensive and accurate under standing of the essay's content. This could enhance the reviewer's credibility and assure the author that their work has been thoroughly reviewed before feedback is provided. Otherwise, the author may hesitate to acept or even reject the feedback received.

![](img/d98ab00d57d011c57b06b90339dd60b38d3bfea6998a176c6ba167dbb8d4c004.jpg)  
Fig. 3. Evaluation conducted by student reviewers.

![](img/f85a929bc0bb3412aa919b83c9ffb0ef25ac4c86273a0c6185bb9d10b593eada.jpg)  
Fig. 4. Eva's feedback on a student reviewer's comments.

3) Identification: reviewers should clearly identify the isues present in the essay and specifically pinpoint their location. This would help the author swiftly identify the problem areas and facilitate targeted revisions.   
4) Justification: reviewers should justify their identification of problems by explaining how these issues would impact the overal quality of the essay and the potential benefits of addressng them effctively. This rationale is likely to encourage the author to accept the identified problems willingly.   
5) Constructiveness reviewers are expected to offer constructive sugestions to asst the author in resolving the identified problems. Providing actionable recommendations can be the most challenging aspect of peer feedback, as finding solutions is often more difficult than identifying the ssues themselves. However, when reviewers can provide helpful action plans, there is a higher likelihood that the author will be more inclined to embrace the fedback received. In some cases, feedback recipients may disengage not due to their lack of awareness but rather because they are unsure how to adress the problems identified by the peer reviewer.

In addition to the AI monitoring and evaluation employed during student reviewers' feedback creation, EvaluMate incorporates another mechanism, namely author evaluation. This mechanism serves dual purposes: ensuring the quality of per feedback while promoting peer interaction. After student reviewers submit their feedback, t is shared with the author. The author has the opportunty to read the feedack and make revisins to their essy draft accordingly. Crucially, EvaluMate includes an author response feature that allows authors to provide their thoughts on the received feedback (Fig. 5).

Firstly, authors evaluate the helpfulness of the feedback using a five-point scale ( ${ \bf \nabla } ^ { 1 } =$ very unhelpful; $5 =$ very helpful). Secondly, they write responses to the reviewer's comments, indicating the revisions they have made or presenting counter arguments to any comments they may disagree with. These ratings and responses are then conveyed to the student reviewer, which has the potential to enable them to comprehend and asess the effectiveness of their fedback from the author's perspective. This practice draws inspiration from the academic publishing field, where authors and reviewers engage in an exchange of ideas during the peer review proces. However, in the writing classroom, such practices are not always implemented due to limitations in class time and the traditional teacher-centred pedagogical approach. Integrating this interactive activity into the system would offr opportunities for feedback recipients to expresstheir opinions and enable feedack providers to understand the impact of their feedback. This could enhance students' awarenessof the audience when generating peer eedack (Er et al., 2021; Zhang et al., 2024). Furthermore, knowing that their feedback will be read and implemented is likely to foster feedback providers' motivation and engagement.

# Your essay has received a reviewer score of 4

![](img/326c7d80a80da4c85fcc9018ad60a43c2289f0d84f77da921f653271c52a6cda.jpg)  
Fig. 5. Author response interface within EvaluMate.

# 4. Limitations

The current design of EvaluMate exhibits certain limitations that warrant consideration. Firstl, the AI monitoring and feedback system primarily focuses on evaluating the qualitative comments provided by student reviewers, while their quantitative scoring remains unsupervised. Future studies may addressthis gap by incorporating techniques proposed in previous research (eg., l Alaoui, 2023; Hernandez-Gonzalez & Herrera, 2023; Li, 2023) to enable comprehensive monitoring and evaluation of both qualitative comments and quantitative scoring. For instance, Li (2023) has suggested the calculation of a rating accuracy measure, which compares a student reviewer's scores with the average scores given by other students who review the same essay. This measure could potentially indicate how accurately student reviewers have evaluated their peers essays, contributing to the validity and fairness of the assessment process.

Secondly, the chatbot's design is constrained by the limited memory capacity of the LLM used, namely ChatGPT. If the conversation exceeds a certain length of words, the performance of the LLM may be afected. As a result, there is a maximum feedback provision limit of three times for student comments in each peer review task see Fig. 3). This limitation also prevents the iclusion of the essay being assessd in the prompt used to generate ChatGPT output. Consequentl, the chatbot may be unable to provide tailored feedback on student reviewers' comments. To overcome this limitation, future studies could explorethe utilisation of more advanced LLMs with higher memory capacity. By incorporating the essay being asessed into the chatbot'sknowledge base, the chatbot would be able to offer more personalised and helpful feedback, ultimately enhancing the quality of students' peer feedback.

# 5. Future considerations

Existing research on peer asessment has primarily focused on the feedback recipients, examining how they perceive and use the feedback received, as well as the impact of peer assessment on their writing sill delopment. Comparatively, fewer studies have explored ways to support and engage feedback providers in the peer asessment process However, it is crucial to recognize that the first tep in theentir er fdback procs ies in the provision fedack by studnt reiewers. The quality of their fedback would determine the succes of the learning activity. Theefore, it is imperative to nhance students feedack provision skils, which would contribute to their ovral feedack literacy and foster their accetance and utilistion of perfedack when they themseles become recipients.

The integration of AI technologies into language education has gained increasing attention and has transformed the learning experience for students. Since the release of ChatGPT in November 2022, substantial research has been conducted to explore the potential of LMs in enhancing language teaching and learning, particularly in the context of writing. This article contributes to this body of research by inroducing LLMs into peer feedback activities. The proposed Al-supported approach to peer feedback provision appears to be time-eficient and effective in training students to become proficient per reviewers. Therefore, it i recommended that writing teachers incorporate this approach and the per rvie system into thir teaching practices. By doing so, te likelihood of lowquality peer feedback could be minimised, and the validity and credibility of peer assessment could be enhanced. Furthermore, adopting the proposed approach has the potential to promote firness in peer evaluation by motivating student reviewers to invest more effort in their evaluations and produce more valuable feedback. This, in turn, would support the growth and development of the students being assessed.

However, it is crucial to consider the potential biases introduced by Al technologies and their implications for writing asessment. AI algorithms, if not properly developed and monitored, can inadvertently perpetuate biases present in the training data or the al. gorithm's design. To mitigate this risk, it is essential to ensure that the AI system is trained on diverse and representative data encompassing various writing styles, genre, and student populations. Additionally, regular monitoring and evaluation of the AI system's performance can help detect and rectify any biases that may arise over time, ensuring afair and unbiased asessment proces.

For writing researchers, it wil be interesting to investgate how students engage with AI-generated feedback to revise and improve their peer feedback comments. Additionall, exploring the effcts of the proposed learning approach on the quality of student re viewers' peer feedback and their own writing ailities will be important. Furthermore, considering the perspective of feedback re cipients is also valuable. For instance, comparing the uptake of peer feedback generated solely by student reviewers versus that produced with the assistance of Al would provide insights into the proposed approach. Leveraging feedback recipients' responses to peer feedback presents an exciting opportunty to trainLLM-based feedback evaluation tools like EvaluMate, enabling them to value specific features and improve their overall performance. Future research could investigate the integration of fedback recipient responses as a training mechanism to enhance the efectivenes of such tool. Lasty, examining the limitations and potential biases associated with AI-supported per feedback provision would contribute to a comprehensive understanding of the learning approach, ensuring the integrity and fairness of the peer assessment process.

# Funding

This work was supported by the Research Postgraduate Student Inovation Award 2022/23, awarded by the Graduate School of th University of Hong Kong, to the author.

# CRediT authorship contribution statement

Kai Guo: Conceptualization, Software, Funding acquisition, Writing - original draft, Writing - review & editing.

# Declaration of Generative AI and AI-assisted technologies in the writing process

During the preparation of this work the author used ChatGPT in order to improve readabilit and language. After using this tool,the author reviewed and edited the content as needed and takes full responsibility for the content of the publication.

# Declaration of Competing Interest

None.

# Data Availability

No data was used for the research described in the article.

# References

Bansh  man i,  o  ler, 2024) a  i  wt   feback? International Journal of Educational Technology in Higher Education, 21(23), 1-15. https://doi.org/10.1186/s41239-024-00455-4   
hang, 015 me   fit 21. 10.1016/j.asw.2015.04.001   
Che   i   . 0 f f   s  l learning outcome in musical theater perfomance. omputers & dcation, 150, Article 103856. htps://do.org/10.1016/j.compedu.2020.103856   
Cho, K., & MacArthur, C. (2011). Learning by reviewing. Jounal of Edcational Psychology, 103(1), 73-84. htps://do.org/10.1037/a0021950   
Deg     e Assessment & Evaluation in Higher Education, 1-14. https:/doi.org/10.1080/02602938.2023.2227358   
laui3.  t d it g e is o e, 66) 892-899. https://doi.org/10.1109/TLT.2023.3321660   
r,   i Education, 46(4), 586-600. https://doi.org/10.1080/02602938.2020.1786497   
lpar    i  y  .g 53, Article 100644. https://doi.org/10.1016/j.asw.2022.100644   
Gu  Ch  . 2022.pin ti a   wig  ts ci  1. doi.org/10.1177/00336882221143192   
Hn,. 0     c Education, 45(5), 680-696. https://doi.org/10.1080/02602938.2019.1689545   
Hn Technologies, 16(6), 926-939. https://doi.org/10.1109/TLT.2023.3319733 dance course. Computers & Education, 96, 55-71. https://doi.org/10.1016/J.COMPEDU.2016.02.004   
Husan  b   rl   B .018   w d     fak perceptions and essa peformance Asesment & alatin in Highe dcation, 436), 955-968. tps:/oi.og/10.1080/02602938.2018.1424318   
an      .  o   f i y writing. Interactive Learning Environments, 1-13. https:/doi.org/10.1080/10494820.2022.2093914   
oaashi   qt      6 (1), 98-110. https://doi.org/10.14742/ajet.4694 j.asw.2023.100746 perceived fairness and attitude toward the system. Computers & Education, 116, 81-92. htps://doi.org/10.1016/j.compedu.2017.08.010   
She  i  .0     n  st h  . n Educational Evaluation, 64, Article 100821. https:/doi.org/10.1016/j.stueduc.2019.100821   
Velamaz   . t  23      tie  g learners' preferences and behaviors. Computers & Education., Article 104848. https://doi.org/10.1016/j.compedu.2023.104848   
u . .2f n  i  ktie  nf y  t.mricn Educational Research Journal, 58(3), 492-526. https://doi.org/10.3102/0002831220945266   
Yu . 2019.  fro ngr ack o t t  sers st in the  ct.  ng 4 42-52. https://doi.org/10.1016/j.asw.2019.03.004   
Yu, . 2 Education, 46(1), 36-53. https://doi.org/10.1080/02602938.2020.1742872   
ag thti . t t  qt   e. Assessing Writing, 51, Article 100597. https://doi.org/10.1016/j.asw.2021.100597   
ag    2t feedback uptake. Teaching and Teacher Education, 138, Article 104408. https:/doi.org/10.1016/j.tate.2023.104408