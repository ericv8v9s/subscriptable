import builtins


builtins_map = map
builtins_zip = zip
builtins_filter = filter


def _fill_items(items, iterable, stop):
	if stop is None or stop < 0:
		items.extend(list(iterable))
	elif stop >= len(items):
		for _, val in builtins_zip(range(stop - len(items) + 1), iterable):
			items.append(val)


class Subscriptable:
	def __init__(self, source):
		self._source = source
		self._items = []

	def __getitem__(self, index):
		if isinstance(index, int):
			_fill_items(self._items, self._source, index)
		elif isinstance(index, slice):
			_fill_items(self._items, self._source, index.stop)
		else:
			raise TypeError
		return self._items[index]

	def __len__(self):
		_fill_items(self._items, self._source, None)
		return len(self._items)

	def __getattr__(self, name):
		return self._source.__getattribute__(name)


class SubscriptableMap(Subscriptable):
	@staticmethod
	def patch():
		builtins.map = SubscriptableMap

	def __init__(self, function, iterable, *iterables):
		super().__init__(builtins_map(function, iterable, *iterables))


class SubscriptableZip(Subscriptable):
	@staticmethod
	def patch():
		builtins.zip = SubscriptableZip

	def __init__(self, *iterables, strict=False):
		super().__init__(builtins_zip(*iterables, strict=strict))


class SubscriptableFilter(Subscriptable):
	@staticmethod
	def patch():
		builtins.filter = SubscriptableFilter

	def __init__(self, function, iterable):
		super().__init__(builtins_filter(function, iterable))


def patch_all():
	builtins.map = SubscriptableMap
	builtins.zip = SubscriptableZip
	builtins.filter = SubscriptableFilter
