# Empowering student self-regulated learning and science education through ChatGPT: A pioneering pilot study

Davy Tsz Kit Ng¹, Chee Wei Tan², Jac Ka Lok Leung³

¹Faculty of Education, The University of Hong Kong, Hong Kong SAR, China  
²School of Computer Science and Engineering, Nanyang Technological University, Singapore  
³Division of Integrative Systems and Design, Hong Kong University of Science and Technology, Hong Kong SAR, China

Correspondence: Davy Tsz Kit Ng, Hong Kong University of Science and Technology, Hong Kong SAR, China.  
Email: davyngtk@connect.hku.hk

In recent years, AI technologies have been developed to promote students' self-regulated learning (SRL) and proactive learning in digital learning environments. This paper discusses a comparative study between generative AI-based (SRLbot) and rule-based AI chatbots (Nemobot) in a 3-week science learning experience with 74 Secondary 4 students in Hong Kong. The experimental group used SRLbot to maintain a regular study habit and facilitate their SRL, while the control group utilized rule-based AI chatbots. Results showed that SRLbot effectively enhanced students' science knowledge, behavioural engagement and motivation. Quantile regression analysis indicated that the number of interactions significantly predicted variations in SRL. Students appreciated the personalized recommendations and flexibility of SRLbot, which adjusted responses based on their specific learning and SRL scenarios. The ChatGPT-enhanced instructional design reduced learning anxiety and promoted learning performance, motivation and sustained learning habits. Students' feedback on learning challenges, psychological support and self-regulation behaviours provided insights into their progress and experience with this technology. SRLbot's adaptability and personalized approach distinguished it from rule-based chatbots. The findings offer valuable evidence for AI developers and educators to consider generative AI settings and chatbot design, facilitating greater success in online science learning.

## Introduction

Students' ability to successfully manage their self-regulated learning (SRL) is important for their lifelong learning in today's digital world (Chen & Huang, 2014; Wolters & Taylor, 2012). However, developing young learners' SRL has been a challenging task due to differences in learning styles and motivation, limited access to learning support and the need for feedback (Wong et al., 2019). According to Zimmerman (2002), SRL refers to a process by which learners utilize their mental abilities to transform into academic skills through self-directed goals. To foster students' SRL behaviours, researchers have suggested decomposing learning strategies, such as providing opportunities for student autonomy and choice, encouraging goal-setting and planning, providing feedback and support and creating a positive learning environment.

SRL and motivation are closely related to the learning performance and process (Zimmerman & Schunk, 2011). Motivation serves as the driving force behind learners' engagement and instigates and sustains goal-directed activities, while SRL skills enable learners

### Practitioner notes

#### What is already known about this topic
- AI technologies have been used to support student self-regulated learning (SRL) across subjects.
- SRL has been identified as an important aspect of student learning that can be developed through technological support.
- Generative AI technologies like ChatGPT have shown potential for enhancing student learning by providing personalized guidance and feedback.

#### What this paper adds
- This paper reports on a case study that specifically examines the effectiveness of ChatGPT in promoting SRL among secondary students.
- The study provides evidence that ChatGPT can enhance students' science knowledge, motivation and SRL compared to a rule-based AI chatbot.
- The study offers insights into how ChatGPT can be used as a tool to facilitate SRL and promote sustained learning habits.

#### Implications for practice and/or policy
- The findings of this study suggest that educators should consider the potential of ChatGPT and other generative AI technologies to support student learning and S

Here's the cleaned Markdown:

Self-regulated learning (SRL) enables students to set meaningful goals, monitor progress and adapt strategies (Schunk & DiBenedetto, 2020). Motivation fuels learning, engagement and persistence of SRL behaviours, and SRL enhances learners' sense of control, mastery, autonomy and competence, leading to increased intrinsic motivation (McCombs, 2013; Reeve et al., 2012). In science education, intrinsic motivation and self-regulation may play a dominant role in developing students' scientific knowledge. Prior research examined the link between SRL environment (e.g., teacher support, investigation, cooperation and task orientation) and motivation in science learning (Velayutham & Aldridge, 2013). By considering students' psychological characteristics, teachers can improve classroom practices by creating a favourable environment where students can feel more motivation and work harder to succeed (Cheng & Tsai, 2020; Zimmerman & Schunk, 2011).

To assist students in improving their SRL and motivation, various technological approaches have been explored. Many studies have focused on the use of learning dashboards, enabling students to monitor their SRL behaviours and enhance their SRL skills (e.g., Perez-Alvarez et al., 2022; Roll & Winne, 2015; Winne & Baker, 2013). For instance, Breitwieser et al. (2023) demonstrated the high effectiveness of mobile interventions in supporting SRL among young learners. These interventions involved providing prompts to remind students of instructions and help them plan their SRL, without fostering excessive reliance on the prompts. Similarly, Fan et al. (2021) assessed students' engagement across content access, revision, participation in discussions, completion of assessments, help-seeking behaviour and search activity. These examples showcase the analysis of students' learning processes through artificial agents, addressing their psychological, affective and metacognitive needs using statistical and machine learning techniques, and offering real-time scaffolding for problem-solving and performance (Roll & Winne, 2015; Winne & Baker, 2013). Such support can assist young learners in developing self-regulation and maintaining a positive online learning experience, particularly during the COVID-19 pandemic and in self-paced learning environments (Ng, 2022).

ChatGPT has gained significant global attention and has shown promise in supporting students' learning (Kasneci et al., 2023; Kohnke et al., 2023; Tlili et al., 2023). Recent studies suggest that students are more optimistic about the potential of generative AI technologies to improve their academic performance and develop effective learning strategies (e.g., Afzaal et al., 2021; Hsu et al., 2023; Wang & Lin, 2023). AI is the simulation of human intelligence processes by machines, and there are various applications or subfields that fall under the umbrella of AI, such as machine learning and data mining (Alam, 2021; Chen et al., 2020; Ng et al., 2021). Generative AI is a type of AI that is designed to generate new content (e.g., text, images and media) (Peres et al., 2023). Unlike rule-based AI systems that follow predefined instructions or rules, generative AI models learn from large datasets and use that knowledge to create new content that is similar to the training data (Caruccio et al., 2024).

In the age of AI, it is important for students to be equipped with adequate capabilities such as understanding what AI is, how it functions, its limitations and how to improve results and suggestions from generative AI (Chiu et al., 2021; Ng, Leung, et al., 2023; Ng et al., 2021; Xia et al., 2023). To obtain desired responses, a concept known as 'prompt engineering' has emerged. This term refers to the process of designing and developing effective prom

## ChatGPT vs. Rule-Based AI

## Introduction

In employing SRL strategies (Devolder et al., 2012). ChatGPT can act as virtual teachers to have both types of SRL interventions, providing direct instruction, while also offering prompts and feedback to assist students in developing their SRL strategies. However, there is a scarcity of studies exploring the potential of (generative) AI chatbots in providing prompts to foster students' SRL development. It remains unclear whether these generative AI technologies can effectively serve as virtual teachers and enhance students' SRL.

To fill this research gap, we developed a ChatGPT-enhanced bot called SRLbot to enhance SRL among Secondary 4 students. This study emphasizes the significance of supporting SRL in secondary school students and explores the potential of effective ChatGPT-enhanced interventions for younger learners. Specifically, we focus on facilitating students' adoption of effective SRL strategies and discuss the utilization of prompt engineering guidelines to stimulate their SRL and science learning. We also address important considerations regarding the implementation of AI to enhance students' SRL, such as frequency of use, AI literacy and challenges. Finally, we present qualitative feedback from students, which complements the quantitative findings and informs the development of successful ChatGPT-enhanced interventions for younger learners.

### Research Questions

Quantitative phase:
- RQ1. To what extent does the use of the SRLbot have an impact on students' SRL, motivation and science knowledge?
- RQ2. Are there any significant differences between the SRLbot and Nemobot platform that influence students' SRL, motivation and science knowledge?
- RQ3. What are the effects of gender and students' interaction on students' SRL?

Qualitative phase:
- RQ4. What are students' perceptions of SRLbot experiences in developing SRL?

## Literature Review

### Self-regulated Learning

SRL involves students' intentional and proactive management of their learning process to achieve specific goals (Pintrich, 2004; Zimmerman & Schunk, 2011). A supportive learning environment is important to encourage and promote students' SRL to fulfil their learning needs (Chiu et al., 2022; Xia et al., 2023). When students' needs are met, they tend to be more motivated and autonomously self-regulate their learning effectively (Littlejohn et al., 2016). With positive learning support, students can exhibit greater enthusiasm, become more attentive and demonstrate their self-regulation (Deci & Ryan, 2004). The fulfilment of the need for autonomy has positive consequences for students' abilities to regulate their independent learning (Jin et al., 2023; Wang & Eccles, 2013).

Self-regulated learners have a mastery goal orientation, which means they seek to develop competencies by mastering skills or tasks, are confident in their learning ability and highly value the learning tasks (Zimmerman & Schunk, 2011). According to Molenaar et al. (2022)'s review, self-regulated learners show three characteristics which include:
1. Cognitive competencies (eg, elaborating and summarizing a topic)
2. Metacognitive competencies (eg, orientation, goal setting, planning, monitoring and evaluation), to actively monitor their learning
3. Regulate their affective states (eg, reducing confusion and frustration and increasing task value and interest) to sustain an appropriate level of learning

Other studies also supported these three dimensions of SRL. Kim et al. (2014) found that students' affects (eg, anxiety, boredom) and motivational beliefs are positively associated with their self-regulation for interaction in online learning environments. Similarly, Cho and Heron (2015) found that online students' intrinsic goal orientation and emotion are positively related to their SRL strategies in a self-paced online course. These studies have highlighted the important dimensions of SRL for this study to design an appropriate toolkit that guides students to enhance

## ChatGPT vs. Rule-Based AI

Chatbots relied heavily on rule-based systems supported by natural language processing (NLP), which follow predefined scripts and patterns based on keyword matching (van der Waa et al., 2021). These systems focused on skills demonstration and problem solving (Wu & Yu, 2024).

In the present study, although students in both groups complete the same science evaluation tasks about force and motion using chatbots, examining students' SRL activities requires more than tracking students' data logs and prompting rule-based conversations. 

Since 2022, the emergence of ChatGPT by OpenAI has captured substantial global attention and demonstrated its potential to support students' learning. Unlike rule-based chatbots, ChatGPT utilizes advanced language models and generative AI techniques, enabling more human-like conversations with users. This breakthrough has opened up new possibilities for leveraging chatbots in educational settings to enhance students' learning experiences (Kasneci et al., 2023; Kohnke et al., 2023; Tlili et al., 2023). It leverages large-scale datasets and deep learning techniques to understand the context of conversations and generate more contextually appropriate responses. Compared to rule-based chatbots, ChatGPT can handle more complex and nuanced conversations. It can generate responses that are more flexible and adaptable to different scenarios. The utilization of ChatGPT in learning technologies, particularly in chatbot design, enables the integration of intelligence, real-time SRL support and personalized feedback within the home environment. This advancement highlights the need for further efforts in leveraging SRL theory to guide students' inquiries and facilitate learners' progress, aided by AI support. By combining SRL principles with generative AI, there is potential to create more effective SRL experiences for students. This can be achieved by addressing the need for automatic scoring and human-like conversations.

## Chatbots for Science Learning

Chatbots have emerged as technology applications that greatly enhance interpersonal communication and learning. They offer interactive methods and user-friendly interfaces to provide diverse information and knowledge, serving as tools for individual consultations (Chang et al., 2022). Chatbots have gained popularity, particularly in providing personalized support to learners. Although research on effective chatbot design for supporting students' SRL and science learning is limited, some studies explored the use of chatbots in science education. Salvagno et al. (2023) designed a chatbot with a responsive teaching function to promote explicit reasoning and writing, and positive attitudes towards science. Deveci Topal et al. (2021) developed an intelligent chatbot to support fifth-grade students in learning about matter and changing states, while Durall and Kapros (2020) designed a self-assessment chatbot to foster secondary students' science learning and self-regulation. These studies demonstrated the potential of chatbots in providing immediate feedback, recommendations, explanations and examples, thereby improving students' conceptual development in subjects.

Previous research has emphasized the importance of SRL in science education, suggesting the need for domain-specific and complementary scaffolding (Alpaslan et al., 2016). With the support of ChatGPT, chatbots can become more adaptive and powerful. Cooper (2023) has discussed the potential of ChatGPT-enhanced chatbots in enhancing students' science learning. First, ChatGPT can respond to teachers' and students' questions related to science education. Second, it explores the ways in which educators can incorporate ChatGPT into their science pedagogy. Third, it reflects on the use of ChatGPT as a research tool for science learning. Although it seems that ChatGPT has shown its potential to enhance students' learning and address scientific misconceptions, there are challenges when using novice technologies. Dao and Le (2023) found that ChatGPT struggled to accurately answer questions on advanced or newly discovered science topics for high school and university students.

Here's the cleaned Markdown:

## Methods

A total of 74 Secondary 4 students at a secondary school in Hong Kong were invited to attend 10-lesson blended learning activities to learn science concepts 'force and motion'. This study employed a quasi-experimental approach, with 36 students in both classes. The experimental group involved students using SRLbot, while the control group involved students using a rule-based AI system. After lessons, both groups were engaged in the chatbot learning activities. Students were encouraged to continue their science learning at home using the chatbots. A teacher with over 7 years of teaching experience taught for both groups and was familiar with the chatbots. A set of guiding materials was given to students on how to use the chatbots to learn science, and how to enhance their SRL at home. Both groups of students were expected to learn how to solve force and motion questions using displacement, velocity, acceleration, friction, mass and weight. An SRL and motivation questionnaire with 5-point Likert scale and a science knowledge test were administered before and after the intervention. To triangulate the quantitative findings, follow-up interviews were conducted to understand how students perceive the chatbot learning experience. The research design is illustrated in Figure 1.

In the experimental group, 22 (59.5%) of the students were male and 15 (40.5%) were female. They use SRLbot to learn science. A set of guiding questions was developed to help students plan ahead their learning using SRL strategies (eg, What type of science problems are you currently working on?, Have you encountered problems similar to the ones you are working on before? and What are your goals for solving the problems?). When students face difficulties while learning at home (eg, lack of motivation, science misconceptions and challenges in the science tasks), they could seek advice from the SRLbot. In the control group, 37 students (19 male and 18 female) participated in 10 blended learning lessons using a chatbot called Nemobot. Nemobot is a bot-building platform for developing AI conversational chatbots and is an effective service to support learning (Li et al., 2021; Tan, 2022, 2023). However, the SRL instruction and scaffolding support (eg, flashcards, hints and e-quizzes) are not provided in Nemobot. When students encounter difficulties with their questions, students could raise in their learning management system. After the lessons, both groups were required to complete exercises in their textbook.

## Instructional Design and Procedures

In the experimental group, students used SRLbot which was built by us in a mobile app platform called POE. With POE, the research team worked with the teacher to design an AI chatbot to support students in developing SRL strategies in science learning contexts at

## CHATGPT VS. RULE-BASED AI

SRLbot was developed based on the ChatGPT-3 language model with the following steps. First, we opened a bot page and customized the bot's appearance (Figure 2). Second, we defined the bot's behaviour using an AI-powered language model. Third, we created a prompt for SRLbot, which included instructions for how it should respond to students' questions and provide recommendations to enhance SRL.

When students encountered difficulties in the process, they typed their questions in the SRLbot. Some recommendations with science-related examples and explanations were suggested (Figure 3, left). Moreover, the chatbot can provide recommendations on enhancing students' SRL. It helped students manage their learning processes via questioning. By doing so, chatbots helped students set goals, suggest ways to improve environmental structuring, recommend some learning strategies and promote time management skills (Figure 3, right).

Different from the experimental group, students in the control group used rule-based chatbot using a social network platform called Facebook Messenger. The platform can be integrated with Nemobot to set up automated and preprogrammed responses for students to continue with their science learning at home (Tan, 2022). However, the chatbot is not as flexible and adaptive as SRLbot since questions. Recommendations needed to be preassigned in the system and tailored to specific use cases and students' responses. If students' responses are unexpected, it would ignore those responses. The chatbot mainly facilitated teachers to provide science learning support (Figure 4, left) and some SRL recommendations (Figure 4, right). The chatbot would ask students some questions, and students answered them by typing or clicking buttons. The chatbot would provide feedback based on students' responses and teachers' preassigned materials.

Before their class, both groups were also given instruction to inform students about the SRL and science learning goals, and how to operate their chatbots (eg, learn how to prompt). Such instructions are important for students to familiarize themselves with their chatbots. There are several occasions to consider when the SRLbot may produce inaccurate results or unsuitable recommendations, such as mixing different topics in a single chat session; inputting non-specific goals and resulting in generic answers; and asking too many questions in one prompt (Young & Shishido, 2023). Students were advised to first familiarize the chatbots under teachers' support.

On the other hand, previous research has demonstrated that students experience positive engagement when using Nemobot in various subject areas, including science, programming, mathematics and language learning (Ling & Tan, 2018). Additionally, studies have highlighted the thoroughness of Nemobot's state machine design (Tan, 2023). Another study showed that Nemobot effectively provided students with a positive learning experience across different pedagogical approaches (eg, flipped classroom and gamification) (Tan, 2022). These papers help justify the usefulness and effectiveness of using Nemobot for learning purposes.

### SRL setting

The study was conducted in an SRL setting, in which students were guided to develop their SRL strategies via interacting with chatbots. At the beginning of the science lessons,

[Figures 1-4 referenced in text but not included in excerpt]

Here's the cleaned Markdown:

## ChatGPT vs. Rule-Based AI

The teacher informed students about the learning goals, contents and assignment, which involved completing questions from the textbook with explanations and answers. Around 15 questions on force and motion were assigned at the end of the class, and students worked in pairs to complete them with the help of a chatbot. The chatbot suggested SRL processes to help students complete their tasks. Specifically, the students asked their chatbots for advice on goal setting, environmental structuring, task strategies, time management and help seeking.

The main difference between them was the use of chatbot technologies. The experimental group used SRLbot to seek advice for SRL strategies, which provided flexible, adaptive and open-ended responses. Appendix 1 displays an example of a dialogue between SRLbot and a student. The control group used Nemobot with the support of teachers' instruction to learn SRL. The SRL recommendations and conversations were preassigned by Nemobot. To reduce potential treatment diffusion between experimental and control groups, both groups were taught by the same teacher using identical learning materials. Students continued their learning at home using different AI chatbots. The control group students used SRLbot, whereas students in the experimental group adopted Nemobot. This enabled us to examine whether rule-based or generative AI-assisted chatbot design can better support students in sustaining their SRL and motivation. The instructional design for SRLbot and Nemobot was aligned with the self-regulation theory adapted from Zimmerman's (2002) three-cycle model and Hsu et al.'s (2023) SRL process (Figure 5).

## Instruments and data analysis

### Data collection

This study used a pre- and post-test adapted from the Online SRL Questionnaire to measure students' self-regulation and motivation. This questionnaire, which is widely used in secondary schools, was developed based on 14 self-regulation theories proposed by Zimmerman and Schunk (2011). These theories comprise three important stages: planning, action and reflection, as shown in Figure 5.

The questionnaire contains 24 items across six dimensions of SRL: goal setting, environmental structuring, task strategies, time management, help seeking and self-evaluation (Lau, 2022). To examine students' learning motivation, four items were added to the questionnaire which was adapted from the revised Chinese version of Motivated Strategies for Learning Questionnaire (Lee et al., 2010; Ng & Chu, 2021). The wording of items was adapted to be context specific; for example, 'I like what I am learning in school' was changed to 'I like what I am learning in the science learning tasks.' Students were asked to answer 10 multiple-choice questions to test their science knowledge learnt in their learning tasks (ie, force and motion). To examine students' AI literacy development, five items were introduced. The questionnaire assessed their perceived knowledge of generative AI and/or ChatGPT.

Here's the cleaned Markdown:

## ChatGPT vs. Rule-Based AI

## Data Analysis

To address RQ1, the improvement in students' levels of SRL, motivation and science knowledge was assessed by comparing pre- and post-test scores using a Wilcoxon signed-rank test. For RQ2, the post-test results of students using the SRLbot and Nemobot platforms were compared using non-parametric Mann-Whitney U tests. To explore the potential influence of students' interaction on SRL, as opposed to gender, quantile regression analysis was conducted to examine the partial effects of number of interactions and gender changes across the distribution of SRL in RQ3.

## Follow-up Interviews

To triangulate the quantitative findings, 12 students (six from experimental and six from control groups) and the teacher were invited to have a follow-up semi-structured interview for around 20 minutes. Examples of how students used chatbots to support their SRL and science learning in both groups were gathered. The collected data, including interview dialogues and chatbot conversations, were presented to address RQ4, focusing on SRL and the benefits and limitations of using SRLbot. A descriptive analysis was conducted to complement students' perceptions of AI literacy. To further analyse the data, the Monkeylearn software was deployed, which is specifically designed for qualitative sentiment analysis. The software used textual analysis models to automatically tag the data, including sentiment and identify key ideas (Sadriu et al., 2021). Based on the students' interview feedback, the key themes were identified and categorized according to SRL and motivation, as shown in Appendix 1.

## Results

### RQ1. To what extent does the use of the ChatGPT have an impact on students' SRL, motivation and science knowledge?

As shown in Table 1, the pre- and post-test scores were compared to assess the improvement of students' levels of SRL, motivation and science knowledge. Since the data were not normally distributed (p < 0.05 in Kolmogorov-Smirnov test), the Wilcoxon signed-rank test, a non-parametric test, was used.

Regarding SRL, there was a significant improvement in scores for goal setting, environmental structuring, task strategies, time management, help seeking and self-evaluation (p ≤ 0.01). There was also a slight improvement in science motivation and knowledge about force and motion (p ≤ 0.05).

| Constructs | N | Pre-test |  | Post-test |  | Wilcoxon signed-rank test |  |  |  |
|------------|---|----------|-----|-----------|-----|-------------------------|-----|------------|----------|
| | | M | SD | M | SD | Mean rank | Z | Effect size R | p-Value |
| Goal setting | 37 | 2.97 | 0.88 | 3.73 | 0.78 | 21.0 | 3.26 | 0.54 | 0.00** |
| Environmental structuring | 37 | 2.21 | 0.95 | 4.12 | 0.73 | 17.1 | 3.86 | 0.63 | 0.00** |
| Task strategies | 37 | 2.91 | 1.11 | 3.80 | 1.03 | 20.0 | 2.78 | 0.46 | 0.01** |
| Time management | 37 | 2.83 | 1.00 | 3.70 | 1.05 | 21.3 | 2.73 | 0.45 | 0.01** |
| Help seeking | 37 | 2.76 | 0.95 | 3.48 | 0.97 |

## CHATGPT VS. RULE-BASED AI

and 0.50 quantiles, whereas motivation did not have any significant difference. Overall, the findings suggest that SRL factors may play a significant role in science learning outcomes.

### RQ3. What are the effects of gender and students' interaction on students' SRL?

As suggested by Buchner and Kerres (2023), gender and students' interaction could have the potential to determine students' science learning regarding media comparison. The number of dialogues in the chatbots, and forum contributions are commonly used indicators of student interaction (Domínguez et al., 2013). This study found that the gender effect is not significant in this study on SRL. However, there is a significant correlation between students' interaction (ie, number of interactions) and SRL.

To examine the effects of students' interaction and their individual differences (ie, gender) towards SRL, another round of quantile regression was conducted. SRL was regressed on gender and number of interactions at five quantiles: 0.10, 0.25, 0.50, 0.75 and 0.90. The slope estimates for the predictors in Table 3 indicate a clear pattern: when using SRLbot, students' interactions have a stronger predictive ability for SRL across all quantiles, while gender does not show any significant differences. This suggests that frequent users of generative AI, such as SRLbot, may have more experience generating prompts and possess a higher awareness of AI when seeking SRL recommendations. However, when using Nemobot, neither gender nor the number of interactions demonstrates a significant influence on SRL at the 0.10, 0.75 and 0.90 quantiles. This suggests that the effect of using Nemobot is not dependent on the number of interactions, as students may not develop stronger AI capabilities when merely having conversations with Nemobot, according to the teacher's comment.

| Constructs | Groups | N | Mean rank | U | Z | Effect size R | p-Value |
|------------|---------|---|------------|---|---|--------------|----------|
| Goal setting | SRLbot | 37 | 44.5 | 424.0 | 2.82 | 0.46 | 0.01** |
| | Nemobot | 37 | 30.5 | | | | |
| Environmental structuring | SRLbot | 37 | 45.7 | 379.5 | 3.30 | 0.54 | 0.00** |
| | Nemobot | 37 | 29.3 | | | | |
| Task strategies | SRLbot | 37 | 42.8 | 488.5 | 2.12 | 0.35 | 0.03* |
| | Nemobot | 37 | 32.2 | | | | |
| Time management | SRLbot | 37 | 43.5 | 464.0 | 2.39 | 0.39 | 0.02* |
| | Nemobot | 37 | 31.5 | | | | |
| Help seeking | SRLbot | 37 | 43.7 | 456.5 | 2.47 | 0.41 | 0.01** |
| | Nemobot | 37 | 31.3 | | | | |
| Self-evaluation | SRLbot | 37 | 44.0 | 442.5 | 2.62 | 0.43 | 0.01** |
| | Nemobot | 37 | 31.0 | | | | |
| Science motivation | SRLbot | 37 | 42.8 | 490.0 | 2.11 |

## ChatGPT vs. Rule-Based AI

To investigate students' SRLbot experiences, six students, divided into lower (n = 3) and higher science knowledge (n = 3) groups, participated in follow-up interviews to examine their interactions with SRLbot and their reflections on their SRL processes. Another six students (three with lower and three with higher science knowledge) from the Nemobot group were invited to provide their feedback on the limitations of the rule-based AI design, particularly in comparison to SRLbot. In each group, students had the opportunity to use the chatbot from the other group, enabling them to compare the learning experience of both chatbots. Their feedback could provide valuable insights into the effectiveness of using SRLbot or other (generative) AI chatbots in supporting their SRL experiences. To analyse students' responses, this section presented (1) students' SRL strategies and (2) the benefits and limitations of using SRLbot over Nemobot.

### Self-regulated Learning

Students in the experimental group expressed positive perceptions towards SRLbot and its role in supporting their SRL journey. The sentiment analysis conducted by Monkeylearn on students' responses provided support for the findings. In the SRLbot group, the sentiment ranged from 55.6% to 99.1% positive, indicating a positive sentiment. On the other hand, students who used Nemobot expressed a sentiment of 40.5% to 54.0% negative towards their chatbot. The responses were coded according to the various SRL strategies, including goal setting, environmental structuring, task strategies, time management, help seeking and self-evaluation.

A student suggested, 'SRLbot is highly beneficial for setting and achieving learning goals. The personalized suggestions and reminders provided by the chatbot serve as a virtual teacher, helping students stay motivated and organized'. Another student also appreciated the goal-setting advice received from the chatbot. 'SRLbot helps me set clear goals, create schedules and routines, and enable me to organize my study materials'. A student highlighted the value of environmental structuring facilitated by SRLbot. 'The chatbot guides me on eliminating distractions and managing my digital learning environment, which creates an effective online learning atmosphere'. When asked about the strategies recommended by the chatbot, a student mentioned, 'Organizing their study space, developing a note-taking system, and participating in discussions with me'. Students followed the chatbot's advice by organizing their study area to avoid distractions and staying away from games. As a result, they experienced improved concentration and sustained their science learning at home.

Students also recognized task strategies introduced by SRLbot. For example, a student commented, 'The chatbot guides me on effective note-taking techniques and recommended useful online collaboration tools'. This exposure to new strategies enhanced students' confidence in approaching learning challenges. Time management was another aspect where students found SRLbot to be beneficial. 'The chatbot encourages me to create study schedules and allocate dedicated time slots for different activities'. Such guidance helped students prioritize tasks, avoid procrastination and make better use of their time. Help-seeking support provided by SRLbot was also appreciated by students. For instance, students asked their bot to provide training questions on topics like displacement, acceleration and velocity. The chatbot effectively provided numerous examples and explanations, enabling students to practice and evaluate their understanding. One student mentioned, 'When I encounter difficulty, I immediately ask my bot. I type the question from my textbook and it provides clear steps and explanations'.

Students who used Nemobot also provided feedback regarding their experience with the chatbot. A student mentioned, 'Nemobot is a useful tool for practicing my force and motion

knowledge. However, it may not be effective in providing SRL recommendations. Its responses are too fixed and close-ended'. Another student echoed this sentiment by stating, 'I agree. It makes goal setting more engaging, but it lacks the ability to provide personalized feedback'.

## Benefit of using SRLbot for SRL

During the follow-up interviews, students with higher science knowledge expressed various benefits of using SRLbot to enhance their SRL strategies. First, SRLbot provides personalized support and helps students develop effective SRL strategies that are tailored to students' learning needs and styles. A student commented, 'SRLbot provided feedback like a real teacher, and can support him with any science problems they encounter'. Students appreciated that the SRLbot responded promptly to their queries when they encountered challenging problems. One student mentioned, 'GPT can help provide answers faster according to their responses, compared to conventional rule-based AI'. Another student said, 'Nemobot could only provide preassigned and fixed responses based on students' interactions. This restricts us from interacting freely with the chatbot'. A student supported this idea and commented, 'Rule-based AI does not exhibit natural reactions, and is less flexible to adapt to students' inputs'. In contrast, SRLbot, driven by a large language model, has the potential to emulate a real teacher, guiding and sustaining students' science learning at home.

Additionally, SRLbot is interactive and enhances students' motivation and organization by offering virtual teacher-like responses. SRLbot also provides students with SRL learning strategies and techniques, on top of teachers' SRL instruction and guidelines. Through interactive conversations, the chatbot introduces students to innovative approaches such as effective time management, note taking and online collaboration. This enables additional strategies that expand students' SRL techniques, maintain their motivation when handling learning challenges and equip them with a broader set of generative AI competencies. To sum up, SRLbot serves as a valuable tool in providing personalized guidance, enhancing motivation and developing students' SRL learning strategies in their online science learning journey.

## Limitations of using SRLbot for SRL

Students with lower science knowledge expressed initial interest in interacting with SRLbot. However, over time, their interest lowered as they found the feedback provided by the chatbot to be boring and not aligned with their science learning goals. When they asked the chatbot to help set goals, they often received lengthy statements that did not address their specific science knowledge needs. This lack of specificity made it challenging for these students to effectively utilize the chatbot's ability to suggest SRL strategies related to force and motion, which was their primary concern.

Despite the limitations, these students recognized the value of SRLbot in addressing their misconceptions and filling gaps in their scientific knowledge. They found it beneficial to ask the chatbot questions when they encountered difficulties. Students also noted other limitations in the chatbot's responses. They observed that to receive accurate and relevant answers, they needed to ask proper questions, providing details such as their grade level, the specific topic of interest (eg, force and motion) and the context of their learning (eg, Newton's laws and specific and measurable goals). For example, students needed to prompt 'specific and measurable goals for secondary students in science lessons', instead

## ChatGPT vs. Rule-Based AI

Without these accurate details, the chatbot tended to respond with information on other concepts and situations, such as acceleration and velocity. The insights from students shed light on both the benefits and limitations of SRLbot in supporting their SRL learning in science contexts. Additionally, it suggests areas for improvement that future research can explore, such as incorporating SRLbot with other platforms (e.g., Facebook Messenger), which enables students to use emojis and multimedia. It is worth noting that the current version of POE does not include any multimedia elements. Also, SRLbot is passive in nature and lacks the ability to automatically prompt responses and reminders like some other platforms.

Table 5 summarizes the benefits and limitations mentioned in this section.

| Benefits | Limitations |
|----------|-------------|
| SRLbot provides personalized guidance and recommendations for developing effective SRL strategies tailored to students' needs and learning styles | Students may initially feel interested in SRLbot, but lose interest due to mismatched feedback and responses |
| SRLbot supports students with science problems and promptly provides solutions to their queries | SRLbot addresses misconceptions and fills knowledge gaps, but it needs students' accurate details in their prompts |
| SRLbot gives quick and accurate answers from the chatbot and enhances their SRL strategies | SRLbot is passive and lacks autonomic response and reminder features. Integration with other platforms like Facebook Messenger can enhance user experience with emojis and multimedia |
| | SRLbot is too flexible and has uncontrollable recommendations. Teachers cannot monitor students' interaction with it |

## Discussion

### Potential of SRLbot for SRL and Science Learning

According to RQ1, this study provides evidence that SRLbot can significantly enhance students' SRL in science learning. First, SRLbot provides personalized support to students by answering their questions/prompts, recommending learning resources and offering guidance and hints for students' learning. It provides step-by-step solutions to students' problems and answers their questions to scaffold science understanding. Second, it helps provide students' instant feedback, and suggests areas for improvement. It offers some practical problems and quizzes to help students reinforce their abilities and identify areas where they need additional support.

RQ2 suggests the significant difference of science learning could be subject more to SRL factors, instead of motivation. Furthermore, the experimental group had a better performance in developing SRL strategies compared with the control group which used Nemobot. This may be because rule-based AI (e.g., Nemobot) could only provide students fixed responses regarding SRL recommendations, as its responses are preassigned by teachers and are often close ended and predictable. In contrast, SRLbot can encourage students to engage in metacognitive reflection by prompting them to reflect on their learning strategies and processes, much like a real teacher would. SRLbot can effectively provide information on task strategies, guidance on goal-setting and planning and support students in reflecting on their progress.

In RQ3, quantile regression analysis indicates that the number of interactions by students has higher slope estimates compared to gender when using SRLbot. Additionally, the effects of students' interactions on their SRL are significant across all quantiles when utilizing AI chatbots, which aligns with previous studies (Lin & Chang, 2023; Xia et al., 2023). Maldonado-Mahauad et al. (2022) have suggested a possible explanation for this, stating that increased interaction with generative AI chatbots makes it easier to ascertain their impact on SRL. Moreover, ChatGPT-enhanced chatbots, as opposed to rule-based AI, are more conducive to bidirectional communication, thus supporting students' active learning (Chang et al., 2023; Lin & Chang, 2023).

SRLbot has great potential for learning, where students can give their chatbot a prompt, and it provides a well-informed response. Researchers believed that educators should leverage AI to their advantage and looked forward to working with educators on useful solutions (Lo

## ChatGPT vs. Rule-Based AI

Teachers need to update their AI competencies to design instruction for effective teaching and learning and provide personalized learning experiences for students. Teachers need to carefully consider the learning context and objectives before choosing a chatbot for their students. Moreover, it is crucial for teachers to possess AI competencies that enable them to preassign instructions for the chatbots, evaluate different AI applications (generative AI vs. rule-based AI) and understand how to effectively incorporate AI into their classroom. Teachers also need to be aware of the limitations associated with AI, make decisions about its implementation and understand the strengths and limitations of AI tools.

Not only do teachers need AI competencies but students also need to know and understand the digital affordances and limitations behind chatbots. Through interacting with AI chatbots, students can use them in a proper and responsible way, and avoid relying too heavily on them. As students reported that some recommendations may not be helpful in RQ3, additional prompts are needed to refine their responses to get desired responses. Throughout this process, when students interact with chatbots, they can develop a range of AI literacy skills such as understanding how chatbots work, how to use them effectively and the limitations of chatbots (Jeon, 2021; Tan, 2023). They can also learn how to formulate effective questions/prompts, interpret responses and use chatbots to support their learning. In today's world, AI literacy has become increasingly important, and incorporating AI tools like chatbots into education can help students develop their learning skills (Chiu et al., 2021; Tan, 2023).

## Conclusion and Limitations

In conclusion, this study has demonstrated that ChatGPT-enhanced bot is not only useful for supporting science learning but also for enhancing students' SRL. This study has shown that SRLbot, in particular, is effective in promoting SRL due to its adaptability and flexibility in providing personalized feedback and guidance to students. By leveraging the power of generative AI, chatbots can help students develop their self-regulation skills, such as planning, acting and reflecting, which are essential for success in science and other academic domains. However, at the same time, teachers also need to be aware of the limitations of different AI tools.

SRL is a complex and multifaceted process that involves multiple cognitive, metacognitive and affective strategies used by learners to manage their own learning (Hsu et al., 2023; Wong et al., 2019; Zimmerman, 2002). It is a dynamic process that requires learners to continuously monitor and regulate their learning activities, set goals, plan strategies and evaluate their progress towards achieving those goals. When a chatbot provides fixed (rule-based AI) or too general advice (ChatGPT-enhanced AI), it may not effectively stimulate students' learning. Both fixed or over-generalized advice does not take into account the individual differences and needs of learners to effectively regulate their learning.

This study makes a valuable contribution to the current AI education field by comparing generative AI and rule-based AI chatbots for enhancing students' SRL and science learning. By incorporating chatbot technologies into blended learning practices, this study adapted a plan-act-reflect SRL cycle to empower students to become more self-directed and independent learners, helping them achieve their full potential. The study also discusses the benefits and limitations of using chatbots for educational purposes, providing useful insights for future research and practice.

While this study provides insights into the use of chatbots to support SRL, there are limitations that need to be addressed in future research. First, the sample size in this study was small, and further research could involve larger samples to enhance the generalizability of the findings. Second, given its existing research scope, this study did not examine what factors, such as students' prior SRL knowledge and experience, learning strategy and their

Here's the cleaned Markdown:

## Limitations and Future Research

other individual differences, may have contributed to the differences in science learning and SRL. Due to the current research scope, future research is needed to address this limitation and provide further analytical directions. More participants could be invited to focus group interviews to generate more information and foster greater interactivity. This can help provide insights into educational technology design and development (eg, 'when' and 'how' generative AI works). Finally, while this study primarily focuses on aspects of SRL, AI literacy and motivation, future research should explore other dimensions of learning that incorporate a more holistic understanding of AI to support the findings.

## Acknowledgement

This project is supported by the EdeX Grant (No. 03INS001595C130) from the Centre for Teaching, Learning and Pedagogy, NTU.

## Conflict of Interest Statement

The authors have no conflicts of interest to disclose. The manuscript has not been published previously and is not being simultaneously submitted elsewhere. There are no real or potential conflicts of interest that could be seen as having an influence on the research. No reproduction of copyrighted material is evident in this manuscript, hence there is no need to apply for any necessary permission.

## Data Availability Statement

Data are available on request from the authors.

## Ethics Statement

Ethical approval for this study was granted by the University. All procedures performed in studies involving human participants were in accordance with the ethical standards of the institutional and/or national research committee and with the 1964 Helsinki declaration and its later amendments or comparable ethical standards. The research has gained approval from institutional ethics committee. Informed consent was obtained from all individual participants included in the study.

## ORCID

Davy Tsz Kit Ng  
https://orcid.org/0000-0002-2380-7814

Chee Wei Tan  
https://orcid.org/0000-0002-6624-9752

## References

Afzaal, M., Nouri, J., Zia, A., Papapetrou, P., Fors, U., Wu, Y., & Weegar, R. (2021). Explainable AI for data-driven feedback and intelligent action recommendations to support students self-regulation. Frontiers in Artificial Intelligence, 4, 723447.

[Additional references omitted for brevity but would continue in same format]

Here is the cleaned Markdown reference list:

Jeon, J. (2021). Exploring AI chatbot affordances in the EFL classroom: Young learners' experiences and perspectives. Computer Assisted Language Learning, 1–26.

Jin, S. H., Im, K., Yoo, M., Roll, I., & Seo, K. (2023). Supporting students' self-regulated learning in online learning using artificial intelligence applications. International Journal of Educational Technology in Higher Education, 20, 32.

Kasneci, E., Seßler, K., Küchemann, S., Bannert, M., Dementieva, D., Fischer, F., Gasser, U., Groh, G., Günnemann, S., Hüllermeier, E., Krusche, S., Kutyniok, G., Michaeli, T., Nerdel, C., Pfeffer, J., Poquet, O., Sailer, M., Schmidt, A., Seidel, T., … Kasneci, G. (2023). ChatGPT for good? On opportunities and challenges of large language models for education. Learning and Individual Differences, 103, 102274.

Kim, C., Park, S. W., & Cozart, J. (2014). Affective and motivational factors of learning in online mathematics courses. British Journal of Educational Technology, 45(1), 171–185.

Kohnke, L., Moorhouse, B. L., & Zou, D. (2023). ChatGPT for language teaching and learning. RELC Journal, 54, 537–550. https://doi.org/10.1177/00336882231162868

Lau, K. L. (2022). Adaptation and validation of a Chinese online self-regulated learning questionnaire. Journal of Psychoeducational Assessment, 40(3), 438–444.

Lee, J. C. K., Yin, H., & Zhang, Z. (2010). Adaptation and analysis of motivated strategies for learning questionnaire in the Chinese setting. International Journal of Testing, 10(2), 149–165.

Li, J., Ling, L., & Tan, C.-W. (2021, June). Blending peer instruction with just-in-time teaching: Jointly optimal task scheduling with feedback for classroom flipping. In Proceedings of the Eighth ACM Conference on Learning@ Scale (pp. 117–126). ACM.

Lin, M. P. C., & Chang, D. (2023). CHAT-ACTS: A pedagogical framework for personalized chatbot to enhance active learning and self-regulated learning. Computers and Education: Artificial Intelligence, 5, 100167.

Ling, L., & Tan, C. W. (2018, June). Pilot study on optimal task scheduling in learning. In Proceedings of the Fifth Annual ACM Conference on Learning at Scale (pp. 1–4). ACM. https://dl.acm.org/doi/abs/10.1145/3231644.3231677

Littlejohn, A., Hood, N., Milligan, C., & Mustain, P. (2016). Learning in MOOCs: Motivations and self-regulated learning in MOOCs. The Internet and Higher Education, 29, 40–48.

Lo, C. K. (2023). What is the impact of ChatGPT on education? A rapid review of the literature. Education Sciences, 13(4), 410.

Maldonado-Mahauad, J., Pérez-Sanagustín, M., Carvallo-Vega, J., Narvaez, E., & Calle, M. (2022, September). Miranda: A chatbot for supporting self-regulated learning. In European Conference on Technology Enhanced Learning (pp. 455

## References

Reeve, J., Ryan, R., Deci, E. L., & Jang, H. (2012). Understanding and promoting autonomous self-regulation: A self-determination theory perspective. In Motivation and self-regulated learning (pp. 223–244). Routledge.

Roll, I., & Winne, P. H. (2015). Understanding, evaluating, and supporting self-regulated learning using learning analytics. Journal of Learning Analytics, 2(1), 7–12.

Sadriu, S., Nuci, K. P., Imran, A. S., Uddin, I., & Sajjad, M. (2021, December). An automated approach for analysing students feedback using sentiment analysis techniques. In Mediterranean Conference on Pattern Recognition and Artificial Intelligence (pp. 228–239). Springer International Publishing.

Salvagno, M., Taccone, F. S., & Gerli, A. G. (2023). Can artificial intelligence help for scientific writing? Critical Care, 27(1), 1–5.

Schunk, D. H., & DiBenedetto, M. K. (2020). Motivation and social cognitive theory. Contemporary Educational Psychology, 60, 101832.

Stevenson, M. P., Hartmeyer, R., & Bentsen, P. (2017). Systematically reviewing the potential of concept mapping technologies to promote self-regulated learning in primary and secondary science education. Educational Research Review, 21, 1–16.

Strobelt, H., Webson, A., Sanh, V., Hoover, B., Beyer, J., Pfister, H., & Rush, A. M. (2022). Interactive and visual prompt engineering for ad-hoc task adaptation with large language models. IEEE Transactions on Visualization and Computer Graphics, 29(1), 1146–1156.

Tan, C.-W. (2022). The value of cooperation: From AIMD to flipped classroom teaching. SIGMETRICS Performance Evaluation Review, 49(4), 8–13.

Tan, C. W. (2023). Large language model-driven classroom flipping: Empowering student-centric peer questioning with flipped interaction. arXiv, arXiv:2311.14708. https://doi.org/10.48550/arXiv.2311.14708 

Tlili, A., Shehata, B., Adarkwah, M. A., Bozkurt, A., Hickey, D. T., Huang, R., & Agyemang, B. (2023). What if the devil is my guardian angel: ChatGPT as a case study of using chatbots in education. Smart Learning Environments, 10(1), 15.

van der Waa, J., Nieuwburg, E., Cremers, A., & Neerincx, M. (2021). Evaluating XAI: A comparison of rule-based and example-based explanations. Artificial Intelligence, 291, 103404.

Veenman, M. V. J., van Hout-Wolters, B. H. A. M., & Afflerbach, P. (2006). Metacognition and learning: Conceptual and methodological considerations. Metacognition and Learning, 1(1), 3–14.

Velayutham, S., & Aldridge, J. M. (2013). Influence of psychosocial classroom environment on students' motivation and self-regulation in science learning: A structural equation modeling approach. Research in Science Education, 43, 507–527.

Wang, C. Y., & Lin, J. J. (2023). Utilizing artificial intelligence to support analyzing self-regulated learning: A preliminary mixed-methods evaluation from a human-centered perspective. Computers in Human Behavior

## Appendices

## Appendix 1: An Example of Conversations Between SRLbot and Students

**SRLbot**: I'm a science teacher and will help you set your self-regulated learning plans. I will help you design your learning plan and set goals to make you sustain your learning. [Introduce itself and tell students the aim of the chatbot]

**Student**: Thanks. Teachers asked us to set goals. Do you have any suggestions? [Ask for suggestions about goal setting]

**SRLbot**: Of course! Setting goals is an important part of your learning journey. Here are a few suggestions for setting science learning goals... Improve understanding: Set a goal to deepen your understanding of a specific scientific concept or topic. This could involve reading additional resources, conducting experiments, or seeking clarification from your teacher or classmates... Remember, it's important to set specific, measurable, achievable, relevant, and time-bound (SMART) goals. This will help you stay focused and motivated throughout your learning journey.

**Student**: Good suggestions. I'm learning about force and motion. Can you suggest ways for me to evaluate my learning? [Ask for suggestions about self-evaluation]

**SRLbot**: Certainly! Evaluating your learning is an important step to ensure that you have a solid understanding of the concepts you are studying. Here are a few ways you can evaluate your learning in the context of force and motion... Self-assessment: Take some time to reflect on your understanding of force and motion. Ask yourself questions like: Can I explain the relationship between force, mass, and acceleration? Can I apply Newton's laws of motion to real-life situations? Can I solve problems related to force and motion? Assess your own knowledge and identify areas where you feel confident and areas where you may need further review.

**Student**: How about task strategies? [Ask for suggestions about task strategies]

**SRLbot**: Certainly! Task strategies are specific approaches or techniques that you can use to effectively tackle science problems and tasks. Here are some task strategies that can help you with force and motion: Read and understand the problem: Start by carefully reading and understanding the problem statement. Identify the key information, variables and relationships involved. Pay attention to any given data or constraints.

**Student**: No, I mean note-taking skills. [Clarify his previous conversation]

**SRLbot**: Apologies for the misunderstanding. Note-taking skills are indeed important for effective learning. Here are some strategies you can use to improve your note-taking skills in the context of force and motion... Active listening: During class or while studying, actively listen to the teacher or read the material, and identify the main ideas and key concepts related to force and motion. Take notes on these main points rather than trying to write down everything...

**Student**: How about displacement versus distance? What are the differences between them? I'm doing a question in my task. [Asking questions]

## Appendix 2: Interview Protocol

1. How did you interact with SRLbot during your learning activities?
2. Can you describe any specific SRL strategies you employed while using SRLbot?
3. In what ways did SRLbot support your SRL processes?
4. Were there any challenges or limitations you encountered while using SRLbot?
5. What are your thoughts on the limitations of rule-based AI design in Nemobot, particularly in comparison to SRLbot?
6. How did the experience of using SRLbot differ from using Nemobot?
7. Did you find SRLbot or Nemobot helpful in addressing your individual learning needs? If so, how?

---
How to cite this article: Ng, D. T. K., Tan, C. W., & Leung, J. K. L. (2024). Empowering student self-regulated learning and science education through ChatGPT: A pioneering pilot study. British Journal of Educational Technology, 55, 1328-1353. https://doi.org/10.1111/bjet.13454