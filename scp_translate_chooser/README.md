# SCP Translate Chooser

This is a simple web crawler done with request and BeautifulSoup 
that can help me to find those SCP entries on [SCP Main Site](http://scp-wiki.net)
that haven't been translated into Chinese.

UPDATE:

I made the windows terminal command work, so you can now use the program with the following command (under Windows cmd):

```
python scp_translate_chooser.py minimum_scp_number maximum_scp_number total_entries_chosen [precise_mode]
```

`minimum_scp_number`  -  The smallest SCP number you want to search, integer.

`maximum_scp_number`  -  The largest SCP number you want to search, integer.

`total_entries_chosen` - The total number of entries to return, integer.

**Note:** In non-precise mode, the program will return this number of entries found firstly in the range given,
sorted by length. If you want the shortest entries within all articles, please check the `precise_mode`.

`precise_mode`    -      Allows the program to go through every entry in range, 
then choose the shortest ones, bool value (True or False).

UPDATE:

I updated the mechanism. Now it can process about 50~100 pages a second, however has to retry multiple times.
