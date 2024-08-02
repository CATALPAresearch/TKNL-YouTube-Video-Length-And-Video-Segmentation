

# Processing
1. Identify all 45,197 edu channels: https://www.channelcrawler.com
2. Extract metadata for the videos in each channel: `youtube-dl --dump-json --skip-download https://www.youtube.com/channel/UCYMpukYeVLigUN7SkxJ23sQ/videos >> output-urdu.json`
3. Convert the relevant metadata into a CSV table:
4. Clean the CSV data (e.g. remove duplicates, filter categories, small channels, sort by date, ...)

# Important links

* https://github.com/ytdl-org/youtube-dl
* https://www.channelcrawler.com



curl \
  'https://youtube.googleapis.com/youtube/v3/videoCategories?part=snippet&hl=es&regionCode=ES&key=xxxx' \
  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
  --header 'Accept: application/json' \
  --compressed


# Some tests

Get video duration:

youtube-dl --get-duration --get-title --get-id --skip-download --console-title https://www.youtube.com/watch?v=O2F91Up9fT8


Chanel:
youtube-dl --get-duration --get-title --get-id --skip-download --console-title https://www.youtube.com/channel/UCYMpukYeVLigUN7SkxJ23sQ/videos


**This works**
youtube-dl --dump--json --get-duration --get-title --get-id --skip-download --max-downloads 2 https://www.youtube.com/channel/UCYMpukYeVLigUN7SkxJ23sQ/videos >> output.json

---
youtube-dl --skip-download --write-info-json --download-archive archive.txt https://www.youtube.com/playlist\?list\=PLMCXHnjXnTnuFUfiWF4D0pYmJsMROz4sA |tee /dev/tty|grep "\[info] Writing video description metadata as JSON to:" |gawk '{ match($0, /-([a-zA-Z0-9_-]+)\.info\.json/, arr); if(arr[1] != "") print "youtube "arr[1] }' >> archive.txt
