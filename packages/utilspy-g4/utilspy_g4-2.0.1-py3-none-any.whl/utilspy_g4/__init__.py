import os
import cv2
import glob
import ffmpeg


def add_ext(path: str, ext: str) -> str:
    """
    Add ext to path

    :param path: Path to file
    :param ext: Added ext
    :rtype: str
    :return: Path with added ext
    """

    path_ext = os.path.splitext(path)
    return path_ext[0] + '.' + ext + path_ext[1]


def compare_frames(frame_path_1: str, frame_path_2: str) -> bool:
    """
    Compare 2 frames

    :param frame_path_1: Path to frame 1
    :param frame_path_2: Path to frame 2
    :return: bool
    """

    # TODO: Check different frames size

    frame_1 = cv2.imread(frame_path_1)
    frame_2 = cv2.imread(frame_path_2)
    diff = cv2.norm(frame_1, frame_2, cv2.NORM_L2)

    if diff == 0.0:
        return True

    return False


def del_ext(path: str, ext_count: int = 1) -> str:
    """
    Del ext from path

    :param path: Path to file
    :param ext_count: Count of deleted ext
    :rtype: str
    :return: Path without ext
    """

    path_no_ext = path
    for _ in range(ext_count):
        path_no_ext = os.path.splitext(path_no_ext)[0]

    return path_no_ext


def templated_remove_files(template: str) -> None:
    """
    Remove files by template

    :param template: Template
    :return: None
    """

    remove_files = glob.iglob(template)

    for file in remove_files:
        os.remove(file)


def get_ext(path: str, ext_count: int = 1) -> str:
    """
    Return file extension from path

    :param path: Path to file
    :param ext_count: Count of returned extension
    :rtype: str
    :return: Extension
    """

    path_no_ext = path
    last_ext = ''
    for _ in range(ext_count):
        split_path = os.path.splitext(path_no_ext)
        path_no_ext = split_path[0]
        last_ext = split_path[1]

    if last_ext != '':
        # Del .
        last_ext = last_ext[1:]

    return last_ext


def concat_video(in_path_1: str, in_path_2: str, out_path: str):
    """
    Concat 2 video files with same codecs (it use ffmpeg)
    :param in_path_1: Path to 1 input video file
    :param in_path_2: Path to 2 input video file
    :param out_path: Path to output video file
    :return: None
    """

    ffmpeg.input(f'concat:{in_path_1}|{in_path_2}')\
        .output(out_path, vcodec='copy', acodec='copy')\
        .overwrite_output()\
        .run(quiet=True)


def get_files_count(files_template: str) -> int:
    """
    Get files count from filesTemplate
    :param files_template:
    :return: Files count from files_template
    """

    files = glob.iglob(files_template)

    i = 0
    for _ in files:
        i += 1

    return i


def int_to_2str(number: int) -> str:
    """
    Convert integer to 2 chars string with 0
    :param number: 1 or 2 digit integer number
    :return: 2 chars number with 0
    """

    if number < 10:
        return '0' + str(number)

    return str(number)
