---
authors:
- Mohammad Amin Kuhail
- Nazik Alturki
- Salwa Alramlawi
- Kholood Alhejori
category: review
confidence_score: 0.8
document_type: journal
has_abstract: true
has_methodology: true
has_results: true
key_findings:
- Chatbots were mainly designed on a web platform to teach computer science, language,
  general education, and a few other fields
- More than half of the chatbots were used as teaching agents, while more than a third
  were peer agents
- Most of the chatbots used a predetermined conversational path, and more than a quarter
  utilized a personalized learning approach
- More than a third of the chatbots were evaluated with experiments, and the results
  primarily point to improved learning and subjective satisfaction
- Challenges and limitations include inadequate or insufficient dataset training and
  a lack of reliance on usability heuristics
methodology: quantitative
pedagogical_confidence: 1.0
pedagogical_implications: true
publication_year: 2022
research_questions: []
source_file: Interacting with educational chatbots A systematic review.clean.md
subject_area: education
tags:
- Chatbot
- Conversational Agent
- Educational Bot
- Literature Review
- Interaction Styles
- Human-Computer Interaction
title: 'Interacting with educational chatbots: A systematic review'
---

Here's the cleaned Markdown:

# Interacting with educational chatbots: A systematic review

Mohammad Amin Kuhail, Nazik Alturki, Salwa Alramlawi, Kholood Alhejori

https://doi.org/10.1007/s10639-022-11177-3

## Abstract

Chatbots hold the promise of revolutionizing education by engaging learners, personalizing learning activities, supporting educators, and developing deep insight into learners' behavior. However, there is a lack of studies that analyze the recent evidence-based chatbot-learner interaction design techniques applied in education. This study presents a systematic review of 36 papers to understand, compare, and reflect on recent attempts to utilize chatbots in education using seven dimensions: educational field, platform, design principles, the role of chatbots, interaction styles, evidence, and limitations. The results show that the chatbots were mainly designed on a web platform to teach computer science, language, general education, and a few other fields such as engineering and mathematics. Further, more than half of the chatbots were used as teaching agents, while more than a third were peer agents. Most of the chatbots used a predetermined conversational path, and more than a quarter utilized a personalized learning approach that catered to students' learning needs, while other chatbots used experiential and collaborative learning besides other design principles. Moreover, more than a third of the chatbots were evaluated with experiments, and the results primarily point to improved learning and subjective satisfaction. Challenges and limitations include inadequate or insufficient dataset training and a lack of reliance on usability heuristics. Future studies should explore the effect of chatbot personality and localization on subjective satisfaction and learning effectiveness.

**Keywords**: Chatbot, Conversational Agent, Educational Bot, Literature Review, Interaction Styles, Human-Computer Interaction

## Introduction

Chatbots, also known as conversational agents, enable the interaction of humans with computers through natural language, by applying the technology of natural language processing (NLP) (Bradeško & Mladenić, 2012). Due to their ability to emulate human conversations and thus automate services and reduce effort, chatbots are increasingly becoming popular in several domains, including healthcare (Oh et al., 2017), consumer services (Xu et al., 2017), education (Anghelescu & Nicolaescu, 2018), and academic advising (Alkhoori et al., 2020). In fact, the size of the chatbot market worldwide is expected to be 1.23 billion dollars in 2025 (Kaczorowska-Spychalska, 2019). In the US alone, the chatbot industry was valued at 113 million US dollars and is expected to reach 994.5 million US dollars in 2024.

The adoption of educational chatbots is on the rise due to their ability to provide a cost-effective method to engage students and provide a personalized learning experience (Benotti et al., 2018). Chatbot adoption is especially crucial in online classes that include many students where individual support from educators to students is challenging (Winkler & Söllner, 2018). Chatbots can facilitate learning within the educational context, for instance by instantaneously providing students with course content (Cunningham-Nelson et al., 2019), assignments (Ismail & Ade-Ibijola, 2019), rehearsal questions (Sinha et al., 2020), and study resources (Mabunda, 2020). Moreover, chatbots may interact with students individually (Hobert & Meyer von Wolff, 2019) or support collaborative learning activities (Chaudhuri et al., 2009; Tegos et al., 2014; Kumar & Rose, 2010; Stahl, 2006; Walker et al., 2011). Chatbot interaction is achieved by applying text, speech, graphics, haptics, gestures, and other modes of communication to assist

Here's the cleaned Markdown:

## Background

(Okonkwo & Ade-Ibijola, 2021). Nonetheless, the existing review studies have not concentrated on the chatbot interaction type and style, the principles used to design the chatbots, and the evidence for using chatbots in an educational setting.

Given the magnitude of research on educational chatbots, there is a need for a systematic literature review that sheds light on several vital dimensions: field of application, platform, role in education, interaction style, design principles, empirical evidence, and limitations.

By systematically analyzing 36 articles presenting educational chatbots representing various interaction styles and design approaches, this study contributes:
1. an in-depth analysis of the learner-chatbot interaction approaches and styles currently used to improve the learning process
2. a characterization of the design principles used for the development of educational chatbots
3. an in-depth explanation of the empirical evidence used to back up the validity of the chatbots
4. the discussion of current challenges and future research directions specific to educational chatbots

This study will help the education and human-computer interaction community aiming at designing and evaluating educational chatbots. Potential future chatbots might adopt some ideas from the chatbots surveyed in this study while addressing the discussed challenges and considering the suggested future research directions.

This study is structured as follows: In Section 2, we present background information about chatbots, while Section 3 discusses the related work. Section 4 explains the applied methodology, while Section 5 presents the study's findings. Section 6 presents the discussion and future research directions. Finally, we present the conclusion and the study's limitations in Section 7.

## Background

Chatbots have existed for more than half a century. Prominent examples include ELIZA, ALICE, and SmarterChild. ELIZA, the first chatbot, was developed by Weizenbaum (1966). The chatbot used pattern matching to emulate a psychotherapist conversing with a human patient. ALICE was a chatbot developed in the mid-1990s. It used Artificial Intelligence Markup Language (AIML) to identify an accurate response to user input using knowledge records (AbuShawar and Atwell, 2015). Another example is Smart Child (Chukhno et al., 2019), which preceded today's modern virtual chatbot-based assistants such as Alexa and Siri, which are available on messaging applications with the ability to emulate conversations with quick data access to services.

Chatbots have been utilized in education as conversational pedagogical agents since the early 1970s (Laurillard, 2013). Pedagogical agents, also known as intelligent tutoring systems, are virtual characters that guide users in learning environments (Seel, 2011). Conversational Pedagogical Agents (CPA) are a subgroup of pedagogical agents. They are characterized by engaging learners in a dialog-based conversation using AI (Gulz et al., 2011). The design of CPAs must consider social, emotional, cognitive, and pedagogical aspects (Gulz et al., 2011; King, 2002).

A conversational agent can hold a discussion with students in a variety of ways, ranging from spoken (Wik & Hjalmarsson, 2009) to text-based (Chaudhuri et al., 2009) to nonverbal (Wik & Hjalmarsson, 2009; Ruttkay & Pelachaud, 2006). Similarly, the agent's visual appearance can be human-like or cartoonish, static or animated, two-dimensional or three-dimensional (Dehn & Van Mulken, 2000). Conversational agents have been developed over the last decade to serve a variety of pedagogical roles, such as tutors, coaches, and learning companions (Haake & Gulz, 2009). Furthermore, conversational agents have been used to meet a variety of educational needs such as

Here's the cleaned Markdown:

keyboard, whereas voice-based agents allow talking via a mic. Voice-based chatbots are more accessible to older adults and some special-need people (Brewer et al., 2018). An embodied chatbot has a physical body, usually in the form of a human, or a cartoon animal (Serenko et al., 2007), allowing them to exhibit facial expressions and emotions.

Concerning the platform, chatbots can be deployed via messaging apps such as Telegram, Facebook Messenger, and Slack (Car et al., 2020), standalone web or phone applications, or integrated into smart devices such as television sets.

## Related work

Recently several studies reviewed chatbots in education. The studies examined various areas of interest concerning educational chatbots, such as the field of application (Smutny & Schreiberova, 2020; Wollny et al., 2021; Hwang & Chang, 2021), objectives and learning experience (Winkler & Söllner, 2018; Cunningham-Nelson et al., 2019; Pérez et al., 2020; Wollny et al., 2021; Hwang & Chang, 2021), how chatbots are applied (Winkler & Söllner, 2018; Cunningham-Nelson et al., 2019; Wollny et al., 2021), design approaches (Winkler & Söllner, 2018; Martha & Santoso, 2019; Hwang & Chang, 2021), the technology used (Pérez et al., 2020), evaluation methods used (Pérez et al., 2020; Hwang & Chang, 2021; Hobert & Meyer von Wolff, 2019), and challenges in using educational chatbots (Okonkwo & Ade-Ibijola, 2021). Table 1 summarizes the areas that the studies explored.

Winkler and Söllner (2018) reviewed 80 articles to analyze recent trends in educational chatbots. The authors found that chatbots are used for health and well-being advocacy, language learning, and self-advocacy. Chatbots are either flow-based or powered by AI, concerning approaches to their designs.

Several studies have found that educational chatbots improve students' learning experience. For instance, Okonkwo and Ade-Ibijola (2021) found out that chatbots motivate students, keep them engaged, and grant them immediate assistance, particularly online. Additionally, Wollny et al. (2021) argued that educational chatbots make education more available and easily accessible.

Concerning how they are applied, Cunningham-Nelson et al. (2019) identified two main applications: answering frequently-asked questions (FAQ) and performing short quizzes, while Wollny et al. (2021) listed three other applications, including scaffolding, activity recommendations, and informing them about activities.

In terms of the design of educational chatbots, Martha and Santoso (2019) found out that the role and appearance of the chatbot are crucial elements in designing the educational chatbots, while Winkler and Söllner (2018) identified various types of approaches to designing educational chatbots such as flow and AI-based, in addition to chatbots with speech recognition capabilities.

Pérez et al. (2020) identified various technologies used to implement chatbots such as Dialogflow, FreeLing (Padró and Stanilovsky, 2012), and ChatFuel. The study investigated the effect of the technologies used on performance and quality of chatbots.

Hobert and Meyer von Wolff (2019), Pérez et al. (2020), and Hwang and Chang (2021) examined the evaluation methods used to assess the effectiveness of educational chatbots. The authors identified that several evaluation methods such as surveys, experiments,

Here's the cleaned Markdown:

## Comparison between this work and relevant studies

| Reference | Field of Application | Platform | Educational Role | Interaction Style | Design Principles | Evaluation | Limitations |
|-----------|---------------------|-----------|-----------------|------------------|------------------|------------|------------|
| (Winkler & Söllner, 2018) | ✓ | - | - | Partial | Partial | - | - |
| (Hobert & Meyer von Wolff, 2019) | - | - | - | - | - | Partial | - |
| (Martha & Santoso, 2019) | - | - | - | - | Partial | - | - |
| (Cunningham-Nelson et al., 2019) | - | - | - | Partial | - | - | - |
| (Pérez et al., 2020) | - | - | Partial | - | - | ✓ | ✓ |
| (Smutny & Schreiberova, 2020) | ✓ | - | Partial | - | - | ✓ | - |
| (Wollny et al., 2021) | ✓ | - | ✓ | - | Partial | - | - |
| (Okonkwo & Ade-Ibijola, 2021) | - | - | Partial | - | - | - | Partial |
| (Hwang & Chang, 2021) | ✓ | - | - | - | - | Partial | - |
| This study | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

In terms of who is in control of the conversation, i.e., the chatbot or the user. As such, we classify the interactions as either chatbot or user-driven.

Only a few studies partially tackled the principles guiding the design of the chatbots. For instance, Martha and Santoso (2019) discussed one aspect of the design (the chatbot's visual appearance). This study focuses on the conceptual principles that led to the chatbot's design.

In terms of the evaluation methods used to establish the validity of the articles, two related studies (Pérez et al., 2020; Smutny & Schreiberova, 2020) discussed the evaluation methods in some detail. However, this study contributes more comprehensive evaluation details such as the number of participants, statistical values, findings, etc.

Regarding limitations, Pérez et al. (2020) examined the technological limitations that have an effect on the quality of the educational chatbots, while Okonkwo and Ade-Ibijola (2021) presented some challenges and limitations facing educational chatbots such as ethical, technical, and maintenance matters. While the identified limitations are relevant, this study identifies limitations from other perspectives such as the design of the chatbots and the student experience with the educational chatbots. To sum up, Table 2 shows some gaps that this study aims at bridging to reflect on educational chatbots in the literature.

## Methodology

The literature related to chatbots in education was analyzed, providing a background for new approaches and methods, and identifying directions for further research. This study follows the guidelines described by Keele et al. (2007). The process includes these main steps: (1) defining the review protocol, including the research questions, how to answer them, search strategy, and inclusion and exclusion criteria. (2) running the study by selecting the articles, assessing their quality, and synthesizing the results. (3) reporting the findings.

### Research questions

Based on the shortcomings of the existing related literature review studies, we formulated seven main research questions:

RQ1 - In what fields are the educational chatbots used?
RQ2 - What platforms do the educational chatb

Here's the cleaned Markdown:

## The Search Process

The search string was defined using the Boolean operators as follows:
('Chatbot' OR 'Conversational Agent' OR 'Pedagogical Agent') AND ('Education' OR 'Learning' OR 'Learner' OR 'Teaching' OR 'Teacher' OR 'Student')

According to their relevance to our research questions, we evaluated the found articles using the inclusion and exclusion criteria provided in Table 3. The inclusion and exclusion criteria allowed us to reduce the number of articles unrelated to our research questions. Further, we excluded tutorials, technical reports, posters, and Ph.D. thesis since they are not peer-reviewed.

After defining the criteria, our search query was performed in the selected databases to begin the inclusion and exclusion process. Initially, the total of studies resulting from the databases was 1208 studies. The metadata of the studies containing; title, abstract, type of article (conference, journal, short paper), language, and keywords were extracted in a file format (e.g., bib file format). Subsequently, it was imported into the Rayyan tool[^1], which allowed for reviewing, including, excluding, and filtering the articles collaboratively by the authors.

The four authors were involved in the process of selecting the articles. To maintain consistency amongst our decisions and inter-rater reliability, the authors worked in two pairs allowing each author to cross-check the selection and elimination of the author they were paired with. The process of selecting the articles was carried out in these stages:

1. Reading the articles' metadata and applying the inclusion criteria of IC-1 and the exclusion criteria of EC-1. As a result, the number of studies was reduced to 1101.
2. As a first-round, we applied the inclusion criterion IC-2 by reading the studies' title, abstract, and keywords. Additionally, the EC-2 exclusion criterion was applied in the same stage. As a result, only 197 studies remained.
3. In this stage, we eliminated the articles that were not relevant to any of our research questions and applied the EC-3 criteria. As a result, the articles were reduced to 71 papers.
4. Finally, we carefully read the entire content of the articles having in mind IC-3. Additionally, we excluded studies that had no or little empirical evidence for their effectiveness of the educational chatbot (EC-4 criterion). As a result, the articles were reduced to 36 papers.

Figure 1 shows the flowchart of the selecting processes, in which the final stage of the selection resulted in 36 papers.

## Results

Figure 2 shows the number and types of articles plotted against time. 63.88% (23) of the selected articles are conference papers, while 36.11% (13) were published in journals. Most conference papers were published after 2017. Interestingly, 38.46% (5) of the journal articles were published recently in 2020. Concerning the publication venues, two journal articles were published in the Journal of IEEE Transactions on Learning Technologies (TLT), which covers various topics such as innovative online learning systems, intelligent tutors, educational software applications and games, and simulation systems for education. Intriguingly, one article was published in Computers in Human Behavior journal. The remaining journal articles were published in several venues such as IEEE Transactions on Affective Computing, Journal of Educational Psychology, International Journal of Human-Computer Studies, ACM Transactions on Interactive Intelligent System. Most of these journals are ranked Q1 or Q2 according to Scimago Journal and Country Rank[^2].

Figure 3 shows the geographical mapping of the selected articles. The total sum of the articles per country in Fig. 3 is more than 36 (the number of selected articles) as the authors of a single article could work in institutions located in different countries. The vast majority of selected articles were written or co-written by researchers from American universities. However, the research that emerged from all European universities combined was the highest in the number of articles (19 articles).

## Educational Chatbots: A Systematic Review

## RQ1: What fields are the educational chatbots used in?

Recently, chatbots have been utilized in various fields (Ramesh et al., 2017). Most importantly, chatbots played a critical role in the education field, in which most researchers (12 articles; 33.33%) developed chatbots used to teach computer science topics. For example, some chatbots were used as tutors for teaching programming languages such as Java (Coronado et al., 2018; Daud et al., 2020) and Python (Winkler et al., 2020), while other researchers proposed educational chatbots for computer networks (Clarizia et al., 2018; Lee et al., 2020), databases (Latham et al., 2011; Ondáš et al., 2019), and compilers (Griol et al., 2011).

Ten (27.77%) articles presented general-purpose educational chatbots that were used in various educational contexts such as online courses (Song et al., 2017; Benedetto & Cremonesi, 2019; Tegos et al., 2020). The approach authors use often relies on a general knowledge base not tied to a specific field.

In comparison, chatbots used to teach languages received less attention from the community (6 articles; 16.66%). Interestingly, researchers used a variety of interactive media such as voice (Ayedoun et al., 2017; Ruan et al., 2021), video (Griol et al., 2014), and speech recognition (Ayedoun et al., 2017; Ruan et al., 2019).

A few other subjects were targeted by the educational chatbots, such as engineering (Mendez et al., 2020), religious education (Alobaidi et al., 2013), psychology (Hayashi, 2013), and mathematics (Rodrigo et al., 2012).

## RQ2: What platforms do the proposed chatbots operate on?

Most researchers (25 articles; 69.44%) developed chatbots that operate on the web. The web-based chatbots were created for various educational purposes. For example, KEMTbot (Ondáš et al., 2019) is a chatbot system that provides information about the department, its staff, and their offices. Other chatbots acted as intelligent tutoring systems, such as Oscar (Latham et al., 2011), used for teaching computer science topics. Moreover, other web-based chatbots such as EnglishBot (Ruan et al., 2021) help students learn a foreign language.

Six (16.66%) articles presented educational chatbots that exclusively operate on a mobile platform (e.g., phone, tablet). The articles were published recently in 2019 and 2020. The mobile-based chatbots were used for various purposes. Examples include Rexy (Benedetto & Cremonesi, 2019), which helps students enroll in courses.

[Table content preserved but formatted for clarity]

Here's the cleaned and normalized Markdown:

## Overview of Educational Chatbot Platforms and Roles

### Platforms

Table 5: Overview of the platforms the chatbots operate on

| Chatbot platform | Number of Articles | Article(s) |
|-----------------|-------------------|------------|
| Web | 25 | (Griol et al., 2011; Latham et al., 2011; Griol et al., 2014; Rodrigo et al., 2012; Alobaidi et al., 2013; Zedadra et al., 2014; Tegos et al., 2015; Ayedoun et al., 2017; Fryer et al., 2017; Song et al., 2017; Clarizia et al., 2018; Coronado et al., 2018; Schouten et al., 2017; Verleger & Pembridge, 2018; da Silva Oliveira et al., 2019; Ondáš et al., 2019; Ruan et al., 2019; Janati et al., 2020; Lee et al., 2020; Law et al., 2020; Tegos et al., 2020; Villegas-Ch et al., 2020; Winkler et al., 2020; Ruan et al., 2021; Wambsganss et al., 2021) |
| Mobile | 6 | (Benedetto & Cremonesi, 2019; Daud et al., 2020; Mellado-Silva et al., 2020; Mendez et al., 2020; Qin et al., 2020; Wambsganss et al., 2020) |
| Desktop | 5 | (D'mello & Graesser, 2013; Redondo-Hernández & Pérez-Marín, 2011; Matsuda et al., 2013; Benotti et al., 2017; Hayashi, 2013) |

Most chatbots were web-based, likely because web-based applications are operating system independent and do not require downloading, installing, or updating. Mobile-based chatbots are increasing in popularity as users increasingly prefer mobile applications. According to an App Annie report, users spent 120 billion dollars on application stores.

### Roles of Educational Chatbots

Table 6: Overview of the roles of chatbots when interacting with students

| Chatbot Role | Number of Articles | Article(s) |
|--------------|-------------------|------------|
| Teaching Agent | 20 | (Latham et al., 2011; D'mello & Graesser, 2013; Redondo-Hernández & Pérez-Marín, 2011; Alobaidi et al., 2013; Griol et al., 2014; Zedadra et al., 2014; Ayedoun et al., 2017; Benotti et al., 2017; Song et al., 2017; Coronado et al., 2018; Ondáš et al., 2019; Ruan et al., 2019; Mellado-Silva et al., 2020; Qin et al., 2020; Villegas-Ch et al., 2020; Winkler et al., 2020; Ruan et al., 2021; Wambsganss et al., 2021; Wambsganss et al., 2020; Rodrigo et al., 2012) |
| Peer Agent | 13 | (Griol et al., 2011; Tegos et al., 2015; Fryer et al., 2017; Clarizia et al., 2018;

## Chatbot Interaction Types and Agents in Education

The teaching agents employed various approaches to engage with students. Some instructed students to watch educational videos (Qin et al., 2020) followed by discussion, while others initiated conversations by prompting reflection on past learning (Song et al., 2017). Several studies explored scenario-based teaching approaches (Latham et al., 2011; D'mello & Graesser, 2013), where agents mimicked tutors by presenting scenarios for discussion. Other implementations focused on formative assessment through multiple-choice questions (Rodrigo et al., 2012; Griol et al., 2014; Mellado-Silva et al., 2020; Wambsganss et al., 2020).

Teaching agents used diverse engagement techniques, including:
- Storytelling-style discussions (Alobaidi et al., 2013; Ruan et al., 2019)
- Empathetic phrases like "uha" to show interest (Ayedoun et al., 2017)
- Adaptive feedback systems (Wambsganss et al., 2021)

### Peer Agents
Peer agent chatbots typically provided on-demand assistance:
- Term and concept lookups (Clarizia et al., 2018; Lee et al., 2020)
- Q&A database interactions (Verleger & Pembridge, 2018; da Silva Oliveira et al., 2019; Mendez et al., 2020)
- Technology usage guidance (Janati et al., 2020)
- Group discussion scaffolding (Tegos et al., 2015; Tegos et al., 2020; Hayashi, 2013)

Only one peer agent (Fryer et al., 2017) enabled free-style conversation, particularly useful for language learning.

### Teachable Agents
Two studies examined teachable agent chatbots:
- Mathematical equation solving guidance (Matsuda et al., 2013)
- Classification task teaching in groups or individually (Law et al., 2020)

### Motivational Agents
Two studies featured motivational agents:
- Question-based interaction with emotional responses (D'mello & Graesser, 2013)
- Emotional reactions and encouraging phrases (Schouten et al., 2017)

### Interaction Styles

| Interaction Style | Number of Articles | Article(s) |
|------------------|-------------------|------------|
| Chatbot-driven conversation: Flow based | 19 | (Griol et al., 2011; Latham et al., 2011; Redondo-Hernández & Pérez-Marín, 2011; Rodrigo et al., 2012; Alobaidi et al., 2013; Matsuda et al., 2013; Zedadra et al., 2014; Wambsganss et al., 2020; D'mello & Graesser, 2013; Daud et al., 2020; Griol et al., 2014; Ayedoun et al., 2017; Hayashi, 2013; Coronado et al., 2018; Schouten et al., 2017; Ruan et al., 2019; Law et al., 2020; Winkler et al., 2020; Wambsganss et al., 2021) |
| Intent based | 13 | (Benotti et al., 2017; Song et al., 2017; Clarizia et al., 2018; Verleger & Pembridge, 2018; da Silva Oliveira et al., 2019; Ondáš et al., 2019; Janati et al., 2020; Lee et al., 2020; Mellado-Silva et al.,

Here's the cleaned Markdown:

## RQ4 – What are the interaction styles supported by the educational chatbots?

As shown in Table 7 and Fig. 7, most of the articles (88.88%) used the chatbot-driven interaction style where the chatbot controls the conversation. 52.77% of the articles used flow-based chatbots where the user had to follow a specific learning path predetermined by the chatbot. Notable examples are explained in (Rodrigo et al., 2012; Griol et al., 2014), where the authors presented a chatbot that asks students questions and provides them with options to choose from. Other authors, such as (Daud et al., 2020), used a slightly different approach where the chatbot guides the learners to select the topic they would like to learn. Subsequently, the assessment of specific topics is presented where the user is expected to fill out values, and the chatbot responds with feedback. The level of the assessment becomes more challenging as the student makes progress. A slightly different interaction is explained in (Winkler et al., 2020), where the chatbot challenges the students with a question. If they answer incorrectly, they are explained why the answer is incorrect and then get asked a scaffolding question.

The remaining articles (13 articles; 36.11%) present chatbot-driven chatbots that used an intent-based approach. The idea is the chatbot matches what the user says with a premade response. The matching could be done using pattern matching as discussed in (Benotti et al., 2017; Clarizia et al., 2018) or simply by relying on a specific conversational tool such as Dialogflow as in (Mendez et al., 2020; Lee et al., 2020; Ondáš et al., 2019).

Only four (11.11%) articles used chatbots that engage in user-driven conversations where the user controls the conversation and the chatbot does not have a premade response. For example, the authors in (Fryer et al., 2017) used Cleverbot, a chatbot designed to learn from its past conversations with humans. The authors used Cleverbot for foreign language education. User-driven chatbots fit language learning as students may benefit from an unguided conversation. The authors in (Ruan et al., 2021) used a similar approach where students freely speak a foreign language. The chatbot assesses the quality of the transcribed text and provides constructive feedback. In comparison, the authors in (Tegos et al., 2020) rely on a slightly different approach where the students chat together about a specific programming concept. The chatbot intervenes to evoke curiosity or draw students' attention to an interesting, related idea.

## RQ5 – What are the principles used to guide the design of the educational chatbots?

Various design principles, including pedagogical ones, have been used in the selected studies (Table 8, Fig. 8). We discuss examples of how each of the principles was applied.

- **Personalized Learning**: The ability to tailor chatbots to the individual user may help meet students' needs (Clarizia et al., 2018). Many studies claim that students learn better when the chatbot is represented by a personalized method rather than a non-personalized one (Kester et al., 2005). From our selected studies, ten (27.77%) studies have applied personalized learning principles. For instance, the study in (Coronado et al., 2018) designed a chatbot to teach Java. The students' learning process is monitored by collecting information on all interactions between the students and the chatbot. Thus, direct and customized instruction and feedback are provided to students. Another notable example can be found in (Latham et al., 2011), where students were given a learning path.

Here's the cleaned Markdown:

## Learning Approaches and Pedagogical Techniques

- **Personalized Learning**: Students received 12% more accurate answers with chatbots providing personalized learning materials. Villegas-Ch et al. (2020) demonstrated AI-based activity recommendations based on students' needs and learning paths, with chatbots evaluating weaknesses to enable personalized learning.

- **Experiential Learning**: Utilizes reflection on experience for knowledge construction through environmental interaction (Felicia, 2011). Song et al. (2017) describe reflection support through chatbot questioning. D'mello and Graesser (2013) present constructivist experiential learning where embodied chatbots mimic human tutors' conversational movements.

- **Social Dialog**: Also called small talk, manages social situations rather than content exchange (Klüwer, 2011). Wambsganss et al. (2021) implemented casual chat modes for jokes and fun facts. Qin et al. (2020) suggested using social phrases showing interest and presence.

- **Collaborative Learning**: Involves group-based problem-solving, improving knowledge and critical thinking (Tegos et al., 2015). Techniques include:
  - Animated Conversational Agents (ACA) for Computer-Supported Collaborative Learning (Zedadra et al., 2014)
  - Open-ended pair discussions (Tegos et al., 2020)
  - MentorChat: cloud-based CSCL for dialog-based activities (Tegos et al., 2015)

- **Affective Learning**: Provides empathetic feedback to maintain learning engagement (Ayedoun et al., 2017). Examples include:
  - Various feedback types: congratulatory, encouraging, sympathetic, reassuring
  - Emotion categorization for low-literate learners (Schouten et al., 2017)

- **Learning by Teaching**: Students learn through generating explanations (Chase et al., 2009). Implemented in:
  - Chatbots learning from students' answers (Matsuda et al., 2013)
  - Teachable agents using question templates (Law et al., 2020)

- **Scaffolding**: Provides temporary support for student comprehension (West et al., 2017; Maybin et al., 1992). Example implementation includes Sara chatbot offering voice and text-based scaffolds for programming tasks (Winkler et al., 2020).

## Empirical Evidence Assessment

Researchers used multiple evaluation methods to assess chatbot effectiveness:

1. Experiment: Scientific tests under controlled conditions (Cook et al., 2002)
2. Evaluation study: Tests for specific parameter insights (Payne and Payne, 2004)
3. Questionnaire
4. Focus group

Here's the cleaned and normalized Markdown:

## An overview of the applied empirical evaluation methods

Table 9: An overview of the applied empirical evaluation methods

| Empirical evaluation | Number of Articles | Article(s) |
|---------------------|-------------------|------------|
| Experiment | 13 | (Matsuda et al., 2013; Tegos et al., 2015; Benotti et al., 2017; Coronado et al., 2018; Schouten et al., 2017; Fryer et al., 2017; Mellado-Silva et al., 2020; Tegos et al., 2020; Winkler et al., 2020; Ruan et al., 2021; Wambsganss et al., 2021; Hayashi, 2013; Rodrigo et al., 2012) |
| Evaluation Study | 10 | (D'mello & Graesser, 2013; Redondo-Hernández & Pérez-Marín, 2011; Alobaidi et al., 2013; Ayedoun et al., 2017; Ruan et al., 2019; Janati et al., 2020; Villegas-Ch et al., 2020; Law et al., 2020; Song et al., 2017; Latham et al., 2011) |
| Questionnaire | 10 | (Griol et al., 2011; Griol et al., 2014; Zedadra et al., 2014; Clarizia et al., 2018; Benedetto & Cremonesi, 2019; Ondáš et al., 2019; Daud et al., 2020; Qin et al., 2020; Wambsganss et al., 2020; da Silva Oliveira et al., 2019) |
| Focus group | 3 | (Verleger & Pembridge, 2018; Lee et al., 2020; Mendez et al., 2020) |

A questionnaire is a data collection method for evaluation that focuses on a specific set of questions (Mellenbergh & Adèr, 2008). These questions aim to extract information from participants' answers. It can be carried on by mail, telephone, face-to-face interview, and online using the web or email. A focus group allows researchers to evaluate a small group or sample that represents the community (Morgan, 1996). The idea behind the focus group is to examine some characteristics or behaviors of a sample when it's difficult to examine all groups.

Table 9 and Fig. 9 show the various evaluation methods used by the articles. Most articles (13; 36.11%) used an experiment to establish the validity of the used approach, while 10 articles (27.77%) used an evaluation study to validate the usefulness and usability of their approach. The remaining articles used a questionnaire (10; 27.7%) and a focus group (3; 8.22%) as their evaluation methods.

### Experiments

Table 10 shows the details of the experiments the surveyed studies had used. Eight articles produced statistically significant results pointing to improved learning when using educational chatbots compared to a traditional learning setting, while a few other articles pointed to improved engagement, interest in learning, as well as subjective satisfaction.

A notable example of a conducted experiment includes the one discussed in (Wambsganss et al., 2021). The experiment evaluated whether adaptive tutoring implemented via the chatbot helps students write more convincing texts. The author designed two groups: a treatment group and a control group. The result showed that students using the chatbot (treatment group) to conduct a writing exercise wrote more convincing texts with a better formal argumentation quality than the traditional approach (control group). Another example is the experiment conducted by the authors in (Benotti et al.,

Here's the cleaned Markdown:

### Tasks and Learning Assessment

The experiment assessed the students' learning by a post-test. Comparing the treatment group (students who interacted with the chatbot) with a control group (students in a traditional setting), the students in the control group have improved their learning and gained more interest in learning. Another study (Hayashi, 2013) evaluated the effect of text and audio-based suggestions of a chatbot used for formative assessment. The result shows that students receiving text and audio-based suggestions have improved learning.

Despite most studies showing overwhelming evidence for improved learning and engagement, one study (Fryer et al., 2017) found that students' interest in communicating with the chatbot significantly declined in an 8-week longitudinal study where a chatbot was used to teach English.

### Evaluation Studies

In general, the studies conducting evaluation studies involved asking participants to take a test after being involved in an activity with the chatbot. The results of the evaluation studies (Table 12) point to various findings such as increased motivation, learning, task completeness, and high subjective satisfaction and engagement.

As an example of an evaluation study, the researchers in (Ruan et al., 2019) assessed students' reactions and behavior while using 'BookBuddy,' a chatbot that helps students read books. The participants were five 6-year-old children. The researchers recorded the facial expressions of the participants using webcams. It turned out that the students were engaged more than half of the time while using BookBuddy.

Another interesting study was the one presented in (Law et al., 2020), where the authors explored how fourth and fifth-grade students interacted with a chatbot to teach it about several topics such as science and history. The students appreciated that the robot was attentive, curious, and eager to learn.

### Questionnaires

Studies that used questionnaires as a form of evaluation assessed subjective satisfaction, perceived usefulness, and perceived usability, apart from one study that assessed perceived learning (Table 11). Assessing students' perception of learning and usability is expected as questionnaires ultimately assess participants' subjective opinions, and thus, they don't objectively measure metrics such as students' learning.

While using questionnaires as an evaluation method, the studies identified high subjective satisfaction, usefulness, and perceived usability. The questionnaires used mostly Likert scale closed-ended questions, but a few questionnaires also used open-ended questions.

A notable example of a study using questionnaires is 'Rexy,' a configurable educational chatbot discussed in (Benedetto & Cremonesi, 2019). The authors designed a questionnaire to assess Rexy. The questionnaires elicited feedback from participants and mainly evaluated the effectiveness and usefulness of learning with Rexy. The results largely point to high perceived usefulness. However, a few participants pointed out that it was sufficient for them to learn with a human partner. One student indicated a lack of trust in a chatbot.

| Article | Chatbot Approach | No. of participants | Findings |
|---------|------------------|-------------------|-----------|
| (Griol et al., 2011) | Peer Agent, Chatbot driven | 15 | High subjective satisfaction |
| (Griol et al., 2014) | Teaching Agent, Chatbot driven | 25 | High ease of learning and subjective satisfaction |
| (Zedadra et al., 2014) | Teaching Agent, Chatbot driven | 39 | High subjective satisfaction |
| (Clarizia et al., 2018) | Peer agent, chatbot driven | 167 | High usability |
| (Benedetto & Cremonesi, 2019) | Peer agent, chatbot driven | 40 | High usefulness |
| (da Silva Oliveira et al., 2019) | Peer agent, chatbot driven | 12 | High subjective satisfaction |
| (Ondáš et al., 2019) |

Here's the cleaned Markdown:

Another example is the study presented in (Ondáš et al., 2019), where the authors evaluated various aspects of a chatbot used in the education process, including helpfulness, whether users wanted more features in the chatbot, and subjective satisfaction. The students found the tool helpful and efficient, albeit they wanted more features such as more information about courses and departments. About 62.5% of the students said they would use the chatbot again. In comparison, 88% of the students in (Daud et al., 2020) found the tool highly useful.

### Focus group

Only three articles were evaluated by the focus group method. Only one study pointed to high usefulness and subjective satisfaction (Lee et al., 2020), while the others reported low to moderate subjective satisfaction (Table 13). For instance, the chatbot presented in (Lee et al., 2020) aims to increase learning effectiveness by allowing students to ask questions related to the course materials. The authors invited 10 undergraduate students to evaluate the chatbot. It turned out that most of the participants agreed that the chatbot is a valuable educational tool that facilitates real-time problem solving and provides a quick recap on course material. The study mentioned in (Mendez et al., 2020) conducted two focus groups to evaluate the efficacy of chatbot used for academic advising. While students were largely satisfied with the answers given by the chatbot, they thought it lacked personalization and the human touch of real academic advisors. Finally, the chatbot discussed by (Verleger & Pembridge, 2018) was built upon a Q&A database related to a programming course. Nevertheless, because the tool did not produce answers to some questions, some students decided to abandon it and instead use standard search engines to find answers.

### RQ7: What are the challenges and limitations of using proposed chatbots?

Several challenges and limitations that hinder the use of chatbots were identified in the selected studies, which are summarized in Table 14 and listed as follow:

- **Insufficient or Inadequate Dataset Training**: The most recurring limitation in several studies is that the chatbots are either trained with a limited dataset or, even worse, incorrectly trained. Learners using chatbots with a limited dataset experienced difficulties learning as the chatbot could not answer their questions. As a result, they became frustrated (Winkler et al., 2020) and could not wholly engage in the learning process (Verleger & Pembridge, 2018; Qin et al., 2020). Another example that caused learner frustration is reported in (Qin et al., 2020), where the chatbot gave incorrect responses.

  To combat the issues arising from inadequate training datasets, authors such as (Ruan et al., 2021) trained their chatbot using standard English language examination materials (e.g., IELTS and TOEFL). The evaluation suggests an improved engagement. Further, Song et al. (2017) argue that the use of Natural Language Processing (NLP) supports a more natural conversation instead of one that relies on a limited dataset and a rule-based mechanism.

- **User-centered design**: User-centered design (UCD) refers to the active involvement of users in several stages of the software cycle, including requirements gathering, iterative design, and evaluation (Dwivedi et al., 2012). The ultimate goal of UCD is to ensure software usability. One of the challenges mentioned in a couple of studies is the lack of student involvement in the design process.

[Tables 12, 13, and 14 preserved as in original]

## Educational Chatbots: A Systematic Review

## Discussion and Future Research Directions

The purpose of this work was to conduct a systematic review of educational chatbots to understand their fields of applications, platforms, interaction styles, design principles, empirical evidence, and limitations.

Seven general research questions were formulated in reference to the objectives:

### Fields of Application (RQ1)
The results show that the surveyed chatbots were used to teach several fields. More than a third of the chatbots were developed to teach computer science topics, including programming languages and networks. Fewer chatbots targeted foreign language education, while slightly less than a third of the studies used general-purpose educational chatbots. These findings align with Wollny et al. (2021) and Hwang and Chang (2021), although both review studies reported language learning as the most targeted educational topic, followed by computer programming. Other reviews like Winkler & Söllner (2018) highlighted chatbots' use in health, well-being, and self-advocacy education.

### Platforms (RQ2)
Most surveyed chatbots operate on web-based platforms, followed by mobile and desktop platforms. The web offers versatility as multiple devices can access it without installation requirements. While some reviews (Cunningham-Nelson et al., 2019; Pérez et al., 2020) focused on development tools rather than platforms, they noted popular tools including Dialogflow, QnA Maker, and ChatFuel. These tools generally allow for both web and mobile deployment. Notably, Winkler and Söllner (2018) found mobile platforms popular for medical education chatbots.

### Chatbot Roles (RQ3)
- More than half served as teaching agents, recommending educational content or engaging students in topical discussions
- About one-third acted as peer agents, providing help with term definitions, FAQs, and discussion scaffolding
- Two chatbots functioned as motivational agents, offering empathetic and encouraging feedback
- Two operated as teachable agents, where students gradually taught the chatbots

### Interaction Styles (RQ4)
Most chatbots used chatbot-driven conversations, with the chatbot controlling the interaction. Some used predetermined paths, while others used intent-triggered responses. Few chatbots allowed for user-driven conversations where users could initiate and lead the interaction. Previous reviews noted that such user-driven chatbots typically rely on AI algorithms (Winkler & Söllner, 2018).

### Limitations

- Personality traits may affect how students perceive learning with chatbots (Law et al., 2020)
- Interest tends to decline over time, suggesting a novelty effect (Fryer et al., 2017)
- Lack of feedback mechanisms can negatively impact success (Villegas-Ch et al., 2020)
- External links and popups can distract from learning (Qin et al., 2020)

Here's the cleaned Markdown:

## Research Questions 5-7 and Design Considerations

### RQ5: Design Principles

Personalized learning is a common approach where the learning content is recommended, and instruction and feedback are tailored based on students' performance and learning styles. Most related review studies did not refer to personalized learning as a design principle, but some review studies such as (Cunningham-Nelson et al., 2019) indicated that some educational chatbots provided individualized responses to students.

Scaffolding has also been used in some chatbots where students are provided gradual guidance to help them become independent learners. Scaffolding chatbots can help when needed, for instance, when students are working on a challenging task. Other review studies such as (Wollny et al., 2021) also revealed that some chatbots scaffolded students' discussions to help their learning.

Other surveyed chatbots supported collaborative learning by advising the students to work together on tasks or by engaging a group of students in a conversation. A related review study (Winkler & Söllner, 2018) highlighted that chatbots could be used to support collaborative learning.

The remaining surveyed chatbots engaged students in various methods such as social dialog, affective learning, learning by teaching, and experiential learning. However, none of the related review studies indicated such design principles behind educational chatbots.

A few surveyed chatbots have used social dialog to engage students. For instance, some chatbots engaged students with small talk and showed interest and social presence. Other chatbots used affective learning in the form of sympathetic and reassuring feedback to support learners in problematic situations. Additionally, learning by teaching was also used by two chatbots where the chatbot acted as a student and asked the chatbot for answers and examples. Further, a surveyed chatbot used experiential learning by asking students to develop explanations to problems gradually.

### RQ6: Empirical Evidence

Most surveyed chatbots were evaluated with experiments that largely proved with statistical significance that chatbots could improve learning and student satisfaction. A related review study (Hwang & Chang, 2021) indicated that many studies used experiments to substantiate the validity of chatbots. However, no discussion of findings was reported.

Some of the surveyed chatbots used evaluation studies to assess the effect of chatbots on perceived usefulness and subjective satisfaction. The results are in favor of the chatbots. A related review study (Hobert & Meyer von Wolff, 2019) mentioned that qualitative studies using pre/post surveys were used. However, no discussion of findings was reported.

Questionnaires were also used by some surveyed chatbots indicating perceived subjective satisfaction, ease of learning, and usefulness. Intriguingly, a review study (Pérez et al., 2020) suggested that questionnaires were the most common method of evaluation of chatbots. Such questionnaires pointed to high user satisfaction and no failure on the chatbot's part.

Finally, only this study reported using focus groups as an evaluation method. Only three chatbots were evaluated with this method with a low number of participants, and the results showed usefulness, reasonable subjective satisfaction, and lack of training.

### RQ7: Challenges and Limitations

A frequently reported challenge was a lack of dataset training which caused frustration and learning difficulties. A review study (Pérez et al., 2020) hinted at a similar issue by shedding light on the complex task of collecting data to train the chatbots.

Two surveyed studies also noticed the novelty effect. Students seem to lose interest in talking to chatbots over time. A similar concern was reported by a related review study (Pérez et al., 2020).

Other limitations not highlighted by related review studies include the lack of user-centered design, the lack of feedback, and distractions. In general, the surveyed chatbots were not designed with the involvement of students in the process. Further, one surveyed chatbot did not assess the students' knowledge, which may have

## Design Considerations

- For instance, Alobaidi et al. (2013) used contrast to capture user attention, while Ayedoun et al. (2017) designed their chatbot with subjective satisfaction in mind. Further, Song et al. (2017) involved the users in their design employing participatory design, while Clarizia et al. (2018) ensured that the chatbot design is consistent with existing popular chatbots. Similarly, Villegas-Ch et al. (2020) developed the user interface of their chatbot to be similar to that of Facebook messenger.

Nevertheless, we argue that it is crucial to design educational chatbots with usability principles in mind explicitly. Further, we recommend that future educators test for the chatbot's impact on learning or student engagement and assess the usability of the chatbots.

### Chatbot Personality 

Personality describes consistent and characteristic patterns of behavior, emotions, and cognition (Smestad and Volden, 2018). Research suggests that users treat chatbots as if they were humans (Chaves & Gerosa, 2021), and thus chatbots are increasingly built to have a personality. In fact, researchers have also used the Big Five model to explain the personalities a chatbot can have when interacting with users (Völkel & Kaya, 2021; McCrae & Costa, 2008). 

Existing studies experimented with various chatbot personalities such as agreeable, neutral, and disagreeable (Völkel & Kaya, 2021). An agreeable chatbot uses family-oriented words such as "family" or "together" (Hirsh et al., 2009), words that are regarded as positive emotionally such as "like" or "nice" (Hirsh et al., 2009), words indicating assurance such as "sure" (Nass et al., 1994), as well as certain emojis (Völkel et al., 2019), as suggested by the literature. On the other hand, a disagreeable chatbot does not show interest in the user and might be critical and uncooperative (Andrist et al., 2015).

Other personalities have also been attributed to chatbots, such as casual and formal personalities, where a formal chatbot uses a standardized language with proper grammar and punctuation, whereas a casual chatbot includes everyday, informal language (Andrist et al., 2015; Cafaro et al., 2016).

Despite the interest in chatbot personalities as a topic, most of the reviewed studies shied away from considering chatbot personality in their design. A few studies, such as (Coronado et al., 2018; Janati et al., 2020; Qin et al., 2020; Wambsganss et al., 2021), integrated social dialog into the design of the chatbot. However, the intention of the chatbots primarily focused on the learning process rather than the chatbot personality. We argue that future studies should shed light on how chatbot personality could affect learning and subjective satisfaction.

### Chatbot Localization and Acceptance 

Human societies' social behavior and conventions, as well as the individuals' views, knowledge, laws, rituals, practices, and values, are all influenced by culture. It is described as the underlying values, beliefs, philosophy, and methods of interacting that contribute to a person's unique psychological and social environment. Shin et al. (2022) defines culture as the common models of behaviors and interactions, cognitive frameworks, and perceptual awareness gained via socialization in a cross-cultural environment. 

The acceptance of chatbots involves a cultural dimension. The cultural and social circumstances in which the chatbot is used influence how students interpret the chatbot and how they consume and engage with it. For example, the study by (Rodrigo et al., 2012) shows evidence that the chatbot 'Scooter' was regarded and interacted with differently in the Philippines than in the United States. According to student gaming behavior in the Philippines, Scooter's

## Conclusion

This study described how several educational chatbot approaches empower learners across various domains. The study analyzed 36 educational chatbots proposed in the literature. To analyze the tools, the study assessed each chatbot within seven dimensions: educational field, platform, educational role, interaction style, design principles, empirical principles, and challenges as well as limitations.

The results show that the chatbots were proposed in various areas, including mainly computer science, language, general education, and a few other fields such as engineering and mathematics. Most chatbots are accessible via a web platform, and fewer chatbots were available on mobile and desktop platforms. This choice can be explained by the flexibility the web platform offers as it potentially supports multiple devices, including laptops, mobile phones, etc.

In terms of the educational role, slightly more than half of the studies used teaching agents, while 13 studies (36.11%) used peer agents. Only two studies presented a teachable agent, and another two studies presented a motivational agent. Teaching agents gave students tutorials or asked them to watch videos with follow-up discussions. Peer agents allowed students to ask for help on demand, for instance, by looking terms up, while teachable agents initiated the conversation with a simple topic, then asked the students questions to learn. Motivational agents reacted to the students' learning with various emotions, including empathy and approval.

In terms of the interaction style, the vast majority of the chatbots used a chatbot-driven style, with about half of the chatbots using a flow-based with a predetermined specific learning path, and 36.11% of the chatbots using an intent-based approach. Only four chatbots (11.11%) used a user-driven style where the user was in control of the conversation. A user-driven interaction was mainly utilized for chatbots teaching a foreign language.

Concerning the design principles behind the chatbots, slightly less than a third of the chatbots used personalized learning, which tailored the educational content based on learning weaknesses, style, and needs. Other chatbots used experiential learning (13.88%), social dialog (11.11%), collaborative learning (11.11%), affective learning (5.55%), learning by teaching (5.55%), and scaffolding (2.77%).

Concerning the evaluation methods used to establish the validity of the approach, slightly more than a third of the chatbots used experiment with mostly significant results. The remaining chatbots were evaluated with evaluation studies (27.77%), questionnaires (27.77%), and focus groups (8.33%). The findings point to improved learning, high usefulness, and subjective satisfaction.

Some studies mentioned limitations such as inadequate or insufficient dataset training, lack of user-centered design, students losing interest in the chatbot over time, and some distractions.

There are several challenges to be addressed by future research. None of the articles explicitly relied on usability heuristics and guidelines in designing the chatbots, though some authors stressed a few usability principles such as consistency and subjective satisfaction. Further, none of the articles discussed or assessed a distinct personality of the chatbots though research shows that chatbot personality affects users' subjective satisfaction.

Future studies should explore chatbot localization, where a chatbot is customized based on the culture and context it is used in. Moreover, researchers should explore devising frameworks for designing and developing educational chatbots to guide educators to build usable and effective chatbots. Finally, researchers should explore EUD tools that allow non-programmer educators to design and develop educational chatbots to facilitate the development of educational chatbots. Adopting EUD tools to build chatbots would accelerate the adoption of the technology in various fields.

## Study Limitations

We established some limitations that may affect this study. We restricted our research to the period January 2011 to April 2021. This limitation was necessary to allow us to practically begin the analysis of articles, which took several months. We potentially missed other interesting articles that could be valuable for this study at the date of submission.

We conducted our search using four digital libraries: ACM, Scopus, IEEE Xplore,

## Funding

No funding was received to assist with the preparation of this manuscript.

The authors have no relevant financial or non-financial interests to disclose.

## Data Availability Statement

The datasets generated during and/or analyzed during the current study are available from the corresponding author on reasonable request.

## Open Access

This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.

## References

1. AbuShawar, B., & Atwell, E. (2015). Alice chatbot: Trials and outputs. Computación y Sistemas, 19(4), 625–632.
2. Baylor, A.L (2011). The design of motivational agents and avatars. Educational Technology Research and Development, 59(2), 291–300.
3. Benotti, L., Martnez, M.C., & Schapachnik, F. (2017). A tool for introducing computer science with automatic formative assessment. IEEE Transactions on Learning Technologies, 11(2), 179–192.
4. Benotti, L., Martnez, M.C., & Schapachnik, F. (2018). A tool for introducing computer science with automatic formative assessment. IEEE Transactions on Learning Technologies, 11(2), 179–192. https://doi.org/10.1109/TLT.2017.2682084
5. Cafaro, A., Vilhjálmsson, H.H., & Bickmore, T. (2016). First impressions in human–agent virtual encounters. ACM Transactions on Computer-Human Interaction (TOCHI), 23(4), 1–40.
6. Car, L.T., Dhinagaran, D.A., Kyaw, B.M., Kowatsch, T., Joty, S., Theng, Y.-L., & Atun, R. (2020). Conversational agents in health care: scoping review and conceptual analysis. Journal of medical Internet research, 22(8), e17158.
7. Chase, C.C, Chin, D.B, Oppezzo, M.A, & Schwartz, D.L (2009). Teachable agents and the protégé effect: Increasing the effort towards learning. Journal of Science Education and Technology, 18(4), 334–352.
8. Chaves, A.P., & Gerosa, M.A. (2021). How should my chatbot interact? a survey on social characteristics in human–chatbot interaction design. International Journal of Human–Computer Interaction, 37(8), 729–758.
9. Chou, C.-Y., & Zou, N.-B. (2020). An analysis of internal and external feedback in self-regulated learning activities mediated by self-regulated learning tools and open learner models. International Journal of Educational Technology in Higher Education, 17(1), 1–27.
10. Cook, T.D, Campbell, D.T., & Shadish, W. (2002). Experimental and quasi-experimental designs for generalized causal inference. MA: Houghton Mifflin Boston.
11. Coronado, M., Iglesias, C.A., Carrera,

## References

D'mello, S., & Graesser, A. (2013). Autotutor and affective autotutor: Learning by talking with cognitively and emotionally intelligent computers that talk back. ACM Transactions on Interactive Intelligent Systems (TiiS), 2(4), 1–39.

Dwivedi, M., Upadhyay, M.S., & Tripathi, A. (2012). A working framework for the user-centered design approach and a survey of the available methods. International Journal of Scientific and Research Publications, 2(4), 12–19.

Fryer, L.K, Ainley, M., Thompson, A., Gibson, A., & Sherlock, Z. (2017). Stimulating and sustaining interest in a language course: An experimental comparison of chatbot and human task partners. Computers in Human Behavior, 75, 461–468.

Haake, M., & Gulz, A. (2009). A look at the roles of look & roles in embodied pedagogical agents–a user preference perspective. International Journal of Artificial Intelligence in Education, 19(1), 39–71.

Hattie, J., & Timperley, H. (2007). The power of feedback. Review of Educational Research, 77(1), 81–112.

Hirsh, J.B, DeYoung, C.G, & Peterson, J.B (2009). Metatraits of the big five differentially predict engagement and restraint of behavior. Journal of Personality, 77(4), 1085–1102.

Kester, L., Kirschner, P.A, & Van Merriënboer, J.J. (2005). The management of cognitive load during complex cognitive skill acquisition by means of computer-simulated problem solving. British Journal of Educational Psychology, 75(1), 71–85.

King, F.B (2002). A virtual student: Not an ordinary joe. The Internet and Higher Education, 5(2), 157–166.

Kulik, J.A, & Fletcher, J.D. (2016). Effectiveness of intelligent tutoring systems: a meta-analytic review. Review of Educational Research, 86(1), 42–78.

Kumar, R., & Rose, C.P (2010). Architecture for building conversational agents that support collaborative learning. IEEE Transactions on Learning Technologies, 4(1), 21–34.

Martha, A.S.D., & Santoso, H.B (2019). The design and impact of the pedagogical agent: A systematic literature review. Journal of Educators Online, 16(1), n1.

Matsuda, N., Yarzebinski, E., Keiser, V., Raizada, R., Cohen, W.W, Stylianides, G.J, & Koedinger, K.R (2013). Cognitive anatomy of tutor learning: Lessons learned with simstudent. Journal of Educational Psychology, 105(4), 1152.

Morgan, D.L (1996). Focus groups. Annual Review of Sociology, 22(1), 129–152.

Narciss, S., Sosnovsky, S., Schnaubert, L., Andrès, E., Eichelmann, A., Goguadze, G., & Melis, E. (2014). Exploring feedback and student characteristics relevant for personalizing feedback strategies. Computers & Education, 71, 56–76.

Okonkwo, C.W., & Ade-Ibijola, A. (2021). Chatbots applications in education: A systematic review. Computers and Education: Artificial Intelligence, 2, 100033.

Pérez, J.Q., Daradoumis, T., & Puig, J.M.M. (

Here is the cleaned Markdown:

## References

Tegos, S., Demetriadis, S., & Karakostas, A. (2015). Promoting academically productive talk with conversational agent interventions in collaborative learning settings. Computers & Education, 87, 309–325.

Tegos, S., Demetriadis, S., & Tsiatsos, T. (2014). A configurable conversational agent to trigger students' productive dialogue: a pilot study in the call domain. International Journal of Artificial Intelligence in Education, 24(1), 62–91.

VanLehn, K., Graesser, A., Jackson, G.T., Jordan, P., Olney, A., & Rosé, C.P. (2007). Natural language tutoring: A comparison of human tutors, computer tutors, and text. Cognitive Science, 31(1), 3–52.

Villegas-Ch, W., Arias-Navarrete, A., & Palacios-Pacheco, X. (2020). Proposal of an architecture for the integration of a chatbot with artificial intelligence in a smart campus for the improvement of learning. Sustainability, 12(4), 1500.

Walker, E., Rummel, N., & Koedinger, K.R (2011). Designing automated adaptive support to improve student helping behaviors in a peer tutoring activity. International Journal of Computer-Supported Collaborative Learning, 6(2), 279–306.

Weizenbaum, J. (1966). Eliza–a computer program for the study of natural language communication between man and machine. Communications of the ACM, 9(1), 36–45.

Wik, P., & Hjalmarsson, A. (2009). Embodied conversational agents in computer assisted language learning. Speech Communication, 51(10), 1024–1037.

Alkhoori, A., Kuhail, M.A., & Alkhoori, A. (2020). Unibud: A virtual academic adviser. In 2020 12th annual undergraduate research conference on applied computing (URC) (pp. 1–4).

Alobaidi, O.G, Crockett, K.A, O'Shea, J.D, & Jarad, T.M (2013). Abdullah: An intelligent arabic conversational tutoring system for modern islamic education. In Proceedings of the world congress on engineering, Vol. 2.

Andrist, S., Mutlu, B., & Tapus, A. (2015). Look like me: matching robot personality via gaze to increase motivation. In Proceedings of the 33rd annual ACM conference on human factors in computing systems (pp. 3603–3612).

Anghelescu, P., & Nicolaescu, S.V. (2018). Chatbot application using search engines and teaching methods. In 2018 10th international conference on electronics, computers and artificial intelligence (ECAI) (pp. 1–6).

Ayedoun, E., Hayashi, Y., & Seta, K. (2017). Communication strategies and affective back channels for conversational agents to enhance learners' willingness to communicate in a second language. In International conference on artificial intelligence in education (pp. 459–462).

Benedetto, L., & Cremonesi, P. (2019). Rexy, a configurable application for building virtual teaching assistants. In IFIP conference on human-computer interaction (pp. 233–241).

Bradeško, L., & Mladenić, D. (2012). A survey of chatbot systems through a loebner prize competition. In Proceedings of Slovenian language technologies society eighth conference of language technologies (pp. 34–37).

Brewer, R.N, Findlater,

Here's the cleaned Markdown bibliography:

1. Dutta, D. (2017). Developing an intelligent chatbot tool to assist high school students for learning general knowledge subjects (Tech. rep.) Georgia Institute of Technology.

2. Felicia, P. (2011). Handbook of research on improving learning and motivation through educational games: Multidisciplinary approaches: Multidisciplinary approaches. iGi Global.

3. Feng, D., Shaw, E., Kim, J., & Hovy, E. (2006). An intelligent discussion-bot for answering student queries in threaded discussions. In Proceedings of the 11th international conference on intelligent user interfaces (pp. 171-177).

4. Følstad, A., Skjuve, M., & Brandtzaeg, P.B. (2018). Different chatbots for different purposes: towards a typology of chatbots to understand interaction design. In International conference on internet science (pp. 145-156).

5. Griol, D., Baena, I., Molina, J.M., & de Miguel, A.S. (2014). A multimodal conversational agent for personalized language learning. In Ambient intelligence-software and applications (pp. 13-21). Springer.

6. Griol, D., García-Herrero, J., & Molina, J. (2011). The educagent platform: Intelligent conversational agents for e-learning applications. In Ambient intelligence-software and applications (pp. 117-124). Springer.

7. Gulz, A., Haake, M., Silvervarg, A., Sjödén, B., & Veletsianos, G. (2011). Building a social conversational pedagogical agent: Design challenges and methodological approaches. In Conversational agents and natural language interaction: Techniques and effective practices (pp. 128-155). IGI Global.

8. Hayashi, Y. (2013). Learner-support agents for collaborative interaction: A study on affect and communication channels.

9. Heffernan, N.T, & Croteau, E.A (2004). Web-based evaluations showing differential learning for tutorial strategies employed by the ms. lindquist tutor. In International conference on intelligent tutoring systems (pp. 491-500).

10. Hobert, S., & Meyer von Wolff, R. (2019). Say hello to your new automated tutor--a structured literature review on pedagogical conversational agents.

11. Hwang, G.-J., & Chang, C.-Y. (2021). A review of opportunities and challenges of chatbots in education. Interactive Learning Environments, 1-14.

12. Inostroza, R., Rusu, C., Roncagliolo, S., Jimenez, C., & Rusu, V. (2012). Usability heuristics for touchscreen-based mobile devices. In 2012 ninth international conference on information technology-new generations (pp. 662-667).

13. Ismail, M., & Ade-Ibijola, A. (2019). Lecturer's apprentice: A chatbot for assisting novice programmers. In 2019 international multidisciplinary information technology and engineering conference (IMITEC) (pp. 1-8).

14. Janati, S.E., Maach, A., & Ghanami, D.E. (2020). Adaptive e-learning AI-powered chatbot based on multimedia indexing. International Journal of Advanced Computer Science and Applications 11(12). Retrieved from https://doi.org/10.14569/IJACSA.2020.0111238.

15. Kaczorowska-Spychalska, D. (2019). Chatbots in marketing. Management 23(1).

16. Keele, S., et

Here is the cleaned reference list in normalized Markdown:

- Law, E., Baghaei Ravari, P., Chhibber, N., Kulic, D., Lin, S., Pantasdo, K.D, Ceha, J., Suh, S., & Dillen, N. (2020). Curiosity notebook: A platform for learning by teaching conversational agents. In Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems (pp. 1–9).

- Lee, L.-K., Fung, Y.-C., Pun, Y.-W., Wong, K.-K., Yu, M.T.-Y., & Wu, N.-I. (2020). Using a multiplatform chatbot as an online tutor in a university course. In 2020 International Symposium on Educational Technology (ISET) (pp. 53–56). IEEE.

- Lieberman, H., Paternò, F., Klann, M., & Wulf, V. (2006). End-user development: An emerging paradigm. In End User Development (pp. 1–8). Springer.

- Mabunda, K. (2020). An intelligent chatbot for guiding visitors and locating venues.

- Maybin, J., Mercer, N., & Stierer, B. (1992). Scaffolding learning in the classroom. Thinking Voices: The Work of the National Oracy Project, 186–195.

- McCrae, R.R., & Costa, P.T.Jr. (2008). The five-factor theory of personality.

- Mellado-Silva, R., Faúndez-Ugalde, A., & Blanco-Lobos, M. (2020). Effective learning of tax regulations using different chatbot techniques.

- Mellenbergh, G.J, & Adèr, H.J. (2008). Tests and questionnaires: Construction and administration. Advising on Research Methods: A Consultant's Companion, 211–236.

- Mendez, S., Johanson, K., Martin Conley, V., Gosha, K., A Mack, N., Haynes, C., & A Gerhardt, R. (2020). Chatbots: A tool to supplement the future faculty mentoring of doctoral engineering students. International Journal of Doctoral Studies, 15.

- Nass, C., Steuer, J., & Tauber, E.R (1994). Computers are social actors. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 72–78).

- Nathoo, A., Gangabissoon, T., & Bekaroo, G. (2019). Exploring the use of tangible user interfaces for teaching basic java programming concepts: A usability study. In 2019 Conference on Next Generation Computing Applications (NextComp) (pp. 1–5).

- Oh, K.-J., Lee, D., Ko, B., & Choi, H.-J. (2017). A chatbot for psychiatric counseling in mental healthcare service based on emotional dialogue analysis and sentence generation. In 2017 18th IEEE International Conference on Mobile Data Management (MDM) (pp. 371–375).

- Ondáš, S., Pleva, M., & Hládek, D. (2019). How chatbots can be involved in the education process. In 2019 17th International Conference on Emerging eLearning Technologies and Applications (ICETA) (pp. 575–580).

- Padró, L., & Stanilovsky, E. (2012). FreeLing 3.0: Towards wider multilinguality. In LREC2012.

- Payne, G., & Payne, J

## References

- Verleger, M., & Pembridge, J. (2018). A pilot study integrating an AI-driven chatbot in an introductory programming course. In 2018 IEEE Frontiers in Education Conference (FIE) (pp. 1–4).

- Völkel, S.T., Buschek, D., Pranjic, J., & Hussmann, H. (2019). Understanding emoji interpretation through user personality and message context. In Proceedings of the 21st International Conference on Human-Computer Interaction with Mobile Devices and Services (pp. 1–12).

- Völkel, S.T., & Kaya, L. (2021). Examining user preference for agreeableness in chatbots. In CUI 2021-3rd Conference on Conversational User Interfaces (pp. 1–6).

- Wambsganss, T., Kueng, T., Soellner, M., & Leimeister, J.M. (2021). ArgueTutor: An adaptive dialog-based learning system for argumentation skills. In Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems (pp. 1–13).

- Wambsganss, T., Winkler, R., Schmid, P., & Söllner, M. (2020). Designing a conversational agent as a formative course evaluation tool.

- Wambsganss, T., Winkler, R., Söllner, M., & Leimeister, J. M. (2020). A conversational agent to improve response quality in course evaluations. In Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems (pp. 1–9).

- West, A., Swanson, J., & Lipscomb, L. (2017). Ch. 11 Scaffolding. Instructional Methods, Strategies and Technologies to Meet the Needs of All Learners.

- Winkler, R., Hobert, S., Salovaara, A., Söllner, M., & Leimeister, Jan Marco (2020). Sara, the lecturer: Improving learning in online education with a scaffolding-based conversational agent. In Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems (pp. 1–14).

- Winkler, R., & Söllner, M. (2018). Unleashing the potential of chatbots in education: A state-of-the-art analysis. In Academy of Management Annual Meeting (AOM).

- Wollny, S., Schneider, J., Di Mitri, D., Weidlich, J., Rittberger, M., & Drachsler, H. (2021). Are we there yet?-A systematic literature review on chatbots in education. Frontiers in Artificial Intelligence 4.

- Xu, A., Liu, Z., Guo, Y., Sinha, V., & Akkiraju, R. (2017). A new chatbot for customer service on social media. In Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems (pp. 3506–3510).

- Zedadra, A., Lafifi, Y., & Zedadra, O. (2014). Interpreting learners' traces in collaborative learning environments. In 2014 4th International Symposium ISKO-Maghreb: Concepts and Tools for Knowledge Management (ISKO-Maghreb) (pp. 1–8).

## Authors and Affiliations

Mohammad Amin Kuhail¹, Nazik Alturki², Salwa Alramlawi³, Kholood Alhejori⁴

1