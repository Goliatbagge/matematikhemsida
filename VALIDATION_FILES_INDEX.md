# Validation System - File Index

Complete guide to all validation system files and their purposes.

---

## 📖 Documentation Files (Read These)

### **START_HERE.md** 👈 **Begin Here**
- **Purpose:** Quick start guide for new users
- **Length:** ~5 min read
- **Contains:**
  - The problem explained simply
  - 30-second fix instructions
  - Common scenarios
  - Troubleshooting tips
- **When to read:** First time using the system

### **VALIDATION_SUMMARY.md**
- **Purpose:** Quick reference for current status
- **Length:** ~3 min read
- **Contains:**
  - Current course status table
  - Critical issues summary
  - Quick fix commands
  - Course content details
- **When to read:** Want a quick overview

### **VALIDATION_REPORT.md**
- **Purpose:** Detailed analysis report
- **Length:** ~10 min read
- **Contains:**
  - Complete course analysis
  - Specific code to fix
  - Prevention strategies
  - Course breakdowns
- **When to read:** Need detailed information

### **VALIDATION_SYSTEM_README.md**
- **Purpose:** Complete system documentation
- **Length:** ~15 min read
- **Contains:**
  - How the system works
  - Integration guide
  - Best practices
  - Troubleshooting
  - Advanced usage
- **When to read:** Want to understand the system fully

### **SYSTEM_OVERVIEW.txt**
- **Purpose:** Visual summary and overview
- **Length:** ~5 min read
- **Contains:**
  - ASCII art diagrams
  - Visual status tables
  - Workflow charts
  - Command reference
- **When to read:** Prefer visual information

### **VALIDATION_FILES_INDEX.md** (this file)
- **Purpose:** Guide to all files
- **Length:** ~3 min read
- **Contains:**
  - File descriptions
  - Reading order
  - Use cases
- **When to read:** Not sure which file to read

---

## 🔧 Executable Scripts (Run These)

### **validate-courses.js** ⭐ Main Script
```bash
node validate-courses.js
```

**What it does:**
- Scans all 8 courses
- Counts section files
- Extracts chapter information
- Validates main index cards
- Identifies inconsistencies
- Generates color-coded report

**Output:**
- Console with colors:
  - 🟢 Green = Correct
  - 🟡 Yellow = Warning
  - 🔴 Red = Critical issue
- Lists all findings
- Provides recommendations

**When to run:**
- Before committing
- After adding content
- During code reviews
- Regular maintenance

**Example output:**
```
=== MATEMATIK-2C ===
Course Content Status:
  - Section files: 41
  - Has actual content: YES
  - Main index says "coming soon": YES
Validation Results:
  ✗ Course HAS content but main index shows "coming soon"
```

---

### **fix-course-cards.js** 🔨 Auto-Fix Script
```bash
node fix-course-cards.js
```

**What it does:**
- Creates backup (index.html.backup)
- Removes "Innehåll kommer snart!" from complete courses
- Preserves badges and topics
- Updates main index.html
- Shows summary of changes

**Safety features:**
- Always creates backup first
- Can be rolled back
- Shows what changed
- Provides restore instructions

**When to run:**
- After validation finds issues
- When you want automatic fixes
- To clean up inconsistencies

**Example output:**
```
╔════════════════════════════════════════╗
║         COURSE CARD FIXER              ║
╚════════════════════════════════════════╝

Step 1: Creating backup...
  ✓ Created backup: index.html.backup

Step 2: Reading index.html...
  ✓ Read 8234 characters

Step 3: Fixing course cards...
  ✓ Fixed Matematik 2c card
  ✓ Fixed Matematik 3c card

Step 4: Writing changes...
  ✓ Changes written to index.html

╔════════════════════════════════════════╗
║              SUCCESS!                  ║
╚════════════════════════════════════════╝
```

---

## ⚙️ Configuration Files

### **package.json**
```json
{
  "scripts": {
    "validate": "node validate-courses.js",
    "fix": "node fix-course-cards.js",
    "validate-fix": "node fix-course-cards.js && node validate-courses.js"
  }
}
```

**Purpose:** NPM script shortcuts

**Usage:**
```bash
npm run validate      # Check for issues
npm run fix          # Auto-fix
npm run validate-fix # Fix then check
```

**Benefits:**
- Shorter commands
- Easier to remember
- Can chain commands
- Standard npm conventions

---

## 📊 Reading Order Guide

### For First-Time Users

```
1. START_HERE.md              ← Quick intro (5 min)
   ↓
2. Run: node validate-courses.js
   ↓
3. Run: node fix-course-cards.js
   ↓
4. VALIDATION_SUMMARY.md      ← Results summary (3 min)
   ↓
5. Test website in browser
```

### For Detailed Understanding

```
1. VALIDATION_REPORT.md            ← Full analysis (10 min)
   ↓
2. VALIDATION_SYSTEM_README.md     ← Complete guide (15 min)
   ↓
3. SYSTEM_OVERVIEW.txt             ← Visual summary (5 min)
   ↓
4. Experiment with scripts
```

### For Quick Reference

```
1. VALIDATION_SUMMARY.md      ← Status and commands
   ↓
2. Run scripts as needed
   ↓
3. Check specific sections in other docs when needed
```

---

## 🎯 Use Case Guide

### I want to fix the issues NOW
→ Read: `START_HERE.md`
→ Run: `node fix-course-cards.js`

### I want to understand what's wrong
→ Read: `VALIDATION_SUMMARY.md`
→ Run: `node validate-courses.js`

### I need detailed information
→ Read: `VALIDATION_REPORT.md`

### I want to learn the system
→ Read: `VALIDATION_SYSTEM_README.md`

### I prefer visual information
→ Read: `SYSTEM_OVERVIEW.txt`

### I'm adding new content
→ Read: `VALIDATION_SYSTEM_README.md` (section: "When adding a new course")
→ Run: `node validate-courses.js` before and after

### I'm reviewing changes
→ Run: `node validate-courses.js`
→ Check: `VALIDATION_SUMMARY.md` for quick status

### I'm troubleshooting
→ Read: `VALIDATION_SYSTEM_README.md` (Troubleshooting section)
→ Run: `node validate-courses.js` with verbose output

---

## 📈 File Relationships

```
START_HERE.md
    ↓ (references)
VALIDATION_SUMMARY.md
    ↓ (references)
VALIDATION_REPORT.md
    ↓ (references)
VALIDATION_SYSTEM_README.md
    ↑ (uses)
validate-courses.js
    ↑ (calls)
fix-course-cards.js
    ↑ (configured in)
package.json
```

---

## 🔍 Content Comparison

| File | Length | Detail Level | Technical | Examples | Commands |
|------|--------|--------------|-----------|----------|----------|
| START_HERE | Short | Low | Low | Yes | Yes |
| VALIDATION_SUMMARY | Medium | Medium | Low | Yes | Yes |
| VALIDATION_REPORT | Long | High | Medium | Yes | Some |
| SYSTEM_README | Long | High | High | Many | Yes |
| SYSTEM_OVERVIEW | Medium | Medium | Low | Some | Yes |

---

## 💡 Quick Tips

### Getting Started
1. Read START_HERE.md first
2. Run the validation
3. Run the fix
4. Check results

### Learning More
1. Read VALIDATION_SUMMARY.md for overview
2. Read VALIDATION_REPORT.md for details
3. Read SYSTEM_README.md for complete knowledge

### Daily Use
1. Keep VALIDATION_SUMMARY.md handy
2. Run validate-courses.js regularly
3. Check SYSTEM_OVERVIEW.txt for commands

---

## 📋 File Sizes (Approximate)

| File | Lines | Size |
|------|-------|------|
| START_HERE.md | 400 | 15 KB |
| VALIDATION_SUMMARY.md | 500 | 20 KB |
| VALIDATION_REPORT.md | 600 | 25 KB |
| VALIDATION_SYSTEM_README.md | 800 | 35 KB |
| SYSTEM_OVERVIEW.txt | 400 | 18 KB |
| validate-courses.js | 450 | 15 KB |
| fix-course-cards.js | 250 | 8 KB |
| package.json | 20 | 500 B |

---

## ✅ Verification Checklist

After reading the appropriate files and running scripts:

- [ ] I understand what the validation system does
- [ ] I know how to run validation
- [ ] I know how to fix issues
- [ ] I've read the documentation I need
- [ ] I've run the validation script
- [ ] I've reviewed the results
- [ ] I know where to find more information

---

## 🆘 If You're Lost

**Start here:**
1. Open `START_HERE.md`
2. Read the first section
3. Run `node validate-courses.js`
4. Follow the output

**Still confused?**
1. Open `VALIDATION_SUMMARY.md`
2. Look at the course status table
3. Check the "Quick Fix" section

**Need more help?**
1. Open `VALIDATION_SYSTEM_README.md`
2. Check the "Troubleshooting" section
3. Review the examples

---

## 📞 Quick Reference

**Check for issues:**
```bash
node validate-courses.js
```

**Fix issues:**
```bash
node fix-course-cards.js
```

**Learn about it:**
- Quick: `START_HERE.md`
- Detailed: `VALIDATION_REPORT.md`
- Complete: `VALIDATION_SYSTEM_README.md`

---

**Remember:** Start with `START_HERE.md` and work your way through as needed!

---

*Last Updated: 2025-11-01*
*Part of: Hemsida Course Validation System v1.0*
