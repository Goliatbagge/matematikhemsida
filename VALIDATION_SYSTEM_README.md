# Course Content Validation System

This validation system automatically checks for inconsistencies between course content and the main index page, helping prevent user confusion about course availability.

## Quick Start

```bash
# Validate all courses
node validate-courses.js

# Automatically fix identified issues
node fix-course-cards.js

# Verify fixes
node validate-courses.js
```

## Files in This System

### 1. `validate-courses.js`
**Purpose:** Validates course content consistency

**What it checks:**
- ✓ Number of section files per course
- ✓ Chapters listed in course index
- ✓ "Innehåll kommer snart!" messages
- ✓ "Fullständig kurs" badges
- ✓ Topic lists on main index
- ✓ Description accuracy

**Output:** Color-coded console report showing:
- Courses with complete content
- Courses without content
- Inconsistencies and issues
- Specific recommendations

**Usage:**
```bash
node validate-courses.js
```

### 2. `fix-course-cards.js`
**Purpose:** Automatically fixes common issues

**What it does:**
- Creates backup of index.html
- Removes "Innehåll kommer snart!" from complete courses
- Preserves badges and topic lists
- Provides rollback instructions

**Usage:**
```bash
node fix-course-cards.js
```

**Safety:**
- Always creates `.backup` file first
- Shows what changes will be made
- Can be rolled back if needed

### 3. `VALIDATION_REPORT.md`
**Purpose:** Detailed validation report and documentation

**Contents:**
- Executive summary of all courses
- Detailed analysis per course
- Specific code changes needed
- Prevention strategies
- Integration recommendations

## Understanding the Validation Report

### Status Indicators

#### ✅ Correctly Configured
Course status matches main index card:
- Complete courses show badge and topics
- Incomplete courses show "coming soon"

#### ⚠️ Issues Found
Mismatches detected:
- Complete course marked as "coming soon"
- Incomplete course marked as complete
- Missing badges on complete courses

### Common Issues

| Issue | What it means | How to fix |
|-------|--------------|------------|
| **"Course HAS content but main index shows 'Innehåll kommer snart!'"** | Course is complete but users see "coming soon" | Remove the "coming soon" message box |
| **"Course marked as 'Fullständig kurs' but has no actual content"** | Badge exists but no sections found | Remove badge, add "coming soon" message |
| **"Main index lists topics but course has no content"** | Topic list exists but course empty | Remove topic list, add "coming soon" message |
| **"Missing 'Fullständig kurs' badge"** | Complete course without badge | Add badge to main index card |

## How It Works

### Course Content Detection

The validator checks for content in three ways:

1. **Section Files**
   ```
   coursename/sections/kap1-01.html
   coursename/sections/kap1-02.html
   ...
   ```
   Counts HTML files in the sections directory

2. **Chapter Navigation**
   ```html
   <a href="#" class="dropbtn">Kapitel 1: Title</a>
   ```
   Extracts chapter titles from course index.html

3. **Coming Soon Message**
   ```html
   <h2>Innehåll kommer snart!</h2>
   ```
   Checks if course index has this message

### Main Index Card Analysis

The validator examines each course card:

1. **Badge Detection**
   ```html
   <div>Fullständig kurs</div>
   ```

2. **Coming Soon Box**
   ```html
   <div style="...background: #f8f9fa...">
       <p>Innehåll kommer snart!</p>
   </div>
   ```

3. **Topics List**
   ```html
   <ul>
       <li>✓ Topic 1</li>
       <li>✓ Topic 2</li>
   </ul>
   ```

4. **Description Text**
   ```html
   <p style="...">Course description here...</p>
   ```

## Integration Guide

### Option 1: NPM Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "validate": "node validate-courses.js",
    "fix-courses": "node fix-course-cards.js",
    "validate-fix": "node fix-course-cards.js && node validate-courses.js"
  }
}
```

Usage:
```bash
npm run validate
npm run fix-courses
npm run validate-fix  # Fix and validate
```

### Option 2: Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/sh
echo "Validating course content..."
node validate-courses.js

if [ $? -ne 0 ]; then
    echo "Validation failed! Please fix issues before committing."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Option 3: GitHub Actions

Create `.github/workflows/validate.yml`:

```yaml
name: Validate Courses

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'

      - name: Validate course content
        run: node validate-courses.js
```

### Option 4: Manual Workflow

1. **Before adding content:**
   ```bash
   node validate-courses.js  # Check current state
   ```

2. **After adding content:**
   - Add section files to `coursename/sections/`
   - Update course `index.html` with chapters
   - Update main `index.html` card

3. **Validate changes:**
   ```bash
   node validate-courses.js  # Check for issues
   ```

4. **Auto-fix if needed:**
   ```bash
   node fix-course-cards.js  # Fix common issues
   node validate-courses.js  # Verify fixes
   ```

## Troubleshooting

### Validation script not finding sections

**Problem:** Shows 0 sections even though files exist

**Solution:** Check that:
- Sections are in `coursename/sections/` directory
- Files have `.html` extension
- Directory name matches course name exactly

### Fix script not making changes

**Problem:** Says "may already be fixed"

**Solution:**
- Run `node validate-courses.js` to see current issues
- Check if HTML structure has changed
- Manually inspect the course card in index.html

### Changes not reflected after fixing

**Problem:** Validation still shows issues after running fix script

**Solution:**
- Clear browser cache
- Check that backup was deleted (should be automatic)
- Verify index.html was actually modified
- Run validation again: `node validate-courses.js`

## Maintenance

### When adding a new course:

1. Create course directory: `newcourse/`
2. Add to `COURSES` array in `validate-courses.js`:
   ```javascript
   const COURSES = [
       'matematik-1b',
       // ... existing courses
       'newcourse'  // Add here
   ];
   ```
3. Run validation to ensure proper setup

### When updating card structure:

If you change the HTML structure of course cards:

1. Update regex patterns in `validate-courses.js`
2. Update fix patterns in `fix-course-cards.js`
3. Update this documentation
4. Test on all courses

## Best Practices

### Do's ✓

- ✓ Run validation before committing
- ✓ Fix issues as soon as they appear
- ✓ Keep descriptions accurate
- ✓ Update main index when adding content
- ✓ Use consistent HTML structure

### Don'ts ✗

- ✗ Skip validation checks
- ✗ Manually edit without validating
- ✗ Leave "coming soon" on complete courses
- ✗ Add badges without content
- ✗ Copy-paste cards without updating

## Example Workflow

### Scenario: Completing a course

```bash
# 1. Initial state - course has no content
$ node validate-courses.js
# Shows: "matematik-4c: No content (correctly marked as coming soon)"

# 2. Add content files
# - Create sections/kap1-01.html, kap1-02.html, etc.
# - Update matematik-4c/index.html with chapter navigation

# 3. Validate again
$ node validate-courses.js
# Shows: "matematik-4c: HAS content but main index shows 'coming soon'"

# 4. Fix the main index
$ node fix-course-cards.js
# Removes "coming soon" message

# 5. Verify fix
$ node validate-courses.js
# Shows: "matematik-4c: No issues found"

# 6. Commit changes
$ git add .
$ git commit -m "Complete Matematik 4c course"
```

## Color Code Reference

When running `validate-courses.js`, colors indicate:

- **Green** ✓ : Everything correct
- **Yellow** ⚠ : Warning, should fix
- **Red** ✗ : Critical issue, must fix
- **Blue** : Informational
- **Cyan** : Section headers

## Support

If you encounter issues:

1. Check this README
2. Review `VALIDATION_REPORT.md`
3. Run `node validate-courses.js` for details
4. Check console output for specific errors
5. Verify file paths and structure

## Version History

- **v1.0** - Initial validation system
  - Course content detection
  - Main index validation
  - Automatic fixing capability
  - Comprehensive reporting

---

**Last Updated:** 2025-11-01
**Maintained by:** Hemsida Development Team
