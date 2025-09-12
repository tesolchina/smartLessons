[[Bytewise Chatbot platform]]
#deadline #toSchedule  


Enhance file reading of Bytewise

Karim ABILGAZIYEV<24210293@life.hkbu.edu.hk>

​Zian ZHENG <22231153@life.hkbu.edu.hk> [[Andy Zian Zheng]]​

​Simon H WANG​

Dear Andy, 

  

I am not familiar with the Bytewise’s extensive codebase, so I am not able to quickly implement the image handling. However, I can share some techniques I used in my grader app.

  

OpenRouter API does not support file (including image) uploading directly. I learned that you still can send the data to LLM. 

  

1. Merge all the images into one PDF file
    
2. Encode the image into Base64 encoding
    
3. Send the encoded string as message through the API
    

  

You can find code example on my repo in Github. Github/Bytewise/ORBS_Grader/app/backend/utilities/GPT_Responder.py The function called get _analysis and notebookToLLMRequest will provide code snippets.

  

Sincerely,

Karim

**From:** Zian ZHENG <22231153@life.hkbu.edu.hk>  
**Date:** Tuesday, 19 August 2025 at 02:14  
**To:** Karim ABILGAZIYEV <24210293@life.hkbu.edu.hk>  
**Cc:** Simon WANG <simonwang@hkbu.edu.hk>  
**Subject:** Fwd: Enhance file reading of Bytewise  
  

Dear Karim,

  

I hope this email finds you well.

  

As mentioned in the email I forwarded to you, the progress of task 2 (image analysis for Bytewise) has not been satisfactory. Simon would like to ask if you could take a look at this and take it over since you’re familiar with how LLMs can handle various file types.

  

Please let me know if you have any questions.

  

Best regards,

Andy

  

Begin forwarded message:

  

> **From:** Simon H WANG <simonwang@hkbu.edu.hk>
> 
> **Date:** July 18, 2025 at 23:18:45 GMT+8  
> **To:** Zian ZHENG <zian-zheng0715@life.hkbu.edu.hk>, Muhammad Ahmad NADEEM <24210323@life.hkbu.edu.hk>, Jiayi NIE <barrynie@life.hkbu.edu.hk>  
> **Cc:** Junxin HUANG <junxin@hkbu.edu.hk>  
> **Subject:** **Enhance file reading of Bytewise**  
>   

> ﻿ Hi Andy 
> 
> I'd like to discuss the need to enhance Bytewise's file reading. Currently it can only OCR image files and read word and PDF to a limited extent. 
> 
> Task 1 to explore integrating MinerU [https://opendatalab.github.io/MinerU/](https://opendatalab.github.io/MinerU/ "https://opendatalab.github.io/MinerU/")
> 
> |   |   |
> |---|---|
> |[![](https://www.bing.com/th/id/OVP.sq-lPbmDLYHyIDjXcK1x6AEiEi?pid=Api)](https://opendatalab.github.io/MinerU/)|[MinerU - MinerU](https://opendatalab.github.io/MinerU/)<br><br>MinerU - MinerU<br><br>opendatalab.github.io|
> 
>  for PDF reading; Ahmad @Muhammad Ahmad NADEEM will work on this 
> 
> Task 2 to revise the system prompt so image files can be sent to LLMs for processing @Jiayi NIE Barry - could you look into this 
> 
> Task 3 to ensure the files uploaded are still accessible (currently- after uploading- they are gone) - Andy - could you look into this 
> 
>   
> 
> Please update our Google sheet and I'll talk to you a bit tomorrow after China Daily meeting. 
> 
> Thanks 
> 
> Simon 
> 
>   
> 
>   
> 
>   
> 
> Dr Simon Wang
> 
> Lecturer in English
> 
> The Language Centre
> 
> Hong Kong Baptist University 
> 
> Phone/WhatsApp 34117044 
> 
> [hkbu.cc/simon](http://hkbu.cc/simon "http://hkbu.cc/simon")    
> 
>   
> 
> |   |   |   |   |
> |---|---|---|---|
> |[![Outlook-wgpuqao5.png](https://attachments.office.net/owa/simonwang%40hkbu.edu.hk/service.svc/s/GetAttachmentThumbnail?id=AAkALgAAAAAAHYQDEapmEc2byACqAC%2FEWg0ARHFNbuconECNES0RyWBtzQADT54B1AAAARIAEADttArm2%2FK1SrYrCKwTvpTB&thumbnailType=2&token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkV0d09aS2IwNzVOSCt6MjdaTjN6U3Z3Z3djbz0iLCJ4NXQiOiJFdHdPWktiMDc1TkgrejI3Wk4zelN2d2d3Y289Iiwibm9uY2UiOiIxMGhrVFdHenpqUEJzNXJYTTFwNkVNSnFVZHQ1UnByeTNTTWI3WktfUzczdDNnUFBMNGFlSFFqTWE1cFhQU3k4YURJWXVycDdRVjNmaFVHeGZGNW5La0dJQnRxM19pOHdhOWxodVh0X3dnYVI1S3JEdmVwNWRkdFdmUDZwVEJ5SF9fQVY1U204YTFhYXNMRThZQWpWd2RHVlBQd1BtU2FxYjItQlNNZEZ2LWsiLCJpc3Nsb2MiOiJTSTJQUjAyTUI1MjI1Iiwic3JzbiI6NjM4OTEyNjI5MzU4NDE2ODQ0fQ.eyJzYXAtdmVyc2lvbiI6IjMyIiwiYXBwaWQiOiJhZjNlYmJiYS1jMjNmLTQ5MmEtYWE5My04MzQyMTY5NmVjNGIiLCJpc3NyaW5nIjoiV1ciLCJhcHBpZGFjciI6IjIiLCJhcHBfZGlzcGxheW5hbWUiOiIiLCJ1dGkiOiI0MzIwODljMi1mMzYwLTRjN2QtOWMzYS1jZmVhMzhhY2IzOGIiLCJpYXQiOjE3NTU3MDc1ODgsInZlciI6IlNUSS5Vc2VyLkNhbGxiYWNrVG9rZW4uVjEiLCJ0aWQiOiJlZDljYTkyMDU0M2U0MzA1OWE2NGQ2MjM5NzE2ZWZiYiIsInRydXN0ZWRmb3JkZWxlZ2F0aW9uIjoiZmFsc2UiLCJ0b3BvbG9neSI6IntcIlR5cGVcIjpcIk1hY2hpbmVcIixcIlZhbHVlXCI6XCJTSTJQUjAyTUI1MjI1LmFwY3ByZDAyLnByb2Qub3V0bG9vay5jb21cIn0iLCJyZXF1ZXN0b3JfYXBwaWQiOiIxNTdjZGZiZi03Mzk4LTRhNTYtOTZjMy1lOTNlOWFiMzA5YjUiLCJyZXF1ZXN0b3JfYXBwX2Rpc3BsYXluYW1lIjoiT2ZmaWNlIDM2NSBFeGNoYW5nZSBNaWNyb3NlcnZpY2UiLCJzY3AiOiJPd2FBdHRhY2htZW50cy5SZWFkIiwib2lkIjoiMmM3YTEzMzQtNGMwZi00ZDIxLTllYjUtODY4OGQxYjFhYzcwIiwicHVpZCI6IjEwMDMyMDAxRDMzODk0RjYiLCJzbXRwIjoic2ltb253YW5nQGhrYnUuZWR1LmhrIiwidXBuIjoic2ltb253YW5nQGhrYnUuZWR1LmhrIiwidXNlcmNhbGxiYWNrdXNlcmNvbnRleHRpZCI6ImU5NDA1YTkyNTcyMzQ2NzU5N2E2NDAxMjBkOWVlYTk4Iiwic2lnbmluX3N0YXRlIjoia21zaSIsImVwayI6IntcImt0eVwiOlwiUlNBXCIsXCJuXCI6XCJvaWN2dWYzOWgwdmYwQkNUeVlyWFNwOVhZNWludTFuZjRLYm8xMEVKYXlzT18xMld1VUFIWUg1M1VOVHVPVVNCTlZneGVTbHUxOHN6VkZoeWxEOExqVjZYRWlRNHA4VW44WHdCQUtFTmxnUVNEamIycmZsR1NqUHpuQUxuMnFQN3JBNVNYdGM2eVIwQkJNZTc2QldhWUljU3R4eFp4WnR1c2dKclRlUHZFVmY2NzlmYndRMURxTXRtR0FqbEFYelp5U1FZdXMxamxvN0NSSEZRbWxySjFDYVJ6bUVyal93XzhCMFRzQktGQ0lrbTlVNkJYLVk1aEs4alVoTEczMXA1NFI4eVdpQWRDMGFZOTBNM3RSTXU3Nm5fN3FFMng2N21SVHNGLWF6VEpwQ1AzTmcxQUJUdTlmdWN3Qmw5LURUU05QZzVZUHZtWjkxTFA3UTRTNlh5RVFcIixcImVcIjpcIkFRQUJcIixcImFsZ1wiOlwiUlMyNTZcIixcImV4cFwiOlwiMTc1NTc5Njc1NlwiLFwiZXhwX2RpZmZcIjpcIjg2NDAwXCIsXCJraWRcIjpcIjZONXNGY1J0WnlsOU1OUkZZckhuMjQwb1lXOFwifS5qNjJNOWh1K1BOQWE3ZTlWU0IxSklxby9mOXJ5L2tSNUovcDYyVXBQREwvMDQ4YkpEbm40dkNmMHFxcjUxeDJuUHcrRDMyaGFzd0tEaUVpcG5TY3F2OXZqRHRROGVoT3dldS9rNnVrb0d6NjFxazJGMXpqMkhZeUNUT2d5blJ2bXNLMHRsVnVTS0dtVndRZ2JLTG92UUYzSDVwVlBzZjh0Z2w4ZVh0cU1pWmx0R2tnUlZMK04vT0VRU2dxU0Z3STlVcGVicUtxaUwwMkNuRmJ0MjMvTERFZUFtWncwV1ZDVllTWVM3Wm1acUJkaDQycFhvcVdYU0tOY1dLb0NHakxNUTVFMzl4N0VpYVcwOG40d1Jvbmk3STFQN2J6TS9CZFdqcWdBRXkzUy81U3dUSHExNitCSCttaXArQ3IvUG5NblBISXpkUHlURWg3N1RKaHFyK3lVWmc9PSIsIm5iZiI6MTc1NTcwNzU4OCwiZXhwIjoxNzU1NzA3ODg4LCJpc3MiOiJodHRwczovL3N1YnN0cmF0ZS5vZmZpY2UuY29tL3N0cy8iLCJhdWQiOiJodHRwczovL291dGxvb2sub2ZmaWNlLmNvbSIsInNzZWMiOiJFN3d3TTRENEY1bFEyRlB0IiwiZXNzZWMiOiJhcnRpZmFjdC1hdXRvLXByb2R8TTM2NTIwMjUtMDYtMjNUMTg6MTU6NDMuMjU2Mjg5Mlp8YWhtVnUyRjRkUHJmYkkifQ.El74iP4ziszWeFBIZPZrPSt8r0MabiauKQgVGV_VPq-U-lrmSaGu7Q7Im35FSqBxfI2oL09MJLuXeW-pRvzTqWMvQa-mkoPPvXpQUiDk6cJMsOKBadz3i_feJzc___nCe3XeJEc6aGcvd3rtrch8ea5m8-hhOyFvUWqUu7jBy_odlkhGekH-s3laUKcesf8R7v5VErFiH1Bg2G_KExNpHr_THy47LbsSPkI0MtJR9sxkXSHjyCFawNtXLVSsbSU1RaMI5avCmQJqN-Mrp44bZjYM7NW-5HFCOyCVkEZ5-cb5G7fBTkJb4FcgbsXUShuUlYWIDCO7Z4m2FXE5Vu0lFw&X-OWA-CANARY=KuLqCXDvtXEAAAAAAAAAACCG4LQH4N0Y_J6CbnR-KEL2b9yyKkIqYg_UlsPNsaqJKsgyMwNxDLg.&owa=outlook.office.com&scriptVer=20250808005.17&clientId=853816AA129F460691F5807A0F9D3F3B&animation=true)](https://outlook.office.com/bookwithme/user/13f5e1db5441410c9070383f3993db0e@hkbu.edu.hk?anonymous&ep=bwmEmailSignature "https://outlook.office.com/bookwithme/user/13f5e1db5441410c9070383f3993db0e@hkbu.edu.hk?anonymous&ep=bwmEmailSignature")||[Book time to meet with me](https://outlook.office.com/bookwithme/user/13f5e1db5441410c9070383f3993db0e@hkbu.edu.hk?anonymous&ep=bwmEmailSignature "https://outlook.office.com/bookwithme/user/13f5e1db5441410c9070383f3993db0e@hkbu.edu.hk?anonymous&ep=bwmEmailSignature")||
> 
> ---
> 
> |   |   |
> |---|---|
> |![Baptist University Logo](https://staffweb.hkbu.edu.hk/BU-logo.png)<br><br>Disclaimer  <br>  <br>This message (including any attachments) may contain confidential information intended for a specific individual and/or purpose. If you are not the intended recipient, please delete this message and notify the sender immediately. Any disclosure, copying, or distribution of this message, or the taking of any action based on it, is prohibited as it may be unlawful or may lead to disciplinary action.|   |

Zian ZHENG

Tue 19/08/2025 02:14

Dear Karim, I hope this email finds you well. As mentioned in the email I forwarded to you, the progress of task 2 (image analysis for Bytewise) has not been satisfactory. Simon would like to ask if you could take a look at this and take it over since you’re

Muhammad Ahmad NADEEM

Fri 25/07/2025 15:44

Hi Dr. Wang, Hope this email finds you well. I've been working on the Mineru project. The primary issue is that Mineru is very nascent so there is no proper documentation for its Python-based applications. There are some basic CLI commands mentioned but the

Muhammad Ahmad NADEEM

Mon 21/07/2025 02:12

Hi Dr. Simon, Thank you for your email, and apologies for the delay in responding, as I was swamped over the weekend. I'll look into the task as mentioned in your email. Cheers, Ahmad

Zian ZHENG

Sun 20/07/2025 20:20

Hi Simon, Apologies for the weekend delay in replying to your email. I've already performed a preliminary investigation into my assigned part, Task 3, regarding file accessibility. I can confirm the bug where uploaded files become 'undefined' in the chat context.

You

Fri 18/07/2025 23:18

Hi Andy I'd like to discuss the need to enhance Bytewise's file reading. Currently it can only OCR image files and read word and PDF to a limited extent. Task 1 to explore integrating MinerU https://opendatalab.github.io/MinerU/ for PDF reading; Ahmad @Muhammad