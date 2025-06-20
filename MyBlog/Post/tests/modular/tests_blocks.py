import os
import time
import lxml

from django.test import RequestFactory, LiveServerTestCase
from django.core.files.base import ContentFile
from django.template import loader
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from bs4 import BeautifulSoup
import lxml.etree

from Post.models import Category, Article, Tool, Tag, Termin, Question, Note
from Post.views import article, tool
from Main.models import Media

class PostTest(StaticLiveServerTestCase):
    ''' Тесты для домашней страницы '''
    def setUp(self):
        # Создаём две необходимые категории для хранения статей и инструментов
        article_cat = Category(slug='articles', name_ru="Статьи", name_en="Articles", description_ru="Описание статей", description_en="Articles\' description" )
        article_cat.save()
        tool_cat = Category(slug='tools', name_ru="Инструменты", name_en="Tools", description_ru="Описание инструментов", description_en="Tools\' description" )
        tool_cat.save()
        # Создаём теги, для проверки соответствующего блока на стр
        tag1 = Tag(slug_en=f"tag{1}_en", slug_ru=f"teg{1}_ru", name_en=f"First {1} tag", name_ru=f"Первый {1} тег")
        tag1.save()
        tag2 = Tag(slug_en=f"tag{2}_en", slug_ru=f"teg{2}_ru", name_en=f"First {2} tag", name_ru=f"Первый {2} тег")
        tag2.save()
        # Создаём файлы для проверки соответствующего блока на стр.
        audio_file = ContentFile('TEXT', name=f"icon.mp3")
        audio = Media(file=audio_file, type=Media.AUDIO)
        audio.save()
        pdf_file = ContentFile('TEXT', name=f"icon.pdf")
        pdf = Media(file=pdf_file, type=Media.PDF)
        pdf.save()
        downloadable_file = ContentFile('TEXT', name=f"icon.mp4")
        downloadable = Media(file=downloadable_file, type=Media.RAW_FILE)
        downloadable.save()
        # Создаём определения и вопросы
        termin1 = Termin(termin_ru="t1", termin_en="t1", description_ru="t1 d", description_en="t1 d", definition_ru="t1 def", definition_en="t1 def")
        termin1.save()
        termin2 = Termin(termin_ru="t2", termin_en="t2", description_ru="t2 d", description_en="t2 d", definition_ru="t2 def", definition_en="t2 def")
        termin2.save()
        question1 = Question(question_ru="t1", question_en="t1", description_ru="t1 d", description_en="t1 d", answer_ru="t1 def", answer_en="t1 def")
        question1.save()
        question2 = Question(question_ru="t2", question_en="t2", description_ru="t2 d", description_en="t2 d", answer_ru="t2 def", answer_en="t2 def")
        question2.save()
    
        self.article1 = self.generate_article(
            1, 
            '''<h2>H2 - 1</h2>
            <h2>H2 - 2</h2> 
                <h3>H3 - 1</h3>
                <h3>H3 - 2</h3>
            <h2>H2 - 3</h2>
            

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut odio et arcu ultrices semper nec a ligula. Proin nec purus eget mi porttitor facilisis. Curabitur semper tellus id sem tincidunt bibendum. Nunc malesuada massa eu maximus consectetur. Sed ut ante eget sem cursus finibus. Vivamus in neque non dui fermentum consequat. Cras fermentum volutpat sapien et tincidunt. Nullam semper, lorem nec vestibulum lobortis, lorem eros hendrerit nibh, ut faucibus enim lacus vitae ante. Nulla vel varius purus. Nunc efficitur tincidunt lorem ut tristique. Mauris sagittis aliquet erat. Mauris eleifend placerat rhoncus. Proin dignissim rhoncus tempor. Nunc scelerisque tortor malesuada tellus placerat, eu vehicula ligula fermentum. Suspendisse eros tellus, sodales in nunc eu, porttitor aliquam ante. Curabitur vehicula urna imperdiet risus mollis feugiat.

Nulla facilisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In hac habitasse platea dictumst. Sed metus augue, fermentum quis efficitur vel, feugiat consequat sem. Donec hendrerit bibendum bibendum. Nam odio mi, iaculis at velit id, interdum consectetur tortor. Nunc hendrerit congue velit id blandit.

Cras volutpat posuere magna, a pulvinar mauris fringilla in. Morbi nec dolor sem. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed aliquam nisi rutrum dolor ullamcorper, nec lobortis lacus condimentum. Pellentesque tempor tristique augue at maximus. Praesent dictum tincidunt dui. Cras efficitur sed nulla non scelerisque. Vestibulum sed lectus quis sem rhoncus elementum vel vel magna. Aliquam elit purus, interdum id faucibus et, vestibulum et metus. Duis semper, lectus vel dictum finibus, turpis massa consequat leo, eu facilisis enim lectus vitae arcu. Ut tincidunt quam ut ligula porta, quis imperdiet mauris fermentum. Ut ac nulla metus.

Integer at velit ut ligula congue tristique nec nec magna. Ut mollis consequat justo, sed dictum justo imperdiet ut. Pellentesque aliquam, tortor ac condimentum tempor, arcu arcu lobortis nulla, quis mattis ex dolor a enim. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam luctus sagittis malesuada. Suspendisse eu posuere felis. Nullam fermentum vulputate est eget tristique. Maecenas nec arcu id est hendrerit vehicula non sit amet arcu. Mauris sed massa nisi. Suspendisse at dolor at nisl efficitur feugiat.

Morbi sed magna non nibh gravida sollicitudin at vitae orci. Praesent vel dolor ac mi lacinia vestibulum elementum sed nulla. Aenean commodo feugiat metus in volutpat. Ut suscipit hendrerit velit sed lobortis. Etiam id fringilla purus. Integer in maximus urna. In in suscipit nisi, id sagittis augue. Proin a sem mattis, fringilla ipsum a, ullamcorper nulla.

Nulla vel volutpat erat, eu faucibus lorem. Vestibulum eget luctus arcu. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam neque erat, aliquet vitae lacus sit amet, blandit venenatis mauris. Vestibulum at velit ac est facilisis molestie facilisis non augue. Vivamus elementum mauris et magna ultrices ullamcorper. Ut eget posuere ipsum, eget feugiat velit. Suspendisse erat elit, convallis sed tellus ac, dictum vehicula quam. Etiam fringilla porttitor purus vitae mollis. Nunc faucibus dui eu massa sagittis, a varius risus congue. Aenean a ante nisi.

Aliquam fringilla finibus ipsum, condimentum pulvinar diam vehicula sed. Fusce id leo at orci facilisis iaculis sed in tellus. Nulla non odio erat. Donec auctor dui sit amet augue posuere, quis placerat nibh porta. Quisque euismod id mauris ut elementum. Fusce condimentum metus ac enim pellentesque, viverra aliquet lorem mattis. Sed in lectus vel risus pharetra mollis. Nulla porttitor velit odio, et porttitor mauris facilisis et. Nulla facilisi. Integer tempus nisl ut leo rhoncus ullamcorper. Proin accumsan ipsum vitae nunc ultrices, vitae aliquet mi sollicitudin. Donec id molestie mi, id sollicitudin dui. Etiam aliquam elit arcu, at malesuada turpis malesuada quis. Donec eros nisl, ultrices id lectus gravida, porta hendrerit magna. Vestibulum ornare a mi et posuere.

Pellentesque faucibus, ligula eu porttitor tristique, ante metus ornare eros, sed maximus turpis leo id lorem. Vivamus nisl massa, iaculis eu erat ac, ultrices blandit sem. Nullam ac ex at lacus sodales semper. Integer id ornare odio, id aliquam augue. Integer eleifend tellus fermentum maximus pellentesque. Integer enim purus, rhoncus vel ullamcorper hendrerit, suscipit sit amet ipsum. Donec ut nunc mi. Phasellus et turpis vitae ex tristique iaculis vitae sed libero. Nam malesuada, dolor sit amet tristique viverra, augue sem lobortis neque, nec eleifend lectus dui sit amet urna.

Quisque ac tellus tortor. Nunc eu ipsum ac tellus mattis mattis eget id nibh. Morbi at faucibus metus, vitae consequat mi. Donec dolor ante, dignissim eget sapien sit amet, pellentesque vulputate tortor. Fusce et purus nec quam viverra porta eget ac dolor. Mauris imperdiet purus ac luctus sodales. Nunc arcu arcu, volutpat in sodales vel, dapibus in orci. Praesent laoreet nisi urna, sit amet vestibulum metus maximus in.

Maecenas ante ligula, cursus sed interdum in, interdum ut metus. In auctor sem nunc, sit amet tempor orci rhoncus eu. Aliquam quis euismod dolor. Quisque pellentesque ut ipsum sed tincidunt. Curabitur dictum sit amet arcu sit amet viverra. Sed malesuada dapibus turpis, et consequat tellus ornare id. Pellentesque sit amet dolor id est interdum porttitor ut sit amet dui. Praesent dapibus diam vitae turpis dignissim, sed pulvinar dui faucibus. Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Praesent et suscipit nisi. Proin nisi nibh, porttitor a dolor vitae, eleifend venenatis neque. Ut pellentesque aliquam metus quis vestibulum. Suspendisse sagittis luctus auctor. In egestas felis ac turpis euismod accumsan. Vestibulum dapibus posuere arcu, ut consequat turpis semper quis. Quisque ullamcorper diam id felis laoreet, id placerat metus suscipit. Etiam vitae mi in ex eleifend ornare. Phasellus sagittis gravida massa, id euismod nibh posuere vel. Cras et neque aliquet, eleifend elit pharetra, pretium ex. Nullam in risus massa. Nulla vitae lectus dolor.

Phasellus a risus nec augue lobortis rutrum. Ut volutpat enim mauris, in faucibus ligula lacinia a. Integer at tortor augue. Nunc ac venenatis lacus, sit amet faucibus tortor. Duis ac mauris sit amet dolor facilisis lacinia. Suspendisse tempus bibendum tortor, et efficitur dolor rhoncus vitae. Etiam volutpat accumsan consectetur. Quisque porta metus nisl.

<div class="text ref">Aliquam at <a href="https://wikipedia.com">nulla</a> lobortis, varius mi nec, interdum massa. Aenean eu lacus quam. Vestibulum bibendum magna vel massa lobortis aliquet nec vel nulla. Maecenas vitae metus pretium, vulputate felis a, pharetra felis. In eu tempor libero. Ut laoreet sollicitudin dolor, sed luctus lectus elementum sed. <a href="https://google.com">Ut</a> dictum fringilla ipsum ac consectetur. Suspendisse at sagittis felis. Quisque sagittis tincidunt dictum. Praesent convallis, ante sed pulvinar commodo, tortor leo dignissim ante, vitae commodo augue mi sit amet sem. Quisque <a href="https://youtube.com" >elementum</a> erat quis lobortis tempus. Morbi imperdiet nisi vel urna vulputate mollis. Sed ac quam scelerisque, aliquet sem at, feugiat nisi.</div>

Aliquam erat volutpat. Suspendisse tincidunt neque sit amet viverra mattis. Nam ornare in lectus vestibulum efficitur. Nam finibus et ipsum pretium volutpat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vivamus non nulla non ipsum aliquam sagittis a et felis. Proin vel nisi tincidunt, suscipit lorem fringilla, consequat lectus. Morbi eu consectetur magna.

Nunc et sem sed turpis pharetra ullamcorper. Nam suscipit gravida tellus eget gravida. In facilisis sagittis consequat. Ut eu dolor commodo ligula interdum pellentesque et vel enim. Nam neque libero, hendrerit eu consectetur et, facilisis sit amet sapien. Vestibulum mattis gravida enim, non viverra dolor ultricies a. Donec dictum massa a eros consequat placerat. ''', 
            '<link data-special="table_of_content" type="text/css" rel="stylesheet" href="/static/table_of_content.css">',
            '<script data-special="table_of_content" src="/static/table_of_content.js"></script> <script src="/static/Post/js/link_gather.js"></script> <script src="/static/Post/js/link_inserter.js"></script>'
        )
        
        # Генерируем похожие статьи
        self.article2 = self.generate_article(2, '', '', '')
        article3 = self.generate_article(3, '', '', '')
        # Сохраняем всё в статью
        self.article1.similar.add(self.article2)
        self.article1.similar.add(article3)
        self.article1.termins.add(termin1)
        self.article1.termins.add(termin2)
        self.article1.questions.add(question1)
        self.article1.questions.add(question2)
        self.article1.tags.add(tag1)
        self.article1.tags.add(tag2)
        self.article1.media.add(audio)
        self.article1.media.add(pdf)
        self.article1.media.add(downloadable)
        self.article1.save()


        self.tool1 = self.generate_tool_custom_template(1, '', '', '')
        self.tool2 = self.generate_tool_default(2)
        self.tool1.similar.add(self.tool2)
        self.tool1.media.add(downloadable)
        self.tool1.media.add(audio)
        self.tool1.media.add(pdf)
        self.tool1.tags.add(tag1)
        self.tool1.tags.add(tag2)
        self.tool1.save()

        self.tool2.similar.add(self.tool1)
        self.tool2.media.add(downloadable)
        self.tool2.media.add(audio)
        self.tool2.media.add(pdf)
        self.tool2.tags.add(tag1)
        self.tool2.tags.add(tag2)
        self.tool2.save()
    
    def generate_article(self, indx, content: str, styles: str, scripts: str):
        ''' Генерирует статью из шаблона по умолчанию с кастомным контекстом'''
        context = {
            "content": content,
            "styles": styles,
            "scripts": scripts,
        }
        template_file_not_rendered = loader.get_template(os.path.join('Post','article_exmpl.html'))
        template_file_rendered = template_file_not_rendered.render(context=context)
        file = ContentFile(template_file_rendered, name=f"index-{indx}.html")
        article = Article(slug=f"article-{indx}", template=file)
        article.save()
        return article
    
    def generate_tool_default(self, indx):
        ''' Генерирует инструмент по умолчанию '''
        tool = Tool(slug=f"tool-{indx}", name_ru="", name_en="", description_ru="", description_en="")
        tool.save()
        return tool
    
    def generate_tool_custom_template(self, indx, content: str, styles: str, scripts: str):
        ''' Генерирует инструмент из шаблона по умолчанию с кастомным контекстом'''
        context = {
            "content": content,
            "styles": styles,
            "scripts": scripts,
        }
        template_file_not_rendered = loader.get_template(os.path.join('Post','tool_exmpl.html'))
        template_file_rendered = template_file_not_rendered.render(context=context)
        # Я не знаю по какой причине, но Django просто не может декодировать русские буквы
        template_file_rendered = template_file_rendered.replace('Описание', '')
        file = ContentFile(template_file_rendered, name=f"index-{indx}.html")
        tool = Tool(slug=f"tool-{indx}", template=file,  name_ru=f"Инструмент {indx}", name_en=f"Tool {indx}", description_ru=f"Описание {indx}", description_en=f" Descript {indx}")
        tool.save()
        return tool

    def test_articles_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для статей'''
        for article in Article.objects.all():
            response = self.client.get(f"{self.live_server_url}{article.get_absolute_url()}")
            self.assertTemplateUsed(response, 'Post/base_article.html')

    def test_tool_with_default_template_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для инструментов у которых 
        используется шаблон по умолчанию'''
        response = self.client.get(f"{self.live_server_url}{self.tool2.get_absolute_url()}")
        self.assertTemplateUsed(response, 'Post/base_tool.html')

    def test_tool_with_custom_template_returned_right_html(self):
        ''' Тест на правильно возвращаемый шаблон для инструментов у которых 
        используется кастомно-созданный шаблон'''
        response = self.client.get(f"{self.live_server_url}{self.tool1.get_absolute_url()}")
        self.assertTemplateUsed(response, 'Post/base_tool.html')
    
    def test_rendered_html_for_article_with_appended_data(self):
        request = RequestFactory().get(f"{self.live_server_url}{self.article1.get_absolute_url()}")
        response = article(request, self.article1.slug)
        html = response.render()
        soup = BeautifulSoup(html.content, 'lxml')
        # Находим и проверяем все ли теги отображены на странице
        soup_tags = soup.select('span.tags-in-post>span')
        self.assertEqual(len(soup_tags), len(self.article1.tags.all()))
        # Находим и проверяем есть ли блок для подкаста
        dom = lxml.etree.HTML(str(soup))
        audio = dom.xpath('/html/body/main/div[2]/div[2]/ul/li[1]/audio')
        self.assertEqual(len(audio), 1)
        # Находим и проверяем есть ли блок для pdf
        pdf = dom.xpath('/html/body/main/div[2]/div[2]/ul/li[2]/div[2]')
        self.assertEqual(len(pdf), 1)
        # Находим и проверяем есть ли блок с внешними ссылками
        soup_ex_links = soup.select_one('#ex_links')
        self.assertIsNotNone(soup_ex_links)
        # Находим и проверяем есть ли блок с похожими статьями
        soup_sim_articles = soup.select_one('h3.sim-art')
        self.assertIsNotNone(soup_sim_articles)
        # Находим и проверяем есть ли блок с определениями
        soup_used_termins = soup.select_one('h3.used-term')
        self.assertIsNotNone(soup_used_termins)
        # Находим и проверяем есть ли блок с вопросами
        soup_used_questions = soup.select_one('h3.rel-que')
        self.assertIsNotNone(soup_used_questions)
    
    def test_rendered_html_for_article_without_appended_data(self):
        request = RequestFactory().get(f"{self.live_server_url}{self.article2.get_absolute_url()}")
        response = article(request, self.article2.slug)
        html = response.render()
        soup = BeautifulSoup(html.content, 'lxml')
        # Находим и проверяем все ли теги отображены на странице
        soup_tags = soup.select('span.tags-in-post>span')
        self.assertEqual(len(soup_tags), len(self.article2.tags.all()))
        # Находим и проверяем есть ли блок для подкаста
        dom = lxml.etree.HTML(str(soup))
        audio = dom.xpath('/html/body/main/div[2]/div[2]/ul/li[1]/audio')
        self.assertEqual(len(audio), 0)
        # Находим и проверяем есть ли блок для pdf
        pdf = dom.xpath('/html/body/main/div[2]/div[2]/ul/li[2]/div[2]')
        self.assertEqual(len(pdf), 0)
        # Находим и проверяем есть ли блок с похожими статьями
        soup_sim_articles = soup.select_one('h3.sim-art')
        self.assertIsNone(soup_sim_articles)
        # Находим и проверяем есть ли блок с определениями
        soup_used_termins = soup.select_one('h3.used-term')
        self.assertIsNone(soup_used_termins)
        # Находим и проверяем есть ли блок с вопросами
        soup_used_questions = soup.select_one('h3.rel-que')
        self.assertIsNone(soup_used_questions)