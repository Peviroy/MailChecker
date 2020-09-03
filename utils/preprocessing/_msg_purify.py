"""
@Author: peviroy
@Date: 2020-09-02
@Last Modified by: peviroy
@Last Modified time: 2020-09-03 10:02
"""

import re


class TextPurifier:
    '''
    [Text Purifier]文字净化器
        Replace words which matchs specific "regular expression" rules.
        By default, we have prepared 6 rules.
    '''
    # Tested

    def __init__(self, texts=None, regex_rules=None):
        '''
        Key Arguments:
            texts       {list of str} -- Text to be purified
            regex_rules {dict} -- In the form of "<name> : <rule>"  -index matters
                               -- if name start with '_', then text will be replaced by <name>
                               -- if name start with '__',text will be replaced by <' '>
                               -- if name start with '___', text will be replaced by <''>
        '''
        self.regex_rules = {
            '_mailaddress': r'(?:[0-9a-zA-Z_])+\S@[^.]+\.[a-z]{2,}',
            '_webaddress': r'(http[s]?\://)?[a-zA-Z0-9\-\.]+\.(com|edu|gov|mil|net|org|biz|info|name|museum|us|ca|uk)(/\S*)*',
            '_phonenumber': r'\(?[\d]{4}\)?[\s-]?[\d]{3}[\s-]?[\d]{4,}',
            '_number': r'\b\d+(\.\d+)?\b',
            '__punctuation': r'[^\w\d\s]|_',
            '__two_many_spaces': r'\s{2,}'
        }
        self.texts = texts

        self.update_regex(regex_rules)

    # Tested
    def __str__(self):
        '''
        Note:
            output self.regex_rules in the format: {Name:<>,Rules:<>}
        '''
        ret_str = ''
        delete_underline = re.compile(r'^_*')
        for rule_name, rule in self.regex_rules.items():
            string = f'Name:{delete_underline.sub("", rule_name):10s}, \tRule:<{rule}>'
            ret_str += string + '\n'
        return ret_str

    # Tested
    def update_regex(self, regex_rules: dict):
        '''
        [Setter]
        Arguments:
            regex_rules {dict} -- In the form of "<name> : <rule>"
                               -- if name start with '_', then text will be replaced by <name>
                               -- if name start with '__',text will be replaced by <' '>
                               -- if name start with '___', text will be replaced by <''>
        '''
        if regex_rules is None:
            return
        for key, value in regex_rules.items():
            self.regex_rules[key] = value

    # Tested
    def set_texts(self, texts):
        '''
        [Setter]
        '''
        self.texts = texts

    # Tested
    def show_iter(self, nums=10):
        '''
        Get matched texts which would be purified
        '''
        for rule_name, rule in self.regex_rules.items():
            matched = []
            pattern = re.compile(rule)
            for index, text in enumerate(self.texts):
                searched = pattern.search(text)
                if searched is not None:
                    matched.append(searched.group())
            yield (rule_name, matched[:10])

    # Tested
    def purify(self):
        '''
        Return:
            purified texts according to regular rules
        '''
        for rule_name, rule in self.regex_rules.items():
            pattern = re.compile(rule)  # for re.sub
            repl = None  # as replacement
            if rule_name.startswith('___'):
                repl = ''
            elif rule_name.startswith('__'):
                repl = ' '
            elif rule_name.startswith('_'):
                repl = rule_name[1:]

            for index, text in enumerate(self.texts):
                self.texts[index] = pattern.sub(repl, text.lower())
        return self.texts


if __name__ == "__main__":
    import os
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    import sys
    sys.path.append(os.path.abspath("../../"))

    from dataset import get_sms_dataset
    data_df = get_sms_dataset()
    testPuridier = TextPurifier(texts=data_df['message'].to_list())

    exit()
    print('|-----------------Import Test------------------|')
    print(data_df.head())

    print('|-----------------__str__ Test-----------------|')
    print(testPuridier)

    print('|-------------------iter Test--------------------|')
    for rule_name, matched_strings in testPuridier.show_iter():
        print(f'Rule name: {rule_name:10s} \n {matched_strings}')

    print('|-----------------purify Test------------------|')
    texts = testPuridier.purify()
    print('As show in dataframe:')
    data_df['message'] = texts
    print(data_df.head())

    print('Iter inspect Again:')
    testPuridier.set_texts(texts)
    for rule_name, matched_strings in testPuridier.show_iter():
        print(f'Rule name: {rule_name:10s} \n {matched_strings}')
