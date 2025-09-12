# Analysis and recommendation system-based on PRIsMA checklist to write systematic review

Smita Agrawala\*, Parita Ozaa\*, Riya Kakkara, Sudeep Tanwara,\*, Vishv Jetani a, Jatin Undhada, Anupam Singhb

a Department of Computer Science and Engineering, Institute of Technology, Nirma University, Ahmedabad, Gujarat 382481, India b Department of Computer Science and Engineering, Graphic Era Hill University, Dehradun, Uttarakhand 248002, India

# ARTICLEINFO

# ABSTRACT

Keywords:   
Prisma checklist   
Systematic review   
Citation analysis   
Author frequency   
Entry types(Type of reference- i.e. magazine)   
Meta-analysis   
Data extraction   
Web-based platform   
Review paper   
Term paper

A systematic review prepared by the researchers or users is transparent, complete, and accurate information that gives deep insights into why the review was done, what they did, and what they found. Various tools can be utilized to conduct a systematic review of the research papers, which is essential for researchers or users who wish to write and publish papers and those who review and evaluate them. By conducting a systematic review, users can gain valuable insights into the landscape of existing literature and identify key trends and influential works in their field from references they used in the article. Many researchers enhance the strength of their systematic review articles by manually preparing and including the analysis of the preferred reporting items for systematic reviews and meta-analyses (PRIsMA)-2020 checklist and flow diagram. Motivated by the aforementioned discussion, this paper uses a web-based application to provide a graphical visualization of the analysis and flow diagram for the PRIsMA. This application is valuable for stakeholders or users involved in the research process, including researchers, students, editors, reviewers, academic institutions, funding agencies, and publication houses. The proposed application enables stakeholders or users to assess the quality of the articles considered for sys. tematic review more effectively along with the student writing assessment. Offering a visual display of the results from individual studies and syntheses enhances their ability to analyze and interpret the findings of the research articles by analyzing reference of research papers concerning year, entry type, authors, keywords, and journals.

# 1. Introduction

A systematic review is a research methodology that follows a rigorous and structured approach to identify, select, and evaluate all relevant studies on a specific reearch question. The primary objective is to summarize the available evidence on the particular topic or research question, providing comprehensive and unbiased overview of the curent knowledge in the field (larke etal., 2015. Several key features must be fllowed to ensure the reliabilit and validt of the systematic review of the reearch artices. Firstly, a clear and welldefined research question should be established based on a specific topic or problem. Secondly, acomprehensive search strategy should be implemented to identify allrelevant studies on the topic, including published and unpublished literature. Thirdly, explicit inclusion and exclusion criteria should be established for selecting studies that meet the research question (Aromataris & Pearson 2014.

Additionally, a systematic review should have a systematic and standardized method for extracting data from the included studies and assessing the included studies' quality using etablished Criteria If necessary, data synthesis should be conducted using appropriate statistical methods to summarize the results of the included studies. Finall, a clear and concise conclusion should be provided based on the available evidence. A systematic review can provide robust and unbiased summary of current knowledge on a particular topic or research question by following these key features. Systematic reviews are used in healthcare, social sciences, and other research fieldsto inform policy and practice decisions. The comparative study of diffrent methodologies used for systematic review, checklists, frameworks and guidelines is presented in Table 1.

Systematic reviews and meta-analyses are important tools in evidence-based research, and establishing guidelines is essential to ensure that these studies are conducted transparently, completely, and accurately. The Prisma (Preferred Reporting Items for Sys. tematic Reviews and Meta-Analyses) checklist is one such guideline that has gained widespread accetance in the research community (Richard et al., 2024. The Prisma checklist was developed in 2009 by an international group of experts in systematic review methodology. Its usage is endorsed by many leading medical journals and databases, such as JAMA and Cochrane Library (Clark t al., 2015. The checklist consists of 27 items covering essential reporting elements of systematic reviews and meta-analyses, including the title, abstract, introduction, methods, and results. These items ensure critical information is noticed and the study is reported trans parently and reproducibly.

# 1.1. Introduction to Web Application

This paper presents a novel web application that provides a bibliometric analysis of the research papers by analyzing their ref. erences. The proposed web application extracts and visualizes meaningful bibliometric data such as research paper tites, author names, reference links, and entry types like book journals, magazines and many more from research paper references. These visuals will sigificantly benefit the research community for the systematic review of the research articles. The bibliometric analysis plays a vital role in evaluating the research pefomance at both individual and instittional level; the proposed we applicatio fill a crucial need in the field by providing a robust plaform for in-depth analysis of the research papers based on its references. The web application is also helpful for generating the Prisma Flow Diagram that depicts the flow of information through the different phases of the systematic review. The proposed web application uses modern web development technologies like Python and Flask. The web application has a user-friendly interfce allowing users to browse research papers and quickly retrieve the bibliometric analysis of its references ater a few clicks. ow, foremost the user-frienines of the we application intrface is mainained by providing easy and understandable access to the stakeholders or users engaged in the web application along with various features such as intuitive, navigation, easy acessibility, and responsiveness The intuitive and responsive are the features of the web application that help stakeholders or users to visualize their research study in a better way. It also helps them to get the desired analysis of ther reference papers easil and concisely with the help of clear intructions and visual cues. Now, there are various users involved in accessing the web application such as reearchers students, publishers, reviewers, funding agncies, and academic insttions. The web application provides equitable privilege to students also to asses their writing skill in terms of grammar and linguistics which furthereseach supervisors can access and check for further improvement. Moreover, supervisors and other stakeholders can directly use the web application for analysis of references of their research papers.

Table 1 Comparative analysis of different review methodologies, checklists, frameworks, and guidelines.   

<html><body><table><tr><td>Review Methods</td><td>Purpose</td><td>Category</td><td>Introduced in Year</td><td>Review Method Proposed By</td></tr><tr><td>MECIR (Higgins et al., 2012</td><td>Ensure that Cochrane reviews are of high quality</td><td>Guidelines</td><td>2011</td><td>Cochrane Collaboration</td></tr><tr><td>PROSPERO (Schiavo, 2019</td><td>reduce the potential for duplication in the systematic reviews</td><td>Database</td><td>2011</td><td>University of York, UK.</td></tr><tr><td>PRISMA (Tricco et al., 2018</td><td>Ensure the transparent reporting of systematic reviews</td><td>Checklist</td><td>2009</td><td>Cochrane authors</td></tr><tr><td>QUORUM (Moher et al., 1999</td><td>Process of assessing the eligibility of studies in the review</td><td>Guidelines</td><td>1999</td><td> international group of experts</td></tr><tr><td>PICO (Eriksen &amp; Frandsen, 2018;</td><td>Commonly used in healthcare research to</td><td>Guidelines</td><td>1990</td><td>Evidence-Based Medicine</td></tr><tr><td>Matthew et al., 2014 SPIDER (Isbister et al., 2005</td><td>guide Specifically designed for qualitative research</td><td>FrameWork</td><td>2014</td><td>Working Group University of Bristol in the UK</td></tr><tr><td>CONSORT (King et al., 2011</td><td>studies Randomization, statistical analysis</td><td>checklist</td><td>1990</td><td>group of medical journals.</td></tr><tr><td>MOOsE (Brooke et al., 2021</td><td>Designed for meta-analyses of observational</td><td>Checklist</td><td>2000</td><td>University of California</td></tr><tr><td>EQUATOR (Altman et al., 2008</td><td>studies It includes 36 items to be reported in health</td><td>Checklist</td><td>2006</td><td>Group of medical journal editors,</td></tr><tr><td>AGREE II (Brouwers et al., 2010</td><td>research Assess the quality of clinical practice guidelines</td><td>Guidelines</td><td>2009</td><td>researchers International collaboration of researcher</td></tr></table></body></html>

# 1.2. Stakeholders

The web application is designed to provide valuable insights and analysis of the research paper references to various users including researchers, publishers, reviewers, funding agencies, academic institutions, university students, and all dealing with research paper writing. .

. The web application is intended for researchers to upload the bibliography file of their research paper to the designed web application for reference analysis. Researchers can personalize their analysis by using different visuals and modifying their references.   
. The web application offers suggestions on whether to include additional references in the research paper or references from a specific year.   
Students can benefit from this web application in the assessment of their own writing. They can use it to analyze their references and ensure the quality and releance of their research papers. It can serve as tool for student writing assessment before submitting it to their research supervisor for further assessment 1.   
Research supervisors can use this web application to evaluate the student's work, while publishers can asss the quality of papers.   
Reviewers with technical expertise use this web application to analyze a specific research paper's keywords and determine if the paper is relevant or sticks to the main context.   
Funding agencies can asss prototype paper results through this web application, whereas academic intitutions can use it to enhance their research paper production.   
. Fig. 1 shows the visualization of the PrismaView web application in which various stakeholders such as university students publishers, academic institutions, funding agencies, reviewers, and researchers can access the web application and use it for referencing research papers and assessig their conducted work For instance, i is also used for student writing asssment in which students can act as a user for assessing their writing in terms of linguistics and grammar and further improve its content for submitting it to the research supervisor.

![](img/7bb935fbe6e02c45e4766a816daefa9fc16ab9391366c24264c60c5def0b9fe9.jpg)  
Fig. 1. Stakeholders engaged with PrismaView Web Application.

# 1.3. Organization

Section II represents a different systematic review methodology study. SectionIII describes the implementation intuition and approach used to build the we application, including data extraction, parsing, and analys. Section IV presents the web application's outcome, challenges facd during development, qualitative and quantitative results, limitations, future directions, and the conclusion.

# 2. Proposed model for prisma analysis and recommended system for paper evaluations

This section presents the proposed model for systematic review analysis and a recommendation system for paper evaluation based on the Prisma checklist. Also, it selected the Prisma checklist for systematic review analysis.

# 2.1. Selection of Prisma checklist for systematic review analysis

The web application utilizes the Prisma checklist to generate visuals and provide appropriate suggestions. This checklist ensures that the reorting of systematic reviews and met-analyes is transparent, complete, and acurate. In addition, the tools utilization of this checklist provides that the systematic reviews are of the highest quality. Based on the Graph in Fig. 2, the Prisma checklist i the most prevalent among the four methods analyzed for reporting systematic reviews. Prisma is a widely recognized and widely used guideline that has been shown to enhance the quality and transparency of such studies. Itis also worth noting that the figure mentions PROSPERO, a database for systematic reviews. It is an essential tol for researchers or students who are conducting systematic reviews. PROSPERO allows researchers to register their systematic review protocol, which helps to reduce duplication of effrt and increase transparency in the reearch proces Page et al., 2018. Moreover, i is also equally useful for student writing assments to improve their writing skills before submitting to a supervisor or publisher.

# 2.2. Proposed model flow

Fig. 3 llustrates the workflow of asystem that receives input, undergoes processing, and generates output in a specific format. The figure serves as a visual rpresentation of the various stages involved in the system's operation. It depicts the processof data gathering input data processing, and, ultimately, data repreentation as the final outut. Further details regarding this proces will be discussed in the subsequent section.

Algorithm 1. Data Gathering.

<html><body><table><tr><td>Require: Document File with .bib Extension.</td><td></td></tr><tr><td colspan="2">Ensure: Document File with .json Extension with useful data</td></tr><tr><td>2:</td><td>1: function DATAGATHERING</td></tr><tr><td>3:</td><td>Input: bibtex_file</td></tr><tr><td>4:</td><td>parsed_data  parse_bibtex_file(bibtex_file)</td></tr><tr><td>5:</td><td>json_data  empty_json_object( json_data[&quot;title&#x27;]  parsed_data[&quot;title&quot;]</td></tr><tr><td>6:</td><td></td></tr><tr><td>7:</td><td>json_data[&quot;authors&quot;]  parsed_data[&quot;authors&quot;] json_data[&quot;year&#x27;] &lt; parsed_data[&quot;year&#x27;]</td></tr><tr><td>8:</td><td>json_data[&quot;entryType&quot;]  parsed_data[&quot;entrytype&quot;]</td></tr><tr><td>9:</td><td>json_string  serialize_json(json_data)</td></tr><tr><td>10:</td><td>save_json_to_file(json_string)</td></tr><tr><td colspan="2">11: end function</td></tr></table></body></html>

# 2.2.1. Data gathering and extraction

Algorithm 1 ilustrates the working of dataextraction and parsing from the given input bib fil. The proposed web application aims to provide researchers with a wide array of visualizations that can be seamlessly integrated into their research papers, offring a streamlined approach to presenting data and improving the overal readability of their work. Data collection i facilitated using a bib file, which can be conveniently sourced from diffrent reference management tools commonly used by researchers. The entire application is developed using the Flask Python framework, which provides various libraries that make the development process more manageable It incorporates the Plotly library, a robust and widely adopted tool for generating interactive data visualizations. The library provides researchers with various customization options, enabling them to taior the visualizations to their needs. Further, we focus on data parsing and processing steps after performing the data gathering and extraction for analyzing the research papers farly

![](img/11d71775098be139a960f4d50a7a6d94d6e53a26cd628f86b49cc0bf3224cbe1.jpg)  
Fig. 2. Comparison of different Review methods: Data from Scopus.

![](img/0d66c05f1ab00722e693d2ea97867442856cfbcf3265a53347c463597f5d0353.jpg)  
Fig. 3. Flow chart of the proposed model.

and transparently.

2.2.1.1. Dat Parsing. The data collected and gathered from the input bib file is considered to provide visualizations to the involved stakeholders in the web application. The bibtexParser library is utilized to parse the data collected through a bib fil. This process involves customizing the parser to met specific requirements based on the uploaded bib file. The resulting output is a JSON file that includes all the data from the bib fileand the total number of records. Furthermore, the data is cleaned during the bib to JSON conversion, with multi-valued attributes partitioned correctly in the JsoON file.Iti a crucial tep in generating the desired visual. zations and highlights the flexibilit of the bibtexParser library to offer tailored solutions to meet specific research needs. The data collection and parsing by uploading the bib file is performed farly and validly by giving equal privilegeto all the stakeholders and also for enhanced student writing assessment.

Algorithm 2. Data Processing.

<html><body><table><tr><td colspan="2">Require: Document File with json Extension</td></tr><tr><td colspan="2">Ensure: Information about research papers attributes (i.e., year, author)</td></tr><tr><td>1: function DATAPROCESSING(json_data)</td><td></td></tr><tr><td>2:</td><td>unique_authors  remove_duplicate_authors(json_data[&quot;authors&quot;])</td></tr><tr><td>3:</td><td>title_without_stopwords  remove_stopwords(json_data[&#x27;title&quot;])</td></tr><tr><td>4:</td><td>title_words  create_dictionary(title_without_stopwords)</td></tr><tr><td>5:</td><td>author_dict  create_dictionary(unique_authors)</td></tr><tr><td>6:</td><td>entry_type_dict  create_dictionary(json_data[&quot;entryType&quot;])</td></tr><tr><td>7:</td><td>year_dict  create_dictionary(json_data[&quot;year&#x27;])</td></tr><tr><td>8:</td><td>author_citation_count  check_author_citation(json_data, &quot;Author Name&quot;)</td></tr><tr><td>9:</td><td>recent_papers_ratio  calculate_recent_papers_ratio(json_data, 5)</td></tr><tr><td>10:</td><td>processed_data  {</td></tr><tr><td colspan="2">11: &quot;title_words&quot;: title_words, &quot;authors&quot;: author_dict, &quot;entry_types&quot;: entry_type_dict, &quot;years&quot;: year_dict, &quot;au-</td></tr><tr><td></td><td>thor_citation&#x27;: author_citation_count, &quot;recent_papers_ratio&quot;: recent_papers_ratio</td></tr><tr><td>12: }</td><td></td></tr><tr><td>13:</td><td>Output: processed_data</td></tr><tr><td>14: end function</td><td></td></tr></table></body></html>

# 2.2.2. Data Processing

Algorithm 2 represents the data processing for finding useful informatio from data for ifferent attribute. The datacollected and parsed is considered for further processing based on various aspects which is explained in the subsequent section.

2.2.2.1. Data Introduction. The application covers several record attributes including entry type, title, year, and author name, to generate visualizations for research papers (Page et al., 2021. Stakeholders can enter these details to visualize the analysis of their research papers moderately by adhering to the data privacy regulations, preventing SS atacks and adopting encrypted communication protocols to safeguard the file transfer between stakeholders and the filing system. Now, we discuss various aspects of analyzing the research papers by facilitating fair privilege to all the stakeholders.

2.2.2.2. Research Paper Enty tpe. The enry type of a research paper represents a cholarly publication that presents original research findings or analysis within a specific field f study. The choice of enry type for a reearch paper affects how the reference is formatted and the spcific atriutes requird for that ry typ. For example, an articlenry type requires the author's name, titef the article, journal name, page numbers, and year of publication. On the other hand, a book entry type requires the author's name, editor's name, title of the book, publisher's name, edition number, and year of publication. Choosing the correct entry type and including allthe required attributes is crucial to ensure accuracy and consistency in citation formatting.

Moreover, different publication venues or journals may have specific guidelines regarding the entry types. Therefore, following these guidelines and choosing the entry type that best fits the cited source is essential. For instance, some journals may use the in. proceedings ery type for citing conference proceedings, while others may prefer the proceedings entry type. Additionall, specific entry types for citing technical reports and datasets should be used whe citing these sources. For example, the entry-type tech report is appropriat for technical reports, and the ery-type dataset i used for datasets. sing the proper entry type, the ctation i more likely to meet the required standards of the reviewing agency and ensure that the research is accurately and appropriately referenced.

2.2.2.3. Reearch Paper Title. The tle f reearch paper serve s an essential source f information for reviewer to quickly identify the main focus and purpose of the paper. It alows authors to concisely summarize the key aspects of their research, including the research question, hypothesis, methodology, and critical findings. Reviewers can use this information to determine whether the paper aligns wit the journal or conferences scope and objecties and ases its potential conribution to the field In adition to providing an overview of the reearch, the title can also help o identify essential keywords associated with the rearch topic. These keywords can then be used to search for related litrature and evaluate the iterature review's quality and relevance. Reviewers can also use the keywords to identify potential gaps in the literature and assess the research's originality and significance.

2.2.2.4. Research paper published yer. The temporal dimension of research, specifically the year f publication, i crucial in assesing paper quality. The year attribute i utilized to determine the recency of the references employed, and it is highly recommended to incorporate rcent references. The year of publication provides valuable insights into the current state of the reearch field. If most of the referenced papers are over 3-4 years old, citing them is not advisable as it may indicate a failure to conduct a comprehensive search for current and relevant literature. Citing recent publications is imperative since technology and research fields are continuously evolving, and research in a given field could have made substantial progressi the last few years. Therefore, authors must cit recent publications to ensure their work is up-to-date and relevant. The use of outdated rferences can lead to complete or accurate findings. Additionall, the year of publication is beneficial in identifying trends and changes in a given field over time, which can be advan. tageous when conducting literature reviews and identifying research gaps.

2.2.2.5. Research Paper Authors. In academic research, the author attribute is utilized to evaluate the frequency of an author's papers being referenced and to identify case f elf-citation, which can suggest potential bias. Self-ittion is the act of an author citing their work in their research paper. While it can be used strategically to promote an author's previous work, excessive self-citation can indicat poor rr practice and  lack f inalit Hosra, 2021; Janssens, 2021 rfre, i is ccioalae elf-itation with external rferences to provide readers with a comprehensive understanding of the research field. Furthermore, by analyzing the author lists of the referced papers, rearchers can identify which authors frequently collaborate, allowing for the identification of potential research partners or a better understanding of the dynamics of the research community.

![](img/d52bf868d20054e2d506a624679b67a62c6021ec9ad9eba18484414f9b920327.jpg)  
Fig. 4. Data validation of the proposed model.

After datais pre-procesed based on various aforementioned aspects including research paper entry type, te, published year, and authors, we have performed the data validation to alert about the missing or incorrect reference entries to the users or stakeholders engaged in the web application. Fig.4 highlights the data validation of the proposed model in which when we upload the input BibTeX fil, it valdates the fie y checkin missing or incorret enries such as year, tite, athor, enty type, ., hich arts uers to upload the updated file for bettr analysis of the reference papers. Moreover, the author attribute aids in identifying the frequency of an author's papers being cited, providing valuable insights into their contributions to the research field. These considerations, along with other factors outlined in the Prisma checkist can help thoroughly asses the quality and validity of a research paper. The entry type, title, year, and authorattributes are crucial elements of the Prisma checklist when assing the quality of a research paper. These attributes provide valuable information on the research field and asst in evaluating the quality of the literature review. For example, an appropriate and descriptive tite, up-to-date references, and a balanced citation analysis indicate a high-quality research paper. Therefore, authors should take particular care to consider and address these atributes when writing and reviewing their research papers. By doing so, authors can enhance their work's credibility and contribute to advancing their research field.

# 2.2.3. Data representation

Fig. 5. This section discusses the data analysis in various visualizations such as bar graphs, scatter plots, bubble charts, and doughnut charts. Furthermore Fig. 6 shows the criteria for selecting the review papers considering the ratio of recent five-year papers, past-year papers and ther count corresponding to varous results, i., acept, partilly accept, or weak consideration. The criteria for analysis of review papers helps stakeholders to get the relevant results in their analysis.

2.2.3.1. Data Analysis. After getting insights into the data processing for analyzing therference papers in the aforementioned section considering research paper entry type, title, published year, and authors which i further analyzed using various visualizations. In that direction, the proposed web application analyses the obtained data afer collcting and converting bibliographic data into JSON format. This involves pasing the JsON file through appropriate functions to analyze its attributes. One essential attribute that undergoes analysis i the title of the research papers. The web alication leverages the natural language tolkit (Nk) library to ensure meaningful analysis. By utilizing the NLTK library, the web application can remove stop words from research paper tites. Stop words are common words that typically do not cary sigificant meaning in text analysis. By eliminating stop words from the tles, the analysis can focus on the more meaningful words essential for deriving insights and conducting further analysis. This step demonstrates the application's use of the NLTK library to preproces and enhance the quality of the research paper tites, ensuring that subsequent analyses are based on meaningful and relevant information.

![](img/075970cb538adef12f4d6616f1c0b420091a30080133d88b2e66cbd6e1549cde.jpg)  
Fig. 5. Flow diagram of suggestion module.

This approach enhances the accuracy and security of the analysis by eliminating frequent words that do not add significant value (Singh et al., 2021. Moreover, the web alication enables users to specify certain keywords for analyzing the frequency of a specific term or phrase in research papers. Users can upload a separate text filecontaining the required keywords and the bib filefor the analysis. The application analyzes the frequency of the provided keywords in the bib file and produces appropriate visualizations, which aids researchers infocusing on particular topics or keywords of interest. The application generates visual, such as bar graphs, scatter plots, bubble graphs, and doughnut charts, to visualize the data and provide a meaningful and understandable analysis representatin  is also useul for student writing asessments by uploading their text and bib files for analysis of rearch papers with the help of keywords. The entire data analys is achieved by ensuring transparency and fainessin the system by handling XS attacks and utilizing encryption communication protocols.

Algorithm 3. Data Representation.

<html><body><table><tr><td>Require: Information based on processed JSON data Ensure: Visual representation of data</td></tr><tr><td>1: function DATAREPRESENTATION</td></tr><tr><td>2: attributes  {&quot;years&quot;, &quot;authors&quot;, &quot;entry_types&quot;, &quot;title_words&quot;}</td></tr><tr><td>3: visuals  {&quot;scatter_plot&quot;, &quot;bar_chart&quot;, &quot;bubble_chart&quot;, &quot;donut_chart&quot;}</td></tr><tr><td>4: for each attribute a in attributes do</td></tr><tr><td>5: for each visual v in visuals do</td></tr><tr><td>6: if is_suitable_attribute_for_visual(a, v) then</td></tr><tr><td>7: create_visual(a)</td></tr><tr><td>8: display_data_representation(</td></tr><tr><td>9: end if</td></tr><tr><td>10: end for</td></tr><tr><td>11: end for</td></tr><tr><td></td></tr><tr><td>12: end function</td></tr></table></body></html>

Algorithm 3 works behind how the whole information is represented in different Graphs & visual format.

2.2.3.2. Bar Graph. In the web application, a bar graph counts the occurrences o frequencies of keywords and published papers in a particular year. This graph provides insights into how much research relies on past published documents i the research domain. The bar graph helps visualize the data distribution clearly and easily. ddtionall, this we application uses bar graphs to visualize almost all reseach paper atrbutes. For example, it includes the frequency of authors being cited, the number of authors per paper, and the number of references per paper. The web appication provides a comprehensive and intuitive way to visualize the research data using bar graphs.

2.2.3.3. Scatter Plot. A scatter plot is a graph that visualizes the relationship between two quantitative variables. In the web application contex, scatter plots help show the relationship betwen rearch paper ttributes and ther relate frequency. It llows the user to identify any pattens or trends in the data. The scattr plot is handy when comparing two characteristcs against each other, as it provides a quick visual asessment of the relationship between the two variables. The scatter plot can identify the highest and lowest frequency values and any outliers in the data. In the web application, scatter plots visualize the frequency of research papers concerning year changes, providing insights into the evolution of research in a particular field over time.

2.2.3.4. Bubble Chart. The application includes a bubble chart representing each entry type's weightage in the research paper ref. erences. The size f the bubbles in the chart is proportional to the number of ocurrences f each entry type. It llows uersto visualize the most common entry types in the research papers easily. The bubble chart provides insights into the kinds of sources that are most frequently cited in rearch papers. I can help rerchers to understand the rarch lanscape beter and idenify the most nluential sources in ther field. Using a bubble chart provides convenient user experience, allowing users to quickly compare each entry type's relative importance based on the bubbles' size. This visualization can be beneficial when dealing with many references and entry types.

![](img/79e3f3e5894aefc1eefbc0b92b8a59be51a828248845d14b03b6a23e5a460ef6.jpg)  
Fig. 6. Criteria for suggestions or review the paper.

2.2.3.5. Donut Chart. The donut chart used in the web application is an effectivetool for visualizing data distribution. It provides a more comprehensive view of the data than traditional pie charts. The donut chart is used in this application to represent the distr. bution of references based on year and keyword.

# 2.3. Recommendation for paper acceptance

This web application feature is designed to provide recommendations on adding more references to a research paper. The eval. uation proces involves analyzing thee parametersto increase the accuracy of the rsults by adding more parameters in future ver. sions. The current parameters used for evaluation are the number of research papers, the proportion of recent year papers, and the proportion of past year papers. Fig. 5 and Fig. 6illustrat the flow diagram of the ugested functionality of the system. These diagrams show the step-by-step process of the application to evaluate the research paper and provide suggestions based on the three parameters mentioned earlier. By providing a visual representation of the proces, the flow diagrams enable esearchers to understand better the system's inner workings and how it arrives at its recommendations.

# 2.3.1. Number of papers

The web application utilizes the number of papers as a parameter toassess the probability of paper acceptance. A research or term paper demonstrating in-depth knowledge is considered high quality, necesstating a substantial number of references to acquire and apply such knowledge. The web appication evaluates this parameter by determining whether the reference count surpasses 30. If the number of refernces is below 30, it generates suitablerecommedations to augment th number f papers, incrsing the likelihoodof the paper's acceptance.

# 2.3.2. Proportion of recent year papers

Assessing the ratio of recently published papers to the total number of papers is a valuable technique for evaluating whether the references used in the reearch paper ae based on current information. For example, the number of recently published papers could be increased. In that case, it may indicate that the research has yet to be conducted using the latest data and information, which can negatively impact the paper's assessment by reviewers.

# 2.3.3. Proportion of past year papers

To ensure that the references used in the research follow the standards of the chosen topic, i is essential to chec the proportion of past year papers concening all papers. f there are no old papers and ll the references are recent, the rearch paper information may

need to follow the standard practice of the domain. It checks the proportion of past year papers and provides appropriate suggestions for unmet criteria. I helps to maintain the quality and standards of the research being conducted. Fig. 7 depicts the recommendation matrix generated by the web application.

# 2.4. Prisma flow diagram

The Prisma flow diagram depicts the flow of information through the different phases of a systematic review. The web application facilitae the generation of Prisma flow diagram based on input from users or stakeholders such as researchers, students, reviewers, funding agencies, and publishers. The application takes various entries, including records identified through database searches or manual sources, records afer duplicate removal, excluded records, and full-text artices that have en excluded. Utilizing this nput, the application generates a Prisma flow diagram, visually representing the flow of information throughout the systematic review process which helps users tovisualize the data and use the relevant papers ccordingly. Fig. 8 deicts the Prisma flow diagram interace generated by the web application. Users or stakeholders can use or acces this interface for analyzing the reviewed research papers with the help of a bib file based on various attributes such as research paper title, year, author, and entry type. Moreover, it provides equal opportunity to student to asess their conducted work. So there is no partialit between stakeholders whil assessing their research papers and can utilize it properl for their rference. However, the web application is protected against  attacks and data breaches while analysis is performed for stakeholders. The security can further be improved using various advanced encryption al. gorithms against various malicious attacks.

# 3. Results and discussion

# 3.1. Motive and goal

The primary objective of the web application is to provide users with a comprehensive analysis of the references included in a research paper, enabling them to evaluate the likelihood of the paper'sacceptance along with the student writing asssment with the help of the we application. Thefore, this application is particularl advantageous for lr oranizations that frequenly reiew and analyze research papers and for individuals composing research papers or searching for relevant content related to their studies more efficiently without spending significant time searching various online resources. To ensure acessibility to users from various backgrounds, the web application's user interface is deliberately designed to be user-friendly and straightforward, catering to individuals without extensive T knowledge. Fig. 9 ilustrates the input intrface of theapplication, where users can upload  Bib file. The intuitive design of the interfce enables researchers to navigate the applicatio effortlesly and swiftly generate the desired visualizations.

![](img/b2da7b53931a631315e168be767e1c2831d0385eb6d94afbfe2c49586f3e2cb1.jpg)  
Fig. 7. Recommendation Matrix Interface.

![](img/c574f851b0a69dd655bec7d7815b2c4c5edfa7733f70a049cc85e757ed5694cf.jpg)  
Fig. 8. Prisma flow Diagram Interface.

![](img/d9910d0daa6f5f9de2de2091b9442960cc8a3dd2af2c6a3416c2a43612c9a875.jpg)  
Fig. 9. Home Page Interface.

Figure 10 depicts the visuals generated through the appication. The visual representation of data aids researchers in identifying patterns and trends that may not be immediately evident from a text-based analysis. As a result, visualizations make it easier for researchers to discern important insights and beter understand their reearch findings. It enhances the quality of research analysis and makes the research process more efficient.

# 3.2.  Quantitative results

Prisma Flow Diagram: Fig. 11 shows the Prisma flow diagram, a pivotal visual component meticulously delineates the methodo logical trajectory followed for study selection and inclusion. In adherenceto Prisma guidelines, systematic review commenced with the identification phase, sourcing an initial pool of articles from diverse databases, suplemented by manual searches and reference mining. Post-deduplication studies underwent rigorous titl and astract creening, strategicall applying predefined inclusion and exclusion criteria. This stringent proces led to a subset of articles undergoing comprehensive full-text ssessments, ensuring alignment with the research objectives and methodological rigour. Ultimately, the inclusion phase culminated in integrating the most pertinent and methodologicall robust studies for quantitative analysis. The Prisma flow diagram serves as a visual testament to the meticulous selection process, underscoring the study's commitment t transparency, reproducibility, and the pursuit of high. quality evidence in the pursuit of robust findings for all the stakeholders in the web aplication. The students can utilize the web application to analyze their writing skills overall improve the student writing assessment.   
Frequency of reference paper concerning year in Fig. 12 and Fig. 13] depicts the chart that holds paramount significance within scholarly research, functioning as a temporal analysis tool for tracking citation trends. This visual representation meticulously delineates the distribution of cited literature over distinct time intervals, providing a quantitatie asessment of scholarly inluence and temporal relevance. This chart elucidates the research's position on prior contributions by contextualizing the current study within the continum of scholarly discourse across ifferent epochs. The chart becomes integral in comprehending the temporal dynamics and scholarly progression within a specific domain, enriching the contextual understanding and depth of the ongoing investigation.   
. The distribution of papers among the various entry categories in the analysis i visually represented in Fig. 14 and Fig. 15. Within this framework, an entry type designates how a cited work, such as research papers, books, article, or other intellectual contri. butions, is categorized. These graphs ilustrate the significance and impact of each sort of entry in the broad context of paper research which helps in student writing asessment and provides a secure platform for other stakeholders to analyze their work. Looking more closely at the charts, one can see how much weight is given to each sort of item, which gives important information about how common and well-known certain scholarly publications are. The graphical depiction provides a more nuanced picture of the composition of our collection f resarch papers by illuminating th ariet of contributions that fall under iferent categories, such as books, articles, research papers, or other miscellaneous scholarly literature. These numbers, which show the proportionate

![](img/24c11bcedfb84ab28a57441828b38726df1e7ea8850483a41027b0097b6cbbcc.jpg)  
Fig. 10. Visual Representation of information.

![](img/334f35699aed677b0194e4856bb9f2bc4f68ac44449601954d6c4574105ed4cf.jpg)  
Fig. 11. Prisma Flow Diagram.

# Reference Papers with respect to years

![](img/2d924a17f1ed347a0a34b83072be8842725270269eba8661d4c4d204784bf816.jpg)  
Fig. 12. Frequency of Reference Paper concerning year.

![](img/7c1b9950cf08c42107c21d26bc366e288ae6f446e3a9b58426bc0c096c37dca6.jpg)  
Year wise number of research papers   
Fig. 13. Frequency of Reference Paper concerning year.

representation of each entry category, essentially emphasize the importance of research papers. This analytical method comprehensively evaluates the overallimpact of research articles within the study's scope by determining the prominence and influence of various types of scholarly literature.   
A graphical llustration of the frequency of reearch publications linked to particular authors in the cited references can be found in Fig. 16. This graphical analys is a valuable tol for identfying elf-citations in published papers and for identifying writers whose works are frequently referenced. Through the analysis of these charts, scholars can identify trends in self-citation, providing valuable perspectives on situations in which authors reference their previous work in later works. Furthermore, the numbers help identify prominent writers, offering a useful resource for evaluating the significance and effect of partcular studies in the larger scholarly community.   
A graphic depiction of the important keywords and the corrsponding statistical frequencies in the proposed study article is presented in Fig. 17. This graphical analysis proves beneficial for researchers or student writing asessment in evaluating the alignment of the study with the defined context through the identified keywords. By providing a thorough summary of word distribution, the figure facilitates the assessment of language accuracy and the use f particular terminology to highlight the overall emphasis of the research. This analysis becomes a tactical too for improving language, eliminating unnecessary words, increasing the study's specificity, and ensuring the information is coherent. Researchers can use this figure to evaluate the significance of individual keywords and to optimize language usage, which helps to produce a more acurate and contextually relevant representation of the research.   
A graphic depiction of the journal name and corresponding statistical frequency is presented in Fig. 18. This depiction of journal names provides students and researchers with valuable insights into the alignment of the study with relevant literature and scholarly discourse. By visually representing the frequency of journal names, students and researchers can asess the prominence of specific publications in the field and ensure that their study engages with pertinent sources for improving their writig asessment. By evaluating the significance of individual journal names and their frequency, researchers can optimize their manuscripts to better reflect the scholarly context and contribute meaningfully to the ongoing discourse in the field. Also, it helps in improving the student writing assessment by analyzing the research papers based on the journals.

# 3.3.  Qualitative results

The alication is designed with an intuitive, user-friendly interface that does not require any technical expertise. I rovides clear instructions and visual cues with allnecessary functions esily accessible. The system also provides feedback and error messages to guide the user through the analysis process. . The application includes proper validation checks to prevent misleading results from being generated.

# 3.4. Outcomes

The web application efficiently analyzes research papers, reducing the manual effort required to find relevant papers for a study. The web application automates many tasks, reing human resources and increasing eficiency. The web application is also able to generate a Prisma flow Diagram. The Prisma flow diagram is an important and valuabl tool for conducting and reporting systematic reviews. The flow diagram provides astandardizd and transparent method of identfying, screening, and selecting relevant studie for inclusion in a systematic review, which ensures rigour, reproducibility, and transparency. The Prisma flow diagram consists of boxes and arrows representing the stes in a systematic review, from intial database searches to final study selction. In adition, the Flow

![](img/358132a2c77a4b97f5c7a61a341d16c693b51c14ca12a513713daa26316cb6aa.jpg)  
Reference Papers with respect to EntryType

# Reference Papers with respect to EntryType

![](img/b2e06773e51308ca9923dd5a106893bfc516432ab4cbc37bb75a165458073b8c.jpg)  
Fig. 14. Frequency of Reference Paper concerning EntryType.   
Fig. 15. Frequency of Reference Paper concerning EntryType.

Diagram includes the number of studies identified, screened, and included at each stage and the reasons for exclusion. Using the Prisma flow diagram in arearch paper can provide transparency and clarity in your reporting of the ystematic review proces. I also makes it easier for readers to understand the selection and inclusion process and evaluate your review's rigor. The stakeholders or users can acces th web application for rigor analysis of their research work based on various arbutes such as research paper entry type, research paper tite, published year, and authors. These atributes ensure that only relevant studies are selected which can be quite useful for stakeholders or user for gting deired reults. Thus, rigorous analysis of reearch papers considers al the osible aspects to get the releant reuls. his applicatio is handy for students, pulishrs, rerchers, rearch groups, and lar organzations that regularly review research papers as part of their work. Automating many tedious and time-consuming tasks involved in research paper analysis can significantly speed up the reviewing process and enable researchers to focus more on the critical aspects of their work. Moreover, stdent writing aessment i one f the critil ascts tha i handed in which studts can utilize the we application and access it for analyzing their conducted work.

# 3.5. Security aspect of the proposed web application

The tol analyses references and produces recommendations using transparent algorithms. Ensuring that the processes and criteria behind the recommendations are transparent and easily understood by users is ensured by placing a high priority on these aspects

![](img/d116bd23138d3372470e866518c65b00e71803af78ec348e1942670e03555fee.jpg)

Reference Papers with respect to keywords

![](img/46dcaf159520f37a27e66bb86ada18f7963d0a507780a4058d899788d760b83e.jpg)  
Fig. 16. Frequency of Reference Paper concerning Author.   
Fig. 17. Frequency of Reference Paper concerning Keywords

. The too places a high priority on maintaining user data privacy and confidentiality. Information is protected against potential breaches and misuse through strict adherence to data privacy regulations and guidelines.   
The tool protects user inputs from malicious script injections by implementing strong input validation and sanitization procedures. To stop XSS attacks, validate and sanitise lluser-provided data, such as form fields, URL parameters, and file uploads.   
. The tool uses encrypted communication protocols, like HTTPs, to ensure safe filetransfers between the user's device and the remote filing system.To prevent sensitive data from being intercepted or altered while in transit, encrypt files when uploading and downloading.

![](img/60f8ed0d72377185929232a056f968c5687ee79657520c71044dcae4c4b01472.jpg)  
Fig. 18. Frequency of Reference Paper concerning journals.

# 3.6. Limitations

It is esential to acknowledge that, similar to any application, the current version of the Web Application has certain limitations..

It necesstates a BibTex fil for analysis, which may not always be readily available to the user. This constraint could potentily restrict the application's use and adoption among a broader user base.   
It is crucial to recognize that the scope of research paper analysisis typically confined to the data contained within that research paper. As a result, the analysis results may be more inclined toward that paper's specific findings and conclusions.   
. While accessing the web application, user or sakeholders have the privilege to analyze their conducted research study. However, there can be some unfair means to the analysis of students' writing assessed by the faculty or researchers' work assessed by the external reviewers that need to be tackled using advanced encryption and cryptography algorithms. Web applications work as a common platform for all stakeholders which is protected against xss atacks, and data breaches using various data privacy regulations and encrypted communication protocols.   
Features and visuals are limited at this point, so the requirements and expectations of the user might not be satisfied.   
The web application tackles some of the security aspects while analyzing the research papers, but i can be further improved against various malicious atacks such as denial-of-service (Dos), distributed denial-of-service (DDos), and cross-ste request forgery attacks by implementing various cryptography, authentication, fairness algorithms using encryption techniques.

espite the aplicaion imitations, it til prides aluable rource for reeachrs, stdents, ad acadms seeking to ealuate the quality of research papers based on specific atributes by facilitating equitable and fair outcomes for all stakeholders, especially students It isuseful for students writing academic writing assessments by considering all the possible attributes for analyzing the research papers. As a result it represents a significant advancement toward enhancing the precision of research quality assessment, which is fundmental to the progression of scientific knowledge. spciall, it has considered various secrit aspects by incorporating xss, encrypted communication protocols, and data privacy regulations for providing student writing asessments for students which further is utilized by the research supervisors for analyzing the student's research work. Moreover, other stakeholders can directly access the web application for analyze their conducted study using reference papers.

# 3.7. Future Directions

Moving forward, the primary emphasis willbe on augmenting the existing tol with additional analysis tools and features, bolstering support for alternative file formats, and mitigating constraints via machine learning methodologies..

The application's functionality can be enhanced by integrating natural language processing techniques, allowing for the direct analysis of PDF files.   
Bibliographic data about authors can be confusing because many authors share the same name or because different names are listed for the same author. To address the limitations associated with author name disambiguation, future iterations of the application may incorporate a feature capable of identifying and distinguishing between authors. One viable solution involves leveraging ML techniquesto automatically categorize authors based on their publication history, reearch interests, and institutional affliations. The application can analyse massve amounts of bibliographic data to find trends and similarities among authors by using machine learning algorithms. Algorithms for clustering, like K-means or hierarchical clustering, can be used to group writers with similar research interests or publication profiles. These algorithms can consider several characteristics, including publication venues, coauthorship relationships, citation patterns, and keywords found in publication titles or abstracts. Furthermore, textual information from bibliographic data can be extracted and analysed using natural language processing (NLP) techniques. From unstructured text, named entit recognition (NER) can assist in identifying author names, affliations, and other pertinent entitie. Authors can then be categorised according to their research topic or areas of expertise using text classfication algorithms like support vector machines (SVM) or deep learning models like recurrent neural networks (RNNs).   
To address the ssue of stop word limitations, users may be given the option to customize the list of stop words or use a more specialized list talored to their research field. Currently, the alication employs a standard set of stop words, which may need to be revised for particular research areas. In addition, to improve the accuracy of keyword analysis, additional stop words may be incorporated into future application versions.   
To enhance the functionalit of the application, customization options may be implemented to llow users to create graphs talored to their individual needs. For example, users may require customized graphs based on their research project requirements or personal preferences. Future iterations of the application could introduce a graph customization feature that permits users to modify the style, size, color, and other attributes of the graphs generated by the application.

# 4. Conclusion

In the paper, a web application is proposed to analyze research papers, generating Prisma flow diagrams based on various attributes like title, author, and entry type for various stakeholders involving students, research supervisor, publisher, etc. Moreover, student writing assessment has been improved to make it more equitable and fair for giving privileges to students for assessing their work before submitting it to research supervisors and publishers. The application's Prisma analysis model involves data gathering, processing, and representation, along with recommendations for paper acceptance. Furthermore, quantitative and qualitatie results of the proposed web application is evaluated with the help of Prisma Flow Diagram for analyzing research papers with various aspects such as analyzing references of research papers concerning year, entry type, authors, keywords, and journals.

However, challenges such as author name disambiguation, lack of fll-text data, and limited keyword analysis accuracy need addressing for improved functionality. To enhance the application's efectivenes, security measures such as cryptography should be implemented to protect user data and ensure analytical integrity. Additionally, integrating advanced ML and NLP techniques can augment the application'scapabilities, providing more accurate recommendations and deper insights into research papers with high transparency, equity, security, and confidentiality for better operationalization of web applications. Moreover, we willimprove the security aspect of the proposed web application by ensuring that none of the stakeholders can be disadvantageous to any unfair means by implementing encryption and cryptography algorithms. Future iterations should focus on refining these aspects to create a more robust and adaptable tool for researchers and academics. The proposed web application presents a valuable tool for research paper analysis, though several shortcomings require attention. By addressing these issues and incorporating security measures while leveraging ML and NLP advancements, the application can evolve into a more rliable and eficient platorm, empowering users to analyze and evaluate research papers with greater precision and insight.

# Data availability

No data was used for the research described in the article.

# References

Alman, G., Sira , He, ., Moher, D., & Schulz,  (208. qatr: rerting gudi for hlh rrch. The Lcet, 371(919), 1149-1150.   
E. Aromataris and A. Pearson, The Systematic Review: An Overview Synthesizing research evidence to inform nursing practice, 2014.   
Brooke, B. ., Scat,  A & Pwk M. (2021)e rrig i for mea-lyf tin sd. J gry, 156(8, 787-78.   
Br    r         l.010 advancing guideline development, reporting and evaluation in health care. Cmaj, 182(18), E839-E842.   
Clarke,  hr, , her,  015. The tent fr ring tmatic reis a meanaly.h Mt  Ring 1,2.   
Erikse,   de018)  f t io, io   t     it a systematic review. Journal of the Medical Library Association: JMLA, 106(4), 420.   
Hs ,,  n ,r, J    12  r  a  of project. Cochrane Methods, 2(3).   
V.d.B.P.Hoekstra, R. (2021). The Impact of self-Citation on the Number of citations: a case Study of four fields in Economics, 2, 15.   
Iister,  a      to J     r,   J   05 - e systematic review of recorded clinical cases. Medical Journal of Australia, 182(8), 407-411.   
W.Lans,  2021) Th onh en elf-ion d ch   e d  t of h scis, 3 30   
ng  a   ,1 l i ti  tc evaluation. Clinical Psychology Review, 31(7), 1110-1116. quorom statement. The Lancet, 354(9193), 1896-1900.   
Page,  J ser,  ico . 018 rti c  i pr 300 rors a tc s, 1) 19   
Pag  J, c, . t     r  f  ,    l. 201) prisma 2020 statement: an updated guideline for reporting systematic reviews. International Jounal of Surgery, 88(105906).   
S.E.J. Richard, A. Guzzo, and R.A. Katze, META-ANALYSIS.2024.   
Schiavo, J. H. (2019). Prospero n international reiser f ysteatic review protocols. Medcl Reeence rices Quarterl, 38(2), 171-180.   
ric   , r  ,  0 c reviews (prisma-scr): checklist and explanation. Annals of Internal Medicine, 169(7), 467-473.   
\*M.J. Page,  hmseer2 ad. ic04   a  a parin sd f ficit  tivit th sh tls o qualitatie systematic reviewsg, 2014.   
S D., B K., Singh R., A Comprehensive Study of Stopwords and Their Removal Techniques in Text Mining., 2021.

Smita n  a P c  0 o e rid r   io r  n 0hm    t id f  li rom HARUAt  01.    thef  ic a P e d  i me  er , ACM and   is   od i  a    STE prestigious membership of the IEEE (SMIEEE) and is a distinguished member of the Indian Society for Technical Education (LMISTE.

Parita Oza is working a n Asstant Poeso i omputer cice ad gnerin men ice une 208. Prof  hs more than 17 yr f teaching exprie h    omti rhl  ig ay ah  tion an ction o .  t  the. h   th   imagg fro Pand yl g sit n 2023.   ad g g d  mn h ce a d a t g hs the Programme commitees and session chair for international conferences and as a reviewer for indexed international journals.

R  iPh  e   tt ived e achr  w s str of   the t h r, n in 2018  201,tiel. She  or c sme publii         ias  o-cted j     E h n   i ih Laboratory (www.sudeeptanwar.in).

Sudeep  er s r  a h thmr cnd t tit  y, irma net,   t   t t i Th in 200 hty, aeh in009 rinrt, hi, Inad Ph i 016 with Such as EE TRANSACTIONS ON NETWORK SCIECE AND ENGINEERING, EE TRANSACTIONS ON VEHICULAR TECHNOLOGY, IEE TRANSACTIONS ON INDUSTRIAL IRTICS IE WIELESCONIIOS I NORKS, ICC GLOBECOM, and IFOCOM He id the e id  bockchan th     07.    50. ei     s .   s id bl    te 2020. i e     t   in Sot.    1 08 019, 1. er any inet  thc -200 20, 01 th  20 2  20 the edrial b of omter ntion tio Jol of ctiost nd ty and Pricy. Heis ao g the  Rech Laboratory, where group members are working on the latest cutting-edge technologies.

Vis Jets  i  c    t d,  s h  chi Learning, Blockchain, and Cryptocurrency.

Jati s  i m cd g  t, d  h  chi Learning, security, and Cryptocurrency.

pam Medil m     / h     nd jt