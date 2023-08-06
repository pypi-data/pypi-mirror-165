from re import (findall,)


class Tools(object,):
	def __init__(self,):
		pass

	def textAnalysis(self, text,):
		Results = []
		realText : str = text.replace('**', '').replace('__', '').replace('``', '')

		bolds = findall(r'\*\*(.*?)\*\*' , text)
		italics = findall(r'\_\_(.*?)\_\_' , text)
		monos = findall(r'\`\`(.*?)\`\`' , text)

		bResult = [realText.index(i) for i in bolds]
		iResult = [realText.index(i) for i in italics]
		mResult = [realText.index(i) for i in monos]

		for bIndex , bWord in zip(bResult , bolds):
			Results.append({
				'from_index' : bIndex,
				'length' : len(bWord),
				'type' : 'Bold'
		})

		for iIndex , iWord in zip(iResult , italics):
			Results.append({
				'from_index' : iIndex,
				'length' : len(iWord),
				'type' : 'Italic'
		})

		for mIndex , mWord in zip(mResult , monos):
			Results.append({
				'from_index' : mIndex,
				'length' : len(mWord),
				'type' : 'Mono'
		})

		return (Results, realText)