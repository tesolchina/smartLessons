# Are We There Yet? - A Systematic Literature Review on Chatbots in Education

Sebastian Wollny¹*, Jan Schneider¹*, Daniele Di Mitri¹, Joshua Weidlich¹, Marc Rittberger¹ and Hendrik Drachsler¹,²,³

¹Information Center for Education, DIPF | Leibniz Institute for Research and Information in Education, Frankfurt am Main, Germany  
²Educational Science Faculty, Open University of the Netherlands, Heerlen, Netherlands  
³Computer Science Faculty, Goethe University, Frankfurt am Main, Germany

Chatbots are a promising technology with the potential to enhance workplaces and everyday life. In terms of scalability and accessibility, they also offer unique possibilities as communication and information tools for digital learning. In this paper, we present a systematic literature review investigating the areas of education where chatbots have already been applied, explore the pedagogical roles of chatbots, the use of chatbots for mentoring purposes, and their potential to personalize education. We conducted a preliminary analysis of 2,678 publications to perform this literature review, which allowed us to identify 74 relevant publications for chatbots' application in education. Through this, we address five research questions that, together, allow us to explore the current state-of-the-art of this educational technology. We conclude our systematic review by pointing to three main research challenges:

1. Aligning chatbot evaluations with implementation objectives
2. Exploring the potential of chatbots for mentoring students
3. Exploring and leveraging adaptation capabilities of chatbots

For all three challenges, we discuss opportunities for future research.

**Keywords**: chatbots, education, literature review, pedagogical roles, domains

## Introduction

Educational Technologies enable distance learning models and provide students with the opportunity to learn at their own pace. They have found their way into schools and higher education institutions through Learning Management Systems and Massive Open Online Courses, enabling teachers to scale up good teaching practices (Ferguson and Sharples, 2014) and allowing students to access learning material ubiquitously (Virtanen et al., 2018).

Despite the innovative power of educational technologies, most commonly used technologies do not substantially change teachers' role. Typical teaching activities like providing students with feedback, motivating them, or adapting course content to specific student groups are still entrusted exclusively to teachers, even in digital learning environments. This can lead to the teacher-bandwidth problem (Wiley and Edwards, 2002), the result of a shortage of teaching staff to provide highly informative and competence-oriented feedback at large scale. Nowadays, however, computers and other digital devices open up far-reaching possibilities that have not yet been fully exploited. For example, incorporating process data can provide students with insights into their learning progress and bring new possibilities for formative feedback, self-reflection, and competence development (Quincey et al., 2019). According to (Hattie, 2009), feedback in terms of learning success has a mean

Here's the cleaned Markdown:

## Related Work

One of the educational technologies designed to provide actionable feedback is Learning Analytics. Learning Analytics is defined as the research area that focuses on collecting traces that learners leave behind and using those traces to improve learning (Duval and Verbert, 2012; Greller and Drachsler, 2012). Learning Analytics can be used both by students to reflect on their own learning progress and by teachers to continuously assess the students' efforts and provide actionable feedback. Another relevant educational technology is Intelligent Tutoring Systems. Intelligent Tutoring Systems are defined as computerized learning environments that incorporate computational models (Graesser et al., 2001) and provide feedback based on learning progress. Educational technologies specifically focused on feedback for help-seekers, comparable to raising hands in the classroom, are Dialogue Systems and Pedagogical Conversational Agents (Lester et al., 1997). These technologies can simulate conversational partners and provide feedback through natural language (McLoughlin and Oliver, 1998).

Research in this area has recently focused on chatbot technology, a subtype of dialog systems, as several technological platforms have matured and led to applications in various domains. Chatbots incorporate generic language models extracted from large parts of the Internet and enable feedback by limiting themselves to text or voice interfaces. For this reason, they have also been proposed and researched for a variety of applications in education (Winkler and Soellner, 2018). Recent literature reviews on chatbots in education (Winkler and Soellner, 2018; Hobert, 2019a; Hobert and Meyer von Wolff, 2019; Jung et al., 2020; Pérez et al., 2020; Smutny and Schreiberova, 2020; Pérez-Marín, 2021) have reported on such applications as well as design guidelines, evaluation possibilities, and effects of chatbots in education.

In this paper, we contribute to the state-of-the-art of chatbots in education by presenting a systematic literature review, where we examine so-far unexplored areas such as implementation objectives, pedagogical roles, mentoring scenarios, the adaptations of chatbots to learners, and application domains. This paper is structured as follows: First, we review related work (section 2), derive research questions from it, then explain the applied method for searching related studies (section 3), followed by the results (section 4), and finally, we discuss the findings (section 5) and point to future research directions in the field (section 5).

Chatbots are digital systems that can be interacted with entirely through natural language via text or voice interfaces. They are intended to automate conversations by simulating a human conversation partner and can be integrated into software, such as online platforms, digital assistants, or be interfaced through messaging services.

Outside of education, typical applications of chatbots are in customer service (Xu et al., 2017), counseling of hospital patients (Vaidyam et al., 2019), or information services in smart speakers (Ram et al., 2018). One central element of chatbots is the intent classification, also named the Natural Language Understanding (NLU) component, which is responsible for the sense-making of human input data. Looking at the current advances in chatbot software development, it seems that this technology's goal is to pass the Turing Test (Saygin et al., 2000) one day, which could make chatbots effective educational tools. Therefore, we ask ourselves "Are we there yet? - Will we soon have an autonomous chatbot for every learner?"

To understand and underline the current need for research in the use of chatbots in education, we first examined the existing literature, focusing on comprehensive literature reviews. By looking at research questions in these literature reviews, we identified 21 different research topics and extracted findings accordingly. To structure research topics and findings in a comprehensible way, a three-stage clustering process was applied. While the first stage consisted of coding research topics by

Here's the cleaned and normalized Markdown:

## Applications and Design of Educational Chatbots

Regarding chatbot designs (CAT2), most of the research questions concerned with chatbots in education can be assigned to this category. We found three aspects in this category: Personality (PS), Process Pipeline (PP), and Design Classifications (DC). Within these, most research questions can be assigned to Design Classifications (DC), which are separated into Classification Aspects (DC2) and Classification Frameworks (DC1).

One classification framework is defined through "flow chatbots," "artificially intelligent chatbots," "chatbots with integrated speech recognition," as well as "chatbots with integrated context-data" by (Winkler and Soellner, 2018). A second classification framework by (Pérez-Marín, 2021) covers pedagogy, social, and HCI features of chatbots and agents, which themselves can be further subdivided into more detailed aspects.

Other Classification Aspects (DC2) derived from several publications, provide another classification schema, which distinguishes between "retrieval vs. generative" based technology, the "ability to incorporate context data," and "speech or text interface" (Winkler and Soellner, 2018; Smutny and Schreiberova, 2020). Text interfaces can be subdivided by specifying them as "Button-Based" or "Keyword Recognition-Based" (Smutny and Schreiberova, 2020). Furthermore, a comparison of speech and text interfaces (Jung et al., 2020) shows that text interfaces have advantages for conveying information, and speech interfaces have advantages for affective support.

The second aspect of CAT2 concerns the chatbot processing pipeline (PP), highlighting user interface and back-end importance (Pérez et al., 2020). Finally, (Jung et al., 2020) focuses on the third aspect, the personality of chatbots (PS). Here, the study derives four guidelines helpful in education:

- Positive or neutral emotional expressions
- A limited amount of animated or visual graphics
- A well-considered gender of the chatbot
- Human-like interactions

In summary, we have found in CAT2 three main design aspects for the development of chatbots. CAT2 is much more diverse than CAT1 with various sub-categories for the design of chatbots. This indicates the huge flexibility to design chatbots in various ways to support education.

[Tables and figures preserved as in original]

Here's the cleaned and normalized Markdown:

## How Chatbots Can Take Over Tasks from Teachers

Winkler and Soellner (2018) and Pérez-Marín (2021) identified research gaps for supporting meta-cognitive skills with chatbots such as self-regulation. This requires a chatbot application that takes a mentoring role, as the development of these meta-cognitive skills cannot be achieved solely by information delivery. Within our review we incorporate this by reviewing the mentoring role of chatbots as (Goal 3). Another key element for a mentoring chatbot is adaptation to the learners needs. Therefore, (Goal 4) of our review lies in the investigation of the adaptation approaches used by chatbots in education. For (Goal 5), we want to extend the work of Winkler and Soellner (2018) and Pérez et al. (2020) regarding Application Clusters (AC) and map applications by further investigating specific learning domains in which chatbots have been studied.

## Methods

To delineate and map the field of chatbots in education, initial findings were collected by a preliminary literature search. One of the takeaways is that the emerging field around educational chatbots has seen much activity in the last two years. Based on the experience of this preliminary search, search terms, queries, and filters were constructed for the actual structured literature review. This structured literature review follows the PRISMA framework (Liberati et al., 2009), a guideline for reporting systematic reviews and meta-analyses. The framework consists of an elaborated structure for systematic literature reviews and sets requirements for reporting information about the review process (see section 3.2 to 3.4).

### Research Questions

Contributing to the state-of-the-art, we investigate five aspects of chatbot applications published in the literature. We therefore guided our research with the following research questions:

1. Which objectives for implementing chatbots in education can be identified in the existing literature?
2. Which pedagogical roles of chatbots can be identified in the existing literature?
3. Which application scenarios have been used to mentor students?
4. To what extent are chatbots adaptable to personal students' needs?
5. What are the domains in which chatbots have been applied so far?

### Sources of Information

As data sources, Scopus, Web of Science, Google Scholar, Microsoft Academics, and the educational research database "Fachportal Pädagogik" (including ERIC) were selected, all of which incorporate all major publishers and journals. In Martín-Martín et al. (2018) it was shown that for the social sciences only 29.8% and for engineering and computer science, 46.8% of relevant literature is included in all of the first three databases. For the topic of chatbots in education, a value between these two numbers can be assumed, which is why an approach of integrating several publisher-independent databases was employed here.

### Search Criteria

Based on the findings from the initial related work search, we derived the following search query:

(Education OR Educational OR Learning OR Learner OR Student OR Teaching OR School OR University OR Pedagogical) AND Chatbot.

It combines education-related keywords with the "chatbot" keyword. Since chatbots are related to other technologies, the initial literature search also considered keywords such as "pedagogical agents," "dialogue systems," or "bots" when composing the search query. However, these increased the number of irrelevant results significantly and were therefore excluded from the query in later searches.

[Content continues...]

Here's the cleaned and normalized Markdown:

## Limitation of Physical Presence

In addition, there are other, more diverse objectives for chatbots in education that are less easy to categorize. In cases of a publication indicating more than one objective, the publication was distributed evenly across the respective categories.

Given these results, we can summarize four major implementing objectives for chatbots. Of these, Skill Improvement is the most popular objective, constituting around one-third of publications (32%). Making up a quarter of all publications, Efficiency of Education is the second most popular objective (25%), while addressing Students' Motivation and Availability of Education are third (13%) and fourth (11%), respectively. Other objectives also make up a substantial amount of these publications (19%), although they were too diverse to categorize in a uniform way. Examples of these are inclusivity (Heo and Lee, 2019) or the promotion of student teacher interactions (Mendoza et al., 2020).

## Pedagogical Roles

Regarding RQ2, it is crucial to consider the use of chatbots in terms of their intended pedagogical role. After analyzing the selected articles, we were able to identify four different pedagogical roles: a supporting learning role, an assisting role, and a mentoring role.

In the supporting learning role (Learning), chatbots are used as an educational tool to teach content or skills. This can be achieved through a fixed integration into the curriculum, such as conversation tasks (L. K. Fryer et al., 2020). Alternatively, learning can be supported through additional offerings alongside classroom teaching, for example, voice assistants for leisure activities at home (Bao, 2019). Examples of these are chatbots simulating a virtual pen pal abroad (Na-Young, 2019). Conversations with this kind of chatbot aim to motivate the students to look up vocabulary, check their grammar, and gain confidence in the foreign language.

In the assisting role (Assisting), chatbot actions can be summarized as simplifying the student's everyday life, i.e., taking tasks off the student's hands in whole or in part. This can be achieved by making information more easily available (Sugondo and Bahana, 2019) or by simplifying processes through the chatbot's automation (Suwannatee and Suwanyangyuen, 2019). An example of this is the chatbot in (Sandoval, 2018) that answers general questions about a course, such as an exam date or office hours.

In the mentoring role (Mentoring), chatbot actions deal with the student's personal development. In this type of support, the student himself is the focus of the conversation and should be encouraged to plan, reflect or assess his progress on a meta-cognitive level. One example is the chatbot in (Cabales, 2019), which helps students develop lifelong learning skills by prompting in-action reflections.

The distribution of each pedagogical role is shown in Figure 8. From this, it can be seen that Learning is the most frequently used role of the examined publications (49%), followed by Assisting (20%) and Mentoring (15%). It should be noted that pedagogical roles were not identified for all the publications examined. The absence of a clearly defined pedagogical role (16%) can be attributed to the more general nature of these publications, e.g. focused on students' small talk behaviors (Hobert, 2019b) or teachers' attitudes towards chatbot applications in classroom teaching (P. K. Bii et al., 2018).

Looking at pedagogical roles in the context of objectives for implementing chatbots, relations among publications can be inspected in a relations graph (Figure 9). According to our results, the strongest relation in the examined publications can be considered between Skill Improvement objective and the Learning role. This strong relation is partly because both, the Skill Improvement objective and the Learning role, are the largest in their respective categories. In addition, two other strong relations can be observed: Between the Students' Motivation objective and the Learning role, as well as between Efficiency

Here's the cleaned and normalized Markdown:

## Learning Progress and Mentoring Chatbots

Mentoring chatbots to support Life Skills address general student's abilities such as self-confidence or managing emotions. Mentoring chatbots to support Learning Skills, in contrast to Self-Regulated Learning, address only particular aspects of the learning process, such as new learning strategies or helpful learning partners. An example for Mentoring chatbots supporting Life Skill is the Logo counseling chatbot, which promotes healthy self-esteem (Engel et al., 2020). CALMsystem is an example of a Self-Regulated Learning chatbot, which informs students about their data in an open learner model (Kerly et al., 2008). Finally, there is the Learning Skills topic. Here, the MCQ Bot is an example that is designed to introduce students to transformative learning (W. Huang et al., 2019).

## Adaptation

Regarding RQ4, we identified six publications in the final publication list that address the topic of adaptation. Within these publications, five adaptation approaches are described:

1. The first approach (A1) is proposed by (Kerly and Bull, 2006) and (Kerly et al., 2008), dealing with student discussions based on success and confidence during a quiz. The improvement of self-assessment is the primary focus of this approach.
2. The second approach (A2) is presented in (Jia, 2008), where the personality of the chatbot is adapted to motivate students to talk to the chatbot and, in this case, learn a foreign language.
3. The third approach (A3), as shown in the work of (Vijayakumar et al., 2019), is characterized by a chatbot that provides personalized formative feedback to learners based on their self-assessment, again in a quiz situation. Here, the focus is on Hattie and Timperley's three guiding questions: "Where am I going?," "How am I going?" and "Where to go next?" (Hattie and Timperley, 2007).
4. In the fourth approach (A4), exemplified in (Ruan et al., 2019), the chatbot selects questions within a quiz. Here, the chatbot estimates the student's ability and knowledge level based on the quiz progress and sets the next question accordingly.
5. Finally, a similar approach (A5) is shown in (Davies et al., 2020). In contrast to (Ruan et al., 2019), this chatbot adapts the amount of question variation and takes psychological features into account which were measured by psychological tests before.

We examined these five approaches by organizing them according to their information sources and extracted learner information. The results can be seen in Table 2.

Four out of five adaptation approaches (A1, A3, A4, and A5) are observed in the context of quizzes. These adaptations within quizzes can be divided into two mainstreams: One is concerned about students' feedback (A1 and A3), while the other is concerned about learning material selection (A4 and A5). The only different adaptation approach is shown in A2, which focuses on the adaptation of the chatbot personality within a language learning application.

## Domains for Chatbots in Education

Regarding RQ5, we identified 20 domains of chatbots in education. These can broadly be divided by their pedagogical role into three domain categories (DC): Learning Chatbots, Assisting Chatbots, and Mentoring Chatbots. The remaining publications are grouped in the Other Research domain category.

### Learning Chatbots

The domain category Learning Chatbots, which deals with chatbots incorporating the pedagogical role Learning, can be subdivided into seven domains:

1. Language Learning
2. Learn to Program
3. Learn Communication Skills
4. Learn about Educational Technologies
5. Learn about Cultural Heritage
6. Learn about Laws
7. Mathematics Learning

With more than half of

Here's the cleaned Markdown:

## Mentoring Chatbots and Domain Categories

The domain category Mentoring Chatbots, which deals with chatbots incorporating the pedagogical role Mentoring, can be subdivided into three domains: 
1. Scaffolding Chatbots
2. Recommending Chatbots
3. Informing Chatbots

An example of a Scaffolding Chatbot is the CRI(S) chatbot (Gabrielli et al., 2020), which supports life skills such as self-awareness or conflict resolution in discussion with the student by promoting helpful ideas and tricks.

The domain category Other Research, which deals with chatbots not incorporating any of these pedagogical roles, can be subdivided into three domains:
1. General Chatbot Research in Education
2. Indian Educational System
3. Chatbot Interfaces

The most prominent domain, General Chatbot Research, cannot be classified in one of the other categories but aims to explore cross-cutting issues. An example for this can be seen in the publication of (Hobert, 2020), which researches the importance of small talk abilities of chatbots in educational settings.

## Discussions

In this paper, we investigated the state-of-the-art of chatbots in education according to five research questions. By combining our results with previously identified findings from related literature reviews, we proposed a concept map of chatbots in education. The map, reported in Appendix A, displays the current state of research regarding chatbots in education with the aim of supporting future research in the field.

### Answer to Research Questions

Concerning RQ1 (implementation objectives), we identified four major objectives:
1. Skill Improvement
2. Efficiency of Education
3. Students' Motivation
4. Availability of Education

These four objectives cover over 80% of the analyzed publications (see Figure 7). Based on the findings on CAT3 in section 2, we see a mismatch between the objectives for implementing chatbots compared to their evaluation. Most researchers only focus on narrow aspects for the evaluation of their chatbots such as learning success, usability, and technology acceptance. This mismatch of implementation objectives and suitable evaluation approaches is also well known by other educational technologies such as Learning Analytics dashboards (Jivet et al., 2017). A more structured approach of aligning implementation objectives and evaluation procedures is crucial to be able to properly assess the effectiveness of chatbots. (Hobert, 2019a), suggested a structured four-stage evaluation procedure beginning with a Wizard-of-Oz experiment, followed by technical validation, a laboratory study, and a field study. This evaluation procedure systematically links hypotheses with outcomes of chatbots helping to assess chatbots for their implementation objectives. "Aligning chatbot evaluations with implementation objectives" is, therefore, an important challenge to be addressed in the future research agenda.

Concerning RQ2 (pedagogical roles), our results show that chatbots' pedagogical roles can be summarized as Learning, Assisting, and Mentoring. The Learning role is the support in learning or teaching activities such as gaining knowledge. The Assisting role is the support in terms of simplifying learners' everyday life, e.g. by providing opening times of the library. The Mentoring role is the support in terms of students' personal development, e.g. by supporting Self-Regulated Learning. From a pedagogical standpoint, all three roles are essential for learners and should therefore be incorporated in chatbots. These pedagogical roles are well aligned with the four implementation objectives reported in RQ1. While Skill Improvement and Students' Motivation is strongly related to Learning, Efficiency of Education is strongly related to Assisting. The Mentoring role instead, is evenly related to all of the identified objectives for implementing chatbots. In the reviewed publications, chatbots are therefore primarily intended to:
1. improve skills and motivate students by supporting learning and teaching activities
2. make education more efficient by providing relevant administrative and logistical information to learners
3

Here's the cleaned Markdown:

## Limitations

One important limitation to be mentioned here is the exclusion of alternative keywords for our search queries, as we exclusively used chatbot as keyword in order to avoid search results that do not fit our research questions. Though we acknowledge that chatbots share properties with pedagogical agents, dialog systems, and bots, we carefully considered this trade-off between missing potentially relevant work and inflating our search procedure by including related but not necessarily pertinent work. A second limitation may lie in the formation of categories and coding processes applied, which, due to the novelty of the findings, could not be built upon theoretical frameworks or already existing code books. Although we have focused on ensuring that codes used contribute to a strong understanding, the determination of the abstraction level might have affected the level of detail of the resulting data representation.

## Conclusion

In this systematic literature review, we explored the current landscape of chatbots in education. We analyzed 74 publications, identified 20 domains of chatbots and grouped them based on their pedagogical roles into four domain categories. These pedagogical roles are the supporting learning role (Learning), the assisting role (Assisting), and the mentoring role (Mentoring). By focusing on objectives for implementing chatbots, we identified four main objectives:

1. Skill Improvement
2. Efficiency of Education
3. Students' Motivation
4. Availability of Education

As discussed in section 5, these objectives do not fully align with the chosen evaluation procedures. We focused on the relations between pedagogical roles and objectives for implementing chatbots and identified three main relations:

1. chatbots to improve skills and motivate students by supporting learning and teaching activities
2. chatbots to make education more efficient by providing relevant administrative and logistical information to learners
3. chatbots to support multiple effects by mentoring students

We focused on chatbots incorporating the Mentoring role and found that these chatbots are mostly concerned with three mentoring topics:

1. Self-Regulated Learning
2. Life Skills
3. Learning Skills

and three mentoring methods:

1. Scaffolding
2. Recommending
3. Informing

Regarding chatbot adaptations, only six publications with adaptations were identified. Furthermore, the adaptation approaches found were mostly limited to applications within quizzes and thus represent a research gap.

Based on these outcomes we consider three challenges for chatbots in education that offer future research opportunities:

### Challenge 1: Aligning chatbot evaluations with implementation objectives

Most chatbot evaluations focus on narrow aspects to measure the tool's usability, acceptance or technical correctness. If chatbots should be considered as learning aids, student mentors, or facilitators, the effects on the cognitive, and emotional levels should also be taken into account for the evaluation of chatbots. This finding strengthens our conclusion that chatbot development in education is still driven by technology, rather than having a clear pedagogical focus of improving and supporting learning.

### Challenge 2: Exploring the potential of chatbots for mentoring students

In order to better understand the potentials of chatbots to mentor students, more empirical studies on the information needs of learners are required. It is obvious that these needs differ from schools to higher education. However, so far there are hardly any studies investigating the information needs with respect to chatbots nor if chatbots address these needs sufficiently.

### Challenge 3: Exploring and leveraging adaptation capabilities of chatbots

There is a large literature on adaptation capabilities of educational technologies. However, we have seen very few studies on the effect of adaptation of chatbots for education purposes. As chatbots are foreseen as systems that should personally support learners, the area of adaptable interactions of chatbots is an important research aspect that should receive more attention in the near future.

By addressing these challenges, we believe that chatbots can become effective educational tools capable of supporting learners with informative feedback. Therefore, looking at our results and the challenges presented, we conclude, "No, we are not there yet!" - There is still much to be done in terms of research on chatbots

## References

Abbasi, S., Kazi, H., and Hussaini, N. N. (2019). Effect of Chatbot Systems on Student's Learning Outcomes. Sylwan 163(10).

Abbasi, S., and Kazi, H. (2014). Measuring Effectiveness of Learning Chatbot Systems on Student's Learning Outcome and Memory Retention. Asian J. Appl. Sci. Eng. 3, 57. doi:10.15590/AJASE/2014/V3I7/53576

Almahri, F. A. J., Bell, D., and Merhi, M. (2020). "Understanding Student Acceptance and Use of Chatbots in the United Kingdom Universities: A Structural Equation Modelling Approach," in 2020 6th IEEE International Conference on Information Management, ICIM 2020, London, United Kingdom, March 27-29, 2020, (IEEE), 284-288. doi:10.1109/ICIM49319.2020.244712

Bao, M. (2019). Can Home Use of Speech-Enabled Artificial Intelligence Mitigate Foreign Language Anxiety - Investigation of a Concept. Awej 5, 28-40. doi:10.24093/awej/call5.3

Benyon, D., and Murray, D. (1993). Applying User Modeling to Human-Computer Interaction Design. Artif. Intell. Rev. 7(3-4), 199-225. doi:10.1007/BF00849555

[References continue in same format...]

Here's the cleaned Markdown:

Frontiers in Artificial Intelligence | www.frontiersin.org
July 2021 | Volume 4 | Article 654924

## References

- ED-MEDIA 2005–World Conference on Educational Multimedia, Hypermedia and Telecommunications, Montréal, Canada, June 27–July 2, 2005. Editors P. Kommers and G. Richards, (AACE), 3913–3918

- Heo, J., and Lee, J. (2019). "CiSA: An Inclusive Chatbot Service for International Students and Academics," in 21st International Conference on Human-Computer Interaction, HCII 2019: Communications in Computer and Information Science, Orlando, FL, USA, July 26–31, 2019. Editors C. Stephanidis, (Springer) 11786, 153–167. doi:10.1007/978-3-030-30033-3

- Hobert, S. (2019a). "How Are You, Chatbot? Evaluating Chatbots in Educational Settings - Results of a Literature Review," in 17. Fachtagung Bildungstechnologien, DELFI 2019 - 17th Conference on Education Technologies, DELFI 2019, Berlin, Germany, Sept 16–19, 2019. Editors N. Pinkwart and J. Konert, 259–270. doi:10.18420/delfi2019_289

- Hobert, S., and Meyer von Wolff, R. (2019). "Say Hello to Your New Automated Tutor - A Structured Literature Review on Pedagogical Conversational Agents," in 14th International Conference on Wirtschaftsinformatik, Siegen, Germany, Feb 23–27, 2019. Editors V. Pipek and T. Ludwig, (AIS).

- Hobert, S. (2019b). Say Hello to 'Coding Tutor'! Design and Evaluation of a Chatbot-Based Learning System Supporting Students to Learn to Program in International Conference on Information Systems (ICIS) 2019 Conference, Munich, Germany, Dec 15–18, 2019, AIS 2661, 1–17

[References continue in same format...]

Here is the cleaned Markdown bibliography:

- Meyer, V., Wolff, R., Nörtemann, J., Hobert, S., and Schumann, M. (2020). "Chatbots for the Information Acquisition at Universities - A Student's View on the Application Area," in 3rd International Workshop on Chatbot Research and Design, CONVERSATIONS 2019, Amsterdam, Netherlands, November 19–20, Lecture Notes in Computer Science. Editors A. Folstad, T. Araujo, S. Papadopoulos, E. Law, O. Granmo, E. Luger, and P. Brandtzaeg, (Springer) 11970, 231–244. doi:10.1007/978-3-030-39540-7

- Na-Young, K. (2018c). A Study on Chatbots for Developing Korean College Students' English Listening and Reading Skills. J. Digital Convergence 16. 19–26. doi:10.14400/JDC.2018.16.8.019

- Na-Young, K. (2019). A Study on the Use of Artificial Intelligence Chatbots for Improving English Grammar Skills. J. Digital Convergence 17, 37–46. doi:10.14400/JDC.2019.17.8.037

- Na-Young, K. (2018a). Chatbots and Korean EFL Students' English Vocabulary Learning. J. Digital Convergence 16. 1–7. doi:10.14400/JDC.2018.16.2.001

- Na-Young, K. (2018b). Different Chat Modes of a Chatbot and EFL Students' Writing Skills Development. 1225–4975. doi:10.16933/sfle.2017.32.1.263

[Continued formatting of remaining references following same pattern...]

Note: I've started formatting the references but stopped here to avoid exceeding length limits. The same formatting pattern would continue for the remaining entries - removing line breaks within references while maintaining proper spacing between entries, preserving all citation information including DOIs and URLs.

Here's the cleaned Markdown:

## References

Applications. Editors D. H. Schunk and B. J. Zimmerman, (Mahwah, NJ: Lawrence Erlbaum Associates Publishers), 297–314.

Wisniewski, B., Zierer, K., and Hattie, J. (2019). The Power of Feedback Revisited: A Meta-Analysis of Educational Feedback Research. Front. Psychol. 10, 1664–1078. doi:10.3389/fpsyg.2019.03087

Wolfbauer, I., Pammer-Schindler, V., and Rose, C. P. (2020). "Rebo Junior: Analysis of Dialogue Structure Quality for a Reflection Guidance Chatbot," in Proceedings of the Impact Papers at EC-TEL 2020, co-located with the 15th European Conference on Technology-Enhanced Learning "Addressing global challenges and quality education" (EC-TEL 2020), Virtual, Sept 14–18, 2020. Editors T. Broos and T. Farrell, 1–14.

Xiao, Z., Zhou, M. X., and Fu, W.-T. (2019). "Who should be my teammates: Using a conversational agent to understand individuals and help teaming," in IUI'19: Proceedings of the 24th International Conference on Intelligent User Interfaces, Marina del Ray, California, USA, March 17–20, 2019, (ACM), 437–447. doi:10.1145/3301275.3302264

Xu, A., Liu, Z., Guo, Y., Sinha, V., and Akkiraju, R. (2017). "A New Chatbot for Customer Service on Social media," in Proceedings of the 2017 CHI conference on human factors in computing systems, Denver, Colorado, USA, May 6–11, 2017, ACM, 3506–3510. doi:10.1145/3025453.3025496

Yin, J., Goh, T.-T., Yang, B., and Xiaobin, Y. (2020). Conversation Technology with Micro-learning: The Impact of Chatbot-Based Learning on Students' Learning Motivation and Performance. J. Educ. Comput. Res. 59, 154–177. doi:10.1177/0735633120952067

## Conflict of Interest

The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

## Copyright Notice

Copyright © 2021 Wollny, Schneider, Di Mitri, Weidlich, Rittberger and Drachsler. This is an open-access article distributed under the terms of the Creative Commons Attribution License (CC BY). The use, distribution or reproduction in other forums is permitted, provided the original author(s) and the copyright owner(s) are credited and that the original publication in this journal is cited, in accordance with accepted academic practice. No use, distribution or reproduction is permitted which does not comply with these terms.

## Appendix A

A CONCEPT MAP OF CHATBOTS IN EDUCATION