# Embedded file name: chunkfile\chunk_utils.pyc
import struct
import collections


def null_termin(value):
    return repr(value[: value.find("\x00")])


char_map = "0123456789ABCDEF"


def hex_dump(value):
    string = ""
    if value and isinstance(value[0], str):
        for index, char in enumerate(value):
            if index > 0:
                string += " "
            string += char_map[ord(char) >> 4 & 15] + char_map[ord(char) & 15]

    else:
        for index, v in enumerate(value):
            if index > 0:
                string += " "
            string += char_map[v >> 4 & 15] + char_map[v & 15]

    return string


def hex_list(a):
    if not isinstance(a, collections.Iterable):
        return hex(a)
    s = ""
    for h in a:
        if s:
            s += ", "
        s += hex(h)

    return "(" + s + ")"


def strz(value):
    return value[: value.find("\x00")]


def strz_add_quotes(value):
    return "'" + value[: value.find("\x00")] + "'"


def ignorable(value):
    return "ignorable"


class FieldDef(object):

    def __init__(self, name, format, print_function=str):
        self.name = name
        self.format = format
        self.print_function = print_function

    def value_str(self, value):
        return self.print_function(value)

    def flag_set(self, name, value):
        return False


class FlagsFormatter(object):

    def __init__(self, flags):
        self.flags = flags

    def __call__(self, value):
        bits = [1 << x for x in xrange(len(self.flags))]
        values = [value & bit != 0 for bit in bits]
        digits = [{False: "0", True: "1"}[x] for x in values]
        bit_string = "".join(reversed(digits))
        flag_strings = [
            flag + "=" + digit + ", " for flag, digit in zip(self.flags, digits)
        ]
        flag_string = "".join(flag_strings)[:-2]
        known_mask = (1 << len(self.flags)) - 1
        error_string = ""
        if value & ~known_mask:
            error_string = " <UNKNOWN FLAGS SET: %.8X>" % value
        return "%s (%s)%s" % (bit_string, flag_string, error_string)


class EnumFormatter(object):

    def __init__(self, values):
        self.values = values

    def __call__(self, value):
        try:
            description = self.values[value]
        except Exception as e:
            description = "<INVALID ENUM VALUE>"

        return "%d (%s)" % (value, description)


class FlagsDef(FieldDef):

    def __init__(self, name, format, flags):
        self.flags = flags
        FieldDef.__init__(self, name, format, FlagsFormatter(self.flags))
        self.flag_map = dict([(flag, index) for index, flag in enumerate(self.flags)])

    def flag_set(self, name, value):
        return value & 1 << self.flag_map[name] != 0


class EnumDef(FieldDef):

    def __init__(self, name, format, values):
        self.values = values
        FieldDef.__init__(self, name, format, EnumFormatter(self.values))

    def get_enum_string(self, value):
        try:
            description = self.values[value]
        except Exception as e:
            description = "<INVALID ENUM VALUE (" + str(value) + ")>"

        return description


class Field(object):

    def __init__(self, field_def, value, pos):
        self.field_def = field_def
        self.value = value
        self.pos = pos

    def format(self, pos):
        if self.field_def.format:
            print(
                "%.8X:    %s = %s"
                % (
                    pos + self.pos,
                    self.field_def.name,
                    self.field_def.value_str(self.value),
                )
            )
        elif self.field_def.format is None:
            print("%s" % self.field_def.name)
        else:
            print("%.8X: %s" % (pos + self.pos, self.field_def.name))

    def flag_set(self, name):
        return self.field_def.flag_set(name, self.value)

    def get_enum_string(self):
        return self.field_def.get_enum_string(self.value)


class DataObject(object):

    def __init__(self, pos, name, fields):
        self.pos = pos
        self.name = name
        self.fields = fields
        self.name_field_map = dict(
            [(field.field_def.name, field) for field in self.fields]
        )

    def find_field(self, name):
        return self.name_field_map[name]

    def format(self, pos):
        if self.name:
            print("%.8X: %s" % (self.pos + pos, self.name))
        for field in self.fields:
            field.format(pos)


def add_chunk_header_fields(field_defs):
    field_defs.extend(
        (
            FieldDef("ChunkHeader:", ""),
            FieldDef("type", "<I", hex),
            FieldDef("version", "<I", hex),
            FieldDef("pos", "<i", ignorable),
            FieldDef("id", "<i", hex),
            FieldDef("", None),
        )
    )


def cumulative_sum(seq):
    csum = []
    total = 0
    for val in seq:
        total += val
        csum.append(total)

    return csum


def remove_endianness(s):
    return "".join((c for c in s if c not in "@=<>!"))


def unpack_fields(name, bigendian, field_defs, data, pos):

    def get_cumulative_format(index, formats):
        format = "".join(formats[:index])
        if formats[index]:
            alignment_format = "0" + formats[index][-1]
            format += alignment_format
        return format

    formats = [(field.format if field.format else "") for field in field_defs]
    format = "".join(formats)
    sizes = [struct.calcsize(remove_endianness(x)) for x in formats]
    cumulative_formats = [
        get_cumulative_format(x, formats) for x in xrange(len(formats))
    ]
    offsets = [struct.calcsize(remove_endianness(f)) for f in cumulative_formats]
    endianness = ["<", ">"][bigendian]
    values = []
    for offset, size, f in zip(offsets, sizes, formats):
        len_clean = len(remove_endianness(f))
        if len_clean <= 0:
            values.append(("",))
        else:
            if len(f) == len_clean:
                f = endianness + f
            value = struct.unpack(f, data[offset : offset + size])
            if len(value) == 1:
                value, = value
            values.append(value)

    attrs = zip(field_defs, values, offsets)
    fields = [Field(n, value, pos + p) for n, value, p in attrs]
    return DataObject(pos, name, fields)


def read_fields(name, bigendian, field_defs, reader):
    formats = [(field.format if field.format else "") for field in field_defs]
    format = "".join(formats)
    pos = reader.position
    sz = struct.calcsize(remove_endianness(format))
    data = reader.read(sz)
    return unpack_fields(name, bigendian, field_defs, data, pos)


def get_fields_size(field_defs):
    formats = [(field.format if field.format else "") for field in field_defs]
    format = "".join(formats)
    format += "0i"
    return struct.calcsize(remove_endianness(format))


def halffloat_to_intfloat(halffloat):
    s = int(halffloat >> 15 & 1)
    e = int(halffloat >> 10 & 31)
    f = int(halffloat & 1023)
    if e == 0:
        if f == 0:
            return int(s << 31)
        while not f & 1024:
            f = f << 1
            e -= 1

        e += 1
        f &= -1025
    elif e == 31:
        if f == 0:
            return int(s << 31 | 2139095040)
        else:
            return int(s << 31 | 2139095040 | f << 13)
    e = e + 112
    f = f << 13
    return int(s << 31 | e << 23 | f)


def intfloat_to_float(intfloat):
    temp = struct.pack("I", intfloat)
    return struct.unpack("f", temp)[0]


def halffloat_to_str(a):
    if not isinstance(a, collections.Iterable):
        return str(intfloat_to_float(halffloat_to_intfloat(a)))
    s = ""
    for h in a:
        if s:
            s += ", "
        s += str(intfloat_to_float(halffloat_to_intfloat(h)))

    return "(" + s + ")"


def normalizeduint8_to_str(a):
    if not isinstance(a, collections.Iterable):
        return str(a / 255.0)
    s = ""
    for h in a:
        if s:
            s += ", "
        s += str(h / 255.0)

    return "(" + s + ")"


def normalizedint16_to_str(a):
    if not isinstance(a, collections.Iterable):
        return str(a / 32767.0)
    s = ""
    for h in a:
        if s:
            s += ", "
        s += str(h / 32767.0)

    return "(" + s + ")"
