# Weather Forecast Downloader

So, when I'm checking the weather on http://www.weather.com.cn, I saw this live weather forecast beside the webpage:
![图像_2020-12-29_092345.png](https://i.loli.net/2020/12/29/2IQ7ft4n9eJx1NC.png)

"It loads the video *as a file*?? That so convenient..."

"Also requires a header?..."

![图像_2020-12-29_092838.png](https://i.loli.net/2020/12/29/LfWYBitJbpFwyse.png)

Then I found [this hub](http://video.weather.com.cn/search/search.shtml?hotspot=0&forecast=1&solarTerm=0&life=0&popularScience=0) which holds basically all weather forecast page links. A perfect crawling practice.

And (boom) this project manifested.

#### *La Fine* (what)

Downloaded files will be stored in videos/, which is ignored in `.gitignore`. If you need those videos for some reasons,
please download them yourself by running the code.
