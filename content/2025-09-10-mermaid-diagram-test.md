---
title: "Testing Mermaid Diagrams"
date: 2025-09-10
category: "Meta"
tags:
  - diagram
  - mermaid
description: "A test post to ensure Mermaid diagrams are processed correctly."
---

This post contains a Mermaid diagram. It should be rendered as an SVG, not as a plain code block.

```mermaid
graph TD
    A[Start] --> B(Process);
    B --> C{Decision};
    C -->|Yes| D[End];
    C -->|No| B;
```

This is a regular code block and should be highlighted as Python code.

```python
print("Hello, World!")
```

The diagram should appear above this final paragraph.
