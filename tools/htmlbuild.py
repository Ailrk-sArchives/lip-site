
import sys
import os
import re

def clear_output(output):
    with open(output, 'w+') as output_file:
        output_file.write('')

def apped_block(txt, output):
    with open(output, 'a') as output_file:
        output_file.write(txt)

def main(argv):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    os.chdir('../')
    dir_path = os.getcwd()

    html = []
    css = ''

    with open(dir_path + argv[0]) as html_file:
        html = re.compile(r'\/\*.?css.*?\*\/').split(html_file.read())

    with open(dir_path + argv[1]) as css_file:
        css = css_file.read()

    output = dir_path + argv[2]
    print('\n=> writing: ({} html | {} css) to {}\n'.format(len(html[0] + html[1]), len(css), output))

    clear_output(output)
    apped_block(html[0], output)
    apped_block(css, output)
    apped_block(html[1], output)

if __name__ == '__main__':
    main(sys.argv[1:])
