---
confidence_score: 0.0
source_file: Adapting self-regulated learning in an age of generative artificial intelligence
  chatbots.clean.md
---

# Adapting Self-Regulated Learning in an Age of Generative Artificial Intelligence Chatbots

Joel Weijia Lai  
Institute for Pedagogical Innovation, Research and Excellence, Nanyang Technological University, 50 Nanyang Avenue, Singapore 639798, Singapore; joellai@ntu.edu.sg

## Abstract

The increasing use of generative artificial intelligence (GenAI) has led to a rise in conversations about how teachers and students should adopt these tools to enhance the learning process. Self-regulated learning (SRL) research is important for addressing this question. A popular form of GenAI is the large language model chatbot, which allows users to seek answers to their queries. This article seeks to adapt current SRL models to understand student learning with these chatbots. This is achieved by classifying the prompts supplied by a learner to an educational chatbot into learning actions and processes using the process-action library. Subsequently, through process mining, we can analyze these data to provide valuable insights for learners, educators, instructional designers, and researchers into the possible applications of chatbots for SRL.

**Keywords**: self-regulated learning; process mining; learning process analytics; generative artificial intelligence; chatbot

## 1. Introduction

Self-regulated learning (SRL) asserts that a learner engaging in SRL succeeds because one can control the learning environment by directing and regulating one's actions based on a learning goal [1,2]. SRL is characterized by interaction with the learning process, for example, actively engaging with the learning material, adapting one's habits to achieve the learning goals, and assuming responsibility for the learning outcomes [3]. Key theoretical foundations include metacognitive theories focusing on awareness and the control of cognition [4]; Zimmerman's cyclical phases model (forethought, performance, self-reflection) [5]; Pintrich's model emphasizing motivation [6]; Bandura's social cognitive theory highlighting self-efficacy [7]; and Deci and Ryan's self-determination theory emphasizing autonomy, competence, and relatedness [8]. Implementing SRL in education involves teaching metacognitive strategies, promoting goal setting, fostering a growth mindset, and providing constructive feedback. Although various theories or models bring different perspectives, they agree that SRL comprises the general objectives of goal setting, plan implementation, and process evaluation [9].

SRL has psychological and social-cognitive benefits for both the learner and the instructor. Studies of the inherent benefits of SRL suggest that it positively affects academic achievement, motivation, and students' beliefs in their abilities [10]. For the learner, SRL facilitates the development of self-efficacy. The process of self-regulation allows learners to monitor their progress actively, set learning goals, and receive feedback to develop an effective learning strategy. As learners experience success and make progress, their confidence grows, leading to increased self-efficacy and motivation. Other psychological benefits include improved metacognitive awareness, enhanced goal orientation, and positive emotional well-being [11-14]. By cultivating SRL skills, learners can develop important psychological resources and competencies that support lifelong learning, personal growth, and success in various domains of life. When students take responsibility for their learning, educators can focus more on guiding and facilitating rather than constantly directing and

## Future Internet 2024, 16, 218

controlling in and outside the classroom, maximizing instructional efficiency [15,16]. This shared responsibility and independence reduce the teacher's workload and provide a more balanced and supportive learning environment. By empowering students to take control of their learning, instructors can witness increased engagement, motivation, and independence among students. This further reaffirms the teacher's belief in their ability to impact the student's academic and social life, fostering a sense of professional accomplishment [17].

In the age of generative artificial intelligence (GenAI), where both instructor and learner are inclined to use artificial intelligence to facilitate the teaching and learning process, it is clear that GenAI is the disruptive technology that has brought prompt-based, contextualized content to every computer. GenAI can produce novel and original content such as text, images, or other forms of media that resemble human-created content. This is achieved through its ability to learn patterns from large datasets and generate content based on learned patterns. There are many use cases of GenAI being used in recent years to create banks of questions for students to answer based on their current level of understanding and achievement; personalized study plans for students based on their performance, strengths, weaknesses, needs, and interests; and to provide tutoring or feedback to students using natural language processing [18].

Take the following examples: TutorAI (https://www.tutorai.me/, accessed on 13 June 2023) is an educational platform that generates interactive content on a topic of choice of the user; and NOLEJ (https://nolej.io/, accessed on 13 June 2023) offers an e-learning module that has interactive video, a glossary, practice, and a summary for a user-chosen topic. Both of these platforms use GenAI technology to produce their content at a much faster pace than any educator can. More capable, innovative, and groundbreaking GenAI tools are released daily. To facilitate learning, students can use GenAI to seek clarification or explain a concept in simpler terms. They can obtain immediate and personalized feedback from GenAI tools in the form of text feedback, communicating areas of improvement and identifying suggestions for enhancement on assignments, essays, or even code submissions from AI bots designed for these specific uses. The learning process is enhanced with feedback catered specifically for the learner to understand their strengths and weaknesses.

Likewise, instructors can use GenAI to generate exciting ideas for lesson materials for a targeted learner group. The capability of GenAI tools to mass produce and provide materials for multiple learning pathways has facilitated lesson planning for many instructors. GenAI can consider the instructor and class profile to provide appropriate scaffolding, learning materials, and activities that cater to each class' specific needs, thus ensuring a more effective and tailored learning experience.

In particular, chatbots present the ability to be a virtual tutor in the absence of an instructor, adult, or peer. GenAI chatbots can operate as virtual tutors that engage in personalized conversations with learners by providing an interactive and adaptive learning environment to answer questions, explain, and offer instant support, assistance, and guidance. Chatbots in education have gained significant traction in recent years [19]. In a systematic review conducted by Okonkwo and Ade-Ibijola [20], the authors concluded that the benefit of using chatbots in an education context is that "Chatbots encourage personalized learning, provide instant support to users, and allow multiple users to access the same information at the same time". In particular, educational chatbots can serve as knowledge repositories, allowing students to retrieve information, review concepts, and interactively engage in practice exercises, enhancing their self-regulated learning process. By engaging in conversations with students, chatbots can also help them articulate their learning objectives, break down goals into actionable steps, and create realistic timelines. This guidance helps students develop a structured approach to their learning and fosters self-regulation in the setting and pursuing of goals. While there are still significant steps forward that chatbots can take, especially with

## Self-Regulated Learning Frameworks for GenAI Chatbots

As with previous research on SRL with educational technology tools such as analyzing trace data on learning management systems [24–26] and massive open online courses [27–30], GenAI is another educational tool that is emerging at a rapid rate. In recent months, new research has emerged aligning the SRL process with the adoption of GenAI, signalling a new frontier for research into this domain. The work by Chiu et al. looks into how motivation and the process of self-determination theory can be fostered with ChatGPT [31]. Another work by Kong and Yang focuses on domain knowledge learning for adolescent learning [32]. With new and emerging research, this work seeks to answer the following questions:

1. Which SRL model helps describe learning processes for GenAI chatbots?
2. How do we identify and classify SRL processes for prompts used for educational chatbots?
3. What learning analytics can we perform?

To answer these research questions, we examine the existing frameworks for SRL in Section 2. We will aggregate our findings from the existing frameworks to develop a refreshed framework suitable for examining SRL in prompts provided to chatbots during the learning process. Next, as a proof-of-concept, we analyze two students' interaction with a chatbot to classify the prompts according to the framework in Section 3. The various stages of the learning process are then examined for learning analytics and are organized and reported in Section 4.

## SRL Framework for Chatbots

Research into self-regulated learning began as early as the 1970s. During this time, several frameworks, theories, and models of SRL have emerged and been developed—some more popular than others and some in greater alignment with others. This section examines a few SRL models to answer the first research question. As this is not a systematic review, we will not evaluate all the existing models but will shed light on why specific models were chosen. We recommend the systematic review by Panadero [9] for an overview of the other models. All the models highlighted in this section and chosen for SRL analysis with GenAI chatbot are aligned in the description and development of the metacognitive aspects of SRL.

### Existing SRL Frameworks and Models

Zimmerman is a prominent researcher who has developed three different SRL models, each with a different focus. The first model, developed with Pons, is a set of 15 self-regulation strategies, comprising self-regulated learning behaviors [33]. This model is useful in identifying the traits of a self-regulated learner. By extension, trace data and prompts provided by the learner to the chatbot can be identified with one or more of these traits, which gives evidence to SRL. 

Secondly, termed the Triadic Analysis of SRL, the model is developed with a focus on the interactions between the environment, behavior, and person [10]. The triadic analysis applied to Bandura's triadic model of social cognition, which asserts the concept of reciprocal determinism, where a person's behavior is influenced by cognitive processes and environmental factors such as social stimuli [7]. While the triadic analysis helps explain behaviors broadly, it is not immediately apparent how it can be made process-driven, which limits its use as a framework within which to answer the research question.

The final model draws from social-cognitive theory, called Zimmermann's Cyclical Phases Model [34,35], which explains the interrelation of metacognitive and motivational processes at the individual level in three domains. The model includes sub-processes classified under each domain: forethought (with sub-processes: task-analysis and self-motivating beliefs); performance (self-control and self-observation); and self-reflection (self-judgment and self-reaction).

Pintrich's work in the field of SRL has been influential due to his contributions to clarifying the conceptual framework of SRL [6]. His efforts to further empirical research on the relationship between SRL and motivation, as well as the development of the widely used MSLQ (Motivated Strategies for Learning

## Self-Regulated Learning with Chatbots: A Process Framework

## Proposed Framework for Chatbot

We amalgamate the SRL processes to discover the underlying patterns of how learners use chatbots for SRL. With disruptive technologies, the framework proposed is suitable for the existing capabilities of conversational chatbots for education purposes.

The SRL framework introduced here is a simple starting point from which to study the SRL process from the data perspective. Conversation data are the most accessible data that chatbots provide; by codifying this data, we can study students' SRL processes by integrating Zimmerman's, Pintrich's, and Winne and Hadwin's models into one.

The process-action framework is developed by strongly considering the metacognitive perspective (called process) from Winne and Hadwin's model, the four phases of SRL by Pintrich and Zimmerman's subprocesses (called actions). In the proposed SRL model for chatbots, there are four learning processes, namely, defining, seeking, engaging, and reflecting, each process has its associated learning action. Table 1 contains a summary of these processes and the description and example prompt to describe the process-action. One should note that chatbots are often not used in isolation. Therefore, certain actions may be associated with user interaction with the chatbot in support of another tool.

### Process-Action Framework

| Process | Action | Code | Description | Conversation Examples |
|---------|---------|------|-------------|---------------------|
| Defining | Identification | D.I | Identifying problems or providing a problem | These are important...; I am given a problem... |
| | Goal-set | D.G | Setting educational goals or sub-goals | I need to achieve...; I want to learn...; Create a checklist... |
| Seeking | Search | S.S | Securing information from a chatbot | Tell me about...; Please recommend some resources...; What is... |
| | Select | S.SL | Recording important information or results | What are the key points...; Extract the main idea of... |
| Engaging | Review | E.RV | Re-engaging with curated material or checking for correctness | This does not seem to be correct...; Does this mean that... |
| | Organise | E.O | Re-arranging materials by category or asking to perform knowledge management | Can you help me to summarise...; Put this in a list/table...; Tell me step by step... |
| | Rehearse | E.RH | Memorising materials or putting it to practice by asking for an example | Can you help me fill the gaps...; Please generate questions on...; I want to spend more time on... |
| Reflecting | Task Evaluation | R.ET | Evaluating the quality of work or indicating an intention to progress | What is the next thing...; I learned (topic), how is this related to (another topic)... |
| | Self Evaluation | R.ES | Evaluating of motivation or checking for learning gaps | Can you tell me where I am lacking...; I am not getting it...; Can you check where I misunderstood... |

## Data Processing and Learning Process-Action Map

This section introduces how the data processing is performed. Raw data are collected from learners by exporting their chat conversation history. This can be carried out natively in ChatGPT, the chatbot of choice in this work. In other educational contexts and class sizes, specialized chatbots can be built to automatically store conversation histories for processing.

Data processing involves parsing raw data containing the prompts submitted by the learner through the process-action library described in Table 1. This process is achieved by manually assigning each prompt to a corresponding process-action code based on how it fits the description and example prompt.

### Proof-of-Concept

As a proof-of-concept, we provide two examples of a student engaging OpenAI's ChatGPT (GPT-3.5). Two learners were tasked with choosing a topic they would like to

## Learning Analytics and Process Mining for Self-Regulated Learning with ChatGPT

## Tables

Table 2. Proof-of-concept of process–action tags for a student engaging ChatGPT to learn about the Shapiro–Wilk test (typographical errors are deliberately left unedited). The full conversation is found at: https://chat.openai.com/share/81f8358a-4303-4fa4-a062-a50d55405809 accessed on 20 June 2023.

| # | Prompts | Code |
|---|----------|-------|
| 1 | I want to study in-depth about the Shapiro-Wilks test | D.G |
| 2 | Great! This is a good overview. However, can you give me an example of how to formulate the null and alternative hypotheses? | S.S |
| 3 | Can you give me an example with data? | S.S |
| 4 | How did you calculate the test statistic in this case? Please do not show me any code. | S.S |
| 5 | Can you point me to some resources that can help me calculate the test statistic using mathematical formulas? | S.S |
| 6 | Thank you. How then do you calculate the p value without using python code? | S.S |
| 7 | How do I obtain the p-value? Can you point me to some resources where I can obtain the p-value? | S.S |
| 8 | Let's go back to the example, in this case the p-value is 0.438 which is greater than the significance level of 0.05. Is there an example where the p-value will be smaller than the significance level? | S.S |
| 9 | Can you help me visualise the two sets of data that you have given by plotting them? | E.O |
| 10 | Going back to the beginning, I think I understand how to calculate the test statistic and find the p-value. Please tell me if I am wrong. The test statistic W is calculated based on a mathematical formula, while the p-value involves a look up statistical table. Am I correct? | E.RV |
| 11 | Note the part about the p-value being calculated from statistical software. I read somewhere about one-tailed and two-tailed test. Does the Shapiro-Wilks test have such a thing? | S.S |
| 12 | What happens if I perform the Shapiro-Wilks test for sample sizes above 5000? | S.S |
| 13 | I think I understand the concepts. Can you quiz me to check if I understand? Please give me 5 multiple choice questions. | E.RH |
| 14 | Are the answers: a, c, d, b, c? | E.RH |
| 15 | I got question 3 wrong, can you explain the concepts relating to question 3 again? | E.RV |
| 16 | Sounds good, I think I am ready to tackle some worked problems and move on to the next topic. What do you suggest I study for the next topic relating to Shapiro-Wilks Test? | R.ET |
| 17 | Ok, maybe I want to learn more about 2. | D.G |

Table 3. Summary table of coded conversation lines (N = 17), including the frequency of each code and the number of ordered pairs, reading the row first.

[Table 3 content preserved as-is]

## Analysis

In our first example, we note that the learner engaged with the chatbot with a small number of prompts (17 prompts), with the majority of the SRL process at the seeking and engaging phase. In the case of the second learner, there is more engagement with the chatbot at the defining and engaging phases. With this cursory information

Here's the cleaned Markdown:

Future Internet 2024, 16, 218

In the case of the example, we note that this student participates actively in seeking and engaging, but not so much in defining and reflecting. This could be interpreted as either (1) the student is not participating fully in the SRL cycle, (2) the student is not sure how to prompt the chatbot to help regulate these two processes, or (3) the student has experience with the chatbot being unhelpful in facilitating these two processes, thus did not perform these steps. These are possible inferences that should be confirmed with further educational research. On the learner front, this could translate to personalized recommendations for this student to engage in learning actions not present in the student's process–action map.

On a broader scale, with multiple students' process–action maps, comparative studies can be conducted by analyzing the prompts given to the chatbot and the associated learning actions and processes. Educators can identify indicators of effective SRL, such as time management, goal setting, metacognitive awareness, and self-assessment techniques. These insights can be used to evaluate the effectiveness of interventions or support tools to promote SRL for individuals and groups of students. Furthermore, by understanding how groups of learners interact with the chatbot and the learning resources provided by the chatbot, instructors can identify usability issues, content gaps, or mismatches between learner expectations and the chatbot learning environment. Further analysis using process mining techniques can also help instructors and instructional designers identify areas for improvement in learning materials. Understanding the limitations of chatbots, instructors can supplement these materials instead of having students prompt continuously with no satisfactory answer from the chatbot.

On a more advanced level, developers can collaborate with instructors to build their chatbot to provide learners with personalized real-time feedback systems or intelligent tutoring systems. By monitoring learners' actions and progress, process mining techniques can identify moments when learners may benefit from specific interventions, such as reminders, prompts, or suggestions to adopt more effective learning strategies. Process mining can help identify meaningful indicators or metrics for learning analytics. Researchers can also identify key performance indicators or process metrics correlating with successful learning outcomes. These indicators can then be used to measure and monitor learners' progress and evaluate the effectiveness of interventions. Process mining can further provide insights into the most effective learning paths taken by successful learners. Researchers can identify common sequences of actions or activities associated with positive learning outcomes by studying the process–action maps of different students in different performance groups. This knowledge can be used to optimize the sequencing and organization of learning materials, ensuring that learners are guided along efficient and effective learning paths toward their learning goals. Lastly, natural language processing techniques such as inter-annotator agreement algorithms can be used to automate the parsing of the process–action tags.

## Implementation Considerations and Conclusions

This work considers SRL at the individual level and how it could potentially be aggregated to derive knowledge about subject- and standard-specific insights. However, SRL is a wide field with many models focussing on various aspects of learning, each with its merit. Therefore, while this work seeks to address the cognitive, metacognitive, and motivational aspects, in-depth research still needs to be carried out to integrate other important and critical aspects of SRL in the age of rapid GenAI usage. These include integrating behavioral models where the chatbot design would focus on observable behaviors and reinforcement learning; constructivist models, where the focus is on active learning and the construction of knowledge through interaction; and collaborative learning models, where chatbots would focus on facilitating interactions between multiple users or between users and the chatbot as a mediator in group activities [43,44].

An example of how this can be expanded is collaborative learning environments that foster shared understanding among learners augmented by chatbots. Chatbots designed with collaborative learning models can facilitate group discussions, provide feedback,

Here's the cleaned Markdown:

Future Internet 2024, 16, 218

## Collaborative Learning and AI Integration

and promote cooperative problem-solving. This collaborative approach can deepen their understanding of the subject matter through shared perspectives and insights while giving them the extended edge of access to knowledge and information provided by the capabilities of GenAI. Such collaborative learning environments also facilitate and encourage peer teaching and feedback mechanisms within the learning process. Groups of students can also leverage GenAI to synthesize and summarize information from diverse sources. AI algorithms can analyze vast amounts of data and distill key insights, facilitating the creation of shared knowledge bases for complex topics.

In pursuing leveraging advanced technologies like ChatGPT, it is imperative to confront the inherent limitations and ethical considerations associated with their deployment. One of the primary concerns surrounding GenAI is the potential for generating misinformation or the chatbot hallucinating. While the model is designed to provide accurate and contextually relevant information, it may inadvertently produce misleading or inaccurate content. In the context of learning, this could be detrimental, especially in cases where students are unaware of the false information received. Recognizing this limitation and implementing measures to mitigate the risk of disseminating unreliable information is vital. We advocate for integrating a human-in-the-loop approach to address the challenges posed by the potential for misinformation and other limitations. This involves educator oversight and intervention in using ChatGPT, ensuring that the technology is used while lowering the chances of learners receiving misinformation. By incorporating human judgment, we can enhance the reliability of the generated content and minimize the risks associated with automated decision-making.

## User Acceptance and Validation

To bolster the credibility and acceptance of our proposed solution, it is imperative to conduct user acceptance studies. These studies gather feedback and insights from potential end-users, stakeholders, and relevant communities. Understanding user perspectives and preferences will significantly refine our approach, ensuring it aligns with real-world needs and concerns. To ensure that validation is ongoing, we recommend a continuous and iterative approach incorporating feedback from pilot implementations and user studies to refine and adapt the solution over time. By engaging in an iterative validation process, we can adapt to evolving requirements and fine-tune our approach for optimal performance. Validation efforts, including scenario-based applications such as the one presented in our proof-of-concept, play a pivotal role in strengthening the overall credibility of our proposed solution. A robust validation process instills confidence in stakeholders and provides empirical evidence of our approach's practical benefits and effectiveness.

## Conclusion

In conclusion, this exploratory research aimed to investigate and answer three fundamental research questions relating to SRL processes for GenAI chatbots. Firstly, we explored the SRL models that effectively describe the learning processes for these chatbots. Through an in-depth analysis of the chatbot interactions and event logs, we identified a process–action library that provides a comprehensive framework for understanding and explaining the SRL behaviors exhibited by learners engaging with GenAI chatbots. Next, we addressed identifying and classifying SRL processes for prompts used in educational chatbots. We successfully developed a methodology to categorize and classify the SRL processes associated with different prompts by examining the process–action tagging and leveraging process mining techniques. This classification approach provides a deeper understanding of the specific SRL strategies employed by learners and allows for the customization and adaptation of prompts to enhance the SRL experience. Lastly, we explored the potential applications of learning analytics that can be performed to extract valuable insights from the SRL processes observed from interacting with educational chatbots. By employing process mining techniques, we could derive meaningful learning analytics indicators. Leveraging these analytics enables educators and designers to monitor learners' progress, evaluate the effectiveness of interventions, and provide personalized feedback, ultimately fostering enhanced SRL experiences.

This research has shed light on the SRL processes exhibited by learners in their interactions with GenAI chatbots. We have advanced our understanding of effectively supporting

Here's the cleaned Markdown:

Future Internet 2024, 16, 218

and optimizing SRL in an age where educational chatbots are the mainstay. These findings have significant implications for the design of personalized learning environments, the improvement of learning outcomes, and the promotion of learner autonomy and skills. Future research can build upon these findings to further explore the dynamics of SRL in chatbot-assisted learning and refine the methodologies and techniques employed for even more robust and effective self-regulated learning experiences.

## Funding
This research received no external funding.

## Data Availability Statement
The original contributions presented in the study are included in the article. Further inquiries can be directed to the corresponding author.

## Acknowledgments
The author would like to thank the two learners for providing their prompts with ChatGPT.

## Conflicts of Interest
The authors declare no conflicts of interest.

## References
1. Zimmerman, B.J. Investigating Self-Regulation and Motivation: Historical Background, Methodological Developments, and Future Prospects. Am. Educ. Res. J. 2008, 45, 166–183. [CrossRef]
2. Zimmerman, B.J. Self-Regulated Learning: Theories, Measures, and Outcomes. In International Encyclopedia of the Social & Behavioral Sciences, 2nd ed.; Wright, J.D., Ed.; Elsevier: Oxford, UK, 2015; pp. 541–546. [CrossRef]
3. Dunlosky, J.; Ariel, R. Chapter four—Self-Regulated Learning and the Allocation of Study Time. In Advances in Research and Theory; Ross, B.H., Ed.; Academic Press: San Diego, CA, USA, 2011; Volume 54, pp. 103–140. [CrossRef]
4. Flavell, J.H. Metacognition and cognitive monitoring: A new area of cognitive–developmental inquiry. Am. Psychol. 1979, 34, 906–911. [CrossRef]
5. Zimmerman, B.J. Attaining self-regulation: A social cognitive perspective. In Handbook of Self-Regulation; Academic Press: San Diego, CA, USA, 2000; pp. 13–39. [CrossRef]
6. Pintrich, P.R. Chapter 14—The Role of Goal Orientation in Self-Regulated Learning. In Handbook of Self-Regulation; Boekaerts, M., Pintrich, P.R., Zeidner, M., Eds.; Academic Press: San Diego, CA, USA, 2000; pp. 451–502. [CrossRef]
7. Bandura, A. Social Foundations of Thought and Action. In The Health Psychology Reader; SAGE Publications Ltd.: London, UK, 2002; pp. 94–106. [CrossRef]
8. Deci, E.; Ryan, R. Intrinsic Motivation and Self-Determination in Human Behavior; Perspectives in Social Psychology; Springer: New York, NY, USA, 2013.
9. Panadero, E. A Review of Self-regulated Learning: Six Models and Four Directions for Research. Front. Psychol. 2017, 8, 422. [CrossRef] [PubMed]
10. Zimmerman, B.J. A social cognitive view of self-regulated academic learning. J. Educ. Psychol. 1989, 81, 329–339. [CrossRef]
11. Daniela, P. The Relationship Between Self-Regulation, Motivation And Performance At Secondary School Students. Procedia Soc. Behav. Sci. 2015, 191, 2549–2553. [CrossRef]
12. Clemons, M.L.; Hopkins, T. Facilitating Success: Using Self-Regulated Learning and Servant Leadership in the College

## References

22. Chocarro, R.; Cortiñas, M.; Marcos-Matás, G. Teachers' attitudes towards chatbots in education: A technology acceptance model approach considering the effect of social language, bot proactiveness, and users' characteristics. Educ. Stud. 2021, 49, 295–313. [CrossRef]

23. Meng, J.; Dai, Y.N. Emotional Support from AI Chatbots: Should a Supportive Partner Self-Disclose or Not? J. Comput.-Mediat. Commun. 2021, 26, 207–222. [CrossRef]

24. Khiat, H.; Vogel, S. A self-regulated learning management system: Enhancing performance, motivation and reflection in learning. J. Univ. Teach. Learn. Pract. 2022, 19, 43–59. [CrossRef]

25. Fan, Y.; Rakovic, M.; van der Graaf, J.; Lim, L.; Singh, S.; Moore, J.; Molenaar, I.; Bannert, M.; Gašević, D. Towards a fuller picture: Triangulation and integration of the measurement of self-regulated learning based on trace and think aloud data. J. Comput. Assist. Learn. 2023, 39, 1303–1324. [CrossRef]

26. Molenaar, I.; de Mooij, S.; Azevedo, R.; Bannert, M.; Järvelä, S.; Gašević, D. Measuring self-regulated learning and the role of AI: Five years of research using multimodal multichannel data. Comput. Hum. Behav. 2023, 139, 107540. [CrossRef]

27. Wong, J.; Baars, M.; Davis, D.; Zee, T.V.D.; Houben, G.J.; Paas, F. Supporting Self-Regulated Learning in Online Learning Environments and MOOCs: A Systematic Review. Int. J. Hum. Comput. Interact. 2018, 35, 356–373. [CrossRef]

28. Alonso-Mencía, M.E.; Alario-Hoyos, C.; Maldonado-Mahauad, J.; Estévez-Ayres, I.; Pérez-Sanagustín, M.; Kloos, C.D. Self-regulated learning in MOOCs: Lessons learned from a literature review. Educ. Rev. 2019, 72, 319–345. [CrossRef]

29. Jansen, R.S.; van Leeuwen, A.; Janssen, J.; Kester, L. Exploring the link between self-regulated learning and learner behaviour in a massive open online course. J. Comput. Assist. Learn. 2022, 38, 993–1004. [CrossRef]

30. Wei, X.; Saab, N.; Admiraal, W. Do learners share the same perceived learning outcomes in MOOCs? Identifying the role of motivation, perceived learning support, learning engagement, and self-regulated learning strategies. Internet High. Educ. 2023, 56, 100880. [CrossRef]

31. Chiu, T.K.F. A classification tool to foster self-regulated learning with generative artificial intelligence by applying self-determination theory: A case of ChatGPT. Educ. Technol. Res. Dev. 2024. [CrossRef]

32. Kong, S.C.; Yang, Y. A Human-Centered Learning and Teaching Framework Using Generative Artificial Intelligence for Self-Regulated Learning Development Through Domain Knowledge Learning in K–12 Settings. IEEE Trans. Learn.