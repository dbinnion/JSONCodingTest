"""Using any technology of your choice, convert the following string:

(id, name, email, type(id, name, customFields(c1, c2, c3)), externalId)

To this output:

- id
- name
- email
- type
    - id
    - name
    - customFields
        - c1
        - c2
        - c3
- externalId



And also to this output:

- email
- externalId
- id
- name
- type
    - customFields
        - c1
        - c2
        - c3
    - id
    - name


--"""
import json
import sys


def print_text(text_input, nesting_level, print_by_alpha):
    if print_by_alpha:
        printable_input = [[j for j in i.keys()][0] if isinstance(i, dict) else i for i in text_input]
        original_indexing = {
                [j for j in text_input[index].keys()][0]
                if isinstance(text_input[index], dict) else text_input[index]: index
                for index in range(len(text_input))
            }
        printable_input = sorted(printable_input)
        for item in printable_input:
            original_index = original_indexing[item]
            if isinstance(text_input[original_index], dict):
                print(('\t' * nesting_level) + '-', item)
                print_text(text_input[original_index][item], nesting_level + 1, print_by_alpha)
            else:
                print(('\t' * nesting_level) + '-', item)
    else:
        for item in text_input:
            if isinstance(item, dict):
                for key in item.keys():
                    print(('\t' * nesting_level) + '-', key)
                    print_text(item[key], nesting_level + 1, print_by_alpha)
            else:
                print(('\t' * nesting_level) + '-', item)


def convert_text(input_text, print_by_alpha):
    input_text = list(input_text)

    is_word = False
    nesting = []
    start_index_last_word = 0
    index = 0
    while index < input_text.__len__():
        if input_text[index] == '(':
            input_text[index] = '['
            if index > 0:
                input_text.insert(index, ":")
            if is_word:
                input_text.insert(index, "\"")
                input_text.insert(start_index_last_word, "{")
                is_word = False
                nesting.append('d')
                nesting.append('l')
            else:
                nesting.append('l')
            index += 1
        elif input_text[index] == ')':
            if is_word:
                input_text.insert(index, "\"")
                is_word = False
                index += 1
            nest_size = len(nesting)
            if nesting[nest_size - 1] == 'l' and nesting[nest_size - 2] == 'd':
                input_text[index] = ']'
                nesting.pop(-1)
                index += 1
                input_text.insert(index, "}")
                nesting.pop(-1)
            elif nesting[-1] == 'l':
                input_text[index] = ']'
                nesting.pop(-1)
        elif input_text[index].isalnum():
            if not is_word:
                input_text.insert(index, "\"")
                is_word = True
                start_index_last_word = index
                index += 1
            index += 1
        else:
            if is_word:
                input_text.insert(index, "\"")
                is_word = False
                index += 1
            index += 1

    json_text = ''.join(input_text)
    print(json_text)
    object_representation = json.loads(json_text)

    print_text(object_representation, 0, print_by_alpha)


# assumption is that as in the given string, nested lists are never given, only dictionary types
# to change to fit more json types, testing must be added to check for internal lists not in dictionaries
# to change to fit more json types, testing must be added to check the greater json object if of type dictionary
if int(sys.argv[2]) == 0:
    convert_text(sys.argv[1], False)
else:
    convert_text(sys.argv[1], True)
