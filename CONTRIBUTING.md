# Contribution Guidelines

So you want to help? First of all, thank you!
There are few rules that we have so anyone can participate while maintaining a good workflow, teamwork, and clean code.
These are likely to get modified or added stuff to it, check them regularly.

## Github

### Pull Requests

- Try one commit per implementation.
- Any spelling mistakes will lead to immediate rejection of pull requests.
- A code that does not compile or crashes is a code that does not get merged.
- If a PR is refused it will most likely have a justification in the comments, though it is not obligatory.
- Use tags and labels.

## Code formatting and structure

### General

- Please, respect the current code architecture; if you think something should change feel free to let know.
- Personal initiative is good, but for the sake of working together in good condition, let other people know what you do or want to do before doing it.

### Naming Convention

- We will prefer using underscores for function and variable names such as my_function.
- A code with unclear function and variable names will be refused.

### Commands

- Every command must have a description.
- If there are arguments, the command should have a usage field.

### Documenting and Comments

- You need to document every function that is not a command using ''' blocs.
- Try to comment your code using comments as much as possible.
- A code that is not documented is a code that gets refused on review.

### Config and Data

- Configs go in the "config.json" file. (see config file for path).
- Any text destined to users has to go in the "strings.json" file. (see config file for path).
- Any data that needs to be written locally goes in the appropriate folder, in a new file. (use the config file for path).

### Tests

- You will not have access to the official instance of the bot.
- Feel free to recreate your discord and bot in a private server to test your code.

## Credits

If you have contributed to the bot, let people know by adding your name and the features you have implemented at the bottom of the list on the README.md.
You can also add more features beneath your name if you contribute again in the future.
