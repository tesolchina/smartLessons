# GCAP3226 Week 4 Lecture Transcript
## Simulation Methods in Public Administration
**Date:** September 20, 2025
**Processed:** 2025-09-23 15:33:11
**Total Entries:** 1079

---

## Lecture Content


### Segment 1 - Simon Wang (00:00:00.230)

[00:00:00.230] Alright, so, we are in week 4 now for our course, and, before we get started, I just want to invite all the students to, log in with your HKBU credentials, so you will be able to have access to this page.

[00:00:18.900] And not every student will have access to this page. By default, I think only the students from science faculty, will have access to the API key. But I submitted your name to ITO, so you should be able to access this page as well.

[00:00:37.880] So very briefly, I want to explain what is API. API stands for Application Programming Interface.

[00:00:45.400] Which is a different way to communicate with the computer system. The more conventional, typical way of

[00:00:55.170] Communicate with the computer system is through what we call graphical user interface.

[00:00:59.890] Like what you can see now. So, you see there's some graphics, and you enter, you type some text.

[00:01:08.550] And you will be able to communicate, and the chatbot will respond in a graphical user interface.

[00:01:16.230] But the application programming interface is, a different interface in the sense that, we do not use this kind of,

[00:01:25.070] GUI, or graphical user interface, instead of we write codes. And, through the codes, and we, following the protocols and rules specified in the API, so that

[00:01:39.540] Our computer program can communicate with a computer system, like large language model.


### Segment 2 - Simon Wang (00:01:45.160)

[00:01:45.160] Now, the reason we need you to grab this key

[00:01:49.840] is because later on, you need to enter the key into a platform that we built. And this way, our platform will be able to leverage

[00:02:00.920] the ITO's platform, and Because, you know, tokens are not free.

[00:02:08.240] You know, that's the basic fact. The fact that whenever you talk to a large language model, somebody has to run the computer somewhere to process your response and to run the model.

[00:02:21.900] So, tokens are not free, and ITO actually bought a lot of tokens from Microsoft Azure, and therefore, each of us can access the HKBU General AI services. Now, when you got the API key, and you enter to our system.

[00:02:41.220] you will be able to use the token from HKB UITO allocated to you.

[00:02:48.780] And, and then you can enjoy the services, okay? So I hope that's…

[00:02:55.650] clear enough instructions or explanation. If it doesn't make sense to you, that's okay, because you don't have to understand everything in order to use it, right? So all you have to do is just come to this page.

[00:03:11.970] and generate the API key, and remember, once you generate the key, you have to keep it somewhere, okay? Because it will show once only.

[00:03:20.220] And I'm not going to generate my key again, because I already generated before.


### Segment 3 - Simon Wang (00:03:25.380)

[00:03:25.380] So, go ahead and do that, and keep it in a place that's safe, okay? So, any, any question?

[00:03:41.140] So take some time and, get your key.

[00:03:48.860] I think I need to find mine as well.

[00:04:11.760] Now, Okay, I think, we should officially get started. We've got 27 students here, which is great.

[00:04:23.310] Well, again, I just want to very briefly talk about… because today, the reason why we are, we are having this, online meeting is because Typhoon, so I want to very quickly, share with you two letters

[00:04:35.960] that I… I published a while ago.

[00:04:38.880] about Typhoon, so… because, in this course, we're trying to…

[00:04:43.840] look at the government's decision and how data is being used to inform the government decisions, and we don't just do things within the classroom. This is an experiential learning course, so we actually want students to experience

[00:04:58.520] something different, something that you don't typically get in a university classroom. So…

[00:05:06.290] One thing that I hope some of you can experience is actually if you write letters to South China Morning Post, because this way you will be able to voice your opinions, you're going to join a conversation about public policy. So here's one example. If you still remember, I don't know whether you remember, this was a letter published


### Segment 4 - Simon Wang (00:05:25.070)

[00:05:25.070] Beck… In 2018, when there's this typhoon called, Menkok, so,

[00:05:35.820] rumor says that, you know, the coming typhoon is as strong, or even stronger than this one.

[00:05:41.920] But look at what happened, the day after typhoon. You know, people get stuck in this, in this, MTR station in Taiwai. And, I was… I was writing, you know, I wrote this letter to argue that actually, we should consider

[00:05:59.710] Allowing people to take a break after the typhoon.

[00:06:03.210] In case, you know, the city, you know, needs some time to recover.

[00:06:07.540] So, so that's, that's one, one…

[00:06:12.490] letter I want to share with you.

[00:06:14.800] And I think it's important to take a data-driven approach to this kind of decision-making. I don't know whether the Security Bureau or the Office of Chief Executive has been reviewing this case.

[00:06:27.050] I hope they have learned a lesson, because in terms of data-driven approach, we should definitely look at the whole, you know, transportation network, the infrastructure, to what extent there's damages to the system that the city needs time to recover.

[00:06:45.090] Right? So, so that's… that's a very important, case we want to, we want to consider. In fact, we have one team who's going to work on Typhoon, this semester, so I hope that team can also take a look at, this, this issue.


### Segment 5 - Simon Wang (00:07:02.840)

[00:07:02.840] Now, another letter I want to share with you, it was published in, last year, actually, 2024,

[00:07:10.700] Because starting from last year.

[00:07:15.060] the Hong Kong stock market will actually operate as usual, even when there's a typhoon.

[00:07:23.210] So, this, this is a new, new arrangement, starting from last year, and the argument I was trying to make is that

[00:07:31.710] as the title suggests, if the Hong Kong stock is changed.

[00:07:36.530] Could operate as usual, you know, because people work from home and, etc.

[00:07:43.390] then everybody should be doing that. Knowledge workers, schools, universities, we should all just, work as usual, you know, even during the typhoon days.

[00:07:55.600] But, unfortunately, at this stage, the Education Bureau

[00:08:00.320] the universities do not really have any official policies over how work should be arranged during the typhoon days. So again, if we think about data-driven approach, if we think about how we can help the government to make better decisions, then we need to

[00:08:17.640] start thinking about how to collect the data, how to use the data to, inform the decisions, alright? So, you know, because of today's timing, I just want to kind of share with, two, essays that,


### Segment 6 - Simon Wang (00:08:31.660)

[00:08:31.660] I published it a while ago.

[00:08:34.350] And another quick update is I've created

[00:08:39.200] Google Drive folders for each team, because I think right now we've got six teams. Each team has already selected a specific topic, so we're kind of ready to move on, to start actually working on the projects. So, anyone who is not yet in a team.

[00:08:59.220] or anyone who cannot access to the Google Drive folder that I share through the small WhatsApp group.

[00:09:05.800] please let me know. You can send a message to the small WhatsApp group, you need to give me your Gmail account. In fact, your classmates, your groupmates who have access to the Google folder, Google Drive folder, they should be able to invite you to access the Google folder.

[00:09:21.490] Alright? So, within the Google Drive folder, you will be able to see a couple of Google Docs. Okay, so all these Google Docs are empty at this stage, but just to kind of quickly go through this…

[00:09:37.820] We will have a meeting notes page. Basically, whenever we meet, whenever we have any progress on the project, you need to update the meeting notes, and you probably want to meet with your teammates from time to time to, you know, start working on the project, then you should update the meeting notes.

[00:09:55.630] We have a data collection plan, because,

[00:09:59.480] Next week, we're going to have small group meetings, and the week after is actually public holiday.

[00:10:05.330] So you should take the time to… the whole week, to doing some data collection.


### Segment 7 - Simon Wang (00:10:10.230)

[00:10:10.230] So, that page, that doc, is for you to update records about data collection.

[00:10:15.850] And there's also a worksheet, this is just a spreadsheet for you to, in case you want to have, put some structured data in that sheet, you can do that.

[00:10:25.240] We have a project report.

[00:10:27.970] document, that's where you can actually start planning your project report. This, this document, I think I'm going to rename it because, you know, on a second thought, I think this document should be more about outreach and presentation, so I'm going to rename it later.

[00:10:43.580] So basically, this Google Drive folder is where you want to do some real work, and you want to move forward.

[00:10:50.410] And just one quick reminder about doing everything is you want to document your contribution, okay? So whenever you're updating the document, whenever you are making some efforts to move the project forward, write down everything you have done with your name on it.

[00:11:07.060] Okay? Because at some point, we will start reviewing, everybody's work, we want to make sure that everybody contributes fairly to the teamwork, because part of the… I think about 50% of the whole course grades is by groups. But, we definitely want, you know, students to.

[00:11:25.740] contribute, and we enjoy teamwork, and we work together. So, it's very important to keep record of everything you do.

[00:11:34.850] In, in this space.

[00:11:37.140] Alright, and both Taylor and I, we have access to this space as well, and feel free to raise any questions, you can add the questions here, and then you can, you know, send us the link through the WhatsApp group or email us, and basically, this is going to be the platform where we're going to do the collaboration work.


### Segment 8 - Simon Wang (00:11:57.000)

[00:11:57.000] Okay, so any, any questions, any concerns, just, let us know.

[00:12:02.330] And this is actually a website I built a bit earlier,

[00:12:11.190] you can check out. It's kind of fun, because we use them

[00:12:16.250] API to access the data from Hong Kong Observatory, and we update this in real time, so we'll be able to see

[00:12:25.060] dumb, the wind data from the 30 stations

[00:12:30.340] And to see whether… to what extent the real, wing strings actually align with the signal number that the observatory published. But I won't get into details, because that's…

[00:12:44.420] basically the project of one of the teams. But just for fun, because you can see that the storm is coming, and we should be able to look at the data in real time.

[00:12:55.010] Right? Now… Before I invite, Taliet, you know, for Dr. Wu to talk about

[00:13:02.900] simulation, which is the main focus of today's topic, today's work discussion, because last week we talked about regression, this week we talked about simulation, there's a little bit more, in-class exercise we're going to work on. I want to talk about reflective essay.

[00:13:19.280] Now, a reflective essay is one of the assessment components. It actually accounts for 20% of the final grades. There's a total of 3 reflective essays you need to write, and this essay is not very long, it's only about 200 words.


### Segment 9 - Simon Wang (00:13:36.270)

[00:13:36.270] And one of the, kind of, the special features of this course is that you can use AI to write an essay. So we have some AI chatbot.

[00:13:46.370] that can help you, which is the reason why we invite you to set up the API key from the ITO page, right?

[00:13:56.220] So, if you come to this Moodle page.

[00:14:00.280] you will be able to see there's the reflective essay assignment. The deadline is,

[00:14:06.350] about two weeks from now, okay? So, there's a little bit of time you can work on, so just take your time, and you don't have to submit it just yet, so any question you may have, just let us know.

[00:14:21.670] The way you submit this essay is just to reply, okay? So you reply here.

[00:14:28.630] And you can submit your… Your essay.

[00:14:35.360] Now, actually, you can read through this Moodle, so a Moodle page, so I'm not going to get into everything, but just one thing to highlight is that we have this

[00:14:46.280] Page.

[00:14:47.900] This is where you can actually, talk to an AI, okay?


### Segment 10 - Simon Wang (00:14:54.190)

[00:14:54.190] So we have this AI writing assistance, as you can see. You need to reflect on what you have learned in the past 4 weeks or so, and also you want to start thinking about the project, alright?

[00:15:07.510] Because in the past 2 weeks, well, including this week, The main task

[00:15:14.810] we're trying to teach you, well, especially Italia, is trying to teach you some tools, okay, for quantitative reasoning. We talked about regression, last week talked about… we're going to talk about simulation.

[00:15:26.390] And once you learn a little bit about these tools, you need to think about how these tools will be applied to your projects.

[00:15:34.430] And while you're doing that, you can start writing this refractive essay, okay? So…

[00:15:42.450] As you can see here, there's a little bit of information, and you can go back to the Moodle page.

[00:15:47.680] But then… how do you use the tutor? Well, basically, you need to get your key.

[00:15:55.030] And then you click here, That will give you… get you to the… the tutor page.

[00:16:06.630] This is iframe, so it takes a while to load.

[00:16:13.430] And, here is where you want to enter the key. Okay, let me see if I got my key.


### Segment 11 - Simon Wang (00:16:29.740)

[00:16:29.740] So you got your key.

[00:16:31.990] And you choose your model, usually 4.1 would be good, and then you click connect.

[00:16:41.990] Now, once you click connect, you get connected.

[00:16:45.320] Right, and then there's some system prompt here. There's a welcome prompt here, it says, You know,

[00:16:52.810] This is your tutor for the course, you need to write a short, refractive essay and everything.

[00:16:58.800] And said, type OK to get started, then you type OK.

[00:17:10.680] Okay, and then the tutorial will start talking to you. Great, let's get started. Thinking about your team project, where were your… the key decisions made by the government that your team plans to focus on?

[00:17:21.849] Remember, we have this post that we talked about a while ago, we talk about, like.

[00:17:29.750] the group project instruction and timeline, I think we talked about this in week 2 or something.

[00:17:35.220] So, last week and this week, we explored topics, we talked about the tools, and next week, when we do the group consultation, we need to


### Segment 12 - Simon Wang (00:17:43.110)

[00:17:43.110] you know, finalize the top… I think everybody already selected topic, but then we have to start working on it.

[00:17:48.590] So go through this page, And then you come back.

[00:17:53.330] And you can start talking, so something like, maybe you can just, use an example.

[00:18:00.130] whether… to… Hello, people.

[00:18:06.210] To take a day off after.

[00:18:09.560] Typhoon. So just, just, just as an example, okay?

[00:18:14.070] And, and, you have a conversation with, with the chatbot.

[00:18:18.480] and go, and so on and so forth, and then your teams look at this, think about the data, right? How did the government use the data to inform the decision, blah blah blah.

[00:18:26.990] And you can say what…

[00:18:30.490] You can say something like, what would you suggest?


### Segment 13 - Simon Wang (00:18:45.300)

[00:18:45.300] And also you can close this if you want a bit more space.

[00:18:54.660] Okay, and then you can, you can start, ask the chatbot about…

[00:19:00.740] the model and everything, okay? But just to remember, AI can hallucinate. You know, AI is not 100% reliable. So part of the skills you need to learn in this course when you interact with AI is to be critical.

[00:19:14.870] Okay, don't just take anything that AI says as correct, or as completely reliable, alright? So you keep going like this for a little while.

[00:19:27.310] And then you click this green button. Well, actually, at some point.

[00:19:33.820] You know, the chapel will start… guide you to write an essay.

[00:19:37.990] But if you say, can you write…

[00:19:41.930] the essay. Well, actually, when you say, can you write an essay for me?

[00:19:46.750] The chat will probably help you to write an essay. But remember, you still have to put a lot of thoughts into it, okay?

[00:19:57.170] Because, because what we're trying to do in this course is…


### Segment 14 - Simon Wang (00:20:00.900)

[00:20:00.900] Okay, so actually, they write an essay for you, you see what I mean?

[00:20:04.450] But that's not… clearly not what you want to do to just submit it to the Moodle, right? So you actually have to put more thoughts and everything. But again, when you click here.

[00:20:17.180] You got… You got a, a page.

[00:20:21.700] Where you can, get a chat history and a little bit of analysis of what you have done.

[00:20:28.170] And, you, you can put your ad… you can put your email here, because…

[00:20:32.710] We don't have a login system.

[00:20:35.170] once you close the browser, everything is gone, okay? So, before you close your browser, make sure that you… you click the green button here, green check, and then you email.

[00:20:46.630] Alright, so, so you will get an email copy.

[00:20:49.890] Of the chat history. And your teacher will also get an email copy of the report.

[00:20:55.930] And if you want to download.


### Segment 15 - Simon Wang (00:20:58.450)

[00:20:58.450] You can also download the Markdown or PDF.

[00:21:01.020] Okay

[00:21:02.370] So that's the… that's the platform we built to help you, okay? So I hope you will enjoy it, I hope it's a good experience for you, because we believe that AI is going to be the partner for all of us, you know, especially when you become a knowledge worker after you graduate.

[00:21:22.510] So we want to create an authentic learning experience for you, that's why we have this AI platform for you to try, and…

[00:21:29.810] And just a kind of disclaimer, the platform is relatively new, and there could be some glitches, some, you know, bugs and everything, so please be patient, and do let us know how it goes, and

[00:21:44.290] try to keep a record of everything you do, just in case you, you know, close the browser or something, or the copy may not… the email function may not work properly, then download the Markdown, or download the…

[00:21:58.990] the, PDF before you hit the send button and before you close the browser.

[00:22:05.250] Alright, so I think that's all I have to say. Any questions?

[00:22:16.050] Remember, in the Moodle forum, we actually have one post for each topic. I think the information here is still useful. You do want to come back to kind of learn more about how this, project, you know, how you should pursue this project. And we have the smaller WhatsApp group for each team.

[00:22:33.720] we should work very closely, through the WhatsApp group, and, you know, you guys may want to, you know, set some meetings, and, because, you know.


### Segment 16 - Simon Wang (00:22:44.900)

[00:22:44.900] I think the goal is for us to…

[00:22:48.520] Send off inquiries to, to the government, around, next week.

[00:22:54.280] So you need to start thinking about that as well. And we're going to have another chatbot to help you with that, but for now, this chatbot for writing reflective

[00:23:07.010] journal, a reflective essay, should be a good start, because you only take the opportunity to reflect on what you have learned, and also to think about how you move forward, with the other… with the projects.

[00:23:19.040] Okay?

[00:23:21.130] So, any, any question?

[00:23:24.640] I think a good place to start is actually… this Moodle page.

[00:23:31.320] Because… I think this is the page where… You should have everything.

[00:23:38.360] I saw some message on the chat.

[00:23:47.230] Oh.


### Segment 17 - Simon Wang (00:23:52.650)

[00:23:52.650] Oh, okay, so I think I need to update the Moodle page about the deadline, because we kind of extend the deadline a little bit, so,

[00:24:01.840] Yeah.

[00:24:02.860] So, one question about the Moodle page, I think I need to update that.

[00:24:09.020] I think the deadline should be October 5th.

[00:24:14.030] What should invite accounts says it's not eligible to use the API service.

[00:24:20.900] I think you have to log out and log in again.

[00:24:23.940] Because the… ITO colleagues told me that they have already updated

[00:24:33.670] the records, so all the names that I submitted should have access to the API service. If you cannot, you log out, and then log in again. If you still cannot access the page, just email me, and I will follow up, because I'm sure that I submitted everybody's name.

[00:24:56.430] Any other… Questions?

[00:25:02.720] Okay, so…


### Segment 18 - Simon Wang (00:25:05.130)

[00:25:05.130] I think, that's all I have to say. I'm going to pass the floor to Talia to talk about simulation.


### Segment 19 - Tian WU (00:25:18.850)

[00:25:18.850] Okay, so good morning, everyone.

[00:25:21.200] Can you hear me clearly?


### Segment 20 - Simon Wang (00:25:26.980)

[00:25:26.980] Yeah, okay.


### Segment 21 - Tian WU (00:25:29.220)

[00:25:29.220] Okay, so, can you see my screen of the Moodle page?

[00:25:40.160] We're seeing…


### Segment 22 - Simon Wang (00:25:40.960)

[00:25:40.960] VS Code.


### Segment 23 - Tian WU (00:25:43.100)

[00:25:43.100] Let me share my screen again.

[00:25:48.290] So now should be the Moodle page, right?


### Segment 24 - Simon Wang (00:25:52.060)

[00:25:52.060] Yes.


### Segment 25 - Tian WU (00:25:52.790)

[00:25:52.790] Yeah, okay, so before I started the, explanation, I would like to remind you that I updated the,

[00:26:02.780] Jupyter Notebook for the regression part.

[00:26:07.060] And I also uploaded a new joker notebook, which is called the Box Whisker Plot.

[00:26:13.250] And also, we have the simulation notebook for today's demonstration. So these are the three documents you may download.

[00:26:23.280] So later, we will discuss them one by one.

[00:26:29.370] And before I start, talking about the simulation, I would like to follow up on the last in-class exercise, which is about some data visualization you worked on.

[00:26:45.100] Let me share… Okay, so now my shared screen should be the, VS Code.

[00:26:53.810] Page Wright.

[00:26:56.400] So last time, at the end of the in-class exercise, I invited you to do two visualization tests to explore the relationship of,

[00:27:09.070] That might be interesting.


### Segment 26 - Tian WU (00:27:12.330)

[00:27:12.330] So recall that the data set we used is the municipal solid waste dataset.

[00:27:19.640] Where our response variable is the level of support for this policy.

[00:27:24.630] And the potential explanatory variables, including the demographic variables, attitude-related variables, and behavior-related variables.

[00:27:34.590] And when I received the in-class exercise.

[00:27:37.960] This is the typical visualization result I get.

[00:27:43.240] So you can see for the first visualization, it is about the support level versus the perceived fairness of the policy.

[00:27:52.310] But what you would observe are these, separated dots.

[00:27:57.880] It is because, for fairness and the support level, they're both categorical variables.

[00:28:05.620] they can only take values like 1, 2, 3, 4, 5. There's very limited and discrete integers.

[00:28:13.560] Okay.


### Segment 27 - Tian WU (00:28:14.500)

[00:28:14.500] So all the possible combinations are shown by these dots.

[00:28:19.910] But this is not that informative, given that these two variables, they are categorical.

[00:28:29.250] So I think a better way to do it is… Then open.

[00:28:38.680] The latest regression… notebook.

[00:28:54.560] So here, it's actually used the bar chart.

[00:28:58.710] To show, in different categories of perceived fairness.

[00:29:04.750] What are the percentages of opposed, neutral, and support?

[00:29:10.800] So to do this, we can first record the, strongly against and against as opposed.

[00:29:18.940] And we code very strongly support and support as support, so we will overall have these three groups.

[00:29:29.130] And then… Show the percentages of these three groups.


### Segment 28 - Tian WU (00:29:34.680)

[00:29:34.680] In different categories of this perceived fairness.

[00:29:40.290] So if we… show… Again, the two variables in this way, we can easily observe the trend.

[00:29:48.980] With the increase of the perceived fairness of this policy, The percentages of a post decrease.

[00:29:58.600] Right? The blue bars, the height, decreased.

[00:30:02.570] Whereas for the height of the green bars.

[00:30:07.200] The percentages of support is increasing from, like, 11% to 75%.

[00:30:15.170] So the message is that if the variables themselves are categorical.

[00:30:21.300] Then, it is better to use bar charts.

[00:30:24.860] And using percentages.

[00:30:27.450] To represent for different categories.


### Segment 29 - Tian WU (00:30:30.650)

[00:30:30.650] The percentages of different, groups.

[00:30:36.130] For… for the other categorical variable.

[00:30:40.490] I think for this, figure, it is… More informative compared to these dots.

[00:30:51.140] Right, hopefully you, agree with me.

[00:30:54.310] So when we do the visualization, we need to consider the type of data.

[00:31:00.630] So then, when we use this scatter plot.

[00:31:04.350] Well, when the variables are continuous, it is more often to use the scatterplot to show the relationship between the two variables.

[00:31:14.840] So I think in the demo.

[00:31:16.880] We once used the, scatter plot to Let me find it.

[00:31:23.760] So now I'm at this regression model's full notebook.


### Segment 30 - Tian WU (00:31:33.020)

[00:31:33.020] Yeah, here.

[00:31:35.800] So this is not a good example, but at least the, one of the variables

[00:31:42.070] the distance between home and the nearest facilities. This is a continuous variable.

[00:31:49.330] And for this scatter plot, we can see whether, on average, with the increase of the distance between the home of the participant of the survey to the nearest

[00:32:02.720] Recycling facility, whether their support level is increasing or decreasing.

[00:32:10.690] So most of the time, we use Scatterflow to measure or to visualize the relationship between two continuous variables.

[00:32:20.250] This is the first message.

[00:32:24.190] And the second is about the, plot.

[00:32:29.210] Showing the education level versus the level of support.

[00:32:35.060] So again, education level is a categorical variable.


### Segment 31 - Tian WU (00:32:40.050)

[00:32:40.050] Right, it can only take these discrete values, 1, 2, 3, 4, and we know the larger the value, it represents the, respondents has, a higher education, higher level of education.

[00:32:55.980] So again, if these two are both categorical, a more appropriate way to visualize the relationship should be, again, the bar plot, showing the percentages.

[00:33:08.540] In each, there's different, level of education, the, percentages of the, against, neutral, and support.

[00:33:21.580] And here, this plot is actually a box whisker plot.

[00:33:27.680] And this is usually used to show the distribution.

[00:33:31.460] Of a continuous variable.

[00:33:35.330] So I will give, a numerical example to…

[00:33:40.940] To show you what does this box mean, and what this whiskers mean.

[00:33:47.970] So now let's move to the box whisker plot.

[00:33:51.480] I mentioned this notebook in the Moodle.


### Segment 32 - Tian WU (00:33:56.620)

[00:33:56.620] So suppose I have this sequence of values, So I generated these values.

[00:34:02.740] In total, there are 26.

[00:34:06.030] And they are, capped as two decimal places.

[00:34:10.739] And it is already sorted.

[00:34:15.900] So the smallest is from 0.15, and the largest is from 4.85.

[00:34:23.159] to generate the box whisker plot.

[00:34:27.780] We need to calculate the so-called five-point summary statistics for these data points.

[00:34:35.429] Specifically, when you find the minimum value, which is obviously 0.15,

[00:34:42.650] And also the maximum value, which is 4.85, right?

[00:34:47.920] And for the middle 3-1, They are median.


### Segment 33 - Tian WU (00:34:53.460)

[00:34:53.460] So the median basically means the data points were cut the whole data set into two parts.

[00:35:01.730] So the first 50% of the data, their value will be smaller than the median.

[00:35:09.520] And the remaining around 50% of the data, their value, will be greater than the median value.

[00:35:17.980] So, in our dataset, Given that there are 26 values.

[00:35:23.700] So there will be two values sitting in the middle.

[00:35:28.500] Which is the, 13th

[00:35:32.980] 13th data, and the 14th data.

[00:35:38.960] For each role, there are 5 data points.

[00:35:42.500] So, the 13th data point is here, and the 14th data point is here.

[00:35:49.720] And the median will be the average value of the two data points.


### Segment 34 - Tian WU (00:35:56.400)

[00:35:56.400] So we take average of these two, and it is 0.8.

[00:36:01.940] So here, originally, the data points are not exactly two decimal places. So after some rounding, we have this 0.79 and 0.8.

[00:36:13.540] And after we take average, and again, doing the rounding, the median is 0.8.

[00:36:20.850] So this means that if we have a

[00:36:23.590] Like, you imagine that if there is a, little vertical bar here.

[00:36:30.200] This is the first 50% of the data.

[00:36:34.150] Given that This data is already sorted from the smallest to the largest.

[00:36:41.700] Whereas the remaining ones are the later. So from here.

[00:36:47.760] These are the later, or the largest, the 50% of the data.

[00:36:54.650] So this is what this medium means.


### Segment 35 - Tian WU (00:36:57.940)

[00:36:57.940] And in the box and whisker plot, this mean is usually shown as the, the horizontal bar in the middle of the box.

[00:37:09.750] So if we go back to this education level.

[00:37:13.970] you see this horizontal line in the middle of the box? So this is the median.

[00:37:20.890] Median value of the, of these data points.

[00:37:27.590] But we also need to decide the, where this, edge of the box is. So there are two edges, the upper one and lower one.

[00:37:37.320] And we need to decide, what this corresponding value is.

[00:37:42.970] And to do that, we need to calculate the so-called the Q1 and Q3.

[00:37:48.970] So it's the, quartile one.

[00:37:51.860] So this is the, value in the dataset that will split

[00:37:58.460] The first 50% of data, again, into two parts, So, 25% and another 25%.


### Segment 36 - Tian WU (00:38:09.900)

[00:38:09.900] For example, for this data, we know that for these highlighted values, These are the first, like.

[00:38:17.830] 50% of the data, right? 13 of them.

[00:38:22.980] And then the value sitting in the middle will be the 7th data point.

[00:38:32.460] So in total, we have 13 data points.

[00:38:36.330] And the seventh data point will split the certain data points into… there are six, data points.

[00:38:46.300] Before, there's 0.57.

[00:38:49.100] And another 6 data points after this 0.57.

[00:38:54.980] Within the first half, of this dataset.

[00:38:59.780] So then the Q1 value will be 0.57.

[00:39:05.540] Whereas, similarly, for this Q3, we focus on the, the median of the Later, 50% of the data.


### Segment 37 - Tian WU (00:39:17.270)

[00:39:17.270] So here is the later 50% of our data.

[00:39:21.750] And we just count the 7ths, 1, 2, 3, 4, 5, 7.

[00:39:29.500] So this… this 1.64 will split

[00:39:35.180] The later 13 data points into two parts.

[00:39:40.290] 6 before it, and 6 after it.

[00:39:43.930] So this is the, Q3.

[00:39:47.900] And with this, 5… point, summary statistics, we can decide where the box is.

[00:39:56.350] So if I scroll down a little bit.

[00:40:01.260] You can see that on the right-hand side of this figure is box and whisker plot.

[00:40:07.390] In total, there are 26 values, all are kept as two decimal places.


### Segment 38 - Tian WU (00:40:14.030)

[00:40:14.030] The median is shown by this green line. The median is 0.8.

[00:40:20.360] So you can find the corresponding value here.

[00:40:23.730] And for the edge of the box.

[00:40:26.310] here is the value of Q1.

[00:40:29.060] So we calculate the Q1 is 0.57, This value is around 0.57.

[00:40:38.990] And the upper edge of this box The value is 1.64.

[00:40:44.700] So here.

[00:40:45.870] The corresponding value on the y-axis is 1.64.

[00:40:53.290] And we also have this minimum and maximum value, so the minimum value is 0.15, which is the end of this whisker.

[00:41:04.310] Whereas… The maximum is 4.85, It is flying out of the, the whisker on the top.


### Segment 39 - Tian WU (00:41:15.310)

[00:41:15.310] So then, how do we decide which values are flying outside of the range?

[00:41:22.600] Well, this is decided by calculating the so-called inner fence, So the inner fence.

[00:41:32.810] depends on the IQR, where the IQR is the Q3 minus Q1.

[00:41:41.600] In this graph, the IQR represents the height of this box.

[00:41:47.460] Right, because here, this value is Q3, and this value is Q1.

[00:41:54.270] So if IQR equals to Q3 minus Q1,

[00:41:58.760] It represents the height of the box.

[00:42:03.020] And the lower fence is calculated by the IQR minus 1.5.

[00:42:10.030] times… Sorry, Q1 minus 1.5 times IQR.

[00:42:16.910] So the formula It's shown in the code.


### Segment 40 - Tian WU (00:42:22.060)

[00:42:22.060] Here, for these three lines.

[00:42:24.740] Because there's no,

[00:42:27.580] predefined formula to calculate the IQR and also the so-called lower and upper fans, so we have to manually calculate these values.

[00:42:43.980] So previously, we have calculated the value of Q1 and Q3, and we also know how… how tall that box is.

[00:42:52.370] So we can just substitute the value and get the inner lower fans and inner upper fans.

[00:43:03.320] So, after calculation, we found the lower fence is negative 1, and the upper fence is 3.2,

[00:43:11.070] As long as the data point

[00:43:13.790] Is lying out of the range.

[00:43:18.000] From negative 1 to 3, then we will define the data points as outliers.

[00:43:26.520] In our dataset, There are 3 values.


### Segment 41 - Tian WU (00:43:31.160)

[00:43:31.160] That are greater than this upper fence.

[00:43:34.450] So you will see the corresponding three data points.

[00:43:38.820] Flying out of the range of this box.

[00:43:42.490] And whisker plot.

[00:43:45.870] And the… the end of this whisker

[00:43:50.010] Will… will be the largest value in our dataset, which is not ex… exceeding the upper fence.

[00:44:00.720] So here, the, the end of this edge is, like, 2.15.

[00:44:09.230] And as I mentioned, this box plot is used to visualize.

[00:44:16.430] First of all, must be the continuous variable.

[00:44:20.410] And also, we can use this box plot to have


### Segment 42 - Tian WU (00:44:27.180)

[00:44:27.180] An intuitive understanding of the distribution of the data points.

[00:44:33.440] For example, we know that there are some extreme values on the… on the large value.

[00:44:40.520] So there must be certain extreme values.

[00:44:43.870] For… for large values.

[00:44:47.320] Correspondingly, on the left-hand side, I plot the histogram.

[00:44:51.400] Which… Divide the range of this dataset into different intervals.

[00:45:00.350] and then I count the number of Values fall into different intervals.

[00:45:07.300] So, for example, here, I think this is around 0.3, so from 0.3 to 1.2, For… for the value.

[00:45:19.180] In our data falls into that interval.

[00:45:23.780] we count the number of values. Say, in total, there are 16 such values.


### Segment 43 - Tian WU (00:45:30.500)

[00:45:30.500] Then we have a, a bar.

[00:45:34.330] Here.

[00:45:35.900] And then we count the number of, values falls between one point 2 to 2.1.

[00:45:44.550] And it turns out that there are 6 of them, so we have the second bar, so on and so forth.

[00:45:50.680] And it is indeed that we found there is a bar, so there are 3 values.

[00:45:57.670] falls between, like, 3.8 to 4.7.

[00:46:05.820] So there are, three values.

[00:46:09.730] Which are really large.

[00:46:12.220] So that corresponds to this outliers on this box plot.

[00:46:17.720] And also, we can pay attention to the distance between Q1 and median versus the distance between median versus Q3.


### Segment 44 - Tian WU (00:46:31.620)

[00:46:31.620] We know that in this box.

[00:46:35.600] There are 50% of the data.

[00:46:38.260] Right, the middle 50% of the data.

[00:46:42.580] But for the lower 25%, Their range is relatively small.

[00:46:49.940] Compared to the range of the other 25%.

[00:46:55.790] So this means that Starting from this median level.

[00:47:01.530] The range of the next 25% of the data is Bone.

[00:47:07.360] Larger.

[00:47:09.190] Compared to the previous 25%.

[00:47:13.100] So… If we look back into the histogram, this is reflected as a,


### Segment 45 - Tian WU (00:47:22.200)

[00:47:22.200] sliding. It's like a slide shape in this histogram.

[00:47:27.370] So on the left-hand side, the distance is relatively short.

[00:47:32.440] Whereas, on the right-hand side, the, the distance is…

[00:47:38.850] It's larger for same 25% of the data.

[00:47:42.970] So you would imagine that if we can, have more data.

[00:47:48.910] So that the histogram will become smoother, then here will be a, here will be a, peak, and then gradually the shape will slide down.

[00:48:03.320] And given that there are some

[00:48:05.800] Large values on the right-hand side, there will be a long tail.

[00:48:10.140] Extending to the right.

[00:48:13.260] So with the tail on the right-hand side, this is called a scale to the right shape of the distribution of this dataset.


### Segment 46 - Tian WU (00:48:22.420)

[00:48:22.420] So roughly, we can see from this, box plot.

[00:48:27.600] About, whether there's an outlier.

[00:48:31.960] And the range of most of the data, and also, somehow, the distribution of the data points.

[00:48:41.510] I think this shape is a bit like when we discussed about the, the salary…

[00:48:48.760] So we know that, there are many super-rich people in Hong Kong.

[00:48:54.160] And if we calculate the average salary of all the people in Hong Kong.

[00:49:00.090] The average will be inflated because of those very rich people.

[00:49:05.610] Right.

[00:49:07.720] So, the mean value, the average salary, will be… Extract to the right.

[00:49:15.170] Due to those very rich people.


### Segment 47 - Tian WU (00:49:18.450)

[00:49:18.450] But for most of the people, if we consider about the median.

[00:49:22.810] The median level of the salary, like, 50% of the people, their salary will be less than this amount.

[00:49:31.400] And the remaining 50th percent will be greater than that amount.

[00:49:35.890] So this… Media will be…

[00:49:39.900] Smaller than the average, than the mean value, if there are some very large value on the right-hand side.

[00:49:49.620] Because median is not that sensitive to the extreme values.

[00:49:55.730] or the outliers, because it's considered the center. It cuts the data points, in the middle.

[00:50:04.070] Whereas for the mean value, when we calculate mean, we need to Sum over all the points.

[00:50:10.990] The value of all the points in all the data points, and then divide it by the total number of data points.

[00:50:18.630] Then, this mean value will be, Dragged to the right.


### Segment 48 - Tian WU (00:50:25.710)

[00:50:25.710] because of these extremely large values. So we observe this mean value sitting

[00:50:32.150] At the right-hand side of the median value.

[00:50:36.470] Or if you translate to the box plot, then it is above.

[00:50:40.960] The, median value.

[00:50:45.260] So hopefully, with this example, you have a better understanding of this box and whisker plot.

[00:50:53.890] And, you could use all this visualization under appropriate circumstances.

[00:51:04.530] Okay, I think maybe we take a 10-minute break, and if you have any questions, you can just send message in the chat box.


### Segment 49 - Simon Wang (00:51:19.860)

[00:51:19.860] So while we're taking a break, if anyone cannot have access to the Google Drive folder I shared in the individual WhatsApp group, just send your Gmail account to the group.

[00:51:33.620] And you know, actually your group members should be able to help you, invite you over to the folder, but you need my help, you can also, tag me and let me know.

[00:51:51.040] And also, if you,


### Segment 50 - Simon Wang (00:51:54.940)

[00:51:54.940] need help regarding the API key, also let us know. I think after, you know, after the break, Talia will talk a bit more about simulation, and then we're going to, have the in-class, exercise.

[00:52:11.750] And I'm going to set up some breakout room, so the…

[00:52:18.210] group members of each group can go to the breakout room, and, you can talk there, you can actually have a meeting about your project while you're doing the in-class exercise. So…

[00:52:29.860] Because next week, we're going to have small group meetings,

[00:52:35.790] We're going to provide more instructions in terms of the arrangement, But,

[00:52:40.880] Next week will be very critical, because you need to make some progress over the… over your own project, and you have to decide how you want to approach the government to collect information.

[00:52:52.320] So, and also this is the week before the public holiday, and you want to think about how you want to collect your data. So, so a lot of decisions will have to be made,

[00:53:04.640] Hopefully before or during.

[00:53:06.880] the group meetings next week. So I think we need to kind of… in addition to learning about the models, we need to start thinking about how to apply the models and tools to our projects.

[00:57:55.240] Right, another quick, message about, about Gihub.


### Segment 51 - Simon Wang (00:58:01.690)

[00:58:01.690] is that since you already took some time and efforts to learn about GitHub, VS Code, and everything, I would encourage you to actually apply for the GitHub education, because, once you

[00:58:19.010] get the GitHub education, eligibility, you will be able to enjoy some, GitHub Copilot Agent

[00:58:29.350] services, which is usually premium services that you have to pay, but if you've got student benefits, then you can use it a little bit more for free.

[00:58:41.200] At some point, we're going to talk about that.

[00:58:44.620] Well, we don't want to overwhelm you with all kinds of technical,

[00:58:51.140] details, but, I think the agent is going to,

[00:58:56.560] you know, give you a lot of, opportunities and, you know, help. So I would encourage you to look into that, but you have to apply for the education benefit first.


### Segment 52 - Tian WU (01:01:01.490)

[01:01:01.490] Okay, so maybe let's resume.

[01:01:04.810] So Simon just mentioned about the GitHub education. If you log in into your GitHub account under this Billing and Licensing.

[01:01:15.790] education benefits, you can go to this GitHub education page to submit an application. So on average, it will take around 5 days to process your application.


### Segment 53 - Tian WU (01:01:31.680)

[01:01:31.680] Okay, so regarding this box and whisker plot, if you ask the AI's help to generate this plot based on certain data, then the plot will be directly out.

[01:01:44.420] So you don't have to actually consider all of these details.

[01:01:48.360] But the reason I explain it is to hopefully help you to have a better understanding of how this is plotted out.

[01:01:58.280] And another point is that if you would like to change the setting of the code.

[01:02:04.580] Say, if you want to plot 30 data points, generate 30 data points rather than 26,

[01:02:11.770] Of course, you can tell the AI assistant to help you to modify the code.

[01:02:19.140] And you actually don't have to copy and paste, because there is apply to this notebook.

[01:02:25.290] So once you click this, So the corresponding, code will be

[01:02:33.180] modified automatically, so you can see the old version with 26, and the new version with 30. So just click keep, if you think everything's fine, just click keep, so that it saves you the copy and paste. You can

[01:02:47.650] Directly apply the modified code to the old version of the code.


### Segment 54 - Tian WU (01:02:54.740)

[01:02:54.740] Okay, so this is a tip.

[01:02:58.440] Okay.

[01:03:00.530] So then, I still have some last words about the, requestion?

[01:03:11.550] Yup.

[01:03:14.100] So last time, we mainly talked about the linear regression, and our purpose is to try to use our data to estimate the values for this beta zero, this intercept, and the slope term, the beta 1.

[01:03:31.930] And that is the case when the response is a continuous response.

[01:03:39.780] Which means Y should be a continuous variable.

[01:03:44.240] But in reality, it is not always the case, right?

[01:03:48.160] In our questionnaire, the response variable is actually categorical, from the strongly opposed to strongly support.

[01:03:59.110] In that case, it is not that appropriate to apply the linear regression, because it already violates one of the assumptions of the linear regression for distribution of the Y, or for this error term.


### Segment 55 - Tian WU (01:04:15.740)

[01:04:15.740] So, based on different types of responsible variable.

[01:04:20.090] If the response variable is binary.

[01:04:23.030] Like, when it can only take value of 0 or 1,

[01:04:27.550] We will have the so-called logistic regression, And if Y is categorical, Especially…

[01:04:36.620] It's an ordinal categorical response, just like

[01:04:41.640] in our questionnaire is from strongly opposed to strongly support

[01:04:46.710] Then it is more appropriate to use the ordinal regression.

[01:04:51.850] Because not all of you will, will make use of, regression, because, as mentioned, regression is only,

[01:05:02.480] Appropriate to be used to model the relationship between a dependent variable and one or more independent variables, assuming a linear relationship.

[01:05:13.150] So if the question type is.


### Segment 56 - Tian WU (01:05:15.670)

[01:05:15.670] We want to explore the relationship between the response and some potential influence of factors, then linear regression might be a useful tool.

[01:05:26.610] But not all of you will use this.

[01:05:30.000] So I will not, spend more time to talk more about the details of logistic regression and the ordinary logistic regression.

[01:05:40.930] But later, if your group project will make use of regression models, then we can, in a small group.

[01:05:51.060] I will talk more about this, correct interpretation of the, the parameters for logistic regression and ordinary logistic regression model.

[01:06:04.570] So that's the final words for the regression models.

[01:06:09.680] And then, finally, we can start with the simulation.

[01:06:18.380] So this is our second,

[01:06:23.860] This is our second case study.

[01:06:27.150] The topic is to evaluate the efficiency of the bus road adjustments. City bus number 56.


### Segment 57 - Tian WU (01:06:34.560)

[01:06:34.560] Thanks.

[01:06:35.910] So here comes the structure of the case study.

[01:06:38.900] We'll first briefly talk about the background of this proposal of adjusting the bus frequency and road.

[01:06:48.530] And also, briefly introduce the simulation design.

[01:06:53.370] And look into the random component in the simulation, and how we interpret the results, and correspondingly, how this study will help generate certain questions that we can acquire with the transport department.

[01:07:10.130] Then we will have the in-class exercise.

[01:07:15.870] So, background.

[01:07:17.970] Actually, every year, this is an annual exercise for the franchise, the bus companies.

[01:07:25.550] to submit these bus road planning programs to the Transport Department.

[01:07:31.700] So… Do you know how many, franchise the bus companies in Hong Kong


### Segment 58 - Tian WU (01:07:43.070)

[01:07:43.070] You can type in the chat box.

[01:07:50.640] 2?

[01:07:55.960] Actually, there are 4 bus companies. So the franchise, the buses, including the city bus, the Colon Motor Bus.

[01:08:04.230] Long Wind Bus and New Lentell Bus. In total, there are 4 franchise bus companies in Hong Kong.

[01:08:12.820] And after they proposed this road change to the Transport Department.

[01:08:18.430] The department will review the proposal and consult with relevant district councils.

[01:08:24.550] Particularly for major changes, because that will affect the residents in the district.

[01:08:31.430] So they will, consult the, district councils, About the adjustment.

[01:08:39.069] Then, this proposal will be implemented, often begins on a temporary basis.

[01:08:45.859] Following up to 24 months of operation without permanent legislative changes.


### Segment 59 - Tian WU (01:08:53.359)

[01:08:53.359] And if this change is determined to be a permanent change, Then, legislative procedures are required.

[01:09:03.130] When the road changes need to be made permanent beyond the 24 months temporary period.

[01:09:09.270] So that's the overall flow of… from proposing the road change to, finally, we have certain legislative procedures.

[01:09:21.229] And in our case study, we will focus on city bus number 56,

[01:09:26.319] So it is, operating in the North District.

[01:09:30.490] So you can actually find that this, proposal is discussed in the committee meetings in the, North District Council.

[01:09:42.270] And in this proposal, it states the criteria for increasing the buzz frequency.

[01:09:50.910] Specifically, our case is, cited from the 2024 to 2005.

[01:09:58.070] This bus road planning program.

[01:10:01.360] It says that for individual bus roads, if the passenger load factor reaches 90% during the busiest half hour.


### Segment 60 - Tian WU (01:10:11.180)

[01:10:11.180] And 75% during the busiest hour of peak periods.

[01:10:17.950] Or 60% during the busiest hour of off-peak periods.

[01:10:24.300] Then, the department and the franchise, the bus company, will consider increasing the service frequency.

[01:10:32.830] So this is written as the criteria for increasing bus frequency.

[01:10:38.490] But… I think…

[01:10:42.490] here, sorry that I cannot find the Chinese version of this, this proposal. It seems that only the traditional Chinese version is provided.

[01:10:52.450] But for this 56, Regarding the, capacity of passengers, It says that in the

[01:11:02.330] In the busiest one hour, The passenger load factor is 32%.

[01:11:10.170] So this is before the adjustment.

[01:11:13.520] They will make, adjustment of the frequency of 56, so that the existing capacity.


### Segment 61 - Tian WU (01:11:23.690)

[01:11:23.690] will be improved.

[01:11:26.610] But it's a little bit weird that we found that for this bus number 56,

[01:11:31.730] Even before the adjustment, the so-called passenger load factor is only 32%.

[01:11:40.400] So then that leads to the question.

[01:11:44.480] It is unclear, first of all, it is unclear how is this passenger load factor is defined.

[01:11:52.500] So if we only consider those, stating passengers.

[01:11:56.890] Then that will be the seed utilization rate.

[01:12:00.360] Like, we use the number of people.

[01:12:03.650] on the bus.

[01:12:05.610] Divided by the capacity, or the number of seats on the bus.


### Segment 62 - Tian WU (01:12:11.040)

[01:12:11.040] Then we can have this, seed utilization rate.

[01:12:17.480] Or, it can be, like, we use the number of people on the bus.

[01:12:22.130] To divide the total capacity of a bus.

[01:12:25.870] Including… In those standing spots.

[01:12:30.120] So then, in this proposal, it is not clear exactly how this passenger load factor is defined.

[01:12:36.660] Which way?

[01:12:38.230] This is calculated.

[01:12:41.040] And specifically, for this number 56, when the business hour occurs.

[01:12:48.670] So I bet for a different, bus road.

[01:12:52.550] The busiest hour will be different.


### Segment 63 - Tian WU (01:12:55.270)

[01:12:55.270] Right, but it is not listed here.

[01:12:58.350] It only lists the, the frequency of the bus during the busiest hour, but it does not mention when exactly the busiest hour occurs.

[01:13:08.850] Also, we only have one single number for this passenger load factor.

[01:13:16.760] And we… by imagination, we… we… we can…

[01:13:21.890] We can see that for different stops.

[01:13:24.940] The seed utilization rate will be different.

[01:13:29.420] Say, for those bus stops, which are near the MTR station.

[01:13:35.270] If it is before the MTR station, I would expect that

[01:13:39.270] The seed utilization rate will be high because

[01:13:43.080] I would bet people taking this bus to go to the MTR station. And after the bus arrives at the MTR station, people get off the bus.


### Segment 64 - Tian WU (01:13:53.250)

[01:13:53.250] And then the seed utilization rate will decrease.

[01:13:57.710] So for every stop, these numbers should be different.

[01:14:02.800] And also, For different time period.

[01:14:06.470] As is mentioned, there are business hours, right?

[01:14:09.470] So for different hours, these… Seat utility rate… utilization rate should be different.

[01:14:15.900] Say, during the morning hours, during the lunch hours, It should be certain variation.

[01:14:22.850] So then, how exactly this single number is calculated?

[01:14:27.020] is not clear.

[01:14:29.750] And also, how an increase in bus frequency is justified.

[01:14:34.370] Given… These percentages is very low, actually.


### Segment 65 - Tian WU (01:14:40.240)

[01:14:40.240] Comparing to the criteria in the same document, it says… it says that When this number reaches…

[01:14:48.050] 90%, then the company and also the transport department will consider increasing the service frequency.

[01:14:56.960] There are many questions.

[01:14:58.880] After we reach this proposal.

[01:15:03.460] So specifically, Originally, the, city bus number 56, the road is from

[01:15:11.930] the road is the, the… represented by the blue line. Blue… blue curve.

[01:15:19.520] So this is from… turn on to so-and-so.

[01:15:25.150] this blue… Curve.

[01:15:29.370] And it turns out that In addition to the frequency change, the rate of this, this,

[01:15:36.080] Buzz also changed.


### Segment 66 - Tian WU (01:15:38.660)

[01:15:38.660] So now it is the, the rotis represented by this red dashed line.

[01:15:44.710] So, visually, it's the distance of the, overall overall distance is increasing.

[01:15:54.630] So we can see some key summaries of the

[01:15:58.560] Of this bus before and after the adjustment.

[01:16:04.020] So before, the, adjustment…

[01:16:08.730] The total distance for the forward direction from Timmun to Shenzhou is 26.9 kilometers, whereas after adjustment, the distance is longer.

[01:16:21.220] Whereas for the service time, it is increased by adding this afternoon to night session.

[01:16:28.520] Plus the weekends.

[01:16:32.100] And the hard way, which is the frequency of the bus.

[01:16:36.060] So, previously, before adjustment, in one hour, there will be 30, there will be 2 buses.


### Segment 67 - Tian WU (01:16:44.240)

[01:16:44.240] Whereas for the proposed change, which is now, in action, it's like in one hour, in the morning sessions.

[01:16:53.460] There will be 3 buses in 1 hour.

[01:16:57.680] Although the road is different, the number of stops is kept the same.

[01:17:03.960] Whereas for the return direction, the overall distance increased.

[01:17:08.450] The overall service time is increased.

[01:17:11.060] Like, adding the, afternoon and night session, plus the weekends.

[01:17:16.930] The frequency is kept the same, and the number of stops increased.

[01:17:22.430] So that's the overall, background for this bus.

[01:17:29.270] And our objective is to develop and analyze a simulation of the bus road 56 operations during the morning.

[01:17:38.750] Using field data, and also the estimated arrival times.


### Segment 68 - Tian WU (01:17:43.320)

[01:17:43.320] It's called ETA, from the Data Gulf of Hong Kong.

[01:17:48.630] So pay attention that this bus starts service after 9.

[01:17:54.880] So I think this is already different from the peak hour we usually define.

[01:18:01.380] If we consider when the students go to school and people go to work, then usually the peak hour will be, like, from 7, or even from half past 6.

[01:18:11.740] But for this boss, It does operate.

[01:18:15.440] ads.

[01:18:17.100] At least after 9 o'clock.

[01:18:22.040] So we want to test, with the change of the frequency and also the bus route.

[01:18:29.300] How would this seat utilization rate change using the simulation method?

[01:18:35.740] And then we can provide the evidence-based policy inquiries to the transport department.


### Segment 69 - Tian WU (01:18:46.800)

[01:18:46.800] So recall that, we introduced this

[01:18:52.630] If you have any comments, you can maybe type in the chat box.

[01:18:58.310] So we talked about this simulation design in the, first class.

[01:19:04.140] We said there are two tools will be introduced. The first is simulation design, and the second is regression.

[01:19:11.380] So, simulation is about mimicking complex systems, Normally, over time, using logic, Maths and computers.

[01:19:20.890] So today, we will have a, kind of, intuitive understanding of what this means.

[01:19:27.340] And simulation is an experimental process. We run and rerun the model many times under different scenarios to predict the system behavior and evaluate performance under each scenario.

[01:19:41.450] Previously, I have shown this, simulation visualization.

[01:19:47.180] So, we have the, clock, which is…

[01:19:51.970] Record… which is recording the time passed by.


### Segment 70 - Tian WU (01:19:55.970)

[01:19:55.970] And say, at 9-10, the first bus set out.

[01:19:59.930] And for each station, there will be passengers queuing.

[01:20:05.300] And of course, we will have the passengers alight the bus, so the number of passengers on the bus will not keep increasing. So at some point, the number of passengers on the bus will decrease.

[01:20:21.000] So this is the, visualization of the simulation. So we can have a real-time

[01:20:28.500] calculation of the utilization rate by different bus stops. So this will keep changing with the clock time past.

[01:20:39.270] So then, let's see how this is, implemented.

[01:20:50.140] So, in our simulation, There are 3 random components.

[01:20:56.460] And this will, these three random components will affect, the seed utilization rate, which is the KPI we focus for this

[01:21:09.460] Simulation.

[01:21:13.210] So to calculate the seat utilization rate, we need to count the passengers on bus at each stop.


### Segment 71 - Tian WU (01:21:21.250)

[01:21:21.250] Right.

[01:21:22.790] But this number is affected by this three components.

[01:21:29.910] The first is the travel time between each pair of stops.

[01:21:36.420] So I said here, the travel time between each pair of stops is random.

[01:21:42.460] This means that if we observe the bus, Starting from stop A, driving to stop B,

[01:21:51.050] This time will be different if we observe it in different time… at different times.

[01:21:57.440] So for day one, I…

[01:22:00.310] I use a clock to, record the traveling time from A to B. It's 10 minutes.

[01:22:08.150] And for day 2, it might be 10 minutes plus 30 seconds.

[01:22:13.990] And the next day, the day 3, will be 9 minutes and 45 seconds.


### Segment 72 - Tian WU (01:22:20.400)

[01:22:20.400] So every time when we try to measure the traveling time between each pair of the stops, it will be slightly different. It is not a constant.

[01:22:31.640] So in this case, we can say that this component is ran…

[01:22:35.930] So for those, say, traffic jams.

[01:22:40.320] then the travel time between stop A and B will be very, very long.

[01:22:45.860] Right? Whereas, if for one day, if the driver, drives the bus, Very fast. Then…

[01:22:54.240] The traveling time will be quite short.

[01:22:57.650] And this time will also affect the number of people waiting at the stop B.

[01:23:06.690] Suppose there is a traffic jam, so it takes super long time to drive from A, stop A to stop B, then we would expect that the number of passengers waiting at stop B will be more than the usual case.

[01:23:23.940] When the buzz just, Drive in an ordinary speed.

[01:23:31.750] So, the number of waiting passengers at stop B is also random.


### Segment 73 - Tian WU (01:23:38.230)

[01:23:38.230] And also, at each stop, the number of passengers getting off is also random.

[01:23:43.860] So, say if we, take that bus, and we take that bus for several times.

[01:23:51.090] We count the number of people who get off at bus stop B.

[01:23:56.360] But every time this number will be slightly different, it cannot be… always be the constant, like, every time it's 5 people who are getting off.

[01:24:05.240] Usually, there will be certain variation, like, 3 people today.

[01:24:10.480] 5 people next day, 4 people on day 3, something like that.

[01:24:16.520] And actually, for this random component, we can use the random variables to describe their behaviors.

[01:24:29.200] So first, it's about the travel time.

[01:24:33.040] The bus travel time between each pair of the stops is modeled as a random variable.

[01:24:39.330] Drawn from a normal distribution.


### Segment 74 - Tian WU (01:24:43.480)

[01:24:43.480] So we know for normal distribution, It's a bell-shaped, It's symmetric.

[01:24:51.730] And the probability that the, if we regard the, maybe let me… That me… A lot.

[01:25:07.530] Let me change the device.

[01:25:24.860] Okay, so for normal distribution, Suppose this is time t.

[01:25:32.850] This is… F15.

[01:25:39.450] So this, travel time, we regard it, follows a normal distribution.

[01:25:46.940] Say the traveling time from stop A and stop B On average, it's 10 minutes.

[01:25:53.930] So the probability that the traveling time is between Baby.

[01:26:04.250] Between here and here.

[01:26:07.210] So suppose this is, like, 9.


### Segment 75 - Tian WU (01:26:12.040)

[01:26:12.040] 2… This is 10.8 minutes.

[01:26:16.850] The probability that the traveling time is between 9.2 to 10.8 minutes the… the probability.

[01:26:25.680] is very high. So you can see the area is very large.

[01:26:30.370] Compared to the case where the driving time between, say, 11 to 12,

[01:26:38.650] Then this variability is very small.

[01:26:43.500] So we can use this, normal distribution to…

[01:26:49.460] to describe the traveling time. So most of the time, the traveling time will be between, say, 9.2 to

[01:26:56.860] 10.8.

[01:26:59.950] Then, with the mean, which is the 10 minute here.

[01:27:04.200] And the standard deviation, so suppose this represents the, 3 standard deviation. Here is 0.8, then I have roughly, this is, like, 0.2…


### Segment 76 - Tian WU (01:27:18.290)

[01:27:18.290] Sixth?

[01:27:22.960] Right.

[01:27:23.880] So I have this standard deviation, Estimated from sample data.

[01:27:31.710] Specifically, we use the API, we can collect the estimated time of arrival.

[01:27:39.110] At each stop for 30 trips of bus number 56.

[01:27:45.490] So I know… from this, ETA data, so this is the real-time, arrival time.

[01:27:55.690] a record the number it takes from stop A to stop B for 30 times.

[01:28:05.160] And I use the average of the travel time of the 30 times as the mean.

[01:28:12.190] Of my normal distribution.

[01:28:15.990] And I also use the standard deviation of this 30, traveling times as the standard deviation of my normal distribution.


### Segment 77 - Tian WU (01:28:27.960)

[01:28:27.960] So then, in each simulation, I can draw a random number from this specific normal distribution.

[01:28:36.570] as the travel time from stop A to stop B.

[01:28:41.800] So every time, the travel time will be different.

[01:28:45.590] Because it is drawn from a normal distribution.

[01:28:49.880] But they are drawn from the same distribution.

[01:28:52.750] Where the mean and standard deviation is estimated based on, the, Via real-time data.

[01:29:05.030] And then, we calculate the mean and standard deviation of travel times between each pair of stops.

[01:29:11.890] For each simulation run, we sample travel times from the corresponding normal distributions.

[01:29:17.360] To represent the bus travel times between stops.

[01:29:22.120] So if there are different pair of stops.


### Segment 78 - Tian WU (01:29:26.560)

[01:29:26.560] So for this pair of stops, each time I will draw a, travel time, from…

[01:29:35.590] A normal distribution with same mean equals to 10, variance equals to 0.3.

[01:29:43.030] Whereas for the next pair of bus stops.

[01:29:48.530] Because the distance between these two might be different from the previous pair of stations.

[01:29:55.340] So, I may need to draw the traveling time from a normal distribution with, say, mean value 15.

[01:30:03.010] And 0.2, something like that.

[01:30:06.780] So for each pair of There's bus stops.

[01:30:11.420] I would draw this travel time from normal distribution

[01:30:16.440] whose mean and standard deviation is estimated from the ETA data.

[01:30:24.780] If we implement it in code, it will be, the random.normal. We use numpy mp.random.normal.


### Segment 79 - Tian WU (01:30:34.620)

[01:30:34.620] These command will help us to draw the random numbers from normal distribution with specific mean and specific standard deviation.

[01:30:46.820] So after we know the traveling time.

[01:30:49.710] Between each pair of the bus stops.

[01:30:52.500] And we know that this will affect the number of waiting passengers at stop B.

[01:30:58.450] Because, as mentioned, the longer the traveling time, the larger number of waiting passengers.

[01:31:07.140] And this number of waiting passengers is often used… is often described by this so-called poison distribution.

[01:31:19.040] So Poisson distribution is a discrete distribution.

[01:31:25.270] So it can only take… It can only take value, like, 0 or 1 or 2 or 3.

[01:31:32.910] And it can be used to describe the number of events happened within a unit's time interval.

[01:31:42.910] Say, we want to describe the number of passengers, waiting at a stop.


### Segment 80 - Tian WU (01:31:50.120)

[01:31:50.120] Or the number of customers go into a supermarket, So this is… about counting.

[01:31:58.050] The number of events happened.

[01:32:01.890] And if we know that it follows a poison distribution, then one of the key parameters

[01:32:09.560] So parameter is just like the mean and standard deviation for a normal distribution.

[01:32:16.230] For poison distribution, the key parameter is lambda.

[01:32:21.120] It represents the average number of occurrence in the time interval.

[01:32:28.990] So suppose we know that if lambda equals to 4, It means, on average, In one hour.

[01:32:38.180] There will be 4 people waiting at bus stop.

[01:32:43.810] Then, we can calculate the corresponding probability when there is, like, only

[01:32:51.750] Zero people waiting at the bus stop.


### Segment 81 - Tian WU (01:32:55.990)

[01:32:55.990] Then we know the average number is 4, then…

[01:33:01.810] If we calculate the probability of zero passengers.

[01:33:05.740] Or waiting at that bus stop, the corresponding probability will be very low.

[01:33:11.580] And it is also, makes sense that if the average number of passengers waiting at the bus stop

[01:33:19.190] Within the unit time, interval is 4, then the probability that

[01:33:25.690] During that time interval, there will be 5 people who are waiting at the bus stop. The probability of this event will be relatively high.

[01:33:37.020] Because… On average, there will be 4 people waiting there.

[01:33:41.160] And 5 people is close to… to the average, close to the… Four people.

[01:33:48.890] So then the chance of There are 5 people waiting there, this probability should be relatively high.

[01:33:57.570] So you can observe this, graph.


### Segment 82 - Tian WU (01:34:02.350)

[01:34:02.350] When the average is 4, then the probability of 5 people waiting there is relatively high, whereas

[01:34:10.420] If we know, on average, there will be 4 people waiting there.

[01:34:14.270] The probability that there will be 20 people waiting there, then…

[01:34:19.200] The likelihood of this event will be relatively small.

[01:34:24.800] So that is the shape of this poison distribution.

[01:34:30.210] And then… Just like what we did for the traveling time, we need to estimate the lambda.

[01:34:38.670] The average number of people waiting at different bus stops.

[01:34:45.350] And this can be estimated by the field observation.

[01:34:49.640] Say, now we are at the bus stop 2.

[01:34:52.760] And suppose, imagine that we are on the bus, Starting from stop 1.


### Segment 83 - Tian WU (01:34:59.090)

[01:34:59.090] We start to see how long it takes

[01:35:01.700] To drive from stop 1 to stop 2, And it turns out that

[01:35:07.090] The travel time is 10 minutes.

[01:35:09.620] And at stop 2, there are 5 people waiting there.

[01:35:14.310] This is our first observation.

[01:35:17.690] Then, for the next day, or for the next shift.

[01:35:21.970] The traveling time between stop 1 and stop 2 is 15 minutes.

[01:35:28.280] And then we observe there are 8 people. We are waiting at stop 2.

[01:35:34.140] So we have a record, so on and so forth.

[01:35:38.250] So after we collected this field data.


### Segment 84 - Tian WU (01:35:41.810)

[01:35:41.810] We can calculate the rate for each observation.

[01:35:46.730] So the rate represents the average number of passengers In the time interval.

[01:35:54.600] So you may imagine that the passengers just come, In a uniformly way.

[01:36:02.520] So during this 10 minutes, In total, there are 5 people.

[01:36:08.170] Catch the… Arrive at stop 2.

[01:36:13.350] So this means, on average, for every minute, There are 0.5 people.

[01:36:20.850] Arrived at the stop tool.

[01:36:24.570] Similarly, we can calculate this arrival rate

[01:36:29.130] For, the next few observations.

[01:36:33.080] And then we can take average of these rates


### Segment 85 - Tian WU (01:36:37.220)

[01:36:37.220] As an estimate of the average number of passengers waiting at stop 2.

[01:36:46.490] Say, if we only have these 4 observations on average, for every minute.

[01:36:52.870] 0.51 passengers will arrive at Stock 2.

[01:36:59.640] And with this estimation, for each time of the simulation.

[01:37:04.460] We can draw a random number of passengers.

[01:37:08.830] from a Poisson distribution with lambda equals to this 0.5.

[01:37:17.290] But, of course, we need to time the, time interval of the traveling time.

[01:37:22.810] So this lambda rate is… per minute, How many passengers will come?

[01:37:28.840] And these need to be multiplied by the time interval of traveling from stop 1 to stop 2.

[01:37:39.320] So this is about how we,


### Segment 86 - Tian WU (01:37:42.440)

[01:37:42.440] Simulate the number of waiting passengers.

[01:37:46.610] And then… the passengers must get off somewhere, right? They cannot, like, stay in the bus forever.

[01:37:55.350] There is another distribution, which is called the binomial distribution.

[01:38:00.110] That can be used to describe the number of passengers getting off at each stop.

[01:38:06.900] So for this distribution, you may just regard it as

[01:38:10.940] If we flip a coin for several times, say, 20 times.

[01:38:17.590] And we care the number of times that we get a hassle.

[01:38:23.510] It gets a heads up.

[01:38:25.410] So, say, I do the experiment, I flip a fair coin for 20 times.

[01:38:30.570] Then, for this experiment, it turns out that there are 8 Coins.


### Segment 87 - Tian WU (01:38:36.230)

[01:38:36.230] That are heads up.

[01:38:38.540] So this is one observation.

[01:38:41.180] And we can repeat this experiment.

[01:38:45.510] And the event that we are interested is the number of Heads up, off the coin.

[01:38:52.550] And we record the number of heads up in the sequence of, flip, this coin flipping.

[01:39:00.980] So here, you may just regard those passengers who get off as the coin has a heads up.

[01:39:08.600] So we just… Regarding the total number of coin flipping as the number of people on the bus.

[01:39:18.040] And then we count how many people get off.

[01:39:23.260] So the number of get-offs is the event that we are interested.

[01:39:28.230] And then…


### Segment 88 - Tian WU (01:39:30.590)

[01:39:30.590] The difference between the coin flipping and the passengers get off is that we know for a fair coin.

[01:39:40.470] The probability of having a heads-up is 50%.

[01:39:44.960] Right.

[01:39:46.120] But here, we actually don't know.

[01:39:49.050] How many percent of the people will get off?

[01:39:53.250] And this probability will be different for different stops.

[01:39:59.230] say, for those stops that are near the MTR station, then it's more likely that the passenger will get off at that station, because they want to take MTR.

[01:40:11.730] Whereas for those small stations, then…

[01:40:15.640] Overall, the number of people who get off the bus will be… will be

[01:40:20.310] Will be fewer, will be smaller, right?


### Segment 89 - Tian WU (01:40:25.750)

[01:40:25.750] So then we can estimate the probability of getting off for each stop, again, using the field data.

[01:40:34.650] So we collect data over several days or weeks, and again, we have certain observations for the specific stop.

[01:40:43.620] So for stop 2, originally there are 10 people on the bus.

[01:40:47.710] And it turns out that 4 of them are light.

[01:40:52.000] For the next observation, in total, there are 12 people Riding on the bus.

[01:40:58.440] And at stop 2, 5 of them are light.

[01:41:01.830] So on and so forth.

[01:41:04.130] So we can use these observations

[01:41:07.510] To estimate the probability of a light lighting, For each stop.

[01:41:16.730] Using this example, at stop 2,


### Segment 90 - Tian WU (01:41:20.530)

[01:41:20.530] The probabilities of getting off will be 0.4, 0.42, 0.4.

[01:41:27.930] These are all the observations for a specific stop, Then we can take average.

[01:41:34.050] Say we can take average as 0.4 and regard this as the probability of getting off.

[01:41:40.600] For this specific stop.

[01:41:44.750] And later in the simulation, we will draw the number of passengers getting off, from… the pool of…

[01:41:54.660] The number of passengers on the bus.

[01:41:57.760] So these passengers depends on the number of people waiting at stop 2, And also the,

[01:42:07.210] The… the passengers who… Get on the bus at stop 1,

[01:42:13.580] So this is our pool of passengers.

[01:42:16.570] And for this group of passengers, The probability of alighting the bus.


### Segment 91 - Tian WU (01:42:23.580)

[01:42:23.580] Will be the probability that is estimated from the, field observations.

[01:42:31.680] So for all the passengers on the bus.

[01:42:36.130] With the probability of a light.

[01:42:39.750] Being estimated by the field data.

[01:42:42.860] We can draw a random number of how many of the passengers will get off at a specific stop.

[01:42:52.410] So that's the three random components in our simulation.

[01:42:59.610] And to implement this simulation, we will make use of the Python library, which is called SynPy.

[01:43:07.770] So, SimPai is a discrete event simulation framework.

[01:43:12.380] And it is specifically designed to model the system where events happened at discrete points in time.

[01:43:23.010] Then what does an event mean?


### Segment 92 - Tian WU (01:43:26.810)

[01:43:26.810] So the event represents a specific action.

[01:43:30.870] For example, when the bus Start to drive.

[01:43:36.320] Or when the bus arrives at a stop, Or when passengers start

[01:43:42.470] Boarding, and bus departure, a stop after a certain dwell time.

[01:43:49.800] So these are, so-called events happened.

[01:43:55.090] And these events are processed in a chromological order according to their scheduled time.

[01:44:02.920] And only when they occur.

[01:44:05.880] So, say, during the time interval between the bus driving from stop A and stop B,

[01:44:12.990] Even though the time passed, So recall that in the visualization, there is a clock, right?

[01:44:20.490] The time just keep pass, Keep passing, but the event will be paused because there's no event happens.


### Segment 93 - Tian WU (01:44:31.110)

[01:44:31.110] There's no, there's no action that changed

[01:44:36.910] The status of the overall, system.

[01:44:42.170] And only when the event happens, like bus arrives, passenger get on board, when this event happens, then we record the time of this event.

[01:44:55.870] And later in the demo, Jupyter Notebook, you can see a typical Sympi structure, including these four steps.

[01:45:05.470] So, first of all, we will create a simple environment.

[01:45:09.240] So we use this, environment, we use… you will see this command.

[01:45:15.260] And second step is to define a generator function.

[01:45:19.380] So to generate the, the process that we… we are interested.

[01:45:25.520] So we have the bus trip.

[01:45:28.240] And the arguments can include many, many scenarios.


### Segment 94 - Tian WU (01:45:35.740)

[01:45:35.740] So the first must be the environment, we just compute.

[01:45:40.950] And then we can consider, if we run the simulation for many, many times, then we can record this number of simulations, so we can record

[01:45:52.100] This round number.

[01:45:54.570] And also, if there are different bus buses on the simulation, we can record the bus ID, and then track the behavior of different buses.

[01:46:04.950] Then we can also, specify the road configuration.

[01:46:10.010] Say, about the forward direction, it passed through, the bus passed through, those 11 stops.

[01:46:18.370] Whereas at the return direction, it will pass another 10 stops. So we can put the road configuration in this generator function.

[01:46:29.450] And also, save the passenger data. Say how many people get on, how many people get off.

[01:46:36.190] So these are all the possible components or arguments in this generator function.

[01:46:43.310] And also, as mentioned, for the discrete event simulation.


### Segment 95 - Tian WU (01:46:50.560)

[01:46:50.560] For the time gap between two events, we need to pause the process, For those,

[01:46:58.110] Time interval between events.

[01:47:01.400] So we will yield this yield.

[01:47:03.670] Comment, environment time out for, say, the travel time.

[01:47:08.960] For the travel time, because nothing special happened,

[01:47:13.200] We will not, like, use the… the resources.

[01:47:18.620] We, we just… Pause the process, but let the time pass.

[01:47:25.380] Then, we can add the generator function to the Sympi environment. So you will see int.process, you will see this key, function name.

[01:47:36.040] And we put… The defined generator function here.

[01:47:42.620] And then, the last step is to run the simulation and to let the time pass. So, environment.run.


### Segment 96 - Tian WU (01:47:49.890)

[01:47:49.890] So this is how we execute the simulation, by processing all the scheduled events until completion.

[01:47:58.540] And you'll always see this environment.nel.

[01:48:02.780] It means we record the current time when an event happens.

[01:48:08.370] So to have a, intuitive understanding, maybe we go back to the demo drop your notebook.

[01:48:32.290] So, as mentioned, we have this week 4 demo Shook your notebook.

[01:48:41.970] It's called the, Week 4 Devo.

[01:48:50.670] So the first part is just show how to use this NumPy to generate, random variables.

[01:48:59.450] Like, we set a random seed, so every time the random numbers you generate it will be the same.

[01:49:06.250] And it's actually quite simple, just use… numpy.random.normal.

[01:49:12.260] And by defining the,


### Segment 97 - Tian WU (01:49:14.390)

[01:49:14.390] The mean and standard deviation, and how many random numbers you want, you can

[01:49:21.010] Generate the, corresponding result.

[01:49:25.610] And again, we can visualize the simulated random numbers.

[01:49:30.510] So this is normally distributed.

[01:49:33.250] If we plot the, histogram, and also the, box and whisker plot.

[01:49:40.200] So hopefully by now, you, you are clear about the meaning of this fox and whisper plot.

[01:49:47.080] These two should be quite consistent.

[01:49:51.550] And then we can go to this four-step structure to set up a simulation using Simply.

[01:49:57.990] As mentioned, the first step is to create a simple environment, and here we just do the simulation for a fixed traveling time from stop A to stop B.

[01:50:11.280] In this case, we defined the generator function.


### Segment 98 - Tian WU (01:50:15.290)

[01:50:15.290] And we first record the, departure time.

[01:50:20.100] And then the bus will travel for 3 minutes.

[01:50:24.250] And because for the 3 minutes, it's not an event.

[01:50:28.760] We just pause the process and use yield, To record the timeout, And then, after 3 minutes.

[01:50:37.690] The time passes.

[01:50:39.590] The bus arrives at stop speed.

[01:50:42.460] Then we, again, record the current time, which is the arrival time, Then we'll print it out.

[01:50:50.810] And then for step 3, we add the generator function to a simple environment.

[01:50:55.670] So this is environmental process.

[01:51:00.220] If we run it, Oops.


### Segment 99 - Tian WU (01:51:03.850)

[01:51:03.850] I think I should have run the… previous cell.

[01:51:09.760] Yep.

[01:51:11.890] The bus process added to the environment.

[01:51:19.250] And then the step 4 is to run the simulation and let time pass. So if I run it, it says bus departs at time 0, bus arrives at time 3, simulation completed. Finally, the time is 3.

[01:51:35.920] So that is a very simple simulation of

[01:51:40.810] just driving the bus from stop A to stop B.

[01:51:44.800] But later, we can add more elements, as discussed, into this framework.

[01:51:51.120] To, simulate more complicated scenarios.

[01:51:56.060] Let's have a 10-minute break first.

[02:02:34.950] Okay, let's resume.


### Segment 100 - Tian WU (02:02:39.310)

[02:02:39.310] So for this code,

[02:02:42.160] Don't worry that you don't have to start from scratch, you just ask the AI assistant of what kind of simulation you want to have.

[02:02:52.130] and add those random components one by one, and I think, the, GitHub compiler can handle this scale of simulation.

[02:03:04.070] So I will use the next around 10 minutes, 10 to 15 minutes, to finish the demonstration and also the remaining slides.

[02:03:13.000] So previously, we just set the very basic simulation for just a bus traveling from stop A to stop B. Now, we add a random travel time and run the simulation for 100 times.

[02:03:27.340] So instead of a fixed traveling time, 3 minutes, we add certain randomness.

[02:03:35.770] We have a list to store our results of the traveling time.

[02:03:42.150] Then here, we first define the generating… generator function.

[02:03:46.740] And later, we follow the remaining steps.

[02:03:51.520] So now, for the generator function, instead of the environment, we will record the run number.


### Segment 101 - Tian WU (02:03:58.820)

[02:03:58.820] Because we have, we will have 100 simulations, so we need to have a placeholder for the number of simulations.

[02:04:11.040] At the beginning, it's the same. We record the departure time, and then we create random travel time from a normal distribution with mean equals to 3 and standard deviation equals to 0.3.

[02:04:23.540] So this is exactly what we did for the first part, which is the random number generation.

[02:04:30.960] Here, we have this maximum function to ensure that the value we draw from the normal distribution must be positive.

[02:04:40.250] Because this is travel time, it must be non-negative.

[02:04:44.430] But if we really randomly drawn from a normal distribution like this.

[02:04:49.820] Although the probability of drawing a negative value is very, very, very, very small, but still, it is possible.

[02:04:57.670] And to avoid that situation, we use this max function to, to set the 0.1 as the lower bound.

[02:05:06.760] If the travel time is lower than the 0.1, we will use the 0.1 as our travel time.

[02:05:14.500] Then, during the travel time, the process will be paused.


### Segment 102 - Tian WU (02:05:19.510)

[02:05:19.510] And then we record the arrival time and print out that the bus arrived at a certain time.

[02:05:25.990] Then we gradually append our results to the, to the… to the big list about the running number, the departure time, the arrival time, so on and so forth.

[02:05:41.810] So, start from here, we, use a loop, tool…

[02:05:48.550] To implement the 100, simulations.

[02:05:53.020] So, again, step one, create the environment. Step two, we define the generator function, which is the upper part.

[02:06:00.270] And then step 3, we add the generator function to a SynPy environment.

[02:06:05.240] Now here, for this process, we have two arguments, the environment and also the number of simulations.

[02:06:14.270] Then we ask the, the SimPai to help us to execute the simulations.

[02:06:21.860] Then print the result.

[02:06:25.140] And the result will… will look like this. So for run 1, bus departures at…


### Segment 103 - Tian WU (02:06:31.730)

[02:06:31.730] Time 0, and arrivals at times 3.2.

[02:06:36.270] So every time, for every run of simulation, you can see that the arrival time will be different, will be slightly different.

[02:06:44.570] So this time, it's drawn from a normal distribution with mean 3 and variance No, standard deviation, 0.3.

[02:06:55.370] Okay, so if you want to read more results, you can click this scrollable element.

[02:07:02.270] So it will show all the, 100 times of the simulation results.

[02:07:12.170] Now we come back to the slice.

[02:07:16.400] Let me share a screen again.

[02:07:27.480] Right.

[02:07:29.040] So after we implement the assimilation, we can get the results.

[02:07:33.580] So recall that our KPI for this project is the ute, sorry, it's the seed utilization rate. So for each stop, we record the, we, we…


### Segment 104 - Tian WU (02:07:47.020)

[02:07:47.020] Use this box and whisker plot to show the distribution of the… in 1,000 times the seed utilization rate for each stock.

[02:07:59.010] So this is the, the existing scenario.

[02:08:03.190] And the direction is forward, so from Qinmen to Shengshui.

[02:08:08.550] And we can see that with the, driving of this bus setting out.

[02:08:14.810] The seed utilization rate increases, So again, this orange vertical bar represents the median.

[02:08:23.240] from… 12% to around 34%.

[02:08:28.440] And here, for this station, this is Shenzhui MTR exit.

[02:08:35.290] So you can observe there is a drop of the seat utilization rate, which makes sense, because people take bus all along… all along the way to get to the MTR station.

[02:08:47.110] And then, finally, all the passengers get off at the last station.

[02:08:51.650] So for this trip, the median of the seed utilization is around 12 to 34 across different stops.


### Segment 105 - Tian WU (02:09:01.860)

[02:09:01.860] And because, on average, this

[02:09:05.240] Distribution shows a slightly right-skilled, because there are many, outliers on the right-hand side.

[02:09:13.280] So the mean value is expected to be a little bit higher compared to these orange bars.

[02:09:20.650] So if we take average, it will be around… Sirty… 30-something. So, 30-something.

[02:09:29.310] So that is the existing… Utilization rate across these different stocks.

[02:09:37.670] Similarly, we can calculate the median of seat utilization for the return direction.

[02:09:44.370] And these circled 3 stops are new.

[02:09:48.920] But we can still observe them, because the stops are there. We can use the field data, as mentioned, use the field data to

[02:09:56.830] To estimate the traveling time, to estimate the number of people waiting at different stops, and also the number of people getting off the bus.

[02:10:08.860] And we can also, based on certain assumption of the removed stops.


### Segment 106 - Tian WU (02:10:16.120)

[02:10:16.120] So for these two stops, they are no longer there, and we have no way to

[02:10:22.170] Track the historical data of the number of passengers, getting on, getting off.

[02:10:28.770] So these are based on certain assumptions. We may use the number of passengers waiting at the neighboring stops as the number of passengers waiting at those stops.

[02:10:42.330] And regarding the traveling time, we can find the distance of this routine estate to the original bus stop, then have an estimate of the traveling time.

[02:10:57.100] So to generate the before adjustments, we need certain assumptions of the traveling time and passenger flow.

[02:11:06.810] And if the assumptions are correct, then…

[02:11:11.180] Based on the simulation results, the median of the seed utilization rate will be between 18% to 56%.

[02:11:19.490] So comparing to the existing scenario, before the adjustment is done, then the seat utilization rate is indeed higher.

[02:11:30.680] Compared to… compared to the situation when the bus frequency is adjusted.

[02:11:40.110] Similarly, we can calculate or estimate the median of seat utilization for the return direction and before the adjustment.


### Segment 107 - Tian WU (02:11:55.270)

[02:11:55.270] So, the results summary, Is that the adjustment appears to have reduced the overall seat utilization rate.

[02:12:04.180] But with the increase of the frequency of bus, the cost of the bus company must also increase.

[02:12:11.400] Right? So, within one hour, there will be one more bus to… to operate, and there must be the captain to drive the bus.

[02:12:22.000] And also, the… the funeral, will… will be a cost.

[02:12:27.020] So, if we consider the cost, then it is a problem, or it is a question that whether the, the income

[02:12:38.930] Produced by this bus frequency increase.

[02:12:42.570] Whether it can cover the cost.

[02:12:45.110] Of the, frequency increase of the bus.

[02:12:52.650] So then we can, formulate the inquiry to the transport department based on our analysis.

[02:12:59.950] So first, what type of operational and passenger flow data, like the stop level boarding and a light peak


### Segment 108 - Tian WU (02:13:08.130)

[02:13:08.130] And off-peak passenger accounts were collected and analyzed when assessing the rerouting and schedule change for this bus number 56.

[02:13:18.690] So you notice that in our simulation.

[02:13:22.760] Some data are collected by ourselves.

[02:13:25.480] And some of them are estimated based on very limited data.

[02:13:31.020] They say we need to count the number of people waiting there, we need to count the number of people alight the bus.

[02:13:37.180] But whether this work, has systematically done by TD.

[02:13:44.070] As a review of the adjustment of the…

[02:13:47.430] of 50… 56. So this is unclear.

[02:13:51.600] But we can ask whether this type of data is available, whether it is already collected and analyzed.

[02:13:59.550] And second is, what quantitative models or criteria were used to evaluate whether the service modification would maintain


### Segment 109 - Tian WU (02:14:08.550)

[02:14:08.550] Or improve the passenger service quality.

[02:14:11.800] So what exactly criteria they use to evaluate whether this is a,

[02:14:18.750] group, this is a good adjustment. And in what sense?

[02:14:23.780] Say, the city utilization rate decreased.

[02:14:27.780] But on the other hand, from the perspective of the bus company.

[02:14:31.800] So that may increase the cost.

[02:14:34.510] Then, how… what kind of index they use to evaluate whether this modification is, is overall a good move or not.

[02:14:46.220] And also, whether the relevant operational data sets, the consultation summaries, or evaluation models are available for public or academic review.

[02:14:58.390] If these datasets are already there, then can we access to it so that it can save us the time to collect the data by ourselves, and also improve the data quality?

[02:15:12.000] Because…


### Segment 110 - Tian WU (02:15:13.590)

[02:15:13.590] what we can do is just collecting very limited data based on our availability, but if the TD conducted that field study, maybe it is more

[02:15:26.630] systematic, the number of data points will be more than ours.

[02:15:31.620] So that will improve our model parameter estimation, so that it will increase the accuracy of our simulation.

[02:15:42.370] We want to know whether such data is available to be accessed.

[02:15:46.970] And if not, would the TD consider releasing or try to summarize the data based on the code on access to information?

[02:16:00.490] So this is the second, case study.

[02:16:04.300] So hopefully, through this case study, you have a taste of, how we can use simulations to quantitatively measure or predict the system behavior of the index we are interested in here, like the seat utilization rate.

[02:16:22.390] And in your own group project, if your focus is on the public transportation, you may also need to apply similar simulation technique into your study.


### Segment 111 - Simon Wang (02:16:39.000)

[02:16:39.000] Okay, so, so, Talia, maybe, allow me to jump in and, just to…

[02:16:44.510] offer kind of a high-level, summary, especially for students, with limited math background, and, you know, some of the technical details may be a little bit, overwhelming to you, but, I'm…


### Segment 112 - Simon Wang (02:17:00.540)

[02:17:00.540] I've only offered kind of, like, a layman's account on what we're trying to do here. So, basically.

[02:17:07.680] But when we do simulation, we are using, mass models,

[02:17:12.459] to try to approximate and try to get as close as we can an account of the reality, right? And because of the limited amount of data that we have.

[02:17:24.240] it's not possible to… to actually grasp, or to… to actually understand the reality, or have a very precise, descriptive account of the reality. So,

[02:17:37.500] So instead of, trying to get that, we, we use the simulation approach. So that's kind of the general, kind of picture, what we're trying to do here. And as we are using, the math model, of course, we have to select different math models, right? There's the…

[02:17:56.370] The first one, we're talking about using the normal distribution, and then there's the binomial model, and then there's the poison.


### Segment 113 - Tian WU (02:18:05.170)

[02:18:05.170] listening.


### Segment 114 - Simon Wang (02:18:05.570)

[02:18:05.570] model for… for different, scenarios and different kind of, descriptions. So… so that's where we, we probably need some inputs from the experts. We have to consult the, the experts on… on this. But then at the same time, in order to have a, a good

[02:18:25.290] approximation or simulation, we also need some real data, right? So we can't just do simulation without any real data. That's why we have to go to the field.

[02:18:37.020] In fact, the master students who did this project, actually, they went to the site, and they collected some data, like when… how many passengers get off and get on the bus, and some real data we have to collect it.


### Segment 115 - Simon Wang (02:18:52.799)

[02:18:52.799] And with that real data fed into the model, we will have a model that can actually provide the kind of approximation or simulation for us to better understand the reality.

[02:19:06.650] So… so that's why, you know, next week or the week after, you need to also think about whether you can collect some field data.

[02:19:16.830] But one thing we have to acknowledge is that we are very small teams, right? We are doing a course project, so it's not possible for us to do any kind of large-scale data collection. But the government, the government has got much more resources, you know? If they decide

[02:19:34.910] it is important to collect some data and then use the simulation to better understand the reality, to better make decisions. Then they can actually make the decision to collect more data. So that's where the data governance

[02:19:48.770] practices and data governance evaluation becomes very important and relevant here. So our job, you know, when we do our project, is to look at, you know, what data has been collected and curated by the government team, and whether or not this kind of data could be used for simulation.

[02:20:07.200] That can help us better understand the reality. So, most likely, the government team is not necessarily doing that. You know, the data they've got may be very limited, or they've got the data, but they've never done any simulation.

[02:20:22.480] to help them make decisions. Then that's our opportunity to make the argument, to say, look, you know, there's actually a better way to make decisions. So if you got the data, if you collect just a small amount of data with reasonable, you know, resources, then we will be able to

[02:20:41.190] build a model, we're going to do the simulation that can help us to make better decisions. So I hope that you can keep this in mind. And of course, you know, there's the more technical details, and the AI can help you to write the code, to run the simulation, but more importantly, you need to know why. Why are we doing this?

[02:20:59.340] So, so I hope that that can sort of clarify things a bit, but of course,

[02:21:04.460] When… in the context of the specific project that we are working on, then we have to decide which model is the most appropriate and relevant for doing the simulation.


### Segment 116 - Simon Wang (02:21:17.990)

[02:21:17.990] Right.


### Segment 117 - Tian WU (02:21:22.640)

[02:21:22.640] Yeah, I think for the remaining time, we'll work on the in-class exercise, too.

[02:21:27.830] But there are only 3 tasks, so hopefully it's more straightforward than last times.

[02:21:36.230] A tip is that when you use the GitHub Copilot, you can make use of the Ghost test.

[02:21:45.710] If you remember, for example, now you can see my…

[02:21:50.600] You can see my notebook, right?

[02:21:54.220] I put my cursor at the end of the comment, starts with this hash, And if I hit enter.

[02:22:02.690] There will be such so-called ghost text showing up.

[02:22:08.040] So if you think it's okay, then you hit the tab button.

[02:22:15.910] You don't have to, like, ask every question in the chat box.


### Segment 118 - Tian WU (02:22:20.880)

[02:22:20.880] So sometimes the, the ghost attacks is already good enough.

[02:22:34.590] You may consider to use this.

[02:22:36.740] Rather than ask everything to GitHub Copilot using this chat box.

[02:22:57.840] Yep, so after I hit the enter button, some… some… Command just shows up.

[02:23:06.470] If you think it's correct, it is consistent with your requirement.

[02:23:11.330] I said set the random seed at 48, but now it's set as 42, which is not right.

[02:23:18.760] But I can, I can change it.

[02:23:29.080] Yep.

[02:23:30.120] And for 20 times, so we need to generate the, random variables for 20 times, and print… to print it out. So you can…

[02:23:38.370] Modify the, the, requirement, you want the,


### Segment 119 - Tian WU (02:23:45.570)

[02:23:45.570] GitHub Copilot to do using this hash, and then just Say…

[02:23:57.740] I don't know why it keeps generating log normal distribution, but it should be poison distribution.

[02:24:03.220] maybe I set these sentences one by one so that it can perform as what I expect.

[02:24:11.160] Let me play with this.

[02:24:14.210] Oops.

[02:24:20.380] Yeah, I think Simon just set out some rooms.

[02:24:24.920] He's setting some rooms.

[02:24:27.490] for questions, If you need help, you can go into the, specific room, We have, in total.

[02:24:40.540] For, teaching staff.

[02:24:43.950] David.


### Segment 120 - Tian WU (02:24:47.480)

[02:24:47.480] Lili… I think Lily is here.

[02:24:55.270] Yeah, Simon and me. So if you have specific questions about this in-class exercise.

[02:25:02.030] Or any questions regarding the course material, feel free to join the room and ask questions to us.


### Segment 121 - Simon Wang (02:25:11.520)

[02:25:11.520] Right, so, yeah, so there's four rooms, and if any of them, any of us are helping other students, you can either wait, or you can try another room. And what was the deadline of this in-class exercise?


### Segment 122 - Tian WU (02:25:27.800)

[02:25:27.800] So far, I think I set it as… Let me see.

[02:25:44.040] 2… 15.9.


### Segment 123 - Simon Wang (02:25:49.490)

[02:25:49.490] Okay, so because I think… I don't know whether, whether most of the students are at home, you know.

[02:25:56.880] just in case, if they need a bit more time, I think we can be a bit more flexible here, but let's see how… because I think the exercise today is actually not very difficult, so maybe we'll see how it goes.

[02:26:14.980] Okay, so yeah, so I will see you in the breakout room, or if you have any questions, you can also send a message to the WhatsApp group, okay?
