def any_to_dec(string_number, radix):
    # the above function takes in a string as input along with a radix of the given number
    string_number = list(string_number)
    if "." not in string_number:
        string_number = string_number + ["."] + ["0"]
    if radix == 16:
        for i in range(len(string_number)):
            if string_number[i] in ["A", "B", "C", "D", "E", "F"]:
                m = str(int(string_number[i], 16))
                string_number[i] = m

    dec_num = 0
    dot_pos = string_number.index(".")
    digits = [0] * len(string_number)
    digits[dot_pos] = -1000
    i = dot_pos-1
    k = 0
    while i >= 0:
        digits[i] = k
        k += 1
        i -= 1
    i = dot_pos+1
    k = -1
    while i < len(string_number):
        digits[i] = k
        k -= 1
        i += 1
    for _ in range(len(string_number)):
        if digits[_] == -1000:
            continue
        else:
            dec_num += (radix ** digits[_]) * int(string_number[_])
    return dec_num


def dec_to_any(string_number, radix):
    if "." not in string_number:
        string_number = string_number + ".0"
    int_part = string_number.split(".")[0]
    fractional_part = "0." + string_number.split(".")[-1]
    conv_int = []
    conv_fractional = []
    int_ = int(int_part)
    fractional_ = float(fractional_part)
    while int_ > 0:
        conv_int.append(str(int_ % radix))
        int_ = int_ // radix
    for i in range(20):
        _ = fractional_ * radix
        lef_ = str(_).split(".")[0]
        rig_ = str(_).split(".")[-1]
        if radix == 16:
            lef_ = hex(int(lef_)).replace("0x", "")
        conv_fractional.append(lef_)
        fractional_ = int(rig_) * (10**-len(rig_))
    final_int = ""
    final_fractional = ""
    for i in conv_int[::-1]:
        final_int = final_int + i
    for i in conv_fractional:
        final_fractional = final_fractional + i
    final_num = final_int + "." + final_fractional
    return final_num


def any_to_any(string_number, given_radix, required_radix):
    dec_of_any = any_to_dec(string_number, given_radix)
    the_any = dec_to_any(str(dec_of_any), required_radix)
    return the_any


