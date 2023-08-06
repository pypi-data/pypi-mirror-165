#!/usr/bin/env python3
# encoding: utf-8
# coding style: pep8
# ====================================================
#   Copyright (C) 2022 Subconscious Compute 'All rights reserved.'
#
#   Author        : Nitish Kumar
#   Email         : nitish.hbp@gmail.com
#   File Name     : file_parsing.py
#   Last Modified : 2022-07-20 12:05
#   Describe      : this contains code that "may" be used later in the project.
#
# ====================================================
import typing as T
import re

import bitia.config 

FILE_EXTENSIONS_CSV : str = ",".join(bitia.config.supported_file_extensions())

def parse_files(cmd: str) -> T.Tuple[str, T.List[str]]:
    """Exract all the files from the passed commands either by matching against
    the file extensions or by extracting explicit file annotation by user
    e.g.`name.lst:file`.

    input: seqtk subseq in.fq name.lst:file > out.fq
    output: "seqtk subseq in.fq name.lst", ["in.fq", "name.lst"]
    """
    reg1 = rf"(?<!\>)\s\w+\.(?:{FILE_EXTENSIONS_CSV})"
    # e.g. the above expands to -> (?<!\>)\s\w+\.(?:fa|fai|fq|lst|gz|sam|bam)
    # which matches all the files with given extensions

    reg2 = r"\S+(?=:file)"  # this matches files with `:file` annotated by the user

    pattern = r":file\s*"
    list_stripped_commands = re.split(
        pattern, cmd
    )  # this strips the commands of `:file` if any
    stripped_cmds = " ".join(list_stripped_commands).strip()
    generic_reg = re.compile(f"{reg1}|{reg2}")
    files = re.findall(generic_reg, cmd)
    files = [s.strip() for s in files]
    return stripped_cmds, files


