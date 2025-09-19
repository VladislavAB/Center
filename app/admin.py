from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
import json
from pathlib import Path

from .models import Stock, Symbol, SymbolOnStock, Agent


# ---------------- Stock ----------------
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ---------------- Symbol ----------------
@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    # подключаем кастомный шаблон для кнопки
    change_list_template = "admin/app/symbol/change_list.html"  # замените your_app на имя приложения

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("load-symbols/", self.admin_site.admin_view(self.load_symbols), name="load_symbols"),
        ]
        return custom_urls + urls

    def load_symbols(self, request):
        """Загрузка symbols.json с удалением старых объектов"""
        file_path = Path("symbols.json")  # JSON в корне проекта
        if not file_path.exists():
            self.message_user(request, "Файл symbols.json не найден!", level=messages.ERROR)
            return redirect("..")

        # Очистка старых данных
        SymbolOnStock.objects.all().delete()
        Symbol.objects.all().delete()
        Stock.objects.all().delete()

        # Загружаем новый JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for symbol_name, info in data.items():
            symbol = Symbol.objects.create(name=symbol_name)
            for stock_name, stock_symbol in info["in_stock"].items():
                stock, _ = Stock.objects.get_or_create(name=stock_name)
                SymbolOnStock.objects.create(
                    symbol=symbol,
                    stock=stock,
                    name=stock_symbol
                )

        self.message_user(request, "✅ symbols.json успешно загружен!", level=messages.SUCCESS)
        return redirect("..")


# ---------------- SymbolOnStock ----------------
@admin.register(SymbolOnStock)
class SymbolOnStockAdmin(admin.ModelAdmin):
    list_display = ("name", "stock", "symbol")
    search_fields = ("symbol__name", "stock__name", "name")


# ---------------- Agent ----------------
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "get_symbols", "get_stocks", "get_symbol_on_stocks")
    filter_horizontal = ("symbols", "stocks")  # удобный выбор нескольких символов и бирж

    def get_symbols(self, obj):
        return ", ".join([s.name for s in obj.symbols.all()])
    get_symbols.short_description = "Symbols"

    def get_stocks(self, obj):
        return ", ".join([s.name for s in obj.stocks.all()])
    get_stocks.short_description = "Stocks"

    def get_symbol_on_stocks(self, obj):
        # Выбираем все SymbolOnStock для выбранных symbols и stocks
        sos = SymbolOnStock.objects.filter(
            symbol__in=obj.symbols.all(),
            stock__in=obj.stocks.all()
        )
        # Возвращаем имена символов именно так, как они на биржах (поле name)
        return ", ".join([s.name for s in sos])
    get_symbol_on_stocks.short_description = "Symbols on Stocks"

