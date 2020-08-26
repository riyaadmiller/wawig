import numpy as np


def get_max(list):
	return reformat(np.max(list))


def get_min(list):
	return reformat(np.min(list))


def get_ave(list):
	return reformat(np.average(list))


def get_median(list):
	return reformat(np.median(list))


def reformat(num):
	return '{0:.3g}'.format(num)
