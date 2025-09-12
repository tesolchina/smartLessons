---
confidence_score: 0.0
source_file: Rule-based chabot for student enquiries.clean.md
---

# Rule-based Chatbot for Student Enquiries

Jagdish Singh¹, Minnu Helen Joesph², Khurshid Begum Abdul Jabbar³

¹Student, Asia Pacific University  
²Lecturer, Asia Pacific University  
³Lecturer, Asia Pacific University

**Email:** ¹9291js@gmail.com, ²minnu.helen@apu.edu.my, ³khurshid@apu.edu.my

## Abstract

Conversational agents, or chatbots, refer to computer programs that conduct conversations and deliver a natural language interface to its users. Due to the significant foothold messaging applications have begun receiving, chatbots have spawned a new revival and gaining vast popularity. The focus of this paper is to present the implementation of a rule-based enquiry chatbot that is designed exclusively toward students of Asia Pacific University (APU). The implemented chatbot known as 'APU Admin Bot' intends to provide students with a quicker solution to resolving their queries instead of heavily depending on the administrative offices. Relying on the rule-based approach of pattern recognition, certain words, phrases and even actions trigger an entire set of responses from the chatbot. Built entirely from the Chatfuel platform and hosted on Facebook Messenger, the implemented chatbot is reliant on a code-less authoring tool and a messaging platform, instead of traditional programming and architectural structures.

**Index Terms:** Chatbot, Chatfuel, Facebook Messenger, Higher education, Rule-based

## 1. Introduction

In APU, the administrative challenge of quickly and efficiently serving several thousand students across a single location is vastly significant. APU students facing qualms and queries regarding administrative and academic issues such as payment, attendance, and course progressions, often do not know the proper individual(s) to refer to nor the procedures to resolution. Students end up waiting in long lines and undergo multiple runarounds to get a query remedied or problem addressed. These unnecessary hurdles in place leave students with less time working towards their academic goals as well as dissatisfaction with the academic institution. This quandary also impacts the administrative faculty, as additional time is consumed redirecting students with queries that are often repetitive, to the proper channels.

The rule-based chatbot allows students to submit their enquiries via Facebook Messenger, via chat prompts or searching for specific keywords. Utilizing the chatbot enables students to avoid waiting in lines at the APU administrative office for the sake of addressing their personal enquiries. Instead, upon engaging with the chatbot, students will be directed to the suitable individual(s) immediately. Apart from that, administration staffs would be able to improve their efficacies, address serious student concerns and take up additional tasks. The chatbot aims to not only reduce the workload of the administration staffs but to also encourage proper workflow within the administrative function.

## 2. Literature Review

The ensuing subsections present related literature central to the understanding of the paper's key themes.

### 2.1 Rule-based Chatbots

The term "chatbot" was coined by Mauldin [1] to describe systems that could mimic human interaction and thereby pass the Turing Test; an experiment crafted by Alan Turing in the 1950s to assess the intelligence of computer programs. Essentially, the test would involve a human judge who must distinguish reliably based on conversation alone, if a computer program is impersonating a human being in real time [2]. Various chatbots have spawned to pass the Turing Test since its initial conceptualization.

Weizenbaum [3] during his tenure in Massachusetts Institute of Technology (MIT) created ELIZA, the first chatbot, that when given an input sentence, could identify keywords and be able to match those keywords against a collection of pre-defined rules to generate appropriate responses. The development of increasingly intelligent chatbots since ELIZA began to advance; most notably with the creation of PARRY, a bot impersonating a paranoid schizophrenic by [4]. Both bots by [3, 4] abide by the

## International Conference on Computer Vision and Machine Learning

## Chatbot Evolution and Applications

Keywords within the user input, and proceed to craft a reply with the most matching keywords, or the most similar wording pattern, from a database or hard code.

In the early 1980s, ALICE [5] was conceived, momentous not for its conversational capabilities but for its role in the development of Artificial Intelligence Markup Language (AIML). AIML is applied to declare pattern-matching rules that links user-submitted words and phrases with related topic categories. Most chatbot platforms and services as well as complex chatbot projects rely upon AIML.

Over the years, as more evolving technologies were introduced, chatbot capabilities began delving into the realms of artificial intelligence with increased knowledge in areas such as machine learning, data analytics and most importantly, natural language processing (NLP); which gives computers the capability of communication to occur between human-to-machine and machine-to-machine, using natural human language [6]. Chatbots have now began understanding human speech as it is spoken, although the technology itself had not turned mainstream. Alternatively, chatbots may not necessarily have to understand human speech, but can also rely on pattern recognition, abiding by the rule-based approach. Rule-based pattern recognition occurs when chatbots identify certain words, phrases or even actions that trigger an entire set of responses. The benefit of such rules is that they are precise, and allow developers to create and remove rules to handle new situations and address bugs with certainty [7].

## Chatbot Revival

At present, chatbots have spawned a new revival and gained vast popularity due to the significant foothold messaging applications have begun receiving. Shevat [7] believes that the "bot revolution" began as the mobile apps ecosystem quickly become saturated, making it harder and costlier to engage with users. As software providers continued to churn out native mobile experiences, users became increasingly tired of installing and uninstalling these apps. Messaging apps such as Kik, Slack and Facebook were apps that continued to prevail as more users spend their time on these applications; a particularly growing trend with youths [7]. Furthermore, according to Shevat [7], the growth of messaging applications, is indicative to the responsiveness of messaging and the ubiquity of connectivity; desired by present users.

This led Facebook to launch the "Messenger Platform" as an avenue to allow businesses to deploy chatbots for purposes such as business-to-consumer (B2C) customer service, sales and marketing, as well as to pioneer the revival of the chatbot [9]. The user growth for Facebook Messenger itself (the default chat component of social networking site, Facebook) has been on an exponential rise with 600 million users in April 2015, 1 billion in July 2016, and 1.2 billion in April 2017 [10, 11, 12].

As technology developers rekindle their interest in chatbots, educators have also begun examining the offerings that chatbots deliver and assess how it can be used toward pedagogical goals. Deakin University, Australia recently launched its Deakin Explore Bot (DEB), which aims to assist high school students to find career options interactively via Facebook Messenger; DEB asks a series questions, which assess students' interests and capabilities [13]. Upon completion, these students will receive a description of their results and will subsequently be linked to a list of courses in Deakin University. Nerdy Bot is another educational bot available through Facebook Messenger that can handle college-related tasks such as solving math equations, plotting graphs, looking up definitions, and finding historical events [14].

## Chatbots as Customer Relationship Management Tools

The delivery of customer service is paramount to attaining sustainable organization performance, even with institutions of private higher education. These organisations must continuously hone in on customer satisfaction as it eases defection and is positively associated with retention and loyalty [15]. Evidently, customer satisfaction is fundamental to the business philosophy of any firm that aims at the conception of worth for consumers, forestalling and managing end-user expectations, and demonstrating capacity

## International Conference on Computer Vision and Machine Learning

## Customer Relationship Management and Chatbots in Education

Grant and Anderson [20] define CRM as both a business strategy and a set of discrete software tools and technologies, with the goal of identifying new opportunities and improving customer value, satisfaction, profitability, and retention. The use of CRM as a process to ascertain customer needs; comprehending and inducing customer behavior, optimizing quality communications strategies so as to obtain and maintain customer satisfaction [16]. Badwan [18] believes the adoption of CRM measures by educational institutions will cultivate a relationship with consumers that is beyond strictly commercial, unilateral and impersonal.

Chatbots can also be considered as one of many CRM tools that can be utilized by the increasingly corporate private institutions; to further boost its popularity among its students. As a simple automated service, a chatbot can instantaneously respond to student queries and help them resolve their issues whilst enabling administrative staff to attend more complex student needs that demand high-touch interactions. Unfortunately, literature discussing chatbots as CRM tools in higher education (within Malaysia and internationally), or in any other industry is unavailable. The concept of chatbots as illustrated in the previous section, is certainly not new but a gap especially in its application in education is present. Further research and academic endeavors need to be undertaken to abridge the existing gap.

## Materials and Methods

Subsequent subsections detail procedures and methods that went into the formulation of the implemented chatbot.

### System Development Methodology

Various methodologies can be applied to developing the enquiry chatbot, however, the developer has decided to employ the Waterfall model due to certain merits. The Waterfall model utilizes a linear approach; breaking down the project into several sequential phases that feed into the subsequent phases. Due to this rigidity, each phase has specific deliverables, which would enable work to be carried out systematically and all encompassing. This provides better indication of the project direction and progress.

Based on the Waterfall approach, user interaction during development is minimal but substantial upon successful build. End users are brought in to conduct testing and provide feedback if any failures occur or if requirements are not properly fulfilled. This level of user interaction is most suitable for the project, since its scope and program complexity is rather narrow and confined.

Although, the Chatfuel implementation is produced much later into the Waterfall lifecycle; prompting some level of risk and uncertainty within the developer. Much of it will be reduced, once all project requirements are well known, clear and fixed during the initial phase of the methodology. The strict controls within the Waterfall approach would assist in ensuring proper implementation of the enquiry chatbot is performed.

### Research Methods

Two research methods are deployed for the development of the chatbot; interviews and questionnaires. A one-to-one interview, of a semi-structured nature will be the primary method for information gathering. Senior member(s) of the administrative team will be interviewed using several key questions to foster insight on all processes under the APU Administrative arm, the individuals in charge and its underlying dependencies. Upon analysis of data gathered from the interview, the developer can proceed to identify and explore patterns that can be utilized to create the conversational narrative of the chatbot.

Subsequently, a mixed questionnaire was applied to elicit feedback from APU students as part of the Requirements Analysis phase to identify and explore areas that can be further enhanced to meet end user needs on top of rectifying any overlooked matters. It is vital that questions are coupled with its corresponding objective to properly ascertain the end user's experience. Usage of Google Forms is highly recommended as it would enable better data tabulation and visualization.

### Analysis

The goal of analysis is to produce some inferences, lessons or conclusions by concentrating and segmenting large amounts of data into relatively small, compacted fragments of understandable information. Findings from the interview were documented via tape recording and note taking. The analysis of data gathered from the interview begins with the categorization of data according to specific themes as part of the coding process. An affinity diagram will be devised from the outcome of previous coding. The gathered data will then be constructed into a flowchart, which would eventually enable the developer to use

## International Conference on Computer Vision and Machine Learning

## Results and Discussion

Major results and findings with regards to the paper are highlighted below.

### Interview

The goal of analysis is to produce some inferences, lessons or conclusions by concentrating and segmenting large amounts of data into relatively small, compacted fragments of understandable information. Findings from the interview were documented via tape recording and note taking. The analysis of data gathered from the interview begins with the categorization of data according to specific themes as part of the coding process. An affinity diagram will be devised from the outcome of previous coding. The gathered data will then be constructed into a flowchart, which would eventually enable the developer to use the flowchart as a foundation for program design on Chatfuel.

### Questionnaire

The goal of analysis is to produce some inferences, lessons or conclusions by concentrating and segmenting large amounts of data into relatively small, compacted fragments of understandable information. Findings from the interview were documented via tape recording and note taking. The analysis of data gathered from the interview begins with the categorization of data according to specific themes as part of the coding process. An affinity diagram will be devised from the outcome of previous coding. The gathered data will then be constructed into a flowchart, which would eventually enable the developer to use the flowchart as a foundation for program design on Chatfuel.

## Conclusions

The subsequent segments aim to highlight and describe main conclusions of the work presented.

### Degree of Success

The proposed "APU Admin Bot" had fulfilled necessary user requirements that were initially gathered during the primary research phase as well as completely satisfying project objectives. The developed chatbot has an extremely simple user interface, which allows users to view information and interact with the chatbot regarding enquiries, rather effortlessly. The beauty of the developed chatbot is that it is accessible to all APU students anytime and anywhere, provided they are connected to the internet and have downloaded the Facebook Messenger application on their mobile devices. Alternatively, the chatbot could also be retrieved via the bot's app page on Facebook for access via laptop or computer devices.

### Limitations

There are several drawbacks to the developed chatbot. Firstly, the develop chatbot does not offer back-end access to actors such as Admin employees or system administrators. Hence, future modifications to the information retained by the chatbot cannot be updated. Possible changes, such as reorganized or restructured administrative processes are highly probably in the future. Secondly, the developed chatbot is unable to produce highly personalized information, according to the specific needs of each individual student. Instead, much of its responses informs student on what to do, on a very general basis. This would at least provide students with a starting point in resolving their enquiries, but perhaps not a complete resolution. Relevant examples would be arranging for a Special Arrangement Exam, a resit or a retake. Thirdly, in terms of functionality, it is rather evident that users are only able to either navigate thru the bot via chat prompts or search for specific keywords to obtain a response. This could be seen as a major limitation as not much can be done by the chatbot.

### Future Enhancements

Several improvements can be made to the developed chatbot to further enhance its effectivity. Firstly, a back-end or a separate interface can be created specifically for admin staff or system administrators to edit existing components of the APU Admin Bot or even possibly expand to include even more detailed components. Next, the developed chatbot could also be increasingly personalized to cater individual needs by pulling student data from APU student database(s). Formulating a mechanism where such personal details can be extracted and be included in resolving queries, would bring additional benefits to both students and the administrative arm. Lastly, with regards to functionality, it is possible for the developed chatbot to incorporate some real-time information, such as the queue at the Administrative office. Other common functionalities that could be added include a feedback or rating capability, providing the option of interacting with a live human agent, or even booking appointments with administrators, or other related actors.

## References

1. M L Mauldin

## References

1. J. Weizenbaum, "Computational Linguistics," Communications of the ACM, vol. 9, no. 1, pp. 36-45, January 1966.

2. A. Deshpande et al., "A Survey of Various Chatbot Implementation Techniques," International Journal of Computer Engineering and Application, vol. 6, May 2017.

3. R. Wallace, "The elements of AIML style," March 2003.

4. V. Sharma, M. Goyal, and D. Malik, "An Intelligent Behaviour Shown by Chatbot System," International Journal of New Technology and Research, vol. 3, no. 4, pp. 52-54, 2017.

5. M. Yuan, "A developer's guide to chatbots," Aug. 10, 2016.

6. A. Shevat, "Designing Bots," 1st ed., USA: O'Reilly Media, 2017.

7. M. Isaac, "Facebook Bets on Bots for Its Messenger App," The New York Times, April 12, 2016.

8. J. Constine, "Facebook Messenger Launches Free VOIP Video Calls Over Cellular And Wi-Fi," TechCrunch, April 27, 2015.

9. M. Singleton, "Facebook Messenger hits 1 billion users," Vox Media, July 20, 2016.

10. K. Wagner and R. Molla, "Facebook Messenger has 1.2 billion users and is now twice the size of Instagram," Vox Media, April 12, 2017.

11. G. Li, "Will a chat bot be your new best friend," 2017.

12. Nerdify, "Nerdy Bot - Home Page," 2017.

13. O. O. Oluseye, T. B. Tairat, and O. Emmanuel, "Customer Relationship Management Approach and Student Satisfaction in Higher Education Marketing," Journal of Competitiveness, vol. 6, no. 6, pp. 49-62, September 2014.

14. K. A. George et al., "The impact of effective customer relationship management (CRM) on repurchase: A case study of (GOLDEN TULIP) hotel (ACCRA-GHANA)," African Journal of Marketing Management, vol. 4, no. 1, pp. 17-29, January 2012.

15. E. D. Seeman and M. O'Hara, "Customer relationship management in higher education: Using information systems to improve the student-school relationship," Campus-Wide Information Systems, pp. 24-34, January 2006.

16. J. J. Badwan et al., "Adopting Technology for Customer Relationship Management in Higher Educational Institutions," International Journal of Engineering and Information Systems (IJEAIS), vol. 1, no. 1, pp. 20-28, March 2017.

17. M. Abubakar and S. Mukhtar, "Relationship Marketing Long Term Orientation and Customer Loyalty in Higher Education," Mediterranean Journal of Social Sciences, vol. 6, no. 4, pp. 466-474, July 2015.