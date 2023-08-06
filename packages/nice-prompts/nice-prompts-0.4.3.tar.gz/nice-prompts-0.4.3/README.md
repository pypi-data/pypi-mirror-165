# Nice-prompts.

Generate nice looking prompts for your cli applications.

[![PyPI](https://img.shields.io/pypi/v/nice-prompts?style=for-the-badge)](https://pypi.org/project/nice-prompts)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nice-prompts?style=for-the-badge)](https://pypi.org/project/nice-prompts)
[![Read the Docs](https://img.shields.io/readthedocs/nice-prompts?style=for-the-badge)](https://nice-prompts.readthedocs.io)

Install from PyPi:
```bash
$ pip3 install nice-prompts
```

### Demo (select 1, select at least 2 with max 2, select any amount):

```python3
import nice_prompts

n = nice_prompts.NicePrompt()

print(n.selection({"I like pizza": "Good taste",
    "I respectfully disagree with the opinion of liking pizza": "Fair enough, good day",
    "I hate pizza": "Bad sport 👎"})) # Select one from the keys, return the value

print(n.multiselection({"I like pizza": "Good taste",
    "I respectfully disagree with the opinion of liking pizza": "Fair enough, good day",
    "I hate pizza": "Bad sport 👎"}, amount=2, required=2)) # Select multiple from the keys, return the values. You must select 2


print(n.multiselection({"I like pizza": "Good taste",
    "I respectfully disagree with the opinion of liking pizza": "Fair enough, good day",
    "I hate pizza": "Bad sport 👎"}, required=0))  # Select multiple from the keys, return the values. No max, can be left blank

```

![Demo](https://raw.githubusercontent.com/kuroyuki-simp/nice-prompts/master/media/demo.gif)