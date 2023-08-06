import sys
import re


# replacement of builtins.print() function, compatible in python 2 and python 3.
def rprint(*args,  **kwargs):
    """
    replacement of builtins.print() function, compatible in python 2 and python 3.

    :Chinese: 打印（兼容Python2, Python3)

    :param args:  arguments to be printed

    :param kwargs:  Optional keyword arguments: <br>
        sep:   string inserted between values, default a space.<br>
        end:   string appended after the last value, default a newline.<br>
        flush: whether to forcibly flush the stream.<br><br>
    :return: None
    """
    sep = kwargs.pop('sep', ' ')
    for index, arg in enumerate(args):
        if index > 0:
            sys.stdout.write(sep)
        sys.stdout.write(str(arg))

    end = kwargs.pop('end', '\n')
    if end:
        sys.stdout.write(end)

    flush = kwargs.pop('flush', None)
    if flush:
        sys.stdout.flush()


class StrUtil:
    """
    Utilities for string process.

    :Chinese: 字符串处理类
    """

    @staticmethod
    def sys_encoding():
        """
        return system encoding.

        :Chinese: 取得系统编码

        :return: str
        """
        # noinspection PyBroadException
        try:
            import locale
            lo = locale.getdefaultlocale()
            if lo[1] == 'cp936':  # Simplified Chinese, 简体中文
                return 'gbk'
            elif lo[1] == 'cp950':  # Traditional Chinese, 繁体中文
                return 'cp950'
            elif lo[1] == 'cp936':
                return 'gbk'
        except Exception:
            return 'gbk'

    @staticmethod
    def trim_quote(s):
        """
        Trim quote marks at the beginning and ending of the string.

        :Chinese: 删除字符串两端的引号 (包括单引号、双引号)

        :param s: the string
        :return: str
        """
        if isinstance(s, str):
            if len(s) >= 2:
                if s.startswith('"') and s.endswith('"'):
                    return s[1:len(s)-1]

                if s.startswith("'") and s.endswith("'"):
                    return s[1:len(s)-1]
        return s

    @staticmethod
    def match_offset_length(text: str, findings: [str, list, tuple], start_offset=0):
        """
        Match the finding condition in the string, return matched offset, length.

        :Chinese: 查找字符串, 返回匹配的offset和长度length。

        :param text:     The string
        :param findings:  Find condition, could be a sub string, or a list of str for continuous finding,
                or a tuple of str for finding one of them.<br>
                :Chinese: 查找条件，可以是一个子字符串，或一个字符串list(表示连续查找、and关系),
                或一个字符串tuple(表示查找其中一个、or关系)
        :param start_offset:    (optional) the offset to start finding.<br>
                :Chinese: (可选)起始查找位置, 默认值为0.
        :return: return a tuple of (offset, length).  If not found, offset is -1.
                :Chinese: 返回一个tuple(offset, length)。如果找不到，tuple 中的 offset = -1
        """
        if findings is None:
            return start_offset, 0

        if text is None:
            return -1, 0

        if not isinstance(text, str):
            text = str(text)

        # convert findings to list
        if not isinstance(findings, list) and not isinstance(findings, tuple):
            findings = [str(findings)]

        is_or = True if isinstance(findings, tuple) else False
        offset_begin = -1
        offset_length = 0

        for item in findings:
            if item is None or item == '':
                continue

            if isinstance(item, list) and not isinstance(item, tuple):
                offset, length = StrUtil.match_offset_length(text, item, start_offset)
                offset_begin = offset if offset_begin < 0 <= offset else offset_begin

            elif isinstance(item, str):
                if item.startswith('<re>'):  # regular expression
                    pattern = item[4:]
                    m = re.search(pattern, text[start_offset:])
                    if m is None:
                        offset = -1
                        length = 0
                    else:
                        offset = start_offset + m.start()
                        length = m.end() - m.start()
                        offset_begin = offset if offset_begin < 0 <= offset else offset_begin
                else:
                    offset = text.find(item, start_offset)
                    length = len(item) if offset >= 0 else 0
                    offset_begin = offset if offset_begin < 0 <= offset else offset_begin
            else:
                raise TypeError('finding item type %s invalid' % type(item))

            if is_or:
                if offset >= 0:
                    # return offset, length
                    if offset < offset_begin:
                        offset_begin = offset
                        offset_length = length
            else:
                if offset < 0:
                    return -1, 0
                else:
                    start_offset = offset + length

        if is_or:
            return offset_begin, offset_length
        else:
            # return start, 0
            return offset_begin, start_offset - offset_begin

    @staticmethod
    def match(text, findings, start_offset=0):
        """
        Whether the string match the finding condition.

        :Chinese: 判断字符串是否符合条件, 返回True, False

        :param text:  the string
        :param findings: Find condition, could be a sub string, or a list of str for continuous finding,
                or a tuple of str for finding one of them.<br>
                :Chinese: 查找条件，可以是一个子字符串，或一个字符串list(表示连续查找、and关系),
                或一个字符串tuple(表示查找其中一个、or关系)
        :param start_offset:    (optional) the offset to start finding.<br>
                :Chinese: (可选)起始查找位置, 默认值为0.
        :return: return True if matched, else return False.
        """
        offset, length = StrUtil.match_offset_length(text, findings, start_offset)
        return offset >= 0

    @staticmethod
    def get_word(text, before, after, start_offset=0, return_offset=False):
        """
        Get a word from text, the word is between before condition, and after condition.

        :Chinese: 从文本中提取一个词，该词在查找条件before后, 查找条件after前

        :param text:    the string
        :param before:  the before condition, could be a sub string or a list of string.<br>
                :Chinese: 查找条件before
        :param after:   the end condition, could be a sub string or a list of string.<br>
                :Chinese: 查找条件end
        :param start_offset:    offset to start finding.
                :Chinese:（可选）开始查找的位置
        :param return_offset:  whether return offset, boolean.
                :Chinese:（可选）是否返回查找后的位置
        :return: return str if found, return None if not found.
                :Chinese: 返回一个词。 如果找不到，返回None
        """
        if start_offset is not None and not isinstance(start_offset, int):
            offset, length = StrUtil.match_offset_length(text, str(start_offset), 0)
            if offset < 0:
                return None
            else:
                start_offset = offset + length

        if start_offset < 0:
            if return_offset:
                return None, start_offset
            else:
                return None

        b, len1 = StrUtil.match_offset_length(text, before, start_offset)
        if b > 0:
            e, len2 = StrUtil.match_offset_length(text, after, b + len1)
            if e > b + len1:
                if return_offset:
                    return text[b + len1: e], e + len2
                else:
                    return text[b + len1: e]
        else:
            if return_offset:
                return None, start_offset
            else:
                return None

    @staticmethod
    def get_word_list(text, begin, betweens, start_offset=0, end=None):
        """
        get a list of keywords from the text.

        :Chinese: 从文本中, 查找出一串单词列表。

        :param text:   the text to process
        :param begin:  begin condition, could be a sub string or a list of string.<br>
        :param betweens:  words definition list
                each item is a keyword definition tuple, which contains a before and after condition.
                Example:
                <code>
                    [
                      (['<li', '<a', '>'], '</a'),
                      (['author', '>'], '</a')
                    ]
                </code>
                define two keywords.

                :Chinese: betweens 是一个单词定义列表。
                         每一个元素单词定义, 一个 2个元素tuple, 第0个元素是before条件，
                         第1个元素是after条件.

        :param start_offset: (optional) offset to start finding
        :param end:  (optional) end condition, could be a sub string or a list of string.<br>
        :return:  return a list of words
        """
        result = []
        if begin:
            offset, length = StrUtil.match_offset_length(text, begin, start_offset)
        else:
            offset = 0

        if end:
            end_offset, _ = StrUtil.match_offset_length(text, end, offset)
        else:
            end_offset = -1

        while offset >= 0:
            words = []
            # search words
            for item in betweens:
                before = item[0]
                after = item[1]
                word, offset = StrUtil.get_word(text, before, after, offset, return_offset=True)

                if offset > end_offset > 0:
                    word = None

                if word:
                    words.append(word)
                else:
                    offset = -1
                    break
            # add words to result
            if words and len(words) == len(betweens):
                result.append(words)

        if len(betweens) == 1:
            ret = []
            for item in result:
                if len(item) == 1:
                    ret.append(item[0])
            return ret
        else:
            return result

    @staticmethod
    def is_json_string(s):
        """
        Whether the string is a JSON string.

        :Chinese: 判断 字符串s 是否是一个json字符串

        :param s: the string
        :return: True or False
        """
        if isinstance(s, str):
            s = s.strip()
            if s.startswith('{') and s.endswith('}'):
                return True
        return False

    @staticmethod
    def is_xml_string(s):
        """
        Whether the string is a XML string.

        :Chinese: 判断 字符串s 是否是一个 xml 字符串

        :param s: the string
        :return: True or False
        """
        if isinstance(s, str):
            s = s.strip()
            if s.startswith('<') and s.endswith('>'):
                return True
        return False

    @staticmethod
    def find_word(text, finding, index=0, sep=None):
        """
        Find a word ing a line.

        :Chinese: 在一行文字中查找符合条件的词.

        :param text:   the string
        :param index:  the index of occurrence , the first is 0, second is 1 ...
                    :Chinese: 第几个. 0表示第一个， 1表示第二个
        :param finding: (optional) finding condition, could be a sub string or a list of string.<br>
                :Chinese:(可选)查找条件，可以是一个子字符串，或一个字符串列表
        :param sep:   separate char, default is blank char.<br>
                :Chinese:(可选)词分割符，默认为空格
        :return: return str if found, return None if not found.
                :Chinese: 如果找到，返回字符串。如果找不到，返回None
        """
        count = 0
        if isinstance(text, str):
            words = StrUtil.split(text, sep)
            for word in words:
                if StrUtil.match(word, finding):
                    if count == index:
                        return word
                    count += 1
        return None

    @staticmethod
    def find_sep(text, sep, start_offset=0):
        """
        find separator char

        :Chinese: 查找分割符

        :param text:  the string
        :param sep:   the separator char
        :param start_offset: 
        :return: return a tuple of (offset, length_of_sep)
        """
        if isinstance(sep, str):
            return text.find(sep, start_offset), len(sep)
        elif isinstance(sep, list) or isinstance(sep, tuple):
            for word in sep:
                ret = text.find(word, start_offset)
                if ret >= 0:
                    return ret, len(word)
        return -1, 0

    @staticmethod
    def is_blank_char(c):
        """ Whether the c is blank char """
        return c == ' ' or c == '\t' or c == '\r'

    @staticmethod
    def split(text, sep=None):
        """
        split the text into word list by specified separator

        :param text:  the text
        :param sep:  separator string
        :return: return a list of str
        """
        if sep is None:
            sep = [' ', '\t']

        if text is None:
            text = ''
        if not isinstance(text, str):
            text = str(text)

        words = []
        length = len(text)
        offset = 0
        word = ''
        while offset < length:
            c = text[offset:offset+1]
            offset += 1
            if c in sep:
                if word == '' and StrUtil.is_blank_char(c):
                    pass
                else:
                    words.append(word)
                    word = ''
            else:
                word += c
        if word:
            words.append(word)
        return words

    @staticmethod
    def split2(text, sep, first=True):
        """
        Split the text into two-word list.

        :Chinese: 将一个字符串切分为两个词

        :param text:  the text
        :param sep:   separator string
        :param first: (optional) If True, when separator is missing, set the first word with text and
                leave the second word empty. If False, vise versa.
        :return: return a 2-word list
        """
        if text is None:
            text = ''

        pos, length = StrUtil.find_sep(text, sep)

        if pos >= 0:
            s1 = text[:pos]
            s2 = text[pos + length:]
            return s1.strip(), s2.strip()
        else:
            if first:
                return text.strip(), ''
            else:
                return '', text.strip()

    @staticmethod
    def split_number_unit(s):
        """
        Split the string, such as '2ms', into number and unit.

        :Chinese: 将一个形如: 2ms 的字符串切分为 数字,单位

        :param s: the string
        :return: return a tuple of (number, unit)
        """
        if s is None:
            s = ''
        if not isinstance(s, str):
            s = str(s)

        number = ''
        unit = ''
        for c in s:
            if unit == '':
                if ('0' <= c <= '9') or c == '.':
                    number += c
                elif len(number) == 0 and c == '-':
                    number = c
                else:
                    unit += c
            else:
                unit += c
        if len(number) > 0:
            number = float(number) if '.' in number else int(number)
        return number, unit.strip()

    @staticmethod
    def grep(text, finding):
        """
        Split the text into lines, return the lines matched the finding condition.

        :Chinese: 将文本切分为多行, 返回符合查找条件的行

        :param text:  the string
        :param finding: the finding condition, could be a sub string, or a list of string.
                :Chinese: 查找条件，可以是一个子字符串，或一个字符串列表
        :return: return a list of str， each element is a line matched the finding condition.
                :Chinese: 返回一个字符串列表， 每个元素是一个符合查找条件的行
        """
        result = []

        # check each line in the text
        if text is None:
            return result

        if isinstance(text, list) or isinstance(text, tuple):
            lines = text
        else:
            text = str(text) if not isinstance(text, str) else text
            lines = text.split('\n')

        if isinstance(lines, list) or isinstance(lines, tuple):
            for line in lines:
                if StrUtil.match(line, finding):
                    result.append(line)

        return result

    @staticmethod
    def is_ip_number(text):
        """
        Whethe the string is a valid IP number, which range is [0-255]

        :Chinese: 判断文字是否是有效的IP数字范围 [0-255]

        :param text: the string
        :return:  True of False
        """
        # noinspection PyBroadException
        try:
            n = int(text)
            if isinstance(text, float):
                return False
            return 0 <= n <= 255
        except Exception:
            return False

    @staticmethod
    def get_words(text, line_findings, word_findings, index=0, multiple=False, number_unit=False):
        lines = StrUtil.match(text, line_findings)
        ret = []
        for line in lines:
            word = StrUtil.find_word(line, word_findings, index)
            if word:
                if number_unit:
                    word, unit = StrUtil.split_number_unit(word)
                if not multiple:
                    return word
                else:
                    ret.append(word)
        return ret

