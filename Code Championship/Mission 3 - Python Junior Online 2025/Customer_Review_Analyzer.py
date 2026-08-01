positive_keywords = {'good', 'great', 'fast', 'helpful'}
negative_keywords = {'bad', 'slow', 'poor', 'not'}

def analyze_reviews(reviews):
    count_positive = 0
    count_negative = 0
    
    for review in reviews:
        negative = False
        positive = False
        
        for word in review.split(' '):
            if word in negative_keywords:
                negative = True
            elif word in positive_keywords:
                positive = True
        if positive and not negative:
            count_positive += 1
        else:
            count_negative += 1
                
    return (count_positive, count_negative)


while True:
    reviews = input("Enter reviews: ").lower()
    
    if len(reviews) == 0:
        print('No reviews entered, try again!')
    else:
        reviews_list = reviews.split(',')
        positive_reviews_count, negative_reviews_count = analyze_reviews(reviews_list)
        print(f"Reviews Count: {positive_reviews_count + negative_reviews_count}")
        print(f"Positive reviews count: {positive_reviews_count}")
        print(f"Negative reviews count: {negative_reviews_count}")
        print(f"Satisfication Ratio: {(positive_reviews_count / (positive_reviews_count + negative_reviews_count)) * 100 :.2f}%")
        