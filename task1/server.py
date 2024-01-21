
from collections import Counter
from flask import Flask
from flask import jsonify, request, abort

def read_dictionary(filename: str) -> Counter:
    '''
        Read dictionary file with words statistics.
        Function results is Counter datatype.
    '''
    #YOUR CODE HERE FROM PREVIOUS CELL
    words = dict()
    with open(filename, 'r') as f:
        for line in f:
            key, val = line.split()
            words[key] = int(val)

    return Counter(words)

WORDS = read_dictionary('dictionary.txt')

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

@app.route('/candidates/<int:edit_distance>', methods=['GET'])
def candidates(edit_distance: int):
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
