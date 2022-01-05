import scrapy
import re

class ChampSpider(scrapy.Spider):
    name = 'champ'
    start_urls = ['https://www.leagueofgraphs.com/es/champions/runes/xayah']

    def parse(self, response):
        tables = response.css('table.data_table.perksTable.perksTableLight')
        result_runes = []
        for table in tables:
            runes = []
            for tr in table.xpath('.//tr'): # Grupo de runas
                all_runes_names = tr.xpath('.//td/div/div/img/@alt').getall() # runes name
                #all_runes_tooltips = tr.xpath('.//td/div/div/img/@tooltip').getall() # runes name
                normal_runes_opacity = tr.xpath('.//td/div/div/img/@style').getall() # length 21 (stat runes dont have img style)
                stat_runes_opacity = []

                max_opacity = 0
                max_rune_name = ""
                if len(normal_runes_opacity) > 0:
                    normal_runes_opacity = [float(re.findall(r'[0-9]+\.?\d*', opacity).pop()) for opacity in normal_runes_opacity]
                    for name, opacity in zip(all_runes_names, normal_runes_opacity):
                        if opacity > max_opacity and opacity > 0.7:
                            max_opacity = opacity
                            max_rune_name = name
                else:
                    stat_runes_opacity = tr.xpath('.//td/div/div/@style').getall() # stat runes have style in div
                    for name, opacity in zip(all_runes_names, stat_runes_opacity):
                        if opacity == '':
                            max_rune_name = name
                            break

                if max_rune_name != "":
                    runes.append(max_rune_name)
            result_runes.append(runes)
        yield {"runes" : result_runes}


