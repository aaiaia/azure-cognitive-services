# for system
import sys
import time
# for stt
import stt
# for Debugging
import getopt

def main(argv):
    print(argv)
    HELP_MSG = '--help, --example=[STRING], --test'

    _funcName = sys._getframe(0).f_code.co_name
    print(_funcName + ' in ' + __name__ + ' is start')

    # Define local variables
    __example = ''

    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
            "he:l:", ["help", "example=", "test"])
    except getopt.GetoptError as e: # 옵션지정이 올바르지 않은 경우
        print(e)
        print(HELP_MSG)
        sys.exit(2)

    for opt, arg in opts: # 옵션이 파싱된 경우
        if opt in ("-h", "--help"): # HELP 요청인 경우 사용법 출력
            print(HELP_MSG)
            sys.exit(2)
        elif opt in ("-e", "--example"):
            __example = arg
            print('set __example: ' + __example)
        elif opt in ("-l", "--test"):
            print('--test option is detected!')

    # Implements
    if __example != '':
        print('__example: ' + __example)
    else:
        print('__example is blank!')

    print(_funcName + ' in ' + __name__ + ' is end')

if __name__ == '__main__':
    main(sys.argv)

