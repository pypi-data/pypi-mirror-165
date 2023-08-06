import os
import re


class Rename:
    def __init__(self, root) -> None:
        self.root = root

    @staticmethod
    def _padding_zero(match):
        number = int(match.group(1))
        return format(number, "02d")

    def padding_zero(self, ext=".mp4"):
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file.endswith(ext):
                    fixed = re.sub("(\d+)", Rename._padding_zero, file, 1)
                    new_dest = os.path.join(root, fixed)
                    old_dest = os.path.join(root, file)
                    os.rename(old_dest, new_dest)

    def replace(self,  needle, ext=".mp4"):
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file.endswith(ext):
                    source = os.path.join(root, file)
                    dest = os.path.join(root, file.replace(needle, ""))
                    # ev_dest = re.sub(r'\s?(\d+-\d+-\d+\s+\d+_\d+)?(\s+\(\d+\))?_ev\s?', '', dest)
                    os.rename(source, dest)

    def replace_reg(self, reg, ext=".mp4"):
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file.endswith(ext):
                    source = os.path.join(root, file)
                    dest = re.sub(reg, '', source)
                    os.rename(source, dest)
