import json
import csv
import re

INPUT = 'wiki.csv'
OUTPUT = 'w_declensions_v2.json'

MAP = {
  'hy-noun-ի-ներ': {
    'singular': [
      ('nominative', '', ''),
      ('dative', '', 'ի'),
      ('ablative', '', 'ից'),
      ('instrumental', '', 'ով'), 
      ('locative', '', 'ում'), 
      ('nominative', 'definite', 'ը'), 
      ('nominative', 'definite', 'ն'), 
      ('dative', 'definite', 'ին'),
      ('nominative', 'first', 'ս'),
      ('dative', 'first', 'իս'),
      ('ablative', 'first', 'իցս'),
      ('instrumental', 'first', 'ովս'),
      ('locative', 'first', 'ումս'),
      ('nominative', 'second', 'դ'),
      ('dative', 'second', 'իդ'),
      ('ablative', 'second', 'իցդ'),
      ('instrumental', 'second', 'ովդ'),
      ('locative', 'second', 'ումդ'),
    ],
    'plural': [
      ('nominative', '', 'ներ'),
      ('dative', '', 'ների'),
      ('ablative', '', 'ներից'),
      ('instrumental', '', 'ներով'),
      ('locative', '', 'ներում'),
      ('nominative', 'definite', 'ները'),
      ('nominative', 'definite', 'ներն'),
      ('dative', 'definite', 'ներին'),
      ('nominative', 'first', 'ներս'),
      ('dative', 'first', 'ներիս'),
      ('ablative', 'first', 'ներիցս'),
      ('instrumental', 'first', 'ներովս'),
      ('locative', 'first', 'ներումս'),
      ('nominative', 'second', 'ներդ'),
      ('dative', 'second', 'ներիդ'),
      ('ablative', 'second', 'ներիցդ'),
      ('instrumental', 'second', 'ներովդ'),
      ('locative', 'second', 'ներումդ'),
    ],
  },
  'hy-noun-ի-եր': {
    'singular': [
      ('nominative', '', ''),
      ('dative', '', 'ի'),
      ('ablative', '', 'ից'),
      ('instrumental', '', 'ով'),
      ('locative', '', 'ում'),
      ('nominative', 'definite', 'ը'),
      ('nominative', 'definite', 'ն'),
      ('dative', 'definite', 'ին'),
      ('nominative', 'first', 'ս'),
      ('dative', 'first', 'իս'),
      ('ablative', 'first', 'իցս'),
      ('instrumental', 'first', 'ովս'),
      ('locative', 'first', 'ումս'),
      ('nominative', 'second', 'դ'),
      ('dative', 'second', 'իդ'),
      ('ablative', 'second', 'իցդ'),
      ('instrumental', 'second', 'ովդ'),
      ('locative', 'second', 'ումդ'),
    ],
    'plural': [
      ('nominative', '', 'եր'),
      ('dative', '', 'երի'),
      ('ablative', '', 'երից'),
      ('instrumental', '', 'երով'),
      ('locative', '', 'երում'),
      ('nominative', 'definite', 'երը'),
      ('nominative', 'definite', 'երն'),
      ('dative', 'definite', 'երին'),
      ('nominative', 'first', 'երս'),
      ('dative', 'first', 'երիս'),
      ('ablative', 'first', 'երիցս'),
      ('instrumental', 'first', 'երովս'),
      ('locative', 'first', 'երումս'),
      ('nominative', 'second', 'երդ'),
      ('dative', 'second', 'երիդ'),
      ('ablative', 'second', 'երիցդ'),
      ('instrumental', 'second', 'երովդ'),
      ('locative', 'second', 'երումդ'),
    ],
  },
  'hy-noun-ություն': {
    'singular': [
      ('nominative', '', 'ություն'),
      ('dative', '', 'ության'),
      ('ablative', '', 'ությունից'),
      ('instrumental', '', 'ությամբ'),
      ('instrumental', '', 'ությունով'),
      ('locative', '', 'ությունում'),
      ('nominative', 'definite', 'ությունը'),
      ('nominative', 'definite', 'ությունն'),
      ('dative', 'definite', 'ությանը'),
      ('dative', 'definite', 'ությանն'),
      ('nominative', 'first', 'ությունս'),
      ('dative', 'first', 'ությանս'),
      ('ablative', 'first', 'ությունիցս'),
      ('instrumental', 'first', 'ությունովս'),
      ('instrumental', 'first', 'ությամբս'),
      ('locative', 'first', 'ությունումս'),
      ('nominative', 'second', 'ությունդ'),
      ('dative', 'second', 'ությանդ'),
      ('ablative', 'second', 'ությունիցդ'),
      ('instrumental', 'second', 'ությամբդ'),
      ('instrumental', 'second', 'ությունովդ'),
      ('locative', 'second', 'ությունումդ'),
    ],
    'plural': [
      ('nominative', '', 'ություններ'),
      ('dative', '', 'ությունների'),
      ('dative', '', 'ությանց'),
      ('ablative', '', 'ություններից'),
      ('instrumental', '', 'ություններով'),
      ('locative', '', 'ություններում'),
      ('nominative', 'definite', 'ությունները'),
      ('nominative', 'definite', 'ություններն'),
      ('dative', 'definite', 'ություններին'),
      ('nominative', 'first', 'ություններս'),
      ('dative', 'first', 'ություններիս'),
      ('dative', 'first', 'ությանցս'),
      ('ablative', 'first', 'ություններիցս'),
      ('instrumental', 'first', 'ություններովս'),
      ('locative', 'first', 'ություններումս'),
      ('nominative', 'second', 'ություններդ'),
      ('dative', 'second', 'ություններիդ'),
      ('dative', 'second', 'ությանցդ'),
      ('ablative', 'second', 'ություններիցդ'),
      ('instrumental', 'second', 'ություններովդ'),
      ('locative', 'second', 'ություններումդ'),
    ],
  },
  'hy-noun-ու-ներ': {
    'singular': [
      ('nominative', '', ''),
      ('dative', '', 'ու'),
      ('ablative', '', 'ուց'),
      ('instrumental', '', 'ով'),
      ('locative', '', 'ում'),
      ('nominative', 'definite', 'ն'),
      ('dative', 'definite', 'ուն'),
      ('nominative', 'first', 'ս'),
      ('dative', 'first', 'ուս'),
      ('ablative', 'first', 'ուցս'),
      ('instrumental', 'first', 'ովս'),
      ('locative', 'first', 'ումս'),
      ('nominative', 'second', 'դ'),
      ('dative', 'second', 'ուդ'),
      ('ablative', 'second', 'ուցդ'),
      ('instrumental', 'second', 'ովդ'),
      ('locative', 'second', 'ումդ'),
    ],
    'plural': [
      ('nominative', '', 'ներ'),
      ('dative', '', 'ների'),
      ('ablative', '', 'ներից'),
      ('instrumental', '', 'ներով'),
      ('locative', '', 'ներում'),
      ('nominative', 'definite', 'ները'),
      ('nominative', 'definite', 'ներն'),
      ('dative', 'definite', 'ներին'),
      ('nominative', 'first', 'ներս'),
      ('dative', 'first', 'ներիս'),
      ('ablative', 'first', 'ներիցս'),
      ('instrumental', 'first', 'ներովս'),
      ('locative', 'first', 'ներումս'),
      ('nominative', 'second', 'ներդ'),
      ('dative', 'second', 'ներիդ'),
      ('ablative', 'second', 'ներիցդ'),
      ('instrumental', 'second', 'ներովդ'),
      ('locative', 'second', 'ներումդ'),
    ],
  },
  'hy-noun-ան-ներ': {
    'singular': [
      ('nominative', '', ''),
      ('dative', '', 'ի'),
      ('dative', '', 'ան'),
      ('ablative', '', 'ից'),
      ('instrumental', '', 'ով'),
      ('instrumental', '', 'ամբ'),
      ('locative', '', 'ում'),
      ('nominative', 'definite', 'ը'),
      ('nominative', 'definite', 'ն'),
      ('dative', 'definite', 'անը'),
      ('dative', 'definite', 'անն'),
      ('dative', 'definite', 'ին'),
      ('nominative', 'first', 'ս'),
      ('dative', 'first', 'իս'),
      ('dative', 'first', 'անս'),
      ('ablative', 'first', 'իցս'),
      ('instrumental', 'first', 'ովս'),
      ('locative', 'first', 'ումս'),
      ('nominative', 'second', 'դ'),
      ('dative', 'second', 'իդ'),
      ('dative', 'second', 'անդ'),
      ('ablative', 'second', 'իցդ'),
      ('instrumental', 'second', 'ովդ'),
      ('locative', 'second', 'ումդ'),
    ],
    'plural': [
      ('nominative', '', 'ներ'),
      ('dative', '', 'ների'),
      ('ablative', '', 'ներից'),
      ('instrumental', '', 'ներով'),
      ('locative', '', 'ներում'),
      ('nominative', 'definite', 'ները'),
      ('nominative', 'definite', 'ներն'),
      ('dative', 'definite', 'ներին'),
      ('nominative', 'first', 'ներս'),
      ('dative', 'first', 'ներիս'),
      ('ablative', 'first', 'ներիցս'),
      ('instrumental', 'first', 'ներովս'),
      ('locative', 'first', 'ներումս'),
      ('nominative', 'second', 'ներդ'),
      ('dative', 'second', 'ներիդ'),
      ('ablative', 'second', 'ներիցդ'),
      ('instrumental', 'second', 'ներովդ'),
      ('locative', 'second', 'ներումդ'),
    ],
  },
  'hy-noun-ոջ-եր': {
    'singular': [
      ('nominative', '', ''),
      ('dative', '', 'ոջ'),
      ('ablative', '', 'ոջից'),
      ('instrumental', '', 'ոջով'),
      ('nominative', 'definite', 'ը'),
      ('nominative', 'definite', 'ն'),
      ('dative', 'definite', 'ոջը'),
      ('dative', 'definite', 'ոջն'),
      ('nominative', 'first', 'ս'),
      ('dative', 'first', 'ոջս'),
      ('ablative', 'first', 'ոջիցս'),
      ('instrumental', 'first', 'ոջովս'),
      ('nominative', 'second', 'դ'),
      ('dative', 'second', 'ոջդ'),
      ('ablative', 'second', 'ոջիցդ'),
      ('instrumental', 'second', 'ոջովդ'),
    ],
    'plural': [
      ('nominative', '', 'եր'),
      ('dative', '', 'երի'),
      ('ablative', '', 'երից'),
      ('instrumental', '', 'երով'),
      ('nominative', 'definite', 'երը'),
      ('nominative', 'definite', 'երն'),
      ('dative', 'definite', 'երին'),
      ('nominative', 'first', 'երս'),
      ('dative', 'first', 'երիս'),
      ('ablative', 'first', 'երիցս'),
      ('instrumental', 'first', 'երովս'),
      ('nominative', 'second', 'երդ'),
      ('dative', 'second', 'երիդ'),
      ('ablative', 'second', 'երիցդ'),
      ('instrumental', 'second', 'երովդ'),
    ],
  },
}

def parse(word, attr):
  if attr[:2] == '{{':
    attr = attr[2:]
  if attr[-2:] == '}}':
    attr = attr[:-2]
  
  attr = attr.split('-')
  
  dec_arr = []
  
  if len(attr) == 4:
    word_dec = attr[2]
    
    if '|' in attr[-1]:
      root = attr[-1].split('|')[-1]
      attr[-1] = attr[-1].split('|')[0]
      word_qnt = attr[-1]
    else:
      root = word
      word_qnt = attr[-1]
    
    declension = MAP.get('-'.join(attr[:4]))
    
    if declension:
      for i in declension:
        for d, form, dec in declension[i]:
          context = {
            'word': ''.join([(word if dec == '' else root), dec]),
            'declension_type': word_dec,
            'declension': d,
            'quantity_ending': word_qnt,
            'quantity_type': i,
            'form': form,
          }
          dec_arr.append(context)
    
  return dec_arr
  
if __name__ == '__main__':
  dictionary = []
  out_file = open(OUTPUT, 'w+', encoding='utf-8')
  
  with open(INPUT, 'r+', encoding='utf-8') as in_file:
    csvreader = csv.reader(in_file, delimiter=',')
    n = 0
    l = 0
    for row in csvreader:
      if isinstance(row, list) and len(row) == 2:
        attr = re.findall(r'\{\{hy\-.+\}\}', row[1])
        if attr:
          parsed_word = parse(row[0], attr[0])
          if parsed_word:
            dictionary.append(parsed_word)
            l += len(parsed_word)
            n += 1
  print(n, l)
  parsed = json.dumps(dictionary, ensure_ascii=False).encode('utf8')
  out_file.write(parsed.decode('utf8'))
  out_file.close()
  
  '''
  1+146+75+1+3193 ? 3810
  ---
  3850
  '''