/**
 * Course Content Validation Script
 *
 * This script validates course content consistency across the Hemsida project.
 * It checks for mismatches between actual course content and the main index.html
 * descriptions, ensuring users see accurate information about course availability.
 *
 * Usage: node validate-courses.js
 */

const fs = require('fs');
const path = require('path');

// Define all courses
const COURSES = [
    'matematik-1b',
    'matematik-2b',
    'matematik-3b',
    'matematik-1c',
    'matematik-2c',
    'matematik-3c',
    'fysik-1',
    'fysik-2'
];

// Color codes for console output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    bold: '\x1b[1m'
};

/**
 * Count section files for a course
 */
function countSectionFiles(courseName) {
    const sectionsDir = path.join(__dirname, courseName, 'sections');

    if (!fs.existsSync(sectionsDir)) {
        return 0;
    }

    const files = fs.readdirSync(sectionsDir);
    return files.filter(f => f.endsWith('.html')).length;
}

/**
 * Extract topics from course index.html
 */
function extractCourseTopics(courseName) {
    const indexPath = path.join(__dirname, courseName, 'index.html');

    if (!fs.existsSync(indexPath)) {
        return { hasContent: false, topics: [], chapters: [] };
    }

    const content = fs.readFileSync(indexPath, 'utf-8');

    // Check if it's a "coming soon" page
    const hasComingSoon = content.includes('Innehåll kommer snart!');

    // Extract chapter titles (looking for navigation menu items or chapter cards)
    const chapterRegex = /Kapitel \d+[:\-]\s*([^<]+)/g;
    const chapters = [];
    let match;

    while ((match = chapterRegex.exec(content)) !== null) {
        chapters.push(match[0].trim());
    }

    // Extract section links
    const sectionRegex = /href="sections\/[^"]+">([^<]+)<\/a>/g;
    const sections = [];

    while ((match = sectionRegex.exec(content)) !== null) {
        sections.push(match[1].trim());
    }

    return {
        hasContent: !hasComingSoon && (chapters.length > 0 || sections.length > 0),
        hasComingSoon: hasComingSoon,
        chapters: chapters,
        sections: sections
    };
}

/**
 * Extract course card info from main index.html
 */
function extractMainIndexInfo(courseName) {
    const mainIndexPath = path.join(__dirname, 'index.html');
    const content = fs.readFileSync(mainIndexPath, 'utf-8');

    // Find the course card section
    const coursePattern = new RegExp(
        `<div class="chapter-card"[^>]*>([\\s\\S]*?)<h3[^>]*>${courseName.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}[\\s\\S]*?</div>`,
        'i'
    );

    const cardMatch = content.match(coursePattern);

    if (!cardMatch) {
        return { found: false };
    }

    const cardContent = cardMatch[0];

    return {
        found: true,
        hasComingSoon: cardContent.includes('Innehåll kommer snart!'),
        hasFullBadge: cardContent.includes('Fullständig kurs'),
        hasTopicsList: cardContent.includes('<ul') && cardContent.includes('</ul>'),
        description: extractDescription(cardContent),
        topics: extractTopics(cardContent)
    };
}

function extractDescription(cardHtml) {
    const match = cardHtml.match(/<p[^>]*>([^<]+)<\/p>/);
    return match ? match[1].trim() : '';
}

function extractTopics(cardHtml) {
    const topics = [];
    const topicRegex = /<li[^>]*>✓\s*([^<]+)<\/li>/g;
    let match;

    while ((match = topicRegex.exec(cardHtml)) !== null) {
        topics.push(match[1].trim());
    }

    return topics;
}

/**
 * Validate a single course
 */
function validateCourse(courseName) {
    console.log(`\n${colors.bold}${colors.blue}=== ${courseName.toUpperCase()} ===${colors.reset}`);

    const sectionCount = countSectionFiles(courseName);
    const courseInfo = extractCourseTopics(courseName);
    const mainIndexInfo = extractMainIndexInfo(courseName);

    const issues = [];
    const warnings = [];

    // Determine actual status
    const hasActualContent = sectionCount > 0 && courseInfo.hasContent;

    console.log(`\n${colors.cyan}Course Content Status:${colors.reset}`);
    console.log(`  - Section files: ${sectionCount}`);
    console.log(`  - Chapters found: ${courseInfo.chapters.length}`);
    console.log(`  - Has actual content: ${hasActualContent ? colors.green + 'YES' : colors.red + 'NO'}${colors.reset}`);
    console.log(`  - Course index says "coming soon": ${courseInfo.hasComingSoon ? colors.yellow + 'YES' : colors.green + 'NO'}${colors.reset}`);

    console.log(`\n${colors.cyan}Main Index Card Status:${colors.reset}`);
    if (mainIndexInfo.found) {
        console.log(`  - Shows "coming soon": ${mainIndexInfo.hasComingSoon ? colors.yellow + 'YES' : colors.green + 'NO'}${colors.reset}`);
        console.log(`  - Has "Fullständig kurs" badge: ${mainIndexInfo.hasFullBadge ? colors.green + 'YES' : colors.yellow + 'NO'}${colors.reset}`);
        console.log(`  - Has topics list: ${mainIndexInfo.hasTopicsList ? colors.green + 'YES' : colors.yellow + 'NO'}${colors.reset}`);
        console.log(`  - Description: "${mainIndexInfo.description}"`);
    } else {
        console.log(`  ${colors.red}Card not found in main index!${colors.reset}`);
        issues.push('Course card not found in main index.html');
    }

    // Check for inconsistencies
    console.log(`\n${colors.cyan}Validation Results:${colors.reset}`);

    if (hasActualContent && mainIndexInfo.hasComingSoon) {
        issues.push(`Course HAS content (${sectionCount} sections, ${courseInfo.chapters.length} chapters) but main index shows "Innehåll kommer snart!"`);
    }

    if (hasActualContent && !mainIndexInfo.hasFullBadge) {
        warnings.push('Course has content but is missing "Fullständig kurs" badge on main index');
    }

    if (hasActualContent && !mainIndexInfo.hasTopicsList) {
        warnings.push('Course has content but main index card does not list the actual topics/chapters');
    }

    if (!hasActualContent && mainIndexInfo.hasFullBadge) {
        issues.push('Course marked as "Fullständig kurs" but has no actual content');
    }

    if (!hasActualContent && mainIndexInfo.hasTopicsList) {
        issues.push('Main index lists topics but course has no content');
    }

    if (!hasActualContent && !mainIndexInfo.hasComingSoon) {
        warnings.push('Course has no content but main index does not show "Innehåll kommer snart!"');
    }

    // Display results
    if (issues.length === 0 && warnings.length === 0) {
        console.log(`  ${colors.green}✓ No issues found - course status is consistent${colors.reset}`);
    } else {
        if (issues.length > 0) {
            console.log(`\n  ${colors.red}${colors.bold}ISSUES (must fix):${colors.reset}`);
            issues.forEach(issue => {
                console.log(`  ${colors.red}  ✗ ${issue}${colors.reset}`);
            });
        }

        if (warnings.length > 0) {
            console.log(`\n  ${colors.yellow}${colors.bold}WARNINGS (should fix):${colors.reset}`);
            warnings.forEach(warning => {
                console.log(`  ${colors.yellow}  ⚠ ${warning}${colors.reset}`);
            });
        }
    }

    // Show detailed content if available
    if (courseInfo.chapters.length > 0) {
        console.log(`\n${colors.cyan}Chapters in course:${colors.reset}`);
        courseInfo.chapters.slice(0, 5).forEach(chapter => {
            console.log(`  - ${chapter}`);
        });
        if (courseInfo.chapters.length > 5) {
            console.log(`  ... and ${courseInfo.chapters.length - 5} more`);
        }
    }

    if (mainIndexInfo.topics && mainIndexInfo.topics.length > 0) {
        console.log(`\n${colors.cyan}Topics listed on main index:${colors.reset}`);
        mainIndexInfo.topics.forEach(topic => {
            console.log(`  - ${topic}`);
        });
    }

    return {
        courseName,
        sectionCount,
        hasActualContent,
        issues,
        warnings
    };
}

/**
 * Generate recommendations
 */
function generateRecommendations(results) {
    console.log(`\n\n${colors.bold}${colors.blue}${'='.repeat(70)}${colors.reset}`);
    console.log(`${colors.bold}${colors.blue}VALIDATION SUMMARY & RECOMMENDATIONS${colors.reset}`);
    console.log(`${colors.bold}${colors.blue}${'='.repeat(70)}${colors.reset}\n`);

    const coursesWithContent = results.filter(r => r.hasActualContent);
    const coursesWithIssues = results.filter(r => r.issues.length > 0);
    const coursesWithWarnings = results.filter(r => r.warnings.length > 0);

    console.log(`${colors.cyan}Overall Status:${colors.reset}`);
    console.log(`  - Total courses: ${results.length}`);
    console.log(`  - Courses with content: ${coursesWithContent.length}`);
    console.log(`  - Courses with issues: ${coursesWithIssues.length}`);
    console.log(`  - Courses with warnings: ${coursesWithWarnings.length}`);

    if (coursesWithIssues.length > 0) {
        console.log(`\n${colors.red}${colors.bold}CRITICAL ISSUES - Fix These First:${colors.reset}`);
        coursesWithIssues.forEach(course => {
            console.log(`\n  ${colors.red}${colors.bold}${course.courseName}:${colors.reset}`);
            course.issues.forEach(issue => {
                console.log(`    ${colors.red}✗${colors.reset} ${issue}`);
            });
        });
    }

    if (coursesWithWarnings.length > 0) {
        console.log(`\n${colors.yellow}${colors.bold}WARNINGS - Consider Fixing:${colors.reset}`);
        coursesWithWarnings.forEach(course => {
            console.log(`\n  ${colors.yellow}${colors.bold}${course.courseName}:${colors.reset}`);
            course.warnings.forEach(warning => {
                console.log(`    ${colors.yellow}⚠${colors.reset} ${warning}`);
            });
        });
    }

    console.log(`\n${colors.cyan}${colors.bold}Specific Recommendations:${colors.reset}\n`);

    results.forEach(course => {
        if (course.issues.length > 0 || course.warnings.length > 0) {
            console.log(`${colors.bold}${course.courseName}:${colors.reset}`);

            if (course.hasActualContent) {
                console.log(`  1. ${colors.green}Update main index.html card:${colors.reset}`);
                console.log(`     - Remove "Innehåll kommer snart!" message`);
                console.log(`     - Add "Fullständig kurs" badge`);
                console.log(`     - List the actual course topics/chapters`);
                console.log(`     - Update description to match actual content`);
            } else {
                console.log(`  1. ${colors.yellow}Ensure main index.html card shows:${colors.reset}`);
                console.log(`     - "Innehåll kommer snart!" message`);
                console.log(`     - No "Fullständig kurs" badge`);
                console.log(`     - No specific topics list (or generic preview)`);
            }
            console.log();
        }
    });

    if (coursesWithIssues.length === 0 && coursesWithWarnings.length === 0) {
        console.log(`${colors.green}${colors.bold}✓ All courses are properly configured!${colors.reset}\n`);
    }

    console.log(`${colors.cyan}${colors.bold}To run this validation automatically:${colors.reset}`);
    console.log(`  - Add to package.json scripts: "validate": "node validate-courses.js"`);
    console.log(`  - Run before committing: npm run validate`);
    console.log(`  - Consider adding to CI/CD pipeline`);
    console.log(`\n${colors.bold}${colors.blue}${'='.repeat(70)}${colors.reset}\n`);
}

/**
 * Main validation function
 */
function main() {
    console.log(`${colors.bold}${colors.blue}╔${'═'.repeat(68)}╗${colors.reset}`);
    console.log(`${colors.bold}${colors.blue}║${' '.repeat(15)}HEMSIDA COURSE CONTENT VALIDATOR${' '.repeat(21)}║${colors.reset}`);
    console.log(`${colors.bold}${colors.blue}╚${'═'.repeat(68)}╝${colors.reset}`);

    const results = COURSES.map(course => validateCourse(course));

    generateRecommendations(results);
}

// Run validation
main();
