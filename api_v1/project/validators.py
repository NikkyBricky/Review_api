from requests import get


class CheckLink:
    def __init__(self,
                 link: str,
                 git: bool = False,
                 site: bool = False,
                 full: bool = False):
        if full:
            self.link = link
            self.git = True
            self.site = True
            self.full = True
        else:
            self.link = link
            self.git = git
            self.site = site
            self.full = full

    def main(self):
        answer = False
        if self.full:
            if self.gits() and self.sites():
                return self.link
        else:
            if self.git:
                answer = self.gits()
            if self.site:
                answer = self.sites()
        if answer:
            return self.link

    def gits(self):
        if 'https://github.com/' in self.link:
            return True
        raise ValueError('Ссылка которую вы передали не ведёт на github.')

    def sites(self):
        resp = get(self.link)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 404:
            raise ValueError('Страница не найдена.')
        else:
            raise ValueError(f'Код ошибки - {resp.status_code}')


# check = CheckLink(link='https://github.com/Palenhame/Django_2.git',
#                   nickname='Palenhame',
#                   project_name='Django_2',
#                   author=True)
# if check.main():
#     print('All good')
