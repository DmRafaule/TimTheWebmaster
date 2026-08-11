from django.test import LiveServerTestCase, RequestFactory, TestCase
from django.core.files.base import ContentFile

from Post.templatetags.addToListInURL import addToListInURL
from Post.templatetags.hasInList import hasInList 
from Post.templatetags.listToURL import listToURL 
from Post.templatetags.removeFromListInURL import removeFromListInURL
from Post.templatetags.urlToBreadcrumbs import urlToBreadcrumbs
from Post.templatetags.urlToList import urlToList
from Post.models import Article, Category, Tag


class PostTemplateTagsTest(LiveServerTestCase):
    ''' Проверка кастомных тегов для использования в шаблонах '''

    def test_addToListInURL_if_new_tag_will_be_added(self):
        ''' Проверка кастомного тега addToListInURL, если новый тег будет добавлен'''
        tags = ['tag1', 'tag2', 'tag3']
        old_path = '&tag=tag1&tag=tag2&tag=tag3'
        new_tag = 'tag4'
        new_path = addToListInURL(new_tag, tags)
        self.assertEqual(new_path, f"&tag={new_tag}{old_path}")

    def test_addToListInURL_if_new_tag_will_not_be_added(self):
        ''' Проверка кастомного тега addToListInURL, если новый тег не будет добавлен'''
        tags = ['tag1', 'tag2', 'tag3']
        old_path = '&tag=tag1&tag=tag2&tag=tag3'
        new_tag = 'tag2'
        new_path = addToListInURL(new_tag, tags)
        self.assertEqual(len(new_path), len(old_path))
    
    def test_if_hasInList_will_true(self):
        ''' Проверка кастомного тега hasInList, если элемент будет найден в списке '''
        items = ['item1', 'item2', 'item3']
        item_old = 'item1'
        self.assertTrue(hasInList(item_old, items))
    
    def test_if_hasInList_will_false(self):
        ''' Проверка кастомного тега hasInList, если элемент не будет найден в списке '''
        items = ['item1', 'item2', 'item3']
        item_new = 'item4'
        self.assertFalse(hasInList(item_new, items))
    
    def test_listToURL_convert(self):
        ''' Проверка кастомного тега listToURL, который конвертирует список тегов в часть параметров запроса в URL '''
        items = ['item1', 'item2', 'item3']
        url = listToURL(items)
        self.assertEqual(url, '&tag=item1&tag=item2&tag=item3')

    def test_removeFromListInURL_to_be_removed(self):
        ''' Проверка кастомного тега removeFromListInURL, по удалению элемента из URL '''
        tags = ['tag1', 'tag2', 'tag3']
        tag_to_remove = 'tag1'
        new_path = removeFromListInURL(tag_to_remove, tags)
        self.assertEqual(new_path, '&tag=tag2&tag=tag3')

    def test_removeFromListInURL_not_to_be_removed(self):
        ''' Проверка кастомного тега removeFromListInURL, по не состоявшемуся удалению элемента из URL '''
        tags = ['tag1', 'tag2', 'tag3']
        old_path = '&tag=tag1&tag=tag2&tag=tag3'
        tag_to_remove = 'tag4'
        new_path = removeFromListInURL(tag_to_remove, tags)
        self.assertEqual(new_path, old_path)
    
    def test_urlToList_to_split_url_onto_el(self):
        ''' Проверка кастомного тега urlToList, по конвертации URL в список '''
        url = 'http://website.com/ru/articles/?page=1&tag=tag1&tag=tag2'
        items = urlToList(url)
        self.assertEqual(len(items), 3)

    def test_urlToBreadcrumbs(self):
        ''' Проверка кастомного тега urlToBreadcrumbs, по конвертации URL в список с необходимыми данными для 
         специальной разметки '''
        # Создаём две необходимые категории для хранения статей и инструментов
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        # Создаём статью
        file = ContentFile('Some text', name=f"index.html")
        article = Article(slug=f"article-1", template=file)
        article.save()
        # Создаём необходимый минимум тегов
        tag1 = Tag(slug_en=f"tag1", slug_ru=f"tag1", name_en=f"First tag", name_ru=f"Первый  тег")
        tag1.save()
        tag2 = Tag(slug_en=f"tag2", slug_ru=f"tag2", name_en=f"Second tag", name_ru=f"Второй тег")
        tag2.save()
        # Тестовые адреса
        url_one_lev = 'http://website.com/ru/'
        url_second_lev = 'http://website.com/ru/articles/'
        url_third_lev_post = 'http://website.com/ru/articles/article-1/'
        url_third_lev_pagin = 'http://website.com/ru/articles/?page=1&tag=tag1&tag=tag2'
        # Проверка первого случая, где будет возвращёт только один элемент, языковой
        result_one_lev: list[dict] = urlToBreadcrumbs(url_one_lev)
        self.assertEqual(len(result_one_lev), 1)
        self.assertEqual(result_one_lev[0].get('url'), '/ru/')
        self.assertEqual(result_one_lev[0].get('level'), 1)
        # Проверка второго случая, где будет возвращёт первый элемент - языковой и второй категория
        result_second_lev: list[dict] = urlToBreadcrumbs(url_second_lev)
        self.assertEqual(len(result_second_lev), 2)
        self.assertEqual(result_second_lev[0].get('url'), '/ru/')
        self.assertEqual(result_second_lev[0].get('level'), 1)
        self.assertEqual(result_second_lev[1].get('url'), '/ru/articles/')
        self.assertEqual(result_second_lev[1].get('level'), 2)
        # Проверка третьего случая, где будет возвращёт первый элемент - языковой, и второй - категория, и третий - сама статья
        result_third_lev: list[dict] = urlToBreadcrumbs(url_third_lev_post)
        self.assertEqual(len(result_third_lev), 3)
        self.assertEqual(result_third_lev[0].get('url'), '/ru/')
        self.assertEqual(result_third_lev[0].get('level'), 1)
        self.assertEqual(result_third_lev[1].get('url'), '/ru/articles/')
        self.assertEqual(result_third_lev[1].get('level'), 2)
        self.assertEqual(result_third_lev[2].get('url'), '/ru/articles/article-1/')
        self.assertEqual(result_third_lev[2].get('level'), 3)
        # Проверка третьего случая, где будет возвращёт первый элемент - языковой, и второй - категория, и третий - страница пагинации
        result_third_lev_pagin: list[dict] = urlToBreadcrumbs(url_third_lev_pagin)
        self.assertEqual(len(result_third_lev_pagin), 3)
        self.assertEqual(result_third_lev_pagin[0].get('url'), '/ru/')
        self.assertEqual(result_third_lev_pagin[0].get('level'), 1)
        self.assertEqual(result_third_lev_pagin[1].get('url'), '/ru/articles/')
        self.assertEqual(result_third_lev_pagin[1].get('level'), 2)
        self.assertEqual(result_third_lev_pagin[2].get('url'), '/ru/articles/?page=1&tag=tag1&tag=tag2')
        self.assertEqual(result_third_lev_pagin[2].get('level'), 3)