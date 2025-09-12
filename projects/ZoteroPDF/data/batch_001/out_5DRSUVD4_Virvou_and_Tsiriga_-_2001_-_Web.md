# Web Passive Voice Tutor: an Intelligent Computer Assisted Language Learning System over the WWW

Maria Virvou   
Department of Informatics,   
University of Piraeus,   
80 Karaoli & Dimitriou St.   
Piraeus 18534, Greece   
mvirvou@unipi.gr   
Victoria Tsiriga   
Department of Informatics,   
University of Piraeus,   
80 Karaoli & Dimitriou St.   
Piraeus 18534, Greece   
vtsir@unipi.gr

# Abstract

In this paper we describe Web Passive Voice Tutor (Web PVT), an adaptive web-based Intelligent Computer Assisted Language Learning (ICALL) program that is aimed at teaching non-native speakers the passive voice of the English language. The design of the system has been largely based on the results of an empirical study that was conducted at schools with the collaboration of human teachers. Web PVT incorporates techniques from Intelligent Tutoring Systems (ITS) and Adaptive Hypermedia (AH) technologies to provide students with individualised instruction and feedback. The system uses a combination of stereotypes and the overlay technique for the initialisation of the student model, which is then refined by observing the student while working with the system. The resulting student model is used for the annotation of the links to topics presented to the student. In addition, it is also used in the process of error diagnosis and the adaptation of feedback and advice provided to the student.

# 1. Introduction

Currently, a lot of research energy is put in the development of web-based educational software. Benefits of web-based education are independence of teaching and learning with respect to time and space [11]. Another important advantage of web-based educational software is platform independence of the application and easy access to it. These advantages ensure that the audience of webbased applications may be very large. However, most existing web-based educational applications lack the sophistication, interactivity and adaptivity of applications, such as ITSs [17].

On the other hand, ITSs are very good at individualising educational support to students, but they are criticised that they are often research products that are not accessible by many students. ITSs may benefit from Web technology to gain more accessibility, and webbased education may gain intelligence and adaptivity from ITSs. Therefore, the combination of these two technologies may produce very powerful and flexible educational programs. However, as Brusilovsky points out [3], web-based ITSs still constitute a rather small steam inside the ITS area. This is even more the case for Intelligent Computer Language Learning (ICALL) systems delivered via the WWW.

The existence of still few web-based ICALL systems does not undermine the educational impact that such systems may have if delivered via the web. Indeed, the domain of language learning is probably among the few domains that may be of interest to students internationally, irrespective of their mother tongue. Other ITS domains may have more restricted audience due to the dependence of the courses on the language they are written in. For example, a web-based course for the French language may be used by students of any mother tongue who learn French, whereas a web-based course for history written in Greek may only be used by history students who know Greek. This is an additional reason that advocates in favour of further research and development in the area of web-based ICALL.

In this paper we describe Web Passive Voice Tutor (Web PVT), an adaptive web-based ICALL that is aimed at teaching non-native speakers the passive voice of the English language. Web PVT has been based on an earlier standalone ICALL system, the Passive Voice Tutor [14, 15]. Prior to designing the web-based version of the system, an empirical study was conducted at schools with the collaboration of school-teachers.

Web PVT provides adaptive navigation support, intelligent analysis of students’ solutions and individualised feedback and advice. The adaptivity of the system is implemented by presenting students with different, dynamically constructed HTML pages. The decision about the content of each page is based on the model of each individual student.

Brusilovsky in [2], outlines three stages in the adaptation process: collecting data about the user, processing the data to build or update the user model, and applying the user model to provide the adaptation. In the case of Web PVT, the system uses a combination of stereotypes and the overlay technique for the initialisation of the student model. The system uses stereotypes along several dimensions to provide initial values to attributes of the student model, which are then refined by observing the student while working with the system. The resulting student model is used by the tutoring module to provide adaptive navigation support while the student is presented with theoretical issues concerning the passive voice. Then the student model is also used for providing individualised problem solving support to students. This includes automatic error diagnosis to the students’ answer to exercises and appropriate advice.

# 2. Requirements analysis and Design

As Mark and Greer point out in [9], the accuracy of ITS components such as domain knowledge should be ensured before a system is completed and assumed thereafter. One good way of ensuring this accuracy is to involve human teachers and students in the early stages of the development process [16].

The design of Web PVT has been based, to a large extent, on the results of an empirical study that involved school-teachers and students. These results were particularly useful for the requirements analysis of Web PVT. They showed what particular pieces of the domain knowledge seem difficult for students to comprehend fully, what misconceptions they may have while learning and what the explanations to those misconceptions may be [15].

# 3. System Architecture

The deployment of Web PVT was based on the "HTML-CGI" architecture. The user interacts with simple HTML pages and entry forms using her/his standard Web browser. Information entered by the user is sent to the Web server which forwards it to the CGI program which then replies with new HTML pages [1]. We have chosen this server centred approach, since the installation and maintenance of the Web-based ITS on the server side allows the designers and developers of the system to modify and update the software without the need of redistributing it to students.

Web PVT follows the main line of an ITS architecture, adjusted to the WWW technology (Figure 1). The system consists of four major components, namely the domain knowledge, the student modeller, the tutoring and the user interface [6, 13, 18].

![](img/ed00a4cd0e7df5eb613c95844dab8a05f64bd69b3d07868c46ca0b12385d1dce.jpg)  
Figure1. Architecture of Web PVT.

The domain knowledge of Web PVT is represented using a semantic network depicting the relations between the concepts of the domain. Each node in the domain knowledge represents a certain category of concept, which may be further divided into smaller sub-concepts. There are three kinds of link between nodes: part-of, is-a, and prerequisite. A part-of relation points from a more general to a more specific concept, which is one of its parts. For example, the "verb tense conversion" concept, is a part of the mundane concepts. An is-a relation, points from an instance of a concept to the concept. For example, there is an is-a relation between the several verb tense forms and the "verb tenses" concept. A precondition relation points from a concept to another, which is its prerequisite. For example, in order to master the simple past tense, one should know how to form irregular verbs.

Web PVT uses a combination of stereotypes and the overlay technique for student modelling [8, 10]. The system uses stereotypes along several dimensions to initialise the student model. These dimensions concern the knowledge level of the student, an estimation of her/his carefulness while solving exercises and her/his prior knowledge of other languages. The student is initially assigned to one of the four distinct stereotypes, namely novice, beginner, intermediate and expert, according to her/his performance on a preliminary test. The system also comprises a long term student model [12], which records information about which concepts the student has mastered and to what extent. In addition, it records the kinds of error the student has made during past interactions as well as the most suitable explanation of each category of error. The information from the long term student model forms an individual model of the student, which together with the active stereotype are used in order to provide adaptive navigation support and perform intelligent analysis of the student's solutions to exercises.

The tutoring component is responsible for making several pedagogical decisions, based on the individual strengths and weaknesses of a student. The tutoring component of Web PVT consults the student model in order to provide adaptive navigation support and to individualise the feedback. Its full functionality is described in the next section.

The user interface of Web PVT consists of a set of dynamically constructed HTML pages and forms. The decision about the content and the form of each page is made by the tutoring component.

# 4. Functionality

Web PVT incorporates techniques from ITS and AH to provide students with individualised instruction and feedback. In particular, the system uses AH techniques, such as adaptive link annotation, to support the navigation of the student through the course material. Furthermore, Web PVT incorporates facilities for intelligent analysis of students’ solutions to exercises. In case an error occurs, it tailors the feedback and advice to the individual student. In this way, advice is individualised to the particular needs of each student.

In the following subsections we analyse the approach taken by Web PVT, to address the above issues.

# 4.1. Adaptive Navigation Support

Due to extra navigational freedom they provide, hyperdocuments impose greater cognitive loads on users than linear documents, such as books on paper or on-line [4]. Therefore, although a good design of the navigation space may help, it is also necessary to provide more sophisticated mechanisms that modify the navigation alternatives by some sort of adaptation procedure [5].

Web PVT uses adaptive annotation of links to guide the student in the navigation process. The idea of adaptive link annotation is to augment the links with some form of comments which can tell the user more about the current state of the nodes behind the annotated links [2].

In particular, Web PVT uses different font types to provide adaptive navigation support. Whenever a link appears in the table of contents or other pages, the font type of the link is annotated so as to reflect the state of the concept behind the link, with respect to the student's current knowledge and misconceptions. The links that are in bold letters point to concepts that are ready to be learned and are recommended by the system. Links that are italicised correspond to concepts that have already been visited and are known to the student. Regular links point to concept pages that have been visited but the student cannot use them correctly while solving exercises. Finally, dimmed links correspond to concepts that are not ready to be learned, since some prerequisite concepts are not known to the student.

# 4.2. Intelligent Analysis of Solutions

In the WWW context, intelligent analysis of solutions is needed to perform error analysis, since the system has to deal with students' final answers to exercises. There are no significant delays, due to the fact that there is only one bi-directional interaction between the client and the server.

In Web PVT, the exercises are presented to students using HTML forms. The student is given a sentence in one voice (active or passive) and is asked to rewrite it using another voice. After solving an exercise, the student submits her/his answer to the server side, which is going to perform analysis of the solution.

ICALL systems have commonly based their error analysis (at least partly) on the mother tongue of the student. A web-based system, however, must adopt a more general scheme in order to accommodate international access [7]. Web PVT, apart from maintaining mal-rules associated with errors due to language transfer, also comprises knowledge about errors that are independent of the mother tongue of a student. Mal-rules related to language transfer are used in case the mother tongue of a student is known (e.g. Greek), while general mal rules are used even in cases we have no information about the native language of the student.

While performing analysis of the student's answer, the system ignores trivial typographic errors such as the absence of a fullstop at the end of the sentence, absence of any space between words, redundant spaces or commas, etc. If the student has made an error other than trivial typographic errors, then the system performs error diagnosis taking into account information that has been collected about the specific user in previous interactions as well as common mistakes that have been identified by the empirical study.

In some cases a mistake of the user may be attributed to more than one categories of error. For example, if a student has typed the word “teacher” instead of “teachers” in the converted sentence, this could either be an accidental slip or a singular/plural mistake. In cases like this the system takes into account the individual features of the user, that have been recorded in previous interactions, in order to formulate the kind of advice to give to her/him. For example, if the particular student has not previously made singular/plural mistakes but has made carelessness mistakes then the system favours carelessness as the most probable cause of the mistake. Based on the results of the error diagnosis, the system is able to provide advice and feedback tailored to the individual student.

# 5. Conclusions and Future Work

In this paper we have described Web PVT, an adaptive web-based ICALL that incorporates techniques from ITS and AH to provide students with individualised instruction and feedback. In particular, the system uses the link annotation technique so as to provide adaptive navigation support. Furthermore, Web PVT is capable of performing error diagnosis and ambiguity resolution based on the long term student model. The design of the diagnostic component has been based on an empirical study that has been held in real classrooms and has shown what the most common students’ mistakes are.

The results of the empirical study have been used for the design of a first version of the system. However, one great advantage of web-based educational technology is that it produces systems that may be accesible by many students. This may serve as a means for collecting more data through the individual student models concerning the most common errors of students belonging to different categories (e.g. students having Greek as their mother tongue). Therefore, there are going to be further refinements based on iterations of empirical studies.

In addition, within the future plans of this research, is the improvement of the student modelling component of Web PVT, so that it may cope with temporal aspects of the student learning process.

# 6. References

[1] S. R. Alpert, M. K. Singley, and P. G. Fairweather, “Deploying Intelligent Tutors on the Web: An Architecture and an Example”, Journal of Artificial Intelligence in Education, 10, 1999, pp. 183-197.   
[2] P. Brusilovsky, “Methods and Techniques of Adaptive Hypermedia”, User Modeling and User Adapted Interaction, 6(2/3), Kluwer, The Netherlands, 1996, pp. 87-129.   
[3] P. Brusilovsky, “Adaptive and Intelligent Technologies for Web-based Education”, Künstliche Intelligenz, 4, 1999, pp. 19- 25.   
[4] L. Calvi, and P. De Bra, “Proficiency-Adapted Information Browsing and Filtering in Hypermedia Educational Systems”, User Modeling and User Adapted Interaction, 7(4), Kluwer, The Netherlands, 1997, pp. 257-277.   
[5] R. Caro, E. Pulido, and P. Rodriguez, “Dynamic Generation of Adaptive Internet-based Courses”, Journal of Network and Computer Applications, 22, Academic Press, 1999, pp. 249-257. [6] J. R. Hartley, and D. H. Sleeman, “Towards intelligent teaching systems”, International Journal of Man-Machine Studies, 5, Academic Press, 1973, pp. 215-236.   
[7] T. Heift, and D. Nicholson, “Theoretical and Practical Considerations for Web-based Intelligent Language Tutoring Systems”, In Gauthier G., Frasson, C., and VanLehn K. (eds.), Lecture Notes in Computer Science: Intelligent Tutoring Systems, Springer, Vienna New York, 2000, pp. 354-363.   
[8] H. Hohl, H. Böcker, and R. Gunzenhäuser, “Hypadapter: An Adaptive Hypertext System for Exploratory Learning and Programming”, User Modeling and User Adapted Interaction, 6(2/3), Kluwer, The Netherlands, 1996, pp. 131-155.   
[9] M. A. Mark, and J. E. Greer, “Evaluation Methodologies for Intelligent Tutoring Systems”, Journal of Artificial Intelligence in Education, 4, 1993, pp. 129-153.   
[10] M. Murphy, and M. McTear, “Learner Modelling for Intelligent CALL”. In Jameson, A., Paris, C. and Tasso, C. (eds.): Proceedings of the Sixth International Conference on User Modeling, Springer, Vienna New York, 1997, pp. 301-312. [11] C. Peylo, W. Teiken, C. Rollinger, and H. Gust, “An Ontology as Domain Model in a Web-based Educational System for Prolog”, In Etheredge J., and Manaris B. (eds) Proceedings of the $I { \ u { 3 } } ^ { t h }$ International Florida Artificial Intelligence Research Society Conference, AAAI Press, Menlo Park CA, 2000, pp. 55- 59.   
[12] E. Rich, “Users are Individuals: Individualizing User Models”, International Journal of Man-Machine Studies, 18, Academic Press, 1983, pp. 199-214.   
[13] J. Self, “The Defining Characteristics of Intelligent Tutoring Systems Research: ITSs Care, Precisely”, International Journal of Artificial Intelligence in Education, 10, 1999, pp. 350-364.   
[14] M. Virvou, and D. Maras, “An intelligent multimedia tutor for English as a second language”. In Collis, B. & Oliver, R. (Eds.) Proceedings of ED-MEDIA 99, World Conference on Educational Multimedia, Hypermedia & Telecommunications, Vol. 2, AACE, Charlottesville, 1999, pp. 928-932.   
[15] M. Virvou, D. Maras, and V. Tsiriga, "Student Modelling in an Intelligent Tutoring System for the Passive Voice of English Language", Educational Technology and Society, 3(4), 2000, pp. 139-150.   
[16] M. Virvou, and V. Tsiriga, "Involving Effectively Teachers and Students in the Life Cycle of an Intelligent Tutoring System", Educational Technology and Society, 3(3), 2000, pp. 511-521.   
[17] G. Weber, and M. Specht, "User Modeling and Adaptive Navigation Support in WWW-based Tutoring Systems", In A. Jameson., C. Paris, and C. Tasso (eds.) Proceedings of the $\boldsymbol { \delta } ^ { t h }$ International Conference on User Modeling, Springer, Vienna New York, 1997, pp. 289-300.   
[18] Wenger, E., Artificial Intelligence and Tutoring Systems, Morgan Kaufman, Los Altos CA, 1987.