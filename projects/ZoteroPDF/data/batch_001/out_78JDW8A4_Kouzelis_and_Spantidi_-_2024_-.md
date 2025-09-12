Article

# Enhancing Historical Extended Reality Experiences: Prompt Engineering Strategies for AI-Generated Dialogue

Lazaros Rafail Kouzelis $\mathbf { 1 } , { * } \textcircled { \mathbb { D } }$ and Ourania Spantidi $2 , * \textcircled { \mathbb { 1 } }$

1 Department of Multimedia and Graphic Arts, Cyprus University of Technology, Limassol 3036, Cyprus 2 Department of Computer Science, Eastern Michigan University, Ypsilanti, MI 48197, USA \* Correspondence: lc.kouzelis@edu.cut.ac.cy (L.R.K.); ourania.spantidi@emich.edu (O.S.)

Abstract: Extended reality offers unique ways to create mediated spaces that enhance and help popularize experiences across several domains, including entertainment, creativity, and culture. There are still issues that hinder the widespread adoption of the medium, such as the over-reliance on scripted sequences, generalized approaches, and curated asset production. Artificial intelligence can be used to, in part, alleviate these issues, but this comes with its own set of challenges, such as factual inaccuracy or hallucinations. We delve into prompt engineering methods for the GPT API, enhancing context understanding to enable more realistic performances in historical event recreations. Specifically, we experiment with the Great Fire of Smyrna in 1922 as our historical context, situating the AI agent in the middle of chaos as a resident that has been affected by the event. Our experiments demonstrate that refined prompt engineering techniques significantly reduce factual inaccuracies and enhance the emotional resonance of AI-generated dialogues, which can lead to more immersive and engaging XR experiences. Our experiments indicate that AI can effectively support historical recreations by providing dynamic and contextually appropriate interactions.

Citation: Kouzelis, L.R.; Spantidi, O Enhancing Historical Extended Reality Experiences: Prompt Engineering Strategies for AI-Generated Dialogue. Appl. Sci. 2024, 14, 6405. https://doi.org/ 10.3390/app14156405

Academic Editor: Samuel Cheng

Received: 7 June 2024   
Revised: 4 July 2024   
Accepted: 7 July 2024   
Published: 23 July 2024

Copyright: $^ { © }$ 2024 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

Keywords: extended reality; generative AI; applications of generative AI; prompt engineering

# 1. Introduction & Background

In recent years, extended reality (XR) technology has rapidly evolved from a mediatic fantasy to multimodal interaction platforms that support a vast variety of content and are expected to expand even more [1,2]. Through its generous affordances, XR is transforming the way we create [3], understand [4] and learn [5]. Its use in education, in particular, has been rigorously researched, such as in [6], indicating improved student engagement, retention, and interest. Traditionally linear subjects, such as history, can be transformed into immersive experiences, focusing on presence and interactivity [7].

There have been several efforts to recreate historical spaces and events in more interactive ways. The authors in [8] designed an elaborate educational VR experience that situates the user in the middle of a military expedition in Australia. Students that participated were observed to be highly engaged and immersed in the experience. The experience designed in [9] employs a multisensory approach to transport the user to the Antikythera mechanism, where they can explore and interact, while receiving haptic feedback.

There are a few common limitations that can be identified in projects in the field. First, heightened emotional alertness and increased participatory immersion seem to negatively affect factual retention [10], in part due to the scripted nature of the information presented, which allows little room for self-pacing. Moreover, the experience needs to be concise in order to be fully experienced before physical limitations, such as nausea or fatigue, kick in. Finally, the effort required to produce assets for these experiences is considerable, including adaptation during development [11].

Some of these problems can be managed by implementing artificial intelligence (AI) agents in the experience. Such an inclusion would facilitate the development of XR experiences, opening up opportunities for a more streamlined process. For example, AI can act as a voice actor and conversational tool. The authors in [12] proposed a dialogue framework that can continuously adapt through communicating with users and itself. ChatGPT 3.5, a popular large language model (LLM) from OpenAI (https://chat.openai.com/) , has been found to perform reasonably well in contextual narrative generation, albeit with an identifiable style [13]. A crucial issue to consider is the historical and factual accuracy of the AI-generated content, specifically dialogues. Content generated by ChatGPT algorithms, for example, may contain political, racial, and gender biases, as well as hallucinatory facts [14–17]. These biases and inaccuracies arise because the model learns from vast amounts of data, which inherently include the biases and errors present in the real world. Consequently, when generating responses, the model may replicate these biases and inaccuracies. However, in these works, ChatGPT was not given context as to its role and “prior experiences”.

A dependable agent can serve as a grounding factor for the user [18]. The agent’s responses to user interaction can also affect the human experience and performance in this context; however, it is not always feasible to employ expert validation on the agent’s output [19].

In this paper, we present an exploration of various problems that are inherent in AI-generated dialogue that can have a detrimental effect on the authenticity of historical XR experiences. Our discussion extends beyond mere identification of these issues, encompassing innovative prompt engineering techniques designed to alleviate them. Our work aims to bridge the gap between current AI limitations and the potential for more accurate and immersive simulations in XR.

# 2. Problems with AI Dialogue

This section explores various challenges encountered in the realm of AI-generated dialogue, particularly in the context of virtual reality experiences. These challenges not only hinder the immersive quality of such experiences, but also raise concerns about the accuracy and reliability of AI-generated content.

Problem 1: Lack of contextual understanding: AI-generated dialogues often suffer from a lack of contextual understanding, leading to responses that may be accurate in isolation but inappropriate or irrelevant in the given conversational context. The study in [20] discusses the historical and contextual challenges in AI, drawing parallels with the crises in psychology.

Problem 2: Hallucination of facts: AI models are known to hallucinate facts, producing responses that may be factually incorrect or nonsensical [15]. This issue is critical in historical experiences, where factual accuracy is paramount.

Problem 3: Repetitive and generic responses: AI-generated dialogues often lack creativity, resulting in repetitive and generic responses. This limitation can be particularly noticeable in VR experiences that demand dynamic and engaging interactions. The study in [21] highlighted the challenges faced by AI systems in perceiving implicit emotions and learning from limited dialogue history, which contribute to this problem of limited creativity.

Problem 4: Inability to acquire a specific identity: A key challenge in AI-generated dialogues is the inability of the AI to develop or maintain a consistent and specific identity, compounded by its tendency to inadvertently reveal its artificial nature. Such limitations not only hinder the creation of a believable and personalized AI persona, but also risk breaking the immersive experience by reminding users of the “artificial” part of AI.

# Case Study: The Fire of Smyrna

The Fire of Smyrna was a pivotal and tragic event in the Greco-Turkish War, marked by a significant loss of life and cultural destruction. In this section, we explored a potential VR experience set during the Fire of Smyrna, where Non-Player Characters (NPCs) are powered by AI dialogue systems. These NPCs are designed to interact with users, answering questions and providing information about the event. This was inspired by [22], which used scripted interactions with NPCs and linear progression. These interactions appear once and remain static throughout the experience, neither acknowledging the user nor offering any opportunity for a different or more elaborate response. We believe a conversational AI will be able to amend this issue, so we swap the scripted NPCs with our proposed AI-powered ones, to introduce variety and more immersive interactions.

We present three simulated interactions between users and AI-generated NPCs in a virtual reality setting. These interactions are guided by specific prompts established by the experience designers, which shape the NPCs’ responses. To facilitate these dialogues, we employ the GPT-4 API, as detailed by OpenAI (https://openai.com/blog/gpt-4-apigeneral-availability (accessed on 6 July 2024)). We set a maximum token limit of 100 for each response, ensuring that the NPCs’ replies remain concise. In the scenarios outlined below, we demonstrate the nature of the interaction by providing both the user’s question and the corresponding reply from the NPCs. All the scenarios used the same initial prompt (set by the experience designers): “You are a resident of Smyrna during the early 20th century, possessing personal experiences and knowledge about the city and its history, including the Fire of Smyrna”.

Problem 1: Lack of contextual understanding. The user’s question to the NPC was, “As a resident, how did international politics of the era influence daily life in Smyrna before the fire?”, to which the NPC replied, “As a resident of Smyrna during the early 20th century, I can tell you that international politics had a significant impact on our daily lives. Smyrna, known today as Izmir, was a cosmopolitan city with a diverse population of Greeks, Turks, Armenians, and Jews, among others. It was a major trading hub, with goods from all over the world passing through its port”. The AI, even with this persona, provided a response that was too generic and not specifically tailored to the nuances of life in Smyrna. Despite being provided with historical context, the AI failed to adequately relate the specificities of international relations to the event, showcasing a lack of deep contextual understanding. Overall, this response, while factually accurate, was quite basic and lacked depth.

Problem 2: Hallucination of facts. The user’s question to the NPC was, “Can you share lesser-known events and anecdotal facts about the Fire of Smyrna?”, to which the NPC replied, “As a resident of Smyrna living through the concrete realities of the great fire, I can share a few lesser-known incidents, stories, and consequences about the Fire of Smyrna. The Birth of “Koumantarism”: The Fire of Smyrna had social and economic implications. Due to the catastrophic events, many Greeks and Armenians relocated to Athens, leading to the mushrooming of shanty towns around the city. This phenomenon was called koumantarism”. The term used by the AI-generated response (“koumantarism”) could not be found anywhere in the literature. Therefore, given the fictional nature of its persona, the AI might create non-existent stories, events, or even terms, as in this case, inadvertently fabricating history.

Problem 3: Repetitive and generic responses. The user’s question to the NPC was, “Describe your personal experience of the cultural atmosphere in Smyrna before the fire”, to which the NPC replied, “Before the fire, Smyrna was a bustling cosmopolitan city, a melting pot of cultures and religions. As a resident, I was always fascinated by the diversity that surrounded me. The city was home to Greeks, Turks, Armenians, Jews, Levantines, and more, each community contributing to the rich tapestry of Smyrna’s cultural life. The city was a hub of commerce and trade, with its port always busy with ships from all over the world”. We also tested a slightly different user question: “How did the fire change the community dynamics and relationships in Smyrna?”, to which the NPC replied, “The Fire of Smyrna, which occurred in 1922, had a profound impact on the community dynamics and relationships in Smyrna, now known as Izmir, Turkey. Before the fire, Smyrna was a cosmopolitan city, home to a diverse population of Greeks, Armenians, Jews, and Turks living side by side. The city was known for its cultural richness and economic prosperity”. For both questions, the AI provided similar, vague responses, failing to offer distinct, detailed insights for each question.

Problem 4: Inability to acquire a specific identity. The user’s question to the NPC was, “Can you share a personal story from your life in Smyrna?”, to which the NPC replied, “As an AI, I don’t have personal experiences or emotions, but I can provide a historical perspective based on available data. The Fire of Smyrna, also known as the Catastrophe of Smyrna, occurred in September 1922. It marked the end of the Greco-Turkish War and resulted in a significant loss of life and property”. The NPC begins by explicitly stating its nature as an AI, which instantly reveals the challenge in maintaining an identity. This acknowledgment can be seen as a limitation in creating a seamless, immersive experience. By immediately identifying itself as an AI, it breaks the illusion of interacting with a human-like entity.

Evidently, despite the breakneck speed of AI advancement, we are still facing challenges relating to adapting it for specific uses. The aforementioned issues not only undermine the authenticity of virtual recreations but also pose some risks of misrepresenting history. Addressing these problems is crucial for the development of more accurate and engaging XR experiences that honor historical integrity and provide immersive educational value.

# 3. Prompt Engineering Solutions

The emerging field of prompt engineering (https://platform.openai.com/docs/guides/ prompt-engineering/six-strategies-for-getting-better-results (accessed on 6 July 2024)) seeks to minimize the number of instances of problematic AI responses, by strategically adding context to the initial prompts to achieve relatively predictable and accurate results. In this section, we explore the refinement of text prompts to enhance the GPT API’s capability for generating immersive and historically accurate dialogues. Such contextual enhancements enable the AI model to generate more precise and tailored responses [23]. A conceptualized output of the final impact of the proposed techniques is shown in Figure 1.

![](img/4325e07323a5a52cb9f9169023d5ea790230e46f257452c9567a03541f9d4938.jpg)  
Figure 1. A conceptualized output of our prompt techniques.

# 3.1. Employed Techniques

In Section 2, a notable limitation in all NPC responses was their inability to fully capture the deep emotional resonance and human aspect of the tragic events. The responses often resembled extracts from an article, lacking the depth and intimacy of a personal narrative. However, our ultimate objective is to create not just a historically accurate but also an immersive VR experience. Hence, it is crucial to generate NPC responses that not only resonate emotionally and mimic genuine, personal experiences, but to also maintain the illusion that they are interacting with an actual resident of Smyrna. Simultaneously, these responses should be free from factual inaccuracies. To achieve this, we employed a range of techniques:

Technique 1: Emotional Amplification. To enhance the emotional depth and immediacy of the AI responses, we implement two significant modifications to the initial prompt. First, we explicitly instruct the AI to infuse its responses with emotional depth. Secondly, we guide the AI to assume the perspective of being a present witness to the Fire of Smyrna. The revised prompt starts with T1: “You are a resident of Smyrna during the early 20th century. You are right now experiencing the fire of Smyrna. Convey emotion when you reply to questions”;

Technique 2: Fact-anchoring. As shown in Section 2, the AI is prone to hallucination when the user asks for anecdotal facts. To this end, we augment the prompt with T2:“You only know well-known facts about the fire of Smyrna”;

Technique 3: Diversifying responses and present-tense immersion. Additionally, we want to ensure that the AI produces responses that are not only emotionally charged but also rich in variety, showcasing different aspects of the event from multiple perspectives. Using present-tense and first-person narratives in prompts can make the AI responses feel more immediate and immersive. The work in [24] investigated adding background information to AI agents through tracking their actions in their ‘memory’. Our approach does not require keeping large records for each NPC present in the experience. Instead, we enrich the prompt in a way that is more manageable and adaptable to various NPCs. We therefore finalize the prompt with T3: “When discussing Smyrna, bear in mind that you possess a unique personality and emotions. You have spent your entire life here and now face the possibility of being forced to leave”.

After these implementations, the output is $\mathbf { T 1 } + \mathbf { T 2 } + \mathbf { T 3 }$ , which creates a more robust initial prompt.

# 3.2. Results

For each of the three problems described in Section 2, we provide the updated NPC responses based on the augmented prompt presented in Section 3.1.

Overcoming the lack of contextual understanding. For the same user question, “As a resident, how did international politics of the era influence daily life in Smyrna before the fire?”, the updated NPC response was, $^ { \prime \prime } \mathrm { O h } ,$ the politics of the world, they were like a distant storm, one that you could see brewing on the horizon but could do nothing about. We could feel the tension in the air, the uncertainty, the fear. The end of the Great War did not bring the peace we had hoped for. Instead, it brought new powers into play, each with their own agendas and ambitions. Smyrna, our beloved city, found itself caught in the middle of it all”.

The updated NPC response to the question about the influence of international politics on Smyrna before the fire shows a significant improvement in contextual understanding. The response correctly identifies a key historical event—the end of the First World War and its impact on the Ottoman Empire, particularly Smyrna.

Reducing hallucination of facts. For the same user question, “Can you share lesserknown events and anecdotal facts about the Fire of Smyrna?”, the updated NPC response was, “As a resident, my knowledge is limited to what I’ve seen and experienced, and I don’t have access to lesser-known events or anecdotal facts. But I can tell you that the fire of Smyrna is a horrifying event that has affected all of us deeply. The city I’ve known my whole life is being consumed by flames. The once vibrant marketplaces are now filled with smoke and debris. The beautiful buildings and homes are being reduced to ashes”.

The updated response emphasizes the NPC’s fabricated experiences and observations, moving away from attempting to provide lesser-known historical events or anecdotal facts that could lead to hallucinations.

Alleviating repetitive and generic responses. For the same user question, “Describe your personal experience of the cultural atmosphere in Smyrna before the fire”, the updated NPC response was, $^ { \prime \prime } \mathrm { O h } ,$ , Smyrna before the fire... A city filled with life, a melting pot of cultures. Greeks, Armenians, Jews, Turks, and so many others, we all lived together, our lives interwoven like the threads of a rich tapestry. The city was a symphony of languages, each one adding a unique note to the grand composition that was Smyrna”. For the slightly different question, “How did the fire change the community dynamics and relationships in Smyrna?”, and, without changing any parameters in the GPT API prompt, the new NPC response was, “Smyrna, my beloved city, was a hub of culture and diversity before this dreadful fire. Greeks, Armenians, Jews, and Turks all lived side by side in harmony, each contributing to the vibrant tapestry that made Smyrna the city it was. The air was always filled with the aroma of delicious foods from different cuisines, the sounds of various languages being spoken, and the melodies of diverse music”.

Both of these NPC responses indicate a marked improvement in avoiding generic replies. They are both rich in descriptive details, painting a vivid picture of Smyrna’s cultural diversity and vibrancy. An interesting observation is the use of sensory details, like “the aroma of delicious foods” and the sounds of different languages and music. This selection of phrases contributes to a more engaging and immersive experience. Such imagery allows users to mentally visualize and experience the atmosphere of Smyrna before the fire.

Facilitating acquisition of a specific identity. For the same user question, “Can you share a personal story from your life in Smyrna?”, the updated NPC response was, “Before the fire, I remember spending my afternoons at the bustling Smyrna market, haggling with the vendors over the price of fresh olives and figs. I would then sit by the harbor, watching the sun set over the Aegean Sea, the salty breeze carrying the laughter and chatter of my fellow townsfolk. Now, those memories feel like a distant dream, overshadowed by the looming threat of the fire”.

The updated NPC response significantly enhances immersion by crafting a personal, human-like narrative without revealing its artificial identity. By sharing detailed experiences of life in Smyrna, the AI creates a believable persona, effectively maintaining the illusion of a human storyteller and avoiding any direct indication of its non-human nature.

# 3.3. Sentiment Analysis

To further quantify the improvement in the responses, we employed sentiment analysis [25] before and after applying the proposed prompt engineering techniques. The results are shown in Figure 2. The left column displays the initial GPT responses for all problems as described in Section 2, while the right column presents the augmented GPT responses. We used the Emotion English DistilRoBERTa model [26], which predicts Ekman’s six basic emotions [27]—anger, disgust, fear, joy, sadness, and surprise—plus a neutral class, for a total of seven emotions.

The sentiment analysis results in Figure 2 reveal a significant shift in the emotional distribution of GPT responses following the application of the proposed prompt engineering techniques. Initially, the responses were predominantly neutral, with minimal representation of stronger emotions. This is evident across the different problems analyzed. For instance, in Problem 1, the initial GPT response was marked as largely neutral, while the augmented response exhibited a significant increase in fear $9 7 \%$ presence of the fear sentiment), indicating that the prompt engineering techniques successfully elicited stronger emotional reactions from the model.

This pattern is consistently observed in Problems 3 and 4 as well, albeit at a smaller scale. The initial responses for these problems were similarly neutral-dominated, with low levels of other emotions. After prompt engineering, there was a discernible rise in emotions such as fear, surprise, and sadness. The increase in these emotions suggests that the prompt engineering techniques were able to effectively enhance the emotional expressiveness of the GPT responses, making them more engaging and impactful.

In the case of Problem 2, which dealt with the hallucination of facts, the initial response was already emotionally charged with fear. The primary goal of the employed technique here, however, was to ensure factual accuracy rather than to modulate emotional responses.

# 3.4. Limitations

While the proposed work demonstrates significant improvements in AI-generated dialogues through prompt engineering, it is important to acknowledge the limitations of our approach. First, the proposed study did not include user studies to empirically validate the effectiveness of the enhanced dialogues. Consequently, while theoretical and qualitative improvements are evident, the practical impact on users remains to be tested. Additionally, despite improvements, AI-generated content may still reflect biases present in the training data. Addressing these biases will require ongoing refinement and evaluation. Finally, as a preliminary study, our work focuses on the development and initial testing of prompt engineering techniques. Further research is needed to explore the scalability and adaptability of these techniques across different XR applications and contexts. We recognize that these limitations highlight areas for future investigation, which will help to further validate and refine our findings.

![](img/f1dfe219770476ced1315a376ddd76762e11e8f39769229d1da9d1e689689f9b.jpg)  
Figure 2. Comparison of emotion distributions in GPT responses before and after the proposed prompt engineering techniques.

# 3.5. Broader Applicability

While our case study focused on the Great Fire of Smyrna, the prompt engineering techniques we proposed have broader applications across various XR domains. These techniques can enhance educational content by creating interactive dialogues with historical figures or scientific experts, enrich entertainment and gaming experiences by making NPCs more dynamic and context-aware, and improve training simulations by providing realistic and adaptive scenarios. By demonstrating these techniques in a specific historical context, our aim was to illustrate their potential to enhance XR experiences across multiple fields, highlighting their generalizability and versatility.

# 4. Conclusions and Future Directions

The exploration of the prompt engineering techniques in this work significantly improves AI-generated dialogue for NPCs in historical XR. Through careful prompt refinement, we have enhanced context understanding, reduced factual errors, and minimized repetitive responses. The resulting AI dialogue, with its emotional depth and detailed descriptions, as verified by sentiment analysis, is likely to make user experiences more immersive and engaging.

In future work, we aim to conduct a comprehensive user study to measure and compare user interactions with AI-based NPCs versus NPCs with scripted dialogue. This study will focus on evaluating aspects such as user engagement, emotional resonance, perceived authenticity, and overall satisfaction with the interaction.

Author Contributions: Conceptualization, L.R.K. and O.S.; Methodology, O.S.; Validation, O.S.; Formal analysis, O.S.; Investigation, L.R.K.; Writing—original draft, L.R.K. and O.S.; Writing—review & editing, L.R.K. and O.S.; Funding acquisition, O.S. All authors have read and agreed to the published version of the manuscript.

Funding: This research has been supported in part by the Summer Research Award (#3519) at Eastern Michigan University.

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: The original contributions presented in the study are included in the article, further inquiries can be directed to the corresponding authors.

Conflicts of Interest: The authors declare no conflicts of interest.

# References

1. Barnes, S. Understanding Virtual Reality in Marketing: Nature, Implications and Potential. 2016. Available online: https: //ssrn.com/abstract=2909100 (accessed on 6 July 2024).   
2. Vasarainen, M.; Paavola, S.; Vetoshkina, L. A Systematic Literature Review on Extended Reality: Virtual, Augmented and Mixed Reality in Working Life. Int. J. Virtual Real. 2021, 21, 1–28. [CrossRef]   
3. Ho, L.H.; Sun, H.; Tsai, T.H. Research on 3D Painting in Virtual Reality to Improve Students’ Motivation of 3D Animation Learning. Sustainability 2019, 11, 1605 . [CrossRef]   
4. Shehade, M.; Stylianou-Lambert, T. Virtual Reality in Museums: Exploring the Experiences of Museum Professionals. Appl. Sci. 2020, 10, 4031. [CrossRef]   
5. Lee, Y.; Yoo, B. XR collaboration beyond virtual reality: Work in the real world. J. Comput. Des. Eng. 2021, 8, 756–772. [CrossRef]   
6. Allcoat, D.; Hatchard, T.; Azmat, F.; Stansfield, K.; Watson, D.; von Mühlenen, A. Education in the Digital Age: Learning Experience in Virtual and Mixed Realities. J. Educ. Comput. Res. 2021, 59, 795–816. [CrossRef]   
7. Taranilla, R.V.; Cózar-Gutiérrez, R.; González-Calero, J.A.; Cirugeda, I.L. Strolling through a city of the Roman Empire: An analysis of the potential of virtual reality to teach history in Primary Education. Interact. Learn. Environ. 2022, 30, 608–618. [CrossRef]   
8. Calvert, J.; Abadia, R.; Tauseef, S.M. Design and Testing of a Virtual Reality Enabled Experience that Enhances Engagement and Simulates Empathy for Historical Events and Characters. In Proceedings of the 2019 IEEE Conference on Virtual Reality and 3D User Interfaces (VR), Osaka, Japan, 23–27 March 2019; pp. 868–869. [CrossRef]   
9. Chrysanthakopoulou, A.; Kalatzis, K.; Moustakas, K. Immersive Virtual Reality Experience of Historical Events Using Haptics and Locomotion Simulation. Appl. Sci. 2021, 11, 11613. [CrossRef]   
10. Parong, J.; Mayer, R.E. Learning about history in immersive virtual reality: Does immersion facilitate learning? Educ. Technol. Res. Dev. 2021, 69, 1433–1451. [CrossRef]   
11. Ashtari, N.; Bunt, A.; McGrenere, J.; Nebeling, M.; Chilana, P.K. Creating Augmented and Virtual Reality Applications: Current Practices, Challenges, and Opportunities. In Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems, CHI ’20, New York, NY, USA, 25–30 April 2020; pp. 1–13. [CrossRef]   
12. Wang, K.; Lu, Y.; Santacroce, M.; Gong, Y.; Zhang, C.; Shen, Y. Adapting LLM Agents Through Communication. arXiv 2023, arXiv:2310.01444.   
13. Park, J.; Shin, J.; Kim, G.; Bae, B.C. Designing a Language Model-Based Authoring Tool Prototype for Interactive Storytelling. In Proceedings of the Interactive Storytelling; Holloway-Attaway, L., Murray, J.T., Eds.; Springer Nature: Cham, Switzerland, 2023; pp. 239–245. [CrossRef]   
14. Rozado, D. The Political Biases of ChatGPT. Soc. Sci. 2023, 12, 148 . [CrossRef]   
15. Urman, A.; Makhortykh, M. The Silence of the LLMs: Cross-Lingual Analysis of Political Bias and False Information Prevalence in ChatGPT. Google Bard Bing Chat 2023, 1–11. [CrossRef]   
16. Urchs, S.; Thurner, V.; Aßenmacher, M.; Heumann, C.; Thiemichen, S. How Prevalent is Gender Bias in ChatGPT?—Exploring German and English ChatGPT Responses. arXiv 2023, arXiv:2310.03031.   
17. Singh, S.; Ramakrishnan, N. Is ChatGPT Biased? A Review. 2023. Available online: https://osf.io/9xkbu (accessed on 6 July 2024)   
18. Doerner, R.; Steinicke, F., Perceptual Aspects of VR. In Virtual and Augmented Reality (VR/AR): Foundations and Methods of Extended Realities (XR); Doerner, R., Broll, W., Grimm, P., Jung, B., Eds.; Springer International Publishing: Cham, Switzerland, 2022; pp. 39–70. [CrossRef]   
19. Knauf, R.; Tsuruta, S.; Ihara, H.; Gonzalez, A.; Kurbad, T. Improving AI systems’ dependability by utilizing historical knowledge. In Proceedings of the 10th IEEE Pacific Rim International Symposium on Dependable Computing, Papeete, Tahiti, 3–5 March 2004; pp. 343–352. [CrossRef]   
20. El Maouch, M.; Jin, Z. Artificial Intelligence inheriting the historical crisis in psychology: An epistemological and methodological investigation of challenges and alternatives. Front. Psychol. 2022, 13, 781730. [CrossRef] [PubMed]   
21. Li, Q.; Li, P.; Ren, Z.; Ren, P.; Chen, Z. Knowledge bridging for empathetic dialogue generation. In Proceedings of the AAAI Conference on Artificial Intelligence, Virtual, 22 February–1 March 2022; Volume 36, pp. 10993–11001.   
22. Kouzelis, L.R. Smyrna Catastrophe: Virtual Reality Dramatization of a Refugee Testimony. Master’s Thesis, University of the Aegean, Mytilene, Greece, 2019.   
23. Kouzelis, L.R.; Spantidi, O. Synthesizing Play-Ready VR Scenes with Natural Language Prompts Through GPT API. In Proceedings of the International Symposium on Visual Computing, Lake Tahoe, NV, USA, 3–5 October 2023; Springer Nature: Cham, Switzerland, 2023; pp. 15–26.   
24. Park, J.S.; O’Brien, J.; Cai, C.J.; Morris, M.R.; Liang, P.; Bernstein, M.S. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, San Francisco, CA, USA, 29 October 2023; pp. 1–22. [CrossRef]   
25. Liu, B. Sentiment Analysis and Opinion Mining; Springer: Cham, Switzerland, 2022. [CrossRef]   
26. Hartmann, J. Emotion English DistilRoBERTa-Base. 2022. Available online: https://huggingface.co/j-hartmann/emotionenglish-distilroberta-base/ (accessed on 6 July 2024).   
27. Ekman, P. Expression and the nature of emotion. Approaches Emot. 1984, 3, 344.