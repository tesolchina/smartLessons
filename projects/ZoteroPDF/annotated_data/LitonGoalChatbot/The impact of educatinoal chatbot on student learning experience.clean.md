---
authors: []
category: research
confidence_score: 0.8
document_type: journal
has_abstract: true
has_methodology: true
has_results: true
key_findings:
- Employing chatbots can greatly enhance student learning experiences by allowing
  them to study at their own speed with less stress, saving them time, and keeping
  them motivated
- Integrating these AI systems into a smart classroom will create a supportive environment
  by encouraging good interactions with students and allow learners to be more engaged
  and achieve better academic objectives
methodology: quantitative
publication_year: null
research_questions: []
source_file: The impact of educatinoal chatbot on student learning experience.clean.md
subject_area: education
tags:
- artificial intelligence
- conversational agents
- natural language processing
- deep learning
- e-learning
title: The impact of educational chatbot on student learning experience
---

# The impact of educational chatbot on student learning experience

## Abstract

Artificial Intelligence (AI) technologies have increasingly become vital in our everyday lives. Education is one of the most visible domains in which these technologies are being used. Conversational Agents (CAs) are among the most prominent AI systems for assisting teaching and learning processes. Their integration into an e-learning system can provide replies suited to each learner's specific needs, allowing them to study at their own pace. In this paper, based on recent advancements in Natural Language Processing (NLP) and deep learning techniques, we present an experimental implementation of an educational chatbot intended to instruct secondary school learners Logo, an educational programming language. The related chatbot was implemented and evaluated in Moroccan public schools with the support of teachers from the Regional Center for Education and Training Professions of Souss Massa. The experiments included 109 students grouped into three separate classes. One is a control class group that uses a traditional approach, while the other two are experimental groups that employ digital content and the chatbot-based method. Preliminary findings indicate that employing chatbots can greatly enhance student learning experiences by allowing them to study at their own speed with less stress, saving them time, and keeping them motivated. Furthermore, integrating these AI systems into a smart classroom will not only create a supportive environment by encouraging good interactions with students, it will also allow learners to be more engaged and achieve better academic objectives.

## 1 Introduction

Educational technologies like learning management systems (LMS) and Massive Open Online Courses (MOOCs) have undoubtedly revolutionized teaching and learning processes by providing increased access to academic resources and enabling innovative teaching techniques (Ferguson & Sharples, 2014). While these technologies play a crucial role, certain essential responsibilities of teachers, such as personalized motivation, tailored feedback, and individualized program adaptation, are not entirely altered by these new technologies.

Traditional e-learning often lacks personalized support and real-time interactions with teachers, which can limit student engagement and limit effective learning experiences (Islam et al., 2015; Rawashdeh et al., 2021). Without the presence of teachers or educational professionals, learners are often left with static content and limited opportunities for immediate feedback, individualized assistance, and tailored learning experiences. The absence of teacher-student interactions in traditional e-learning settings may lead to decreased motivation, lack of accountability, and reduced opportunities for collaborative learning (Klisowska et al., 2020; Raspopovic et al., 2017). Consequently, learners may struggle to actively engage with the material and address their individual learning needs, potentially impeding their overall academic progress.

To address these limitations, there is a growing interest in the integration of Conversational Agents (CAs) in e-Learning environments. CAs, also known as chatbots or virtual tutors, are AI-powered systems designed to simulate human-like conversations and provide interactive support to learners. These intelligent agents are capable of engaging with students in natural language interactions, delivering personalized responses, and offering targeted assistance based on individual learning preferences and needs. Nowadays, these technologies are one of the most widely used AI technologies across a variety of industries, including banking, marketing, health and education (Hwang & Kim, 2021; Lekha et al., 2020; Ait Baha et al., 2022; Lee et al., 2022). Thanks to recent developments in Machine Learning (ML) and Natural Language Processing (NLP) techniques, these systems are able to engage with their users in a variety of ways using natural language.

Through the integration of CAs into e-Learning systems, learners gain access to real-time and adaptive support that mimics the role of a human teacher. CAs can provide immediate feedback, answer questions, offer explanations, and deliver additional learning resources, all tailored to the learner's specific requirements (Kuhail et al., 2023). This personalized guidance and interactive dialogue foster a more engaging and effective learning experience, allowing students to overcome challenges, deepen their understanding, and progress at their own pace. Additionally, these systems could assist educators by liberating

## Educational Conversational Agents for Language Learning: A Study in French Education

## Research Questions and Overview

The proposed chatbot was examined in a real-world setting, specifically using French since it is the first foreign language offered at a public College in Morocco. We conducted analyses based on the acquired data to answer four important research questions:

- RQ1: How effective are students' interactions with the proposed chatbot?
- RQ2: In what ways can the chatbot offer information and teach content to students?
- RQ3: Do learners who use the chatbot outperform pupils who learn in a traditional classroom setting?
- RQ4: How engaged is the student while adopting a chatbot-based learning approach?

Through these analyses, we aimed to evaluate the effectiveness and impact of the chatbot on student learning experiences and outcomes. The data collected allowed us to gain insights into the quality of students' interactions with the chatbot, the various ways in which the chatbot provided information and taught content, and the potential advantages of using the chatbot over traditional classroom learning approaches.

## Related Work

### Overview of Conversational Agents

Conversational agents refers to AI systems that can communicate and converse in natural language with people or other agents. Technologies such as voice assistants (Speech recognition and speech synthesizer) and chatbots are included in these systems. The first generation of conversational agents focused on answering users' questions through rule-based (Weizenbaum, 1966) and retrieval-based approaches (Croes & Antheunis, 2021). Despite the fact that these models' responses are grammatically correct, they lack in generating diversified replies due to the use of predefined question/answer pairing. To address these shortcomings, generative-based models have been developed (Adiwardana et al., 2020). Taking advantage of recent advancements in machine learning and natural language processing techniques, generative-based models may engage with people, identify their requests, map their preferences and offer a suitable action without requiring human intervention. Conversational agents have emerged as valuable tools in the field of education, offering unique benefits that make them educationally valuable (Ait Baha et al., 2022).

### Overview of Educational Conversational Agents

Unlike traditional conversational agents, educational conversational agents are specifically designed to support learning, monitor progress, and assist students in their educational journey. The distinctive feature of educational conversational agents lies in their capability to offer personalized and tailored support to meet the unique needs of individual learners.

In recent years, the use of chatbots in education has drawn more attention. Most studies on educational chatbots in the literature have focused on supporting learning, monitoring, and assisting as their core roles:

1. Supporting learning (teaching): Chatbots serve as a medium for transmitting knowledge or skills, such as providing a voice-assistant digital person to enhance learning at home (Ait Baha et al., 2022).

2. Assisting: Chatbots ease the learning process by making information more accessible or automating tasks, such as responding to FAQs about test dates or office hours (Sandoval & Zoroayka, 2018).

3. Monitoring: These chatbots focus on student self-improvement, with conversation centered on motivating learners to plan, analyze, or evaluate their development, such as providing life skills tutoring for mental health support during adolescence (Gabrielli et al., 2020).

The goals of these chatbots primarily focus on improving student motivation, academic achievement, and competency development. In our experiment, particular attention was given to the role of learning and assisting chatbots, designed to serve as a medium for transmitting knowledge and skills, as well as to ease the learning process for students.

## Methodology

Specifically, in this section, we highlight the first completed experience, which enabled us to undertake an early validation of the utility and advantages of the chatbot with secondary school students studying Logo at a college in the Souss Massa region of Morocco.

Quasi-experimental designs (Harris et al., 2006) were applied to understand whether the implementation of the virtual tutor affects learners' learning effectiveness. The sample utilized for the experiment is detailed in the subsections below. The process of the evaluation technique is depicted in Fig. 1.

## Experimental settings

The experiment in this study was conducted over a span of five class sessions, with each session lasting approximately 2 hours. The sample consisted of third-year secondary school students who were divided into three different classes: one control class (CC) and two experimental classes (EC).

In the control class (CC), the conventional teaching approach was followed. The teacher delivered lessons in a traditional manner, which included explaining algorithms and programming concepts, engaging in discussions with the students, assigning exercises, and providing feedback through class interactions. This approach focused on the teacher-led instruction and the dissemination of information through lectures and class discussions.

On the other hand, the experimental classes (EC) implemented two distinct teaching strategies to explore alternative approaches to enhance the learning experience:

- In EC1, the suggested chatbot-based strategy was employed, utilizing an educational chatbot as a virtual tutor. The chatbot facilitated student engagement by offering interactive conversations and tailored assistance throughout the learning materials. This strategy aimed to provide personalized support and enhance the students' learning experience.

- In EC2, an alternative strategy was employed, which involved the use of additional digital learning materials. These materials included videos, digital files (such as PDFs and PowerPoint presentations), and other multimedia resources. The purpose of integrating these materials was to supplement the traditional teaching methods and provide students with a variety of resources to enhance their understanding and engagement with the educational content.

All three classes covered the same educational content, ensuring a fair comparison between the different teaching strategies. This allowed for a focused investigation into the effectiveness of the chatbot-based strategy and the use of digital learning materials as compared to the conventional teaching approach.

To assess the impact of these teaching strategies, a pre-test and a post-test were conducted to evaluate the content and knowledge acquisition of the students. These tests consisted of a series of questions designed to measure the students' understanding and progress. Additionally, students were prompted to respond to questions and complete activities as they advanced through the learning process (See Appendix A). Furthermore, an additional questionnaire was presented to the learners in the experimental group (EC1) to measure their satisfaction with both the usability of the chatbot and their overall learning experience (refer to subsection 3.5). This allowed for the collection of valuable feedback regarding the students' perceptions and satisfaction with the chatbot-based strategy.

## Participants

The control and experimental groups were carefully selected to ensure a balanced representation of learners based on demographic variables, including gender and their level of fundamental competencies. The study included a total of 109 third-year secondary school students. The students' competency levels were determined based on the grades obtained in the first semester. By categorizing the students according to their academic performance, the study aimed to create comparable groups for a comprehensive analysis. Table 2 provides a comprehensive overview of the experiment, presenting the details categorized by group, competence level, and teaching approaches.

[Table 1 and Figure 1 preserved as in original]

Here's the cleaned Markdown:

### 3.3 Pre-test

Before starting the educational program, a questionnaire-based pre-test was completed by students. The purpose of this test is to collect information about the situation and the potential for conducting this investigation. The questionnaire asked about the students' access to the internet, their use of phones, and their preferred types of digital resources for learning. Most students favor animated digital content (videos, PPTs, and PDFs) over printed documents and have access to smartphones and the internet. Additionally, they favor utilizing a virtual assistant to aid with learning. However, they have no prior knowledge of using chatbots.

### 3.4 Post-test

The teaching sessions ended with learners filling out a questionnaire-based pre-test. The goal of this quiz is to evaluate the efficacy of the educational program that used the three teaching techniques. There were a total of 4 exercises and a practical exercise in this test (see Appendix B).

### 3.5 The proposed chatbot evaluation questionnaire

A final questionnaire was subsequently presented to learners in the experimental group (EC1), where the chatbot-based teaching technique is employed, to measure their satisfaction with both the chatbot's usability and their entire learning experience. Eight questions made up this questionnaire, which was divided into two parts. Questions in the first part evaluated learners' learning experiences using the proposed chatbot, while questions in the second part evaluated participants' learning experiences in regard to the chatbot-based teaching approaches (see Appendix C). 

| Groups | Competence Level | Teaching method | Participants | Girls | Boys | Total |
|--------|------------------|-----------------|--------------|-------|------|-------|
| Control Class (CC) | High level (42.1%)<br>Intermediate level (47.4%)<br>Low level (10.5%) | Traditional learning | 23 | 15 | 38 |
| Experimental Class (EC1) | High level (31.6%)<br>Intermediate level (57.9%)<br>Low level (10.5%) | Chatbot-based learning | 11 | 23 | 34 |
| Experimental Class (EC2) | High level (34.2%)<br>Intermediate level (52.6%)<br>Low level (13.2%) | Digital content based learning | 25 | 12 | 37 |
| Total: 109 |

Mostly three-point satisfaction measures were used to collect the responses (Satisfied, Neutral, and Dissatisfied). This questionnaire was carefully designed to evaluate the satisfaction and learning experience of participants within the specific context of chatbot-based learning. A pilot study with a subset of participants was done to confirm the reliability of the questionnaire, and the consistency of the questionnaire questions was verified using Cronbach's alpha coefficient (Cronbach, 1951). The found alpha coefficient of 0.937 demonstrated high reliability, indicating that the questionnaire items measured the target variables consistently. On the other hand, content validity was established through consultation with experts in educational technology.

## 4 Proposed system

The proposed system is an innovative instructional chatbot that applies the fundamental concept of teaching Logo content in an interactive educational environment. This technology is mostly focused on message exchanges between a learner and a virtual tutor. The virtual tutor attempts to guide students via the conversation in order to explore and learn the programming language content. The chatbot supports the French language since it is the first foreign language used in Moroccan public schools.

### 4.1 Design principal

Our proposed chatbot was designed to fulfill the following primary functional needs:

- The learner interacts with the chatbot through structured dialogue.
- The learner can direct the conversation through using multiple alternatives, such as Buttons.
- The chatbot may be accessed online.
- The chatbot understands its learner's first foreign language (French).
- In the situation of a message misunderstanding, the chatbot alerts the user so that he may take the required action, such as reformulating

## Results & Discussion

## Results

The study utilized a pre-test and a post-test to compare the knowledge gained by participants in the control and experimental groups, with one group using the proposed chatbot-based approach and the other group using different teaching techniques. In the first experimental group, which used the chatbot, the average performance of the 34 learners was 10.97 with a standard deviation of 4.03. The second experimental group, using digital content, had an average performance of 12.35 with a standard deviation of 3.80 for the 37 learners. In the control class, the average performance was 10.5 with a standard deviation of 3.34 for the 38 learners. The success rates in the examinations were 65% for the chatbot-based experimental group (EC1), 78% for the experimental group using digital content (EC2), and 71% for the control group (CC).

### Implementation on the e-learning platform

The conversational agent was integrated into the educational program's official webpage. The website was developed to handle the educational resources and interactive learning activities of the course (pedagogical, assessment, communication, and/or collaboration features). On the website, the chatbot was proposed as a pop-up window. Initially, the bot is minimized. A chat widget is opened by clicking the button (bottom-right side). To start, the bot requests that the user enter his name. After this, the user can begin asking questions concerning Logo.

### Architecture Components

1. The interface layer receives user input (in text form), processes the request by passing it through to the conversation engine layer, and returns the final response to the endpoint once processing is complete.

2. Conversation engine layer, which is composed of:
   - The NLU component for categorizing user utterances into predetermined classes (intents)
   - The DM component for tracking dialogue state and managing conversation data
   - The NLG component for turning chosen actions into natural language responses

3. Data layer, consisting of databases that store conversational and non-conversational data used by the dialogue manager.

### Study Findings

Notably, none of the participants had previous experience with chatbots. In response to RQ1, the majority of participants (82%) expressed satisfaction with their interactions with the chatbot as a learning tool, with the remaining participants being neutral. However, 52% of participants reported linguistic difficulties due to the chatbot using their first foreign language (French), while only 20% encountered technical difficulties.

Addressing RQ2, conversational agents significantly enhanced traditional instruction by offering an ergonomic e-learning platform where students could study at their preferred time and pace without fear of making mistakes.

Regarding RQ3, chatbot users did not outperform students who learned through traditional classroom methods.

For RQ4, most students reported learning at their own pace, experiencing less stress, saving time, and feeling motivated while using the chatbot compared to traditional learning methods. Many participants expressed interest in using chatbots in future programs.

| Groups | N | Mean | Standard Deviation (SD) | Success Rate |
|--------|---|------|----------------------|--------------|
| Control Class (CC) | 38 | 10.5 | 3.34 | 71% |
| Experimental Class (EC2) | 37 | 12.35 | 3.80 | 78% |
| Experimental Class (EC1) Chatbot-based method | 34 | 10.97 | 4.03 | 65% |

## Discussion

Based on the findings from the evaluation of our proposed chatbot-based approach, several important considerations emerged regarding the application of chatbots as virtual instructors in the classroom.

Our study revealed that conversational agents, such as chatbots, can significantly enhance conventional instruction in various ways. By utilizing an ergonomic e-learning platform, students have the flexibility to study their chosen subjects at their preferred time and pace, free from the fear of making mistakes. The results of the study indicate that the implementation of the proposed chatbot-based approach, as well as the use of digital content, led to improved knowledge acquisition compared to the control group. The average performance scores of the experimental groups using the chatbot and digital content were 10.97 and 12.35, respectively, while the control group had an average performance of 10.5. These findings suggest that both the chatbot-based approach and digital content were effective in enhancing students' knowledge acquisition.

The average performance scores and success rates were higher in the experimental groups, indicating the effectiveness of these interventions in enhancing students' learning outcomes. However, it is crucial to examine the educational outcomes of this innovative approach and understand its potential contributions to student learning and development. In this study, we aimed to investigate the educational outcomes of chatbot-based learning and explore its impact on various factors that influence students' learning experiences.

One of the key factors examined in this study was knowledge acquisition. Through the use of chatbots, students were able to engage in interactive and personalized learning experiences, which facilitated the acquisition of subject-specific knowledge. These findings are consistent with prior studies by (Sandoval & Zoroayka, 2018; Essel et al., 2022), where chatbot-based learning positively influenced knowledge acquisition. Our results contribute to the growing body of evidence that supports the role of chatbots in fostering subject-specific knowledge acquisition.

Another significant outcome explored in this study was the impact of chatbot-based learning on student engagement and motivation. The interactive nature of chatbots and their ability to provide immediate feedback and support created an engaging learning environment. Students reported increased motivation and a higher level of active participation in their learning process. This finding suggests that chatbot-based learning can enhance students' intrinsic motivation and foster a positive attitude towards learning which aligns with the findings of (Chang et al., 2022; Sandu & Gide, 2019) in their research on chatbots' effects on student engagement.

Language proficiency was a significant educational outcome investigated in our study. The utilization of the chatbot in participants' first foreign language, specifically French, offered an immersive language learning experience. It is crucial to acknowledge that the use of chatbots in a foreign language context, as observed in our study, presented certain linguistic challenges for participants, affecting their complete comprehension of the educational content. This observation is in line with previous research by (Huang et al., 2022), who noted that language learning through chatbots requires careful attention to linguistic complexities. This inspired us to explore the potential of integrating the chatbot as a tool to complement the Content and Language Integrated Learning (CLIL) approach (Harrop, 2012; Mageira et al., 2022). By adopting this approach, in addition to acquiring knowledge in the programming domain, students also develop essential vocabulary and language skills specific to the chosen language of instruction.

Furthermore, chatbot-based learning has demonstrated a positive influence on students' self-directed learning capabilities. Through engagement in autonomous conversations with the chatbot, students are encouraged to assume responsibility for their learning journey and develop self-regulation skills. This alignment is mirrored in the study by (Han et al., 2022), reinforcing our own investigation by highlighting how students progressively cultivate autonomy and enhanced self-directed learning practices. Han et al.'s findings, much like our own, indicate a notable shift towards increased independence and improved self-directed learning habits among students.

Social interaction and collaboration were also observed as important outcomes of chatbot-based learning. While students primarily interacted with the chatbot, the study highlighted the potential for chatbots to facilitate peer collaboration through group discussions and knowledge sharing. This observation

Here's the cleaned Markdown:

In conclusion, this study provides valuable insights into the educational outcomes of chatbot-based learning. The findings demonstrate the positive impact of chatbot-based learning on various factors, including knowledge acquisition, engagement and motivation, language proficiency, self-directed learning, and social interaction. These outcomes highlight the potential of chatbot-based learning to transform traditional educational approaches and offer personalized and interactive learning experiences. It is important to acknowledge that this study represents the first version of the chatbot system. Further research and development are needed to address technical challenges, enhance the chatbot's functionality, and explore additional educational outcomes. Future investigations can focus on developing an improved version of the chatbot, incorporating natural language and computer languages to further enhance the learning experience. Additionally, exploring students' adaptation to this new technology and incorporating adaptive learning techniques can further enhance the personalized nature of chatbot-based learning.

## Conclusion

In conclusion, our study highlights the practical implications of integrating an AI-powered chatbot into an e-learning system to support students in their learning process. This innovative feature aims to assist teachers in delivering programming language content by enabling students to ask questions and receive responses that enhance their understanding and overall learning experience. The suggested chatbot was tested in French as it is the first foreign language given at a Moroccan public college. The findings from our experiments demonstrate the effectiveness of deploying AI-powered chatbots in enhancing students' educational experiences. The majority of participants found the use of chatbots in the classroom to be highly engaging, and many expressed a desire to continue utilizing this approach in future programs. The chatbot's interactive nature not only provides students with the answers they need, reducing uncertainty in various subjects of study, but also alleviates the teacher's workload and strengthens the teacher-student relationship. To further solidify our conclusions regarding the pedagogical efficiency of the chatbot-based teaching approach, future investigations should involve an improved version of the proposed system and a larger sample size of participants. This will enable us to draw more robust conclusions about the effectiveness and broader applicability of chatbot-based learning across different learning contents and contexts. The potential practical use of chatbot-based learning in other educational domains merits more investigation and research to fully explore its benefits.

## Abbreviations

AI: Artificial Intelligence  
CA: Conversational Agent  
ML: Machine Learning  
NLP: Natural Language Processing  
LMS: Learning Management System  
MOOCs: Massive Open Online Courses  
NLU: Natural Language Understanding  
DM: Dialogue Manager  
NLG: Natural Language Generation  
FAQs: Frequently Asked Questions

## Acknowledgements

This work was supported by the Ministry of Higher Education, Scientific Research and Innovation, the Digital Development Agency (DDA), and the CNRST of Morocco (Al-Khawarizmi program, Project 22). Authors are thankful to all the teaching staff from the Regional Center for Education and Training Professions of Souss Massa (CRMEF-SM) for their help in the evaluation, and all of the participants who took part in this study.

## Authors' contributions

- TA: Conceptualization, methodology, software, validation, investigation and writing—original draft preparation
- ME: Supervision, validation, project administration and funding acquisition and writing—review and editing
- YE: Supervision, writing—review and editing
- HF: Supervision, writing—review and editing

All authors read and approved the final manuscript.

## Funding

This work was supported by the Ministry of Higher Education, Scientific Research and Innovation, the Digital Development Agency (DDA), and the CNRST of Morocco (Al-Khawarizmi program, Project 22).

## Data availability

The datasets used and/or analyzed during the current study are available from the corresponding author on reasonable request.

## Declarations

The authors declare that they have no competing interests.

## References

Adiwardana, D., Minh-Thang Luong, So, D. R., & Hall, J. (2020). Towards a Human-like Open-Domain Chatbot. https://arxiv

Here is the cleaned Markdown:

## References

- Han, J.-W., Park, J., & Lee, H. (2022). Analysis of the effect of an artificial intelligence chatbot educational program on non-face-to-face classes: A quasi-experimental study. BMC Medical Education, 22(1), 830. https://doi.org/10.1186/s12909-022-03898-3

- Harris, A. D., McGregor, J. C., Perencevich, E. N., Furuno, J. P., Zhu, J., Peterson, D. E., & Finkelstein, J. (2006). The Use and Interpretation of Quasi-Experimental Studies in Medical Informatics. Journal of the American Medical Informatics Association, 13(1), 16–23. https://doi.org/10.1197/jamia.M1749

- Harrop, E. (2012). Content and Language Integrated Learning (CLIL): Limitations and Possibilities. In Online Submission. https://eric.ed.gov/?id=ED539731

- Huang, W., Hew, K. F., & Fryer, L. K. (2022). Chatbots for language learning—Are they really useful? A systematic review of chatbot-supported language learning. Journal of Computer Assisted Learning, 38(1), 237–257. https://doi.org/10.1111/jcal.12610

- Hwang, S., & Kim, J. (2021). Toward a Chatbot for Financial Sustainability. Sustainability, 13(6), 6. https://doi.org/10.3390/su13063173

- Islam, N., Beer, M., & Slack, F. (2015). E-Learning Challenges Faced by Academics in Higher Education: A Literature Review. Journal of Education and Training Studies, 3(5), 5. https://doi.org/10.11114/jets.v3i5.947

- Ji, H., Han, I., & Ko, Y. (2023). A systematic review of conversational AI in language education: Focusing on the collaboration with human teachers. Journal of Research on Technology in Education, 55(1), 48–63. https://doi.org/10.1080/15391523.2022.2142873

- Klisowska, I., Seń, M., & Grabowska, B. (2020). Advantages and disadvantages of distance learning. E-Methodology, 7(7), 7. https://doi.org/10.15503/emet2020.27.32

- Kuhail, M. A., Alturki, N., Alramlawi, S., & Alhejori, K. (2023). Interacting with educational chatbots: A systematic review. Education and Information Technologies, 28(1), 973–1018. https://doi.org/10.1007/s10639-022-11177-3

- Lee, K., Jo, J., Kim, J., & Kang, Y. (2019). Can Chatbots Help Reduce the Workload of Administrative Officers? - Implementing and Deploying FAQ Chatbot Service in a University. In C. Stephanidis (Ed.), HCI International 2019—Posters (pp. 348–354). Springer International Publishing. https://doi.org/10.1007/978-3-030-23522-2_45

- Lee, Y.-F., Hwang, G.-J., & Chen, P.-Y. (2022). Impacts of an AI-based chatbot on college students' after-class review, academic performance, self-efficacy, learning attitude, and motivation. Educational Technology Research and Development, 70(5), 1843–1865. https://doi.org/10.

## References

Rawashdeh, A. Z. A., Mohammed, E. Y., Arab, A. R. A., Alara, M., & Al-Rawashdeh, B. (2021). Advantages and Disadvantages of Using e-Learning in University Education: Analyzing Students' Perspectives. Electronic Journal of E-Learning, 19(3), 3. https://doi.org/10.34190/ejel.19.3.2168

Sandoval, & Zoroayka. (2018). Design and implementation of a chatbot in online higher education settings. Issues in Information Systems, 19(4).

Sandu, N., & Gide, E. (2019). Adoption of AI-Chatbots to Enhance Student Learning Experience in Higher Education in India. 2019 18th International Conference on Information Technology Based Higher Education and Training (ITHET), 1–5. https://doi.org/10.1109/ITHET46829.2019.8937382

Tegos, S., Psathas, G., Tsiatsos, T., Katsanos, C., Karakostas, A., Tsibanis, C., & Demetriadis, S. (2020). Enriching Synchronous Collaboration in Online Courses with Configurable Conversational Agents. In V. Kumar & C. Troussas (Eds.), Intelligent Tutoring Systems (pp. 284–294). Springer International Publishing.

Weizenbaum, J. (1966). ELIZA—a computer program for the study of natural language communication between man and machine. Communications of the ACM, 9(1), 36–45. https://doi.org/10.1145/365153.365168

Xiao, Z., Zhou, M. X., & Fu, W.-T. (2019). Who should be my teammates: Using a conversational agent to understand individuals and help teaming. Proceedings of the 24th International Conference on Intelligent User Interfaces, 437–447. https://doi.org/10.1145/3301275.3302264

Yin, J., Goh, T.-T., Yang, B., & Xiaobin, Y. (2020). Conversation Technology With Micro-Learning: The Impact of Chatbot-Based Learning on Students' Learning Motivation and Performance. Journal of Educational Computing Research. https://doi.org/10.1177/0735633120952067

## Author Information

Tarek Ait Baha is PhD student in Artificial Intelligence & Natural Language Processing and member of the IRF-SIC Laboratory at Ibn Zohr University.

Mohamed El Hajji is a Professor at the Regional Center for Education and Training Professions in Souss Massa, Morocco, and the head of the project Smart Class for "Smart Adaptation and Recommendation" (CISAR). His research focuses on education and training, Digital learning, Artificial Intelligence, Big Data Science, and Machine Learning.

Youssef Es-Saady is a Professor at the polydisciplinary faculty of Taroudant, Morocco and is a part of the IRF-SIC Laboratory at Ibn Zohr University. His most recent work focuses on a number of initiatives using AI, Big Data, and IoT, notably in education and precision agriculture.

Hammou Fadili is an Engineer and Doctor qualified to lead computer science research. Head of Digital Research at FMSH Paris and Member of Paragraphe laboratory: Digital Innovation and Artificial Intelligence at Paris 8 and CY Cergy Universities and Former of Centre d'Étude et de Recherche en Informatique (CEDRIC) laboratory at CNAM Paris, France.

### Affiliations

1. IRF-SIC Laboratory, Ibn Zohr University, Agadir, Morocco
2. Regional Center for Education and Training Professions - Souss Massa,