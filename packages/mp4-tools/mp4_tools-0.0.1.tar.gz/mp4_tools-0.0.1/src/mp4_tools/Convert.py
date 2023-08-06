import ffmpy
import ffmpeg
import os
import shutil
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class ConvertThread:

    def __init__(self, source, output):
        self.source = source
        self.output = output

    def run(self):
        try:
            logger.info("Begin to convert " + self.source)
            ff = ffmpy.FFmpeg(
                global_options=['-hide_banner', '-loglevel panic'],
                inputs={self.source: None},
                outputs={self.output: '-max_muxing_queue_size 1024'})
            # print(ff.cmd)
            ff.run()
            self.check()
        except Exception as e:
            if os.path.exists(self.output):
                os.unlink(self.output)
            logger.error("Convert failed: " + self.output)

    @staticmethod
    def get_duration(source):
        prob = ffmpeg.probe(source)
        # stream = next((stream for stream in prob['streams'] if stream['codec_type'] == 'video'), None)
        return float(prob["format"]["duration"])

    def check(self):
        diff = abs(
            self.get_duration(self.source) - self.get_duration(self.output))
        if diff < 3:
            os.unlink(self.source)
        else:
            print(self.source)


class Convert:

    def __init__(self, path):
        self.path = path
        self.extensions = (".mp4", ".wmv", ".ts", ".avi", ".flv", "mkv")
        self.files_lists = []

    def r_replace(self, s, new, occurrence):
        ext = Path(s).suffix
        if ext in self.extensions:
            li = s.rsplit(ext, occurrence)
            return new.join(li)
        else:
            return s

    def walk_dirs(self, roots, save_to_path):

        Path(save_to_path).mkdir(parents=True, exist_ok=True)
        for root, dirs, files in os.walk(roots):
            # if os.path.exists(convert_path):
            #     shutil.rmtree(convert_path)
            for file in files:
                if file.lower().endswith(self.extensions):
                    new_path = root.replace(roots, save_to_path)
                    Path(new_path).mkdir(parents=True, exist_ok=True)
                    source_file = os.path.join(root, file)
                    output_file = os.path.join(new_path,
                                               self.r_replace(file, ".mp4", 1))
                    if not os.path.exists(output_file):
                        self.files_lists.append({
                            "input": source_file,
                            "output": output_file
                        })

    def replace(self, text):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.lower().endswith(self.extensions):
                    source = os.path.join(root, file)
                    dest = os.path.join(root, file.replace(text, ""))
                    os.rename(source, dest)

    def clean(self):
        for root, dirs, files in os.walk(self.path, topdown=False):
            if len(files) == 0:
                try:
                    os.rmdir(root)
                except OSError:
                    logger.error("Folder is not empty: " + root)
                    pass

    def run(self):
        save_path = self.path + '_convert'
        self.walk_dirs(self.path, save_path)
        executor = ThreadPoolExecutor(max_workers=os.cpu_count())
        # semaphore = threading.Semaphore(os.cpu_count())
        all_tasks = [
            executor.submit(ConvertThread(f['input'], f['output']).run)
            for f in self.files_lists
        ]
        wait(all_tasks)
        # for future in as_completed(all_tasks):
        #     pass
        # for f in self.files_lists:
        # semaphore.acquire()
        # task = executor.submit(ConvertThread, (f,))
        # convert = ConvertThread(f['input'], f['output'])
        #  convert.start()
        self.clean()
        return self


if __name__ == "__main__":
    path = 'D:\\Downloads\\'
    Convert(path).run()
