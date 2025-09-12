# Building a customised Google-based collocation collector to enhance language learning

Shesen Guo and Ganzhou Zhang

Qianjiang College, Hangzhou Teacher’s College—Literature Department Office, Hangzhou Zhejiang 310012, People’s Republic of China. Email: guoshesen@126.com

A collocation is defined as an arrangement or juxtaposition of words or other elements, especially those that commonly co-occur, as rancid butter, bosom buddy or dead serious (American Heritage Dictionary of the English Language, 2004), the association between two words that are typically or frequently used together (Encarta World English Dictionary, 2006), a habitual combination of words that sounds natural (Longman Dictionary of Contemporary English, 1992). There is no doubt that such definitions are intuitively correct when we encounter co-occurrences of words in text and speech. As a component of vocabulary and language learning and as an interesting area for linguistic investigation, collocation study and building of collocation dictionary or corpus have been given considerable emphasis since Cruden identified the repeated co-occurrences of certain words such as ‘dry’ and ‘ground’ in the Bible more than 250 years ago (Cruden, 1954; Kennedy, 2000).

Clearly, collocation collection and research for language learning is based on empiricism—an approach dominated by the observation of really and naturally occurring data. Noam Chomsky (1959) specifically challenged such language enquiry by stating

We constantly read and hear new sentences of words, recognize them as sentences and understand them. It is easy to show that the new events that we accept and understand as sentences are not related to those with which we are familiar by any simple notion of formal (or semantic or statistical) similarity or identity of grammatical frame.

He was actually implying that the sequencing of words—characteristics of collocation, is infinite. According to his innatism, such infiniteness or externalised language performance is determined by language competence or internalised knowledge of language due to genetic inheritance. It is therefore not possible and not useful to enumerate all sentences, all collocations for language investigation.

However, none would agree that syntactically generated correct sentence will ensure freedom from awkwardness, inappropriateness and ambiguity. What we accept is call it a day rather than name it a day. Language learning is the result not only of surface structural and phonological imitation but also of deeper structural or semantic imitation, and practice plays a key role in this process. (Brown, 2002). Altenberg (1991)

strikingly showed that about $7 0 \%$ of the words of running text in the half-million-word London–Lund Corpus are part of recurrent word combinations. Most of combinations are two to three words in length, but some have more than five words. The evidence demonstrates that we are constantly using collocations.

Sinclair (1991) suggests that language users tend to choose words on two complementary principles, namely, open choice and idiom choice. The open choice determines what unique sentence can be generated based on grammatical rules, while idiom choice recognises word associations just as we have tendencies for physical, cognitive and social phenomenon to be associated. That is why there are some co-occurrences of words like ‘ice’ and ‘cold’, ‘cry’ and ‘tears’. In testing the word ‘blue’ associations, Cook (2000) found that the very first response to it was syntagmatic (blue sky, blue jeans ...), the second was paradigmatic (red, pink...) and the third was a klang response (new...) because it clangs with the word as a rhyme (like true and Sue). Cook (2000) emphasises that in both the first and the second, language learning students go through a regular progression called syntagmatic/paradigmatic shift—they start with the syntagmatic responses and move on to paradigmatic responses. Without reserve of basic level combinations and prototypes of words, students would not be able to build their imaginative writing with originality.

In summing up approaches to language acquisition, Lightbown and Spada (2002) propose that behaviourism should be used to guide learning of vocabulary and morpheme, that innatism be employed to explain complex grammar.

Questions arise when we consider collocation learning and teaching, and the collocation definitions previously mentioned.

1. How often does a combination have to recur to be considered ‘frequently’ or ‘typically’?   
2. How can we determine a combination ‘commonly co-occurs’?   
3. How can we know a combination is ‘habitual’?   
4. Who is the judge that rules that a collocation does ‘sound natural’?   
5. Should a sequence that occurs only once in textbooks or database but is recognised immediately and intuitively by a native speaker as a combination be taught as a collocation?

The Internet can give fast, reliable, valid and correct answers to these questions. Surprisingly huge amount of information, ubiquitous presence of computers and easy access to the Net provide a convenient platform for such investigation and verification as frequency, context and source of a combination.

Although there are a number of online dictionaries, encyclopedias, references, archives, databases and libraries for meanings of words, few of them provide a professional, systematic and dynamic description of collocations. To most ordinary language learners and teachers, large corpora for linguistic investigation are either inaccessible or unreachable because of their prohibitive prices or unreliability and complexity of connection, difficult retrieval and analysis of data from remote servers.

To a degree, internet web pages together with websites and servers distributed all over the world are the largest corpus storing different languages and variations. They adequately enable us to probe into collocations and language phenomena in terms of

1. time—static or dynamic: researchers and teachers are able to analyse collocation features either by noting the time mark or attribute of every source file or web page, or by limiting files or pages by setting time span searched at search engine websites.   
2. representativeness and balance: a variety of resources covering all human knowledge and genre in the form of hierarchical order or directories in most large search engines facilitate availability and search of all information.   
3. size: even a small search engine is now able to index millions of web pages, and the number of new servers and web pages is rapidly growing at light speed.

In database and web page search syntax, proximity and order operators are the most powerful tools for indexing collocations. Previously, Alta Vista was the most effective and efficient search engine in this respect for exactly listing requested collocations for study. It fully supported searching of numbered proximity without order (symbol ∼∼), before order $( < )$ , before order and proximity $( < \sim )$ , after order $( > )$ , and after order and proximity $( > \sim )$ . Even in its simple search mode, users were able to approximately search collocations by operation of the command NEAR. After it was bought by Yahoo in 2004, these very useful search operations were removed. The other search engines such as WebCrawler were able to search adjacent words by using the operator ADJ. According to Answers.com (2006), as of February 2006, among hundreds of Internet search engines, only Exalead still implements proximity searching. The new search engine Welhello claims to be able to implement proximity search. But neither Exalead nor Welhello worked properly and did not correctly generate the indexing pages of information and collocations by using the operator NEAR in our test.

It is possible to use Google to collect and index requested collocations. Though it only indexes the first $1 0 0 \mathrm { K b }$ of any page, information available from Google is undoubtedly the largest corpus in the world. In 2006, Google has indexed more than 25 billion web pages, and over one billion Usenet messages—in total, approximately 12 billion items. It also caches much of the content that it indexes (Wikipedia, 2006). Though it does not support the proximity operator NEAR, wild cards can be used with double quotation marks for retrieval of collocations from its large database (Figure 1). To realise automation and convenient observation, we may transfer collocations and context embedded in the innertext of hypertext mark-up language files to a list of components by using browser ActiveX, IOleCommandTarget interface, and exposed DownloadComplete function, programmatically adding simple algorithm for ascending and descending sorting of both preceding context and collocations, moving up and down, copy and saving for comparison and analysis. Such a fast, economic, efficient and pragmatic concordance tool based on Google is able to not only index discontinuous collocations like at times, at a time, at the present time, at just the right time in plain text for frequency analysis in language learning and investigation, but also to list with combinations of operators and in designated order target items like Rowling (specified number of truncations)

![](img/d0e6455697db2c8213fbe67e44b7b8e0eaf56767eb01d7e20c7ecba1d6e6bfce.jpg)  
Figure 1: A fragment of sorted list based on Google search syntax allintext and wild cards

Harry, Iran (predefined number of wild cards) nuclear and Gates (set number of asterisks) Africa for discourse analysis.

# References

Altenberg, B. (1991). Amplifier collocations in spoken English. In S. Johansson & A. Stenstrom (Eds), English computer corpora (pp. 127–147). Berlin: Mouton de Gruyter.   
American Heritage Dictionary of the English Language (2004). Boston, MA: Houghton Mifflin Company.   
Answers.com (2006). Google. Retrieved May 10, 2006, from http://www.answers.com   
Brown, H. D. (2002). Principles of language learning and teaching. Beijing: Foreign Language Teaching and Research Press.   
Chomsky, N. (1959). Review of Skinner, B.F. Verbal Behavior. Language, 35, 1, 26–58.   
Cook, V. (2000). Second language learning and language teaching. Beijing: Foreign Language Teaching and Research Press.   
Cruden, A. (1954). Cruden’s Concordance. Grand Rapids, MI: Baker Book House.   
Encarta World English Dictionary (2006). Collocation. Retrieved May 9, 2006, from http:// encarta.msn.com/   
Kennedy, G. (2000). An introduction to corpus linguistics. Beijing: Foreign Language Teaching and Research Press.   
Lightbown, P. M. & Spada, N. (2002). How languages are learned? Shanghai: Shanghai Foreign Language Education Press.   
Longman Dictionary of Contemporary English (1992). London: Longman.   
Sinclair, J. (1991). Corpus, concordance, collocation. Oxford: Oxford University Press.   
Wikipedia. (2006). Google. Retrieved on May 8, 2006, from http://en.wikipedia.org