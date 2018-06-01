#coding=utf-8
from haystack import indexes
from models import GoodsInfo  # 导入当前数据　表
#指定对于某个类的某些数据建立索引，　当前设置的类名为ｇｏｏｄｓｉｎｆｏｉｎｄｅｘ继承于　ｉｎｄｅｘｅｓ属性
class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #　检索ｔｅｘｔ字段的

    def get_model(self):
        return GoodsInfo # 建立索引的表。　就对此表进行检索　,生成该表索引后到ｗｈｏｏｓｈ_index

    def index_queryset(self, using=None):
        return self.get_model().objects.all()