# Twitch Online Video

An online streaming website that includes many anchors and online information.We can conduct data mining and analysis,
ultimately enabling AI model prediction

```
firefox catalog:
--- catalog or file
	|-- get_twitch_data.py        Click on this file to obtain the core summary information of this page
    |-- download_twitch_ts.py     Concurrent.futures.ThreadPoolExecutor for downloading
	|-- twitch_ts_to_mp4.py       Many ts converted mp4 at local path
```

# prepare

You need to put ../scripts/chromedriver.exe into your local python jdk environment scripts

# Test

FireFox-Google-Browser:   **[Twitch Online Video](https://www.twitch.tv/directory?sort=VIEWER_COUNT)**

You can click F12 from pages, which can get require element-id class and css (first floor element)