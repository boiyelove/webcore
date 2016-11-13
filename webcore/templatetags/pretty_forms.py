# from collections import OrderedDict
# from django import template
# from django.core.urlresolvers import reverse
# from reviews.models import Category, Product
# from blog.models import Post

# register = template.Library()

# @register.filter
# def addcss(field, css):
# 	try: 
# 		if field.field.widget.input_type == "text" or field.field.widget.input_type == "password" or field.field.widget.input_type == "email" or field.field.widget.input_type == "hidden":
# 			return field.as_widget(attrs={'class': css})
# 	except:
# 		return field


# @register.filter
# def getCategories(x):
# 	cat = Category.objects.all()
# 	return cat

# @register.filter
# def topreviews(x):
# 	topreviewdict = dict()
# 	topreviewlist = list()
# 	allproduct = Product.objects.all()
# 	for product in allproduct:
# 		score = product.get_reviewscore()
# 		productslug = product.slug
# 		topreviewdict[productslug] = score

# 	newtopreviewdict = OrderedDict(sorted(topreviewdict.items(), key=lambda t: t[1], reverse=True))
# 	topreviewlist = list(newtopreviewdict.keys())
# 	topreviewlist = topreviewlist[:5]
# 	topreviewlist = Product.objects.filter(slug__in = topreviewlist)
# 	return topreviewlist



# @register.filter
# def topcategories(x):
# 	topcatydict = dict()
# 	topcatylist = list()
# 	allcategory = Category.objects.all()
# 	for caty in allcategory:
# 		score = caty.get_productscore()
# 		catyslug = caty.slug
# 		topcatydict[catyslug] = score
# 	print(topcatydict.items)
# 	topcatydict = OrderedDict(sorted(topcatydict.items(), key=lambda t: t[1], reverse=True))
# 	topcatylist = list(topcatydict.keys())
# 	topcatylist = topcatylist[:5]
# 	topcat = Category.objects.filter(slug__in = topcatylist)
# 	return topcat

# @register.filter
# def resolvemyurl(urlname):
# 	resolved = reverse(urlname)
# 	return resolved


# @register.filter
# def latestblogpost(x):
# 	lastestposts = Post.objects.all()[:3]
# 	return lastestposts

# @register.filter
# def popularblogpost(x):
# 	popularposts = Post.objects.order_by('views')[:3]
# 	return popularposts