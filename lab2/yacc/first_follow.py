def first_follow(rules):
    from collections import OrderedDict
    firsts = []  # Used as temp storage for firsts if needed

    # Ordered dictionary to maintain the order of saving in the dictionary
    # useful when doing the actual first finding in one pass.
    rules_dict = OrderedDict()  # Dictionary to store all the rules in the grammar
    firsts_dict = OrderedDict()  # Dictionary to store all the firsts
    follow_dict = OrderedDict()  # Dictionary that stores all follows

    def non_term_appender(firsts, rules):
        """Adds the non terminals on the left to the firsts_dict"""
        for rule in rules:
            if rule[0] not in firsts:
                firsts.append(rule[0])
                firsts_dict[rule[0]] = []
                follow_dict[rule[0]] = []
    number_of_rules = len(rules)
    rule_count = first_count = 0
    non_term_appender(firsts, rules)
    for ru in rules:
        if rules_dict.has_key(ru[0]):
            rules_dict[ru[0]].append(ru[2:])
        else:
            rules_dict[ru[0]] = [ru[2:]]
        rule_count += 1

    for rule in rules:
        if rule[2] not  in firsts:
            firsts_dict[rule[0]].extend(rule[2])
    flag=True
    while flag:
        flag=False
        for rule in reversed(rules):
            if rule[2] in firsts and len([x for x in firsts_dict[rule[2]] if x not in firsts_dict[rule[0]]])>0:
                firsts_dict[rule[0]].extend(firsts_dict[rule[2]])
                flag=True

    rules_keys = rules_dict.keys()
    key_count = len(rules_keys)
    for k,lis in rules_dict.items():
        if k == rules_keys[0]:
            follow_dict[k].append('$')
        for tmp_rule_str in lis:

            for i in xrange(key_count):
                if rules_keys[i] in tmp_rule_str:
                    tmp_rule_list = tmp_rule_str
                    current_non_term_index = tmp_rule_list.index(rules_keys[i])

                    if current_non_term_index == (len(tmp_rule_list) - 1):
                        ext=[x for x in follow_dict[rules_keys[0]] if x not in follow_dict[rules_keys[i]]]
                        follow_dict[rules_keys[i]].extend(ext)
                    else:
                        ttt=tmp_rule_list[current_non_term_index+1]
                        if ttt not  in rules_keys and ttt not in follow_dict[rules_keys[i]]:
                            follow_dict[rules_keys[i]].append(ttt)
                        else:
                            ext=[x for x in firsts_dict[tmp_rule_list[current_non_term_index+1]] if x not in follow_dict[rules_keys[i]]]
                            follow_dict[rules_keys[i]].extend(ext
                                )

    print "Follow Dict:" + " " + follow_dict.__str__()
    print "Firsts Dict:" + " " + firsts_dict.__str__()
