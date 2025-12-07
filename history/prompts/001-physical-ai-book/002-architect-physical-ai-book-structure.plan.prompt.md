---
id: 002
title: Architect Physical AI Book Structure
stage: plan
date: 2025-12-07
surface: agent
model: gemini
feature: 001-physical-ai-book
branch: 001-physical-ai-book
user: siddi
command: /sp.plan
labels: [plan, architecture, documentation]
links:
  spec: ../../specs/001-physical-ai-book/spec.md
  plan: ../../specs/001-physical-ai-book/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/001-physical-ai-book/plan.md
tests:
  - none
---

## Prompt

/sp.plan ## Architecture Sketch

### Book Structure (REVISED)
physical-ai-book/ ├── docs/ │ ├── intro.md # Course overview │ │ │ ├── 01-robotic-nervous-system/ # Module 1 │ │ ├── index.md # Module 1 overview and learning path │ │ ├── 01-introduction-physical-ai.md │ │ ├── 02-ros2-architecture.md │ │ ├── 03-ros2-python-development.md │ │ └── 04-urdf-robot-modeling.md │ │ │ ├── 02-digital-twin/ # Module 2 │ │ ├── index.md # Module 2 overview │ │ ├── 05-gazebo-fundamentals.md │ │ ├── 06-physics-simulation.md │ │ └── 07-unity-integration.md │ │ │ ├── 03-ai-robot-brain/ # Module 3 │ │ ├── index.md # Module 3 overview │ │ ├── 08-nvidia-isaac-sim.md │ │ ├── 09-isaac-ros-perception.md │ │ └── 10-nav2-path-planning.md │ │ │ ├── 04-vision-language-action/ # Module 4 │ │ ├── index.md # Module 4 overview │ │ ├── 11-voice-to-action.md │ │ ├── 12-llm-cognitive-planning.md │ │ └── 13-capstone-autonomous-humanoid.md │ │ │ ├── appendices/ │ │ ├── hardware-guide.md │ │ ├── troubleshooting.md │ │ ├── cloud-setup.md │ │ └── resources.md │ │ │ └── glossary.md │ ├── code-examples/ # Separate repository ├── src/ # Docusaurus components ├── static/ # Images, videos, assets ├── docusaurus.config.js ├── sidebars.js └── package.json



### Folder Naming Convention
- **Format**: `##-descriptive-module-title/` (e.g., `01-robotic-nervous-system/`)
- **Module Index**: Each module folder MUST contain `index.md` as entry point
- **Chapter Files**: `##-chapter-title.md` format within module folders
- **No Generic Names**: Never use "module-1", "module-2" - always use descriptive titles

### Module Index File Purpose
Each `index.md` serves as:
1. **Module Landing Page**: Overview of what students will learn
2. **Learning Path**: Visual roadmap of chapters in this module
3. **Prerequisites Check**: What students need before starting
4. **Module Outcomes**: What students will build/achieve
5. **Estimated Time**: How long this module takes to complete
6. **Navigation Hub**: Links to all chapters in logical order

## Content Generation Strategy

### AI Writing Instructions

**CRITICAL RULE**: When AI generates content, it must produce COMPLETE, READY-TO-PUBLISH content, NOT placeholders.

### ❌ NEVER Generate This:
````markdown
Chapter 1: Introduction to Physical AI
This chapter will introduce the concept of Physical AI and its importance in modern robotics.
TODO: Write the detailed content for Chapter 1.
````

### ✅ ALWAYS Generate This:
````markdown
# Introduction to Physical AI

## Learning Objectives
By the end of this chapter, you will:
- Understand what Physical AI is and how it differs from traditional AI
- Recognize the key components of embodied intelligence systems
- Identify real-world applications of Physical AI in robotics
- Set up your development environment for the course

## Prerequisites
- Python programming fundamentals
- Basic understanding of AI/ML concepts
- Ubuntu 22.04 LTS installed (or Docker)
- 8GB+ RAM available

## Estimated Time: 2 hours

---

## What is Physical AI?

Physical AI represents a fundamental shift in artificial intelligence—moving from systems that exist purely in digital space to AI that understands and operates in the physical world. Unlike traditional AI models that process text, images, or abstract data, Physical AI systems must:

- **Perceive** the 3D environment through sensors (cameras, LIDAR, IMUs)
- **Reason** about physical constraints like gravity, friction, and momentum
- **Act** through motors, actuators, and mechanical systems
- **Learn** from real-world interactions and consequences

[Continue with 3000-5000 words of complete, detailed content...]

## Hands-On: Installing ROS 2 Humble

Let's get your environment ready for Physical AI development.

### Step 1: Set Up Ubuntu 22.04

Open your terminal and update your system:
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Add ROS 2 Repository

[Complete, tested, step-by-step instructions...]

## Summary

In this chapter, we've covered:
- The definition and scope of Physical AI
- How it differs from traditional AI systems
- Real-world applications in robotics
- Your development environment setup

In the next chapter, we'll dive into ROS 2 architecture and understand how robots communicate internally.

## Practice Exercises

1. **Environment Verification**: Run `ros2 --version` and confirm you see "humble" in the output...
2. **Concept Check**: Write a 200-word explanation of how Physical AI differs from LLMs...

## Additional Resources
- [ROS 2 Official Documentation](https://docs.ros.org/en/humble/)
- [NVIDIA Physical AI Research](https://research.nvidia.com/labs/srl/)
````

## Writing Phases

### Phase 1: Module Index Creation (Per Module)
**Output**: Complete `index.md` file for each module

**Content Requirements**:
1. **Module Title & Subtitle** (H1)
   - Example: "# Module 1: The Robotic Nervous System
     *Mastering ROS 2 for Robot Control*"

2. **Module Overview** (200-300 words)
   - What this module covers
   - Why it matters for Physical AI
   - Real-world relevance

3. **Learning Outcomes** (5-7 bullet points)
   - Specific, measurable outcomes
   - Tied to hands-on projects

4. **Module Roadmap** (Visual chapter list)
````markdown
   ## Chapters in This Module
   
   1. **[Introduction to Physical AI](./01-introduction-physical-ai.md)** - 2 hours
      - Understand embodied intelligence
      - Set up development environment
   
   2. **[ROS 2 Architecture](./02-ros2-architecture.md)** - 3 hours
      - Master nodes, topics, and services
      - Build your first ROS 2 package
````

5. **Prerequisites** (Checklist format)
   - Software installed
   - Prior knowledge
   - Hardware available

6. **Estimated Duration**
   - Total module time
   - Per-chapter breakdown

7. **Module Project Preview**
   - What students will build
   - Example screenshot or diagram

### Phase 2: Chapter Content Creation (Per Chapter)
**Output**: Complete 3000-5000 word chapter with working code

**Mandatory Sections** (in order):
1. **Front Matter**
   - Title (H1)
   - Learning objectives (3-5 items)
   - Prerequisites
   - Estimated time
   - Required tools/hardware

2. **Conceptual Introduction** (500-800 words)
   - Why this topic matters
   - Real-world context
   - Connection to previous chapter

3. **Core Concepts** (800-1200 words)
   - Detailed explanations
   - Architecture diagrams (Mermaid)
   - Technical terminology
   - Key principles

4. **Hands-On Tutorial** (1500-2500 words)
   - Step-by-step instructions
   - Complete code examples (not snippets)
   - Configuration files
   - Expected outputs with screenshots
   - Verification steps

5. **Deep Dive** (500-800 words)
   - Advanced details
   - Performance considerations
   - Best practices
   - Common patterns

6. **Troubleshooting** (300-500 words)
   - 5+ common errors with solutions
   - Debugging techniques
   - How to get help

7. **Practice Exercises** (300-500 words)
   - 3 exercises: Easy, Medium, Hard
   - Clear acceptance criteria
   - Starter code links

8. **Summary** (200-300 words)
   - Recap key points
   - Preview next chapter
   - Additional resources (3-5 links)

### Phase 3: Code Examples Creation (Parallel to Writing)
**Output**: Fully functional, tested code in separate repository

**Requirements**:
- Each tutorial has corresponding code directory
- README.md with setup instructions
- requirements.txt or package.xml
- Tested on Ubuntu 22.04
- Licensed appropriately (MIT)

## AI Generation Workflow

### Step 1: Generate Module Index
**Prompt Format**:
/sp.write Module 1 Index Generate COMPLETE index.md for Module 1: The Robotic Nervous System (ROS 2)

Include:

Full module overview (250 words)
7 specific learning outcomes
Visual chapter roadmap with descriptions
Prerequisites checklist
4-week timeline estimate
Module project preview: "Voice-Controlled Robot Arm"
Do NOT use placeholders. Write complete, publication-ready content.



### Step 2: Generate Chapter Content
**Prompt Format**:
/sp.write Chapter 1 - Introduction to Physical AI

Generate COMPLETE chapter content (3500-4000 words) including:

Front matter with learning objectives
Conceptual overview of Physical AI (600 words)
Core concepts: embodied intelligence, sensor-motor loops (900 words)
Hands-on tutorial: Installing ROS 2 Humble on Ubuntu 22.04 (1800 words)
Include complete bash commands
Show expected terminal outputs
Add verification steps
Deep dive: Why ROS 2 vs ROS 1 (500 words)
Troubleshooting: 5 common installation errors with solutions
3 practice exercises with acceptance criteria
Summary and next steps
Do NOT write "TODO" or placeholders. Every section must be complete and ready for students to follow.



### Step 3: Generate Code Examples
**Prompt Format**:
/sp.code Chapter 1 - Hello ROS 2 Example

Create complete, tested ROS 2 package:

Package name: hello_physical_ai
Language: Python
Features: Simple publisher/subscriber demo
Include: package.xml, setup.py, launch file, README.md
Comments: Explain every section for beginners
Output as file tree with complete file contents. No placeholders.



## Quality Validation Strategy

### Automated Checks (CI/CD)
````yaml
# .github/workflows/book-quality.yml
name: Book Quality Check

on: [push, pull_request]

jobs:
  content-validation:
    runs-on: ubuntu-latest
    steps:
      - name: Check for TODO placeholders
        run: |
          if grep -r "TODO:" docs/; then
            echo "ERROR: Found TODO placeholders in content"
            exit 1
          fi
      
      - name: Check for placeholder text
        run: |
          if grep -r "This chapter will" docs/; then
            echo "ERROR: Found placeholder chapter descriptions"
            exit 1
          fi
      
      - name: Verify chapter word count
        run: |
          for file in docs/**/*.md; do
            words=$(wc -w < "$file")
            if [ $words -lt 2000 ]; then
              echo "ERROR: $file has only $words words (minimum 2000)"
              exit 1
            fi
          done
      
      - name: Check for broken links
        uses: lycheeverse/lychee-action@v1
      
      - name: Build Docusaurus
        run: |
          npm install
          npm run build
````

### Manual Review Checklist
**Before marking chapter as "complete"**:
- [ ] No "TODO", "TBD", or "Coming soon" text
- [ ] No placeholder sentences like "This chapter will cover..."
- [ ] All code examples are complete and tested
- [ ] All diagrams are created (not described)
- [ ] All screenshots are captured and annotated
- [ ] Word count meets minimum (3000 words)
- [ ] At least 3 practice exercises included
- [ ] Troubleshooting section has 5+ items
- [ ] Next chapter preview written
- [ ] External links verified

## Content Templates

### Module Index Template
````markdown
# Module [X]: [Descriptive Title]
*[Compelling Subtitle]*

## Overview
[250-300 words explaining what this module covers, why it matters, and what students will build]

## Learning Outcomes
By completing this module, you will:
- [Specific outcome 1]
- [Specific outcome 2]
- [Specific outcome 3]
- [Specific outcome 4]
- [Specific outcome 5]

## Chapters

### Chapter [X.1]: [Title]
**Duration**: [X] hours | **Difficulty**: [Beginner/Intermediate/Advanced]

[2-3 sentence description of what this chapter covers]

**You'll learn:**
- [Key skill 1]
- [Key skill 2]
- [Key skill 3]

**You'll build:** [Specific project/example]

➡️ **[Start Chapter [X.1]](./[filename].md)**

---

### Chapter [X.2]: [Title]
[Repeat pattern for each chapter]

## Module Project
[Description of the integrative project that combines all chapter concepts]

**Project Requirements:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Expected Outcome:**
[Screenshot or diagram of finished project]

## Prerequisites
Before starting this module, ensure you have:
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]
- [ ] [Prerequisite 3]

## Hardware Required
- [Hardware item 1] - [Why needed]
- [Hardware item 2] - [Why needed]

## Estimated Timeline
- **Total Module Duration**: [X] weeks ([Y] hours)
- **Chapter breakdown**: 
  - Chapter [X.1]: [Y] hours
  - Chapter [X.2]: [Y] hours
  
## Getting Help
- [Link to discussion forum]
- [Link to troubleshooting guide]
- [Community Discord/Slack]

---

**Ready to begin?** Start with [Chapter [X.1]: [Title]](./[filename].d)
````

### Chapter Content Template
````markdown
# [Chapter Number]: [Full Chapter Title]

:::info Chapter Info
**Module**: [Module Name] | **Duration**: [X] hours | **Difficulty**: [Level]
:::

## Learning Objectives
By the end of this chapter, you will:
1. [Specific, measurable objective]
2. [Specific, measurable objective]
3. [Specific, measurable objective]

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]
- [Software/hardware requirement]

## What You'll Build
[1-2 sentences + image/diagram of the end result]

---

## Introduction
[500-800 words: Why this matters, real-world context, connection to previous learning]

## Core Concepts

### [Concept 1]
[Detailed explanation with diagrams]

### [Concept 2]
[Detailed explanation with diagrams]

### [Concept 3]
[Detailed explanation with diagrams]

## Hands-On Tutorial

### Step 1: [Action]
[Detailed instructions with code]
```bash
# Complete, working commands
```

**Expected Output:**
````
[Show what user should see]
Step 2: [Action]
[Continue pattern...]

Advanced Topics
[Advanced Topic 1]
[Deeper dive for interested students]

[Advanced Topic 2]
[Performance optimization, etc.]

Troubleshooting
Error: [Common Error Message]
Cause: [Why this happens] Solution: [Step-by-step fix]

[Repeat for 5+ common errors]

Practice Exercises
Exercise 1: [Title] (⭐ Easy)
Goal: [What to achieve] Instructions: [Step-by-step] Acceptance Criteria: [How to verify success] Starter Code: [Link]

Exercise 2: [Title] (⭐⭐ Medium)
[Similar pattern]

Exercise 3: [Title] (⭐⭐⭐ Hard)
[Similar pattern]

Summary
In this chapter, you learned:

[Key point 1]
[Key point 2]
[Key point 3]
You built: [Project description]

Next Steps
In the next chapter, we'll [preview], where you'll learn to [outcomes].

➡️ Continue to Next Chapter Title

Additional Resources
[Resource 1 with description and link]
[Resource 2 with description and link]
[Resource 3 with description and link]
Questions? Join the discussion in [forum link]



## Decisions Needing Documentation

### Decision 1: Module Folder Naming
**DECISION MADE**: Use descriptive names with numbering
- ✅ `01-robotic-nervous-system/`
- ✅ `02-digital-twin/`
- ✅ `03-ai-robot-brain/`
- ✅ `04-vision-language-action/`
- ❌ NOT `module-1/`, `module-2/`

**Rationale**: Descriptive names are self-documenting and more professional. URLs will be readable.

### Decision 2: Content Completeness Standard
**DECISION MADE**: Zero-tolerance for placeholders
- ✅ Every generated section must be complete
- ✅ Minimum 3000 words per chapter
- ✅ All code must be functional
- ❌ NO "TODO" or "This chapter will cover..."

**Rationale**: From your feedback - AI must generate publish-ready content, not outlines.

### Decision 3: Module Index Requirement
**DECISION MADE**: Mandatory `index.md` per module
- ✅ Every module folder has `index.md`
- ✅ Index serves as module landing page
- ✅ Includes roadmap of all chapters
- ✅ Shows learning progression

**Rationale**: Provides navigation hub and sets expectations for the module.

## Success Metrics

### Content Quality Metrics
- **Completeness**: 0 TODOs or placeholders in published content
- **Word Count**: 100% of chapters meet 3000-word minimum
- **Code Quality**: 100% of examples execute without errors
- **Link Validity**: 0 broken links in production

### Student Success Metrics  
- **Chapter Completion**: >80% complete each chapter
- **Exercise Success**: >75% complete practice exercises
- **Module Projects**: >65% complete module-end projects
- **Time Accuracy**: Actual time within 20% of estimates

## Timeline (Revised)

### Week 1: Project Setup
- Set up Docusaurus with correct folder structure
- Create all module folders with descriptive names
- Write all 4 module `index.md` files (complete, not placeholders)
- Set up CI/CD with placeholder detection

### Weeks 2-5: Module 1 (4 chapters)
- Week 2: Chapter 1 + 2
- Week 3: Chapter 3 + 4  
- Week 4: Module project + testing
- Week 5: Alpha feedback + revisions

### Weeks 6-8: Module 2 (3 chapters)
- Week 6: Chapter 5 + 6
- Week 7: Chapter 7 + module project
- Week 8: Beta testing + revisions

### Weeks 9-11: Module 3 (3 chapters)
- Week 9: Chapter 8 + 9
- Week 10: Chapter 10 + module project
- Week 11: Testing + revisions

### Weeks 12-14: Module 4 (3 chapters)
- Week 12: Chapter 11 + 12
- Week 13: Chapter 13 (Capstone) + testing
- Week 14: Final polish

### Weeks 15-16: Launch Prep
- Full book review
- Appendices completion
- Final beta testing
- Deployment automation
- Launch

---

**CRITICAL REMINDER FOR AI GENERATION**:
When you receive a prompt like `/sp.write Chapter 1`, you MUST generate:
1. Complete 3000-5000 word content
2. All sections filled in (no TODOs)
3. Working code examples (not pseudocode)
4. Actual diagrams (Mermaid code)
5. Real troubleshooting items (not "TBD")

NOT:
- Outlines
- "This chapter will cover..." descriptions
- TODO markers
- Placeholder text

## Response snapshot

An implementation plan for the "Physical AI & Humanoid Robotics Book" has been created at `specs/001-physical-ai-book/plan.md`. The plan outlines the project's technical stack, the detailed content and code repository structure, and confirms alignment with the project's constitution.

## Outcome

- ✅ Impact: High. Provides a clear architectural blueprint for the book's development, including technology choices and project structure.
- 🧪 Tests: N/A.
- 📁 Files: 
  - Modified: specs/001-physical-ai-book/plan.md
- 🔁 Next prompts: The user can now proceed with generating the tasks for the first phase of the plan using `/sp.tasks`.
- 🧠 Reflection: The detailed prompt provided a clear architectural vision, which was translated directly into the implementation plan. The separation of content and code into two repositories is a key architectural decision that will improve maintainability.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Proceed with generating the tasks for the first week of the timeline.
