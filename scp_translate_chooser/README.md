# SCP Translate Chooser

This is a simple web crawler done with request and BeautifulSoup 
that can help me to find those SCP entries on [SCP Main Site](http://scp-wiki.net)
that haven't been translated into Chinese.

I made the windows terminal command to work, now you can use the program as:

`C:\Your\Path> python scp_translate_chooser.py minimum_scp_number maximum_scp_number total_etries_chosen precise_mode`

`minimum_scp_number`: The smallest SCP number you want to search, integer.

`maximum_scp_number`: The largest SCP number you want to search, integer.

`total_entries_chosen`: The total number of entries to return, integer.

**Note:** In non-precise mode, the program will return this number of entries found firstly in the range given,
sorted by length. If you want the shortest entries within all articles, please check the `precise_mode`.

`precise_mode`: Precise mode allows the program to go through every entry in range, 
then choose the shortest ones indicated by the `total_entries_chosen` argument, bool value (True or False).

Py2exe coming soon.