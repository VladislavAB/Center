# views.py
from django.http import JsonResponse
from .models import Agent, SymbolOnStock


def agent_symbols_api(request, agent_name):
    """
    Получаем JSON с символами агента, их биржами и именами на биржах.
    """
    try:
        agent = Agent.objects.get(name=agent_name)
    except Agent.DoesNotExist:
        return JsonResponse({"error": "Agent not found"}, status=404)

    # Все SymbolOnStock, которые соответствуют выбранным symbols и stocks агента
    sos = SymbolOnStock.objects.filter(
        symbol__in=agent.symbols.all(),
        stock__in=agent.stocks.all()
    )

    result = {}

    for s in sos:
        symbol_name = s.symbol.name
        stock_name = s.stock.name
        if symbol_name not in result:
            result[symbol_name] = {"in_stock": {}}
        result[symbol_name]["in_stock"][stock_name] = s.name  # имя на бирже

    return JsonResponse(result)
