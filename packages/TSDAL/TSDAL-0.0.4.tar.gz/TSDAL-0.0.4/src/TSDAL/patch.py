import json


class Patch:

#导出json
    def expoortJson(self):
        text1 = {}
        text1["ID"] = self.ID
        text1["FatherNode"] = self.FatherNode
        text1["GridNum"] = self.FatherNode
        text1["Href"] = self.Href
        textarr = []
        textarr.append(text1)
        # print(textarr)
        jtext = json.dumps(textarr, ensure_ascii=False)
        return jtext

    def setId(self,ID):
        self.ID = ID

    def setFatherNode(self,FatherNode):
        self.FatherNode = FatherNode

    def setGridNum(self,GridNum):
        self.GridNum = GridNum

    def setHref(self,Href):
        self.Href = Href
