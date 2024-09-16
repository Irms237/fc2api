import json

def check_attack_method(user_plans, attack_methods):
    allowed_methods = []
    user_plans_upper = user_plans.upper()
    
    for attack_method in attack_methods:
        if 'plans' in attack_method:
            plans_value = attack_method['plans'].upper()
            if plans_value == user_plans_upper:
                allowed_methods.append(attack_method['methods'])
        else:
            allowed_methods.append(attack_method['methods'])

    return allowed_methods