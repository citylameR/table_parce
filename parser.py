from time import perf_counter
import requests
from lxml import html

from models import session, Auction


def parse_page(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    data = []

    rows = tree.xpath('//tbody/tr')
    for row in rows:
        date = row.xpath('.//td[1]/a/text()')[0].strip()
        place = row.xpath('.//td[2]/a/text()')[0].strip()
        region = row.xpath('.//td[3]/a/text()')[0].strip()
        status = row.xpath('.//td[4]/a/text()')[0].strip()

        link = row.xpath('.//td[4]/a/@href')[0]
        auction_data = parse_auction_page('https://nedradv.ru' + link)

        data.append({
            'date': date,
            'place': place,
            'region': region,
            'status': status,
            **auction_data
        })
    return data


def parse_auction_page(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    deadline = tree.xpath('//text()[contains(.,"Срок подачи заявок")]/parent::*/following-sibling::dd[1]/text()')
    deadline = deadline[0].strip() if deadline else None

    fee = tree.xpath('//text()[contains(.,"Взнос за участие в аукционе")]/parent::*/following-sibling::dd[1]/text()')
    fee = fee[0].strip() if fee else None

    organizer = tree.xpath('//text()[contains(.,"Организатор")]/parent::*/following-sibling::dd[1]/text()')
    organizer = organizer[0].strip() if organizer else None

    return {
        'deadline': deadline,
        'fee': fee,
        'organizer': organizer
    }


if __name__ == '__main__':

    for page in range(1, 40):
        start = perf_counter()
        url = f'https://nedradv.ru/nedradv/ru/auction?ap={page}'
        print(url)
        data = parse_page(url)
        for auction in data:
            auction_model = Auction(
                date=auction['date'],
                place=auction['place'],
                region=auction['region'],
                status=auction['status'],
                deadline=auction['deadline'],
                fee=auction['fee'],
                organizer=auction['organizer']
            )

            session.add(auction_model)

        session.commit()
        print(data)
        print(len(data))
        print(f'time: {perf_counter() - start}:.02f')
