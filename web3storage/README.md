# web3.storage video performance testing

During the initial technical evaluation of web3.storage as the Livepeer storage provider I discovered two performance/reliability issues:
1. **upload time** - the file upload was fast, but I couldn't access it for some long time (~30 min), at least with the expected speed (even though the status at the web3.storage website was `Complete`)
2. **read reliability** - the read performance was good enough, but sometimes I got a timeout, which caused the video stream to stop/pause

## Quick step to reproduce the read reliability issue

To reproduce the **read reliability** issue, you can try to playback one of the uploaded steams:

```
ffplay https://bafybeibowt4rc4g2lahrl4e7esuwykfrf35ciid6i6lzbcz33czk3wzcjq.ipfs.w3s.link/cracow_video/index.m3u8
```

What I experience is that the stream stops at some point, because one of the segment cannot be downloaded in time.

## Detailed steps to reproduce both issues

### 1. Download a sample transcoded video

You can use one of the sample video I prepared or any other segmented/transcoded video.

Download and extract the sample file: https://drive.google.com/file/d/1zIQRyqun4beTcjhtuIzhkZuqQ5gtxq_9/view?usp=share_link

```
unzip cracow_video.zip && rm cracow_video.zip
```

### 2. Upload video to web3.storage

```
npm i
node put-files.js --token=$W3S_TOKEN cracow_video/
```

Files should be uploaded to web3.storage and you should see the generated CID.

```
$ node put-files.js --token=$W3S_TOKEN cracow_video/
(node:53730) ExperimentalWarning: stream/web is an experimental feature. This feature could change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
Uploading 190 files
Content added with CID: bafybeibowt4rc4g2lahrl4e7esuwykfrf35ciid6i6lzbcz33czk3wzcjq
```

### 3. Play video just after the upload

Now, we can play the uploaded video.

```
ffplay https://bafybeibowt4rc4g2lahrl4e7esuwykfrf35ciid6i6lzbcz33czk3wzcjq.ipfs.w3s.link/cracow_video/index.m3u8
```

The first issue related to the upload is that, even though the files seem to be uploaded and the web3.storage website state `Complete`, the playback fails.

```
[https @ 0x12590d8a0] HTTP error 504 Gateway Timeout=    0B f=0/0   
https://bafybeibowt4rc4g2lahrl4e7esuwykfrf35ciid6i6lzbcz33czk3wzcjq.ipfs.w3s.link/cracow_video/index.m3u8: Server returned 5XX Server Error reply
```

### 4. Play video after some time

When we wait for some time (from 15 min to a few hours) the video starts to play, but the playback always fails while reading some of the segments. The user experience the video to pause or stop and the logs indicates that the given segment could not be retrieved in time.
