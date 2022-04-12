const word1 = process.argv[2].toLowerCase(), word2 = process.argv[3].toLowerCase();

if (word1 > word2) console.log(1);
else if (word1 < word2) console.log(-1);
else console.log(0);