import toml

def read_frontmatter(md_file: str) -> dict:
    '''
    Read the frontmatter from a markdown file

    Parameters:
    - md_file: path to the markdown file

    Returns:
    - dictionary of frontmatter key-value pairs
    '''
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.lstrip().startswith('+++'):
                _, frontmatter, _ = content.split('+++', 2)
                return toml.loads(frontmatter.strip())
            return {}
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return {}
    
def front_matter(fm: str, mag_name: str) -> str:
    '''
    Generate front matter for a markdown file

    Parameters:
    - fm: dictionary of frontmatter key-value pairs
    - mag_name: name of the magazine

    Returns:
    - string of front matter
    '''
    return f'''
    +++
    title = "{fm['title']}, Vol {fm['volume']}, No {fm['issue']}"
    date = "{fm['date']}"

    template = "post.html"

    [taxonomies]
    tags = ["{fm['title']}", "{fm['date'].split("-")[0]}"]

    [extra]
    lang = "en"
    toc = true
    comment = true
    copy = true
    math = false
    mermaid = false
    display_tags = true
    truncate_summary = false
    featured = false
    reaction = false
    +++

    ![header](/images/{mag_name}/header.png)

    '''