# Realizing Corrective Feedback in Task-Based Chatbots Engineered for Second Language Learning

# Dongkwang Shin

Gwangju National University of Education, Republic of Korea

# Jang Ho Lee

Chung-Ang University, Republic of Korea

# Wonjun Izac Noh

Unnam Elementary School, Republic of Korea

# Abstract

Building on the work of customized chatbots for language teaching and learning and the secondlanguage acquisition literature on corrective feedback (CF), this article showcases an innovative practice for building a tailored and task-based chatbot to provide CF. Given that extant chatbots are generally not sensitive to learners’ grammatical errors, we illustrate a way to install a CF function by using ‘action and parameters’ and ‘define prompts’ options in the chatbot-building platform known as Google DialogflowTM. Our study, which included upper-grade English-as-a-foreign language learners in South Korea, demonstrated that customized chatbots could offer CF when students made non-target utterances and elicit learner uptake successfully. Based on our innovation, we then provide directions for pedagogy on chatbot-based language learning.

# Keywords

chatbots, corrective feedback, Google DialogflowTM, task-based chatbot, English-as-a-foreign language

# Introduction

The recent advances in artificial intelligence have opened new doors for language teaching and learning through the use of conversational chatbots (Fryer et al., 2020; Lee et al., 2020). However, despite their potential to provide unlimited practice opportunities, extant chatbots such as Amazon’s Alexa and Apple’s Siri may be limited in terms of their applicability to second language (L2) classrooms, because their programming does not allow them to carry out tasks relevant to L2 teaching and learning, and to provide appropriate linguistic feedback on learners’ output. This article aims to address this gap by presenting an innovative approach to building customized, task-based chatbots that can provide corrective feedback (CF) to L2 learners.

Recent reviews (e.g., Fryer et al., 2020; Huang et al., 2022; Kohnke et al., 2023; Lee et al., 2020) have highlighted the merits of using chatbots in language teaching and learning, while some researchers have employed Google DialogflowTM to create tailored chatbots for language teaching and learning (e.g., Kim et al., 2022; Kohnke, 2023). One notable instance of a language learning chatbot is ‘Ellie’ (Kim et al., 2022), which differs from extant chatbots in that its developers first determine the target linguistic functions and expressions (e.g., persuading and asking) and relevant contexts (e.g., arranging for a time to meet with friends). With this chatbot, learners can engage in ‘goal-oriented and meaning-focused cognition activities’ (Kim et al., 2022, p. 9) and practise the target linguistic functions and expressions in meaningful situations. However, this type of chatbot is also limited like the extant ones in that it cannot offer CF on students’ output. That is, the user could achieve the task goal with the chatbot, even when their output contained grammatical errors. As Figure 1 illustrates, the chatbot does not provide feedback on the user’s output, including grammatical errors (e.g., ‘She is 16 year_ old now’).

Given that CF plays a crucial role in L2 learning by helping learners to notice their errors and produce repaired output (e.g., Long, 1996; Mackey, 2006), it seems crucial to equip customized chatbots with the ability to provide CF to enhance their pedagogical benefits. In response to this need, our article shares an innovative practice for building task-based and customized chatbots capable of providing CF. With such an approach, L2 learners could receive valuable opportunities to receive linguistic feedback on their ungrammatical output from chatbots and repair their errors in subsequent turns.

# The Teaching Context

The teaching context of this innovative practice was the upper-grade English classes in a South Korean public elementary school. The teacher of the sampled students has been building and employing his chatbots, which he had been using as supplementary language practice tools for his English lessons for fifth-graders and sixth-graders. Thus, he engineered these chatbots to engage the learners with tasks involving various linguistic functions and expressions in upper-grade English curricula.

![](img/602c69fd502dc6613b0d56aba7d59b023e2173b0cdcd7bb8c104e5e08183ade2.jpg)  
Figure 1. The sample conversation log between the chatbot (agent) and learner.

In total, 24 fifth-grade and sixth-grade English-as-a-foreign language (EFL) learners in his classes, aged 11 to 12, participated in this practice. The participants’ English proficiency was pre-intermediate, and they had received about 187 and $^ { 2 8 9 \mathrm { h } }$ of English instruction, respectively, by the time of the study. The students had been using chatbots built by their teacher such that the teacher and students first went over a dialogue in the speaking section of their textbook, and the students individually talked to the chatbot specifically built to enable learners to practise the dialogue (as a follow-up task). The students underwent the same procedure for the current innovative practice (i.e., review the textbook and then talk to the chatbot to practise the dialogue). They then had opportunities to talk to the chatbot, equipped with a ‘CF’ function.

# Reason for the Innovation

The innovation came from the above-mentioned teacher’s concerns about his students English accuracy during chatbot-based language practices. Although his students were in favour of such type of practices overall, he noticed that several students frequently made grammatical errors when responding to the chatbots. The problem was that the students could achieve the target goal when engaged in chatbot-based tasks, despite their errors, because the chatbots were likely to respond as long as the user’s output contained the relevant keywords. Given that these chatbots could not provide CF on learners’ errors, the teacher believed the students’ errors might become fossilized. Thus, the teacher employed the current innovative practice to address this problem.

For the current innovative practice, the teacher and researchers selected two dialogues from the textbook, which respectively included common errors that his previous students had frequently made (see Table 1). He built a chatbot for each dialogue, with which the students could engage in a follow-up practice activity after being exposed to the textbook dialogue.

# Description of the Innovation

This study used Google’s free chatbot builder, DialogflowTM ES, to develop two chatbots that enabled learners to engage in two different chatbot-based tasks based on the dialogues extracted from the students’ English textbook. DialogflowTM is a scenario-based chatbot builder. Its advantage is that it is easy to develop a chatbot by basically typing each conversion turn into an input field called ‘Intent.’ In addition, it instantly generates the Uniform Resource Locator, which provides an environment like practising conversations on a social networking service. The development manual for the DialogflowTM-based chatbot is available at https://m.cafe.daum.net/sdhera/G3Jv/134.

Table 1. Target forms, students’ common errors and target feedback.   

<html><body><table><tr><td></td><td>Target forms</td><td>Students&#x27; errors</td><td>Target feedback (to be given by the chatbot)</td></tr><tr><td>Task I</td><td>(someone is) ...13 years old.</td><td>...I 3 year old</td><td>year or years?</td></tr><tr><td>Task 2</td><td>I&#x27;d like (something) There is a bed</td><td>I like... There is bed</td><td>I&#x27;d like...? a...?</td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td>(something is)...in the living room.</td><td>...on the living room</td><td>on or in?</td></tr><tr><td></td><td></td><td></td><td></td></tr></table></body></html>

In the free version of DialogflowTM, the learner’s input can be voice or text, but the chatbot’s utterances are only in text. Also, even if the learner speaks in voice on the dialogue screen, it is presented as text through speech recognition. Therefore, in this study, the students engaged in each chatbot-based task twice, the first by responding to the chatbot in text and then by responding in voice. Of course, the chatbot’s speech and feedback are different from actual voice conversations because they are text-based, but considering that the participants were in the lower grades, it was easier for them to recognize errors through text feedback. Even when they tried to speak, they could see their utterances in the text, so if there was a mispronunciation, they could recognize it and correct it in subsequent turns.

# Development and Implementation of the Innovation

This section illustrates the overall procedure regarding developing and implementing the current innovation (see Figure 2 for the overall procedure).

# Selecting Target Dialogues and Entering Dialogues in DialogflowTM

For the present study, the previously mentioned teacher and the researchers selected two dialogues from the textbook to develop two chatbots. The first dialogue (i.e., Task 1) consisted of ordering food and making plans, and the second dialogue (i.e., Task 2) involved asking and answering questions about the structure of a house and its furniture. Once we selected the dialogues, we entered them in DialogflowTM, illustrated in Except 1.

In Task 1, learners interacted with the chatbot to solve two sub-tasks: ordering a meal based on a given menu; and setting up a date to play a game with a friend. First, to develop the first chatbot with DialogflowTM, we wrote a dialogue scenario for learning the target expressions (i.e., I am (number) years old, I would like (something)), as follows (see Figure 3 for Task 1’s dialogue flow).

Excerpt 1   

<html><body><table><tr><td>AI</td><td>Hi</td></tr><tr><td>BI</td><td>Hi! My name is Tony. What is your name?.</td></tr><tr><td>A2</td><td>My name is Peter.  Peter-link-@sys.person</td></tr><tr><td>B2</td><td>Hello, $person. Nice to meet you. How old are you?</td></tr><tr><td>A3</td><td>I am 13 years old.  13-link-@sys.number, years-link-@age</td></tr><tr><td>B3</td><td>Oh, you are $number years old. We are the same age. Good to see you! Are you ready to start?</td></tr><tr><td>A4</td><td>Yes!</td></tr><tr><td>B4</td><td>Alright. Let&#x27;s have lunch. What do you want to eat?</td></tr><tr><td>A5</td><td>I&#x27;d like spaghetti.  Spaghetti-link-@food ...</td></tr></table></body></html>

![](img/7216f80f4f5fc3bdba00089e0e824ad7436a236d568bf5769df82f4f7288c7b4.jpg)  
Figure 2. The flowchart of the development and implementation of the innovation.

In Excerpt 1, we assume A is a user (i.e., a student) and B is a chatbot. As such, we entered A’s utterances in Training Phrases in DialogflowTM Application Programming Interface and B’s utterances in Text Response in the function ‘Intents.’ ‘Intent’ is where one enters a dialogue scene with a single conversation turn (i.e., one $\mathbf { A } + \mathbf { B }$ set); this constitutes one ‘intent.’ It is better to enter as many diverse expressions for the same meaning as possible because doing so could increase the chatbot’s ability to comprehend the user’s utterances. If the learner greets the chatbot in the Welcome Intent, it will ask for the user’s name (B1 in Excerpt 1), then the teacher could identify the student’s name in DialogflowTM’s History to see who engaged in the task. Thus, by dragging the name of any particular learner (e.g., Peter in A2) in Training Phrases of Intents, we could link it to DialogflowTM’s built-in entity, called $@$ sys.person. In so doing, the chatbot can recognize all users’ names. If one enters ‘\$person’ in the chatbot’s subsequent response (e.g., \$person in B2), then the chatbot can say the name (e.g., Peter) during the conversation.

We could engage learners with practising specific expressions, like a substitution drill, by creating a pool of the same type of words (e.g., ‘food’) in the function ‘Entities.’ Then, by dragging a target expression (e.g., Spaghetti in A5), the chatbot would link the word to the target entity name (e.g., $@$ food).

![](img/dc302254a0e13689ec3184752337f3f676af687c7afe3fce318e2316f320cf57.jpg)  
Figure 3. Task 1 dialogue flow.

# Entering Feedback and Pilot Testing

When entering dialogues in DialogflowTM, we considered the expected errors (see Table 1), and we entered target and non-target expressions in Training Phrases so that the chatbot could provide feedback on the students’ erroneous expressions. For example, look at the sentence ‘I am 13 years old’ in A3 in Excerpt 1. Our experience with the upper-grade Korean EFL students suggested that they often made the error of saying year instead of years. Anticipating this error, we thus created an Entity called ‘age’ and entered only the correct expression years into this word pool. We then entered the target (i.e., grammatical) sentence, ‘I am 13 years old,’ and the non-target (i.e., ungrammatical) sentence, ‘I am 13 year old,’ into Training Phrases, as shown in Figure 4. In the correct sentence, we linked the word years to $@$ age, representing the entity ‘age.’

As shown in Figure 4, there is a link between the number (13) and $@$ sys.number and a link between years and $@$ age, so it is possible to check the entities associated with the expression in the ‘action and parameters’ function in Figure 5. In addition, we have set $@$ age as the default condition by selecting ‘required;’ thus, if the student utters a different expression, such as year instead of the required expression years, the chatbot will randomly present one of the expressions (e.g., year or years?, years!, or $I$ am 13 years old.) entered in the ‘define prompts.’

![](img/278b6e629a8c9e7d94fd5eb9ae1bc3a34d919b89b98a29f44aa50fd97b3f1670.jpg)  
Figure 4. Entering target expressions and expected learner utterances in training phrases.

![](img/519fbbb36a88ca6c017722166b9f82c0b966bc682a446cacf2eb52eacdabbbe6.jpg)  
Figure 5. The interface of the ‘action and parameters’ menu in dialogflowTM.

Figure 6 shows how the chatbot related to Task 1 provided feedback on the non-target expression and how the dialogue moved forward again when the learner repaired the error and reformulated the correct expression.

After developing the initial version of the chatbots, the teacher and researchers piloted them, especially regarding whether they could provide CF properly when the user gave utterances, including the target errors.

# The Implementation of the Chatbot-Based Tasks and Participant Survey

Regarding the implementation of the chatbot-based tasks, the homeroom teacher led the overall procedure, and we followed ethical guidelines, including parental and student consent. The class where the study was conducted was a computer laboratory.

The students first learned the dialogue from the textbook and then engaged in the chatbot-based task as a follow-up activity. As mentioned above, the students engaged in each chatbot-based task twice, the first by responding to the chatbot in text and then by responding in voice.

We conducted Task 1 and Task 2 one week apart. After completing Task 2, we surveyed the students about their perception of chatbot-based tasks. The survey consisted of questions on whether chatbots helped develop their speaking and pronunciation and reviewed previous materials, the extent to which they felt comfortable (or nervous), and the open-ended questions on: (a) what they liked (or did not like) about the chatbotbased tasks; and (b) why they wished (or did not wish to) continue talking to the chatbot.

![](img/899d7aebcfbc4e59d9707ddeae4a8e6d116925714c42e891991213c6158605ea.jpg)  
Figure 6. The sample dialogue between the conversational agent and the learner.

# Evaluation of the Innovation

The investigation into the dialogues between the students and the chatbot revealed that the students could repair their utterances, including the target grammatical errors. This repair was possible because they could not progress in the task without fixing their errors (i.e., the chatbot would keep offering CF). For example, Excerpt 2 relays the dialogues between the learners and the chatbot built for Task 2, in which the learners practised the expressions related to the existence and location of a particular item. In Excert 2, after the greeting, the chatbot asked Student#8 about the type of furniture in her room, to which she responded with a grammatically well-formed utterance. However, in the next response, Student#8 omitted the indefinite article, ‘There is bed,’ one of the target expressions. During her next turn, the chatbot gave a metalinguistic clue for the article (i.e., ‘a . . . ?’), thereby encouraging Student#8 to repair her previous phrasing. The chatbot’s CF resulted in learner uptake, which was also the correct reformulation of her last utterance that had contained a grammatical error. Only after such a revision could she move on in the dialogue.

Excerpt 2   

<html><body><table><tr><td>Chatbot</td><td>Hello! My name is Tony. What&#x27;s your name?</td></tr><tr><td>Student#8</td><td>My name is Chloe.</td></tr><tr><td>Chatbot</td><td>Nice to meet you, Chloe. Are you ready to start?</td></tr><tr><td>Student#8</td><td>Yes.</td></tr><tr><td>Chatbot</td><td>Great. What is in your room?.</td></tr><tr><td>Student#8</td><td>There is a desk..</td></tr><tr><td>Chatbot</td><td>Anything else? Tell me &#x27;No&#x27; if you are finished.</td></tr><tr><td>Student#8</td><td>There is bed.</td></tr><tr><td>Chatbot</td><td>A...?</td></tr><tr><td>Student#8</td><td>There is a bed.</td></tr></table></body></html>

According to the results of the survey, the chatbot-based tasks were overall wellaccepted by the students. For example, the students were in favour of such activities in terms of reviewing previously learned English phrases (Q1; mean $( M ) = 3 . 9 2 $ ) and developing their speaking ability (Q4; $M = 3 . 9 6$ ) and pronunciation (Q5; $M = 3 . 7 1$ ). Indeed, in response to the open-ended question about what they liked about the chatbot-based tasks, some students $( n = 6 )$ mentioned that it helped them to improve their pronunciation and boost their confidence in speaking. Some of the comments on this topic were as follows:

I think my pronunciation has improved a lot after the [chatbot-based] activities. (Student #9)

I feel more confident speaking in English now. (Student #14)

Some students $( n = 7 )$ also enjoyed the chatbot-based tasks because they were ‘not embarrassed to make mistakes when talking to the chatbot’ $( n = 7 )$ .

In addition, the students generally felt comfortable talking to the chatbot (Q2; $\begin{array} { r } { M { = } 3 . 7 5 } \end{array}$ ) rather than nervous (Q3; $M { = } 2 . 1 7$ ). For instance, in the open-ended question about why they wanted to continue talking to the chatbot, several students mentioned that they liked talking to the chatbot ‘because it was like talking to [my] friends’ $( n = 5 )$ . Meanwhile, regarding why they did not want to continue talking to the chatbot, about a third of students $( n = 8 )$ said they were annoyed when the chatbot did not comprehend what they were saying. However, we believe such a moment may have pushed the students to revise their grammar and pronunciation to make their utterances more comprehensible.

# Future Pedagogical Directions

This article showcased an innovative practice for building customized chatbots with a CF function, in light of the second-language acquisition literature on CF (e.g., Li and Vuono, 2019; Lyster and Ranta, 1997; Lyster and Saito, 2010). The evaluation of our customized chatbots demonstrated that the chatbots indeed provided CF properly when upper-grade EFL learners produced non-target utterances. We also found that learners could respond to such feedback with uptake by repairing the errors made in their previous utterances. Finally, the chatbot-based tasks were generally well received by the students.

Based on our practice, we suggest the following three pedagogical directions. First, teachers can use the customized chatbot in the speaking activity for practising textbook dialogues1 . Such an activity with the chatbot could be administered individually or in a group, depending on the availability of resources. In this process, students would receive some grammar feedback related to the phrases contained in the target dialogue from the chatbot. Second, educators could build chatbots designed to perform the same task by using DialogflowTM or accessing $\mathrm { P O E } ^ { 2 }$ (https://poe.com), but each equipped with different types of CF. They could also investigate which type of chatbot CF works best for their students. For example, it may be the case that more explicit types of feedback, such as metalinguistic feedback and explicit correction, are more effective for a particular age group than recasts, which are reformulations of students’ utterances but with errors corrected. Third, L2 teachers can develop customized chatbots for their purposes and share them in online teacher communities. DialogflowTM has a feature called Export that allows one to save the code used to create a chatbot in a portable format and share it with others. Labelling your custom chatbots with target language functions and grammar (e.g., persuasion/use of the modal verb ‘should’) would be very useful for this purpose.

Recently, a conversational articial intelligence called ChatGPT has received substantial attention, and researchers consider it a possible substitute for existing chatbots (see Kohnke et al., 2023 for review). However, ChatGPT’s design is to provide information and perform tasks according to the input prompt, so it is limited in its application to language education based on everyday English usage (Lee et al., 2020) . Therefore, we argue that chatbots with CF functionality, such as the one introduced in this article, will still be helpful for language learning.

# Author’s Note

Wonjun Izac Noh is also affiliated with Massey University, New Zealand.

# Funding

The authors received no financial support for the research, authorship, and/or publication of this article.

# Conflict of Interests

The authors have no conflict of interests to declare.

# ORCID iDs

Dongkwang Shin $\textcircled{1}$ https://orcid.org/0000-0002-5583-0189   
Jang Ho Lee $\textcircled{1}$ https://orcid.org/0000-0003-2767-3881   
Wonjun Izac Noh $\textcircled{1}$ https://orcid.org/0000-0002-4020-8143

# Notes

1. An example of this type of chatbot could be accessed at: https://bot.dialogflow.com/94994dbe764e-42f8-9171-99c7b2576590/   
2. POE is a website that provides access to chatbots such as GPT-4, gpt-3.5-turbo and Claude, and has a chatbot creation feature for people without any programming knowledge.

# References

Fryer L, Coniam D, Carpenter R, et al. (2020) Bots for language learning now: current and future directions. Language Learning & Technology 24(2): 8–22.   
Huang W, Hew KF and Fryer LK (2022) Chatbots for language learning—are they really useful? A systematic review of chatbot-supported language learning. Journal of Computer Assisted Learning 38(1): 237–257.   
Kim H, Yang H, Shin D, et al. (2022) Design principles and architecture of a second language learning chatbot. Language Learning & Technology 26(1): 1–18.   
Kohnke L (2023) A pedagogical chatbot: A supplemental language learning tool. RELC Journal 54(3): 828–838.   
Kohnke L, Moorhouse BL and Zou D (2023) ChatGPT for language teaching and learning. RELC Journal 54(2): 537–550.   
Lee JH, Yang H, Shin D, et al. (2020) Chatbots. ELT Journal 74(3): 338–344.   
Li S and Vuono A (2019) Twenty-five years of research on oral and written corrective feedback in system. System 84(1): 93–109.   
Long MH (1996) The role of the linguistic environment in second language acquisition. In: Ritchie W and Bhatia T (eds) Handbook of second language acquisition. New York, NY: Academic Press, 413–468.   
Lyster R and Ranta L (1997) Corrective feedback and learner uptake. Studies in Second Language Acquisition 19(1): 37–66.   
Lyster R and Saito K (2010) Oral feedback in classroom SLA: a meta-analysis. Studies in Second Language Acquisition 32(2): 265–302.   
Mackey A (2006) Feedback, noticing and instructed second language learning. Applied Linguistics 27(3): 405–430.

# Author Biographies

received his PhD in Applied Linguistics from Victoria University of Wellington Dongkwang Shinand is currently a professor at Gwangju National University of Education, Republic of Korea. His research interests include corpus linguistics, CALL, and AI-based language learning.

received his DPhil in education from the University of Oxford, and is presently a proJang Ho Leefessor at Chung-Ang University, Republic of Korea. His areas of interest are CALL, L1 use in L2 teaching, and vocabulary acquisition. All correspondence regarding this publication should be addressed to him.

is currently a doctoral student at Institute of Education, Massey University of Wonjun Izac NohNew Zealand. His research interests include CALL and AI-based language learning.