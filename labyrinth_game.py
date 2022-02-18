import random
import json

class Action:
	"""
	Базовые свойства выбранных направлений
	"""
	def wall(self):
		text_lst = random.choice(
			[
				"Шарик влип. В стену",
				"Шарик не пережил бетонного рандеву",
				"Шарик|Ночь|стена- что может пойти не так? ;)",
			]
		)
		return {False: text_lst}

	def true_way(self):
		text_lst = random.choice(
			[
				"Верный выбор!",
				'Верный ход!',
				'Шарик на верном пути!',
			]
		)
		return {True: text_lst}

	def false_way(self):
		text_lst = random.choice(
			[
				'Шарик свернул не туда и потерялся )',
				'Шарик ошибся в выборе пути и потерялся',
			]
		)
		return {False: text_lst}

	def backward(self):
		text_lst = random.choice(
			[
				'Шарик струсил и убежал :)',
				'Шарик трус и вернулся ни с чем :)',
			]
		)
		return {False: text_lst}

	def la_fin(self):
		text_lst = 'Финиш, аплодисменты, титры. Вы победили!!!!\nА Шарик поел ;)'
		return {'la_fin': text_lst}


class GamePlay:
	"""
	Стартовая точка лабиринта, логика перемещения
	"""
	default_Y_axis = 0#9
	default_X_axis = 0#7
	default_selected_direction = int()

	def __init__(self, **kwargs):
		self.Y_axis = kwargs.get('Y_axis', self.default_Y_axis)
		self.X_axis = kwargs.get('X_axis', self.default_X_axis)
		self.map = Game_map().labyrinth()
		self.selected_direction = kwargs.get('selected_direction', self.default_selected_direction)

	def control(self):
		"""
		Ввод направления движения в лабиринте
		"""
		print('Выберите направление: ')
		side_choice = input().strip()
		side = ['влево', 'вправо', 'вверх', 'вниз']
		if side_choice in side and side.index(side_choice) != None:
			self.selected_direction = side.index(side_choice)
			return self.selected_direction
		else:
			print('=' * 50)
			print('Ошибка ввода, повторите попытку (влево, вправо, вверх, вниз): ')
			self.control()


	def choise_in_step(self, axis=False):
		"""
		Логика результат выбора направления
		"""
		if axis:
			self.Y_axis, self.X_axis = axis

		position_options = Game_map().map_point_decode(self.map[self.Y_axis][self.X_axis])

		self.control()

		for key, value in position_options[self.selected_direction].items():
			if key == 'la_fin':
				print('=' * 50)
				print(value)
				GameSave().clear_save()
				quit()
			if key:
				print('=' * 50)
				print(value)

				if self.selected_direction == 0:
					GameSave().save(self.Y_axis, self.X_axis)
					self.X_axis -= 1
					self.choise_in_step()
				if self.selected_direction == 1:
					GameSave().save(self.Y_axis, self.X_axis)
					self.X_axis += 1
					self.choise_in_step()
				if self.selected_direction == 2:
					GameSave().save(self.Y_axis, self.X_axis)
					self.Y_axis -= 1
					self.choise_in_step()
				if self.selected_direction == 3:
					GameSave().save(self.Y_axis, self.X_axis)
					self.Y_axis += 1
					self.choise_in_step()
			else:
				print('=' * 50)
				print(value)
				self.Y_axis, self.X_axis = GameSave().load()
				self.choise_in_step()





class GameSave:
	"""
	Лог последнего верного хода
	"""
	def save(self, Y_axis, X_axis):
		"""
		Дамп кортежа оси х, у последней точки с верно выбранным направление
		"""
		with open('save.json', 'w') as file:
			json.dump((Y_axis, X_axis), file, indent=4)

	def load(self, recursive_input=None):
		"""
		Загрузка последнего сохранения с верно выбранным направление
		"""
		if recursive_input == None:
			str_intput = input("Загрузить сохраненную игру с последнего удачного хода?  Да/Нет: ").strip().lower()
		if str_intput == 'да' or recursive_input == "да":
			with open('save.json') as file:
				Y_axis, X_axis = json.load(file)
				return Y_axis, X_axis
		elif str_intput == 'нет' or recursive_input == "нет":
			quit()

		else:
			print("=" * 50)
			print('неверный ввод, повторите команду (Да/Нет): ')
			self.load(input().strip().lower())



	def clear_save(self):
		"""
		Очистка сохранения
		"""
		with open('save.json', 'w'):
			Y_axis, X_axis = 0, 0
			return Y_axis, X_axis

	def start_load(self):
		"""
		Логика проверки сейва при первичной загрузке
		"""
		try:
			with open('save.json') as file:
				if file:
					Y_axis, X_axis = json.load(file)
					inpt = input('Начать игру с последнего сохранения ? (Да/Нет): ').strip().lower()
					if inpt == "да":
						return Y_axis, X_axis
					elif inpt == 'нет':
						return False
					else:
						print("=" * 50)
						self.start_load()
				else:
					return False
		except Exception:
			pass



class Game_map(Action):
	"""
	Представление игрового поля типа "лабиринт"
	"""
	default_field = ()
	default_false_way = Action().false_way()
	default_true_way = Action().true_way()
	default_wall = Action().wall()
	default_backward = Action().backward()
	default_la_fin = Action().la_fin()

	def __init__(self, **kwargs):
		self.field = kwargs.get('field', self.default_field)
		self.false_way = kwargs.get('false_way', self.default_false_way)
		self.true_way = kwargs.get('true_way', self.default_true_way)
		self.wall = kwargs.get('wall', self.default_wall)
		self.backward = kwargs.get('backward', self.default_backward)
		self.la_fin = kwargs.get('la_fin', self.default_la_fin)

	def labyrinth(self, ):
		"""
		Загрузка численного представления игрового поля
		"""
		with open('map.json') as file:
			self.field = json.load(file)
		return self.field

	def map_point_decode(self, map_point):
		"""
		Предание формального значения игровому полю (свойств выбранных направлений)
		"""
		dic = {0: self.false_way, 1: self.true_way, 2: self.backward, 3: self.wall, 4: self.la_fin}
		return [dic[x] for x in map_point]


def main():
	Game_map = GamePlay()
	Game_map.choise_in_step(GameSave().start_load())


if __name__ == "__main__":
	main()
