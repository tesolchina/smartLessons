# Towards a large-language-model-based chatbot system to automatically monitor student goal setting and planning in online learning

Khe Foon Hew*, Weijiao Huang, Sikai Wang, Xinyi Luo and Donn Emmanuel Gonda

The University of Hong Kong, Hong Kong SAR  
*Corresponding author  
kfhew@hku.hk, wjhuang1@connect.hku.hk, sikaiw@connect.hku.hk, xinyiluo@hku.hk, dgonda@hku.hk

## Abstract

Despite the prevalence of online learning, the lack of student self-regulated learning (SRL) skills continues to be persistent issue. To support students' SRL, teachers can prompt with SRL-related questions and provide timely, personalized feedback. Providing timely, personalized feedback to each student in large classes, however, can be labor-intensive for teachers. This 2-stage study offers a novel contribution by developing a Large Language Model (LLM)-based chatbot system that can automatically monitor students' goal setting and planning in online learning. Goal setting and planning are two important skills that can occur in all SRL phases. In stage 1, we developed the Goal-And-Plan-Mentor ChatGPT system (GoalPlanMentor) by creating an SRL knowledge base with goal and plan indicators, using Memory-Augmented-Prompts to automatically detect student goals and plans, and providing personalized feedback. In stage 2, we compared the accuracy of GoalPlanMentor's detection (coding) of students' goals and plans with human coders, examined the quality of GoalPlanMentor's feedback, and students' perceptions about the usefulness of GoalPlanMentor. Results show substantial to near perfect agreement between GoalPlanMentor's and human's coding, and high quality of GoalPlanMentor's feedback in terms of providing clear directions for improvement. Overall, students perceived GoalPlanMentor to be useful in setting their goals and plans, with average values being significantly higher than the midpoint of the scale. Students who highly perceived the system's usefulness for goal-setting exhibited significantly greater learning achievements compared to those with a low perception of its usefulness. Implications for future research are discussed.

**Keywords**: Generative artificial intelligence, Chatbot, Self-regulated learning, Online learning, Large language models

## 1. Introduction

The COVID-19 pandemic has dramatically shifted online learning into the mainstream of education. Even after the pandemic has ended, online learning will remain an option for students, offering flexibility and convenience (Dos Santos, 2022). Online learning is also an essential component of blended learning which combines face-to-face and online activities. The use of online learning will expand since blended learning will become more important in a post-COVID world (Singh et al., 2021).

Although online learning has benefits, the lack of student self-regulated learning (SRL) skills is concerning. In online or blended courses, resources are placed in learning management systems for on-demand use (Pedrotti & Nistor, 2019). With students determining the 'when,' 'how,' and 'where' of learning, self-regulation becomes crucial (Pedrotti & Nistor, 2019; Rasheed et al., 2020). Poor self-regulation can lead to unrelated online activities (Rasheed et al., 2020), negatively impacting learning.

SRL involves individuals intentionally planning, monitoring, reflecting, and adapting their learning progress to achieve learning goals (Pintrich, 2000; Zimmerman, 2002). Students with strong SRL tend to perform better (Cheng et al., 2023). Training students in SRL is thus crucial for enhancing online learning. Scholars identify multiple SRL phases (Panadero, 2017), with Wolters and Brady (2021) proposing three main phases based on prominent models: forethought,

## Self-Regulated Learning and Feedback

Each other as students first define their learning goals and then propose how they plan to reach their goals (Nussbaumer et al., 2011).

In the second phase, performance, students engage in academic work, such as completing writing tasks on the learning management system. Monitoring, a key process in this phase, involves students' ongoing awareness of their actions and adaptation during academic work (Usher & Schunk, 2017). It helps students plan and set goals for future efforts more effectively (Zimmerman & Paulsen, 1995). For example, monitoring writing behavior, during the early stages of a semester, can help students plan subsequent writing sessions, evaluate the effectiveness of writing strategies, and decide on future writing goals.

In the third phase, post-performance, students engage in self-regulation by assessing and reflecting on their learning performance (Usher & Schunk, 2017). Described as self-judgment (Zimmerman, 2002), this phase involves people evaluating the outcomes of their efforts in light of previously established goals (Wolters & Brady, 2021). Depending on whether their performance met their goals, people may need to revise their future goals and plans in order to better achieve their desired outcomes.

Given the importance of SRL, scholars have explored various strategies to promote students' SRL in online learning. One strategy is to use reflective writing exercise to foster students' awareness of SRL. For example, students completed a weekly planning exercise by stating their learning goals of the week, the time spent on the previous week's course activities, and things they learned in the previous week (Pérez-Sanagustín et al., 2021). Butzler (2016) employed a document, called exam wrapper, asking students to answer questions such as how they prepared for the exam.

Another strategy is to embed SRL-related prompts into video lectures. Moos and Bonde (2016) embedded planning prompts (e.g., What do you already know about [this topic]?) at the start of the video, monitoring prompts (e.g., Do you need to adjust how you are learning?) halfway through the video, and reflection prompts (e.g., Do you need to go back in the video and fill any gaps in understanding) at the end of the video. Students verbalized their replies to these prompts. Van Alten et al. (2020a, 2020b) also embedded SRL prompts (e.g., What are your goals when learning from this video?) into video lectures. Students answered the questions in order to continue the video. In about half the SRL prompts, hints would pop up after a student's answer to show an example of that SRL behavior.

These strategies have two drawbacks. First, they often lack timely feedback after students complete reflective writing activities. Hattie and Timperley (2007) define feedback as providing information about students' performance regarding what they attempted. Without timely feedback, less proficient self-regulating students may struggle to know their next steps. Feedback should be within 48 hours to prevent context loss (Barboza & da Silva, 2016; McCarthy, 2016). For Generation Z, raised in an instant-reaction world (Gabrielova & Buchko, 2021), immediate feedback is crucial, as they dislike delays (Eckleberry-Hunt et al., 2018).

Teacher feedback on students' reflections may not be timely due to the laborious process of reading individual responses and tracking his/her goals and plans. For example, in Butzler's (2016) study, students completed exam wrappers, and the teacher provided individual student feedback on SRL strategies. This feedback was not immediate due to the time needed to read each student's answers. Scaling up such feedback for larger student numbers is challenging. The second drawback is the lack of personalized feedback, as seen in van Alten et al. (2020a, 2020b), where hints were general to all students (e.g., make notes, rewind video)

## Overview of GoalPlanMentor

automatically monitor students' goal setting and planning activities in online learning. Although goals and planning most often occur in the forethought phase, they can also occur in the performance phase (monitoring goal progress and plans), and post-performance phase (evaluating whether one has achieved one's goal and adjusting future plans).

In this two-stage study, we first addressed a key major LLM limitation – the inability to store new experiences in long-term memory during a dialog (Sejnowski, 2023). LLMs are "amnesics, like humans who have lost their hippocampus and are unable to remember new experiences for more than a few minutes, unable to create long-term memories" (Sejnowski, 2023, p. 327). We developed an SRL knowledge base to store the user chat records, along with relevant Memory-Augmented-Prompts that enabled GoalPlanMentor to retrieve students' goals and plans and provide personalized feedback. Next, we compared GoalPlanMentor's detection (coding) accuracy of students' goals and plans with human coders, assessed the quality of GoalPlanMentor's feedback on students' goals and plans, and student perceptions on the usefulness of the feedback. We addressed the following research questions:

Research question 1: Can GoalPlanMentor accurately detect students' goals and plans, and in particular, what is the comparative accuracy between GoalPlanMentor system and human evaluators?

Research question 2: What is the quality of the feedback provided by GoalPlanMentor?

Research question 3: What are students' perceived usefulness of the GoalPlanMentor?

## Designing the goal-plan-mentor chatbot system (GoalPlanMentor)

### Overview of GoalPlanMentor

GoalPlanMentor is a web-based system designed to facilitate the goal setting and planning processes of students' online learning. We utilized Vue.js, a JavaScript framework, for the frontend development of the system. The frontend webpage allows students to interact with the chatbots (see Figures 1 and 2). Initially, students input their usernames before selecting a chatbot by clicking on the green button (see Figure 1) to start a conversation. Upon concluding the conversation, students can submit their current assignments to teacher or access previous submission records through the system (see Figure 2).

For the backend, we chose Python and Django, a framework for swift, secure, and maintainable web development, providing a set of application programming interfaces (APIs) that the frontend uses to interact with the system (Christie et al., 2020). They enable essential operations such as user authentication, conversation management, and assignment submission. The core of the backend comprises the agent module (Figure 3), which integrates OpenAI's latest generative AI for processing and understanding user inputs, providing appropriate responses, and maintaining conversational context. We leveraged algorithms related to databases, prompt engineering, and finite state machines (FSM) to develop GoalPlanMentor with a dual-agent architecture. The system comprises two agents: (1) GoalPlanDetectAgent (GPDA) identifying students' goals and plans based on their chat logs, and (2) GoalPlanAwareTeachingAgent (GPATA) assisting students in reflecting on and revising their previous goals and plans throughout course instruction. By combining the GPDA and the GPATA agents, our system creates an environment that both recognizes students' goals and plans, and actively assists students in achieving them.

### GoalPlanDetectAgent (GPDA)

Key SRL indicators such as goal-setting and planning facilitate insights into students' learning strategies, enabling pattern recognition and progress tracking. This allows for personalized feedback that cultivates SRL behaviors and ultimately improves learning outcomes (Raković et al., 2022). Thus, we intended the GPDA agent to recognize patterns and phrases indicating a student's goals and plans from chat logs. Once identified, they are stored in a database for future reference and tracking

## 3.2 Data Analysis

### 3.2.1 Database Design

The GPDA comprises two databases: the Chat History Database (CHDb) and the Goal setting and Planning Database (GPDb).  

The CHDb stores the chat records of each student with each chatbot, as well as the progress of each conversation (e.g., welcome, ongoing, and finished). It can provide accurate context for each dialogue, aiding the chatbot in remembering and understanding past discussions, thus reducing the generation of hallucinatory responses by supporting the LLM's external memory. The GPDb is responsible for storing the weekly goals and plans set by students that are extracted from dialogues.  

Relational databases simplify the storage, query, and analysis of the aforementioned personalized goal and plan data. The structured storage approach allows data attributes such as goal content and planning time frame to be independently managed, thereby enhancing data consistency and validity and improving data readability and operability.  

The relational database also facilitates efficient and flexible data queries and analysis. We can obtain the goals and plans of specific students or count the number and proportion of student goals achieved over a period by writing SQL queries. Additionally, by leveraging the database's data correlation, we can gain a deeper understanding of students' learning behaviors and progress. Analyzing students' goals, plans, and their completion status can reveal learning patterns (e.g., whether students tend to set long- or short-term goals, their pace in achieving those goals, etc.). This information forms a significant reference in our design and provision of personalized learning support.

### 3.2.2 Goal and Plan Detection

The GPDA's main task is to extract specific content relating to students' goal-setting and planning behavior from chat records. As these goals and plans often gradually emerge over multiple rounds of dialogue, stronger Natural Language Understanding (NLU) capabilities are needed to recognize intent and entity in context. Transformer-based LLMs such as GPT, unlike humans, inherently lack long-term memory beyond their immediate context window due to their auto-regressive nature, which predicts the next token purely based on preceding context (Vaswani et al., 2017).   

To address this, we designed a Memory-Augmented Prompt (MAP) to drive GPT-4 (via the OpenAI API, model name gpt-4-0613) (OpenAI, 2023), which is among the most advanced current LLMs. MAP incorporates past interactions into current context, simulating the model's "memory" and overcoming its inherent inability to remember past interactions. Accordingly, the dialogues stored in the CHDb are made available for GPT-4 to query and analyze. By combining past interactions, MAP stimulates GPT-4 to perform more accurate intent and entity recognition across multiple dialogue turns.

Table 1. Memory-augmented prompt (MAP) for goal/plan detection

| MAP Component | Prompt Text |
|---------------|-------------|
| Chain of Thought Nodes | You are skilled at extracting key information from conversations, and you can analyze the intent and entity of each sentence. Your task is to analyze the whole conversation history and determine: 1. What personal learning goal has the user established? 2. What plan has the user formulated to meet this goal? |
| Role Configuration | Here are the steps to identify the user's goal and plan: 1. Examine the assistant's discussions about the user's goals and plans. 2. Derive from the user's replies their specific goals and plans for the course. Prioritize the user's actual learning objectives for the course over the assistant's hypothetical situations or proposed cases. 3. Locate user plan: Users may use the SMART framework to make plans for achieving goals, or they might also directly say their own plans. 4. Addressing undefined goals and plans: In situations where the user's goals remain undefined, it is reasonable to infer that plans associated with these goals are also absent. |
| Dialogue History Analysis | Here is a corner case to help you better understand and analyze user objectives and strategies: EXAMPLE #1: |

## Memory Augmented Prompting Components

## Chain of Thought Integration

Table 1 shows how our MAP integrates the Chain of Thought (CoT), Response Formatter, and Memory Injection components to enhance the GPT-4 model's understanding of these "memories." Fundamentally, CoT aims to provide LLMs with illustrative examples that clarify an underlying reasoning which the LLM should mirror within its responses, enhancing the precision of generated text (Wei et al., 2022). Our CoT method delineates the essential steps involved in extracting goals and plans, providing the model with a structured approach to processing and understanding information retrieved from CHDb.

The first CoT node is Role Configuration, which involves assigning the model a specific role and task. This pivotal step equips the model to better grasp the actions it is anticipated to perform.

The following node is Dialogue History Analysis. Here, the MAP directs the model to critically analyze previous dialogues the assistant has participated in, focusing on the user's goals and plans. CoT then shifts the model's attention to deriving these goals and plans. This reasoning process emphasizes the user's actual learning objectives for a particular course, giving precedence to these over any theoretical scenarios (e.g., course design cases) suggested by the assistant.

Once identified, the CoT transitions to fine-tuning and validating the extracted goal and plan; it instructs the model to determine if the user has utilized a specific framework, such as SMART, to achieve their goals, or if they have explicitly outlined their plans. This process exemplifies the reasoning involved in understanding the user's strategies for achieving their objectives. In this way, the model gains a comprehensive understanding of the conversational context and nuances; thus, it learns a reasoning process facilitating accurate analysis and information extraction.

In the subsequent One-Shot Corner Case Demonstration node, the MAP addresses situations where the user's goals are vaguely defined. The model is guided to deduce that associated plans are likely null in these instances. This design aims to strike a trade-off between providing structured guidance and preserving the model's generative potential. Controlling the breadth and depth of examples in prompts presents a significant challenge: overly detailed examples may make the model's generative direction overly singular, while a lack of detail can exacerbate hallucinations (Sun et al., 2023). Accordingly, we emphasize using negative examples in the MAP. This helps the model understand unclear user goals and plans and promotes its capacity to generate concise summaries of user goals and plans from multiple-round dialogues.

## 3.3. GoalPlanAwareTeachingAgent (GPATA)

The GPATA chatbot is specifically designed to interact directly with students. It leverages the capabilities of prompted GPT3.5 (via the OpenAI API, model name gpt-3.5-turbo-16k-0613) and an FSM to enable smooth conversation and effective dialogue-state management. Its core functionality lies in retrieving individual student-related information from the GPDA. It focuses mainly on the learning goals and plans set by the student in the weeks leading up to the current interaction and chat records within the same timeframe. Therefore, the GPATA can integrate the information of goals and plans to form a personalized conversational context for each student. This context not only reflects a history of the student's interactions with the GPATA to complete their learning tasks, but also serves as a reference for understanding the student's learning situation. With this context, the GPATA obtains an accurate awareness of each student's goal setting and planning behaviors during current chat interactions and provides personalized recommendation. We explained the overall design of the FSM and the prompts for GPT3.5 in GPATA below.

The FSM is a mathematical model used to simulate sequential logic and procedural control. It is an abstract machine that can be in one of a finite number of states, transitioning between them in response to external inputs (Lee et al., 2018). By managing conversation states clearly, the FSM ensures organized and systematic dialogue progression. It also bolsters maintainability and scalability, permitting state transitions without system disruption. Moreover, FSM is beneficial in error handling, effectively managing unexpected user inputs and steering the conversation towards a stable state.

[Figure 4. Unified Modeling Language diagram of the FSM used in GPATA]

The Unified Modeling Language (UML) diagram in Figure 4 lists the various states and transitions defined in the proposed FSM, systematically demonstrating the dialogue flow progression. Student–GPATA dialogues begin by entering the GoalPlanReflectAndModify state, in which GPATA retrieves the student's goals and plans established over the past two weeks from the GPDb. It then employs a rubric to categorize the student into one of three cases:

- The student established goals and plans in the previous week.
- The student only set goals and plans two weeks prior and not in the preceding week.
- The student did not set any goals or plans over the past two weeks.

Once the GPATA identify students' status, it can guide individual students to reflect and modify learning goals and plans and guiding them to complete weekly online learning tasks. For each stage, the GPATA utilize prompts to stimulate GPT3.5 to generate dialogues. Prompt engineering—strategically crafting input prompts to obtain desired model outputs (Liu et al., 2023)—is crucial when working with LLMs. Appendix A shows the prompts design in each stage of the GPATA.

### 3.3.1 Reflection stage

For cases 1 and 2, GPATA guides the student to reflect. It initially prompts the student to recall and input the goals and plans they set. Regular reflection allows students to evaluate whether their current goals are realistic and attainable. Next, GPATA returns the stored "ground truth" from GPDb to the student, encouraging them to revisit their previous goals and plans. Figure 5 demonstrates how the GPATA support a student to recall and revisit her goals and plans. The dialogue then transitions into the Modification stage, where GPATA queries whether the student needs to modify their current goals and plans. The student can inform GPATA of newly established goals and plans (if any), which GPATA subsequently stores in the GPDb. For case 3, GPATA directly enters the Modification stage.

### 3.3.2. Modification stage

The modification process is initiated by a prompt that encourages students to reconsider and potentially revise their goals and plans. The SMART framework, encompassing Specific, Meas

## Method

## Participants and Context

A total of 25 Asian students (20 female, 5 male) participated in an eight-week Education course. Ethical approval was obtained from the University Ethics Review Board. The course consisted of six weeks of lectures on adult learning strategies, followed by two weeks in which students demonstrated the application of these strategies in the classroom.

During the six-week lecture period, the GoalPlanMentor system was implemented to help students set personal learning goals and plans and monitor students' goals and plans by giving personalized feedback. GoalPlanMentor also guided students to complete the weekly online learning tasks. GoalPlanMentor was accessible via Moodle, a learning management platform where the teacher had uploaded all learning materials.

In the first week, a researcher introduced the study and GoalPlanMentor. From week 1 to week 3, students interacted with GoalPlanMentor to familiarize themselves with it. During this time, students were able to set their personal learning goals and plans with GoalPlanMentor. At the same time, we fixed any technical issues reported by the students and make the necessary updates. In week 4, we implemented the goal and plan detection feature (i.e., GPDA) in the backend of the system. This feature is used to recognize each student's previously set goals and plans and later provide them with appropriate feedback for their personal learning. Before releasing this feature to students in the frontend, we measured its accuracy in detecting students' goals and plans by comparing it with human coders in week 4 (RQ1). Since the detection accuracy was satisfactory, GoalPlanMentor started monitoring students' goals and plans by the GPTAT agent from week 5.

After the intervention, we assessed the quality of the system's feedback in terms of coherence, relevance, and positive tone (RQ2). Students' perceptions of the GoalPlanMentor's feedback on their goals and plans were assessed through a usefulness questionnaire and follow-up semi-structured interviews (RQ3). Figure 6 illustrates the intervention process.

[Figure 6. The intervention process of this study]

## Measurements

### Accuracy of Goal and Plan Detection

To answer the first research question, we coded the accuracy of the system's goal and plan detection in weeks 4-6 on a scale of five: 5 for being completely accurate, 4 for being more than half accurate, 3 for being half accurate, 2 for less than half accurate, and 1 for being not at all accurate. Appendix B presents some examples of the goal and plan detection.

### Quality of Feedback

Drawing from prior studies (e.g., Motz et al., 2021; Munoz et al., 2006; Siekmann et al., 2022), we evaluated the quality of feedback provided by the chatbot system in week 5 and week 6 based on three dimensions: Coherence, Relevance, and Positive Tone (see Appendix C for examples). Our scores for these dimensions are calculated as follows:

- Coherence: Coherence refers to "a form of connecting sentences and ideas aimed at supporting readers' understanding" (Siekmann et al., p. 2). Coherent feedback relates information together so that the reader can follow the thread of ideas (Munoz et al., 2006). We give a score of 3 if the feedback is coherent, 2 if the feedback is somewhat coherent, and 1 if it is incoherent.

- Relevance: Students should be provided with relevant feedback on their work because this will motivate them to improve both the work they have already done and the work they will do in the future (Goodwin & Kirkpatrick, 2023). We give a score of 3 if the feedback relates to the students' goal setting and planning, 2 if the feedback has some digressions and irrelevancies, and 1 if the feedback is not related to the

Here's the cleaned Markdown:

## 5. Results

### 5.1. Accuracy of Goal and Plan Detection

For 1 student who did not discuss personal learning plans with the system, it generated plans based on the students' chat history. There was perfect agreement between the two coders' judgements, κ = 1.000, 95% CI [1, 1], p < .001.

The Cohen's kappa results show that the observed agreements between the two coders are statistically significant (for both goal and plan detection, p < .001), indicating a high level of agreement between the coders. Therefore, we averaged the system detection accuracy levels coded by the two researchers. The average goal detection accuracy was 4.68 (SD = .802), while the average plan detection accuracy was 4.32 (SD = 1.215).

To further verify the accuracy of the automatic detection system, we implemented it during weeks 5 and 6. As there was one missing value for each week, we examined the goals and plans of 24 students. In week 5, the average goal detection accuracy was 4.58 (SD = 1.100), while in week 6, it was 4.54 (SD = .833). Regarding plan detection, the average accuracy for week 5 was 4.21 (SD = 1.179) and for week 6, it was 4.58 (SD = 1.176). We conducted a Friedman test to investigate any significant differences in the system's goal and plan detection accuracy across weeks 4, 5, and 6 (Table 2). This test was chosen due to the violation of the normality assumption in the data for each of the three weeks. The results showed no significant differences in the system's goal detection accuracy over the three weeks, with χ²(2) = 0.950, p = 0.622. Similarly, the system's plan detection accuracy results were χ²(2) = 3.636, p = 0.162, indicating no significant differences across the three weeks. Thus, the automatic detection system demonstrated consistent accuracy in detecting goals and plans during weeks 4, 5, and 6.

Table 2. Friedman's ANOVA Test on the system's goals and plans detection accuracy

| Dimension | Group | N | Mean (SD) | Chi-Square | df | Sig. |
|-----------|--------|---|------------|------------|----|----|
| Goal Accuracy | Week 4 | 24 | 4.68 (0.082) | .950 | 2 | .622 |
| | Week 5 | 24 | 4.58 (1.100) | | | |
| | Week 6 | 24 | 4.54 (1.179) | | | |
| Plan Accuracy | Week 4 | 24 | 4.32 (1.215) | 3.636 | 2 | .162 |
| | Week 5 | 24 | 4.21 (1.179) | | | |
| | Week 6 | 24 | 4.58 (1.176) | | | |

### 5.2. Quality of feedback of GoalPlanMentor

In Week 5, twenty-one students participated in the goal setting and planning activity, and the feedback provided by GoalPlanMentor to these students was analyzed. Both coders agreed that 20 students received coherent feedback, except for one student who received partially coherent feedback ("Apologies for any confusion earlier. Let's focus on your goal...") due to this student's brief input ("no"). The agreement between the two coders was substantial as indicated by the Cohen's kappa result, κ = 0.64, 95% CI [0.01, 1.28], p = .002. Additionally, there was perfect agreement between both coders that GoalPlanMentor

## Results

monitoring their goals (item 4) and plans (item 10). We conducted t-tests to determine if the results are statistically different from the midpoint. Following the practice of previous research (e.g., Beder et al., 2011; Wang et al., 2017), we defined the midpoint as a score of 2.5 (midpoint of rating 1 to 5), which indicates neither a positive nor negative finding. Results show that the overall mean perceived usefulness in goal-setting score (M = 3.40, SD = 0.94), and overall mean perceived usefulness in planning score (M = 3.35, SD = 0.93) were significantly greater than the midpoint score of 2.5, t(19) = 4.28, p < .001, and t(19) = 4.09, p < .001 respectively. This suggests that participants found the system to be useful in both goal-setting and planning aspects.

Table 3. Mean and standard deviation for students' perceived usefulness of the system

| Item | M (SD) |
|------|---------|
| **Perceived usefulness in goal-setting (n = 20)** | |
| 1. Using the system enabled me to reflect on my personal goal-setting. | 3.15 (.81) |
| 2. Using the system made it easier to comprehend my personal goal-setting. | 3.35 (.88) |
| 3. My comprehension of the personal goal-setting would be easy to obtain with the system. | 3.20 (.83) |
| 4. The system enhanced my effectiveness in preparing my personal goal-setting. | 3.30 (.87) |
| 5. Overall, I found the system was useful in my personal goal-setting. | 3.40 (.94) |
| **Perceived usefulness in planning (n = 20)** | |
| 6. Using the system enabled me to reflect on my personal plan. | 3.50 (1.00) |
| 7. Using the system made it easier to comprehend my personal plan. | 3.30 (.92) |
| 8. My comprehension of the personal plan would be easy to obtain with the system. | 3.35 (.93) |
| 9. The system enhanced my effectiveness in preparing my personal plan. | 3.30 (.80) |
| 10. Overall, I found the system was useful in my personal plan. | 3.35 (.93) |

We examined the differences in students' learning achievement on their final assignment between the low- and high-groups in terms of their perceived usefulness. Students were categorized into either a high-perceived usefulness group (n = 5, top 25% of students) or a low-perceived usefulness group (n = 5, bottom 25% of students) based on the ranking of their responses on perceived usefulness in the goal setting and planning scales. The course instructor, with eight years of experience, assessed students' final assignments on designing an adult workshop toolkit, which included a document outlining the workshop's topic, goals, activities and their rationale. Both the instructor and a coder individually rated the assignments and then reconciled any differences in their evaluations.

### Difference in learning performance between the low- and high-perceived usefulness groups in terms of goal-setting

The final scores of the high-perceived group (M = 51.0, SD = 5.15) and the low-perceived group (M = 31.8, SD = 14.26) were normally distributed for both groups (Shapiro-Wilk's test, p ≥ .05). The variances of the final scores were homogeneous for both groups (Levene's test, p = .119). An independent-samples t-test showed that students who highly perceived GoalPlanMentor's usefulness for goal-setting exhibited significantly greater learning achievements compared to those with a

## Table 4. Independent-samples t-tests on students' learning performance between the low- and higher-achievers

| Perceived usefulness | Group | n | Mean (SD) | p-value |
|---------------------|-------|---|------------|----------|
| Goal setting | High | 5 | 51 (5.15) | .022 |
| | Low | 5 | 31.8 (14.26) | |
| Planning | High | 5 | 52 (5.52) | .156 |
| | Low | 5 | 40.6 (14.35) | |

We analyzed students' interview data to better understand their perceptions of GoalPlanMentor's usefulness and gather suggestions for future improvements. Three key themes emerged from the interview data highlighting the usefulness of GoalPlanMentor: clear goals and plans clarification, ongoing learning reflection, and personalized communication.

## Clear goals and plans clarification

Setting clear goals and plans is crucial, especially at the beginning of a course. Students (n = 8) reported GoalPlanMentor clarified their goals and plans through the SMART framework and provided diverse ideas and suggestions. Students elaborated on the initial simplicity of their goals and how they gradually refined them with the guidance of GoalPlanMentor. For example:

> At the beginning of our conversation, I stated my goals in a very simple way. However, as it [GoalPlanMentor] prompted me to become more specific using the SMART framework, my learning goals became more concrete at the end. (Participant 8)

Providing diverse ideas and suggestions on students' goals "broaden my perspectives and expand my thinking during the goal-setting and planning process" (Participant 12). This highlights students' active engagement with GoalPlanMentor for varied perspectives in goal setting. Clear goals and plans at the start of the course encourages student ownership and set the tone for a self-regulated learning experience.

## Ongoing learning reflection

In weeks 5 and 6, GoalPlanMentor displayed students' previous goals and plans, "providing a time-saving advantage" (Participant 14), enabling students to recall and reflect on their personal goals and plans without the need for extensive memory retrieval. These students (n = 12) highlighted the importance of the weekly reminders in maintaining their learning focus. For example:

> In the midst of absorbing new knowledge and completing various learning activities throughout this course, I sometimes forget my learning objectives. The weekly reminders not only help me recall my goals but also allow me to reflect on my learning progress and assess whether I am on track. (Participant 6)

Students also appreciated the flexibility offered by GoalPlanMentor to modify their goals and plans as their understanding of the course content deepened in later sessions:

> My initial goals were unrelated to the course since I was not familiar with the learning content at the beginning of the semester. As my knowledge of the course material deepened, I tended to revise some of my initial goals. I would ask the system to repeat what we discussed last week. Based on that, I would make modifications. (Participant 4)

The ability to revise goals and plans helped students reflect on their own learning and align their objectives with the course material, ensuring that their goals remain relevant and mirror their developing understanding.

## Personalized communication

Some students (n = 3) reported that GoalPlanMentor helped them customize learning goals and plans to their individual needs and professional contexts. The lack of human judgment allowed students to freely explore goal-setting questions related to their unique backgrounds. One student shared:

> It [GoalPlanMentor] allows me to make my goals more related to my personal development. I work in a startup and my background is different from the majority of my classmates who are in-service teachers. Sometimes I'm hesitant to ask questions in class because my questions may not be relevant to them. So having this [GoalPlanMentor] allows me to set my personal learning goals because

## Acknowledgment

All authors declare that they have no conflicts of interest. This work was supported by the Research Grants Council of Hong Kong Research Fellow Scheme (Reference no: RFS2223-7H02). Generative AI tool (ChatGPT 4) was used to improve the readability of some writings in this manuscript. After using this tool, the authors reviewed and edited the specific contents and take full responsibility for the accuracy of the contents.

## References

- Baidoo-Anu, D., & Owusu Ansah, L. (2023). Education in the era of Generative Artificial Intelligence (AI): Understanding the potential benefits of ChatGPT in promoting teaching and learning. Journal of AI, 7(1), 52-62. https://doi.org/10.61969/jai.1337500

- Barboza, E.J.S., & da Silva, M.T. (2016). The importance of timely feedback to interactivity in online education. In I. Nääs, O. Vendrametto, J. M. Reis, R. F. Goncalves, M. T. Silva, G. von Cieminski & D. Kiritsis (Eds.), Advances in Production Management Systems. Initiatives for a Sustainable World (pp. 307-314). Springer. https://doi.org/10.1007/978-3-319-51133-7_37

- Beder, J., Coe, R., & Sommer, D. (2011). Women and men who have served in Afghanistan/Iraq: Coming home. Social Work in Health Care, 50(7), 515-526. https://doi.org/10.1080/00981389.2011.554279

- Butzler, K. B. (2016). The synergistic effects of self-regulation tools and the flipped classroom. Computers in the Schools, 33(1), 11–23. https://doi.org/10.1080/07380569.2016.1137179

- Cheng, Z., Zhang, Z., Xu, Q. Maeda, Y., & Gu, P. (2023). A meta-analysis addressing the relationship between self-regulated learning strategies and academic performance in online higher education. Journal of Computing in Higher Education, 1-30. https://doi.org/10.1007/s12528-023-09390-1

- Christie, M., Marru, S., Abeysinghe, E., Upeksha, D., Pamidighantam, S., Adithela, S. P., Mathulla, E., Bisht, A., Rastogi, S., & Pierce, M. (2020). An extensible Django-based web portal for Apache Airavata. In Practice and Experience in Advanced Research Computing (pp. 160-167). Association for Computing Machinery. https://doi.org/10.1145/3311790.3396650

- Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS quarterly, 319-340. https://doi.org/10.2307/249008

- Dos Santos, L. M. (2022). Online learning after the COVID‐19 pandemic: Learners' motivations. Frontiers in Education, 7, 879091. https://doi.org/10.3389/feduc.2022.879091

- Eckleberry-Hunt, J., Lick, D., & Hunt, R. (2018). Is medical education ready for Generation Z? Journal of Graduate Medical Education, 10(4), 378–381. https://doi.org/10.4300/JGME-D-18-00466.1

- Fergus, S., Botha, M., & Ostovar, M.

## References

Liu, P., Yuan, W., Fu, J., Jiang, Z., Hayashi, H., & Neubig, G. (2023). Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. ACM computing surveys, 55(9), 1-35. https://doi.org/10.1145/3560815

Locke, E.A., & Latham, G.P. (1990). A theory of goal setting and task performance. Prentice-Hall Inc.

Locke, E. A., & Latham, G. P. (2002). Building a practically useful theory of goal setting and task motivation: A 35-year odyssey. American Psychologist, 57(9), 705–717. https://doi.org/10.1037/0003-066X.57.9.705

MacLeod, L. (2012). Making SMART goals smarter. Physician Executive, 38(2), 68-72.

McCarthy, J. (2016). Timely feedback: Now or never. Edutopia. George Lucas Educational Foundation. https://www.edutopia.org/blog/timely-feedback-now-or-never-john-mccarthy

Moos, D. C., & Bonde, C. (2016). Flipping the classroom: Embedding self-regulated learning prompts in videos. Technology, Knowledge and Learning, 21(2), 225-242. https://doi.org/10.1007/s10758-015-9269-1

Motz, B., Canning, E., Green, D., Mallon, M., & Quick, J. (2021). The influence of automated praise on behavior and performance. Technology, Mind, and Behavior, 2(3), 1–12. https://doi.org/10.1037/tmb0000042

Munoz, A. P., Mueller, J., Álvarez, M. E., & Gaviria, S. (2006). Developing a coherent system for the assessment of writing abilities: Tasks and tools. Íkala, revista de lenguaje y cultura, 11(1), 265-307. https://doi.org/10.17533/udea.ikala.2791

Nussbaumer, A., Albert, D., & Kirschenmann, U. (2011). Technology-mediated support for self-regulated learning in open responsive learning environments. In 2011 IEEE global engineering education conference (EDUCON) (pp. 421–427). IEEE. https://doi.org/10.1109/EDUCON.2011.5773171

OpenAI. (2023). GPT-4 Technical Report. https://cdn.openai.com/papers/gpt-4.pdf

Panadero, E. (2017). A review of self-regulated learning: Six models and four directions for research. Frontiers in Psychology, 8. https://doi.org/10.3389/fpsyg.2017.00422

Pedrotti, M., & Nistor, N. (2019). How students fail to self-regulate their online learning experience. In M. Scheffel, J. Broisin, V. Pammer-Schindler, A. Ioannou & J. Schneider (Eds.), Transforming Learning with Meaningful Technologies: 14th European Conference on Technology Enhanced Learning (pp. 377-385). Springer. https://doi.org/10.1007/978-3-030-29736-7_28

Pérez‐Sanagustín, M., Sapunar‐Opazo, D., Pérez‐Álvarez, R., Hilliger, I., Bey, A., Maldonado‐

## Appendix A. Prompts design in GPATA

### Stage: Reflection

Taking Case 1 as an example, we prompted the GPT3.5 as follow:

Your first prompt is: "We've been putting in effort to become self-regulated learners, and I really hope you're actively embracing your learning journey in this course, aligning it with your own personal goals for growth and improvement. Can you recall what personal learning goal you've set in week 4?"

You should refine the following sentence using the expression of the second person:
"I remember we talked about your goal and plan in week 4: '<week 4 goal>,<week 4 plan>.' Have you changed/modified your learning goal and plan? If so, what are your goal and plan now? Here you should wait for my answer."

### Stage: Modification

We just finished recalling my own personal learning goal of the course in week 4.

Your first prompt should be: "Do you want to revise your goal and plan using the SMART framework?" You should wait for my response.

If I don't want to revise my goal and plan, you should skip the first section, and dive into the second section directly.

If I want to revise, you should guide me to clarify and plan my new goals based on 5 aspects ("SMART," "Specific," "Measurable," "Attainable," "Relevant," "Time-based") in SMART in order.

Here are some example questions for SMART Framework you can use in your response to my goal:

1. Specific: Define a clear, specific goal (e.g., What do I want to accomplish?)
2. Measurable: make sure you can track progress (e.g., How will I know when it is accomplished?)
3. Relevant: A relevant goal can answer "yes" to these questions (e.g., Does this match my other efforts/needs?)
4. Attainable: (e.g., How can I accomplish this goal?)
5. Time-bound/Timely (reference data for completion): (e.g., When do you expect to achieve your learning goals?)

## Rules and Instructions for Course Design Activity

## SMART Framework Guidelines
1. If I ask for your suggestion, provide suggestions and ask me to revise or adapt them to my own goal
2. Keep responses under 100 words
3. Provide concise summary of personal learning goals and verify accuracy with: "Did I summarize your goals and plans accurately? If not, feel free to edit"
4. Discuss all 5 SMART aspects (Specific, Measurable, Relevant, Attainable, Time-bound)

## Task Instructions
You will act as a guide to help complete a course design activity. Begin with:

"Your task is to design a lesson to teach adults on the topic 'Writing an effective resume'. I will guide you step by step. Shall we start?"

Guide the "resume course" design through five components:
- Learning objectives
- Course structure
- Course content
- Teaching methods
- Assessment

Remind and request completion if any components are missed.

## Appendix B: Goal and Plan Detection Accuracy Scale

| Scale | Accuracy | Definition | Example Student Response | System Detection Result |
|-------|-----------|------------|------------------------|------------------------|
| 1 | 0% | System fabricates goals/plans | None provided | System generated fabricated plan |
| 2 | <50% | Minor portion correctly detected | Feedback plan with timeline | Only timeline detected |
| 3 | 50% | Half correctly detected | Workshop organization goal | Basic workshop creation goal detected |
| 4 | >50% | Mostly correctly detected | Detailed learning and implementation plan | Most elements accurately captured |
| 5 | 100% | Completely correctly detected | "Learn how to engage adult learner" | Exact goal captured |

## Appendix C: Feedback Quality Coding Scheme

### Coherence
1. Incoherent feedback
2. Somewhat coherent feedback
3. Coherent feedback with clear logic

### Relevance
1. Not related to goals/plans
2. Some digressions from goals/plans
3. Directly relates to goals/plans

### Positive Tone
1. Lacks support, may be critical
2. Neutral tone
3. Positive and encouraging