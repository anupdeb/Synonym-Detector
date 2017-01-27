
'''By Rojigan Gengatharan and Anup Deb''' 
import math
def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    numerator = 0 
    total1 = 0 
    total2 = 0
    for i in vec1: 
        if i in vec2:
            numerator += vec1[i] * vec2[i] 
        total1 += vec1[i]**2
        
    for i in vec2:
        total2 += vec2[i]**2 
    
    return numerator/(math.sqrt(total1*total2))
    
    
def build_semantic_descriptors(sentences):
    results = {}
    for i in range(len(sentences)):
        temp = set(sentences[i])
        for j in temp:
            if j == "":
                continue 
            if j not in results:
                results[j] = {}
            for x in temp: 
                if x == "":
                    continue 
                if x != j: 
                    if x not in results[j]:
                        results[j][x] = 0
                    results[j][x] += 1  
                    
    
    return results 
    
def build_semantic_descriptors_from_files(filenames):
    new_list = []
    for i in range(len(filenames)):
        c = open(filenames[i], "r", encoding="latin1")
        c = c.read() 
        c = c.lower() 
        middle_punc = [",", ":",";", "-"]
        end_punc = [".", "!", "?"]
        j = 0
        new_string = ""
        c = c.replace("\n"," ") 
        while j < len(c):
            temp = c[j]
            if temp in middle_punc:
                middle_punc_starting_index = j
                while (j < (len(c) - 1) and c[j] in middle_punc): 
                    j += 1
                if middle_punc_starting_index > 0 and (c[j] == " ") and (c[middle_punc_starting_index - 1] == " "):
                    j += 1
                elif middle_punc_starting_index > 0 and (c[j] != " ") and (c[middle_punc_starting_index - 1] != " "):
                    new_string += " "
                    new_string += c[j]
                    j += 1
                elif middle_punc_starting_index > 0 and (c[j] != " ") and (c[middle_punc_starting_index - 1] == " "):
                    new_string += c[j]
                    j += 1
                else: 
                    new_string += " " 
                    j += 1     
            elif temp in end_punc:
                end_punc_starting_index = j
                while (j < len(c) - 1) and (c[j] in end_punc): 
                    j += 1
                if end_punc_starting_index > 0 and (c[j] == " "):
                    new_string += "." 
                    j += 1
                elif end_punc_starting_index > 0 and (c[j] != " "):
                    new_string += "."
                    new_string += c[j] 
                    j += 1 
            else:
                if temp != " ":    
                    new_string += temp
                else:
                    if j > 0 and c[j-1] != " ":
                        new_string += " " 
                    
                j += 1
                
                
                
        new_string = new_string.split(".") 
        new_list += new_string
    for i in range(len(new_list)):
        new_list[i] = new_list[i].split(" ") 
    return build_semantic_descriptors(new_list)         
            


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):  
    new_word_order = word.lower() 
    
    k = semantic_descriptors.get(new_word_order, 2)
    x = semantic_descriptors.get(choices[0].lower(), 2)
    max_word = choices[0].lower() 
    if k == 2 or x == 2:
        max_score = -1 
    else:
        max_score = similarity_fn(k,x) 
    if k == 2:
        return -1 
    for i in range(1,len(choices)):
        x = semantic_descriptors.get(choices[i].lower(), 2)
        if x == 2: 
            temp = -1 
        else: 
            temp = similarity_fn(k,x)
        if temp > max_score :
            max_word = choices[i].lower() 
            max_score = temp
        
    return max_word 

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    s = open(filename, "r", encoding="latin1")
    s = s.read() 
    s = s.split("\n")
    
    for i in range(len(s)):
        s[i] = s[i].split(" ") 
    total_questions = len(s) 
    total_right_answers = 0 
    for i in range(len(s)):
        if s[i][0] == "":
            total_questions -= 1
            continue 
        target = s[i][0] 
        answer = s[i][1]
        calced_answer = most_similar_word(target, s[i][2::], semantic_descriptors, similarity_fn)
        if calced_answer == answer:
            total_right_answers += 1
    return (total_right_answers/total_questions) * 100

def euclidean_space(v1, v2):
    new_vector = {}
    for key in v1:
        new_vector[key] = v1[key] 
    for key in v2:
        if new_vector.get(key, -1) != -1:
            new_vector[key] -= v2[key] 
        else:
            new_vector[key] = -v2[key]  
    return -norm(new_vector)


def euclidean_space_normalized(v1, v2):
    new_vector = {}
    norm_v1 = norm(v1)
    for key in v1:
        new_vector[key] = v1[key]
        new_vector[key] /= norm_v1
    norm_v2 = norm(v2)     
    for key in v2:
        if new_vector.get(key, -1) !=  -1:
            new_vector[key] -=  (v2[key] / norm_v2)
        else:
            new_vector[key] = -(v2[key] / norm_v2)
    return -norm(new_vector) 


if __name__ == '__main__':
    
    filenames = ['swannsway.txt', 'warandpeace.txt']
    print(run_similarity_test('test.txt', build_semantic_descriptors_from_files(filenames), euclidean_space_normalized))     
   
    
    

    
    
    
    
    
    
    
