import sublime
import sublime_plugin
import datetime
import traceback


class BaseTimeAggregatorCommand(sublime_plugin.TextCommand):
	zeroTime = datetime.datetime.strptime("00:00", "%H:%M")

	def lineRevWalker(self, startingindex):
		line = self.view.line(startingindex)
		while True:
			if line.begin() - 1 < 0:
				return
			line = self.view.line(line.begin()-1)
			yield self.view.substr(line)

	def tryParseTime(self, line):
		try:
			timediff = datetime.datetime.strptime(line, "%H:%M") - BaseTimeAggregatorCommand.zeroTime
			return timediff
		except ValueError:
			print('could not parse time in: %s'%line)
		except:
			print('unexpected error:')
			traceback.print_exc()

	def formatDelta(self, delta):
		hours, remainder = divmod(delta.total_seconds(), 3600)
		minutes, seconds = divmod(remainder, 60)

		if seconds != 0:
			return '%02d:%02d:%02d' % (hours, minutes, seconds)	
		return '%02d:%02d' % (hours, minutes)

	def evaluateAt(self, region, edit):
		line = self.view.line(region)
		print('prev lines:')
		walker = self.lineRevWalker(line.begin())
		c = 0
		sum = datetime.timedelta()
		for linetext in walker:
			#print('line: %s'%linetext)
			parts = linetext.split()
			if len(parts) < 1:
				print('end reached, empty line')
				break
			timediff = self.tryParseTime(linetext.split()[0])
			if not timediff:
				print('end reached, could not parse: %s'%linetext)
				break
			sum = sum + timediff
		return self.formatDelta(sum)

class CurrentLineTimeAggregatorCommand(BaseTimeAggregatorCommand):

	def run(self, edit):
		for region in reversed(self.view.sel()):
			# do in reverse order to not mess up indexes
			value = self.evaluateAt(region, edit)
			self.view.replace(edit, region, value)

class KeywordTimeAggregatorCommand(BaseTimeAggregatorCommand):

	def run(self, edit):
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		for region in reversed(self.view.find_all('<< TIMESUM')):
			# do in reverse order to not mess up indexes
			value = self.evaluateAt(region, edit)
			self.view.replace(edit, self.view.line(region.begin()), '%s << TIMESUM   (%s)'%(value, now))

