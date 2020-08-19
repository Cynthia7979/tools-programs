# EmotionType Record Statistics
So this one is used to analyze my emotion, recorded every half hour in an .xlsx file.

`emotion_record.xlsx` is randomly colored for testing and demonstration.
You can download this file for your own use if needed.

To run the program in test mode (to use `/emotion_record.xlsx`), change `main(test=False)` to `main(test=True)`.
To specify your own file, change `PATH_` to your own file path.

Change `show_misc` or `show_happy` to `False` if they take up too much space in emotion type statistics.
Do the opposite if you would like to see how much space do `HAPPINESS` or `MISC_EMOTIONS` take.

*Important Notes*
* `NONE` emotion (uncolored cell) is NOT counted as ANY of the 5 emotion types (happiness, anxiety/fear, anger, sadness, and misc).
It is also not counted when calculating average emotion values.