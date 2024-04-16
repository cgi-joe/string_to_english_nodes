# Copyright (c) 2023 Lincoln D. Stein

from typing import Literal
from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import (
    InputField,
    OutputField,
)

translate_available = False
try:
    import translators as ts
    translate_available = True
    TRANSLATORS = tuple(ts.translators_pool)
except:
    TRANSLATORS = ("google", "bing")

DEFAULT_PROMPT = "" if translate_available else "To use this node, please 'pip install --upgrade translators'"

@invocation_output("Str2EngOutput")
class Str2EngOutput(BaseInvocationOutput):
    """Translated string output"""
    prompt: str = OutputField(default=None, description="The translated prompt string")

@invocation(
    "Str2EngInvocation",
    title="String to English",
    tags=["prompt", "translate", "translator"],
    category="prompt",
    version="1.0.1",
)
class Str2EngInvocation(BaseInvocation):
    """Use the translators package to translate 330 languages into English prompts"""

    # Inputs
    text: str = InputField(default=DEFAULT_PROMPT, description="Prompt in any language")
    translator: Literal[TRANSLATORS] = InputField(default="google", description="The translator service to use")

    def invoke(self, context: InvocationContext) -> Str2EngOutput:
        translation: str = ts.translate_text(self.text, translator=self.translator)
        return Str2EngOutput(prompt=translation)