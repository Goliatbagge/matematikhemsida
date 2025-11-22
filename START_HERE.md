# START HERE - Quick Setup Guide

## What This System Does

This validation system automatically checks if your course cards match the actual content. It caught 2 critical issues where complete courses were showing "coming soon" messages.

---

## The Problem We Found

### Matematik 2c
- **Has:** 41 complete sections across 6 chapters
- **Shows:** "Innehåll kommer snart!" on main page
- **Result:** Users think the course isn't ready

### Matematik 3c
- **Has:** 39 complete sections across 6 chapters
- **Shows:** "Innehåll kommer snart!" on main page
- **Result:** Users think the course isn't ready

---

## Quick Fix (30 seconds)

```bash
# 1. Open terminal in the Hemsida folder
cd C:\claude\Hemsida

# 2. Run the automatic fix
node fix-course-cards.js

# 3. Verify it worked
node validate-courses.js
```

That's it! The script will:
- ✓ Create a backup
- ✓ Remove the "coming soon" messages
- ✓ Keep the badges and topics
- ✓ Show you what changed

---

## What You'll See

### Before Fix:
```
Matematik 2c card:
├── "Fullständig kurs" badge ✓
├── Topic list ✓
└── "Innehåll kommer snart!" ✗ (WRONG!)
```

### After Fix:
```
Matematik 2c card:
├── "Fullständig kurs" badge ✓
├── Topic list ✓
└── No "coming soon" message ✓ (CORRECT!)
```

---

## Understanding the Output

When you run `node validate-courses.js`, you'll see:

**Green ✓** = Everything is correct
**Yellow ⚠** = Warning (should fix)
**Red ✗** = Critical issue (must fix)

The script checks all 8 courses:
- Matematik 1b, 2b, 3b, 1c, 2c, 3c
- Fysik 1, 2

---

## Files You Got

| File | What It Does |
|------|-------------|
| `validate-courses.js` | Checks all courses for issues |
| `fix-course-cards.js` | Auto-fixes common problems |
| `VALIDATION_SUMMARY.md` | Quick reference of findings |
| `VALIDATION_REPORT.md` | Detailed analysis |
| `VALIDATION_SYSTEM_README.md` | Complete documentation |
| `SYSTEM_OVERVIEW.txt` | Visual summary |
| `package.json` | NPM script shortcuts |

---

## Using NPM Scripts

If you prefer using npm:

```bash
npm run validate      # Check for issues
npm run fix          # Auto-fix issues
npm run validate-fix # Fix and check
```

---

## When to Use This

### Run validation:

1. **Before committing changes**
   ```bash
   git add .
   node validate-courses.js  # Check first!
   git commit -m "Update courses"
   ```

2. **After adding course content**
   - Added new section files?
   - Updated course navigation?
   - Run validation to check consistency

3. **When updating course cards**
   - Changed main index.html?
   - Added/removed badges?
   - Validate to ensure accuracy

4. **Regular maintenance**
   - Weekly checks
   - Before deployments
   - After content updates

---

## Common Scenarios

### Scenario 1: I just added content to a course

```bash
# Step 1: Check current status
node validate-courses.js

# Step 2: Add your content files
# (create sections, update course index.html)

# Step 3: Validate again
node validate-courses.js
# Will show: "HAS content but shows coming soon"

# Step 4: Fix it
node fix-course-cards.js

# Step 5: Verify
node validate-courses.js
# Should show: "No issues found"
```

### Scenario 2: I want to mark a course as complete

1. Ensure all sections are in `coursename/sections/`
2. Update course `index.html` with chapter navigation
3. Run `node validate-courses.js`
4. If issues found, run `node fix-course-cards.js`
5. Update main `index.html` manually if needed:
   - Add "Fullständig kurs" badge
   - Remove "Innehåll kommer snart!" box
   - List actual topics

### Scenario 3: Something went wrong with the fix

```bash
# The fix script creates a backup automatically
# Look for: index.html.backup

# On Windows:
copy index.html.backup index.html

# On Mac/Linux:
cp index.html.backup index.html
```

---

## Need More Information?

### Quick Reference
→ Read: `VALIDATION_SUMMARY.md`

### Detailed Analysis
→ Read: `VALIDATION_REPORT.md`

### Full Documentation
→ Read: `VALIDATION_SYSTEM_README.md`

### Visual Overview
→ Read: `SYSTEM_OVERVIEW.txt`

---

## Troubleshooting

### "node: command not found"
**Solution:** Install Node.js from nodejs.org

### "Cannot find module"
**Solution:** Make sure you're in the Hemsida directory

### Script shows no changes
**Solution:** Issues may already be fixed, or HTML structure changed

### Validation still shows issues after fix
**Solution:**
1. Check if backup exists (should be auto-deleted)
2. Verify index.html was modified
3. Run validation again
4. Check console output for specific errors

---

## For Future Reference

### Adding a New Course

1. Create course directory: `newcourse/`
2. Add sections to: `newcourse/sections/`
3. Create: `newcourse/index.html`
4. Add card to main `index.html`
5. Update `validate-courses.js`:
   ```javascript
   const COURSES = [
       'matematik-1b',
       // ... existing courses
       'newcourse'  // Add here
   ];
   ```
6. Run validation: `node validate-courses.js`

---

## Success Indicators

You'll know it worked when:

✅ Validation shows 0 critical issues
✅ Matematik 2c displays correctly on main page
✅ Matematik 3c displays correctly on main page
✅ Users can see and access complete courses
✅ No confusion about course availability

---

## Quick Command Reference

```bash
# Validate all courses
node validate-courses.js

# Fix issues automatically
node fix-course-cards.js

# Fix and validate in one go
node fix-course-cards.js && node validate-courses.js

# Using npm
npm run validate
npm run fix
npm run validate-fix
```

---

## What Happens Next?

After you run the fix:

1. ✅ Backup created (index.html.backup)
2. ✅ "Innehåll kommer snart!" removed from complete courses
3. ✅ Badges and topics preserved
4. ✅ Main index updated
5. ✅ Validation confirms success

Then:
- Test the website in your browser
- Verify courses display correctly
- Delete the backup if everything looks good
- Commit your changes

---

## Important Notes

⚠️ **Always test in browser** after running fixes
⚠️ **Keep backups** until verified
⚠️ **Run validation** before committing
⚠️ **Check both course pages and main index**

---

## Summary

**The Issue:** Complete courses showing "coming soon"
**The Fix:** One command removes incorrect messages
**The Result:** Accurate course availability for users
**Time Required:** 30 seconds

**Ready? Run this now:**
```bash
cd C:\claude\Hemsida
node fix-course-cards.js
```

---

*Questions? Check VALIDATION_SYSTEM_README.md for complete documentation*
