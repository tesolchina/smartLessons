---
# Email Draft - LC Website Updates Request
# Machine-readable metadata

email_metadata:
  date_created: "2025-09-06"
  priority: "Normal"
  category: "Website Updates"
  status: "Draft"
  
recipients:
  to:
    - name: "Hermine Chan"
      email: "hermine_chan@hkbu.edu.hk"
      role: "LC Manager"
  cc:
    - name: "Cissy Li"
      email: "yxli@hkbu.edu.hk"
      role: "Head of LC"

sender:
  name: "Simon Wang"
  role: "Lecturer I & Innovation Officer"

subject: "Quick Website Updates While We Plan the Revamp"

requested_changes:
  - type: "removal"
    location: "front_page"
    element: "2024 Conference link"
    current_url: "https://lc.hkbu.edu.hk/main/lconference/"
    action: "Remove top bar link"
    
  - type: "update"
    location: "staff_profile"
    person: "Simon Wang"
    pages:
      - "https://lc.hkbu.edu.hk/main/simonwang/"
      - "https://lc.hkbu.edu.hk/main/staff-english/"
    current_title: "Lecturer I"
    new_title: "Lecturer I & Innovation Officer"
    reason: "Recent appointment as Innovation Officer"

---

# EMAIL DRAFT

## Subject: Quick Website Updates While We Plan the Revamp

Hi Hermine,

Hope you're doing well! I know the website revamp project has been delayed, and we should definitely catch up soon to get things back on track.

In the meantime, I was wondering if we could make a couple of quick updates to keep the current site fresh:

### Quick Updates Needed:

#### 1. Remove the 2024 Conference Link
- **Where:** Front page top bar
- **What:** That link to the 2024 Conference (https://lc.hkbu.edu.hk/main/lconference/)
- **Why:** Since the conference is over, we should probably take it down

#### 2. Update My Title
- **Where:** My profile pages:
  - https://lc.hkbu.edu.hk/main/simonwang/
  - https://lc.hkbu.edu.hk/main/staff-english/
- **Change:** From "Lecturer I" to "Lecturer I & Innovation Officer"
- **Why:** I've been appointed as Innovation Officer, so it would be great to have this reflected

### No Rush, But...
These are pretty small changes that shouldn't take much work - just quick fixes really.

Let me know if you need any more details for the technical team.

In a separate email, we'll discuss how to make some major changes to the front page, but these two items should be straightforward.

Looking forward to catching up about the website project soon!

Cheers,

Simon

Simon Wang  
Lecturer I & Innovation Officer  
Language Centre  
Hong Kong Baptist University

---

## Technical Notes for Implementation:
1. **Conference Link Removal**: Locate top navigation/header bar element and remove or comment out the 2024 Conference link
2. **Title Updates**: Update text content in both specified pages from "Lecturer I" to "Lecturer I & Innovation Officer"
3. **Verification**: Please confirm changes are live on both main site and UAT environment

---

*Email generated: September 6, 2025*  
*Status: Ready for review and sending*
