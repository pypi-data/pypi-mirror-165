
from typing import List, Tuple, Union
from collections import defaultdict
import re
from pprint import pprint

class Splicer:
    """Specify blocks of text in files with special tags and paste them
    in other files with a different tag
    
        Usage:

            # make block:
            splice@:block1
            some text
            /splice@:block1
            
            # insert block here
            insert@:block1
    """

    def __init__(self, parse_prefix="splice@:", splice_prefix="insert@:") -> None:
        """Args:

            parse_prefix: str, prefix for starting a new block
            splice_prefix: str, prefix for pasting a block
        """
        
        self._parse_prefix = parse_prefix
        self._end_parse_prefix = f"/{self._parse_prefix}"
        self._splice_prefix = splice_prefix 
        self._segments = {}

    def __str__(self) -> str:
        return self._segments

    def parse_batch(self, files: List[str], encoding="utf-8"):
        """Parse a bunch of files at once
        
        Args:
            files: list, a list of files
            encoding: str, file encoding
        """
        for f in files:
            self.parse_segments(f, encoding=encoding)

    def splice_batch(self, files: List[Tuple[str, str]], encoding="utf-8"):
        """Splice a bunch of files at once
        
        Args:
            files: list, a list of tuples with 'filename' and 'out_filename' args 
            encoding: str, file encoding
        """
        for (f_in, f_out) in files:
            self.splice_into(f_in, f_out, encoding=encoding)

    def parse_segments(self, filename, encoding="utf-8"):
        """Parse a file for blocks

        Args:
            filename: str, path to a file
            encoding: str, file encoding
        """
        
        new_segments = defaultdict(list)
        current_segments = set()
        with open(filename, "r", encoding=encoding) as f:
            for line in f:
                if self._parse_prefix in line and self._end_parse_prefix not in line:  
                    re_seg = rf"(?<={self._parse_prefix})(.*)"
                    new_seg = re.findall(re_seg, line)[0]  
                    if new_seg in current_segments:
                        raise RuntimeError(f"'{type(self).__name__}': key '{new_seg}' appeared twice")
                    if new_seg in self._segments:
                        raise RuntimeError(f"'{type(self).__name__}': key '{new_seg}' is already present")
                    current_segments.add(new_seg)
                    continue
                if self._end_parse_prefix in line:
                    re_seg = rf"(?<={self._end_parse_prefix})(.*)"
                    end_seg = re.findall(re_seg, line)[0]
                    if end_seg not in current_segments:
                        raise RuntimeError(f"'{type(self).__name__}': cannot close never started segment '{end_seg}'")
                    current_segments.remove(end_seg)
                    continue

                for key in current_segments:
                    new_segments[key].append(line)
            if len(current_segments) != 0:
                raise RuntimeError(f"'{type(self).__name__}': segments were never closed {current_segments}")

        self._segments = self._segments | new_segments
    def add_segment_manual(self, key: str, text: Union[str, List[str]], overwrite=False):
        """Manually add a segment
        
        Args:
            key: str, segment name
            text: str or List[str], segment content
            overwrite: bool, allow overwrites of existing keys
        """
        if not isinstance(key, str):
            raise TypeError(f"'{type(self).__name__}': 'key' must be str")
        if not isinstance(key, (str, list)):
            raise TypeError(f"'{type(self).__name__}': 'text' must be str or a list")
        if key in self._segments and not overwrite:
            raise RuntimeError(f"'{type(self).__name__}': key '{key}' is already present")
        
        text = text if isinstance(text, list) else text.split("\n")
        if not text[-1].endswith("\n"):
            text[-1] = text[-1] + "\n"

        self._segments[key] = text

    def splice_into(self, filename: str, out_filename: str, encoding="utf-8"):
        """Splice parsed blocks into a file
        
        Args:
            filename: str, path to a file
            out_filename: str, path to an output file
            encoding: str, file encoding
        """
        result_text = []
        with open(filename, "r", encoding=encoding) as f:
            for line in f:
                if self._splice_prefix in line:
                    re_seg = rf"(?<={self._splice_prefix})(.*)"
                    seg_name = re.findall(re_seg, line)[0]
                    if seg_name not in self._segments:
                        raise KeyError(f"'{type(self).__name__}': no '{seg_name}' found")
                    result_text += self._segments[seg_name]
                    continue
                result_text.append(line)
                
        with open(out_filename, "w", encoding=encoding) as f:
            f.writelines(result_text)

    def clear_segments(self):
        """Delete all parsed segments"""
        self._segments = {}
