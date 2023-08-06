# SEETM 0.0.1a1 Release

### SEETM (Sinhala-English Equivalent Token Mapper) allows creating equivalent token maps and replace them with a base token to avoid OOV tokens and generate a single feature for all equivalent tokens in a Sinhala-English code-switching dataset in rasa-based conversational AIs.

## Features
- Allows mapping multiple equivalent tokens into a base token
- Fully supports rasa 2.8.x projects
- Provides an easy-to-use CLI
- Provides an efficient server-based GUI
- Provides a fully-functional custom whitespace tokenizer
- Fully-supports Sinhala in the GUI

## What's Cooking?
- Mapping suggestions in the SEETM server GUI
- Automatically generated mappings

## Limitations and Known Issues
- Should manually add the SEETM tokenizer to the rasa pipeline or else the token maps are not taking any effect
- IPA-based suggestions could contain slight changes based on th IPA mapping origin. (SEETM uses CMU)

## Resources and References
- [CMU](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) Pronunciation Dictionary
- [eng-to-ipa](https://pypi.org/project/eng-to-ipa/) pip package ([GitHub](https://github.com/mphilli/English-to-IPA))

📒 Docs: https://seetm.github.io  
📦 PyPi: https://pypi.org/project/seetn/0.0.1a1/  
🪵 Full Changelog: Refer the relevant GitHub branch (v0.0.1a1) 