# for system
import sys
import time
# for stt
import stt as AZURE_STT
# for Debugging
import getopt

def main(argv):
    print(argv)
    HELP_MSG = '--help, --server_type=MODE(=local or cloud), --push_mode=PUSH_MODE(file or stream), --stream_source=STREAM_SOURCE(file or queue), --local_url=ws://IP_ADDR:PORT, --cloud_speech_key=KEY_VALUE, --cloud_service_region=REGION, --in_file=FILE_PATH, --test'

    _funcName = sys._getframe(0).f_code.co_name
    print(_funcName + ' in ' + __name__ + ' is start')

    # Define local variables
    __server_type = 'local'
    __push_mode = 'file'

    __stream_source = 'file'

    __local_url = 'ws://127.0.0.1:5500'

    __cloud_speech_key = ''
    __cloud_service_region = ''

    __in_file = ''

    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
            "hm:p:s:u:k:r:f:t:", [
                "help",
                "server_type=",
                "push_mode=",
                "stream_source=",
                "local_url=",
                "cloud_speech_key=",
                "cloud_service_region=",
                "in_file=",
                "test"
        ])
    except getopt.GetoptError as e: # 옵션지정이 올바르지 않은 경우
        print(e)
        print(HELP_MSG)
        sys.exit(2)

    for opt, arg in opts: # 옵션이 파싱된 경우
        if opt in ("-h", "--help"): # HELP 요청인 경우 사용법 출력
            print(HELP_MSG)
            sys.exit(2)
        elif opt in ("-m", "--server_type"):
            __server_type = arg
            print('set __server_type: ' + __server_type)
        elif opt in ("-p", "--push_mode"):
            __push_mode = arg
            print('set __push_mode: ' + __push_mode)
        elif opt in ("-s", "--stream_source"):
            __stream_source = arg
            print('set __stream_source: ' + __stream_source)
        elif opt in ("-u", "--local_url"):
            __local_url = arg
            print('set __local_url: ' + __local_url)
        elif opt in ("-k", "--cloud_speech_key"):
            __cloud_speech_key = arg
            print('set __cloud_speech_key: ' + __cloud_speech_key)
        elif opt in ("-r", "--cloud_service_region"):
            __cloud_service_region = arg
            print('set __cloud_service_region: ' + __cloud_service_region)
        elif opt in ("-f", "--in_file"):
            __in_file = arg
            print('set __in_file: ' + __in_file)
        elif opt in ("-t", "--test"):
            print('--test option is detected!')

    print('__server_type         : ' + __server_type)
    print('__push_mode           : ' + __push_mode)

    print('__stream_source       : ' + __stream_source)

    print('__local_url           : ' + __local_url)

    print('__cloud_speech_key    : ' + __cloud_speech_key)
    print('__cloud_service_region: ' + __cloud_service_region)

    print('__in_file             : ' + __in_file)

    # Implements
    try:
        __server_info = None
        if __server_type == 'local':
            __server_info = AZURE_STT.local_info(host=__local_url)
        elif __server_type == 'cloud':
            __server_info = AZURE_STT.cloud_info(speech_key=__cloud_speech_key, service_region=__cloud_service_region)
        else:
            raise Exception('server_type is unknown: ' + str(__server_type))

        __sound_info = None
        if __push_mode == 'file':
            __sound_info = AZURE_STT.file_info(file_path=__in_file)
        elif __push_mode == 'stream':
            if __stream_source == 'file':
                __sound_info = AZURE_STT.stream_info(source=__stream_source, source_info=__in_file)
            else:
                raise Exception('stream_source is unknown: ' + str(__stream_source))
        else:
            raise Exception('push_mode is unknown: ' + str(__push_mode))

        __speech = AZURE_STT.speech_recognize_continuous(server_info=__server_info, sound_info=__sound_info)
        print('stt result: ' + __speech)

    except Exception as e:
        print('Exception: ' + str(e))
    finally:
        pass

    print(_funcName + ' in ' + __name__ + ' is end')

if __name__ == '__main__':
    main(sys.argv)

