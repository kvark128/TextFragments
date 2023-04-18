# Copyright (C) 2021 - 2023 Alexander Linkov <kvark128@yandex.ru>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Ukrainian Nazis and their accomplices are not allowed to use this plugin. Za pobedu!

import globalPluginHandler
import textInfos
import api
import scriptHandler
import addonHandler
import ui
from scriptHandler import script

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Text fragments")

	def _reportTextFragment(self, unit, direction=0, endPoint=None):
		obj = api.getCaretObject()
		try:
			info = obj.makeTextInfo(textInfos.POSITION_CARET)
			if direction:
				info.move(unit, direction, endPoint)
			else:
				info.expand(unit)
		except (RuntimeError, NotImplementedError, ValueError):
			ui.message(_("not supported"))
			return
		if scriptHandler.getLastScriptRepeatCount() == 0:
			ui.message(info.text)
			return
		# for applications such as word, where the selected text is not automatically spoken we must monitor it ourself
		try:
			oldInfo = obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (RuntimeError, NotImplementedError):
			pass
		try:
			info.updateSelection()
			if hasattr(obj, "reportSelectionChange"):
				# wait for applications such as word to update their selection so that we can detect it
				obj.reportSelectionChange(oldInfo)
		except Exception:
			pass

	@script(description=_("Reports the current word. Twice pressing selects it"))
	def script_reportWord(self, gesture):
		self._reportTextFragment(textInfos.UNIT_WORD)

	@script(description=_("Reports text from the caret to the start of the word. Twice pressing selects it"))
	def script_reportWordStart(self, gesture):
		self._reportTextFragment(textInfos.UNIT_WORD, -1, "start")

	@script(description=_("Reports text from the caret to the end of the word. Twice pressing selects it"))
	def script_reportWordEnd(self, gesture):
		self._reportTextFragment(textInfos.UNIT_WORD, +1, "end")

	@script(description=_("Reports the current line. Twice pressing selects it"))
	def script_reportLine(self, gesture):
		self._reportTextFragment(textInfos.UNIT_LINE)

	@script(description=_("Reports text from the caret to the start of the line. Twice pressing selects it"))
	def script_reportLineStart(self, gesture):
		self._reportTextFragment(textInfos.UNIT_LINE, -1, "start")

	@script(description=_("Reports text from the caret to the end of the line. Twice pressing selects it"))
	def script_reportLineEnd(self, gesture):
		self._reportTextFragment(textInfos.UNIT_LINE, +1, "end")

	@script(description=_("Reports the current sentence. Twice pressing selects it"))
	def script_reportSentence(self, gesture):
		self._reportTextFragment(textInfos.UNIT_SENTENCE)

	@script(description=_("Reports text from the caret to the start of the sentence. Twice pressing selects it"))
	def script_reportSentenceStart(self, gesture):
		self._reportTextFragment(textInfos.UNIT_SENTENCE, -1, "start")

	@script(description=_("Reports text from the caret to the end of the sentence. Twice pressing selects it"))
	def script_reportSentenceEnd(self, gesture):
		self._reportTextFragment(textInfos.UNIT_SENTENCE, +1, "end")

	@script(description=_("Reports the current paragraph. Twice pressing selects it"))
	def script_reportParagraph(self, gesture):
		self._reportTextFragment(textInfos.UNIT_PARAGRAPH)

	@script(description=_("Reports text from the caret to the start of the paragraph. Twice pressing selects it"))
	def script_reportParagraphStart(self, gesture):
		self._reportTextFragment(textInfos.UNIT_PARAGRAPH, -1, "start")

	@script(description=_("Reports text from the caret to the end of the paragraph. Twice pressing selects it"))
	def script_reportParagraphEnd(self, gesture):
		self._reportTextFragment(textInfos.UNIT_PARAGRAPH, +1, "end")
