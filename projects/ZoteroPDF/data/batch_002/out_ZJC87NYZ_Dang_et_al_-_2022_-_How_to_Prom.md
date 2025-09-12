# How to Prompt? Opportunities and Challenges of Zero- and Few-Shot Learning for Human-AI Interaction in Creative Applications of Generative Models

Hai Dang   
hai.dang@uni-bayreuth.de   
Research Group $\mathrm { H C I } + \mathrm { A I }$ ,   
Department of Computer Science,   
University of Bayreuth   
Bayreuth, Germany   
Lukas Mecke   
lukas.mecke@unibw.de   
Bundeswehr University Munich   
Munich, Germany   
LMU Munich   
Munich, Germany   
Florian Lehmann   
florian.lehmann@uni-bayreuth.de   
Research Group HCI + AI,   
Department of Computer Science,   
University of Bayreuth   
Bayreuth, Germany   
Sven Goller   
sven.goller@uni-bayreuth.de   
Research Group HCI + AI,   
Department of Computer Science,   
University of Bayreuth   
Bayreuth, Germany   
Daniel Buschek   
daniel.buschek@uni-bayreuth.de   
Research Group $\mathrm { H C I } + \mathrm { A I }$ ,   
Department of Computer Science,   
University of Bayreuth   
Bayreuth, Germany

# ABSTRACT

Deep generative models have the potential to fundamentally change the way we create high-fidelity digital content but are often hard to control. Prompting a generative model is a promising recent development that in principle enables end-users to creatively leverage zero-shot and few-shot learning to assign new tasks to an AI adhoc, simply by writing them down. However, for the majority of end-users writing effective prompts is currently largely a trial and error process. To address this, we discuss the key opportunities and challenges for interactive creative applications that use prompting as a new paradigm for Human-AI interaction. Based on our analysis, we propose four design goals for user interfaces that support prompting. We illustrate these with concrete UI design sketches, focusing on the use case of creative writing. The research community in HCI and AI can take these as starting points to develop adequate user interfaces for models capable of zero- and few-shot learning.

# CCS CONCEPTS

# • Computing methodologies Cooperation and coordination; $\bullet$ Human-centered computing Collaborative interaction.

# KEYWORDS

HCI, Artificial Intelligence, Co-Creation, UI Design, Prompt Engi neering

# ACM Reference Format:

Hai Dang, Lukas Mecke, Florian Lehmann, Sven Goller, and Daniel Buschek. 2022. How to Prompt? Opportunities and Challenges of Zero- and FewShot Learning for Human-AI Interaction in Creative Applications of Generative Models. In GenAICHI: Generative AI and Computer Human Interaction, Workshop at CHI’22. ACM, New York, NY, USA, 7 pages. https: //doi.org/10.1145/nnnnnnn.nnnnnnn

# 1 INTRODUCTION

Recent advances in deep generative systems have enabled the creation of high fidelity media such as music, images, and text. These developments are becoming increasingly relevant also for creative domains as they potentially enable more collaborative and dynamic co-creative work of humans and AI systems. Trained on a large data corpus, such generative system can now synthesize new original content. However, user control over the generated output remains challenging. This requires effective interactions and user interfaces, as well as underlying AI mechanisms to support conditional and controlled generation.

One emergent interaction technique, especially for text generation, is the use of natural language prompts to steer the generative system: It was found that large language models (LLMs) do not necessarily need to be fine-tuned for specific tasks, such as for sentiment classification or topical text generation [6]. Instead, users may write a short text prompt to tell the system what to generate. Depending on how many examples are provided in the text prompt, we may differentiate between zero-, one-, and few-shot learning. Zero shot-learning refers to prompts where no specific example is given, such as: “Translate the following sentence into German: Good morning, how are you doing?”. However, providing one ex ample (one-shot learning) or more examples (few-shot learning) in the prompt may improve the output. For a detailed overview, see the recent survey by Liu et al. [13].

From an end-user perspective, writing prompts is largely ap proached as a trial and error process. Several influences have been identified and addressed in research (e.g. order of words) and best practices are shared informally on the web. However, the design of an effective prompting interface has not yet been explored systematically from a Human-Computer Interaction perspective. To address this, we collected and present key opportunities and challenges for prompting as a new paradigm for Human-AI interaction and propose and illustrate four design goals for user interfaces that support this. With this, we provide an overview and starting points for future research on user interfaces for models capable of zeroand few-shot learning.

# 2 RELATED WORK

We give an overview of work on interactive use of prompting, as well as techniques developed in prompt engineering.

# 2.1 Interactive Applications Using Few-shot Learning

Writing effective prompts is often not straightforward for users. A couple of recent projects have addressed this: For example, AI Chains is an interactive tool to combine a sequence of (sub-)tasks to be solved with repeated runs of one LLM [21]. Related, SynthBio uses few-shot learning to synthesise a data corpus of biographies [22] . This text synthesis consists of multiple steps, involving both an LLM to synthesize new biographies and humans to rate them. Both these systems [21, 22] focus on a combination of prompts as a means to reduce task complexity. In this paper, we highlight the idea of supporting prompt composition and combination as a key design goal and direction for user interfaces for prompting.

Further interactive examples include Story Centaur by Pietrzak et al. [16], an application for non-technical users to quickly construct prompts with few-shot examples: Through a graphical user interface users can define input and output text phrases, as well as phrases to be included before, in-between, or after each such example. The tool formats these components as a text prompt for few-shot learning. Related, Austin et al. [2] also built a tool that provides a template for prompt input in its UI, here to support synthesis of computer programs. Supporting prompt formulation and input is one of the key design goals for user interfaces that we discuss in this paper.

# 2.2 Prompt Engineering

Prompt engineering refers to the systematic practice of constructing prompts to improve the generated output of a generative model. Particular examples include these insights: Lu et al. [14] have found that word order affects the generated outcome. Moreover, while providing longer context in prompts empirically resulted in better text outputs [3, 8], Wu et al. [21] have found that task instructions within a longer context body can also conflict with each other. O’Connor and Andreas [15] provide a framework to determine “how much” information of the original context the prompt can actively use in the generation process. Another approach to elicit better prompts is to use the LLM itself for problem elaborations [4], inspired by the “think aloud” strategy humans use to solve complex problems.

Other strategies improve text prompts algorithmically: For example, Liu et al. [12] use sentence embedding on prompts to automatically sample neighboring prompt alternatives for comparison. AutoPrompt [20] optimises a set of words in the prompt using the gradient with respect to a task output (e.g. sentiment classification). Related, “prefix tuning” draws inspiration from prompting but optimises context tokens that do not need to map to actual words [11].

Finally, prompt-style input/output can also be used to finetune language models (“Pattern Exploiting Training” [19]) yet this is different from the prompts we discuss in this paper in that we aim to utilise their capability to perform (end user-specified) tasks ad-hoc without task-specific model training/finetuning.

# 3 METHOD

We organised two one-hour long brainstorming sessions with five HCI researchers to discuss and collect speculative opportunities and challenges that result from the prompt design paradigm to spark new discussions about the impact of prompt writing for creative expression. The first session included multiple phases. First, each participant quietly noted potential opportunities and challenges on a virtual whiteboard. In the second step, each participant briefly introduced their idea and then similar ideas were clustered. Finally, following a discussion and using the previously formed clusters, we identified overarching topics that we introduce in sections 4 and 5.

In the second session we started with a similar approach and collected ideas on the interactive use of prompt writing. In the brainstorming session we listed existing interactive systems that support users to prompt large language models (refer to 2.1) and drew inspiration for designing new scenarios to help users in their creative writing process. We started with the question of what creative writing means, followed by each researcher noting down potential goals and motivations for creative writing. Based on these notes we identified a three phase creative writing process which the ideal prompt writing support tool should cover at the very least (6).

# 4 OPPORTUNITIES

We highlight three opportunities that prompting may bring to the table. While our concrete examples focus on the use case of creative writing, the opportunities themselves are not limited to that domain.

# 4.1 End-User Programming of Creative Tools

Fundamentally, prompting LLMs at runtime gives the user the opportunity to define new tools ad hoc as needed, without retraining the model. This could be especially interesting for users without a technical background, because they can use natural language to define the tools they need and when they need it.

By defining generic prompts the users may also build up a library of generative tools for reuse in different contexts. Defining such tools can be done through programming by example (few-shot learning) or by declaration (zero shot learning).

Generating code from natural language prompts (e.g. OpenaAI’s Codex [7]) empowers users to create, adapt and appropriate digital tools (cf. [9]). However, prompting need not be limited to an interpretation as “code generation”; it could also be viewed as powering a conversation of humans and AI involved in a task, in which users can now define and delegate tasks verbally. This elevates the AI to be an active and dynamic contributor for the joint generation of new media instead of being a predefined assistant or toolbox.

# 4.2 Extending and Augmenting Creative Expressiveness

It is often not straight forward to sufficiently describe certain concepts in detail, especially in artistic contexts. For example, it would be very difficult to exactly describe certain text styles, but it is easy to express vague concepts via a prompt to an LLM, such as to “write a text in the prose of Shakespeare”. Other creative use involves prompting across modalities, such as text to image models [17], or prompting with images from which the generative systems may extract the mood or atmosphere (cf. AI-supported moodboards [10]). Formatting and rephrasing prompts have been shown to influence the text outcome. Therefore, prompting may allow users to synthesize new forms and styles, or translate between different ones. For example, a prompt might be designed to turn a novel into a screen play text or a non-linear format (e.g. text adventure).

# 4.3 Providing Inspiration and Feedback

Prompts may help to overcome a creative block by generating content. Related, prompts may be useful to simulate personal feedback on a given text (e.g. from the perspective of a famous author). Users can also prompt the model to provide input based on other works and styles (e.g. “What would Shakespeare write here?”), or more generally to optimise drafts with various objectives (e.g. “Make this text more formal”). Moreover, creating new media, such as writing an article, typically involves iteration. Prompts may help users to quickly iterate and explore multiple variations of a text, also by using different examples and by giving high-level directions (e.g. keywords, styles).

# 5 CHALLENGES

Here we describe key challenges of interactive use of prompting. These are based on the literature, material shared by practitioners online, and our own experiences.

# 5.1 Trial and Error / Lack of Guidance

Prompt design or engineering has seen little systematic research from an HCI perspective and for users remains mostly a trial and error process. This is also evident from the best practices shared in informal resources such as blogs and forums on the internet [1, 5]. Beyond that, recent work in HCI and AI reports on techniques such as elaboration [4], optimisation of key “trigger” words [20] or changing the word order [14]. A collection of prompts has also been started, with a tool to support researchers in writing prompts on datasets [18]1. However, few of the practically discovered or researched strategies have led to dedicated user interfaces and interactive tools for non-technical users.

The most elaborate user interface design we found is AI Chains, which embodies the strategy of breaking down complex prompts into subtasks that are easier for the model [21]. Extrapolating these observations raises questions about how future interfaces may support even more complex prompts and exploring multiple prompts. Overall, we envision that future interactive tools support users in creating and applying more effective prompts more efficiently and creatively.

# 5.2 Representation of Tasks and Effects / Prompt IO

If prompts enable users to define custom AI tools, default graphical representations (e.g. icons) might not suffice to describe them. Thus, it is an open question how prompts are represented in the interface and how users can interact to apply or execute them. Realising this requires discoverability and explanations as well: For instance, how might users be enabled to understand or remember what a prompt-based tool does without rereading the underlying prompt?

Related, current prompts mainly incentivise verbal thinking despite visuals or tacit knowledge and skills being part of many creative practices. It is not clear how to meaningfully incorporate images in prompts or how to visualise prompts (e.g. to integrate them into a GUI).

In addition, prompts are often conceptualised as one-time executions (e.g. write the prompt, then “run” it). However, creative work is often an iterative approach that requires the exploration of multiple potential outcomes and effects. Currently, it is an open question how interfaces might support such iterative explorations of input and output mappings for prompting.

Moreover, current constraints may defeat the upside of using natural language, for instance, if the prompt has to follow a strict structural format or specific “hidden rules” to be effective. Without adequate interactions and user interfaces, for creative practitioners, writing prompts might end up being very similar to writing code.

# 5.3 Computational Costs, Generalisation and Ethical Concerns

Large generative systems may introduce a noticeable delay which might affect users’ (creative) work process. For example, delays may prevent quick iterations. A related concern is gatekeeping access to such tools if they are only feasible to operate, for example, for large companies.

It is also not clear how well prompts generalise across different models. Optimizing a prompt in the context of one model does not guarantee the same performance when using another generative system. Besides usability issues this may create a lock-in effect where users are forced to continue to use one specific system.

Finally, content created via prompting is expected to replicate biases known from large language models in general, such as racist and stereotypical language.

# 6 DESIGNING USER INTERFACES THAT SUPPORT PROMPTING

Based on the literature and own ideas collected in a design session, we have identified four design goals for user interfaces that support prompting. A particular design may also address multiple of these goals. We mainly discuss the use case of creative writing in our examples here but expect these design ideas to be useful starting points for future work more generally as well.

![](img/ca23220504ec6514400d4b369ab968fb4e8086dd1e5bf8efaf948d63aee12dbc.jpg)  
Figure 1: In this GUI example, users enter a prompt in natural language and the system automatically parses this input. Key parameters such as detected task and task parameters can thus be edited directly. Then, the system automatically creates the (refined) text prompt for the generative model.

![](img/3a5614639470298e39f80f4c7e8a6c8390e5b91ab6b066d1d327a7e6c4e5b699.jpg)  
Figure 2: In this example GUI, users create a prompt not by writing from scratch but by selecting from predefined “building blocks” that have been proven to work well and cover typical use case-specific aspects. Free entry is still supported as well.

# 6.1 Supporting Users in Formulating Prompts

An effective user interface should support users in drafting prompts quickly and effortlessly. One way this could be achieved is to let the system automatically parse a user’s input and create text prompts as in Fig. 1. Furthermore, detected elements can be made editable as graphical UI elements (e.g. dropdown lists). While potentially easy to use, automatic detection may come with limitations, such as on the number of elements the systems recognises. A bottom-up approach would allow a user to manually define prompt improvements by selecting pre-defined parameters. This way, users have more granular control over the text prompt (see Fig. 2).

# 6.2 Supporting Users in Combining Prompts

Another key aspect for interaction is to support users in combining multiple prompts [21]. For example, for creative writing, this could enable users to explore multiple story lines in parallel (see Fig. 3). The user starts out with an initial prompt to generate a number of potential story lines and decides which are worth continuing. The selected text outputs can then serve as the context for the next text prompt. Given the uncertainty of LLM this can be good way to spark the users imagination and explore different directions before deciding on a final story line. Another way multiple prompts can be organised can be seen in Fig. 6, where prompts are structured in a separate view similar to the computational notebooks, e.g jupyter notebook.

# 6.3 Supporting Users in Applying Prompts

Next to creating text prompts it is also important to think about how text prompts are embedded in a (known and existing) user interface and the interactions that apply or execute these prompts. In Fig. 4 we present a potential interaction flow where users assign a symbol to a reusable text prompt in a toolbar. Once such a defined symbol is selected the user can mark text to apply the underlying prompt, which brings up a dialog showing the generated output. More generally, stored prompts in the GUI could also be textual or, if possible, represented by a suitable symbol as illustrated in our example here.

![](img/c17d459364e52f929304ea38d6ab5f7529acba4cf6fceec228c2906f0cb95a98.jpg)  
Figure 3: This example GUI focuses on prompt exploration and combination: Users write prompts to direct a “narrative tree” showing multiple possible responses to each prompt. Users select some of them as context for the next prompt(s), which direct the narrative further.

![](img/b0b98db274aa49934495ab1fc57f9a377d67472834d8fb63728f20132b78fc56.jpg)  
Figure 4: This GUI example supports users in applying prompts by enabling them to write and save prompts as tools in a toolbar. Users can then (re-)apply the text transformations defined by these prompts to text selections, such as the “reformulate friendly” tool here.

As discussed, computational delay can be one of the challenges of designing effective interactions with text prompts. Thinking about how such delays can be incorporated in the design may help a user in applying prompts more creatively. For creative writing, one such opportunity could aim to maintain the writer’s flow. For example, a user might have a short-term writer’s block in which case it could be helpful to continue writing down another thought first, while letting the LLM finish the current paragraph (Fig. 5). Once the results are ready the user will be notified and can return to edit this text passage.

# 6.4 Representing Prompts in User Interfaces

Prompts also have to be represented in the user interface. One example is shown in Fig. 4 where a prompt is visualised as a symbol (smiley) and annotated to a text paragraph (highlighting, popup). Alternatively, prompts can also be organised along side a text. A simple split between a “prompt” and a “text” view allows users to switch between editorial and evaluative tasks (Fig. 6). In this scenario, the prompt interface is similar to a hypertext or annotation interface, allowing users to define the structure and the creative annotations of the text. The resulting text view can serve as interface for light edits, but mainly to evaluate the generated output.

# 7 CONCLUSION

In this paper, we have argued to investigate prompting as a novel approach for human-AI interaction in creative tasks, motivated by promising opportunities around end-user programming of creative tools, creative expressiveness, and inspiration and feedback. Reflecting on the broader workshop theme, prompting could democratise creative activities and domains, for example, by enabling users with no specific training to create personalised tools and more creatively work with text. Furthermore, users might be able to learn through the verbally expressive interactions and effects enabled by prompts and thereby improve their own creative skills. Prompting also extends creative possibilities – not only how, but also what we can create – by empowering individuals to flexibly and declaratively tap into the models’ generative capabilities. In order to realise this potential we need adequate user interfaces for prompting. Future work should therefore explore design directions at the intersection of HCI and AI, such as the ones provided as starting points here.

![](img/869e3fb6427c0244a7e2814cf6d738001261bd3656696ea0babe6b9f3fc9bce9.jpg)  
Figure 5: This example GUI supports asynchronous human-AI collaboration and in doing so also addresses potential delays of computationally costly prompts: The user can insert prompts into a text document anywhere, which trigger asynchronous calls to the LLM system, for example, to extend a part of the text. In the meantime, the user can continue working on another part of the text.

![](img/c02812d543be726ddcc15333a7a3191796d02a49c7fd5e4de6ab066eb085e56d.jpg)  
Figure 6: This GUI example treats the presentation of prompts similar to markdown, LaTeX or code editors: The GUI is split between prompt view and text view, allowing users to switch between editorial and evaluative tasks.

# ACKNOWLEDGMENTS

This project is funded by the Bavarian State Ministry of Science and the Arts and coordinated by the Bavarian Research Institute for Digital Transformation (bidt).

# REFERENCES

[1] Cohere AI. 2021. API Documentation | Cohere AI. https://docs.cohere.ai/   
[2] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. 2021. Program synthesis with large language models. arXiv preprint arXiv:2108.07732 (2021).   
[3] Iz Beltagy, Matthew E Peters, and Arman Cohan. 2020. Longformer: The longdocument transformer. arXiv preprint arXiv:2004.05150 (2020).   
[4] Gregor Betz, Kyle Richardson, and Christian Voigt. 2021. Thinking Aloud: Dynamic Context Generation Improves Zero-Shot Reasoning Performance of GPT-2. arXiv preprint arXiv:2103.13033 (2021).   
[5] Gwern Branwen. 2020. GPT-3 Creative Fiction. https://www.gwern.net/GPT-3   
[6] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. Language Models are Few-Shot Learners. In Advances in Neural Information Processing Systems, H. Larochelle, M. Ranzato, R. Hadsell, M. F. Balcan, and H. Lin (Eds.), Vol. 33. Curran Associates, Inc., 1877–1901. https://proceedings. neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf   
[7] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Evaluating Large Language Models Trained on Code. arXiv:2107.03374 [cs.LG]   
[8] Urvashi Khandelwal, He He, Peng Qi, and Dan Jurafsky. 2018. Sharp Nearby, Fuzzy Far Away: How Neural Language Models Use Context. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers).   
[9] Clemens N. Klokmose, James R. Eagan, Siemen Baader, Wendy Mackay, and Michel Beaudouin-Lafon. 2015. <i>Webstrates</i>: Shareable Dynamic Media. In Proceedings of the 28th Annual ACM Symposium on User Interface Software & Technology (Charlotte, NC, USA) (UIST ’15). Association for Computing Machinery, New York, NY, USA, 280–290. https://doi.org/10.1145/2807442.2807446   
[10] Janin Koch, Nicolas Taffin, Michel Beaudouin-Lafon, Markku Laine, Andrés Lucero, and Wendy E. Mackay. 2020. ImageSense: An Intelligent Collaborative Ideation Tool to Support Diverse Human-Computer Partnerships. Proc. ACM Hum.-Comput. Interact. 4, CSCW1, Article 045 (may 2020), 27 pages. https: //doi.org/10.1145/3392850   
[11] Xiang Lisa Li and Percy Liang. 2021. Prefix-Tuning: Optimizing Continuous Prompts for Generation. arXiv:2101.00190 [cs.CL]   
[12] Jiachang Liu, Dinghan Shen, Yizhe Zhang, Bill Dolan, Lawrence Carin, and Weizhu Chen. 2021. What Makes Good In-Context Examples for GPT-3? arXiv:2101.06804 [cs.CL]   
[13] Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, and Graham Neubig. 2021. Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing. arXiv:2107.13586 [cs] (July 2021). http://arxiv.org/abs/2107.13586 arXiv: 2107.13586.   
[14] Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus Stenetorp. 2021. Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity. arXiv preprint arXiv:2104.08786 (2021).   
[15] Joe O’Connor and Jacob Andreas. 2021. What Context Features Can Transformer Language Models Use? arXiv preprint arXiv:2106.08367 (2021).   
[16] Ben Pietrzak, Ben Swanson, Kory Mathewson, Monica Dinculescu, and Sherol Chen. 2021. Story Centaur: Large Language Model Few Shot Learning as a Creative Writing Tool.   
[17] Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. 2021. Zero-Shot Text-to-Image Generation. arXiv:2102.12092 [cs.CV]   
[18] Victor Sanh, Albert Webson, Colin Raffel, Stephen H. Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Chaffin, Arnaud Stiegler, Teven Le Scao, Arun Raja, Manan Dey, M Saiful Bari, Canwen Xu, Urmish Thakker, Shanya Sharma Sharma, Eliza Szczechla, Taewoon Kim, Gunjan Chhablani, Nihal Nayak, Debajyoti Datta, Jonathan Chang, Mike Tian-Jian Jiang, Han Wang, Matteo Manica, Sheng Shen, Zheng Xin Yong, Harshit Pandey, Rachel Bawden, Thomas Wang, Trishala Neeraj, Jos Rozen, Abheesht Sharma, Andrea Santilli, Thibault Fevry, Jason Alan Fries, Ryan Teehan, Stella Biderman, Leo Gao, Tali Bers, Thomas Wolf, and Alexander M. Rush. 2021. Multitask Prompted Training Enables Zero-Shot Task Generalization. arXiv:2110.08207 [cs.LG]   
[19] Timo Schick and Hinrich Schütze. 2021. Exploiting Cloze Questions for Few Shot Text Classification and Natural Language Inference. arXiv:2001.07676 [cs] (Jan. 2021). http://arxiv.org/abs/2001.07676 arXiv: 2001.07676.   
[20] Taylor Shin, Yasaman Razeghi, Robert L Logan IV, Eric Wallace, and Sameer Singh. 2020. AutoPrompt: Eliciting Knowledge from Language Models Using Automatically Generated Prompts. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP). 4222–4235.   
[21] Tongshuang Wu, Michael Terry, and Carrie J Cai. 2021. AI Chains: Transparent and Controllable Human-AI Interaction by Chaining Large Language Model Prompts. arXiv preprint arXiv:2110.01691 (2021).   
[22] Ann Yuan, Daphne Ippolito, Vitaly Nikolaev, Chris Callison-Burch, Andy Coenen, and Sebastian Gehrmann. 2021. SynthBio: A Case Study in Human-AI Collaborative Curation of Text Datasets. arXiv preprint arXiv:2111.06467 (2021).