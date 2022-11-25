# for system
import sys
import time
import threading
# for wave
import wave
# for azure
import azure.cognitiveservices.speech as speechsdk

class local_info:
    def __init__(self, host):
        self.name = 'local'
        self.host = host
        self.language = "ko-KR"
    def __del__(self):
        pass
class cloud_info:
    def __init__(self, speech_key=None, service_region=None):
        self.name = 'cloud'
        self.speech_key = speech_key
        self.service_region = service_region
        self.language = "ko-KR"
    def __del__(self):
        pass

class stream_info:
    def __init__(self, sample_per_second:int=16000, bit_per_sample:int=16, channels:int=1, source:str='file', source_info:str=''):
        self.name = 'stream'
        self.sps = sample_per_second
        self.bps = bit_per_sample
        self.ch = channels
        self.src = source
        self.src_info = source_info  # insert file path when src is file
        if self.src != 'file':
            print('in stream mode, only support \'file\' source')
        else:
            pass

class file_info:
    def __init__(self, file_path):
        self.name = 'file'
        self.file_path = file_path

def speech_recognize_continuous(server_info:(cloud_info or local_info), sound_info:(stream_info or file_info)):
    speech_config = None
    if server_info.name == 'local':
        speech_config = speechsdk.SpeechConfig(host=server_info.host)
    elif server_info.name == 'cloud':
        speech_config = speechsdk.SpeechConfig(subscription=server_info.speech_key, region=server_info.service_region)
    else:
        raise Exception('server_info.name is unknown: ' + str(server_info.name))
    print('server_info.name: ' + server_info.name)

    audio_config = None
    stream = None
    if sound_info.name == 'stream':
        stream_format = speechsdk.audio.AudioStreamFormat(samples_per_second=sound_info.sps, bits_per_sample=sound_info.bps, channels=sound_info.ch)
        stream = speechsdk.audio.PushAudioInputStream(stream_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)  # using stream
    elif sound_info.name == 'file':
        audio_config = speechsdk.audio.AudioConfig(filename=sound_info.file_path)
    else:
        raise Exception('sound_info.name is unknown: ' + str(sound_info.name))
    print('sound_info.name: ' + sound_info.name)

    __accumulate_speech = ''
    __stt_done = False
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language=server_info.language)

    def push_stream_writer(stream, sound_info):
        # The number of bytes to push per buffer
        n_bytes = (sound_info.sps>>2)*(sound_info.bps>>3)  # 250ms
        print('set read {} bytes'.format(n_bytes))
        wav_fh = wave.open(sound_info.src_info)
        # start pushing data until all data has been read from the file
        try:
            while True:
                frames = wav_fh.readframes(n_bytes // 2)
                if len(frames) != n_bytes:
                    print('last read {} bytes'.format(len(frames)))
                if not frames:
                    break
                stream.write(frames)
                time.sleep(.1)
        finally:
            wav_fh.close()
            stream.close()  # must be done to signal the end of stream

    def stop_cb(evt: speechsdk.SessionEventArgs):
        nonlocal __stt_done
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        __stt_done = True

    def recognized_cb(evt: speechsdk.SessionEventArgs):
        nonlocal __accumulate_speech
        print('RECOGNIZED: {}'.format(evt))

        if __accumulate_speech == '':
            __accumulate_speech = evt.result.text
        else:
            __accumulate_speech += ' ' + evt.result.text

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    if stream != None:
        # start push stream writer thread
        push_stream_writer_thread = threading.Thread(target=push_stream_writer, args=[stream, sound_info])
        push_stream_writer_thread.start()

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not __stt_done:
        time.sleep(.1)

    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>
    
    return __accumulate_speech

def main():
    """
    __sound_file_info = file_info(file_path='FILE_PATH')
    __sound_stream_info = stream_info(source='file', source_info='FILE_PATH')

    __local_server_info = local_info(host='ws://IP_ADDR:PORT')
    __cloud_server_info = cloud_info(speech_key='Intently_Removed_Speech_Key', service_region='koreacentral')

    __speech = speech_recognize_continuous(server_info=__local_server_info, sound_info=__sound_file_info)
    print('stt result: ' + __speech)
    __speech = speech_recognize_continuous(server_info=__cloud_server_info, sound_info=__sound_file_info)
    print('stt result: ' + __speech)
    __speech = speech_recognize_continuous(server_info=__local_server_info, sound_info=__sound_stream_info)
    print('stt result: ' + __speech)
    __speech = speech_recognize_continuous(server_info=__cloud_server_info, sound_info=__sound_stream_info)
    print('stt result: ' + __speech)
    """
    print('refer example codes in comments')

if __name__ == '__main__':
    main()

