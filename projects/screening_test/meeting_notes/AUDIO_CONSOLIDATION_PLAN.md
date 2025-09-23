# Listening Test Audio Consolidation Plan

**Date:** September 21, 2025  
**Status:** 📋 PLANNING PHASE  
**Priority:** HIGH - Platform Constraint

## 🚨 **Core Issue**
**Platform Limitation:** Cannot display/play multiple audio files on the same screen during listening tests.

**Current Problem:** 
- Markdown file references 2 separate audio files
- Platform architecture requires single audio per test section
- Raw materials contain 3+ audio files creating confusion

## 📊 **Current Audio Inventory**

### **Raw Test 1 Materials:**
```
/test_questions/raw/test1&2/Test 1/
├── Audio Recording (Listening).mp3      # ❓ Unknown content
├── Listening Excerpt 1 (V3).MP3         # ✅ Used in Q1-4
├── Listening Excerpt 2 (V2).MP3         # ✅ Used in Q5
├── Audio Recording (Writing).mp3        # ⚠️ Different section
└── Writing V2.MP3                       # ⚠️ Different section
```

### **Current Markdown Structure:**
- **Questions 1-4**: `Listening Excerpt 1 (V3).mp3`
- **Question 5**: `Listening Excerpt 2 (V2).mp3` 
- **Instructions**: "You will hear TWO excerpts"

## 🎯 **Solution Strategy**

### **Phase 1: Audio Consolidation (Technical)**
1. **Combine Audio Files:**
   - Merge `Listening Excerpt 1 (V3).mp3` + `Listening Excerpt 2 (V2).mp3`
   - Add transitional instructions between excerpts
   - Create single consolidated file: `Listening_Combined_V1.mp3`

2. **Transitional Audio Content:**
   ```
   [Excerpt 1 content]
   → "You have just heard the first excerpt. Now listen to the second excerpt 
      for the cloze summary questions."
   [Excerpt 2 content]
   → "This concludes the listening section."
   ```

3. **Markdown Update:**
   ```markdown
   <audio id="examAudio" preload="auto">
     <source src="...../Listening_Combined_V1.mp3" type="audio/mpeg">
   </audio>
   ```

### **Phase 2: Content Standardization (Communication)**

#### **2.1 Exam Writer Communication**
**Immediate Action Items:**
- [ ] Document current audio file confusion
- [ ] Establish single-audio-per-section requirement  
- [ ] Create standardized markdown template
- [ ] Set up content review workflow

#### **2.2 Standard Format Agreement**
**Required Specifications:**
1. **Audio Requirements:**
   - ONE audio file per test section
   - Maximum duration: 8 minutes for listening sections
   - Include clear transitions between question segments
   - Professional voice instructions for transitions

2. **Markdown Template:**
   ```markdown
   ## Listening
   duration: 10
   audio_file: single_combined_file.mp3
   question_mapping: 
     - Q1-4: 0:00-4:30 (first excerpt)
     - Q5: 4:30-8:00 (second excerpt)
   ```

3. **Content Workflow:**
   - Exam writers provide content outline
   - Audio team creates consolidated recordings
   - Markdown team formats for platform
   - QA team validates before deployment

## 📋 **Implementation Timeline**

### **Week 1: Immediate Fixes**
- [ ] **Day 1**: Undo current markdown changes ✅ DONE
- [ ] **Day 2**: Audit all audio files in raw materials
- [ ] **Day 3**: Create audio consolidation script/process
- [ ] **Day 4**: Produce consolidated listening audio
- [ ] **Day 5**: Update markdown with single audio reference

### **Week 2: Communication & Standards**
- [ ] **Meeting**: Present findings to exam writing team
- [ ] **Documentation**: Create standardized markdown template
- [ ] **Agreement**: Establish content creation workflow
- [ ] **Training**: Brief team on new requirements

### **Week 3: Validation & Testing**
- [ ] **Platform Testing**: Verify single audio playback
- [ ] **Content Review**: Validate consolidated audio quality
- [ ] **User Testing**: Test student experience
- [ ] **Iteration**: Refine based on feedback

## 🔧 **Technical Requirements**

### **Audio Processing:**
- **Software**: Audacity, Adobe Audition, or similar
- **Format**: MP3, 128kbps minimum
- **Transitions**: 2-3 second gaps with voice instructions
- **Quality**: Clear audio, consistent volume levels

### **Platform Updates:**
- Verify single audio player functionality
- Test audio loading and playback controls
- Validate timing mechanisms during playback
- Check mobile/desktop compatibility

## 📞 **Communication Strategy**

### **Stakeholder Meetings Required:**
1. **Exam Writing Team**: Content format requirements
2. **Audio Production Team**: Technical specifications  
3. **Platform Development**: Implementation constraints
4. **Testing Team**: Validation protocols

### **Key Messages:**
- Platform constraint requires single audio per section
- Need standardized content creation workflow
- Quality over quantity - better single audio than multiple confusing files
- This fix improves student experience and reduces technical issues

## 📁 **Documentation Updates Needed**

### **Files to Create/Update:**
- [ ] `AUDIO_CONSOLIDATION_PROCESS.md`
- [ ] `MARKDOWN_TEMPLATE_STANDARDS.md` 
- [ ] `EXAM_WRITER_GUIDELINES.md`
- [ ] `AUDIO_TECHNICAL_SPECS.md`

### **Templates to Develop:**
- [ ] Standard listening section markdown template
- [ ] Audio consolidation checklist
- [ ] Quality assurance validation form

## 🎯 **Success Criteria**

1. **Technical:** Single audio file plays correctly on platform
2. **Content:** Clear transitions between question segments
3. **User Experience:** Students understand audio structure
4. **Workflow:** Exam writers follow standardized process
5. **Quality:** No confusion about audio file relationships

---

**Next Immediate Action:** Schedule stakeholder meeting to present this plan and get buy-in from exam writing team.

**Estimated Timeline:** 3 weeks to full implementation  
**Risk Level:** Medium (requires coordination across teams)  
**Impact:** High (improves platform stability and user experience)