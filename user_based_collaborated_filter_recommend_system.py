import math
import collections

users_interests = [
["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
["R", "Python", "statistics", "regression", "probability"],
["machine learning", "regression", "decision trees", "libsvm"],
["Python", "R", "Java", "C++", "Haskell", "programming languages"],
["statistics", "probability", "mathematics", "theory"],
["machine learning", "scikit-learn", "Mahout", "neural networks"],
["neural networks", "deep learning", "Big Data", "artificial intelligence"],
["Hadoop", "Java", "MapReduce", "Big Data"],
["statistics", "R", "statsmodels"],
["C++", "deep learning", "artificial intelligence", "probability"],
["pandas", "R", "Python"],
["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
["libsvm", "regression", "support vector machines"]
]

def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))
def magnitude(v):
    return math.sqrt(dot(v,v))
##cosine_similarity函数定义
def cosine_similarity(v,w):
    return dot(v,w)/(magnitude(v)*magnitude(w))

##对上面的users_interests列表进行处理，生成一个包括所有兴趣点的集合
unique_interests = sorted(list({ interest
                            for user_interests in users_interests
                                for interest in user_interests }))

##生成每个用户的兴趣列表向量
def make_user_interest_vector(user_interests):
##given a list of interests, produce a vector whose ith element is 1
##if unique_interests[i] is in the list, 0 otherwise"""
    return [1 if interest in user_interests else 0
            for interest in unique_interests]
##生成所有的用户的兴趣矩阵，user_interest_matrix[i][j]代表了第i个用户对
##j个条目是否感兴趣，如果值为1就是感兴趣，如果为0就是不感兴趣
user_interest_matrix = map(make_user_interest_vector, users_interests)
##下面的user_similarities为用户相似度矩阵，其中 user_similarities[i][j]的值
##代表了用户i和用户j的相似度
user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                      for interest_vector_j in user_interest_matrix]
                          for interest_vector_i in user_interest_matrix]
##下面这个函数找出了和指定user_id的这个用户的最相似的用户的列表
def most_similar_users_to(user_id):
    pairs = [(other_user_id, similarity) # find other
            for other_user_id, similarity in # users with
            enumerate(user_similarities[user_id]) # nonzero
            if user_id != other_user_id and similarity > 0] # similarity
    return sorted(pairs, # sort them
                    key=lambda similarity: similarity, # most similar
                    reverse=True)
##
def user_based_suggestions(user_id, include_current_interests=False):
    # sum up the similarities
    suggestions = collections.defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity
    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                        key=lambda weight: weight,
                        reverse=True)
    # and (maybe) exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]



##测试一下以上的代码，比如说为用户0做推荐
print(user_based_suggestions(0))    
