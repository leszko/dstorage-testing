# dStorage testing

## Download
```
python download.py <playback_url> <output_directory>
```

## STORJ
```
uplink mb sj://readtesting
uplink cp -r output sj://readtesting
uplink share --url --not-after=none sj://readtesting
```

## web3.storage
```
cd web3-storage-quickstart
node put-files.js --token=$W3S_TOKEN ../output
cd ..
```