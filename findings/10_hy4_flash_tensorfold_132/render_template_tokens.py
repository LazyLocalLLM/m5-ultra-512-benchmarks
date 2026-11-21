"""Render a build's chat template for each thinking setting and count the prompt tokens.

    python3 render_template_tokens.py <build folder>

The folder must hold chat_template.jinja and tokenizer.json, as the two Hy4-flash MLX builds do. Needs the
tokenizers and jinja2 packages. It loads no weights and sends no request.
"""
import os
import sys

from jinja2.sandbox import ImmutableSandboxedEnvironment
from tokenizers import Tokenizer

PROMPT = ('Session probe1\n\nWrite a Python function that returns the n-th Fibonacci number, '
          'with a short docstring.')


def refuse(message):
    raise ValueError(message)


def main(folder):
    tokenizer = Tokenizer.from_file(os.path.join(folder, 'tokenizer.json'))
    environment = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
    environment.globals['raise_exception'] = refuse
    template = environment.from_string(open(os.path.join(folder, 'chat_template.jinja')).read())
    messages = [{'role': 'user', 'content': PROMPT}]
    settings = [('no setting', {}), ('reasoning_effort high', {'reasoning_effort': 'high'}),
                ('reasoning_effort no_think', {'reasoning_effort': 'no_think'}),
                ('enable_thinking false', {'enable_thinking': False})]
    for label, extra in settings:
        text = template.render(messages=messages, add_generation_prompt=True, **extra)
        count = len(tokenizer.encode(text, add_special_tokens=False).ids)
        print('{}: {} tokens, ends with {!r}'.format(label, count, text[-60:]))


if __name__ == '__main__':
    main(sys.argv[1])
