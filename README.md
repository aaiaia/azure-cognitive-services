# azure-cognitive-services
example of azure-stt

reference: [cognitive-services-speech-sdk/samples/python/console/speech_sample.py](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/306bda0acdc85e70fdb51e43a635535df2dc580e/samples/python/console/speech_sample.py)

# azure stt
## options
`--help`

`--server_type=SERVER_TYPE(=local or cloud)`

`--push_mode=PUSH_MODE(=file or stream)`

`--stream_source=STREAM_SOURCE(=file)`: only used with `--push_mode=stream`

`--local_url=LOCAL_URL(=ws://IP_ADDR:PORT)`

`--cloud_speech_key=CLOUD_SPEECH_KEY`: only used with `--server_type=cloud`

`--cloud_service_region=CLOUD_SERVICE_REGION`: only used with `--server_type=cloud`

`--in_file=FILE_PATH`

`--test`

## RUN commands example
### for local server
```bash
$ python test_stt.py --server_type=local --local_url=ws://IP_ADDR:PORT --push_mode=file --in_file=PATH_WAV_FILE
$ python test_stt.py --server_type=local --local_url=ws://IP_ADDR:PORT --push_mode=stream --stream_source=file --in_file=PATH_WAV_FILE
```
### for cloud server
```bash
$ python test_stt.py --server_type=cloud --cloud_speech_key=INTENTLY_REMOVED --cloud_service_region=koreacentral --push_mode=file --in_file=PATH_WAV_FILE
$ python test_stt.py --server_type=cloud --cloud_speech_key=INTENTLY_REMOVED --cloud_service_region=koreacentral --push_mode=stream --stream_source=file --in_file=PATH_WAV_FILE
```
