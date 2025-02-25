import csv
import os
import re
import shutil


def multi_replace(string, mapping):
    """
    Simultaneously replaces multiple strings or patterns within a string.
    Unlike chaining .replace, the result of one replacement will not be subject to another replacement.
    Therefore, it is possible to swap two words with each other.

    mapping: A dictionary where the search target is the key and the replacement string is the value.
        The key can be specified as a str or re pattern object.
        If the key is an re pattern object, group references '\\1', '\\2',... are valid in the replacement string.
    """
    catch_all_pattern = "|".join(map(to_pattern, mapping))
    replacer = make_replacer(mapping)

    return re.subn(catch_all_pattern, replacer, string)[0]


_PatternType = type(
    re.compile("")
)  # workaround for Python which does't have typing module


def to_pattern(key):
    if isinstance(key, str):
        return "(" + re.escape(key) + ")"
    elif isinstance(key, _PatternType):
        return "(" + key.pattern + ")"
    else:
        raise ValueError(f"{key} is not a str, neither re.compile.")


def make_replacer(mapping):

    def _replacer(match):
        src = match.group(0)
        for key, val in mapping.items():
            if src == key:
                return val
            elif isinstance(key, _PatternType) and re.match(
                "(?:" + key.pattern + r")\Z", src
            ):  # workaround for Python which doesn't have re.fullmatch
                return key.sub(val, src)

    return _replacer


os.chdir(os.path.dirname(os.path.abspath(__file__)))

filename_keymap = "./config/roBa.keymap"
fileneme_lastmode = "./last_convert_mode.txt"

# select mode
mode_select = input("Select mode 1(us->jis) or 2(jis->us): ")
if mode_select == "1":
    mode_convert = "us2jis"
elif mode_select == "2":
    mode_convert = "jis2us"
else:
    print("Invalid mode.")
    exit()

csv_table = f"table_{mode_convert}.csv"

# check if conversion has already been done
match_layout = re.match(r"(us|jis)2(us|jis)", mode_convert)
layout_before = match_layout.group(1)
layout_after = match_layout.group(2)

if os.path.exists(fileneme_lastmode):
    with open(fileneme_lastmode, "r", encoding="utf-8") as f:
        last_mode = f.read().strip()
    if last_mode == mode_convert:
        print(f"{layout_before}->{layout_after} conversion has already been done.")
        exit()

with open(fileneme_lastmode, "w", encoding="utf-8") as f:
    f.write(mode_convert)

# make keymap backup
shutil.copyfile(filename_keymap, filename_keymap + ".bak")

# read keymap as dictionary
with open(csv_table, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    l = [row for row in reader]

# convert keymap
l_jis = [d.get("jis_zmk") for d in l]
l_us = [d.get("us_zmk") for d in l]

if mode_convert == "us2jis":
    l_from = l_us
    l_to = l_jis
elif mode_convert == "jis2us":
    l_from = l_jis
    l_to = l_us
l_from = [re.sub(r"(\(|\))", r"\\\1", r) for r in l_from]

re_from = [re.compile(f"(^|\\s+){r}($|\\s+|>)") for r in l_from]
re_to = [f"\\1{r}\\2" for r in l_to]
mapping = dict(zip(re_from, re_to))

with open(filename_keymap, "r", encoding="utf-8") as f:
    keymap = f.read()
    keymap_converted = multi_replace(keymap, mapping)

with open(filename_keymap, "w", encoding="utf-8") as f:
    f.write(keymap_converted)
