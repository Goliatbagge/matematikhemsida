#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improved script to split the single-page mathematics website into multiple section pages
"""

import re
import os
from bs4 import BeautifulSoup

def read_file(filepath):
    """Read file with UTF-8 encoding"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write file with UTF-8 encoding"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_sections_with_bs(html_content):
    """Extract all sections using BeautifulSoup for better parsing"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all sections with class="content-section"
    sections = soup.find_all('section', class_='content-section')

    result = []
    for section in sections:
        section_id = section.get('id', '')
        if section_id.startswith('kap'):
            # Get the section content as string
            section_content = str(section)
            # Remove the outer <section> tags to get just the inner content
            inner_content = re.sub(r'^<section[^>]*>', '', section_content)
            inner_content = re.sub(r'</section>$', '', inner_content)
            result.append((section_id, inner_content.strip()))

    return result

def extract_section_titles(html_content):
    """Extract section IDs and titles from navigation"""
    titles = {}
    # Pattern to match navigation links
    pattern = r'<a href="#(kap\d+-\d+)">([^<]+)</a>'
    matches = re.findall(pattern, html_content)
    for section_id, title in matches:
        titles[section_id] = title
    return titles

def get_header_and_nav(html_content):
    """Extract the header and navigation from original HTML"""
    # Get everything from start to hero section
    match = re.search(r'(<!DOCTYPE html>.*?</nav>)', html_content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def get_footer(html_content):
    """Extract footer from original HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    footer = soup.find('footer')
    if footer:
        return str(footer)
    # Fallback
    match = re.search(r'(<footer>.*?</footer>)', html_content, re.DOTALL)
    if match:
        return match.group(1)
    return '''<footer>
        <div class="container">
            <p>&copy; 2024 Matematik 3c Kurshemsida</p>
        </div>
    </footer>'''

def get_script_tags(html_content):
    """Extract script tags from end of body"""
    pattern = r'(<script src="script\.js"></script>.*?)</body>'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1).replace('</body>', '')
    return '<script src="../script.js"></script>'

def update_nav_links(header_nav, for_section_page=True):
    """Update navigation links to point to section pages"""
    if for_section_page:
        # For section pages in sections/ directory - use relative paths
        updated = re.sub(r'href="#(kap\d+-\d+)"', r'href="\1.html"', header_nav)
    else:
        # For index.html - point to sections/
        updated = re.sub(r'href="#(kap\d+-\d+)"', r'href="sections/\1.html"', header_nav)
    return updated

def create_section_page(section_id, section_content, titles, all_section_ids):
    """Create a complete HTML page for a section"""

    # Find current section index
    current_idx = all_section_ids.index(section_id)

    # Determine previous and next sections
    prev_section = all_section_ids[current_idx - 1] if current_idx > 0 else None
    next_section = all_section_ids[current_idx + 1] if current_idx < len(all_section_ids) - 1 else None

    # Read the original HTML to get header/footer
    original_html = read_file(r'C:\claude\Hemsida\index_original.html')
    header_nav = get_header_and_nav(original_html)
    footer = get_footer(original_html)
    script_tags = get_script_tags(original_html)

    # Update navigation links for section pages
    header_nav = update_nav_links(header_nav, for_section_page=True)

    # Update CSS and JS paths to go up one directory
    header_nav = header_nav.replace('href="styles.css"', 'href="../styles.css"')
    header_nav = header_nav.replace('src="animations.js"', 'src="../animations.js"')
    header_nav = header_nav.replace('src="graphs.js"', 'src="../graphs.js"')
    header_nav = header_nav.replace('src="script.js"', 'src="../script.js"')
    header_nav = header_nav.replace('src="hero-graphics.svg"', 'src="../hero-graphics.svg"')

    # Fix image paths in section content
    section_content = re.sub(r'src="images/', r'src="../images/', section_content)

    # Update script tags
    script_tags = script_tags.replace('src="script.js"', 'src="../script.js"')
    script_tags = script_tags.replace('src="graphs.js"', 'src="../graphs.js"')

    # Build navigation buttons
    nav_buttons = '<div class="section-navigation" style="margin: 2rem 0; display: flex; justify-content: space-between; gap: 1rem;">\n'

    if prev_section:
        prev_title = titles.get(prev_section, prev_section)
        nav_buttons += f'    <a href="{prev_section}.html" class="nav-btn prev-btn" style="padding: 0.75rem 1.5rem; background: #4a90e2; color: white; text-decoration: none; border-radius: 4px;">← Föregående: {prev_title}</a>\n'
    else:
        nav_buttons += '    <span></span>\n'

    if next_section:
        next_title = titles.get(next_section, next_section)
        nav_buttons += f'    <a href="{next_section}.html" class="nav-btn next-btn" style="padding: 0.75rem 1.5rem; background: #4a90e2; color: white; text-decoration: none; border-radius: 4px;">Nästa: {next_title} →</a>\n'
    else:
        nav_buttons += '    <span></span>\n'

    nav_buttons += '</div>\n'

    # Disqus integration
    disqus_code = f'''
<!-- Kommentarsfält -->
<div class="container" style="margin-top: 3rem; margin-bottom: 2rem;">
    <div id="disqus_thread"></div>
    <script>
        var disqus_config = function () {{
            this.page.url = window.location.href;
            this.page.identifier = '{section_id}';
        }};
        (function() {{
            var d = document, s = d.createElement('script');
            s.src = 'https://YOUR_DISQUS_SHORTNAME.disqus.com/embed.js';
            s.setAttribute('data-timestamp', +new Date());
            (d.head || d.body).appendChild(s);
        }})();
    </script>
    <noscript>Aktivera JavaScript för att se kommentarer.</noscript>
</div>
'''

    # Construct the complete page
    page = header_nav + '''<main class="container" role="main" id="main-content">
        <section id="''' + section_id + '''" class="content-section">
''' + section_content + '''
        </section>

''' + nav_buttons + '''

''' + disqus_code + '''
    </main>

    ''' + footer + '''

    ''' + script_tags + '''
</body>
</html>'''

    return page

def main():
    """Main function to split the HTML file"""
    input_file = r'C:\claude\Hemsida\index_original.html'
    output_dir = r'C:\claude\Hemsida\sections'

    print("Reading original HTML file...")
    html_content = read_file(input_file)

    print("Extracting sections with BeautifulSoup...")
    sections = extract_sections_with_bs(html_content)
    print(f"Found {len(sections)} sections")

    print("Extracting section titles...")
    titles = extract_section_titles(html_content)

    # Get all section IDs in order
    all_section_ids = [section_id for section_id, _ in sections]

    print("Creating individual section pages...")
    for section_id, section_content in sections:
        title = titles.get(section_id, section_id)
        print(f"  Creating {section_id}.html - {title}")

        page_content = create_section_page(section_id, section_content, titles, all_section_ids)
        output_file = os.path.join(output_dir, f'{section_id}.html')
        write_file(output_file, page_content)

    print(f"\nSuccessfully created {len(sections)} section pages in {output_dir}")
    print("\nSection list:")
    for i, section_id in enumerate(all_section_ids, 1):
        print(f"  {i:2d}. {section_id}: {titles.get(section_id, 'Unknown')}")

if __name__ == "__main__":
    main()
