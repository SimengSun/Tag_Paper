__author__ = 'ssm'

'''
1. prepare data(centroids, people, paper)
	parse people/paper json data
2. cluster paper (tag papers with different centroids)
	1) 1st match
	2) 2nd match, if has significant one, assign 2nd; or assign 1st;
3. match people entity to paper_clusters (if cannot match, create new entity)
	match with 2nd centroids, giving merge reminders (sibling or father node)
4. produce hot words and print
'''

import load_data as ld
import tagpaper as tp
import tagpeople as tpe
import Util
import datetime

dictionary, tfidf = Util.get_models()
print('end loading models..')

#prepare data
centroids, people, paper = ld.load_data()
print('end preparing data')

#cluster paper
tagged_paper, paper_wordweights, tfidf_kw = tp.tagpaper(centroids, paper, dictionary, tfidf)
print('end tagging paper {}'.format(datetime.datetime.now()))

#match people_entity to paper_clusters
result = tpe.tagpeople(centroids, tagged_paper, people, dictionary, tfidf)
print('end tagging people')

#print result
Util.printresult(result, paper)

#generate cloud tag
#Util.generate_cloud_tag(result, paper_wordweights)
Util.generate_cloud_tag_tfidf(result, tfidf_kw, dictionary, paper)