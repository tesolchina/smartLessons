# Test Account Locations & Information

## 📍 **Where to Find All Test Accounts**

### **1. Simon Testing Accounts (UI Testing)**
**Location:** Currently active for platform testing  
**Range:** 
- **Test 1:** `simon001` - `simon010` (10 accounts)
- **Test 2:** `simon101` - `simon110` (10 accounts)

**Purpose:** UI testing for both test sets  
**Platform:** https://test-taker-test.hkbu.me/  
**Documentation:** `/ui_testing/account_testing_log.md`

### **2. Staff Testing Accounts (ACTIVE!)**
**Range:** `staff001` - `staff500` (500 accounts)  
**Status:** ✅ **CONFIRMED ACTIVE** - These accounts are live and being used!  
**Type:** Production-scale testing accounts

## 📊 **How to Monitor Staff001-500 Account Activity**

### **🎯 Real-Time Monitoring Dashboard**
**NEW!** Access via: `http://localhost:8000/proctor/monitor/dashboard`

**Features:**
- ✅ **Login Status**: Last login time for each account
- ✅ **Exam Progress**: Current section, completion status
- ✅ **Live Activity**: Who's testing right now
- ✅ **Answer Tracking**: Number of submitted responses
- ✅ **Auto-Refresh**: Updates every 30 seconds

### **📈 Detailed Reporting Script**
**Location:** `/platform-source/ExamPlatform-BE/app/data/tool/account_status_report.py`

**Usage:**
```bash
# Generate summary for all staff accounts
python account_status_report.py --summary-only

# Detailed report for staff001-050
python account_status_report.py --start 1 --end 50

# Export to Excel
python account_status_report.py --start 1 --end 100 --output staff_report.xlsx
```

**Report Includes:**
- 📊 Login history and frequency
- 🎯 Exam completion status by section
- 📝 All submitted answers and scores
- ⏱️ Time spent on each section
- 🔍 Behavior tracking (clicks, navigation)

### **📋 Available Data Points**

#### **Login & Activity:**
- Last login timestamp
- Total login count
- Session duration
- IP addresses used
- Behavior patterns (clicks, navigation)

#### **Exam Progress:**
- Exam status (Not Started/In Progress/Completed)
- Current section (Reading/Listening/Writing/Speaking)
- Section start/end times
- Timeout status
- Overall score

#### **Submitted Answers:**
- Question-by-question responses
- Answer submission timestamps
- Marked questions (flagged for review)
- Correctness scoring
- Time spent per question

## 🔧 **Database Queries for Custom Analysis**

### **Quick Status Check:**
```sql
-- Active accounts in last 24 hours
SELECT COUNT(*) FROM users u 
JOIN behavior b ON u.id = b.user_id 
WHERE u.enroll_number LIKE 'staff%' 
AND b.behavior_type = 'login' 
AND b.created_at >= NOW() - INTERVAL '24 HOURS';

-- Currently testing
SELECT COUNT(*) FROM exam e 
JOIN users u ON e.examinee_id = u.id 
WHERE u.enroll_number LIKE 'staff%' 
AND e.status IN (1, 2);
```

### **Detailed Analysis:**
```sql
-- Complete account status
SELECT 
    u.enroll_number,
    u.email,
    MAX(b.created_at) as last_login,
    COUNT(DISTINCT e.id) as total_exams,
    COUNT(DISTINCT ea.id) as total_answers
FROM users u
LEFT JOIN behavior b ON u.id = b.user_id AND b.behavior_type = 'login'
LEFT JOIN exam e ON u.id = e.examinee_id
LEFT JOIN exam_answer ea ON u.id = ea.examinee_id
WHERE u.enroll_number LIKE 'staff%'
GROUP BY u.id, u.enroll_number, u.email
ORDER BY u.enroll_number;
```

## 📊 **Account Structure Overview**

### **Current Active Accounts (520 total)**
```
simon001-010: UI testing (20 accounts)
simon101-110: UI testing continuation

staff001-500: Production testing (500 accounts) ✅ ACTIVE
```

### **Platform Account Management**
**Database:** PostgreSQL with comprehensive tracking  
**Tables:**
- `users` - Account information
- `exam` - Test sessions
- `exam_section` - Section progress
- `exam_answer` - Submitted responses
- `behavior` - Login/activity tracking

## 🎯 **Access Methods**

### **1. Web Dashboard (Recommended)**
- **URL:** `http://localhost:8000/proctor/monitor/dashboard`
- **Features:** Real-time monitoring, auto-refresh
- **Requires:** Proctor login credentials

### **2. API Endpoints**
- **Summary:** `GET /proctor/monitor/api/summary`
- **Returns:** JSON with current statistics

### **3. Command Line Reports**
- **Script:** `account_status_report.py`
- **Output:** Excel files with detailed analysis

### **4. Direct Database Access**
- **Connection:** PostgreSQL database
- **Tables:** `users`, `exam`, `exam_answer`, `behavior`

## 📂 **Related Files & Documentation**

### **New Monitoring Files:**
- `ExamPlatform-BE/app/ui/proctor/monitor_ui.py` - Web dashboard
- `ExamPlatform-BE/app/data/tool/account_status_report.py` - Report generator

### **Existing Files:**
- `ui_testing/account_testing_log.md` - Simon account testing
- `ui_testing/platform_access_credentials.md` - Login details
- `emails/communication_002_River-Testing-Instructions.md` - Original instructions

## 🔍 **Quick Access Summary**

| Account Type | Range | Count | Status | Monitoring Available |
|-------------|-------|-------|--------|---------------------|
| Simon Test 1 | simon001-010 | 10 | ✅ Active | ✅ Manual tracking |
| Simon Test 2 | simon101-110 | 10 | ✅ Active | ✅ Manual tracking |
| Staff Accounts | staff001-500 | 500 | ✅ **ACTIVE** | ✅ **Full monitoring** |

**Total Available:** 520 test accounts  
**Monitoring Capability:** Full real-time tracking for staff accounts

## � **Next Steps**
1. **Access dashboard:** Login to monitoring interface
2. **Generate report:** Run status report for current activity
3. **Set up alerts:** Monitor for unusual patterns
4. **Regular analysis:** Weekly reports on usage patterns
