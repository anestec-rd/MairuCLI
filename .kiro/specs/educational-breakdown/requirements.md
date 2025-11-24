# Requirements Document - Educational Breakdown Mode

## Introduction

The Educational Breakdown Mode enhances MairuCLI's educational value by providing detailed, interactive explanations of dangerous commands. When users attempt dangerous commands, the system will offer to explain:
- What each part of the command means (command breakdown)
- What would happen if executed (timeline simulation)
- Real-world incidents related to the command (incident stories)

This feature addresses the common problem where CLI beginners don't understand command arguments (e.g., "What does -rf mean?" or "What is 777?") and lack concrete understanding of consequences.

## Glossary

- **System**: MairuCLI educational CLI wrapper
- **User**: Person interacting with MairuCLI
- **Dangerous Command**: Command pattern detected by the interceptor (includes both CRITICAL and CAUTION level commands)
- **Command Breakdown**: Detailed explanation of command parts and arguments
- **Timeline Simulation**: Step-by-step visualization of command execution consequences
- **Incident Story**: Real-world case study of command-related accidents
- **Educational Content**: JSON files containing breakdowns, simulations, and incidents
- **Breakdown Mode**: Interactive mode showing detailed command explanations
- **Halloween Theme**: Spooky, entertaining presentation style with emojis and humor

## Requirements

### Requirement 1: Command Breakdown Display

**User Story:** As a CLI beginner, I want to understand what each part of a dangerous command means, so that I can learn why it's dangerous.

#### Acceptance Criteria

1. WHEN the System detects a dangerous command (CRITICAL or CAUTION level), THEN the System SHALL offer to show a detailed breakdown
2. WHEN the User requests a breakdown, THEN the System SHALL display each command part with its meaning
3. WHEN displaying command parts, THEN the System SHALL include emoji indicators for danger level
4. WHEN showing the breakdown, THEN the System SHALL provide a plain-language translation of the full command
5. WHEN presenting the breakdown, THEN the System SHALL maintain the Halloween theme with appropriate emojis and humor

### Requirement 2: Timeline Simulation Display

**User Story:** As a user, I want to see what would happen if I executed a dangerous command, so that I can understand the concrete consequences.

#### Acceptance Criteria

1. WHEN the User requests a simulation, THEN the System SHALL display a step-by-step timeline of consequences
2. WHEN showing timeline events, THEN the System SHALL include timestamps (T+0s, T+1s, etc.)
3. WHEN displaying each event, THEN the System SHALL use emoji indicators for severity
4. WHEN presenting the timeline, THEN the System SHALL show progressive damage or impact
5. WHEN the simulation completes, THEN the System SHALL display a final summary message with Halloween humor

### Requirement 3: Real Incident Story Display

**User Story:** As a user, I want to learn about real-world incidents related to dangerous commands, so that I understand these are not theoretical risks.

#### Acceptance Criteria

1. WHEN the System has incident data for a pattern, THEN the System SHALL offer to show the incident story
2. WHEN displaying an incident, THEN the System SHALL include the date, company, and summary
3. WHEN showing incident details, THEN the System SHALL present a timeline of what happened
4. WHEN presenting incidents, THEN the System SHALL include the official source URL for verification
5. WHEN displaying the story, THEN the System SHALL frame it with Halloween-themed presentation

### Requirement 4: Educational Content Management

**User Story:** As a developer, I want educational content stored in structured JSON files, so that I can easily add new content without modifying code.

#### Acceptance Criteria

1. WHEN the System loads educational content, THEN the System SHALL read from JSON files in the data/educational/ directory
2. WHEN loading command breakdowns, THEN the System SHALL read from data/educational/command_breakdowns/
3. WHEN loading simulations, THEN the System SHALL read from data/educational/simulations/
4. WHEN loading incidents, THEN the System SHALL read from data/educational/incidents/
5. WHEN content files are missing, THEN the System SHALL gracefully fall back to basic warnings

### Requirement 5: Interactive Breakdown Mode

**User Story:** As a user, I want to choose what level of detail I see, so that I can control my learning experience.

#### Acceptance Criteria

1. WHEN a dangerous command is blocked, THEN the System SHALL offer three options: quick explanation, full breakdown, or skip
2. WHEN the User selects quick explanation, THEN the System SHALL display a 5-second summary
3. WHEN the User selects full breakdown, THEN the System SHALL display command breakdown, simulation, and incident story
4. WHEN the User selects skip, THEN the System SHALL return to the prompt immediately
5. WHEN displaying options, THEN the System SHALL use numbered choices for easy selection

### Requirement 6: chmod Permission Explanation

**User Story:** As a user confused by chmod numbers, I want to understand what 777, 666, 644 mean, so that I can use permissions safely.

#### Acceptance Criteria

1. WHEN the System detects a chmod command, THEN the System SHALL explain the numeric permission format
2. WHEN explaining permissions, THEN the System SHALL break down each digit (owner, group, others)
3. WHEN showing permission values, THEN the System SHALL explain what each number means (4=read, 2=write, 1=execute)
4. WHEN presenting chmod 777, THEN the System SHALL show the attack scenario (unlock → modify → lock)
5. WHEN explaining chmod, THEN the System SHALL provide safe alternative permissions

### Requirement 7: rm Command Argument Explanation

**User Story:** As a user, I want to understand what -r, -f, and / mean in rm commands, so that I know why the combination is dangerous.

#### Acceptance Criteria

1. WHEN the System detects rm with flags, THEN the System SHALL explain each flag separately
2. WHEN explaining -r, THEN the System SHALL describe recursive deletion with folder metaphor
3. WHEN explaining -f, THEN the System SHALL describe force mode and lack of confirmation
4. WHEN explaining /, THEN the System SHALL describe the root directory and its scope
5. WHEN showing the combination, THEN the System SHALL explain why together they are catastrophic

### Requirement 8: Content Scalability

**User Story:** As a developer, I want to easily add new educational content, so that the system can grow without code changes.

#### Acceptance Criteria

1. WHEN adding a new command breakdown, THEN the developer SHALL only need to create a new JSON file
2. WHEN adding a new simulation, THEN the developer SHALL only need to create a new JSON file
3. WHEN adding a new incident, THEN the developer SHALL only need to create a new JSON file
4. WHEN the System loads content, THEN the System SHALL automatically discover new files
5. WHEN content is malformed, THEN the System SHALL log an error and continue with available content

### Requirement 9: Halloween Theme Consistency

**User Story:** As a user, I want educational content to maintain the fun Halloween theme, so that learning remains entertaining.

#### Acceptance Criteria

1. WHEN displaying any educational content, THEN the System SHALL use Halloween-themed emojis (🎃, 🔥, 💀, 🐺, etc.)
2. WHEN showing serious information, THEN the System SHALL balance education with humor
3. WHEN presenting incidents, THEN the System SHALL frame them as "spooky stories" while remaining factual
4. WHEN explaining technical concepts, THEN the System SHALL use analogies related to Halloween themes
5. WHEN displaying warnings, THEN the System SHALL maintain the "Halloween Party" aesthetic (fun, not scary)

### Requirement 10: Source Attribution

**User Story:** As a user, I want to verify incident information, so that I can trust the educational content.

#### Acceptance Criteria

1. WHEN displaying an incident, THEN the System SHALL include the source URL
2. WHEN showing incident details, THEN the System SHALL include the publication date
3. WHEN presenting incidents, THEN the System SHALL clearly distinguish facts from Halloween-themed commentary
4. WHEN source URLs are available, THEN the System SHALL display them in a readable format
5. WHEN incidents are referenced, THEN the System SHALL use only verified, publicly documented cases

## Non-Functional Requirements

### Performance
- Educational content loading SHALL complete within 100ms
- Breakdown display SHALL render within 50ms
- Content files SHALL be cached after first load

### Usability
- Breakdown text SHALL be readable on 80-character terminals
- Options SHALL be numbered 1-3 for easy selection
- Educational content SHALL not exceed 30 seconds of reading time

### Maintainability
- Each command SHALL have its own JSON file
- JSON schema SHALL be documented
- Content SHALL be validated on load

### Compatibility
- Educational content SHALL work on Windows, Linux, and macOS
- JSON files SHALL use UTF-8 encoding
- Emoji SHALL have text fallbacks for unsupported terminals
