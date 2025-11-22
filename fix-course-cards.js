/**
 * Automatic Course Card Fixer
 *
 * This script automatically fixes the identified issues in the main index.html:
 * - Removes "Innehåll kommer snart!" from Matematik 2c and 3c cards
 *
 * Usage: node fix-course-cards.js
 * Note: Creates a backup before making changes
 */

const fs = require('fs');
const path = require('path');

const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    bold: '\x1b[1m'
};

function log(message, color = '') {
    console.log(`${color}${message}${colors.reset}`);
}

function createBackup(filePath) {
    const backupPath = filePath + '.backup';
    fs.copyFileSync(filePath, backupPath);
    log(`✓ Created backup: ${backupPath}`, colors.green);
    return backupPath;
}

function fixCourseCard(htmlContent, courseName) {
    log(`\n${colors.cyan}Fixing ${courseName} card...${colors.reset}`);

    // Pattern to find the course card and remove the "Innehåll kommer snart!" box
    // This pattern finds the div with "Innehåll kommer snart!" and removes it

    const pattern = new RegExp(
        `(<!-- ${courseName} -->.*?<h3[^>]*>${courseName}<\/h3>.*?)` +
        `(<div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 4px;">\\s*` +
        `<p style="margin: 0; color: #666; font-style: italic;">Innehåll kommer snart!<\/p>\\s*<\/div>\\s*)` +
        `(.*?<a href="${courseName.toLowerCase().replace(' ', '-')}\/index.html")`,
        'is'
    );

    if (pattern.test(htmlContent)) {
        const newContent = htmlContent.replace(pattern, '$1$3');
        log(`  ✓ Removed "Innehåll kommer snart!" message`, colors.green);
        return newContent;
    } else {
        log(`  ⚠ Pattern not found - card may already be fixed or structure changed`, colors.yellow);
        return htmlContent;
    }
}

function fixMainIndex() {
    const indexPath = path.join(__dirname, 'index.html');

    log(`${colors.bold}${colors.blue}╔${'═'.repeat(68)}╗${colors.reset}`);
    log(`${colors.bold}${colors.blue}║${' '.repeat(20)}COURSE CARD FIXER${' '.repeat(31)}║${colors.reset}`);
    log(`${colors.bold}${colors.blue}╚${'═'.repeat(68)}╝${colors.reset}`);

    // Check if file exists
    if (!fs.existsSync(indexPath)) {
        log(`\n✗ Error: index.html not found at ${indexPath}`, colors.red);
        process.exit(1);
    }

    // Create backup
    log(`\n${colors.cyan}Step 1: Creating backup...${colors.reset}`);
    const backupPath = createBackup(indexPath);

    // Read the file
    log(`\n${colors.cyan}Step 2: Reading index.html...${colors.reset}`);
    let content = fs.readFileSync(indexPath, 'utf-8');
    log(`  ✓ Read ${content.length} characters`, colors.green);

    // Fix Matematik 2c
    log(`\n${colors.cyan}Step 3: Fixing course cards...${colors.reset}`);
    const originalContent = content;

    // For Matematik 2c - look for the specific pattern
    content = content.replace(
        /<!-- Matematik 2c -->\s*<div class="chapter-card"[^>]*>[\s\S]*?<h3[^>]*>Matematik 2c<\/h3>[\s\S]*?<div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 4px;">\s*<p style="margin: 0; color: #666; font-style: italic;">Innehåll kommer snart!<\/p>\s*<\/div>/,
        function(match) {
            // Remove the "Innehåll kommer snart!" div from the match
            return match.replace(
                /<div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 4px;">\s*<p style="margin: 0; color: #666; font-style: italic;">Innehåll kommer snart!<\/p>\s*<\/div>/,
                ''
            );
        }
    );

    if (content !== originalContent) {
        log(`  ✓ Fixed Matematik 2c card`, colors.green);
    } else {
        log(`  ⚠ Matematik 2c card not changed (may already be fixed)`, colors.yellow);
    }

    const afterMat2c = content;

    // For Matematik 3c - look for the specific pattern
    content = content.replace(
        /<!-- Matematik 3c -->\s*<div class="chapter-card"[^>]*>[\s\S]*?<h3[^>]*>Matematik 3c<\/h3>[\s\S]*?<div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 4px;">\s*<p style="margin: 0; color: #666; font-style: italic;">Innehåll kommer snart!<\/p>\s*<\/div>/,
        function(match) {
            // Remove the "Innehåll kommer snart!" div from the match
            return match.replace(
                /<div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 4px;">\s*<p style="margin: 0; color: #666; font-style: italic;">Innehåll kommer snart!<\/p>\s*<\/div>/,
                ''
            );
        }
    );

    if (content !== afterMat2c) {
        log(`  ✓ Fixed Matematik 3c card`, colors.green);
    } else {
        log(`  ⚠ Matematik 3c card not changed (may already be fixed)`, colors.yellow);
    }

    // Check if any changes were made
    if (content === originalContent) {
        log(`\n${colors.yellow}No changes were made to the file.${colors.reset}`);
        log(`${colors.yellow}The issues may already be fixed, or the HTML structure has changed.${colors.reset}`);
        log(`\n${colors.cyan}Restoring from backup and exiting...${colors.reset}`);
        fs.unlinkSync(backupPath);
        log(`  ✓ Backup removed`, colors.green);
        return;
    }

    // Write the fixed content
    log(`\n${colors.cyan}Step 4: Writing changes...${colors.reset}`);
    fs.writeFileSync(indexPath, content, 'utf-8');
    log(`  ✓ Changes written to index.html`, colors.green);

    // Summary
    log(`\n${colors.bold}${colors.green}╔${'═'.repeat(68)}╗${colors.reset}`);
    log(`${colors.bold}${colors.green}║${' '.repeat(28)}SUCCESS!${' '.repeat(32)}║${colors.reset}`);
    log(`${colors.bold}${colors.green}╚${'═'.repeat(68)}╝${colors.reset}\n`);

    log(`${colors.cyan}Summary:${colors.reset}`);
    log(`  ✓ Backup created: ${backupPath}`, colors.green);
    log(`  ✓ Fixed course card issues`, colors.green);
    log(`  ✓ Changes saved to index.html`, colors.green);

    log(`\n${colors.cyan}Next steps:${colors.reset}`);
    log(`  1. Review the changes in index.html`);
    log(`  2. Test the website to ensure it looks correct`);
    log(`  3. Run: node validate-courses.js to verify fixes`);
    log(`  4. If everything looks good, delete the backup:`);
    log(`     ${colors.yellow}del ${backupPath}${colors.reset}`);
    log(`  5. If something went wrong, restore from backup:`);
    log(`     ${colors.yellow}copy ${backupPath} ${indexPath}${colors.reset}`);

    log(`\n${colors.bold}${colors.blue}${'='.repeat(70)}${colors.reset}\n`);
}

// Run the fixer
try {
    fixMainIndex();
} catch (error) {
    log(`\n${colors.red}${colors.bold}ERROR:${colors.reset} ${error.message}`, colors.red);
    log(`\n${error.stack}`, colors.red);
    process.exit(1);
}
