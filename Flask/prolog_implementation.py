import pytholog

knowledge_base = pytholog.KnowledgeBase('KB')
knowledge = [
    'father(X, Y):- male(X), parent(X, Y)',
    'mother(X, Y):- female(X), parent(X, Y)',
    'child(X, Y):- parent(Y, X)'
]
knowledge_base(knowledge)

def set_fact(fact, value, value2=None):
    if value2:
        new_fact = fact + '(' + value.lower() + ',' + value2.lower() + ')'
    else:
        new_fact = fact + '(' + value.lower() + ')'

    knowledge.insert(0, new_fact)
    knowledge_base(knowledge)
    bot.respond('reset facts', 'user1')


def query_kb(fact, value):
    bot.respond('reset questions', 'user1')
    query = fact + '(X, ' + value.lower().strip() + ')'
    result = knowledge_base.query(pytholog.Expr(query))

    response = ''
    for value in result:
        try:
            response += value['X'].title() + ', '
        except:
            return None
    
    return response[:-2]


# function to check predicates
def check_predicates():
    male = bot.getPredicate('male', 'user1')
    female = bot.getPredicate('female', 'user1')
    parent = bot.getPredicate('parent', 'user1')
    child = bot.getPredicate('child', 'user1')
    father_of = bot.getPredicate('father_of', 'user1')
    mother_of = bot.getPredicate('mother_of', 'user1')
    child_of = bot.getPredicate('child_of', 'user1')

    result = None

    if male != 'unknown':
        set_fact('male', male)
    elif female != 'unknown':
        set_fact('female', female)
    elif parent != 'unknown':
        set_fact('parent', parent, child)
    elif father_of != 'unknown':
        result = query_kb('father', father_of)
    elif mother_of != 'unknown':
        result = query_kb('mother', mother_of)
    elif child_of != 'unknown':
        result = query_kb('child', child_of)
    
    return result
