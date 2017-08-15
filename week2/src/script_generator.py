# -*- coding: utf-8 -*-
"""
@author: Xihao Liang
@created: 2017.07.29
"""

import re
import xlwt
import copy


def np_sum(nums): # instead of importing numpy
    s = 0
    for n in nums: s+= n
    return s


def name_to_bits_len(name):
    """
    e.g.
        a     -> 1
        a[16] -> 16
    """

    m = re.match('(.*)\[(\d+)\]', name)
    if m is None:
        return 1
    else:
        return int(m.group(2))


def bits_to_str(bs):
    """
    e.g. [True, True, False] -> '110'
    """

    if isinstance(bs, list):
        s = ''
        revbs = copy.deepcopy(bs)
        revbs.reverse()
        for b in revbs:
            s += '1' if b is True else '0'
        return s 
    else:
        return '1' if b is True else '0'


def boolean_enumerate(n):
    """
    e.g. for n = 2, yield
    [True, True]
    [True, False]
    [False, True]
    [False, False]
    """
    for i in xrange(1 << n):
        flag = 1
        bits = []
        for j in xrange(n):
            bits.append(i & flag == 0)
            flag <<= 1
        bits.reverse()
        yield bits


def generate_first_cmp_line(col_names, col_lens):
    """
    generate the first line for .cmp file
    """
    for name, l in zip(col_names, col_lens):
        if len(name) > l:
            raise Warning('Column length is too short')

    line = '|'
    for i in range(len(col_names)):
        col_len = col_lens[i] - len(col_names[i])
        l_span = col_len / 2
        r_span = col_len - l_span
        line += ' ' * l_span + col_names[i] + ' ' * r_span + '|' 

    return line


def generate_first_tst_line(chip_name, col_names, bits_lens, spans):
    """
    generate the first line for .tst file
    """
    output_format = ''
    cols = []
    n_col = len(col_names)
    for i in range(n_col):
        cols.append('%s%%B%d.%d.%d' % (col_names[i], spans[i], bits_lens[i], spans[i]))

    return 'load %s.hdl,\noutput-file %s.out,\ncompare-to %s.cmp,\noutput-list %s;' % (
                chip_name, chip_name, chip_name, ' '.join(cols))


def generate_expr_header(chip_name, input_names, output_names):
    """
    generate the first part for CHIP_NAME_expr.txt
    """
    return '%s\n%s\n%s' % (chip_name, ' '.join(input_names), ' '.join(output_names))


def generate_cmp_truthtable_line(spans, bits_lens, all_bits):
    """
    generate one line of the truth table for the .cmp file
    """
    line = '|'
    bias = 0

    for span, bits_len in zip(spans, bits_lens):
        line += ' ' * span + bits_to_str(all_bits[bias:bias + bits_len]) + ' ' * span + '|'
        bias += bits_len
    return line


def generate_tst_eval_line(bits, n_input, col_names, bits_lens):
    """
    generate one line of the evaluation part for the .tst file
    """
    line = ''
    bias = 0
    for i in range(n_input):
        partial_bits = bits[bias: (bias + bits_lens[i])]

        line += 'set %s %s%s, ' % (
            col_names[i],
            '' if bits_lens[i] == 1 else '%B',
            bits_to_str(partial_bits))
        bias += bits_lens[i]
    line += 'eval, output;'

    return line


def generate_truthtable_line(all_bits):
    return ' '.join(map(lambda b: '1' if b is True else '0', all_bits))


def generate_xor_output(bits):
    a = bits[0]
    b = bits[1]
    return not (a == b)


def generate_or2_output(bits):
    a = bits[:2]
    b = bits[2:]
    out = [ai or bi for ai, bi in zip(a, b)]
    return out


def generate_or8_output(bits):
    a = bits[:8]
    b = bits[8:]
    out = [ai or bi for ai, bi in zip(a, b)]
    return out


def generate_mux_output(bits):
    a = bits[0]
    b = bits[1]
    sel = bits[2]
    return a if sel is False else b


def generate_dmux_output(bits):
    in_ = bits[0]
    sel = bits[1]
    if sel is True:
        return [0, in_]
    else:
        return [in_, 0]

def generate_full_adder_output(bits):
    a = 1 if bits[0] else 0
    b = 1 if bits[1] else 0
    c = 1 if bits[2] else 0
    d = a + b + c

    sum_ = d & 1
    carry = (d & 2) > 1 
    return [sum_, carry]


def generate_half_adder_output(bits):    
    a = 1 if bits[0] else 0
    b = 1 if bits[1] else 0
    c = a + b

    return {
        0: [0, 0],
        1: [1, 0],
        2: [0, 1]
    }[c]


def generate_not4_output(bits):
    return [not b for b in bits]


def generate_add2_output(bits):
    a = eval('0B0' + bits_to_str(bits[:2]))
    b = eval('0B0' + bits_to_str(bits[2:]))

    c = a + b
    out = []
    for i in range(2):
        out.append((c & 1) is 1)
        c >>= 1
    out.reverse()
    return out


def generate_add4_output(bits):
    a = eval('0B0' + bits_to_str(bits[:4]))
    b = eval('0B0' + bits_to_str(bits[4:]))

    c = a + b
    out = []
    for i in range(4):
        out.append((c & 1) is 1)
        c >>= 1
    out.reverse()
    return out


def calculate_span(name_len, bit_len):
    if bit_len >= name_len:
        return 1
    else:
        return (name_len - bit_len + 1) / 2 + 1


def remove_array(name):
    return re.sub('\[(\d+)\]', '', name)


def generate_scripts(chip_name, input_names, output_names, generate_output, out_dir='out/'):
    """
    4 files are generated after this function is successfully called
    * CHIP_NAME.cmp is a Nand2Tetris-defined file containing the expected truth table
    * CHIP_NAME.tst is a Nand2Tetris-defined automatic examination script, which test whether the .hdl fulfils the truth table in the .cmp file
    * CHIP_NAME_exp.txt, whose format is defined by me, is a template ready for be appended by the boolean expressions generated by Mathematica
    * CHIP_NAME.xls, whose format is defined by me, contains the expected truth table and some configuration, which is supposed to be the input for table2expr.nb 
    """
    cmp_lines = []
    tst_lines = []
    expr_lines = []

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet1')

    input_names = input_names.split(' ')
    output_names = output_names.split(' ')
    expr_lines.append(generate_expr_header(chip_name, input_names, output_names))

    n_input = len(input_names)

    col_names = []
    col_names.extend(input_names)
    col_names.extend(output_names)

    bits_lens = map(name_to_bits_len, col_names)

    n_bit_input = np_sum(bits_lens[:n_input])
    n_bit_output = np_sum(bits_lens[n_input:])

    sheet.write(0, 0, n_bit_input); sheet.write(0, 1, n_bit_output)

    col_names = map(remove_array, col_names)
    names_lens = map(lambda name:len(name), col_names)
    spans = [calculate_span(nl, bl) for nl, bl in zip(names_lens, bits_lens)]
    
    col_lens = [span * 2 + l  for span, l in zip(spans, bits_lens)]    
    cmp_lines.append(generate_first_cmp_line(col_names, col_lens))

    tst_lines.append(generate_first_tst_line(chip_name, col_names, bits_lens, spans))

    i = 1
    for bits in boolean_enumerate(np_sum(bits_lens[:len(input_names)])):
        out = generate_output(bits)
        all_bits = []
        all_bits.extend(bits)
        if isinstance(out, bool):
            all_bits.append(out)
        else:
            all_bits.extend(out)

        cmp_line = generate_cmp_truthtable_line(spans, bits_lens, all_bits)
        cmp_lines.append(cmp_line)

        tst_line = generate_tst_eval_line(bits, n_input, col_names, bits_lens)
        tst_lines.append(tst_line)

        #truthtable_line = generate_truthtable_line(all_bits)
        #truthtable_lines.append(truthtable_line)

        for j, b in enumerate(all_bits):
            sheet.write(i, j, 1 if b is True else 0)

        i += 1

    open('%s%s.cmp' % (out_dir, chip_name), 'w').write('\n'.join(cmp_lines) + '\n\n')
    open('%s%s.tst' % (out_dir, chip_name), 'w').write('\n'.join(tst_lines) + '\n\n')
    open('%s%s_expr.txt' % (out_dir, chip_name), 'w').write('\n'.join(expr_lines) + '\n\n')
    wbk.save('%s%s.xls' % (out_dir, chip_name))


def main():
    generate_scripts('Xor', 'a b', 'out', generate_xor_output)
    generate_scripts('Mux', 'a b sel', 'out', generate_mux_output)
    generate_scripts('DMux', 'in sel', 'a b', generate_dmux_output)
    generate_scripts('Or2', 'a[2] b[2]', 'out[2]', generate_or2_output)
    generate_scripts('FullAdder', 'a b c', 'sum carry', generate_full_adder_output)
    generate_scripts('HalfAdder', 'a b', 'sum carry', generate_half_adder_output)
    generate_scripts('Add2', 'a[2] b[2]', 'out[2]', generate_add2_output)
    generate_scripts('Add4', 'a[4] b[4]', 'out[4]', generate_add4_output)
    generate_scripts('Not4', 'in[4]', 'out[4]', generate_not4_output)


if __name__ == '__main__':
    main()

