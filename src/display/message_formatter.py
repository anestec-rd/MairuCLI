"""
Message formatter for MairuCLI display system.

Provides template-based message formatting with placeholders.
"""

from typing import List, Dict, Any


class MessageTemplate:
    """Represents a message template with placeholders."""

    def __init__(self, template: str, required_fields: List[str]):
        """
        Initialize template with structure and required fields.

        Args:
            template: Template string with {placeholder} syntax
            required_fields: List of required field names
        """
        self.template = template
        self.required_fields = required_fields

    def format(self, **kwargs) -> str:
        """
        Populate template with provided values.

        Args:
            **kwargs: Field values to populate

        Returns:
            Formatted string

        Raises:
            KeyError: If required field is missing
        """
        # Validate required fields
        if not self.validate(**kwargs):
            missing = [f for f in self.required_fields if f not in kwargs]
            raise KeyError(f"Missing required fields: {missing}")

        return self.template.format(**kwargs)

    def validate(self, **kwargs) -> bool:
        """
        Check if all required fields are provided.

        Args:
            **kwargs: Field values to check

        Returns:
            True if all required fields present, False otherwise
        """
        return all(field in kwargs for field in self.required_fields)


class MessageFormatter:
    """Formats warning messages using templates."""

    def __init__(self):
        """Initialize message formatter with templates."""
        # Define templates for different message types
        self._danger_template = MessageTemplate(
            template=(
                "{emoji} {title} {emoji}\n"
                "{subtitle}\n"
                "\n"
                "{explanation}\n"
                "{consequence}\n"
                "\n"
                "💡 Safe alternative:\n"
                "{advice}\n"
                "\n"
                "Blocked command: {command}"
            ),
            required_fields=["emoji", "title", "subtitle", "explanation",
                           "consequence", "advice", "command"]
        )

        self._typo_template = MessageTemplate(
            template=(
                "{message}\n"
                "\n"
                "You typed: {typed_command}\n"
                "Did you mean: {correct_command}?"
            ),
            required_fields=["message", "typed_command", "correct_command"]
        )

        self._repeat_template = MessageTemplate(
            template=(
                "{emoji_line}\n"
                "{lines}"
            ),
            required_fields=["emoji_line", "lines"]
        )

    def format_danger_warning(
        self,
        title: str,
        subtitle: str,
        explanation: str,
        consequence: str,
        advice: List[str],
        command: str,
        emoji: str
    ) -> str:
        """
        Format a danger warning message.

        Args:
            title: Warning title
            subtitle: Warning subtitle
            explanation: What the command does
            consequence: Why it's dangerous
            advice: List of safe alternatives
            command: The dangerous command
            emoji: Emoji to use

        Returns:
            Formatted warning message
        """
        # Format advice list
        advice_text = "\n".join(f"  - {item}" for item in advice)

        return self._danger_template.format(
            emoji=emoji,
            title=title,
            subtitle=subtitle,
            explanation=explanation,
            consequence=consequence,
            advice=advice_text,
            command=command
        )

    def format_typo_warning(
        self,
        message: str,
        typed_command: str,
        correct_command: str
    ) -> str:
        """
        Format a typo warning message.

        Args:
            message: Fun typo message
            typed_command: What user typed
            correct_command: Correct command

        Returns:
            Formatted typo message
        """
        return self._typo_template.format(
            message=message,
            typed_command=typed_command,
            correct_command=correct_command
        )

    def format_repeat_warning(
        self,
        emoji: str,
        title: str,
        lines: List[str],
        command: str = "",
        count: int = 0
    ) -> str:
        """
        Format a repeat command warning message.

        Args:
            emoji: Emoji to display (or empty string)
            title: Warning title
            lines: List of message lines
            command: The repeated command (for placeholder replacement)
            count: Attempt count (for placeholder replacement)

        Returns:
            Formatted repeat warning message
        """
        # Format emoji line
        if emoji:
            emoji_line = f"{emoji} {title}"
        else:
            emoji_line = title

        # Format lines with placeholder replacement
        formatted_lines = []
        for line in lines:
            # Replace placeholders
            formatted_line = line.replace("{command}", command)
            formatted_line = formatted_line.replace("{count}", str(count))
            formatted_lines.append(formatted_line)

        lines_text = "\n".join(formatted_lines)

        return self._repeat_template.format(
            emoji_line=emoji_line,
            lines=lines_text
        )
