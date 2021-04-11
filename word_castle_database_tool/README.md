# Word Castle Database Tool

将有道单词本XML格式转换成单词城堡的`.db`格式

也支持手动/txt录入

## Usage

## Q&A
* 为什么我导出的单词本是`.bin`格式？
    * 选择保存路径的窗口中可以下拉选择格式
* 为什么我在游戏中找不到单词 / 单词存放在哪个难度？
    * 简单难度。其他难度的单词列表是空的，我也不知道打开会发生什么（

## Research Note
### WordCastle `.db` format
Columns:
* wordId（0起，按顺序填即可）
* spell
* phoneticSymbol（音标）
* explaination（原文如此）
* sentenceEN
* sentenceCH
* pronouncationURL（原文如此）
* wordLength（字母数）
* learnedTimes（填0）
* ungraspTimes（填0）
* isFamiliar（填0）
* backupPronounciationURL（原文如此）
