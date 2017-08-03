# -*- coding: utf-8 -*-
"""
@author: xihao liang
"""

import re

class PortNameGenerator:
    def __init__(self, prefix='p'):
        self.count = -1
        self.prefix = prefix

    def generate(self):
        self.count += 1
        return '%s%d' % (self.prefix, self.count)

class HDLGenerator:
    src_code_format = 'CHIP %s {\n\tIN %s;\n\tOUT %s;\n\tPARTS:\n\t\t%s\n}'

    def __init__(self):
        pass

    def add_statement_and(self, a, b, out=None):
        if out is None:
            out = self.port_name_generator.generate()        

        s = 'And(a=%s, b=%s, out=%s)' % (a, b, out)
        self.parts_statements.append(s)
        return out        

    def add_statement_or(self, a, b, out=None):
        if out is None:
            out = self.port_name_generator.generate()        

        s = 'Or(a=%s, b=%s, out=%s)' % (a, b, out)
        self.parts_statements.append(s)
        return out

    def add_statement_not(self, a, out=None):
        if out is None:
            out = self.port_name_generator.generate()        

        s = 'Not(in=%s, out=%s)' % (a, out)
        self.parts_statements.append(s)
        return out

    def generate_from_file(self, filename):
        lines = open(filename, 'r').readlines()
        chip_name = lines[0].strip()
        input_part = re.sub('\s+', ', ', lines[1].strip())
        output_part = re.sub('\s+', ', ', lines[2].strip())

        def name_to_names(name):
            m = re.match('(.*)\[(\d+)\]', name)
            if m is None:
                return [name, ]
            else:
                return ['%s[%d]' % (m.group(1), i) for i in range(int(m.group(2)))]

        def part_to_names(part):
            names = []
            for name in part.split(', '):
                names.extend(name_to_names(name))
            return names

        input_names = part_to_names(input_part)
        output_names = part_to_names(output_part)
        print input_names
        print output_names

        #exprs = lines[3:3 + len(output_names)]
        #exprs = [expr.strip() for expr in exprs]
        line_expr = ''.join(lines[3:]).replace('\\\n', '').replace('{', '').replace('}', '')
        exprs = line_expr.split(', ')
        exprs = map(lambda expr: expr.strip(), exprs)

        parts_statement = self.generate(exprs, input_names, output_names)

        return self.src_code_format % (chip_name, input_part, output_part, parts_statement)


    def generate(self, exprs, input_names, output_names):
        self.port_name_generator = PortNameGenerator()
        self.parts_statements = []

        def part_to_input_name(in_ID_str):
            return input_names[int(in_ID_str) - 1]

        for expr, output_name in zip(exprs, output_names):
            if expr[-1] == '&':
                expr = expr[:-1]
            expr = expr.replace('#', '').replace(' ', '')

            conj_parts = expr.split('||')

            if len(conj_parts) > 1:
                conj_outs = []
                for i, conj_part in enumerate(conj_parts):
                    if not conj_part.startswith('('):
                        if conj_part.startswith('!'):
                            out_name = self.add_statement_not(part_to_input_name(conj_part[1:]))
                        else:
                            out_name = part_to_input_name(conj_part)
                    else:
                        conj_part = conj_part[1:-1]
                        disj_parts = conj_part.split('&&')
                        and_parts = []
                        for part in disj_parts:
                            if part.startswith('!'):
                                out_name = self.add_statement_not(part_to_input_name(part[1:]))
                            else:
                                out_name = part_to_input_name(part)
                            and_parts.append(out_name)
                        
                        tmp_port = and_parts[0]
                        for part in and_parts[1:]:
                            tmp_port = self.add_statement_and(tmp_port, part)
                        out_name = tmp_port
                    conj_outs.append(out_name)
                
                tmp_port = conj_outs[0]
                for part in conj_outs[1:-1]:
                    tmp_port = self.add_statement_or(tmp_port, part)
                self.add_statement_or(tmp_port, conj_outs[-1], output_name)
            else:
                part = conj_parts[0]
                disj_parts = part.split('&&')
                
                if len(disj_parts) == 1:
                    part = disj_parts[0]
                    if part.startswith('!'):
                        self.add_statement_not(part_to_input_name(part[1:]), output_name)
                    else:
                        raise Warning
                else:
                    and_parts = []
                    for part in disj_parts:
                        if part.startswith('!'):
                            out_name = self.add_statement_not(part_to_input_name(part[1:]))
                        else:
                            out_name = part_to_input_name(part)
                        and_parts.append(out_name)
                    
                    tmp_port = and_parts[0]
                    for part in and_parts[1:-1]:
                        tmp_port = self.add_statement_and(tmp_port, part)
                    self.add_statement_and(tmp_port, and_parts[-1], output_name)
                
        parts_statement = ';\n\t\t'.join(self.parts_statements) + ';'
        return parts_statement

def max_num(nums):
    m = nums[0]
    for n in nums:
        if n > m:
            m = n
    return m

def main():
    import sys    

    chip_name = sys.argv[1]
    filename = 'project1/%s_expr.txt' % chip_name
    output_filename = 'project1/%s.hdl' % chip_name
    
    hdlgenerator = HDLGenerator()
    src_code = hdlgenerator.generate_from_file(filename)
    open(output_filename, 'w').write(src_code)

if __name__ == '__main__':
    main()
