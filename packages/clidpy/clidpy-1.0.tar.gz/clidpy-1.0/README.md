# clidpy

A Python module for making CLI-configured Discord bots that respond to commands by evaluating Python expressions.

I make a surprising number of "single-serving" bots, so I figured this module would be useful for me — like `python -m http.server` but for Discord bots.

Example usage:

```sh
python -m clidpy $BOT_TOKEN "!" "wp" "'https://en.wikipedia.org/wiki/' + title.replace(' ', '_')"
```

Free variables in the expression are automatically turned into parameters using `ast`.

You can import modules with `-i` and call their functions:

```sh
python -m clidpy -i num2words $BOT_TOKEN "!" "spell" "num2words.num2words(number)"
python -m clidpy -i random $BOT_TOKEN "!" "roll" "f'Rolling a {sides}-sided die: **{random.randint(1, int(sides))}**'"
```
