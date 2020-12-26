# Random Chooser
A simple program that uses [RANDOM.ORG](http://random.org)'s API to generate
true random choices.

If RANDOM.ORG is unavailable at the moment, the program will use `random.randint` to
generate pseudo-random choices.

## Command

To customize, run the file with the following command:
```
python random_chooser.py [file=<filename>] [how_much=<how_much>] [repeated=(True|False)] [debug=(True|False)]
```
`file`: Source file to get choices from. The choices **cannot** include spaces, and each choice have to be 
written **on a separate line**. A choice can be "weighted" with a space and an integer following the choice. For example:
```
choice1
choice2 12
```
adds **one** "choice1" and **twelve** "choice2" to the pool.

`how_much`: The number of choices to choose.

`repeated`: Whether the choices are repeated or not. **Note:** Using weights will create repeated results in
spite of this switch being set to `False`.

`debug`: Changing this to `True` will let the program print the processed pool (with weights added) after 
showing the results.

## Example

To generate 10 choices from `custom_file.abc` non-repeatedly:

```
python random_chooser.py file=custom_file.abc repeated=False how_much=10
