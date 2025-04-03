# time format helper

 @staticmethod
    def str_time_to_ms(value: str) -> int:
        """
        Для преобразования времени формата чч:мм в микросекунды
        :param value: строковое значение формата "чч:мм"
        :return: int значение в мс
        """
        return (int(value.partition(":")[0]) * 60 + int(value.partition(":")[2])) * 60 * 1000

    @staticmethod
    def str_time_to_minutes(value: str) -> int:
        """
        Для преобразования времени формата чч:мм в минуты
        :param value: строковое значение формата "чч:мм"
        :return: int значение в мин
        """
        return int(value.partition(":")[0]) * 60 + int(value.partition(":")[2])
