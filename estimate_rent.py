import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Render(QWebEngineView):
    def __init__(self, url):
        self.html = None
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        #self.setHtml(html)
        self.load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        # This is an async call, you need to wait for this
        # to be called before closing the app
        self.page().toHtml(self._callable)

    def _callable(self, data):
        self.html = data
        # Data has been stored, it's safe to quit the app
        self.app.quit()


if __name__ == '__main__':
    # import requests
    #
    boa_url = "https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address="
    boa_substitute = lambda x: boa_url + str(x).replace(',', '').replace(' ', '+')
    address = '7318 MIDDLEBURY PL, CHARLOTTE, NC 28212'

    url = boa_substitute(address)#
    url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address={}'.format(address)
    # url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=7318+MIDDLEBURY+PL+CHARLOTTE+NC+28212'
    url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=7318+MIDDLEBURY+PL+CHARLOTTE+NC+28212'
    url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=7318+MIDDLEBURY+PL+CHARLOTTE+NC+28212'

    print(url)

    #
    # resp = requests.get(url, stream=True)
    # print(resp.text)
    res = Render(url).html
    print(res)
    open('del.html','w').write(res)
