import tkinter
import math

button_values = [
    ['HEX','DEC','BIN','OCT'],
    ['AC','+/','%','÷'],
    ['7','8','9','×'],
    ['4','5','6','-'],
    ['1','2','3','+'],
    ['0','.','√','=']
]

topsymbols = ['HEX','DEC','BIN','OCT']
rightsymbols = ['÷','×','-','+','=']

greyy = "#999E97"
darkgrey = "#545454"
orange = "#e55c26"
wwhite = "#ffffff"

window = tkinter.Tk()
window.title('pyproject')
window.resizable(False, False)

frame = tkinter.Frame(window)
frame.pack()

label = tkinter.Label(
    frame, text="0", font=("Arial",45),
    background=greyy, foreground=wwhite,
    anchor='e', width=4
)
label.grid(row=0, column=0, columnspan=4, sticky='we')

first_number = None
operator = None
base = 'DEC'

def reset():
    global first_number, operator, base
    first_number = None
    operator = None
    base = 'DEC'
    label['text'] = '0'
    update_buttons()

def format_number(n):
    if n % 1 == 0:
        return str(int(n))
    return str(n)

def valid_dec(text):
    if text == '' or text == '-' or text == '.':
        return False
    if text.count('.') > 1:
        return False
    if text.startswith('-'):
        text = text[1:]
    return text.replace('.', '', 1).isdigit()

def valbin(text):
    if text == '':
        return False
    for c in text:
        if c not in '01':
            return False
    return True

def valoct(text):
    if text == '':
        return False
    for c in text:
        if c not in '01234567':
            return False
    return True

def valhex(text):
    if text == '':
        return False
    for c in text:
        if c not in '0123456789ABCDEFabcdef':
            return False
    return True

def button_clicked(value):
    global first_number, operator, base

    if value in '0123456789':
        if label['text'] == '0':
            label['text'] = value
        else:
            label['text'] += value

    elif value == '.':
        if '.' not in label['text']:
            label['text'] += '.'

    elif value == 'AC':
        reset()

    elif value == '+/':
        if base == 'DEC' and valid_dec(label['text']):
            label['text'] = format_number(float(label['text']) * -1)

    elif value == '%':
        if base == 'DEC' and valid_dec(label['text']):
            label['text'] = format_number(float(label['text']) / 100)

    elif value == '√':
        if base != 'DEC' or not valid_dec(label['text']):
            label['text'] = 'Error'
            return
        num = float(label['text'])
        if num < 0:
            label['text'] = 'Error'
            return
        label['text'] = format_number(math.sqrt(num))

    elif value in '+-×÷':
        if base != 'DEC' or not valid_dec(label['text']):
            label['text'] = 'Error'
            return

        current = float(label['text'])

        if first_number is None:
            first_number = current
        else:
            if operator == '+':
                first_number += current
            elif operator == '-':
                first_number -= current
            elif operator == '×':
                first_number *= current
            elif operator == '÷':
                first_number /= current

        operator = value
        label['text'] = '0'

    elif value == '=':
        if base != 'DEC' or first_number is None or operator is None:
            return
        if not valid_dec(label['text']):
            label['text'] = 'Error'
            return

        second = float(label['text'])

        if operator == '+':
            result = first_number + second
        elif operator == '-':
            result = first_number - second
        elif operator == '×':
            result = first_number * second
        elif operator == '÷':
            result = first_number / second

        label['text'] = format_number(result)
        first_number = None
        operator = None

    elif value in topsymbols:
        text = label['text']

        if base == 'DEC' and valid_dec(text):
            num = int(float(text))
        elif base == 'BIN' and valbin(text):
            num = int(text, 2)
        elif base == 'OCT' and valoct(text):
            num = int(text, 8)
        elif base == 'HEX' and valhex(text):
            num = int(text, 16)
        else:
            label['text'] = 'Error'
            return

        if value == 'BIN':
            label['text'] = bin(num)[2:]
            base = 'BIN'
        elif value == 'HEX':
            label['text'] = hex(num)[2:]
            base = 'HEX'
        elif value == 'OCT':
            label['text'] = oct(num)[2:]
            base = 'OCT'
        elif value == 'DEC':
            label['text'] = str(num)
            base = 'DEC'

        update_buttons()

buttons = {}

def update_buttons():
    for v in ['+','-','×','÷','√','%','+/','.','=']:
        if base == 'DEC':
            buttons[v]['state'] = 'normal' 
        else:
            buttons[v]['state']='disabled'

for r in range(len(button_values)):
    for c in range(4):
        v = button_values[r][c]
        b = tkinter.Button(
            frame, text=v, font=("Arial",30),
            width=3, height=1,
            command=lambda x=v: button_clicked(x)
        )
        b.grid(row=r+1, column=c)
        buttons[v] = b

        if v in topsymbols:
            b.config(background=greyy, foreground=wwhite)
        elif v in rightsymbols:
            b.config(background=orange, foreground=wwhite)
        else:
            b.config(background=darkgrey, foreground=wwhite)

update_buttons()
window.mainloop()
