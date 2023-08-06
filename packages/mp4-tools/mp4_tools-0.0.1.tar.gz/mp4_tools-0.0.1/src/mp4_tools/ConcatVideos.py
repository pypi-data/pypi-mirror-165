import os
import re
import ffmpy


class ConcatVideos:

    def __init__(self, path, copy=False) -> None:
        self.root = path
        self.is_saved_file_copy = copy
        self._generate_dest_dir()
        self.walk_dirs()

    def _generate_dest_dir(self):
        self.dest = os.path.join(os.path.dirname(self.root),
                                 os.path.basename(self.root) + "_tmp")
        if not os.path.isdir(self.dest):
            os.mkdir(self.dest)

    def sort_files(self, video_file):
        result = re.search(r'(\d+)', os.path.basename(video_file))
        if result:
            return int(result.group())
        else:
            return video_file

    def get_all_video_files(self, files, root, basename):
        all_mp4 = []
        for f in files:
            full_path = os.path.join(root, f)
            if os.path.isfile(full_path) and f.lower().endswith(
                    '.mp4') and not f.endswith(basename + '_temp.mp4'):
                all_mp4.append(full_path)

        all_mp4.sort(key=self.sort_files)
        for mp4 in all_mp4:
            print(mp4)

        return all_mp4

    def convert_to_ts_files(self, all_mp4, root):
        for i, f in enumerate(all_mp4):
            saved_file_ts = os.path.join(root, str(i) + '.ts')
            if os.path.isfile(saved_file_ts):
                continue
            saved_file_temp_config = "-c:v copy" if self.is_saved_file_copy else "-c copy -bsf:v h264_mp4toannexb -f mpegts"
            ff = ffmpy.FFmpeg(
                global_options="-hide_banner -loglevel panic -y",
                inputs={f: None},
                # mkv to ts outputs={ saved_file_ts: "-c:v copy" })
                outputs={
                    #saved_file_ts: "-c:v copy"
                    saved_file_ts: saved_file_temp_config
                })
            ff.run()

    def concat_mp4_files(self, root, all_mp4, saved_file_temp):
        new_ts_files = [
            os.path.join(root, str(i)) + '.ts' for i in range(len(all_mp4))
        ]
        concat_files = 'concat:' + '|'.join(new_ts_files)
        saved_file_temp_config = "-c:v copy" if self.is_saved_file_copy else "-c copy -bsf:a aac_adtstoasc -movflags +faststart -y"

        ff = ffmpy.FFmpeg(
            global_options="-hide_banner -loglevel panic -y",
            inputs={concat_files: None},
            # mkv to ts outputs={ saved_file_temp: "-c:v copy" })
            outputs={
                saved_file_temp: saved_file_temp_config
            })
        ff.run()

    def walk_dirs(self):
        for root, dirs, files in os.walk(self.root):
            if root != self.root:
                output = os.path.basename(os.path.normpath(root))
                saved_file_temp = os.path.join(self.dest, output + '.mp4')
                print(saved_file_temp)

                all_mp4 = self.get_all_video_files(files, root, output)
                self.convert_to_ts_files(all_mp4, root)
                self.concat_mp4_files(root, all_mp4, saved_file_temp)

                if os.path.isfile(saved_file_temp):
                    for i, f in enumerate(all_mp4):
                        saved_file_ts = os.path.join(root, str(i) + '.ts')
                        if os.path.isfile(saved_file_ts):
                            os.remove(saved_file_ts)


if __name__ == "__main__":
    ConcatVideos("E:\\BaiduNetdiskDownload")
