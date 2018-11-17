from tool import find_pattern_spacy_result , pair_key

def look_index_result(index):
    result , tag_sen = find_pattern_spacy_result(Tmp_VT[index])
    for item in match(result , tag_sen):
        rule , pair = item[0] , item[1]
        key = pair_key(pair)
        print('Rule : ',rule ,"|", 'Main verb : ',key ,"|", pair )  
    print("# Sentence : #")
    print('##################################################')
    print(tag_sen)
    print('##################################################')
    
def look_all_rule_count(d):
    def look_rule_count(d , rule):
        count = 0
        for verb in d[rule].keys():
            count+=len(d[rule][verb])
        return count
    for rule in d.keys():
        print(rule , look_rule_count(d , rule))
    return

def look_rule_verb_count(d , rule , number=None):
    dd = {}
    for verb in d[rule].keys():
        count = 0
        count+=len(d[rule][verb])
        dd[verb] = count
    print(sorted(dd.items() , key = lambda x:x[1] , reverse=True)[:number])
    return 

def confuse_look(d , rule , verb , number=10):
    print("# Rule #")
    for i in d[rule][verb][:number]:
        look_index_result(i)
        print('-------------------------END--------------------------------------------')
    print('')
    print('')