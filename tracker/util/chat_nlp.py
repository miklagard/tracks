import nltk.classify.util
import os
from word2number import w2n
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from django.conf import settings

def find_chat_node(conditions, answer):
	for condition in conditions['if']:
		if answer == condition:
			return conditions['if'][condition]

	return conditions['default']


def determinate_yes_or_no(sentence):
	'''
		Returns true if answer is yes.
	'''
	word_feats = lambda words: dict([(word, True) for word in words])
	 
	positive_vocab = [ 'yes', 'ja', 'have', 'da', 'are', 'several', 'some' ]
	negative_vocab = [ 'no', 'not',' have no', 'don\'t', 'aren\'t' ]
	 
	positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
	negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
	 
	train_set = negative_features + positive_features
	 
	classifier = NaiveBayesClassifier.train(train_set) 
	 
	# Predict
	neg = 0
	pos = 0
	sentence = sentence.lower()
	words = sentence.split(' ')

	for word in words:
	    classResult = classifier.classify(word_feats(word))
	    if classResult == 'neg':
	        neg = neg + 1
	    if classResult == 'pos':
	        pos = pos + 1

	if pos > neg:
		return 'yes'
	else:
		return 'no'


def get_numbers_in_sentence(sentence):
	result = 0

	try:
		result = w2n.word_to_num(sentence)
	except:
		sentence_pos = nltk.pos_tag(sentence.split())

		for word in sentence_pos:
			if word[1] == 'CC': # Is number?
				result = word[0]

	return result