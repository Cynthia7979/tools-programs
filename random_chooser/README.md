# Random Chooser
A simple program that uses [RANDOM.ORG](http://random.org)'s API to generate
true random choices.

**Note:** Repeated choices may appear.  
If RANDOM.ORG is unavailable at the moment, the program will use `random.choice` to
generate pseudo-random choices.

----

To customize, run the file with the following command in terminal:
```
python random_chooser.py <number_of_choices> [file]
```

`file` can be of any types, as long as it contains text.

For example, to generate 10 choices from `custom_file.abc`:

```
python random_chooser.py 10 custom_file.abc
```

Changing `debug_` at the end of `random_chooser.py` to `True` will let the program
show the pool. This can be used to confirm if the file is read correctly.
