# Project Design and Architecture

This document outlines the architecture, processes, and user flows of the static site generator and the resulting blog. All diagrams are generated using Mermaid.

## Table of Contents
1.  [C4 Component Diagram](#1-c4-component-diagram)
2.  [Class Diagram](#2-class-diagram)
3.  [Sequence Diagram (Build Process)](#3-sequence-diagram-build-process)
4.  [Flowchart (Build Logic)](#4-flowchart-build-logic)
5.  [Entity Relationship Diagram](#5-entity-relationship-diagram)
6.  [State Diagram (Build State)](#6-state-diagram-build-state)
7.  [User Journey Map](#7-user-journey-map)

---

### 1. C4 Component Diagram

This diagram provides a high-level overview of the major components *within* the Static Site Generator system and how they interact during the build process.

```mermaid
C4Component
  title Refined Component diagram for Static Site Generator

  Container_Boundary(c1, "Static Site Generator") {
    Component(fs_in, "File System (Input)", "Directory", "Markdown content, templates, static assets")
    Component(parser, "Parser", "Python Module", "Reads files, parses frontmatter and markdown")
    Component(builder, "SiteBuilder", "Python Class", "Orchestrates the build, copies static files, generates search index")
    Component(renderer, "Renderer", "Python Class", "Uses Jinja2 to generate HTML, XML, and RSS files")
    Component(fs_out, "File System (Output)", "Directory", "The final generated site (`/output`)")
  }
  
  System_Ext(ci_cd, "CI/CD System", "GitHub Actions")

  Rel(ci_cd, builder, "Executes")
  Rel(builder, parser, "Uses to read and parse source files")
  Rel(builder, renderer, "Uses to render templates")
  Rel(parser, fs_in, "Reads from")

  Rel(renderer, fs_out, "Writes HTML/XML to", "Jinja2")
  Rel(builder, fs_out, "Writes JSON & copies static files to")
```

### 2. Class Diagram

This diagram shows the primary Python classes in the `src` directory, their attributes, methods, and relationships. It details the object-oriented structure of the application.

```mermaid
classDiagram
  direction LR

  class SiteBuilder {
    +site_url: str
    +output_dir: Path
    +renderer: Renderer
    +build()
    - _calculate_related_posts(list~Post~)
    - _collect_tags(list~Post~)
    - _collect_categories(list~Post~)
    - _generate_search_index(list~Post~)
  }

  class Renderer {
    -env: Jinja2.Environment
    +render_post(Post, site_url)
    +render_paginated_index(Paginator)
    +render_page(Post)
    +render_tag(Tag)
    +render_category(Category)
    +render_sitemap(list~Post~)
    +render_rss(list~Post~)
  }

  class Paginator {
    +posts: list~Post~
    +per_page: int
    +get_page(int)
  }

  class Post {
    +title: str
    +date: date
    +slug: str
    +category: str
    +tags: list~str~
    +content_html: str
    +content_raw: str
    +description: str
    +related_posts: list~Post~
    <<property>> +permalink: str
  }

  class Tag {
    +name: str
    +posts: list~Post~
    <<property>> +slug: str
  }

  class Category {
    +name: str
    +posts: list~Post~
    <<property>> +slug: str
  }

  SiteBuilder "1" *-- "1" Renderer : creates
  SiteBuilder ..> Paginator : uses
  SiteBuilder ..> Post : builds
  
  Renderer ..> Post : renders
  Renderer ..> Tag : renders
  Renderer ..> Category : renders
  Renderer ..> Paginator : renders

  Post "0..*" o-- "0..*" Post : related to
  Tag "1" o-- "0..*" Post : groups
  Category "1" o-- "0..*" Post : groups
  Paginator "1" o-- "many" Post : pages
```

### 3. Sequence Diagram (Build Process)

This diagram illustrates the sequence of interactions between the different components when the `uv run python -m src.main` command is executed.

```mermaid
sequenceDiagram
  participant User/CI
  participant main.py
  participant SiteBuilder
  participant Parser
  participant Paginator
  participant Renderer

  User/CI->>main.py: Executes `uv run python -m src.main`
  activate main.py
  main.py->>SiteBuilder: creates instance
  main.py->>SiteBuilder: calls build()
  activate SiteBuilder

  SiteBuilder->>SiteBuilder: Cleans output dir, copies static files

  loop For each markdown file in /pages and /content
      SiteBuilder->>Parser: parse_markdown_file(filepath)
      activate Parser
      Parser-->>SiteBuilder: returns Post object
      deactivate Parser
  end

  SiteBuilder->>SiteBuilder: _calculate_related_posts()
  SiteBuilder->>SiteBuilder: _collect_tags() & _collect_categories()
  
  loop For each Page object
      SiteBuilder->>Renderer: render_page(page)
      activate Renderer
      deactivate Renderer
  end

  loop For each Post object
    SiteBuilder->>Renderer: render_post(post)
    activate Renderer
    deactivate Renderer
  end
  
  SiteBuilder->>Paginator: creates instance
  activate Paginator
  Paginator-->>SiteBuilder: returns Paginator object
  deactivate Paginator
  
  SiteBuilder->>Renderer: render_paginated_index(paginator)
  SiteBuilder->>Renderer: render_sitemap()
  SiteBuilder->>Renderer: render_rss()
  SiteBuilder->>SiteBuilder: _generate_search_index()

  SiteBuilder-->>main.py: build complete
  deactivate SiteBuilder
  main.py-->>User/CI: Process finishes
  deactivate main.py
```

### 4. Flowchart (Build Logic)

While the Sequence Diagram shows object interaction, this flowchart provides a clearer view of the logical flow and decision-making within the `build()` method itself.

```mermaid
graph TD
    A[Start Build] --> B[Clean /output Directory];
    B --> C[Copy /static Directory to /output];
    C --> D[Parse All Markdown from /pages & /content];
    D --> E[Calculate Related Posts];
    E --> F[Group Posts by Tags & Categories];
    F --> G[Render Standalone Pages];
    G --> H[Render Individual Post Pages];
    H --> I[Render Tag & Category Pages];
    I --> J[Render Paginated Index Pages];
    J --> K[Render Sitemap & RSS Feeds];
    K --> L[Generate Search Index JSON];
    L --> M[End Build];
```

### 5. Entity Relationship Diagram

The ERD focuses solely on the data model, illustrating the relationships between the core content entities.

```mermaid
erDiagram
    POST {
        string title
        date date
        string slug
        string content_html
        string content_raw
        string description
        list~string~ tags
        list~string~ keywords
    }

    CATEGORY {
        string name
        string slug
    }

    TAG {
        string name
        string slug
    }

    POST }o--|| CATEGORY : "belongs to"

    POST }o--o{ TAG : "has"

    POST }o--o{ POST : "related to"
```

### 6. State Diagram (Build State)

This diagram models the different states of the build process from the moment it is triggered until it completes or fails.

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Idle
    Idle --> Initializing : Build Triggered
    
    Initializing --> Parsing : Dependencies Installed
    Parsing --> Rendering : Content Parsed
    Rendering --> Finalizing : HTML Pages Rendered
    Finalizing --> BuildComplete : Feeds & Indexes Generated
    
    BuildComplete --> [*]

    Initializing --> BuildFailed : on Error
    Parsing --> BuildFailed : on Error
    Rendering --> BuildFailed : on Error
    Finalizing --> BuildFailed : on Error
    BuildFailed --> [*]
```

### 7. User Journey Map

This diagram visualizes a typical user's experience interacting with the final, deployed blog, from discovery to engagement.

```mermaid
journey
    title A Blog Reader's Journey
    section Discovery
      Finds link on social media or search: 5: User
      Lands on a specific blog post: 5: User
    section Exploration
      Reads the article: 5: User
      Clicks on a tag to find related content: 4: User
      Reads a second article: 5: User
    section Deeper Dive
      Navigates to the Home page: 4: User
      Wants to find a specific article: 5: User
      Goes to the Search page: 5: User
      Finds the desired post via search: 5: User
    section Engagement
      Finds the post very useful: 5: User
      Uses the "Share on X" link: 4: User
      Subscribes to the RSS feed: 4: User
```
