# Data Model for Physical AI Book

## Entities

### 1. Book
- **Description**: The overarching product, a comprehensive guide to Physical AI and humanoid robotics.
- **Fields**:
    - `id`: Unique identifier for the book.
    - `title`: "Physical AI & Humanoid Robotics: From Simulation to Reality"
    - `modules`: List of Module entities.
    - `appendices`: List of Appendix sections.
    - `code_repository_url`: URL to the companion GitHub repository.
    - `deployment_url`: URL to the deployed Docusaurus site.
- **Relationships**: Contains `Module`s and `Appendix`es. Linked to `Code Example`s.

### 2. Module
- **Description**: A major section of the book, covering a specific theme or technology area.
- **Fields**:
    - `id`: Unique identifier (e.g., "01-robotic-nervous-system").
    - `title`: Descriptive title (e.g., "The Robotic Nervous System").
    - `subtitle`: Catchy subtitle.
    - `overview`: 200-300 words summary.
    - `learning_outcomes`: List of specific learning goals.
    - `chapters`: List of Chapter entities.
    - `roadmap`: Visual representation of chapter progression.
    - `prerequisites`: Checklist of required software/knowledge.
    - `estimated_duration`: Total time to complete the module.
    - `module_project`: Description of the integrative project for the module.
- **Validation Rules**: `id` must follow `##-descriptive-title/` format. `index.md` must exist.
- **Relationships**: Belongs to `Book`, contains `Chapter`s.

### 3. Chapter
- **Description**: A unit of content within a module, focusing on a specific topic.
- **Fields**:
    - `id`: Unique identifier (e.g., "01-introduction-physical-ai").
    - `title`: Full chapter title.
    - `module_id`: Reference to parent `Module`.
    - `learning_objectives`: List of specific learning objectives for the chapter.
    - `prerequisites`: List of required knowledge/tools.
    - `estimated_time`: Time to complete the chapter.
    - `required_tools_hardware`: List of tools/hardware needed.
    - `content`: Markdown/MDX content (3000-5000 words).
    - `code_examples`: Links to relevant `Code Example`s.
    - `hands_on_tutorial`: Step-by-step instructions.
    - `troubleshooting`: Common errors and solutions.
    - `practice_exercises`: Easy, Medium, Hard exercises.
    - `summary`: Recap and next steps.
    - `additional_resources`: Links to external resources.
- **Validation Rules**: `id` must follow `##-chapter-title.md` format. Minimum word count (3000 words). No placeholders. All code functional.
- **Relationships**: Belongs to `Module`, links to `Code Example`s.

### 4. Code Example
- **Description**: Fully functional, tested code demonstrating concepts from a chapter.
- **Fields**:
    - `id`: Unique identifier (e.g., "chapter1-hello-ros2-example").
    - `chapter_id`: Reference to parent `Chapter`.
    - `package_name`: Name of the ROS 2 package.
    - `language`: Programming language (e.g., Python).
    - `features`: Description of what the example demonstrates.
    - `files`: List of files in the package (`package.xml`, `setup.py`, `launch file`, `README.md`, source files).
    - `readme_content`: Setup and usage instructions.
    - `license`: MIT.
- **Validation Rules**: Must be tested on Ubuntu 22.04. Must be functional.
- **Relationships**: Linked from `Chapter`.

### 5. User
- **Description**: The target audience for the book (student, AI practitioner, hobbyist).
- **Fields**:
    - `type`: "Student", "AI Practitioner", "Hobbyist".
    - `background`: Prior knowledge (e.g., Python background).
    - `goals`: What they aim to achieve (e.g., set up environment, implement AI, build capstone).
- **Validation Rules**: Corresponds to user stories in `spec.md`.
- **State Transitions**: Moves from "beginner" to "proficient" in topics.

### 6. Development Environment
- **Description**: The software and hardware setup required to follow the book.
- **Fields**:
    - `os`: Ubuntu 22.04 LTS.
    - `robotics_middleware`: ROS 2 Humble.
    - `simulation_platforms`: Gazebo, Unity, NVIDIA Isaac Sim.
    - `programming_languages`: Python 3.10+.
    - `hardware_requirements`: Minimum CPU, GPU, RAM, storage.
    - `docker_support`: Yes/No.
- **Validation Rules**: Must provide clear setup instructions. Must support all examples.
- **Relationships**: Used by `User` for `Code Example`s.

### 7. Robot
- **Description**: A simulated or physical robot used in examples and projects.
- **Fields**:
    - `type`: "Humanoid", "Manipulator", "Mobile".
    - `model`: URDF/SDF description.
    - `sensors`: List of attached `Sensor`s.
    - `actuators`: List of actuators.
    - `kinematics`: Description of kinematic chains.
- **Relationships**: Has `Sensor`s, performs `Action`s.

### 8. Sensor
- **Description**: Devices used by robots to perceive the environment.
- **Fields**:
    - `type`: "Camera", "LiDAR", "IMU", "Depth Camera".
    - `data_output`: Format of sensor data.
    - `simulation_model`: How it's simulated.
- **Relationships**: Belongs to `Robot`.

### 9. Action
- **Description**: A specific task or movement performed by a robot.
- **Fields**:
    - `name`: Descriptive name (e.g., "pick up red cube", "navigate to blue square").
    - `parameters`: Inputs to the action.
    - `outcome`: Expected result.
- **Relationships**: Performed by `Robot`. Triggered by `Voice Command` (for VLA).

### 10. Voice Command
- **Description**: User input in natural language, converted to robot actions by VLA systems.
- **Fields**:
    - `text`: Natural language command.
    - `transcription_service`: (e.g., Whisper).
    - `llm_planner`: The LLM used for cognitive planning.
    - `action_sequence`: The derived sequence of `Action`s.
- **Validation Rules**: Must be transcribable, understandable by LLM.
- **Relationships**: Triggers `Action`s.

### 11. Appendix
- **Description**: Supplementary material for the book.
- **Fields**:
    - `id`: Unique identifier (e.g., "hardware-guide").
    - `title`: Title of the appendix.
    - `content`: Markdown content.
- **Relationships**: Belongs to `Book`.