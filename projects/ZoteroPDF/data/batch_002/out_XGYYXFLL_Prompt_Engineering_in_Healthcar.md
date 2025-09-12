# Article Prompt Engineering in Healthcare

Rajvardhan Patil $^ { 1 , * \textcircled { \| } }$ , Thomas F. Heston ${ \mathfrak { 2 } } _ { \bigoplus }$ and Vijay Bhuse 1

Citation: Patil, R.; Heston, T.F.; Bhuse, V. Prompt Engineering in Healthcare. Electronics 2024, 13, 2961. https:// doi.org/10.3390/electronics13152961

Academic Editors: Jun-Ho Huh and Yeong-Seok Seo

Received: 1 July 2024   
Revised: 22 July 2024   
Accepted: 24 July 2024   
Published: 26 July 2024

1 School of Computing, Grand Valley State University, Grand Rapids, MI 49503, USA; bhusevij@gvsu.edu 2 Department of Family Medicine, University of Washington, Seattle, WA 98195, USA; theston@uw.edu \* Correspondence: patilr@gvsu.edu; Tel.: $+ 1$ -616-331-4375

Abstract: The rapid advancements in artificial intelligence, particularly generative AI and large language models, have unlocked new possibilities for revolutionizing healthcare delivery. However, harnessing the full potential of these technologies requires effective prompt engineering—designing and optimizing input prompts to guide AI systems toward generating clinically relevant and accurate outputs. Despite the importance of prompt engineering, medical education has yet to fully incorporate comprehensive training on this critical skill, leading to a knowledge gap among medical clinicians. This article addresses this educational gap by providing an overview of generative AI prompt engineering, its potential applications in primary care medicine, and best practices for its effective implementation. The role of well-crafted prompts in eliciting accurate, relevant, and valuable responses from AI models is discussed, emphasizing the need for prompts grounded in medical knowledge and aligned with evidence-based guidelines. The article explores various applications of prompt engineering in primary care, including enhancing patient–provider communication, streamlining clinical documentation, supporting medical education, and facilitating personalized care and shared decision-making. Incorporating domain-specific knowledge, engaging in iterative refinement and validation of prompts, and addressing ethical considerations and potential biases are highlighted. Embracing prompt engineering as a core competency in medical education will be crucial for successfully adopting and implementing AI technologies in primary care, ultimately leading to improved patient outcomes and enhanced healthcare delivery.

Keywords: prompt engineering; ChatGPT; healthcare; GPT; chatbot; healthcare; prompts; primary care providers; PCP; healthcare providers

# 1. Introduction

Artificial Intelligence (AI) has made remarkable strides since its early days in the 1940s and 1950s when pioneering work laid the foundation for neural networks and machine learning [1–3]. For instance, ref. [1] mentions how propositional logic can be used to capture neural events and the relations among them, ref. [2] presents a theory of behavior using the concept of the reverberatory circuit and the assumption that “some growth process or metabolic change” in neurons takes place as a result of repeated transmission across synapses, and ref. [3] identifies how a system consisting of randomly connected units can learn to associate or generate responses to specific input stimuli. In recent years, the development of large language models (LLMs) and generative AI, such as the GPT (Generative Pre-trained Transformer) architecture in 2017 [4], has opened up new possibilities for AI to revolutionize various industries, including healthcare. These advanced AI systems have demonstrated the ability to generate human-like text, engage in natural conversations, and even pass the Turing test [5]. In healthcare, generative AI holds immense potential to automate tasks, support clinical decision-making, and improve patient outcomes by rapidly analyzing vast amounts of medical data [6]. For example, generative AI can automatically generate clinical notes, patient education materials, and treatment recommendations, streamlining clinical workflows and enhancing patient care.

While generative AI has demonstrated value in primary care settings, harnessing its full potential requires effective prompt engineering—designing and optimizing input prompts to guide the AI system toward generating desired outputs. Practical prompt engineering ensures the AI system generates medically accurate outputs relevant to the specific patient or clinical scenario and aligned with the application’s intended purpose [7,8].

Previous research has highlighted the importance of prompt engineering across various healthcare domains, demonstrating its impact on the quality and effectiveness of generative AI outputs [9]. Prompt engineering involves carefully designing and refining the input prompts given to the AI system, considering factors such as the specific task, the desired output format, and the relevant contextual information. By optimizing these prompts, researchers and practitioners can guide the AI system to generate more accurate, appropriate, and valuable outputs. Practical prompt engineering can streamline clinical workflows by enabling AI systems to produce more accurate and targeted patient summaries, treatment recommendations, and referral suggestions [10].

However, despite the rapid rise of generative AI, medical education has yet to fully incorporate comprehensive training on prompt engineering, creating a knowledge gap in primary care settings. Consequently, an educational gap exists regarding comprehensive guidelines and best practices for generative AI prompt engineering in family medicine.

Addressing this educational gap is crucial for successfully adopting and implementing generative AI in primary care. To bridge this gap, focused education on prompt engineering concepts, from static prompts to prompt pipelines [11], and their relevance to primary care settings is necessary. This article aims to provide an overview of generative AI prompt engineering, discuss its potential applications and benefits in family medicine, and offer insights into best practices and challenges. Furthermore, the importance of effective prompt engineering in ensuring the accuracy of AI-generated recommendations and improving clinical efficiency is emphasized [12].

This article aims to empower Primary Care Providers (PCPs) to harness the potential of generative AI effectively and responsibly by addressing the educational gap and providing practical insights into prompt engineering. Additionally, it provides overview on different prompt engineering techniques, and demonstrates their potential applications in primary care medicine using large language models such as ChatGPT, along with best practices for their effective implementation. The following list enumerates the major contributions of this article.

# Contributions and Outline

1. Overview and providing practical insights into prompt engineering techniques;   
2. Importance of well-crafted prompts to elicit valuable responses from AI models;   
3. Potential applications of prompt engineering in primary care medicine;   
4. Best practices for the effective implementation of prompts in primary care.

The outline of this paper is as follows. In Section 2, we go over the related work of prompt engineering in healthcare. Section 3 discusses the methods that can be used to enhance patient–provider communication, streamlining clinical documentation and administrative tasks in family medicine using prompt-engineering techniques. In Section 4, we perform experiments and elucidate the results. We discuss the challenges, limitations, and future directions in Section 5, followed by the conclusion in Section 6.

# 2. Related Work

# 2.1. Understanding Prompt Engineering

Prompt engineering designs and optimizes input prompts to guide generative AI models toward producing desired outputs [13]. Given the vast amount of training data utilized by generative AI models, retrieving the best, most appropriate information can be challenging. Prompt engineering involves constructing text-based instructions, questions, and/or context to elicit accurate, relevant, and valuable responses from these models.

The prompts serve as the primary interface between the user and the AI model, directing attention to specific tasks and shaping the generated content [14].

Well-crafted prompts help align the AI outputs with the user’s intentions, ensuring the generated content is coherent and appropriate for the context [15]. For example, in a primary care setting, a well-crafted prompt for generating patient education materials on hypertension might include specific instructions such as “Explain the causes, symptoms, and management of hypertension in simple language suitable for a lay audience. Emphasize the importance of lifestyle modifications and adherence to prescribed medications”. Prompts can range from simple, open-ended questions to complex, multi-step instructions that break tasks into smaller, more manageable components [16,17]. By providing clear and specific guidance, prompts enable AI models to generate more focused, accurate, and valuable outputs for the intended purpose.

Effective prompts require a deep understanding of the AI model’s capabilities, limitations, and potential biases. Prompt engineers must consider the model’s training data, capacity to handle different tasks, and the desired output format. Clear, specific, and contextappropriate prompts are essential for eliciting high-quality responses from generative AI models. Ambiguous or overly broad prompts can lead to irrelevant or nonsensical outputs. In contrast, prompts lacking sufficient context may result in incomplete responses or failure to capture the nuances of the task [18].

Effective prompt engineering in primary care medicine ensures that generative AI models provide the most accurate, relevant, and actionable insights to support clinical decision-making. Prompts must be designed to elicit responses grounded in medical knowledge, aligned with evidence-based guidelines, and tailored to the specific needs of individual patients. This requires close collaboration between medical professionals and AI experts to ensure that prompts are clinically relevant and adhere to best practices in healthcare. By crafting prompts incorporating relevant clinical information, such as patient history, symptoms, and diagnostic data, prompt engineers can guide AI models to generate more precise and valuable recommendations for diagnosis, treatment, and care management [19].

For example, a well-designed prompt for a patient presenting with chest pain might include details such as the patient’s age, gender, risk factors, and the nature and duration of the pain. The prompt can also instruct the AI to play the role of a medical colleague so the response is appropriately sophisticated. By providing this context, the AI model can generate a more accurate list of potential diagnoses, such as acute coronary syndrome or pulmonary embolism, and suggest appropriate diagnostic tests or treatment options. This specificity in prompts can help Primary Care Providers make more informed decisions and improve patient outcomes.

It is important to note that prompt engineering is an iterative process that requires continuous refinement based on feedback and real-world performance metrics. As AI models are deployed in clinical settings, prompt engineers must actively engage with healthcare professionals to gather insights and adapt prompts to better suit the needs of patients and providers. This ongoing collaboration and refinement process ensures that generative AI models consistently deliver accurate, relevant, and trustworthy outputs that support high-quality patient care.

# 2.2. Best Practices for Prompt Engineering in Healthcare

To ensure the effective and responsible use of prompt engineering in healthcare, particularly in family medicine, it is essential to adhere to best practices that prioritize patient safety, clinical accuracy, and ethical considerations.

# 2.2.1. Incorporating Domain-Specific Knowledge and Guidelines

One of the essential best practices in prompt engineering for healthcare is incorporating domain-specific knowledge and guidelines. This can be facilitated by developing custom

GPTs that include a specialized knowledge base and/or a base prompt that applies to the entire conversation with the user.

# 2.2.2. Iterative Refinement and Validation of Prompts

Another critical best practice is the iterative refinement and validation of prompts. Prompt engineering in healthcare should be an ongoing process that involves the continuous testing, evaluation, and improvement of prompts based on feedback from medical professionals and real-world performance metrics [20]. This iterative approach helps identify and address any weaknesses or limitations in the prompts, ensuring they remain practical and relevant over time. Validation of prompts should involve quantitative and qualitative assessments, such as measuring the accuracy of AI-generated outputs against expert human judgment and soliciting feedback from family medicine clinicians on the usability and usefulness of the prompts in clinical practice [12]. By engaging in this iterative refinement and validation process, prompt engineers can continuously optimize the performance of AI models in healthcare settings.

# 2.2.3. Addressing Ethical Considerations and Potential Biases

Addressing ethical considerations and potential biases is another crucial best practice in prompt engineering for healthcare. Prompt engineers must know the potential risks and unintended consequences of using AI in medical decision-making, such as perpetuating or amplifying existing health disparities [21]. To mitigate these risks, prompt engineers should design prompts that are inclusive, diverse, and free from biases based on factors such as race, ethnicity, gender, or socioeconomic status. This may involve incorporating adversarial testing and bias detection algorithms to identify and remove any discriminatory patterns in the prompts or the AI-generated outputs [22,23]. Additionally, prompt engineers should collaborate with bioethicists and patient advocates to ensure that the use of AI in healthcare aligns with fundamental ethical principles, such as autonomy, beneficence, non-maleficence, and justice [24]. Adhering to these best practices can prompt engineers to create a foundation for the responsible and effective use of generative AI in family medicine. This will improve patient care and outcomes while minimizing potential risks and unintended consequences.

# 3. Methods

# 3.1. Applications of Prompt Engineering in Family Medicine

Prompt engineering has numerous potential applications in family medicine, from improving patient–provider interactions to streamlining administrative tasks and supporting medical education. By leveraging the power of generative AI models, prompt engineering can help family medicine clinicians deliver more efficient, personalized, and highquality care.

# 3.2. Enhancing Patient–Provider Communication

One of the primary applications of prompt engineering in family medicine is enhancing patient–provider communication. Well-designed prompts can guide AI models to generate patient-friendly explanations of medical concepts, conditions, and treatment options, helping to bridge the knowledge gap between clinicians and patients. For example, a prompt could ask the AI model to explain the concept of joint pain in simple terms, along with its potential complications and management strategies. The generated response can supplement the clinician’s explanation during a patient consultation, ensuring that the patient clearly understands their condition and the importance of adherence to treatment plans. Some more examples of ‘Good’ vs. ‘Better’ prompts are highlighted in Table 1.

Table 1. Prompt examples.   

<html><body><table><tr><td>Task</td><td>Good Prompt</td><td>Better Prompt</td></tr><tr><td>Explaining a di- abetes diagno- sis to a patient</td><td>Explain what dia- betes is and how it affects the body.</td><td>You are a family clinician. Explain a new diabetes diagnosis to a 45-year-old patient with a high school education. Define diabetes, how it affects the body, potential complications, and the importance of lifestyle changes and medication adherence. Use simple language and analogies to ensure understanding. Use a friendly tone.</td></tr><tr><td>Providing instructions for using an inhaler</td><td>Provide step-by- stepinstructions on how to use an inhaler properly.</td><td>Play the role of a family clinician. Give clear, step-by-step instructions to a 60-year-old patient with asthma on how to properly use their new metered-dose inhaler. Include information on priming the inhaler, shaking it, exhaling before use, inhaling deeply, holding their breath, and cleaning the device. Use simple language and short sentences.</td></tr><tr><td>Discussing the benefits and risks of a prostate cancer screening</td><td>Discuss the poten- tial benefits and risks of prostate cancer screening for a 55-year-old male patient.</td><td>You are a primary care clinician. Discuss the potential benefits and risks of prostate cancer screening with a 55-year-old male patient who has no family history of prostate cancer. Cover the purpose of the PSA test, its limitations, the possibility of false positives, and the potential for overdiagnosis and overtreatment. Use balanced language and provide context to help the patient make an informed decision.</td></tr></table></body></html>

# 3.3. Streamlining Clinical Documentation and Administrative Tasks

Prompt engineering can also be crucial in streamlining clinical documentation and administrative tasks. AI models can generate draft clinical notes, referral letters, and other documentation by designing prompts that accurately capture patient information, medical history, and clinical findings, saving clinicians valuable time [25]. For instance, a prompt could be crafted to summarize a patient’s medical history and current medications and present complaints based on the information gathered during a consultation. The clinician can then review and edit the AI-generated summary, ensuring accuracy and completeness while reducing the time spent on documentation. Similarly, prompts can be designed to help AI models extract relevant information from medical records, identify potential coding errors, and suggest appropriate billing codes, streamlining administrative processes and improving the efficiency of family medicine practices.

# 3.4. Supporting Medical Education and Training

Prompt engineering can revolutionize medical education and training in family medicine. AI models can generate interactive case studies, virtual patient encounters, and adaptive learning materials by developing prompts that simulate real-world clinical scenarios. These AI-generated resources can help medical students and residents develop critical thinking, decision-making, and problem-solving skills in a safe and controlled environment.

For example, a prompt could describe a patient with abdominal pain and ask the learner to generate a differential diagnosis, suggest appropriate diagnostic tests, and propose a management plan. The AI model can then provide feedback on the learner’s response, highlighting areas for improvement and suggesting evidence-based approaches. Furthermore, prompt engineering can create personalized learning pathways based on individual learners’ strengths, weaknesses, and learning preferences, ensuring a more targeted and practical educational experience.

# 3.5. Facilitating Personalized Care and Shared Decision Making

Finally, prompt engineering can facilitate personalized care and shared decisionmaking in family medicine. AI models can generate tailored treatment recommendations and risk assessments by designing prompts incorporating patient-specific information, such as genetic data, lifestyle factors, and personal preferences. For instance, a prompt could include a patient’s age, gender, family history, and specific genetic variants to guide the AI model in generating personalized cancer screening recommendations. These AI-generated insights can help clinicians and patients engage in informed discussions about the risks and benefits of various screening and treatment options, fostering a collaborative approach to healthcare decision-making. Moreover, prompt engineering can be used to develop AIpowered tools that enable patients to explore the potential outcomes of different treatment choices, empowering them to take an active role in their care and aligning treatment plans with their individual goals and values. Table 2 enumerates different type of prompts (with examples) that can be used in a healthcare environment.

Table 2. Types of prompts.   

<html><body><table><tr><td>Prompt Type</td><td>Description</td><td>Usefulness</td><td>Example</td></tr><tr><td>Zero-shot</td><td>A prompt that provides a task or question without any examples (zero-shot) or additional context</td><td>Useful for quickly gener- ating responses to simple, straightforward queries or task</td><td>&quot;What are the common symptoms of influenza?&quot;</td></tr><tr><td>Few-shot</td><td>A prompt that includes a few examples (few-shot) or demonstrations of the desired output before pre- senting the actual task or question</td><td>Helps the AI model better understand the expected format, style, and content of the response</td><td>&quot;&#x27;Here are two examples of patient education materials on hypertension: [Example 1] [Example 2]. Now, create a similar patient education material on type 2 diabetes.&quot;</td></tr><tr><td>Ask Me Any- thing</td><td>An open-ended prompt that encourages the AI model to respond to a wide range of questions or tasks related to a spe- cific domain or topic</td><td>Enables  clinicians to quickly access informa- tion and insights on various aspects of patient care, from diagnosis to treatment and beyond</td><td>&quot;As a family clinician, I often encounter patients with mental health concerns, such as anxiety and depression. What are sy me best ractices o screning dingnosing setting?&quot;</td></tr><tr><td>Least-to- Most</td><td>A prompt that breaks dowsmalleo mplex etask steps, gradually guiding the AI model towards the final desired output</td><td>Useful for tackling more challengngroblemulti healthcare, such as de- veloping comprehensive treatment plans</td><td>&quot;Let&#x27;s develop a personalized care plan for a patient with multiple chronic conditions. First, list the patient&#x27;s diag- noses and current medications. Next, identify potential drug interactions and contraindications. Then, suggest lifestyle modifications and preventive measures. Finally,  llow-up</td></tr><tr><td>Role Assign- ment</td><td>A prompt that assigns a spec ic rel ompdrespec- couraging it to respond as if it were a particular type of entity or expert</td><td>Helps clinicians obtain in- sights and recommenda- points, such as those of specialists or patient ad- vocates</td><td>&quot;Act as an endocrinologist and provide guidance on man- aging a patient with poorly controlled type 2 diabetes and comorbid hypertension.&quot;</td></tr><tr><td>Tone</td><td>A prompt that specifies the desired tone, style, or level of complexity for the AI-generated re- sponse</td><td>Enables clinicians to tai- lor the output to the in- tended audience or pur- pose, such as creating patient-friendly explana- tions or generating pro- fessional medical reports</td><td>&quot;Explain the concept of herd immunity in simple terms suitable for a patient with limited health literacy. Use a friendly, direct tone.&quot;</td></tr><tr><td>Contextual Priming</td><td>A prompt that provides relevant bac ground ie- fore presenting the main task or question</td><td>Helps the AI model gen- erate more accurate and con tex-aware re sponses such as patient demo- graphics, medical history, or clinical setting</td><td>&quot;A 65-year-old female patient with a history of hyper- tension and hyperlipidemia presents to your clinic for a routine chec -upl Her blood p mgure s 145/90 mm Hg. age, gender, and medical history, what lifestyle modifi- cations and pharmacologic interventions would you rec- ommend to reduce her risk of cardiovascular disease?&quot;</td></tr></table></body></html>

# 4. Experiments and Results

In this section, we provide prompt templates that PCPs can use to query LLM and obtain possible answers to the health problems or illnesses the patients are facing. These prompt templates focus on common illnesses, such as obesity, flu, cold, cough, mental illness, dental issues, high and low blood pressure, diabetes, and joint issues. Prompts mainly consist of the following components:

1. Task or instruction to be carried out;   
2. Assign a role to ChatGPT;   
3. Examples provided through context;   
4. Input for which LLM should generate an output.

In order to yield better results, while constructing the prompt templates, we have tried to encompass all the essential or main keywords that are required in a prompt of a particular domain (illness). These templates also highlight the minimal information that needs to be fed in as contextual input to these prompts.

There are two ways in which these prompt templates can be fed to the LLMs. The first is the Inline-Approach, where PCPs can directly enter the examples (one or few shot style) as part of the prompt into the web based chat-interface (e.g., https://chat.openai. com/). The second is the Bot-Approach, where a customized bot is first constructed using the knowledge graph. The PCPs can then interact with the bot and elicit the required information. Below, we first explore the Inline-Approach for nine common illnesses. In Table 2, we list different prompt engineering techniques. In the following subsections, we use the few-shot technique, where we provide one example as part of the context.

# 4.1. In-Line Approach

The examples provided in the prompt templates mainly have two parts: “PatientInfo” and the expected “Output”. Inside the PatientInfo, PCP can provide the patient’s personal information (such as age, gender, height, weight, etc.) along with symptoms, history, habits, allergies and diagnostic data. Additionally, using prompts, PCP can ask the LLM to provide the results or output in some desired format. For example, the proposed template prompts request the LLM to provide output in json format consisting of the following keys or fields: “Natural Remedies, Over the Counter Medicines, Prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes of the disease, illness, or health problem”. The PCPs or readers can simply cut and paste these prompts into the ChatGPT, Claude.ai, or Gemini interface for testing purposes. Note that the recommendations or output generated by these prompt templates can be misleading or incorrect. The users are therefore advised to consult their doctor, clinician, or healthcare provider before making any informed decisions on these recommendations suggested by the LLMs. Below, we demonstrate the usage of these prompt-template examples on nine use cases, along with the output generated by ChatGPT.

# 4.1.1. Obesity Prompt

Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: {   
age: 41,   
Gender: “Male”,   
height: “6 feet”,   
weight: “190 pounds”,

Symptoms: “breathlessness, increased sweating, snoring, difficulty doing physical activity, often feeling very tired, joint and back pain, low confidence and self-esteem, feeling isolated”,

Habits: “binge eating”,   
History: “”,   
Allergies: “”,   
Diagnostic Data: “BMI above $2 5 ^ { \prime \prime }$   
}

# Output: {

Natural Remedies: “Dietary changes, Cutting calories, Feeling full on less, eat more plant-based foods, physical activity, exercise, keep moving, Limiting unhealthy foods and beverages, Increasing physical activity, Limiting television time, screen time, and other sit time, Improving sleep, Reducing stress”,

Over the Counter Medicines:

Prescription Medication: “Bupropion-naltrexone, Hydrogels, Liraglutide (Saxenda), Orlistat (Alli, Xenical), Phentermine-topiramate (Qsymia), Semaglutide (Ozempic, Rybelsus, Wegovy)”,

Medical Treatment: “general physical exam, calculating BMI, Endoscopic sleeve gastroplasty, Intragastric balloon for weight loss, Counseling, support groups, Weight-loss surgery, Adjustable gastric banding, Gastric bypass surgery, Gastric sleeve, Vagal nerve blockade, Gastric aspirate”,

Preventive Measures: “Keep a food diary of what you eat, Eat five to nine servings of fruits and vegetables daily, Choose whole grain foods, Weigh and measure food to learn correct portion sizes, Learn to read food nutrition labels and use them; keep track of the number of portions been eaten, reduce portion sizes and using a smaller plate can help lose weight, Aim for an average of 60 to 90 min or more of moderate to intense physical activity three to four days each week”,

Precautions: “avoid high-carbohydrate or full-fat foods, Don’t eat highly processed foods made with refined white sugar, flour, high fructose corn syrup and saturated fat, Don’t eat foods that are high in “energy density”, or that have a lot of calories in a small amount of food, For dessert have a serving of fruit yogurt a small piece of angel food cake or a piece of dark chocolate instead of frosted cake ice cream or pie,”,

Possible Causes: “Unhealthy diet, Liquid calories, sugared soft drinks, Inactivity, diet that’s high in calories, full of fast food, and laden with high-calorie beverages, eating oversized portions, lacking in fruits and vegetables, Family inheritance, genetics and influences, lack of sleep, stress, Metabolism”   
}

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution. Query#1: “PatientInfo: {age: 28, Symptoms: “High BMI, overweight”, Habits: “job that requires $1 0 \mathrm { { h } }$ sitting. like to eat sweets”}” The output generated by ChatGPT for Query#1 is shown below in Figure 1.

![](img/b9f79c3385dc9da0e8cac1dd7eeabe215e72fda06694e11bd96c2e9418754da4.jpg)

Figure 1. ChatGPT Output for Query#1.

4.1.2. Flu, Cold, Cough—Prompt Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Clinical Care, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: { age: 23, Gender: “Male”,

Symptoms: “fever, cold, cough, stuffy nose, runny nose, sneezing, watery eyes, sore throat, respira   
tory virus”,   
History “”,   
Habits: “”,   
Allergies: “pollen, Penicillin”,   
Diagnostic Data: “”   
}

Output: { Natural Remedies: “Hot Water, Hot Drinks, Steam, Gargling, Humidifier, Honey, Turmeric, drink hot fluid, cool mist humidifier, saline nose drops or sprays, nasal suctioning with a bulb syringe”,

Over the Counter Medicines: “Cough Drops, Menthol, syrup, Nasal Spray, Tylenol, Advil, robitussin, Antihistamines, Decongestants, Expectorants, Suppressants, Acetaminophen (e.g., Tylenol, Panadol), Ibuprofen (e.g., Advil, Nuprin), Naproxen sodium (e.g., Aleve), Cough expectorants (e.g., Robitussin), Cough suppressants (e.g., Robitussin DM ), Lozenges and throat sprays (e.g., Chloraseptic, Cepastat, Halls), Paracetamol”,

Prescription Medication: “Antibiotics such as Amoxicillin, Augmentin (amoxicillin/clavulanate), Cefdinir Cefpodoxime, Clindamycin, Daxbia (cephalexin), Doxycycline, Keflex (cephalexin), Penicillin, Suprax (cefixime), Zithromax (azithromycin), Antiviral medication (e.g., Tamiflu), Mortin, ibuprofen, aspirin, Nasal decongestants”,

Medical Treatment: “”,

Preventive Measures: “flu shot”,

Precautions: “avoid cold water, avoid oily and spicy food, avoid bathing by cold water”,

Possible Causes: “dust, pollen, allergens, viruses, other irritants, viral infection, influenza viruses,   
irritation to the mucous membranes of the nose or throat”   
}

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution.

Query#2: “{age: 55, Gender: “Male”,Symptoms: “Sore throat, Nasal congestion”, Allergies: “peanut butter”}”

The output generated by ChatGPT for Query#2 is shown below in Figure 2.

<html><body><table><tr><td>&quot;Natural Remedies&quot;: &quot;Warm salt gargle, steam inhalation, honey, ginger tea, eucalyptus oil, saline nasal drops, humidifier&quot;,</td></tr><tr><td>&quot;Over the Counter Medicines&quot;: Antihistamines, Decongestants, Pain relievers like Acetaminophen or Ibuprofen, Throat lozenges&quot;,</td></tr><tr><td>&quot;Prescription Medication&quot;: &quot;None, unless bacterial infection is suspected then antibiotics like Amoxicillin may be required&quot;,</td></tr><tr><td>&quot;Medical Treatment&quot;: &quot;If symptoms persist or worsen, consult a healthcare provider for further evaluation and management&quot;,</td></tr><tr><td>&quot;Preventive Measures&quot; &quot;Avoid known allergens, stay hydrated, maintain good hygiene, avoid smoking and exposure to secondhand smoke&quot;,</td></tr><tr><td>&quot;Precautions&quot;: &quot;Avoid irritants like smoke, strong odors, and extreme temperatures, rest the voice, avoid throat clearing&quot;,</td></tr><tr><td>&quot;Possible Causes&quot;: &quot;Viral infection, seasonal allergies, irritants, postnasal drip&quot;</td></tr></table></body></html>

4.1.3. Mental Illness—Prompt

Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: {   
age: 31,   
Symptoms: “obsessive Compulsive Disorder (OCD), Obsessive Compulsive Personality Disorder $\overline { { ( O C P D ) } }$ , and phobias, Personality disorders, Paranoia, disturbances in thinking, disturbances in emotional regulation, disturbances in behaviour, Anxiety Disorders, depression, Bipolar Disorder, feeling sad, Schizophrenia, attention deficit hyperactivity disorder (ADHD), autism, Autism spectrum disorder (ASD), psychosis, Mental disorders, Eating disorders, Post traumatic stress disorder

(PTSD), Dissociation and dissociative disorders, Anxiety and panic attacks, Borderline personality disorder (BPD), Loneliness, Stress, Suicidal feelings, Trauma, addiction, social anxiety disorder”,

Habits: “”,   
History: “”,   
Allergies: “”,   
Diagnostic Data: “ ”   
} Output: {   
Natural Remedies: “mindfulness, relaxation techniques, breathing techniques, learning to be assertive, dietary adjustments, meditation and yoga, exercise, physically active, building self-esteem, structured problem solving, support groups, family interventions, cognitive problem solving, social skills training, social support, Skills training, Lifestyle Modifications, Keeping a journal, Socialize, delve into a hobby, refocus mind, socialize”,

Over the Counter Medicines:

Prescription Medication: “Antidepressants, anti-anxiety medication, Selective Serotonin Reuptake Inhibitor (SSRI), Benzodiazepines, Buspirone, Tricyclics, Monoamine oxidase inhibitors (MAOIs), Beta blockers, Atypical Antipsychotics,”,

Medical Treatment: “Talk based therapies, Lifestyle and behavioural advice, psychoeducation, counselling and cognitive behavioural therapy, psychosocial rehabilitation, psychosocial interventions, psychological treatments, Cognitive behavioral therapy (CBT), Exposure and response prevention (ERP), Behavioral therapy, Speech therapy, Occupational therapy, Social skills therapy, Counseling, cognitive therapy, Psychotherapy,”,

Preventive Measures: “Develop healthy coping mechanisms, maintain a routine, prioritize selfcare, establish a support system”,

Precautions: “Avoid alcohol and recreational drugs, Quit smoking, cut back or quit drinking caffeinated beverages, avoid triggers or stressors”,

Possible Causes: “genetic predisposition, environmental factors, traumatic life events” }

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution. Query#3: “{age: 22, Symptoms: “anxiety, depressed, negative emotions, pessimistic”}” The output generated by ChatGPT for Query#3 is shown below in Figure 3.

![](img/1a17cb30befae1df61f1669f132e26bca5ba7d1a464a1e7bdf1bd2c1774dd631.jpg)  
Figure 3. ChatGPT output for Query#3.

4.1.4. Dental Issues—Prompt Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: { age: 41,

Symptoms: “cracks fractures and cavities, Chipped Tooth, tooth decay, sensitive teeth, Inflam mation of tooth pulp, cracked tooth, impacted tooth, Persistent Bad breath, Black or brown spots on the teeth, Gingivitis, swollen gums, bleeding gums, toothache, periodontitis, swelling in jaw, pain while chewing and biting, gum irritation, Sharp, jabbing tooth pain, Shrinking and receding gums, red swollen tender gums, Stained Teeth”,

Habits: “sweet tooth, each too much chocolates”,   
History: “”,   
Allergies: “”,   
Diagnostic Data: “ ”   
}

Output: { Natural Remedies: “Saltwater rinse, Hydrogen peroxide rinse, Ice packs”,

Over the Counter Medicines: “acetaminophen, ibuprofen, Orajel, Toothache Oil, Oral Pain Relief, Genexa Pain Reliever, Gum Relief gel, Toothache Spray, Anbesol Pain Relief, Advil Liqui-Gels”,

Prescription Medication: “Antibiotics, pain relievers ”,

Medical Treatment: “dental restoration like dental filling or dental crown, inlay, onlay, dental X-ray, ceramic restoration, Root canal therapy, tooth extraction, dental bridge, dental implant, sealants and fluoride treatments”,

Preventive Measures: “brush teeth twice a day, use fluoride toothpaste, use toothbrush with softer bristles, Floss between teeth once a day, Use an antibacterial mouthwash twice a day, don’t smoke, thorough cleaning from dental health professional, regular dental checkups”,

Precautions: “avoid eating sugary and acidic foods, avoid or limit soft drinks and ice creams, visit dentist regularly for exams and cleanings, avoid cold air, avoid hot and cold drinks”,

Possible Causes: “Poor oral hygiene, eating extreme hot and cold foods which worns off the enamel, soft drinks, smoking, Chewing hard foods, Grinding of teeth while asleep, Brushing teeth too hard too often and too long, consuming plenty of sugary and acidic foods such as soda and sweets over a long period of time, Bedtime Bottles for kids, Cough Drops, Gummy Candy, Soda, Opening Stuff With Teeth, Sports drinks, Potato Chips, Constant Snacking, Chewing on Pencils, Frequently drinking Tea Coffee wine, Binge Eating”

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution.

Query#4: “{age: 35, Symptoms: “dental cavities, swollen gums”, Habits: “drink tea and coffee twice a day”}” The output generated by ChatGPT for Query#4 is shown below in Figure 4.

<html><body><table><tr><td>&quot;Natural Remedies&quot;: &quot;Saltwater rinse, Clove oil, Aloe vera gel&quot;,</td></tr><tr><td>&quot;Over the Counter Medicines&quot;: &quot;Toothache Gel, Oral Pain Relief, Ibuprofen, Acetaminophen, Anbeso! Pain Relief, Orajel&quot;,</td></tr><tr><td>&quot;Prescription Medication&quot;: &quot;Antibiotics, Prescription strength fluoride toothpaste&quot;,</td></tr><tr><td>&quot;Medical Treatment&quot;: &quot;Dental filling, Root canal therapy, Scaling and root planing&quot;,</td></tr><tr><td>&quot;Preventive Measures&quot;: &quot;Limit sugary and acidic beverages, Brush teeth twice a day with fluoride</td></tr><tr><td>toothpaste, Floss daily, Reduce tea and coffee intake, Regular dental check-ups&quot;,</td></tr><tr><td>&quot;Precautions&quot; &quot;Avoid sugary snacks and drinks, Rinse mouth after drinking tea or coffee, Maintain good oral hygiene, Avoid tobacco products&quot;,</td></tr><tr><td>&quot;Possible Causes&quot;: &quot;Poor oral hygiene, Consuming sugary and acidic beverages, Tea and coffee consumption, Bacteria in the mouth due to cavities&quot;</td></tr></table></body></html>

Figure 4. ChatGPT output for Query#4.

4.1.5. High Blood Pressure—Prompt Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: {   
age: 53,   
Symptoms: “headaches, blurred vision, chest pain, dizziness, difficulty breathing, nausea, vomiting,   
anxiety, confusion, buzzing in the ears, nosebleeds, abnormal heart rhythm”,   
Habits: “eat oily and salty food”,   
History: “”,   
Allergies: “”,   
Diagnostic Data: “systolic blood pressure readings is greater than 140 mmHg, diastolic   
blood pressure readings is greater than $9 0 \mathrm { m m H g ^ { \prime \prime } }$   
}   
Output: {   
Natural Remedies: “eating a healthier diet, eating low-salt diet, quitting tobacco, losing weight,   
being physically active, exercise”,

Over the Counter Medicines:

Prescription Medication: “Water pills, diuretics, ACE inhibitors, enalapril and lisinopril, Angiotensin-2 receptor blockers (ARBs), losartan and telmisartan, calcium channel blockers, amlodipine and felodipine, Diuretics, hydrochlorothiazide, chlorthalidone, Angiotensin-converting enzyme (ACE) inhibitors, Beta blockers, Renin inhibitors, Aldosterone antagonists, Alpha blockers, Alpha-beta blockers, Central acting drugs, Vasodilators”,

Medical Treatment: “urine and blood test, Electrocardiogram (ECG or EKG)”,

Preventive Measures: “Lifestyle changes, Eat more vegetables and fruits, sit less, Be more physically active, walking, running, swimming, activities that build strength, aerobic activity, Lose weight if overweight, Keep appointments with your healthcare professional, Get regular exercise, Develop healthy sleeping habits to get a good night’s rest, Use less salt, Manage stress, Maintain a healthy weight, eat a healthy diet rich in whole grains, fruits and vegetables, and low-fat dairy products”,

Precautions: “avoid eating salty food, avoid food high in saturated or trans fats, stop smoking, avoid tobacco and alcohol,”,

Possible Causes: “old age, genetics, overweight, obesity, physical inactivity, high-salt diet, drinking too much alcohol, excessive salt consumption, diet high in saturated fat and trans fats, low intake of fruits and vegetables, consumption of tobacco and alcohol, family history of hypertension, age over 65”   
1

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution. Query#5: “{age: 47, Symptoms: “hypertension, chest pain, dizziness”, Habits: “smoke and drink alcohol”}” The output generated by ChatGPT for Query#5 is shown below in Figure 5.

![](img/ec2df50b122f559972034a8fb83f76429fade8b1cada06e50df861118e70a556.jpg)  
Figure 5. ChatGPT output for Query#5.

4.1.6. Low Blood Pressure—Prompt Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: {   
age: 53,   
Symptoms: “Confusion, Dizziness or lightheadedness, Nausea, Fainting, passing out, syncope,   
Fatigue, Neck or back pain, Headache, Distorted or Blurred vision, Heart palpitations, fluttering,   
vomiting, Fast, shallow breathing, Fatigue or weakness, Feeling tired, sluggish or lethargic, Confu  
sion or trouble concentrating, Pale skin, Low cardiac output, Low urine output”,   
Habits: “”,   
History: “”,   
Allergies: “”,   
Diagnostic Data: “blood pressure is below 90/60 mmHg”   
}   
Output: {   
Natural Remedies: “Increasing salt intake, Eating smaller meals with fewer carbohydrates, Drink   
more water, Drink alcohol in moderation, drinking more fluids”,   
Over the Counter Medicines: “”,   
Prescription Medication: “”   
Medical Treatment: “urine and blood test, Electrocardiogram (ECG or EKG), Increasing blood   
volume, fluid resuscitation, intravenous (IV) fluids or plasma or blood transfusions, Making blood   
vessels constrict,”,   
Preventive Measures: “”,

Precautions: “”,

Possible Causes: “Prolonged bed rest (orthostatic), Depression, Parkinson’s disease, Pregnancy, low blood volume, Endocrine problems, Allergic reaction (anaphylaxis), Nutritional deficiencies, Dehydration, Orthostatic hypotension, Extreme temperatures, Anti-anxiety medicines, antidepressants, Diuretics, Painkillers, Not drinking enough fluids (dehydration), Hormonal problems such as an underactive thyroid (hypothyroidism), diabetes, or low blood sugar (hypoglycemia), overthe-counter medications, prescription medicines, Heart arrhythmias, dehydration from vomiting, diarrhea, or fever, Loss of blood from bleeding, High or Low body temperature” }

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution.

Query#6: “ {age: 51, Symptoms: “hypotension, Feeling tired, Fainting”}” The output generated by ChatGPT for Query#6 is shown below in Figure 6.

![](img/61f7b2dbc384f14747c21dd4bc63b9a633df470ab06fb77e6a732c5ae1d301b3.jpg)  
Figure 6. ChatGPT output for Query#6.

4.1.7. LDL (Bad) Cholesterol—Prompt

Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: { age: 41, Symptoms: “” Habits: “”, History: “”, Allergies: “”,

Diagnostic Data: “ ” }

Output: {   
Natural Remedies: “Positive lifestyle habits, eating healthy, exercise, maintain healthy weight,   
manage stress, get enough good qaulity sleep”,

Over the Counter Medicines:

Prescription Medication: “statins, mipomersen, ezetimibe, bile acid sequestrants, bempedoic acid, PCSK9 Inhibitors, lomitapide and evinacumab, Bile acid sequestrants, Cholesterol absorption inhibitors, Zetia, Bile-acid-binding resins, cholestyramine (Prevalite), colesevelam (Welchol) and colestipol (Colestid), Fibrates, Niacin, Omega-3 fatty acid supplements, nicotinic acid”,

Medical Treatment: “blood test, LDL apheresis”,

Preventive Measures: “healthy diet that limits saturated fat, maintain healthy weight, physical activity”,

Precautions: “avoid smoking, usage of tobacco products”,

Possible Causes: “Family history of high cholesterol, familial hypercholesterolemia, Unhealthy eating habits, Not being physically active, Being overweight, Smoking, Tobacco use, exposure to second-hand smoke, stress, drinking alcohol, less active, overweight, obesity, Genetic conditions” }

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution.

Query#7: “{age: 38, Symptoms: “low-density lipoprotein cholesterol”, Habits: “eat oily food”}” The output generated by ChatGPT for Query#7 is shown in Figure 7.

![](img/4fd048821a0a87240ca4da802584055c84e3b3e00be5ae24612a85c45e779576.jpg)

Figure 7. ChatGPT output for Query#7.

# 4.1.8. Diabetes—Prompt

Template

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Medical Treatment, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

# PatientInfo: {

age: 41,   
Symptoms: “Urinating often, Feeling very thirsty, Feeling very hungry even though eating enough,   
Extreme fatigue, Blurry vision, Cuts and bruises are slow to heal, Weight loss even though eating   
more, tingling, pain, or numbness in the hands or feet, Lose weight without trying, dry skin, sores   
that heal slowly, more infections than usual, Presence of ketones in the urine, Feeling irritable or   
having other mood changes, Dry mouth and itchy skin, Yeast infections, Unplanned weight loss,   
Nausea and vomiting”,   
Habits: “”,   
History: “”,   
Allergies: “”,   
Diagnostic Data: “ ”   
}

Output: { Natural Remedies: “”

Over the Counter Medicines:

Prescription Medication: “metformin, sulfonylureas, sodium-glucose co-transporters type 2 (SGLT2) inhibitors, Alpha-glucosidase inhibitors, Biguanides, Dopamine-2 agonist, Bromocriptine, Dipeptidyl peptidase-4 (DPP-4) inhibitors, Glucagon-like peptide-1 (GLP-1) receptor agonists, Meglitinides, Sodium-glucose transport protein 2 (SGLT2) inhibitors, Sulfonylureas, Thiazolidinediones (TZDs), Metformin, GLP-1 and Dual GLP-1/GIP Receptor Agonists, Insulin releasing pills (secretagogues), Starch blockers, Repaglinide, Nateglinide”,

Medical Treatment: “Incretin based therapies”,

Preventive Measures: “maintain health body weight, stay physically active, eat a healthy diet”,

Precautions: “avoid sugar and saturated fat, avoid smoking, avoid tobacco, Monitor Your Blood Sugar Levels, Eat A Healthy Diet, Exercise Regularly, Manage Stress Levels, reduce alcohol intake”,

Possible Causes: “Insulin resistance, Autoimmune disease, Hormonal imbalances, Pancreatic damage, Genetic mutations, Overweight, obesity, Genes and family history of diabetes, high blood pressure, high cholesterol, physically inactive”   
}

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution. Query#8: “{age: 62, Symptoms: “Urinating often, Cuts and bruises are slow to heal”, Habits: “eating too much sweets”}” The output generated by ChatGPT for Query#8 is shown below in Figure 8.

![](img/aa8c8b98b65ea6620f0c46f37ef3f46303ba9ff241b7db69660b19c1404b792a.jpg)  
Figure 8. ChatGPT output for Query#8.

4.1.9. Joint Issues—PromptTemplate

Instruction: You are a healthcare provider. Provide remedies for the patient based on the symptoms they are describing. Generate output in json format, having “Natural Remedies, Over the Counter Medicines, prescription Medication, Clinical Care, Preventive Measures, Precautions, and Possible Causes” as keys.

Context: Below is an example

PatientInfo: {   
age: 65,   
Gender: “Male”,   
height: “”,   
weight: “”,   
BMI: “”,   
Symptoms: “joint pain, joint, Stiffness, joint swelling, Inflammation, joint redness, joint warmness,   
Tenderness or sensitivity around a joint, heat or warmness around joints, reduced range of motion,   
Reduced ability to move the joint, Redness and warmth of the skin around a joint, Warm, red,   
tender joints, Difficulty moving a joint, Loss of flexibility, Grating sensation, Difficulty walking or   
climbing stairs, Popping or cracking sound, Grinding sensation,”,

History: “”, Habits: “run 3 miles every day on road”,

Allergies: “”,   
Injuries: “”,   
Diagnostic Data: “ANA Test, CBC, Uric Acid Test”   
} Output: {   
Natural Remedies: “Ice packs and heating pads, Regular exercise, physical therapy, Stretching, Yoga, Swimming, Losing excess weight, Eating a healthy plant-based diet, Acupuncture, Massage therapy”,

Over the Counter Medicines: “anti-inflammatory medicine like acetaminophen, nonsteroidal anti-inflammatory drugs (NSAIDs), Ointments that contain menthol or capsaicin to soothe aching joints, glucosamine, chondroitin, and fish oil, supplements, Ibuprofen, Aspirin”,

Prescription Medication: “Disease-modifying antirheumatic drugs (DMARDs), injections, Azathioprine, Adalimumab, Etanercept, Methotrexate, Hydroxychloroquine, Infliximab, Leflunomide, Sulfasalazine, Celecoxib, Naproxen, Diclofenac, Abatacept, Certolizumab pegol, Golimumab, Meloxicam, Acetaminophen, Anakinra, Corticosteroids, Diclofenac sodium with misoprostol, Rituxan, Actemra, Hyaluronic acid therapy, Surgery”,

Preventive Measures:

Medical Treatment: “X-ray, ultrasound, MRI, CT Scan”,

Precautions: “Doing low-impact exercise, Rest, Avoiding tobacco products, avoid running on hard surface (e.g., road), Always wearing proper protective equipment, Using assistive devices (e.g., Canes, crutches, and walkers)”,

Possible Causes: “age, overweight, obesity, wear and tear, running, playing too much sports” }

Sample Query and Output

Based on the above template, the PCP can enter the following query into the ChatGPT prompt and request a possible solution. Query#9: “{age: 73, Gender: “Male”, Symptoms: “Knee Joint pain”, Habits: “Cycling for 30 min everyday, Smoking”}” The output generated by ChatGPT for Query#9 is shown in Figure 9.

![](img/e03904b3e803425c745ccfa5a7358eda57426a9e5d0cb6b281e11777732b9874.jpg)

Figure 9. ChatGPT output for Query#9.

# 4.2. Bot Approach

In the second approach, a custom ChatBot can be built using some examples. PCPs can then interact with these custom-built ChatBots. For example, ChatGPT provides this feature of creating a ‘customized version’ for a specific purpose or goal. Figure 10 illustrates an example where we create a custom bot for answering obesity-related questions. We also incorporate sample examples (few-shot prompt) as part of the knowledge graph.

![](img/6ccbae7c08b2667ad717c6ddfc5c60e5cb781aeaee74bfcbc8fd74de56af6c86.jpg)  
Figure 10. Configuration of custom ChatBot.

Once the bot is created, the PCPs can interact with it and provide patient information as demonstrated in Figure 11.

![](img/d6f7c33316dce5488573c78be88ce6566401ad11193ffc5e58c875ac2a59634c.jpg)  
Figure 11. Providing patient information.

Figure 12 showcases the output snippet generated by the ChatBot for the query provided in Figure 11. The complete output generated by the ChatBot is displayed in Figure 13.

![](img/61f9810e87651cad7695a65e6fbfc670f3e666617c36ffa1ded74fc093dacbb8.jpg)  
Figure 12. Output snippet

![](img/cd19f5b3085e698e76e9cc4c5a43ae237c3246856b0b3f1d706e85572b9fbd02.jpg)  
Figure 13. Complete output.

Overall, although we do not cover all the disciplines in the medical domain, we propose a unique approach on how to construct effective prompt templates. These templates can be used by PCPs to effectively retrieve the desired results by providing a patient’s history, symptoms, habits, allergies, injuries and/or diagnostic data into the prompt context. However, when interacting with LLMs using such prompts, measures should be taken to secure the patient’s personal and medical information.

# 5. Discussion

As the field of prompt engineering for generative AI continues to evolve, family medicine practitioners and researchers must be aware of the challenges and opportunities that lie ahead. We can harness the full potential of AI to improve patient care and outcomes by addressing these challenges and exploring new directions.

# 5.1. Ensuring the Safety, Accuracy, and Reliability of Generative AI in Healthcare

One of the primary challenges in implementing generative AI in healthcare is ensuring the safety, accuracy, and reliability of the AI-generated outputs. Despite the promising results demonstrated by LLMs in various medical domains, there are still concerns about the potential for errors, biases, and unintended consequences [26]. To address these concerns, it is essential to establish robust evaluation and validation frameworks that assess the performance of AI against human experts and real-world clinical outcomes. This may involve conducting large-scale clinical trials, developing standardized benchmarks and metrics, and creating guidelines for the transparent reporting of AI model development and deployment processes.

# 5.2. Navigating Regulatory and Legal Considerations

Another significant challenge is navigating the regulatory and legal landscape surrounding the use of generative AI in healthcare. As AI-based tools and applications become more prevalent in clinical practice, there is a need for clear guidelines and policies that govern their development, validation, and deployment. This includes addressing data privacy, informed consent, liability, and intellectual property rights [27]. Collaboration between healthcare providers, AI researchers, policymakers, and legal experts is essential to create a regulatory framework that balances the need for innovation with patient safety and ethical considerations.

For instance, there are 18 identifiers that are considered protected health information. The disclosure of any of these identifiers is considered a HIPAA violation. Most of these identifiers represent attributes such as geographic regions smaller than a state—information that one would not normally think of as identifiable. Other examples are patient names, including nicknames; dates of birth; admission or discharge dates; and social security numbers [28]. ChatGPT is not HIPAA compliant and cannot be used to (for example) summarize patients’ notes or compile letters to patients that include protected health information since OpenAI might not have Business Associate Agreement with the covered entities and business associates.

However, there are ways to use ChatGPT in compliance with HIPAA [29]. A data governance framework should be in place to ensure compliance with privacy regulations and to promote responsible data handling practices. By implementing strong privacy protections and ensuring transparency and accountability in the use of ChatGPT, healthcare organizations can maximize the benefits of AI while protecting patient privacy and trust [30]. To mitigate privacy risks, healthcare organizations should implement robust security measures, including encryption, access controls, and regular vulnerability assessments.

# 5.3. Continuously Updating Prompts to Reflect Evolving Medical Knowledge and Practices

The rapid pace of medical research and the constant evolution of clinical practice guidelines present another challenge for prompt engineering in healthcare. To ensure that AI-generated outputs remain accurate, relevant, and up to date, prompt engineers must continuously update and refine the prompts to reflect the latest medical knowledge and best practices. This requires a proactive approach to monitoring the medical literature, engaging with domain experts, and incorporating feedback from healthcare providers and patients. Developing automated tools and pipelines that can efficiently extract, synthesize, and integrate new knowledge into existing prompts could help streamline this process and reduce the burden on prompt engineers.

# 5.4. Fostering Interdisciplinary Research and Collaboration

Fostering interdisciplinary research and collaboration is crucial to fully realize the potential of generative AI in family medicine. This involves bringing together experts from various fields, such as medicine, computer science, data science, psychology, and bioethics, to work on common challenges and share knowledge and resources. Collaborative efforts can lead to the development of more sophisticated and robust AI models, identifying novel applications and use cases, and creating best practices and guidelines tailored to the unique needs of family medicine. Furthermore, promoting collaboration between academia, industry, and healthcare organizations can accelerate the translation of research findings into clinical practice and ensure that the benefits of generative AI are widely accessible to patients and providers.

By addressing these challenges and pursuing interdisciplinary research and collaboration, we can create a future in which generative AI is seamlessly integrated into family medicine practice, empowering clinicians to deliver more personalized, efficient, and effective care to their patients.

# 6. Conclusions

In this article, we have explored the emerging field of prompt engineering and its potential to revolutionize family medicine. We have discussed the key concepts and techniques involved in designing and optimizing prompts for generative AI models, and we have highlighted the various applications of prompt engineering in primary care, from enhancing patient–provider communication to streamlining administrative tasks and supporting medical education. Moreover, we have emphasized the importance of adhering to best practices in prompt engineering, such as incorporating domain-specific knowledge, engaging in iterative refinement and validation, and addressing ethical considerations and potential biases. By following these best practices, we can ensure that the use of generative AI in family medicine is safe, effective, and aligned with the values and goals of patient-centered care.

As we look to the future, it is clear that prompt engineering and generative AI will play an increasingly important role in transforming healthcare delivery. Family clinicians have a unique opportunity to shape this transformation by actively engaging with prompt engineering and collaborating with AI researchers and developers. Family medicine clinicians can help create AI tools and applications tailored to primary care practice’s specific needs and challenges by providing their clinical expertise and insights. We call upon family clinicians to embrace this opportunity and take an active role in developing and deploying generative AI in their field. This may involve participating in research studies, providing feedback on AI-generated outputs, or advocating for policies and guidelines that promote the responsible use of AI in healthcare. By working together, family medicine clinicians and AI experts can create a future in which generative AI is seamlessly integrated into primary care practice, empowering clinicians to deliver more personalized, efficient, and effective patient care.

Ultimately, the vision for AI-assisted healthcare delivery is one in which technology and human expertise are harmoniously combined to improve patient outcomes, reduce healthcare disparities, and enhance the well-being of both patients and providers. By harnessing the power of prompt engineering and generative AI, family medicine can lead the way in realizing this vision and shaping a brighter future for healthcare.

Author Contributions: Conceptualization, T.F.H.; Methodology, R.P.; Software, R.P.; Validation, V.B.; Formal analysis, R.P.; Investigation, T.F.H.; Writing—original draft, R.P. All authors have read and agreed to the published version of the manuscript.

Funding: This research received no external funding.

Data Availability Statement: No new data were created or analyzed in this study. Data sharing is not applicable to this article.

Conflicts of Interest: The authors declare no conflicts of interest.

# References

1. McCulloch, W.S.; Pitts, W.A. Logical calculus of the ideas immanent in nervous activity. Bull Math Biophys. 1943, 5, 115–133. [CrossRef]   
2. Hebb, D.O. The Organization of Behavior: A Neuropsychological Theory, 1st ed.; Psychology Press: New York, NY, USA, 1949.   
3. Rosenblatt, F. The perceptron: A probabilistic model for information storage and organization in the brain. Psychol. Rev. 1958, 65, 386–408. [CrossRef] [PubMed]   
4. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A.N.; Kaiser, Ł.; Polosukhin, I. Attention is all you need. Adv. Neural Inf. Process. Syst. 2017, 30. [CrossRef]   
5. ChatGPT Passes Turing Test: A Turning Point for Language Models. Available online: https://www.mlyearning.org/chatgptpasses-turing-test/ (accessed on 15 June 2024).   
6. Sallam, M. ChatGPT utility in healthcare education, research, and practice: Systematic review on the promising perspectives and valid concerns. Healthcare 2023, 11, 887. [CrossRef] [PubMed] [PubMed Central]   
7. Heston, T.F.; Khun, C. Prompt engineering in medical education. Int. Med. Educ. (IME) 2023, 2, 198–205. [CrossRef]   
8. Meskó, B. Prompt engineering as an important emerging skill for medical professionals: Tutorial. J. Med. Internet Res. 2023, 25, e50638. [CrossRef] [PubMed] [PubMed Central]   
9. Liévin, V.; Hother, C.E.; Motzfeldt, A.G.; Winther, O. Can large language models reason about medical questions? Patterns 2024, 5, 100943. [CrossRef] [PubMed] [PubMed Central]   
10. Ahmed, A.; Zeng, X.; Xi, R.; Hou, M.; Shah, S.A. MED-Prompt: A novel prompt engineering framework for medicine prediction on free-text clinical notes. J. King Saud Univ.-Comput. Inf. Sci. 2024, 36, 101933. [CrossRef]   
11. Greyling, C. Eight Prompt Engineering Implementations, Medium. 2023. Available online: https://cobusgreyling.medium.com/ eight-prompt-engineering-implementations-fc361fdc87b (accessed on 15 June 2024).   
12. Wang, L.; Chen, X.; Deng, X.; Wen, H.; You, M.; Liu, W.; Li, Q.; Li, J. Prompt engineering in consistency and reliability with the evidence-based guideline for LLMs. Npj Digit. Med. 2024, 7, 41. [CrossRef] [PubMed] [PubMed Central]   
13. Prompt Engineering for Generative AI. Google Machine Learning Education. 2023. Available online: https://developers.google. com/machine-learning/resources/prompt-eng (accessed on 15 June 2024).   
14. Chen, B.; Zhang, Z.; Langrené, N.; Zhu, S. Unleashing the potential of prompt engineering in large language models: A comprehensive review. arXiv 2023, arXiv:2310.14735. https://doi.org/10.48550/arxiv.2310.14735.   
15. Lin, Z.How to write effective prompts for large language models. Nat. Hum. Behav. 2024, 8, 611–615. [CrossRef] [PubMed]   
16. Arora, S.; Narayan, A.; Chen, M.F.; Orr, L.; Guha, N.; Bhatia, K.; Chami, I.; Re, C. Ask me anything: A simple strategy for prompting language models. arXiv 2022, arXiv:2210.02441. [CrossRef].   
17. Zhou, D.; Schärli, N.; Hou, L.; Wei, J.; Scales, N.; Wang, X.; Schuurmans, D.; Cui, C.; Bousquet, O.; Le, Q.; et al. Least-to-most prompting enables complex reasoning in large language models. arXiv 2022, arXiv:2205.10625. [CrossRef].   
18. Zamfirescu-Pereira, J.D.; Wong, R.Y.; Hartmann, B.; Yang, Q. Why Johnny can’t prompt: How non-AI experts try (and fail) to design LLM prompts. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems, Hamburg, Germany, 23–29 April 2023; ACM: New York, NY, USA, 2023; pp. 1–21. [CrossRef]   
19. Guilleminot, S.; Cadogan, M. AI Prompting Techniques. Life in the Fast Lane. 2024. Available online: https://litfl.com/aiprompting-techniques/ (accessed on 15 June 2024).   
20. Hu, Y.; Chen, Q.; Du, J.; Peng, X.; Keloth, V.K.; Zuo, X.; Zhou, Y.; Li, Z.; Jiang, X.; Lu, Z.; et al. Improving large language models for clinical named entity recognition via prompt engineering. arXiv 2024, arXiv:2303.16416. [CrossRef].   
21. Khan, B.; Fatima, H.; Qureshi, A.; Kumar, S.; Hanan, A.; Hussain, J.; Abdullah, S. Drawbacks of artificial intelligence and their potential solutions in the healthcare sector. Biomed. Mater. Devices 2023, 1, 731–738. [CrossRef] [PubMed]   
22. Alnegheimish, S.; Guo, A.; Sun, Y. Using natural sentence prompts for understanding biases in language models. In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Seattle, WA, USA, 10–15 July 2022; pp. 2824–2830.   
23. Xu, Z.; Peng, K.; Ding, L.; Tao, D.; Lu, X. Take Care of Your Prompt Bias! Investigating and Mitigating Prompt Bias in Factual Knowledge Extraction. arXiv 2024, arXiv:2403.09963.   
24. Farhud, D.D.; Zokaei, S. Ethical issues of artificial intelligence in medicine and healthcare. Iran. J. Public Health 2021, 50, i–v. [CrossRef] [PubMed]   
25. Singhal, K.; Azizi, S.; Tu, T.; Mahdavi, S.S.; Wei, J.; Chung, H.W.; Scales, N.; Tanwani, A.; Cole-Lewis, H.; Pfohl, S.; et al. Large language models encode clinical knowledge. Nature 2023, 620, 172–180. [CrossRef] [PubMed] [PubMed Central]   
26. Tang, L.; Sun, Z.; Idnay, B.; Nestor, J.G.; Soroush, A.; Elias, P.A.; Xu, Z.; Ding, Y.; Durrett, G.; Rousseau, J.F.; et al. Evaluating large language models on medical evidence summarization. Npj Digit. Med. 2023, 6, 158. [CrossRef] [PubMed]   
27. Gerke, S.; Minssen, T.; Cohen, G. Ethical and legal challenges of artificial intelligence-driven healthcare. In Artificial Intelligence in Healthcare; Academic Press: New York, NY, USA, 2020; pp. 295–336.   
28. Hetrick, C. Why Doctors Using ChatGPT Are Unknowingly Violating HIPAA. Available online: https://priceschool.usc.edu/ news/chatgpt-doctors-data-privacy-hipaa/ (accessed on 7 July 2023).   
29. Alder, S. Is ChatGPT HIPAA Compliant? Available online: https://www.hipaajournal.com/is-chatgpt-hipaa-compliant/ (accessed on 15 December 2023).   
30. Wang, C.; Liu, S.; Yang, H.; Guo, J.; Wu, Y.; Liu, J. Ethical considerations of using ChatGPT in health care. J. Med. Internet Res. 2023, 25, e48009. [CrossRef] [PubMed]

Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.