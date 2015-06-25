#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Support for formatting a data pack file used for platform agnostic resource
files.

NOTE: this module was modified from the original by Joshua "jduck" Drake
(the original file lives in grit/grit/format/data_pack.py). Further, unecessary
components of grit were eliminated from this distribution.
"""

import collections
import os
import struct
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'grit'))
from grit import util


PACK_FILE_VERSION = 4
HEADER_LENGTH = 2 * 4 + 1  # Two uint32s. (file version, number of entries) and
                           # one uint8 (encoding of text resources)
BINARY, UTF8, UTF16 = range(3)


class WrongFileVersion(Exception):
  pass


DataPackContents = collections.namedtuple(
    'DataPackContents', 'resources encoding')


def ReadDataPack(input_file):
  """Reads a data pack file and returns a dictionary."""
  data = util.ReadFile(input_file, util.BINARY)
  original_data = data

  # Read the header.
  version, num_entries, encoding = struct.unpack('<IIB', data[:HEADER_LENGTH])
  if version != PACK_FILE_VERSION:
    print 'Wrong file version in ', input_file
    raise WrongFileVersion

  resources = {}
  if num_entries == 0:
    return DataPackContents(resources, encoding)

  # Read the index and data.
  data = data[HEADER_LENGTH:]
  kIndexEntrySize = 2 + 4  # Each entry is a uint16 and a uint32.
  for _ in range(num_entries):
    id, offset = struct.unpack('<HI', data[:kIndexEntrySize])
    data = data[kIndexEntrySize:]
    next_id, next_offset = struct.unpack('<HI', data[:kIndexEntrySize])
    resources[id] = original_data[offset:next_offset]

  return DataPackContents(resources, encoding)


def WriteDataPackToString(resources, encoding):
  """Returns a string with a map of id=>data in the data pack format."""
  ids = sorted(resources.keys())
  ret = []

  # Write file header.
  ret.append(struct.pack('<IIB', PACK_FILE_VERSION, len(ids), encoding))
  HEADER_LENGTH = 2 * 4 + 1            # Two uint32s and one uint8.

  # Each entry is a uint16 + a uint32s. We have one extra entry for the last
  # item.
  index_length = (len(ids) + 1) * (2 + 4)

  # Write index.
  data_offset = HEADER_LENGTH + index_length
  for id in ids:
    ret.append(struct.pack('<HI', id, data_offset))
    data_offset += len(resources[id])

  ret.append(struct.pack('<HI', 0, data_offset))

  # Write data.
  for id in ids:
    ret.append(resources[id])
  return ''.join(ret)


def WriteDataPack(resources, output_file, encoding):
  """Writes a map of id=>data into output_file as a data pack."""
  content = WriteDataPackToString(resources, encoding)
  with open(output_file, 'wb') as file:
    file.write(content)


# Temporary hack for external programs that import data_pack.
# TODO(benrg): Remove this.
class DataPack(object):
  pass
DataPack.ReadDataPack = staticmethod(ReadDataPack)
DataPack.WriteDataPack = staticmethod(WriteDataPack)
