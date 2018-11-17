def match(spacy_result , tag_sen):
    Rule = []
    for pair in spacy_result:
        if pair[0] and pair[1]:
            before , after = pair[0] , pair[1]
            tmp_b , tmp_bb , tmp_a , tmp_aa  = '' , '' , '' , ''
            now_b , past_b , future_b = now(before) , past(before) , future(before)
            now_a , past_a , future_a = now(after) , past(after) , future(after)
            #print(now_b , past_b , future_b)
            #print(now_a , past_a , future_a)
            simple_b , nowing_b , finish_b , finishing_b = simple(before) , nowing(before) , finish(before) , finishing(before)
            simple_a , nowing_a , finish_a , finishing_a = simple(after) , nowing(after) , finish(after) , finishing(after)
            tmp_b = find_time(tmp_b , now_b , past_b , future_b)
            tmp_bb = find_tense(tmp_bb , simple_b , nowing_b , finish_b , finishing_b )
            tmp_a = find_time(tmp_a , now_a , past_a , future_a)
            tmp_aa = find_tense(tmp_aa , simple_a , nowing_a , finish_a , finishing_a )
            #print(tmp_b , tmp_a)
            #print(tmp_bb , tmp_aa)
            if tmp_a and tmp_b:
                rule1 = tmp_b + '->' + tmp_a
                Rule.append((rule1 , pair))
                #print(rule)
                #print(before , after)
                #print(tag_sen)
            if tmp_aa and tmp_bb:
                rule2 = tmp_bb + '->' + tmp_aa
                Rule.append((rule2 , pair))
                #print(before , after)
                #print(tag_sen)
    return Rule


def now(pair):
    try:
        if not future(pair):
            if pair[0][1]=='VBP' or pair[0][1]=='VBZ':
                return 'now'
    except:pass
def past(pair):
    try:
        if not future(pair):
            if pair[0][1]=='VBD':
                return 'past'
    except:pass
def future(pair):
    try:
        if ((pair[0][0]=='is' or pair[0][0]=='are' or pair[0][0]=='am')  and pair[1][0]=='going') or pair[0][0]=='will':
            if pair[-1][1]=='VB':
                return 'future'
    except:pass
    

def simple(pair):
    try:
        if not nowing(pair) and not finish(pair) and not finishing(pair):
            if now(pair) or past(pair) or future(pair):
                return 'simple'
    except:pass
def nowing(pair):
    try:
        if len(pair)==2:
            if pair[0][0]=='is' or pair[0][0]=='are' or pair[0][0]=='am' or pair[0][0]=='was' or pair[0][0]=='were':
                if pair[-1][1]=='VBG':
                    return 'nowing'
            if pair[0][0]=='will':
                if pair[1][0]=='be':
                    if pair[-1][1]=='VBG':
                        return 'nowing'
    except:pass
    
def finish(pair):
    try:
        if len(pair)==2:
            if pair[0][0]=='have' or pair[0][0]=='has'or pair[0][0]=='had':
                if pair[-1][1]=='VBN' and pair[-1][0] != 'been':
                    return 'finish'
        if len(pair)==3:
            if pair[0][0]=='will':
                if pair[1][0]=='have':
                    if pair[-1][1]=='VBN' and pair[-1][0] != 'been':
                        return 'finish'
    except:pass
def finishing(pair):
    try:
        if len(pair)==3:
            if pair[0][0]=='have' or pair[0][0]=='has'or pair[0][0]=='had':
                if pair[1][0]=='been':
                    if pair[-1][1]=='VBG':
                        return 'finishing'
        if len(pair)==4:
            if pair[0][0]=='will':
                if pair[1][0]=='have':
                    if pair[2][0]=='been':
                        if pair[-1][1]=='VBG':
                            return 'finishing'
    except:pass
    
def find_time(tmp , now , past , future):
    if not tmp:
        if now : tmp = now
        elif past : tmp = past
        elif future : tmp = future
    return tmp
def find_tense(tmp , simple , nowing , finish , finishing):
    if not tmp:
        if simple : tmp = simple
        elif nowing : tmp = nowing
        elif finish : tmp= finish
        elif finishing : tmp = finishing
    return tmp