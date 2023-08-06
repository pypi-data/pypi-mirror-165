

class AssetsClassifier:
    def __init__(self):
        self.assets = {
            "cash": ["CashAndCashEquivalentsAtCarryingValue"],
            "total_current_assets": ["AssetsCurrent"],
            "property_plant_and_equipment": [
                "PropertyPlantAndEquipmentNet",
                "PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization",
            ],
            "total_assets": ["Assets"],
        }

    def _assets(self):
        return self.assets

    def search_in_assets(self, tag):
        for line_item, tags in self._assets().items():
            if tag in tags:
                return line_item


class LiabilitiesClassifier:
    def __init__(self):
        self.liabilities = {
            "total_current_liabilities": ["LiabilitiesCurrent"],
            "long_term_debt": ["LongTermDebtNoncurrent"],
            "total_liabilities": ["Liabilities"],
        }

    def _liabilities(self):
        return self.liabilities

    def search_in_liabilities(self, tag):
        for line_item, tags in self._liabilities().items():
            if tag in tags:
                return line_item


class StockholdersEquityClassifier:
    def __init__(self):
        self.stockholders_equity = {"total_stockholders_equity": ["StockholdersEquity"]}

    def _stockholders_equity(self):
        return self.stockholders_equity

    def search_in_stockholders_equity(self, tag):
        for line_item, tags in self._stockholders_equity().items():
            if tag in tags:
                return line_item


def assets_classifier(tag):
    return AssetsClassifier().search_in_assets(tag)


def liabilities_classifier(tag):
    return LiabilitiesClassifier().search_in_liabilities(tag)


def stockholders_equity_classifier(tag):
    return StockholdersEquityClassifier().search_in_stockholders_equity(tag)


class BalanceSheetClassifier:
    def __init__(self):
        self.statement = "balance_sheet"

    def search_in_balance_sheet(self, tag):
        if type(assets_classifier(tag)) is not None:
            line_item = assets_classifier(tag)

        elif type(liabilities_classifier(tag)) is not None:
            line_item = liabilities_classifier(tag)

        elif type(stockholders_equity_classifier(tag)) is not None:
            line_item = stockholders_equity_classifier(tag)

        return line_item, self.statement


class IncomeStatementClassifier:
    def __init__(self):
        self.statement = "income_statement"


def classifier(tag):
    if type(BalanceSheetClassifier().search_in_balance_sheet(tag)) is not None:
        return BalanceSheetClassifier().search_in_balance_sheet(tag)

    # elif type(IncomeStatementClassifier().search_in_income_statement(tag)) is not None:
    #     return IncomeStatementClassifier().search_in_income_statement(tag)

    # elif type(CashFlowStatementClassifier().search_in_cash_flow_statement(tag)) is not None:
    #     return CashFlowStatementClassifier().search_in_cash_flow_statement(tag)
