from abc import ABC, abstractmethod

from investing_algorithm_framework.core.exceptions import OperationalException
from investing_algorithm_framework.core.models import OrderSide, OrderType


class OrderValidator(ABC):

    def validate(self, order, portfolio):

        if OrderSide.BUY.equals(order.side):
            self.validate_buy_order(order, portfolio)
        else:
            self.validate_sell_order(order, portfolio)

        if OrderType.LIMIT.equals(order.type):
            self.validate_limit_order(order, portfolio)
        else:
            self.validate_market_order(order, portfolio)

        self._validate_order(order, portfolio)

    def validate_sell_order(self, order, portfolio):

        position = portfolio.get_position(order.get_target_symbol())
    
        if position is None:
            raise OperationalException(
                "Can't add sell order to non existing position"
            )

        if OrderType.LIMIT.equals(order.type):
            if position.amount < order.amount_target_symbol:
                raise OperationalException(
                    "Order amount is larger then amount of open position"
                )
        else:
            if position.amount < order.amount_target_symbol:
                raise OperationalException(
                    "Order amount is larger then amount of open position"
                )

        if not order.trading_symbol == portfolio.trading_symbol:
            raise OperationalException(
                f"Can't add sell order with target "
                f"symbol {order.target_symbol} to "
                f"portfolio with trading currency {portfolio.trading_symbol}"
            )

    @staticmethod
    def validate_buy_order(order, portfolio):

        if not order.get_trading_symbol() == portfolio.get_trading_symbol():
            raise OperationalException(
                f"Can't add buy order with trading "
                f"symbol {order.trading_symbol} to "
                f"portfolio with trading currency {portfolio.trading_symbol}"
            )

    @staticmethod
    def validate_limit_order(order, portfolio):
        total_price = order.get_amount_target_symbol() * order.get_price()
        unallocated = portfolio.get_unallocated()

        if unallocated.get_amount() < total_price:
            raise OperationalException(
                f"Order total: {total_price} {portfolio.trading_symbol}, is "
                f"larger then unallocated size: {unallocated.get_amount()} "
                f"{portfolio.trading_symbol} of the portfolio"
            )

    @staticmethod
    def validate_market_order(order, portfolio):

        if OrderSide.BUY.equals(order.side):

            if order.amount_trading_symbol is None:
                raise OperationalException(
                    f"Market order needs an amount specified in the trading "
                    f"symbol {order.trading_symbol}"
                )

            if order.amount_trading_symbol > portfolio.unallocated:
                raise OperationalException(
                    f"Market order amount {order.amount_trading_symbol} "
                    f"{portfolio.trading_symbol.upper()} is larger then "
                    f"unallocated {portfolio.unallocated} "
                    f"{portfolio.trading_symbol.upper()}"
                )
        else:
            position = portfolio.get_position(order.get_target_symbol())

            if position is None:
                raise OperationalException(
                    "Can't add market sell order to non existing position"
                )

            if order.amount_target_symbol > position.amount:
                raise OperationalException(
                    "Sell order amount larger then position size"
                )

    @abstractmethod
    def _validate_order(self, order, portfolio):
        pass
