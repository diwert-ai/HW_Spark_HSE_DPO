
from collections import Counter
from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

def read_dictionary(filename: str) -> Counter:
    '''
        Read dictionary file with words statistics.
        Function results is Counter datatype.
    '''
    #YOUR CODE HERE
    words = dict()
    with open(filename, 'r') as f:
        for line in f:
            key, val = line.split()
            words[key] = int(val)

    return Counter(words)

WORDS = read_dictionary('dictionary.txt')


def P(word, N=sum(WORDS.values())): 
    '''
        Probability of `word`: (num occurances of `word`)/ (total count of words) 
    '''
    # YOUR CODE HERE
    return WORDS[word]/N

def most_probable(word): 
    '''
        Find most probable (with max ) spelling correction for word. 
        Hint: see max function + key param 
            https://www.programiz.com/python-programming/methods/built-in/max
    '''
    # YOUR CODE HERE
    return max(candidates(word), key=lambda w: P(w))

def candidates(word): 
    '''
        Generate most nearest spelling corrections for word.
        If found word in dictionary then return word, otherwise
        try found words from one and then two edit distance
    '''
    one_symbol_change = generate_candidates_one_symbol(word)
    two_symbol_change = generate_candidates_two_symbol(word)
    return (known([word]) or known(one_symbol_change) or known(two_symbol_change) or [word])

def known(words): 
    '''
        The subset of `words` that appear in the dictionary of WORDS.
    '''
    return set(w for w in words if w in WORDS)

def generate_candidates_one_symbol(word):
    '''
        Generate candidates that are one edit symbol away from `word`.
    '''
    
    letters    = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def generate_candidates_two_symbol(word): 
    '''
        Generate all сandidates that are two edits away from `word`.
    '''
    return [
        e2 for e1 in generate_candidates_one_symbol(word)
        for e2 in generate_candidates_one_symbol(e1)
    ]

app = Flask(__name__)

@app.route('/version', methods=['GET'])
def get_version():
    # YOUR CODE HERE
    return jsonify({'version':'1.0'})

@app.route('/correct', methods=['GET'])
def correct():
    # YOUR CODE HERE
    check_word = request.args.get('check_word')
    corrected = most_probable(check_word)
    return jsonify({'correct_word': corrected})

@app.route('/add_word', methods=['POST'])
def add_word():
    # YOUR CODE HERE
    added_word =  request.json['added_word']
    WORDS[added_word] += 1

    return jsonify(success=True)

@app.route('/candidates/<int:edit_distance>', methods=['GET'])
def get_candidates(edit_distance: int):
    # YOUR CODE HERE
    word =  request.args.get('word')
    one_symbol_change = generate_candidates_one_symbol(word)
    two_symbol_change = generate_candidates_two_symbol(word)
    responses = {
        1: {'words': list(set.union(known([word]), known(one_symbol_change), [word]))},
        2: {'words': list(set.union(known([word]), known(one_symbol_change), known(two_symbol_change), [word]))}
    }
    
    return jsonify(responses[edit_distance]) if edit_distance in responses else abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
