# Logically Incorrect Arguments

Vladimı´r Svoboda1 $\cdot$ Jaroslav Peregrin1 $©$ Springer Science+Business Media Dordrecht 2015

Abstract What do we learn when we find out that an argument is logically incorrect? If logically incorrect means the same as not logically correct, which in turn means not having a valid logical form, it seems that we do not learn anything too useful—an argument which is logically incorrect can still be conclusive. Thus, it seems that it makes sense to fix a stronger interpretation of the term under which a logically incorrect argument is guaranteed to be wrong (and is such for purely logical reasons). In this paper, we show that pinpointing this stronger sense is much trickier than one would expect; but eventually we reach an explication of the notion of (strong) logical incorrectness which we find non-trivial and viable.

Keywords Argumentation $\cdot$ Logical form $\cdot$ Incorrect argument $\cdot$ Correct arguments

# 1 Are There Any Logically Incorrect Arguments?

It is a common wisdom that some arguments are logically correct. But are there any arguments that are logically incorrect? The answer seems close to trivial. Whereas the argument

(A1) If it rains,then the streets are wet It rains The streets are wet   
is logically correct, the argument

(A2) If it rains,then the streets are wet It rains The streets are not wet

is logically incorrect.

The fact that there are examples of arguments that seem to be patently logically incorrect certainly indicates that there is indeed such a category of arguments; however, identifying individual cases is nothing but the initial step towards the identification of the kind. Only if we have some well-formed criteria to be satisfied by arguments of the category can we say that we have a proper grasp on the concept of logical incorrectness.

Detecting incorrect arguments, needless to say, is an important task; and it may seem that logic contributes to it by way of demarcating correct ones—the incorrect ones thus being those which are not correct. But the situation is not so simple, for two reasons: (1) Demonstration that an argument is not correct from the viewpoint of a certain system of logic—say classical propositional calculus—does not prove that it is not correct from the viewpoint of another system—for example predicate calculus, modal logic, etc. (2) Logic conceived narrowly as the science of deductive reasoning concentrates on a specific kind of correctness (viz. correctness in virtue of logical form) 1 ; and many arguments are correct or incorrect for different reasons— thus to say that an argument is not logically correct is not to say that is it logically incorrect (in the sense of incorrect for logical reasons)—many arguments are correct for reasons that are outside the scope of logic. Therefore it seems that logical incorrectness in a strong sense becomes a problem of its own.

To be sure, there is a straightforward (and often tacitly adopted) understanding of the concept of logically incorrect argument which identifies logically incorrect arguments with those which are not logically correct. 2 However, an argument that is logically incorrect in this sense can still be correct (though not logically) and, hence, saying ‘‘Your argument is logically incorrect’’ would not put an end to a discussion concerning the correctness of the argument (though it may make such an impression).

Thus, it seems reasonable to try to pinpoint a stronger sense of the term logically incorrect, one which warrants that every logically incorrect argument is guaranteed to be wrong (and is such for logical reasons). Using such a notion, it makes sense to say ‘‘Your argument is correct, but it is not logically correct’’ whereas we cannot say ‘‘Your argument is correct, but it is logically incorrect’’.

In this article, we will survey some possible ways of explicating this stronger concept and show that those construals of the concept which seem prima facie most promising, are quite controversial or lead to dead ends. Nevertheless, we will not admit defeat and will attempt to pin down an explanation that we think is usable. And we believe that even those who will not be satisfied with our conclusion will be able to benefit from following the course of our struggle with the conceptual issues surrounding the problem.

# 2 Weak Notion of Logical Incorrectness

As we have suggested, the most straightforward answer to the question of which arguments qualify as logically incorrect is that they are exactly those that are not logically correct. Let us call this construal of logical incorrectness the weak notion of logical incorrectness. Adoption of the weak notion, however, forces us to adopt the implausible conclusion that many logically incorrect arguments are in fact correct. For example, the argument

# (A3) All dogs are mammals All dogs are animals

is not logically correct (its correctness being a matter of the meaning of the extralogical words mammal and animal), hence on the weak construal it is logically incorrect despite the fact that if anybody were to reason from its premise to its conclusion her inferential step could hardly be challenged—the inferential move is obviously correct.3

A possible response might be that, despite appearances, (A3) is not a correct argument—that it can be considered correct only on the assumption that it contains another (covert) premise, say All mammals are animals or If something is a mammal, it is an animal. (That means: it is not a correct argument as it stands, it is correct only if we construe it as a shorthand for the extended version in which the premise is overtly present.) We disagree with this view. (A3) is correct as it stands on the sole grounds that the sentences it consists of mean what they do. And it would seem that we must presuppose that the words and sentences constituting the arguments we are to assess have a fixed meaning.

True, some arguments may already be correct in virtue of the meanings of only some of the expressions they contain, independently of those of the rest. Thus, (A1)

is correct independently of the meanings of the sentences It rains and The streets are wet. This, however, does not mean that we do not need to distinguish arguments and argument forms or that arguments may consist of meaningless, or partly meaningless, sentences. An argument is always a step from a claim or claims (and hence a meaningful sentence(s)), to a claim—a meaningful sentence.4 Of course, we can speak also about correct—or, better, valid—argument forms; but this does not mean that we should call a step such as that which proceeds from All X’s are mammals to All X’s are animals an argument, it is merely an argument form.

Once we realize this, we cannot but accept that (A3) is a correct argument as it stands: once the words and sentences it consists of mean what they do in English, there is no way to contravene it. We are surely not free to tamper with meanings of expressions within arguments. If we were, it would be easy to undermine not only the correctness of (A3) but also the correctness of (A1) or any other argument—if the meaning of if… then… were not fixed, then the form of (A1) could not be considered as valid.5 Thus, we want to argue that the idea that some correct arguments should be classified not only as not logically correct (not correct for merely logical reasons), but as logically incorrect (incorrect for logical reasons) appears to be quite counterintuitive. Later in the paper we will present a further reason for dissatisfaction with the weak concept of logical incorrectness.

# 3 Correct Arguments

Before we try to pin down a concept of logical incorrectness conforming to the intuition that logical incorrectness should entail incorrectness simpliciter, let us pay attention to a more fundamental question, namely: What does it take for an argument to be logically correct? And before we do this, let us, in turn, address the still more fundamental question of what it takes for an argument to be correct (simpliciter). But at the very beginning we have to fix the concept that is at the centre of our focus—the concept of argument.

Arguments (inferences) normally consist of one or more premises followed by a conclusion. In logic, arguments are usually considered in a somewhat more general way: they are taken as ordered pairs, each of which consists of a set of statements (propositions) and a statement (proposition) where the set of premises may even be empty. Sometimes logicians study also logical features of arguments involving sentences lacking truth values like: Keep your promises! You promised to quit smoking. Hence: Quit smoking! The modern discussions about possible logical correctness of arguments of this kind were initiated by Jørgensen (1937) and proceed in contemporary deontic logic and the logic of imperatives (see for example Gabbbay et al. 2013, Vranas 2011). In these areas of logic the concept of argument has to be defined more broadly. Here, however, we will limit attention to arguments which consist exclusively of statements.6

Let us now move to the concept of correct argument. The following necessary condition of correctness appears plausible:

NecCor If an argument is correct then it is impossible that all its premises are true and at the same time its conclusion is false.

This appears to be natural and uncontroversial; but should we see the necessary connection between the truth values of the premises and the conclusion also as a sufficient condition of argument correctness? If so, then we should also endorse the following condition:

SufCor If it is impossible that all the premises of an argument are true and at the same time its conclusion is false then the argument is correct.

This condition is, however, much more controversial than the previous one. It is clear that its adoption inevitably results in a very broad concept of argument correctness. It seems, for example, natural to require that at least some of the premises of a correct argument are connected, as concerns their contents, to its conclusion. Or we might want to insist that all the premises play a non-trivial role in the argument in the sense that if we omit any of them, the argument ceases to be correct. Adoption of SufCor violates these intuitions. And not only that—it forces us to admit that arguments with premises that are inconsistent are to be automatically classified as correct.7 Similarly, arguments whose conclusion cannot be false count as correct no matter what their premises are or whether there are any. Though we might feel uneasy about such a radical extension of the common concept of correct argument, its simplicity and clarity surely is a substantial virtue. Of course these qualities will be highly appreciated especially when what we are after are methods of establishing correctness of arguments (proofs) on systematic and rigorous grounds, i.e. especially in the context of scientific reasoning. We think that the ‘technical’ concepts of argument and of correct argument just outlined provide acceptable approximations for many contexts in which we need to scrutinize argumentation (though we must be aware of the fact that they are not more than approximations). For the purpose of this article we will thus accept the cavalier notion of correct argument, not uncommon among logicians, that equates correctness with truth preservation.

As a result of these considerations, we reach the following explication of the concept of correct argument:

DefCor An argument is correct iff it is impossible that its premises are true and at the same time its conclusion is false.8

This account of correct (deductive) argument is quite commonly accepted. In the relevant literature we can find various kinds of variations on this idea. Thus Rips (1994, p. 3), says: ‘‘A deductively correct argument, roughly speaking, is one in which the conclusion is true in any state of affairs in which the premises are true’’. Copi et al. (2014, p. 24) write ‘‘A deductive argument is valid when, if its premises are true, its conclusion must be true.’’9 Walton (2006, p. 56) says that ‘‘an inference is deductively valid if and only if it is logically impossible for the premises to be true and the conclusion false’’, and Smith (2003, p. 9) writes ‘‘An inference step from given premisses to a particular conclusion is (classically) valid if and only if there is no possible situation in which the premisses would be true and the conclusion false.’’

It is clear that provided that the main point of argumentation is to establish some thesis—a conclusion, the study of argumentation cannot focus only on whether the argument in question is (deductively) correct. What matters is also the truth of the premises. Thus we should identify a specific subset of all arguments—those that are correct and at the same time have true premises. Such arguments are usually called sound. But, of course, even sound arguments need not be useful or convincing and hence serve their purpose in communication. (The argument The Earth is round hence The Earth is round is surely sound but obviously useless). Thus, for example, Hocutt (1979, p. 138) distinguishes between valid, sound, and good arguments. Good arguments not only have to be sound; they also must ‘‘carry conviction’’, i.e. they must make the person who admits the premises see that the move from them to the conclusion is warranted.

Though the definition DefCor seems quite perspicuous, some clarifications may be needed. The most apparent among them concerns the meaning of the word ‘‘impossible’’. Should we take the term as referring to the most general (though not entirely clear) concept of possibility—inconceivability? In other words, should we take the definition as claiming that an argument is correct if and only if there are no conceivable circumstances (no thinkable situations or worlds) which would make its premises true and its conclusion false? This might be too limiting if we have in mind a practical assessment of the correctness of argumentation. Consider the inferences

(A4) Socrates lived in Athens Socrates lived in Europe   
(A5) Fido is a dog Fido does not live on Mars

It is hardly contentious to assert that whoever normally reasons from the premise of any of these arguments to its conclusions proceeds correctly. Yet we can imagine situations in which the premises are true and the conclusion false—though the circumstances would presuppose a very dramatic change of the status quo. Hence, it seems reasonable to admit that the notion of impossibility invoked in DefCor need not be a too narrow kind of impossibility—the impossibility may well be a looser one.

In such cases as (A4) and (A5), unlike the case of (A3), we might be justified in seeing the arguments as not literally correct—we may see them as correct only on the background of some additional, tacit premises (Athens is in Europe, Nothing lives on Mars). However, as Quine (1960) taught us, it would be very difficult to draw a sharp dividing line between arguments that are correct merely on the basis of meaning and those that are correct on the basis of some very general facts. Moreover, if we derive the concept of argument from what we really do when we argue and reason, then we must conclude that such facts are not taken to be covert premises, but rather parts of a general framework within which the reasoning takes place. This seems to make a strong case for also accepting arguments like (A4) and (A5) as correct as they stand (though in this case, we admit, it would also be possible to regiment the concept of correctness in a different, more stringent way).

# 4 Logically Correct Arguments

The considerations concerning the logical correctness of arguments have a straightforward starting point: logically correct arguments should form a subset of correct arguments. If the contribution of the word ‘‘logically’’ to the meaning of the phrase ‘‘logically correct’’ is to be non-trivial, then, of course, logical correctness requires more than correctness simpliciter—not every correct argument deserves to be classified as logically correct. Hence, the characterization of arguments that are logically correct requires some additional specification.

A variant of DefCor strengthening the concept of impossibility in a suitable way seems then like a natural option. The first idea that may come to mind leads us to the following definition:

DefLogCor1 An argument is logically correct iff it is logically impossible that its premises are true and at the same time its conclusion is false.

This definition, however, is obviously problematic. If the term ‘‘logically’’ is supposed to mean the same in both definiendum and in definiens then the definition appears to be circular. This problem may be resolved by insisting that in the definiendum the term is used in a narrow ‘technical’ sense (as it is used in formal logic) while in the definiens it is used in a broader sense in which it means ‘‘conceptually incoherent’’ or ‘‘inconceivable’’ (which is the interpretation that we considered as the initial reading of ‘‘impossible’’ in DefCor). But on this reading DefLogCor1 clearly does not provide an acceptable delineation of the concept of logical correctness. The point then is that surely arguments like (A3) (and perhaps even arguments like (A4)) come out as logically correct which is, for the reasons that we suggested, inadequate. We might, of course, reject the broader understanding of logical impossibility and insist that the term has (or should be given) a more specific meaning. Such a project, however, is hardly worth pursuing—the concept of logical impossibility appears to be more in need of explication than that of logical correctness and reducing the latter to the former would not then seem like an achievement.

The main reason that will likely divert us from the demanding enterprise of circumscribing the concept of logical impossibility is that there seems to be a different, more feasible way of getting a grasp on the concept of a logically correct argument. The point is that a natural way of explaining the logical correctness of an argument is explaining its correctness as being in virtue of the logical vocabulary contained in it alone, which is usually further explicated as the validity of its logical form. Hence we arrive at the following criterion:

DefLogCor2 An argument is logically correct iff if it is an instance of a valid logical form.

This definition sounds prima facie plausible; but the concept of logical form is so complex that the plausibility stands and falls with the possibility of making this concept clear enough.

# 5 Logical Form

Let us first start with the question what, in general, is a form of an argument. It seems natural to say that argument forms consist of sentence forms in place of the premises and the conclusion. What is a sentence form? On first approximation, it can be seen as a sentence with some part or parts left out, or replaced by parameters—letters acting as mere placeholders.10 Thus we can say that $X$ has a son is a sentence form that is embodied or instantiated, e.g. by the sentence Hugo has $a$ son. Now we can easily see that in certain cases all arguments which instantiate a given form will be correct. Let us take the argument form

It is obvious that all arguments which instantiate this form are correct, hence we can classify the form as valid and the arguments which have this form as correct due to their form and we can call them correct due to their form or formally correct. It is obvious that by far not all arguments which instantiate a valid form are logically correct—not every possible form of a sentence (or an argument) is its logical form.

What is then a logical form of an argument? It is obvious that the logical form of an argument is determined by the logical forms of its constitutive sentences. But what is the logical form of a sentence? There is a spectrum of views stretching in between two extremes. At the one extreme, a logical form may be thought of as simply what remains of an expression if we remove its extralogical parts (replace them with parameters).11 Construed in this way, a logical form is something closely connected with a natural language (though in the majority of cases the proponents of this view do not base the logical form of a sentence directly on its surface form, but rather on a grammatical form regimented by a linguistic theory). This is not to say that it is not possible for sentences of different languages to share the same logical form; but this possibility is conditioned by the intertranslatability of the logical parts of the two languages. In addition, articulating a logical form of a natural language sentence by means of a formula of a formal language is possible only in so far as we are able to capture the logical vocabulary of the natural language by means of that of the formal one. At the other extreme, a logical form is often thought of as being something utterly independent of any factual languages, and languages of formal logic are seen as capturing it independently of any investigations of natural languages.

Our notion of logical form is closer to the former extreme than to the latter one— for us, logical forms are always something abstracted from natural languages. This is not to say that a logical form of a sentence is always just a template reached by stripping away the extralogical parts of a natural language sentence—it is not merely stripping away, but also various kinds of rearrangement, simplification, etc., that lead us from a sentence to what we proclaim to be its logical form.12 But the validity of a logical form on our construal cannot but reduce to the correctness of its instances—there is no property of ‘validity per se’ that would pertain to the forms independently of the nature of their instances.

Let us stress that it is crucially important to realize that though logically correct arguments are those that have a valid logical form, it is not the case that those that have an invalid form are logically incorrect. Often, no terminological distinction is made between what we call correctness (of arguments) and what we term validity (of forms),13 which then stimulates an essential confusion. As Massey (1981, p. 493) puts it:

Philosophers, logicians, and their students routinely do pretend to convict arguments of invalidity by producing invalid forms that the arguments instantiate. Introductory textbooks aid and abet this pernicious practice. After each installment of theory, they proffer exercises that require the student to prove certain arguments invalid. How? By translating them (as fully as possible) into the formal language at hand and then showing that the theory just imbibed declares the form of the resulting argument invalid.

It is important to keep in mind that while only correct arguments have valid forms, instances of invalid forms can well be correct.

Logical forms, as we construe them, presuppose a boundary between logical and extralogical vocabulary. Admittedly, this boundary is fuzzy. But our everyday experience with our mother tongues testifies that we are very good at drawing consequences which deserve to be classified as logical. We are capable of doing this mainly because we learned to understand and use specific kind of vocabulary that warrants the inferential (argumentation) steps.

How unwittingly we do this can be illustrated with a somewhat bizarre example: Consider the sentence ‘‘Twas brillig, and the slithy toves did gyre and gimble in the wabe’’.14 Even if we can hardly say that we understand it, we are quite ready to ‘forget’ about the unintelligible parts and admit that whatever the sentence says, it implies that ‘‘the slithy toves did gyre and gimble in the wabe’’ as well as that ‘‘the slithy toves did gyre’’. Our understanding of the word ‘‘and’’ as it occurs in the grammatical construction grounds our endorsement of the inferences which are obviously logical in their nature. This suggests that the concept of logical form is closely connected with our ability to abstract systematically from meanings of certain expressions while assessing argument correctness and concentrate only on the role of a limited vocabulary.

We take the logical vocabulary to consist of exactly those ‘topic-neutral’ expressions which license, by themselves, inferences of this very general kind. There is, to be sure, no universal key to differentiating logical terms from nonlogical ones,15 but we certainly do not think that the project of drawing a reasonable boundary between logical and non-logical vocabulary should be abandoned for this reason.16 Nevertheless, the inherent fuzziness of such a boundary makes DefLogCor2, as it stands, too elusive to provide a satisfactory grounding for explication of logical correctness for our purposes.

Another problem is that in many cases the very correctness of individual arguments may be a debatable matter. Even those who are fully competent speakers may disagree or be in a quandary over the problem of correctness of many concrete arguments (and there is no higher authority appointed to resolve such disagreements). Though we do believe that inference in natural language is far from indeterminate,17 presupposing complete determinateness may be too much. The correctness/incorrectness of natural language arguments is an objective, but often a fuzzy and indefinite matter. Thus, any theory of correctness of arguments must ‘consolidate’ the data from natural language: it must draw sharp boundaries where there are none, extrapolate, standardize and streamline. Therefore, as we put it elsewhere (Peregrin and Svoboda 2013; t.a.), the laws of logic, and the notion of correctness of argument we normally apply, is a matter of a reflective equilibrium.

Finally, there is the specific problem of uniqueness of logical form. It is clear that we can often think of more than one logical form of a given sentence. Thus consider the sentence

(S1) If Fido is a dog, then Fido is a mammal

Considering it from the viewpoint of propositional logic, we would probably think about

$$
A  B
$$

Perhaps we could also consider

and, taking into account the resources of predicate logic, also

$$
( \mathrm { S F 1 ^ { \prime \prime } } ) \quad P ( a ) \to Q ( a )
$$

Which of these forms is the right one?

An answer might stem from the observation that the three forms can be ordered according to their specificity: (SF1) is more specific than $( \mathrm { S F } 1 ^ { \prime } )$ , and $( \mathrm { S F 1 ^ { \prime \prime } } )$ is in turn more specific than (SF1). Thus, we could perhaps say that all three forms are forms of (S1), but that it is $( \mathrm { S F 1 ^ { \prime \prime } } )$ which is the ‘true’ form in that it is the most specific. However, how do we know that there is no form which would be more specific even than $( \mathrm { S F 1 ^ { \prime \prime } } ) ?$ Because we can readily ‘see’ that there is no such form in the predicate calculus? But what if there is one in a logical language that we have not conceived of yet?

Such considerations lead Massey (1975, p. 66) to the conclusion that though we can convincingly demonstrate, by logical methods, that some arguments are good, there is at present no logical method that would allow us to show that an argument is bad (invalid).

To show that an argument is valid it suffices to paraphrase it into a demonstrably valid argument form of some (extant) logical system; to show that an argument is invalid it is necessary to show that it cannot be paraphrased into a valid argument form of any logical system, actual or possible. The latter necessary condition is also sufficient if and only if the former sufficient condition is also necessary (when the reference to some logical system is understood as reference to some actual or possible system.)

Hence, we think that the problems arising from the fact that DefLogCor2 hinges on the raw, ‘unconsolidated’ data are serious.

# 6 Logically Correct Arguments Redux

Some of the problems we pointed out in the previous section are in the nature of things; they stem from the fact that if logic is to be regarded as having authority over the assessment of arguments that we formulate in natural language and use in real life, it inevitably has something of an ‘empirical dimension’—it interacts with natural languages that are empirical phenomena and hence cannot ignore their twists and turns. Thus, similarly as there cannot be any mathematical theory suited to decide which empirical phenomena a given mathematical theory applies to, we cannot have a logical theory deciding which natural language instances a given logical form has. But there are, of course, other problems that can be (and successfully are) managed by logical means—standard logical theories are suited to systematize possible logical forms and give us formal criteria of their correctness. This, we think, should be more explicitly utilized in our definition of logical correctness; we therefore suggest that it is reasonable to replace DefLogCor2 with:

DefLogCor3 An argument is logically correct iff it is an instance of an argument form that is sanctioned by logic (i.e. its conclusion is provable from its premises by means of logic, or is sanctioned by logic in another way).

This definition seems precise enough and it does not suffer from the shortcomings which affected the previous version. It is, however, also controversial. Unless we suppose that there is one and only one ‘correct’ logic, the concept of logical correctness will be relative to our choice of a background logical theory. We, however, know that the domain of logical theories is quite diverse.

In so far as it is an objective—though, as we have stressed, also a fuzzy—matter which arguments are correct in natural languages, it should, at least in principle, be possible to compare the different systems of logic as concerns their adequacy and comprehensiveness with respect to a language, say English. Thus, we might hope that we could select something as the ‘right’ or ‘best’ logical system(s). It does not in fact seem to be far-fetched to assume that at least to a certain extent such a selection already took place and our most common logical systems are those which are ‘tried and true’. Of course, it would be good to have the assumption supported by research explicitly aimed at assessing the ‘empirical adequacy’ of different logical systems, but studies of this kind are, as far as we know, in short supply.18

This is not too surprising—it is not entirely certain that such studies are worthwhile. Clearly logic’s main ambition is not to capture as faithfully as possible the inferential structure of natural language. Logic should primarily offer a suitable simplification and standardization. In many cases, for example, the austerity of a system of logic is valued more than this kind of faithfulness. Thus, we can hardly believe that mankind will ever identify anything like The Logical System whose existence is presumed by diehard logical monists. However we are inclined to admit that the idea that there is a core system (or a core body of systems) of logic that can be used as a benchmark of correctness of arguments is not an unacceptable simplification.

Even if we adopt such simplification, DefLogCor3 is still vulnerable to further criticism. For one thing, it tacitly presupposes that it is determinate which arguments are instances of which argument forms—i.e. which logical forms sentences of natural language have. This supposition may not be unacceptable, but we should be aware that the notion of correctness obtained in this way can be accepted as clear only provided that we get a firm grasp on the relation of instantiation.

Another problem is connected with the fact that if the word ‘‘logic’’ in DefLogCor3 is supposed to refer to a ‘‘logical system that is used as the benchmark’’, we might be lead to conclude that the concept of logical correctness is historically relative. The point is that the definition may be taken to suggest that before Aristotle nobody could make a logically correct argument as there were no logical systems. But the idea that logical correctness of arguments emerges only as a ‘product’ of the processes of our creating logical systems appears quite strange. It seems then much more natural to interpret DefLogCor3 as presupposing an ‘objectivist’ interpretation of the definition.

The interpretation we call objectivist maintains that logical systems are not created, that they are rather discovered, by us, humans. Thus, e.g. the most common logical system—the first-order predicate logic—is an abstract structure existing beyond space and time and suitable to serve as a measure to any (natural language or other) arguments independently of when, in human history, they occur. (That it is only at some historical point that we become able to apply the measure is quite another matter.) We must of course suppose that, among the many structures that exist in this way, this one is somehow intrinsically privileged in that it is normative with respect to our reasoning.19

An alternative to this ‘objectivist’ interpretation would be an interpretation that we can call ‘presentist’. The presentist would rather say that all arguments (including those formulated in pre-Aristotelian ages) are to be judged by our present standards—arguments are (and were) correct if they instantiate argument forms that are recognized as valid within current logical systems, i.e. systems that we—for good reasons—now adopt as respectable.20

Both the objectivist and the presentist interpretation of DefLogCor3 are philosophically controversial, but we are not going to discuss their problematic aspects here as we are interested primarily in logical incorrectness. We will simply suppose that DefLogCor3 is one of the possibilities of how to make the concept of a logically correct argument clear enough for the purposes of our discussion, the main point of which is to achieve the concept of logical incorrectness that would be explicated on a similar level of clarity.

# 7 Classification of Correct Arguments

Before we proceed to the explication of the strong concept of logical incorrectness, we should make one more preparatory step which concerns the classification of correct arguments. As we have said, it is a common wisdom that some arguments are logically correct. A paradigmatic example is the argument (A1).

But as we have already seen, there are some arguments that are correct, but not correct for logical reasons. Remember our argument (A3)—arguments similar to it are sometimes called analytically correct. Their correctness—the fact that they manifest a reliable (justified) step in reasoning or argumentation—can be revealed by semantic analysis of the sentences of which they consist. Thus, in the case of (A3) all competent English speakers are able to identify the argument as correct— their competence regarding the words dog and animal involves the knowledge that nothing can be a dog unless it is an animal.

Besides logically and analytically correct arguments, it makes sense to consider correct arguments of yet another type, viz. (A4) and (A5). Their existence is connected to the fact that, as we noted, the ‘‘impossibility’’ involved in DefCor need not be the most narrow kind of impossibility that amounts to inconceivability, it may be merely impossibility given that the world will not be radically different from the actual world with its physical laws, history etc. (A4) is a good argument because we take for granted (and we do not take the opposite as a ‘‘possibility’’) that Athens is in Europe; and we similarly accept (A5) because we take for granted that there are no animals on Mars. Let us call the arguments that are correct due to some fixed and stable (though perhaps not eternal and unalterable) factual setup status quo correct.21

It is clear that in natural language the boundaries between these types of arguments are far from sharp and that talking about them as separable is an idealization. However, as the distinctions can make the landscape of arguments a bit more comprehensible, let us take them for granted and depict the set up by a diagram. We will adopt the notational convention that classes of arguments which are given names in the diagram are always full circles or ellipses (rather than, say, annuli or other more complex shapes). Then we may draw the following pictures:

![](img/0e6e31f3b2883975e28ddb8886ad2f34668818c37ef4b27ceab8b015a73ac042.jpg)  
Picture 1

Now we are getting close to disclosing further reasons why the weak conception of logical incorrectness is problematic. Let us ponder how we might in a similar way depict the place of different kinds of incorrect arguments within the domain of all arguments. At first sight it may come to mind that echoing the terminology indicated by Picture 1 we should—in case of incorrect arguments—get a picture that is close to it, namely

![](img/23771761976f680ccda33d0c9c460427dcfd51a2afa7ffb901f72b38d3f8aaf6.jpg)  
Picture 2

However, if we understand incorrectness in the weak way, then Pictures 1 and 2 are clearly incompatible. If we accept Picture 1, the classes of logically incorrect, analytically incorrect and status quo incorrect arguments will not be disjoint as in Picture 2. Picture 1 shows that for example those arguments which are weakly analytically incorrect (in the sense of not being analytically correct) include all incorrect arguments as well as arguments which are logically or status quo correct. Thus, for example, the incorrect argument It rains hence it is windy should obviously be classified at the same time as logically incorrect, analytically incorrect and status quo incorrect which is at odds with the depiction on Picture 2. And it turns out that on the construal of incorrectness suggested by Picture 2 we are not able to depict the categories of incorrect arguments using the convention introduced above (namely, always depicting the salient classes of arguments as circles).22 Such a picture is quite unappealing—it is strange to admit that logically correct arguments are analytically incorrect.

But perhaps Picture 1 is not well conceived and we should adopt another view of the interrelations among the domains designated by the terms ‘‘logically correct’’, ‘‘analytically correct’’ and ‘‘status quo correct’’. It seems, in fact, quite natural to take logically correct arguments as specific cases of analytically correct arguments (which is quite plausible, for logically correct arguments do appear to be a kind of analytically correct arguments—arguments correct in virtue of meanings of merely the logical expressions contained in them) and analytically correct arguments as specific cases of status quo correct ones. This gives us the following picture:

![](img/fc29ec0326c8ba81e39b1deedefca42d2b88067cf5539cb3cb84b8e3f1a3a5f0.jpg)  
Picture 3

This construal of the classes of correct arguments together with the weak interpretation of incorrectness then yield a similar depiction of the respective classes of incorrect arguments:

![](img/60f423c3c74fbaa01a217d367cd37b0d550ff2fda8a6e1cd0b359e519bda1c25.jpg)  
Picture 4

This picture suggests that analytically incorrect arguments are a specific type of logically incorrect arguments and status quo incorrect arguments are a specific type of analytically incorrect arguments. Though, as we have said, the terminology is unsettled and to a large extent a matter of convention, these inclusions appear intuitively quite strange. Thus, for example, while it seems natural to presuppose that arguments that are logically incorrect should be incorrect quite independently of circumstances, according to the terminology suggested by Picture 4 this is not the case. The set of logically incorrect arguments also includes—in its most inner section—arguments whose incorrectness is conditioned by some persistent features of the status quo, arguments like:

It is obvious that while here and now the argument is incorrect, it need not be so in all circumstances whatsoever. Though the scenario in which the Earth becomes uninhabitable and Mars the only place in the universe inhabited by humans and animals is unlikely, it is not utterly inconceivable and might even acquire the status of the status quo.

The relationship between the classes of incorrect arguments that appears to be most intuitively plausible is thus rather.23

![](img/5c8c0d9a69dc25752da4a4f480d8957551b0ea55542cc9a9d5c9db8690e680f4.jpg)  
Picture 5

It is natural to assume that language and logic are viewed as fixed and thus for example the analytically correct argument Tracy is a sister of John hence Tracy is a woman as well as a logically correct argument Tracy is tall and thin hence Tracy is tall are true in all circumstances that we take into account.24 This picture, however, is quite clearly excluded as long as we accept the weak conception of incorrectness. We can thus conclude that our previous impression that we should search for a stronger conception of logical incorrectness is reinforced. Considerations aiming in this direction will engage us for the rest of this article.

# 8 Incorrect Arguments

Before we turn our attention to logical incorrectness, let us try to get some firmer grasp on incorrectness in general. Which arguments deserve to be called incorrect? We may try to formulate a definition that is quite straightforwardly derived from DefCor:

DefWInCor An argument is incorrect iff it is possible that its premises are true and at the same time its conclusion is false.

This definition obviously suggests a weak concept of incorrectness. What exactly the concept is depends on how we interpret the ‘‘possible’’ in this definition. Clearly, if we interpret it widely (e.g. as ‘‘conceivable’’), some (if not all) arguments that we call status quo correct turn out to be incorrect according to this definition. This suggests that it might be reasonable to stick to our former, looser construal of the ‘‘possible’’ under which it is impossible that Athens is not in Europe or that a dog lives on Mars. Even so, we still encounter some prima facie plausible sounding arguments like

or

that would come out as incorrect. But perhaps this is as it should be—those who reason in ways suggested by (A7) and (A8) cannot completely rely on their reasoning—sometimes, though only exceptionally, they may start with a premise that is true and end up with a false conclusion.25

Can we, aside from this weak notion of incorrectness, have some similarly simple stronger notion? The following definition of strong incorrectness comes out naturally:

DefSInCor An argument is incorrect iff it is not possible that its premises are true and at the same time its conclusion is true.

or, in other words:

DefSInCor0 An argument is incorrect iff it its conclusion is inconsistent with its premises.26

This account of incorrectness is, of course, very strong—an argument counts as incorrect in this strong sense only if it is inevitably misleading—whenever the premises are true the conclusion is surely not. Neither (A7) nor (A8) will be incorrect in this strong sense and this seems reasonable—they are arguments that may (in exceptional cases) lead us astray, but this will happen only rarely. Less plausible is that arguments which also usually lead us astray and do not do so only exceptionally will not be classified as incorrect—thus, according to DefInCor0 , the following arguments will not be (strongly) incorrect:

(A7’) John is a teacher John is illiterate   
(A8’) Fido is a dog Fido does not bark

This is, however, acceptable if what we are after is a strong concept of incorrectness. Thus, we might take DefSInCor0 as a promising candidate for the definition of strong incorrectness. All strongly incorrect arguments are, of course, also weakly incorrect.

Unfortunately, both DefWInCor and DefSInCor have an unacceptable consequence. The point is that any argument with inconsistent premises will according to them be classified as incorrect—despite the fact that it will be, at the same time, classified as correct by DefCor. This problem can be fixed by giving special treatment to arguments with inconsistent premises, which are clearly anomalous. We can stick to DefCor and decide, by stipulation, that such arguments are not incorrect. (It might seem more plausible to exclude arguments with inconsistent premises from logically correct arguments, rather than, as we do, from logically incorrect ones; but this would clash with the notions of validity and correctness which are standard in logic.) This leads us to the following modification of DefSInCor027:

DefSInCor00 An argument is incorrect iff its premises are consistent, but they are inconsistent with its conclusion

This, finally, seems to be an acceptable definition of strong incorrectness. Now what about its specific subcases, (strong) analytic incorrectness and (strong) logical incorrectness? We have suggested that these concepts should be embedded in such a way that all logically incorrect arguments are analytically incorrect and all analytically incorrect arguments are status quo incorrect.

It would seem that to find the strengthening of our concept of (strong) incorrectness to (strong) analytical incorrectness is not difficult—an argument is analytically incorrect iff it is incorrect and its incorrectness is exclusively a matter of the meaning of expressions of which it consists; hence, to determine the incorrectness we need not consult any extra-semantic facts.

# DefSAnInCor

An argument is analytically incorrect iff its premises are consistent and they are inconsistent with its conclusion, where the inconsistency is guaranteed alone by the semantics of the expressions of which the argument consists.

An example of an analytically incorrect argument would be the following28

(A9) Fido is a dog Fido is not an animal

This definition, of course, is far from unproblematic. One point is that we cannot draw a sharp boundary of semantics. Another point is that the formulation ‘‘impossibility is guaranteed alone by semantics’’ may need some clarification. However, we take it to be based on an acceptable simplification, and we will not spend more time on its elaboration. The reason is that we want to move on to the ultimate topic of the paper—the concept of logical incorrectness.29

# 9 A Strong Notion of Logical Incorrectness

It would seem that the step from the definition we have reached in the previous section to the definition of strong logical incorrectness is straightforward. We might say, in analogy with DefSAnInCor, that an argument is logically incorrect in case its incorrectness is guaranteed by the meanings of the logical expressions occurring in the sentences of which the argument consists.

How would we recognize that the incorrectness is merely a matter of the meaning of the logical expressions? A straightforward way is the one that we outlined when we dealt with the concept of the logically correct argument. Namely, to consider variants of the argument with different extralogical expressions—if incorrectness is only a matter of logical vocabulary, then these variants would be incorrect as well. We might thus make a move analogous to the one above when we stepped from DefLogCor1 to DefLogCor2. In this way, we would reach that definition by saying that an argument is logically incorrect iff it has consistent premises and every instance of its logical form has premises inconsistent with its conclusion. But in view of the reasons that led us from DefLogCor2 to DefLogCor3, we conclude that it is better to proceed directly to a definition that is construed along the same lines as DefLogCor3:

DefSLogInCor1 An argument is logically incorrect iff it is an instance of an argument form that is invalid within the logical system(s) we take as the benchmark of correctness.

The important question here is what exactly does ‘‘invalid’’ mean in this context. First, let us try to construe it simply as ‘‘not valid’’. This does not seem to lead to a usable criterion of logical incorrectness. Consider, for example, (A3). Its logical form within the standard predicate logic would be

$$
{ \frac { \forall x \ ( F ( x ) \to G ( x ) ) } { \forall x \ ( F ( x ) \to H ( x ) ) } }
$$

which is certainly not valid (does not have only correct instances); and it does not seem that any other logical calculus can improve on this. (Indeed (A3) is not logically correct, and thus any account of its correctness would have to trespass on the boundaries of logic). Hence, according to DefSLogInCor3, (A3) would have to be proclaimed logically incorrect. This would be all right if we had settled for the weak notion of logical incorrectness, but for a stronger logical incorrectness, which should amount to proving incorrectness by logical means, this means so serious an overstretching of the concept that it does not seem acceptable. We need another interpretation of the term ‘‘invalid’’.

It would seem that such a stronger construal would result from understanding an argument form ‘‘(strongly) invalid’’ if it is the opposite counterpart of a valid argument. The question, however, is whether we can give the phrase ‘‘opposite counterpart’’ a clear and useful sense.

If we consider the general argument scheme

$$
\frac { A _ { 1 } \ldots A _ { \mathrm { n } } } { B }
$$

then it seems natural to propose that it is

$$
\begin{array} { r l } { ( \mathrm { A F 1 0 ^ { * } } ) } & { { } \underline { { A _ { 1 } \ldots A _ { \mathrm { n } } } } } \\ { } & { { } \overline { { \qquad \quad \neg B } } } \end{array}
$$

that should be adopted as its opposite counterpart.30 If an argument form is logically valid then the truth of its premises guarantees the truth of its conclusion; in case of the opposite counterpart, the form of the argument should guarantee that the conclusion cannot be true if the premises are true. Hence, the concept of the opposite counterpart is such that the opposite counterpart of an argument form AF is the argument form with the same premises as AF and with the conclusion that is the negation of the conclusion of AF.

Then we arrive at the following definition of the logically incorrect argument:

DefSLogInCor2 An argument is logically incorrect iff the opposite counterpart of its logical form is valid in the logical system we take as the benchmark.

Is this explication of the opposite counterpart satisfactory? Consider the argument form

$$
\frac { A \wedge B } { B }
$$

This argument form is clearly valid in classical logic. Now its opposite counterpart is

$$
\begin{array} { r l } { ( \mathrm { A F 1 1 ^ { * } } ) } & { { } { \frac { A \wedge B } { \neg B } } } \end{array}
$$

Do we want to see all arguments of this form as logically incorrect? Consider the following argument:

(A12) Fido is a cat and Fido is not a cat and Fido is black Fido is not black

The argument can be ascribed the form $( \mathrm { A F 1 1 ^ { * } } )$ (where Fido is a cat and Fido is not a cat replaces $A$ and Fido is black replaces $B$ ), and hence it should count as logically incorrect. However, it can also be ascribed the logical form

$$
\frac { ( A \land \neg A ) \land B } { \neg B }
$$

which is valid in classical logic. Thus, it might seem that (A12) should be classified as logically correct and logically incorrect at the same time.

But we already know how to do away with this problem. For one should note that the argument (A12) (and indeed any argument of the form (AF12)) is the problematic kind of argument that has contradictory premises. We, obviously, must exclude this kind of argument either from the set of correct arguments, or from the set of incorrect ones. It might seem tempting to proclaim such arguments as neither logically correct nor logically incorrect, or to exclude them, as ‘pseudoarguments’, from the domain of arguments altogether. The first option, however, requires giving up DefCor (and parting with the mainstream tradition in logic). The second one would lead to a situation where we need not always be able to recognize what an argument is and what it is not, which seems to be at odds with our intuitive notion of an argument. Hence we suggest as a solution to the mentioned problem the following modification of DefLogInCor2:

DefSLogInCor3 An argument is logically incorrect iff if it has consistent premises and the opposite counterpart of its logical form is valid in the logical system we take as the benchmark.

This definition provides for an elucidation of the concept of logical incorrectness that is dependent on the logical theories that we accept. This gives the definition a slightly relativistic flavor; but we assume that if we assess logical systems according to how faithfully they reflect inference in natural language, there is no room for any boundless relativism. (A space for relativism exists only where the inference is essentially fuzzy, which is far from everywhere).

# 10 Conclusion

Consider the argument (A13) All dogs are mammals All mammals are animals All animals are dogs

It has a logical form which is clearly invalid and this can be shown by means of Aristotle’s syllogistics as well as by means of modern predicate logic. As it is simple it is easy to see that it does not instantiate any other logical form which might be logically valid. Thus it is ‘‘logically incorrect’’ in the sense of not being logically correct—but it is not logically incorrect in the sense of being guaranteed by logic to lead us to a wrong conclusion. We know that logic does not pay attention to the meanings of extralogical words; hence consider the case that the word animal would be systematically substituted by the word dog and the word mammal by the phrase an individual of the genus Canis lupus familiaris. Then we would receive an argument that has from the viewpoint of syllogistic and predicate logic the same structure as (A13), namely the argument

(A14) All dogs are individuals of the genus Canis lupus familiaris All individuals of the genus Canis lupus familiaris are dogs All dogs are dogs

But this argument could be hardly proclaimed as wrong. In contrast to this, the argument

(A15) All dogs are mammals All mammals are animals Some dogs are not animals

is wrong for no other reasons than the logical ones. (Note that the analogous substitution we used to turn (A13) into (A14) would turn it into the argument with the patently unacceptable conclusion Some dogs are not dogs.) As the incorrectness of (A15) is demonstrable by means of logic, we claim that there is, pace Massey, a ‘‘way to show that an argument is invalid’’ (1975, p. 64).31

Unlike arguments that are logically correct, arguments that are logically incorrect in the sense just specified are probably not very frequent. But they form a distinctive category, and to be clear about the role of logic in the classification of argument we must distinguish it from the category of arguments that are merely not logically correct. (As we have said—an argument that is logically incorrect in this weaker sense can still be correct.).

To sum up, the ultimate concept of strong logical incorrectness that has resulted from our considerations is hence DefLogInCor3. It has the following properties:

1. Every logically incorrect argument is incorrect. This was a basic desideratum for strong—in contrast to weak—logical incorrectness and our definition does fulfil it.

2. There are no circumstances which could make a logically incorrect argument into a correct one.

This means that an argument that is (strongly) logically incorrect, as we have already noted, is not one that is not guaranteed to be right, but rather one that is guaranteed to be wrong.

3. All logically incorrect arguments are incorrect for logical reasons.

We have treated the distinction between incorrectness for logical reasons and that for other reasons as derivative from the distinction between logical correctness and other forms of correctness; we did this in that we identified logically incorrect arguments with arguments that are incorrect and are, in a clearly delimited sense, opposites of logically correct arguments.

4. Logical incorrectness presupposes a logical system we take as a benchmark. This is probably the most controversial feature of our definition. We are, however, convinced that any reasonable account of logical incorrectness has to view natural language arguments through a prism of a certain logical theory. The data concerning correctness of the arguments must be ‘consolidated’ by logic, before they could serve as determinate footing for the definition of (in)correctness.

5. Logical incorrectness is not a purely formal property—logically incorrect arguments are not distinguished only by their forms.

This is the price we have to pay if we want, as we do, to identify correctness generally with truth-preservation, strong incorrectness generally with ‘truthblocking’ (the impossibility of preserving truth from premises to conclusion, i.e. inconsistency) and if we do not want to have arguments that are correct and incorrect at the same time. For it is clear that an argument with inconsistent premises is (trivially) both truth-preserving (has a true conclusion in every case it has true premises) and truth-blocking (has a false conclusion in every case it has true premises).

6. The proposed concept of logical incorrectness is not overly narrow.

Arguments that come out as logically incorrect according to our definition are thus more interesting than arguments that instantiate the ‘‘super-invalid argument forms’’ mentioned by Cheyne.32 Diagnosing an argument as logically incorrect is a non-trivial matter; it does not concern only arguments that are trivially incorrect. Thus, the following argument, to cite one example, is logically incorrect:

(A16) All those who vote for democrats want health insurance Nobody wants flat tax, health insurance and social security Everybody wants social security Some of those who vote for democrats want flat tax

Acknowledgments Work on this paper was supported by the research Grant No. 13-21076S of the Czech Science Foundation. We are grateful to Georg Brun, Hans Rott, Vı´t Puncˇocha´rˇ, Marta Vlasa´kova´ and anonymous reviewers of Argumentation for valuable critical comments.

# References

Bolzano, B. 1837. Wissenschaftslehre. Sulzbach: Seidel. English translation The Theory of Science, Berkeley: University of California Press, 1972.   
Carroll, L. 1895. What the tortoise said to Achilles. Mind 4: 278–280.   
Cheyne, C. 2012. The assymetry of formal logic. In The logica yearbook 2011, ed. M. Pelisˇ, and V. Puncˇocha´rˇ. London: College Publications.   
Copi, I.M., C. Cohen, and K. McMahon. 2014. Introduction to logic, 14th ed. Harlow: Pearson.   
Finocchiaro, M.A. 1981. Fallacies and the evaluation of reasoning. American Philosophical Quarterly 18: 13–22.   
Frege, G. 1879. Begriffsschrift. Halle: Nebert. English translation Begriffsschrift in From Frege to Go¨del: A source book from mathematical logic, ed. J. van Heijenoort, 1–82. Cambridge (Mass.): Harvard University Press.   
Gabbay, D., et al. (eds.). 2013. Handbook of deontic logic and normative systems. London: College Publications.   
Hocutt, M. 1979. The elements of logical analysis and inference. Cambridge: Winthrop.   
Jørgensen, J. 1937. Imperatives and logic. Erkenntnis 7: 288–296.   
Massey, G.J. 1975. Are there any good arguments that bad arguments are bad? Philosophy in Context 4: 61–77.   
Massey, G.J. 1981. The fallacy behind fallacies. Midwest Studies in Philosophy 6: 489–500.   
Peregrin, J., and V. Svoboda. 2013. Criteria for logical formalization. Synthese 190: 2897–2924.   
Peregrin, J., and V. Svoboda. (t.a.). Logical formalization and the formalization of logic(s). To appear in Logique et Analyse.   
Quine, W.V.O. 1960. Word and object. Cambridge, MA: MIT Press.   
Rips, L.J. 1994. The psychology of proof: deductive reasoning in human thinking. Cambridge, MA: MIT Press   
Smith, P. 2003. An introduction to formal logic. Cambridge: Cambridge University Press.   
Tarski, A. 1936. O pojeciu wynikania logicznego. Przeglad Filozoficzny 39: 58–68. English translation On the concept of following logically, History and Philosophy of Logic 23: 155–196, 2000.   
Vranas, P.B.M. 2011. New foundations for imperative logic: Pure imperative inference. Mind 120: 369–446.   
Walton, D. 1986. What is a fallacy? In Argumentation: Across the lines of discipline, ed. F.H. van Eemeren, et al., 323–330. Dordrecht: Foris.   
Walton, D. 2006. Fundamentals of critical argumentation. Cambridge: Cambridge University Press.   
Woods, J., and A. Irvine. 2004. Aristotle’s early logic. In Handbook of the history of logic, vol. I, ed. D.M. Gabbay, and J. Woods. Amsterdam: Elsevier.