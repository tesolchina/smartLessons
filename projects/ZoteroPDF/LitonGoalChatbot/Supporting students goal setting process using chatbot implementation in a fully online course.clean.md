# Supporting Students Goal Setting Process Using Chatbot Implementation in a Fully Online Course

**Jiahui Du**, **Weijiao Huang**, **Khe Foon Hew**  
Faculty of Education  
The University of Hong Kong  
Hong Kong SAR, China  
{dujiah, wjhnang1, kfhew}@connect.hku.hk

## Abstract

School closures during the COVID-19 pandemic highlight the need for promoting efficient online learning. Without external pressure and guidance, fully online learners are expected to self-monitor their learning process and find paths to achieve learning goals; such abilities are considered self-regulated learning (SRL) skills. To become a self-regulated learner, the first step is to learn how to set effective learning goals. However, this is difficult for learners with lower SRL skills, since they may not have enough knowledge on selecting and adopting the appropriate goal setting strategies. Thus, there is a need for supporting fully online learners on setting effective learning goals. This study introduces a new approach of enhancing students' goal setting skills by interacting with a chatbot, which embedded some guiding questions based on a goal setting strategy. Students in an online course were invited to complete a goal setting activity prior to class, and their perceptions of the activity were collected via interviews. The findings from this study shed light on future designs of chatbot supporting SRL activities.

**Keywords**: Self-regulated learning, goal setting, chatbot, online learning

## Introduction

The COVID-19 pandemic has caused large-scale disruptions in the education field. Reports show that more than 91% of total enrolled learners worldwide were affected by school closures [1]. In response to the urgent demands on continuation of school education, adapting to fully online learning became the only choice for most learners. In the absence of face-to-face guidance and support from instructors, fully online learners are expected to self-monitor their learning process and find paths to achieve learning goals [2]. Such abilities to conduct autonomous learning and taking control over one's learning process by applying cognitive strategies are considered as self-regulation skills. However, many online learners are reported as lacking self-regulation skills and not ready for conducting autonomous learning online [3], [4].

Self-regulated learners are expected to set goals at the beginning of their learning, yet, not all goals set by learners are effective [5], [6]. Without being able to accurately estimate the workload of the learning process as well as evaluate individual abilities of completing tasks, goals can be ineffective in directing learners toward success. Moreover, in a fully online context, learners might not be able to receive immediate feedback from their teachers, which might delay the progress of learning. These gaps indicate the critical need to support learners on setting and evaluating their learning goals.

The present study implemented a chatbot to help learners set effective goals at the beginning of their learning. By outlining the questions using a goal setting strategy, the chatbot guides students through the process and enables them to find their most appropriate learning goals. This study is a follow-up study of [7], which only examined students' perceived usefulness and ease of use of the chatbot. In this study, we emphasized the use of chatbot in the context of SRL. We focused more on exploring students' perceptions of the entire learning process with the support of chatbot, particularly in promoting goal setting skills and investigating its potential for bolstering other SRL activities. Thus, we proposed two research questions:

1. In what ways do students think that chatbot activity helps them in their goal setting process?
2. What are students' expectations towards the future development of chatbot activity?
   - How can the current chatbot-assisted goal setting activity be improved?
   - What expectations do students have on chatbot toward supporting other SRL activities?

This study contributes ideas for exploring new perspectives on supporting students' goal setting process in fully online courses. We provide insight into the design of SRL scaffold from the chatbot approach, with a particular aim of facilitating SRL by enhancing the awareness and abilities to adopt goal setting strategies. Students' responses toward their experience of learning with chatb

Here's the cleaned and normalized Markdown:

## Goal Setting in Learning

To better control the learning performance, a self-regulated learner will set specific learning goals at the beginning of their learning experience, such as before starting a course or a new semester. In this way, the learning goal can serve as a guidance to give learners a clear indication of what they expect to attain for their future learning [6]. This goal setting process is one of the key factors that can promote an effective learning experience. Previous study also found that successful learners have significantly higher applications of goal setting strategy [13].

In the goal setting process, learners will define the outcomes for their learning and propose how they plan to reach their goals [14]. However, the challenge of adopting this strategy is that learners with lower self-regulation skills tend to have ambitious and unrealistic goals, which may finally disappoint the learners after their learning [10]. In this case, goal setting strategies such as SMART [15], can be extremely helpful for learners who do not know how to set effective goals. SMART framework contains five key criteria of writing meaningful objectives and goals. Starting from "S", each letter refers to a rule: specific, measurable, achievable or assignable, realistic, and time-related. Each learning goal should be set and evaluated based on these five rules. Nowadays, the SMART framework has been used widely for developing program goals and objectives [16].

Previous studies reported that goal setting is a foundational strategy that developers need to take into consideration when promoting SRL [17]. [18] explored the influence of using e-portfolio to help students set learning goals. Within the personal e-portfolio, students are able to view and organize their own works and learning progress, which can be used as indicators to adjust the learning goals in their further study. Similar approaches of using profiles to assist students to set goals and monitor learning process were also applied in other studies [19], [20]. However, in addition to assisting learners to adjust goals during the process, learners might also need support for goal setting at the beginning of their learning since they have limited knowledge on what they will learn. In this case, the present study attempts to implement a new approach to address these concerns.

## Chatbot

In this study, we used a chatbot to facilitate students' course goal-setting at the beginning of their online learning process via conversation. Chatbots are programs developed to engage humans via natural language interaction. Current chatbots are able to interact with users via images, videos, textual, and auditory messages [21]. The common types of chatbots employed in educational environments include open discussion chatbot, intelligent assistant chatbot, and task-oriented chatbot. Open discussion chatbot can interact with students with any topics in order to engage students in a long conversation. For instance, chatbot Elbot enabled students to freely talk about daily life topics including school life and movies [22]. Chatbots as intelligent assistants are designed to serve students by answering students' questions in specific domains. Chatbot CBET was applied to answer students' concerns about educational technology [23]. The task-oriented type refers to a chatbot that performs as a teaching assistant or tutor to provide guidance and instant feedback to help students complete learning tasks, such as writing assessment [24] and accounting practice [25].

Chatbots have shown their beneficial effects on students' learning. Through talking with a chatbot partner to learn a new language, students felt less anxious and more engaged to communicate in the target language [26]. For example, Gada et al [27] used a chatbot to facilitate students' preparedness for a peer group discussion. The results indicated that the chatbot increased the number of students' conversation actions in the discussion activity. A recent research examining the use of a chatbot to scaffold students' online learning indicated that students who learned with the chatbot had higher self-regulated learning levels than students who received self-regulated learning information online [28]. However, the use of chatbots to promote students' SRL skills is still underexplored. In this study, we designed a task-oriented chatbot to support students to complete a goal-setting task for a fully online course.

## Method

### Research Backgroun

Here's the cleaned Markdown:

## Learning Buddy Chatbot Development and Implementation

We developed the Learning Buddy chatbot using Dialogflow, a Google platform for building conversations between chatbots and humans. Three components were required when designing conversations in Dialogflow platform: intents, entities, and responses.

Intents referred to predefined training phrases, which help chatbots understand students' inputs by comparing what students said with the training phrases. For example, the training phrase of the Measurable question "May I know what grade level you want to get in this course? Grade A, B, or C?" were: grade A, grade B, and grade C.

Entities included the predefined synonyms and misspellings of the training phrases. The use of entities helps chatbot understand students' different answers to one question. Responses were teacher's feedback and recommendations on ways to pursue particular learning goals.

The mechanism of the Learning Buddy chatbot was supported by Dialogflow Messenger integration and Moodle system. Dialogflow Messenger integration enabled us to insert the chatbot into the website via embedded HTML code. The Moodle learning management system allows us to add HTML embedded code under the page setting to present the add-in chatbot activity. Therefore, we created an activity page in Moodle and inserted the Dialogflow Messenger code into Moodle's page setting. Through this way, students can click the activity page to start their conversations with chatbot.

### Data Collection and Analysis

After the last session of the course, students were invited to attend a semi-structured interview. A total of 18 participants voluntarily attended our interview and answered our open-ended interview questions related to the chatbot goal-setting activity. Participants were firstly asked to explain how chatbot helped them during the goal setting process. Second, participants were asked to indicate their suggestions or expectations toward future development of chatbots. 

The interviews were recorded and transcribed for further analysis, and the transcripts were coded by two authors. For both questions, a separate coder applied the coding schemes to the data set. The percent of agreement between two raters was 89%, and the disagreements were resolved after discussion.

For the first research question, transcripts were analyzed based on a grounded approach, which aimed to identify the themes in the data set in terms of the research question. For the second research question, we collected students' suggestions of improving the current goal-setting chatbot activity design and expectations of chatbot on supporting other SRL activities. We analyzed the second research question based on SRL framework. A major advance of this framework compared to others in previous SRL studies can be explained below. Nussbaumer et al. defined learning strategies as what to do, while learning techniques as how to perform particular activities.

### SMART Design Framework

| SMART Questions | Choice examples | Rules | Chatbot Recommendation examples |
|----------------|-----------------|-------|--------------------------------|
| Specific | Why do you take this course? | I'll teach adults. | Good to know! Keep the adult learning strategies introduced in this course in mind and reflect them on your own experience. |
| Measurable | May I know what grade level you want to get in this course? | Grade A, B, or C? | Please refer to the recommendations and seek for extra help whenever you feel unconfident |
| Attainable | Can you foresee any difficulties you may have while pursuing your learning goal in this course? | I might have difficulties in understanding or applying the adult learning strategies appropriately in my own study. | Try to engage more in the pre and in-class activities/cases. Those stories and scenarios will help you better understand the concept and relate to real-life situations |
| Relevant | Could you tell me what you want to gain most from this course? | Knowledge of adult learning strategies and how to apply them in my own study. | Then I will advise you to look for more supplemental readings on the strategies that you find appropriate for your learning. |
| Timely | May I know when you plan to complete all the six written assignments? | I might not be able to complete it in time. | Then I

## Student Perceptions of Chatbot Support for Self-Regulated Learning

## Research Question 1: In what ways do students think that chatbot activity helps them in their goal setting process?

To answer the first research question, participants were asked to describe how they think this chatbot activity can help them in setting learning goals. The results suggested two key roles that this activity played in students' goal setting practice: helped students clarify the learning goals, and raised students' awareness of setting learning goals before they actually start to learn.

### Clarify the learning goals
For goals to be effective, students firstly need to have an overview of the proposed learning activities and objectives. Some students came to the class with no idea of what they will learn in the next few weeks, while others might have a rough understanding of some course topics. In this case, this chatbot activity can offer students a general overview of the course by indicating some key learning objectives. Students can find the most appropriate learning goals from the given answers followed by each guiding question. In our interview, students (n=7) indicated that this activity could help them clarify learning goals and plans.

Some students also indicated that the questions proposed in the chatbot helped them visualize the goals they had in mind. Since there is no such conversational goal setting design in other courses, students were either unsure of what they needed to do or had vague ideas about what they want to do before they start to learn. However, in this course, students were asked to set goals by interacting with a chatbot, which may shed light on the direction of their future learning:

"I think it is an interesting setting. It points out a clear direction of my future learning." (Student P)

### Raise awareness
Another key factor that students found chatbot can be helpful is that the conversations could raise their awareness of setting a goal before starting to learn and monitoring the learning progress. In our interview, students (n=6) expressed their general perceptions on how this goal setting activity raised their awareness of the importance of goal setting, a sample response is:

"Chatbot inspires me to remind myself of what I promised myself to do, or what i plan to do and what i aim to do so." (Student N)

Students also indicated that since previously they were not aware of the goal setting process, completing this chatbot activity increases their knowledge on goal setting procedures and the importance of using such strategies in their learning.

## Research Question 2: What are students' expectations towards the future development of chatbot activity?

In response to the second research question, which explored the potential of chatbot for supporting SRL activities, students were firstly asked to give suggestions on how to improve the current goal setting chatbot, and then to indicate any other functions that they expected the chatbot to have in order to support their future learning. Students' responses toward their other expectations of chatbot on SRL were coded based on a model of the SRL ontology proposed by Nussbaumer et al. [9].

### Improvements of current design
Students' responses toward the improvements of current chatbot design can be summarized into three major aspects. Firstly, since the current chatbot focused mainly on supporting goal setting strategy, students only interacted with the chatbot at the beginning of the first session.

Some students (n=5) indicated that they expected the chatbot to show up more during their learning process, with an aim of reminding and assisting them to follow through the goals they set:

"I think if there's a chatbot after every two sessions to help me follow up the goals I set could be better." (Student H)

"I would easily forget what goals I set before. So it's better to remember during the process. It's better to show up more." (Student P)

One student mentioned that the goals provided in chatbot were relatively general. Narrowing down the learning goals or breaking them into specific subgoals can give students better ideas on what to expect and how to plan for their next step.

Finally, the current chatbot design ended with a greeting after students completed the last question. Thus, students (n=3) suggested that there should be a summary of all the selections that students had made, which can be

Here's the cleaned and normalized Markdown:

## Further Expectations of Chatbot on Supporting SRL Activities

Students' responses were coded based on the SRL model introduced in the previous section (Nussbaumer et al., 2014). Overall, most of the students indicated their expectations of implementing chatbot for various learning activities, which demonstrated a great potential of chatbot for supporting SRL from students' perspectives. SRL phases, strategies and the techniques are displayed in Table 2, and in this section we'll use these terms to discuss students' responses by categorizing them in each SRL phase.

In the planning phase, most of the SRL strategies are related to goal setting and time management. The possible techniques that can be adopted to implement these strategies include but are not limited to things like making to-do lists or event calendars to clarify the upcoming learning events. Students (n=2) expected chatbot to have the function of notifying them important timelines and latest news in the learning platforms, so that they can refer to the notifications provided by chatbot to make and adjust their learning plans according to the course progress:

> "It can remind me of my schedules and plans. Since the checklist in Moodle is messy, I'm very likely to miss the new forum or quiz. If chatbot can send me notifications on new tasks, files and deadlines, it can be more helpful." (Student E)

In the searching phase, self-regulated learners are expected to use some resource management strategies such as help seeking. Related SRL techniques include searching for resources and seeking for information and so on. Students (n=5) indicated such expectations of chatbot from two perspectives. Firstly, they wished chatbot would provide them with more academic resources during their experience. Second, some students suggested to include frequently asked questions in chatbot, so that whenever students have general questions about the course, they can directly search or type in the chat. A sample of student's response can be:

> "It could be perfect if we can have a course bot to collect all the questions and strategies used for each session in this course. So the bot can answer students' questions if it is already there." (Student F)

Learning phase refers to the ability of students to organize and elaborate the learning contents. Some common SRL techniques include concept mapping, highlighting and so on. One student mentioned her wish to get help from chatbot by receiving some interpretations of those conceptual knowledge discussed in class. In this course, the final group project requires students to demonstrate their understandings toward some learning strategies in a given scenario. However, these strategies are not fully discussed in class, with an aim of fostering students to explore by themselves. In this case, Student C indicated that chatbot can be helpful in a way of assisting students to develop better understandings of these concepts:

> "It can give us more conceptual interpretations, such as for the content we need to explore in our group teaching demonstration." (Student C)

Last but not least, the final phase of a SRL process is reflecting. Effective strategies include reflecting and regulating the learning activities that have been done, techniques can be used such as self-assessment and reviewing. Students (n=5) indicated their expectations of chatbots related to some of these reflection techniques, and the common idea they conveyed in their responses is that they expected the chatbot to help them review what they have learned during the class, or to check how well they have learned so far.

> "I think the chatbot can help me revise some key points highlighted by the instructor. It can do things like key concepts review." (Student J)

## Discussion

The main purpose of this study is to explore the use of a chatbot to support fully online students' SRL, especially for the goal setting process. We attempt to understand the potential of chatbot for supporting SRL related activities from students' perspectives. Since very limited previous research has been done from this approach, there is little room for us to compare the results we got in this study with others. Thus, we will discuss our results primarily based on the qualitative data we collected from students' interviews in this study.

The first research question focused on how the chatbot activity helped students in their goal

## References

[1] UNESCO. (n.d.). COVID-19 educational disruption and response. https://en.unesco.org/themes/education-emergencies/coronavirus-school-closures

[2] Kizilcec, R. F., Perez-Sanagustin, M., & Maldonado, J. J. (2017). Self-regulated learning strategies predict learner behavior and goal attainment in Massive Open Online Courses. Computers & Education, 104, 18-33. https://doi.org/10.1016.j.compedu.2016.10.00120J.

[3] Hidayah, I., Adji, T. B., & Setiawan, N. A. (2018). A Framework for Improving Recommendation in AdaptiveMetacognitive Scaffolding. In Proceedings of the fourth International Conference on Science and Technology (ICST) (pp. 1-5). IEEE. https://doi.org/10.1109/ICSTC.2018.8528664

[4] Manso-Vazquez, M., & Llamas-Nistal, M. (2015). Proposal of a learning organization tool with support for metacognition. IEEE Revista Iberoamericana de Tecnologias del Aprendizaje, 10(2), 35-42. https://doi.org/10.1109/RITA.2015.2417932

[5] Capuano, N., Mangione, G. R., Pierri, A., & Salerno, S. (2012). Learning Goals Recommendation for Self-Regulated Learning. International Journal of Engineering Education, 28(6), 1373-1379.

[6] Louvigne, S., Kato, Y., Rubens, N., & Ueno, M. (2015). SNS messages recommendation for learning motivation. In: Vol. 9112. Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics) (pp. 237-246). https://doi.org/10.1007/978-3-319-19773-9_2,1

[7] Hew, K., Huang, W., Du, J., & Jia, C. (2021). Using Chatbots in Flipped Learning Online Sessions: Perceived Usefulness and Ease of Use. In Proceedings of the 14th International Conference on Blended Learning (ICBL).

[8] Littlejohn, A., Hood, N., Milligan, C., & Mustain, P. (2016). Learning in MOOCs: Motivations and self-regulated learning in MOOCs. Internet and Higher Education, 29, 40-48. https://doi.org/10.1016/j.iheduc.2015.12.003

[9] Nussbaumer, A., Dahrendorf D., Schmitz, H. C., Kravcik, M., Berthold, M., & Albert, D. (2014). Recommender and guidance strategies for creating personal Mashup learning environments. Computer Science and Information Systems, 11(1), 321-342. doi:10.2298/CSIS121210011N

[10] Shih, K. P., Chen, H. C., Chang, C. Y., & Kao, T. C. (2010). The development and implementation of scaffolding-based self-regulated learning system for e-learning. Educational Technology & Society, 13(1), 80-93.

[11] Lachmann, P., & Kiefel, A. (2012, 4-6 July 2012). Recommending Learning Activities as Strategy for Enabling Self-Regulated Learning. Paper presented at the 2012 IEEE

[29] Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. Psychiatric Quarterly, 3(2), 77-111. https://doi.org/10.1111/j.1460-2466.1978.tb01621.x

[30] Bodily, R., Ikahihifo, T. K., Mackley, B., & Graham, C. R. (2018). The design, development, and implementation of student-facing learning analytics dashboards. Journal of Computing in Higher Education, 30(3), 572-598. https://doi.org/10.1007/s12528-018-9186-0

[31] Wong, J., Baars, M., Davis, D., van Der Zee, T., Houben, G-J, & Paas, F. (2019). Supporting Self-Regulated Learning in Online Learning Environments and MOOCs: A Systematic Review. International Journal of Human-Computer Interaction, 35(4-5), 356-373. https://doi.org/10.1080/10447318.2018.1543084

[32] Zimmerman, B. J. (1989). A Social Cognitive View Of Self-regulated Academic Learning. Journal of Educational Psychology, 81(3), 329-339. doi:10.1037/0022-0663.81.3.329