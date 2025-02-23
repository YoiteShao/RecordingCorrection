import warnings
import re
import ffmpeg
from colorama import init, Fore, Style
from recognize_module import recognize_audio, compare_texts
from record_module import record_main

# 在文件开头添加这行代码来过滤警告
warnings.filterwarnings('ignore', category=FutureWarning, module='whisper')

STANDARD_RECORD_AUDIO = "standard_audio.wav"
MY_RECORD_AUDIO = "record_audio.wav"
OWN_CONTEXT = "own.txt"
init()


def split_standard_audio(standard_audio, start_time, end_time):
    """
    Split an audio file based on start and end timestamps.

    :param input_file: Path to the input audio file.
    :param output_file: Path to the output audio file.
    :param start_time: Start time in the format 'HH:MM:SS'.
    :param end_time: End time in the format 'HH:MM:SS'.
    """
    start_time = start_time.replace("：", ":")
    end_time = end_time.replace("：", ":")

    ffmpeg.input(standard_audio, ss=start_time, to=end_time).output(
        STANDARD_RECORD_AUDIO).run(overwrite_output=True)


def colorize_text(text):
    pattern = r'\[(.*?)\]'
    colored_text = ''
    last_end = 0

    for match in re.finditer(pattern, text):
        start, end = match.span()
        colored_text += Fore.GREEN + text[last_end:start] + Style.RESET_ALL
        colored_text += Fore.RED + '[' + match.group(1) + ']' + Style.RESET_ALL
        last_end = end

    colored_text += Fore.GREEN + text[last_end:] + Style.RESET_ALL
    return colored_text


def using_own_passage(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace('\n', '').replace('\r', '')

    return content


if __name__ == "__main__":
    """Split your standard audio if you need it"""
    # split_standard_audio('2007.06CET4.wma', "22:15", "24:40")

    """Use your audio"""
    # standard_res = recognize_audio(STANDARD_RECORD_AUDIO)["text"]
    """Use your text"""
    standard_res = using_own_passage(OWN_CONTEXT)

    # print("\n Your standard passage is:\n", standard_res, "\n")
    input("Please ready to read the passage... press any key to start...\n")

    """Read your passage"""
    record_main(MY_RECORD_AUDIO)
    my_res = recognize_audio(MY_RECORD_AUDIO)["text"]
    # print("Your recognization result:", my_res, ":\n:\nAnalysis result:\n")
    compare_res = compare_texts(standard_res, my_res)
    print_compare_res = colorize_text(compare_res)
    print(print_compare_res, "\n")
