from django.db import models


class Stock(models.Model):
    """ Биржа (например, OKX, MEXC). """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Symbol(models.Model):
    """ Универсальный торговый символ (например, BTC/USDT). """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SymbolOnStock(models.Model):
    """ Привязка символа к конкретной бирже с её внутренним именем. """

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="on_stocks")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="symbols")
    name = models.CharField(max_length=100)  # как символ выглядит на конкретной бирже

    class Meta:
        unique_together = ("symbol", "stock")

    def __str__(self):
        return f"{self.symbol.name} на {self.stock.name} ({self.name})"


class Agent(models.Model):
    """
    Агент — пользовательский объект, где вручную выбираем символы и биржи.
    После сохранения подтягиваются все соответствующие SymbolOnStock.
    """
    name = models.CharField(max_length=100, unique=True)

    # выбор нескольких символов и бирж
    symbols = models.ManyToManyField(Symbol, blank=True)
    stocks = models.ManyToManyField(Stock, blank=True)

    def __str__(self):
        return self.name
