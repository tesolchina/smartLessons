# Simon Wang - Course Instructor Transcript

## Overview
**Content:** Course introduction, logistics, technical setup  
**Generated from:** Chunk 1, Chunk 2 (partial), Chunk 3, Chunk 4  
**Date:** Week 2, GCAP 3226  

---

## Course Introduction

Alright, so for the first two weeks, we're going to record our lecture on Zoom. And, you should be able to refer to the Zoom recording. And again, this is the second week of our course, **GCAP 3226**, and please come to the Zoom, including those who are watching this video, you can come to our Moodle classroom, and you should be able to find the Week 1 video, and also transcripts.

Just to catch up, you know, I know some of you were not here last week, so if you want to catch up, you want to know more about this course, what we're trying to do, you can just, well, I mean, you probably don't want to watch the whole video, but there's actually **transcripts available** you can take a look as well.

Now, please go to **week 2 notes**. So, as you can see, we've got in-class and after-class discussion, and then we have week two notes. So, just a little bit of recap. I think I have already talked about this, but the basic course objectives are here. I don't want to necessarily repeat myself. You can refer to the week one video, week one scripts, and also the bullet points here.

### Course Structure
And then we have got a course hub and, you know, there's a course overview, there's a link to the Google Docs and everything. Again, it's for your reference. We can update here, but mainly, if you just want more direct access to the materials, you can come back to Moodle. We don't want to kind of overwhelm you with all the different information, so we go back to the Moodle notes.

### Course Roadmap
So maybe we can show the roadmap. Right, so we have a roadmap. Again, right now, we are in week two, and because it's during the **shopping period**, we're not going to ask you to form the groups or select the topics or anything yet, so we're just going to give you a taste of what we're trying to do.

Because the **AI tool**, using AI to write programming codes, that's kind of one of the highlights of this course. And also, it can be a little bit overwhelming and scary, so it's like, we want to eat the frog first, so to speak.

So today, it won't be like a full 3-hour session, you know, maybe for some of you from computer science major, it's just like a breeze. It's very, very straightforward for you. But in that case, **please do help all the other, your fellow students**, okay? So, help them a little bit, and help us.

### Future Plans
And then starting from **week three and four**, we will start looking at some of the case studies that we're going to focus on in this course, and we're also going to:
- Form groups
- Invite you to start picking some projects and start working in this course
- Ensure each group has students from different backgrounds, so we can work together

### Course Philosophy
So, yeah, so the rest of the roadmap, you can just take a look, and **this is actually the first time we run this course**, so we are still kind of finalizing things a bit, so there might be some changes over the course.

But, in general, I think the rule of thumb is that **we try to support you**, especially when you are not from a math or computer science background. So, if you feel like there's a little bit difficult or challenging at this stage, do not worry too much, because we're here to help you, and we want to ensure that this course is friendly to everybody, you know, not just for students from science background, okay?

### Getting Started
So, with that, let's move on. You can look at… there's also assessment information from last week, which we will not repeat, but you can check out. We are going to offer more information and instruction about the assessment in due course.

Now, we're going to get into the **actual hands-on parts** of today's work, so, if you can, come to this Moodle page, the notes, you should be able to download the **week 2 materials**. It's a zip file, so once you download it, you can unzip it, you should be able to get a folder.

#### Technical Requirements
For those of you who are getting a tablet computer, like an iPad, I'm not sure whether this is going to work. Hi, Pat. Yeah, so, I think for those of you who are using a tablet computer, I would encourage you to **get a mobile computer next week**, but for now, I mean, you can still just kind of tag along and look at what we're doing, and maybe go to some... Go to one of the students with a mobile computer, so you know how things will work, and then you can go home, and with your mobile computer, or go to a computer lab, you should be able to get things done fairly quickly.

#### File Structure
So again, going back to the ZIP package, there will be:
1. **CSV file** - this is the data, okay? So, CSV is very similar to spreadsheet, but it's simpler, okay? So you can think of it as a spreadsheet. When you open it, it will be a spreadsheet, okay?
2. **Jupyter Notebook** - Now, Jupyter Notebook, you would consider this as some codes, okay? And, this is a file that you can write some codes, and the codes can be run right there, okay?

And in order to run the Jupyter Notebook, you can't just open the Jupyter Notebook, like, on your Word or Notepad or anything, so you have to install a software called **VS Code**.

#### Course Philosophy on AI
So again, what we're trying to do today is to introduce some analytical tools including **GitHub Copilot** that can help you write the codes, alright? Because, you know, I don't think we can run this course without AI, basically.

> If we talk about, like, two years ago, like, even one year ago, AI is not really that good at programming or writing program calls. We can't really run this course, you know, or we can only run this course for students who have already done some programming. But now with AI, we can basically teach this course even to students who have zero programming background, okay?

---

## Course Logistics Interruption

Sorry to interrupt, I don't know. Because we have a couple of students just join us. Just want to make sure that we're on the same page. If you can go to our **Week 2 notes in Moodle**.

And then, I actually replied. To share a, maybe I have to refresh. Just refresh. So, there's actually a link to the **Google Form**, right? So you should be able to access, you only take a quick look.

### Today's Learning Journey
The idea is that, as we explained earlier, today we're going to teach you how to use some… writing some **Python codes to analyze the data**, right? But for illustration purpose, we need to have some data to write the code, and the codes can perform, you know, can take the data as input, and then there will be output, which would become the **charts and graphs** and everything.

All right, so now what **Dr. Wu** is doing is to explain the context, right? So we know what the data looks like. If you want to look at the data, you can just go to that download zip file… the zip file, go to that folder, you will find a **CSV**.

Okay? So the CSV file is the data, is the responses to that questionnaire. Okay?

### Research Workflow
The whole journey would be:
1. You want to do some project, you want to do some research
2. You want to gauge the people's opinions, so you run a questionnaire
3. When people fill in the questionnaire, they will become like a **CSV file**
4. There's data, you know, quantitative data
5. You can't just make sense of data, right? It's all just numbers, you know, rows and cells
6. So we have to **write a program** that can do the kind of tedious work to turn the data into something that makes more sense to humans, which is **graphs and charts** and everything

So that's what we're trying to do today, okay? I hope that makes sense.

And again, if you are on a tablet computer, like an iPad, you can just probably listen a little bit, get to know what's going on, and when you go home, you can run the code very quickly on your own computer, right? Thanks.

---

## Technical Setup

For today, we will use the questions in this questionnaire to do the data visualization. So later, I think… I'm not sure how many of you have installed **VS Code**. Do you mind raising your hand? Not many. I think during the break, you can still do it. Just follow the reference book, which I screenshot yesterday, sent you by email.

### VS Code Interface
So, from there, we can download the… this is the **code editor**, which is called VS Code, that we will use to write Python code. So here shows the interface of this VS Code.

Because there are, I would say, many panels in this interface, so I think it's still useful to briefly talk about the structures:

#### Interface Components
- **Activity Bar** (left-hand side): The most commonly used one should be this, so you see these blocks? So this shows the extensions you need to install to open the Jupyter Notebook file we provided
- **Sidebar** (next to activity bar): Shows the folder you opened, and the scripts, or the notebook files in the directory
- **Editor Panels**: We basically type our code here, so this is the editing panel
- **Run Button**: If we want to run the code, actually for Jupyter Notebook, this run button is not here, but just next to the code, on the left-hand side. So after you install it, you will see that small button
- **Output and Terminal Panel** (bottom): I think at the very beginning stage, we don't even have to open this panel
- **Copilot Symbol**: So if it looks like this, it means that your AI programming assistant is there for you. So as long as you install the GitHub Copilot extension, you will be able to see this icon

### Jupyter Notebook
And what we will use to write code, it's called the **Jupyter Notebook**. So this notebook is an interactive tool that lets you:
- Write and run codes
- View results immediately
- Add notes

So here shows the interface of a web version of Jupyter Notebook, so we will use a local version. Basically, there are **two types of cells**:
1. **Code cell** - Where we input our code
2. **Markdown cell** - Where we can add the notes

The reason we choose to use Jupyter Notebook is that the results of the code can be immediately shown up just right after the code, so it's quite friendly. Say I have many code for my visualization, and after I run it, then the corresponding figures will show up immediately below this code cell.

### Setup Instructions
So, I think maybe later we have the break first, and during this break, as mentioned, you could:
- Go ahead to download Python VS Code
- Install the relevant extension from here

And then we will go to this scene. So, I think after the break, I will continue from here.

Alright, so let's take a **short break**, and if you have any questions about the setup, you can reply to our Week 2 notes. And I will be monitoring, you know, any reply, but of course, you know, you can raise your hand.

And starting from next week, once we, after the add/drop period, I'm going to **set up a WhatsApp group**. So you guys can join the group, and we can have further discussion, alright?

### Programming Philosophy
Right, so there's a little bit of technical details here, so I hope you can be patient if this is new to you. I think all this software and interface has been designed to be **human-friendly**.

Alright, so there's actually a lot of codes and a lot of magic running behind the scenes. So when we write a program with **AI assistance**, there's different levels of abstraction that we can decide, you know.

> At the highest level, you can treat all this as **black box**. In other words, all you care about is the input and output. What happened in between? You don't really have to worry much about.

And I think that's probably good enough for students taking this course, especially those with **no programming background**. You just:
1. Follow the instruction
2. Do a bit copy and pasting
3. Send the instruction to AI
4. The AI will generate codes
5. Copy and paste back to the Jupyter Notebook VS Code, and it will run

Alright, if it doesn't run, there may be some errors, there's some warning, you copy those errors and warning to AI again, and AI will tell you what to do, and you do it.

### Learning Journey
Okay, and why do you want to do that? And how the codes actually work? You don't have to worry about that at this stage. I mean, at some point, if you feel like you want to learn more, you want to become a more advanced learner of programming, then you can look into the codes.

But at this stage, for our purpose, for our course, you don't have to worry about all those technical details. So I hope that can give you kind of a **peace of mind**, you know, in terms of if you are from a non-programming background.

But at the same time, I also hope this experience would give you the opportunity to actually **open the door** for you, right? So maybe later on in your work, in your life, there's some other problems that need programming to help, then it can help, you see what I mean?

> So the next time when people talk to you about VS Code, Python, or Jupyter Notebook, it's not just all, like, a foreign language or Greek to you, you see what I mean?

So I think that's really important. I don't want to preach, but I think it's really important to **get out of our comfort zone and try new things**, right?

---

## Software Setup

### Progress Check
Let's take a short break, and we'll come back to do the hands-on thing. Let's check the progress:

**Raise your hand if you already got your VS Code installed on your computer.** That seems to be a very important step. Raise your hand. Okay?

**Now, raise your hand if you got that zip file downloaded from Moodle** and opened it/unzipped it. Yeah? Okay?

### Next Steps
Now, what you need to do, if you haven't done, is to **go to VS Code and open that folder** where you unzipped the zip file from. Okay?

Because once you download the zip file, it must be somewhere, right? It could be:
- On your desktop
- One of the folders
- For the course, you probably have a folder for this course

So, you unzip that file into your course folder, so there will be a folder for this specific activity.

#### File Contents
And in that folder, you should find:
1. **One CSV file** - that's the data file
2. **Another file that ends with .ipynb** - which is a Jupyter Notebook
3. **Another file** - I think it's a PDF or something

So basically, you have to **use VS Code to open that folder**. And, on the left-hand side, you will see a panel where you can see the folder, alright? And also the files.

Now, once you are at that stage, **you are in business**, okay? So you can open the Jupyter Notebook file in the VS Code. So you can start doing the coding.

### AI Assistance Options
Alright? Now, I mean, if you are a good programmer, you're an experienced programmer, you can even just write the code by yourself. You don't need AI. But for beginners, then you can **get some help from AI**.

So how do you get help from AI? Well, you can actually go to:
- Poe
- Grok  
- DeepSeek

You can do that as well. But the **Copilot is more integrated**, right? So that's why you want to start using Copilot.

### GitHub Copilot Setup
Now, in VS Code, you need to install an extension called **GitHub Copilot**. So you can access Copilot. That's your friend, okay? It can help you solve all the problems related to programming for this course, so make sure that you install the extension GitHub Copilot.

We do need to register, right? **Sign up for a GitHub account**, do we?

Okay, so once you have your extension of the GitHub Copilot ready, when you try to fire it up and start using Copilot, then Copilot would ask you to **log in to GitHub**, right, because it's a GitHub service.

#### Joining the GitHub Community
So then, this is a very important moment now, okay? Once you join the GitHub, **you join a community of programmers**. Alright?

So, and, next time when you talk to people, you say, **"I have a GitHub account"**, alright? That's something you should be proud of. And you can start making friends on GitHub. There's so many very interesting **open source projects** and things that's going on in GitHub.

Right? So maybe you are running into some really interesting project, and you can do a build-up, do a follow-up on that project, you see. **GitHub is an amazing community**, okay?

#### GitHub Education Benefits
And now, once you're on GitHub, once you have the account, you should have access to Copilot. All right?

And at some point, you may want to **apply for the GitHub education**. Because you are a university student, you are entitled to the education benefits of GitHub, so you can do that later. Because for this particular project, the **free account** should give you all the resources, all the tokens, and everything you need. Okay, so you don't have to worry.

### Getting Help
So I think we have kind of just explained to you how you can reach the stage, you have a **co-pilot next to you** to start writing codes. If you need some help to get to that step, just let us know, okay?

So, we want to make sure that everybody is on the same page, everybody can have access to Copilot. You know, you need to:
1. Install VS Code
2. Open the folder
3. Install the GitHub Copilot extension
4. Join GitHub, get a GitHub account
5. Login, and then we're in business, okay?

### Screen Sharing Demo
It's better to have, maybe I'll share my screen, too, so I can… Wait, that's selfish. Oh, no. Oh, the… But we also need to watch it. Oh, gosh.

So, for those of you who need some help, you can look at the screen here. So, of course, I'm using Mac. If you are using a Windows PC, it's a little bit different.

#### VS Code Walkthrough
So basically, what you can do is go to **VS Code**. And, VS Code is actually just called Code. Let me see if I can make it a bit bigger.

Alright, so, you are in VS Code, you will be able to see codes here. You just **open the folder**, right? So you open the folder. And it is the folder where you have unzipped the zip file we provided is called **"Week 2 Data Visualization GitHub Copilot"**.

Now, you open it. And once you open it, you can see there's **3 files**:
1. **The CSV** - The week 2 CSV, that's the spreadsheet, okay? That's all the data we got from the questionnaire
2. **The PDF** - So the PDF is the slides that Dr. Wu just presented
3. **The .ipynb file** - So this is the Jupyter notebook where you want to work on

#### Copilot Integration
So, I hope you are here. Now, once you are here, then you want to **open up the sidebar**, so there's a side window here, that's the Copilot. That's the GitHub Copilot.

Now, in order to fire up this GitHub Copilot thing, you will have to **install the extension**. So where do you install an extension? You come here. Oh, sorry. Right, so you come here, you see there's 3 squares, and one also square, but rotated a little bit. So that's the **extension**, right? So it's like, extension is like a piece of puzzle added to your picture, right?

So, there's many extensions. And you need to find an extension which is the **GitHub Copilot**, okay? And once you install it, you can open up here, and you can start getting some help from Copilot.

#### Copilot Modes
Now, in Copilot, there are 3 options:
1. **Agent** - more advanced, very recent feature
2. **Ask** - I would encourage you to go for Ask
3. **Edit**

Because **Agent Mode can be a bit confusing for beginners**, so let's try Agent Mode later. Agent mode is actually very amazing, you know, but for beginners, let's start with the **ask mode**, because you will have more control.

Agent Mode is like, they will take over. The AI will take over and do everything for you. All you have to do is just continue, continue, and they will do everything for you. But for our purpose, **let's still do a little bit of copy and paste**, all right?

### Getting Support
So I hope this has helped you a bit more, but do raise your hand if you have questions. You know, if you have no idea what's going on, that's normal, okay? Don't worry, that's normal. Just raise your hand, and we'll help you.

And for the **computer science majors**, do you want to stand up so you can offer some help?

### Command Line Usage
Alright, anyone needs help? Yeah. So if there's a need to run something like pip, or, you know, those are what we call **command line**. I would recommend you to go to VS Code, because VS Code has got its own command line, right?

So if you go to the top right corner, you see there's this icon, this button here. That's how you **open the command line**. Open the terminal, okay? So you need to learn how to open the terminal, and then you can start running some command.

---

*End of Simon Wang's Course Instructor Transcript*
