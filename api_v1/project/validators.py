from requests import get
from fastapi import HTTPException, status


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": 'The link, you have sent does not go to github. Please use: \"https://github.com/...\"'}
        )

    def sites(self):
        resp = get(self.link)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": 'Project not found.'}
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": {'error code': {resp.status_code}}}
            )

# check = CheckLink(link='https://gthub.com/Palenhame/Django_2.git',
#                   full=True
#                   )
# print(check.main())
# if check.main():
#     print('All good')
