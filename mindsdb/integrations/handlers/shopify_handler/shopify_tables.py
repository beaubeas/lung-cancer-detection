import shopify
import pandas as pd

from typing import Text, List, Dict

from mindsdb.integrations.libs.api_handler import APITable
from mindsdb.integrations.utilities.sql_utils import extract_comparison_conditions

from mindsdb_sql.parser import ast

from mindsdb.utilities import log


def filter_df(df, conditions):
    for condition in conditions:
        column = condition[1]
        operator = '==' if condition[0] == '=' else condition[0]
        value = f"'{condition[2]}'" if type(condition[2]) == str else condition[2]

        query = f"{column} {operator} {value}"
        df.query(query, inplace=True)

    return df


class ProductsTable(APITable):
    """The Shopify Products Table implementation"""

    def select(self, query: ast.Select) -> pd.DataFrame:
        """Pulls data from the Shopify "GET /products" API endpoint.

        Parameters
        ----------
        query : ast.Select
           Given SQL SELECT query

        Returns
        -------
        pd.DataFrame
            Shopify Products matching the query

        Raises
        ------
        ValueError
            If the query contains an unsupported condition
        """

        # SELECT
        selected_columns = []
        for target in query.targets:
            if isinstance(target, ast.Star):
                selected_columns = self.get_columns()
                break
            elif isinstance(target, ast.Identifier):
                selected_columns.append(target.parts[-1])
            else:
                raise ValueError(f"Unknown query target {type(target)}")

        # WHERE
        conditions = extract_comparison_conditions(query.where)

        # ORDER BY
        order_by_conditions = {}
        if query.order_by and len(query.order_by) > 0:
            order_by_conditions["columns"] = []
            order_by_conditions["ascending"] = []

            for an_order in query.order_by:
                if an_order.field.parts[0] == "products":
                    if an_order.field.parts[1] in self.get_columns():
                        order_by_conditions["columns"].append(an_order.field.parts[1])

                        if an_order.direction == "ASC":
                            order_by_conditions["ascending"].append(True)
                        else:
                            order_by_conditions["ascending"].append(False)
                    else:
                        raise ValueError(
                            f"Order by unknown column {an_order.field.parts[1]}"
                        )

        # LIMIT
        if query.limit:
            total_results = query.limit.value
        else:
            total_results = 20

        products_df = pd.json_normalize(self.get_products(limit=total_results))

        if len(products_df) == 0:
            products_df = pd.DataFrame([], columns=selected_columns)
        else:
            products_df = products_df[selected_columns]

            if len(order_by_conditions.get("columns", [])) > 0:
                products_df = products_df.sort_values(
                    by=order_by_conditions["columns"],
                    ascending=order_by_conditions["ascending"],
                )

        return products_df

    def get_columns(self) -> List[Text]:
        return pd.json_normalize(self.get_products(limit=1)).columns.tolist()

    def get_products(self, **kwargs) -> List[Dict]:
        api_session = self.handler.connect()
        shopify.ShopifyResource.activate_session(api_session)
        products = shopify.Product.find(**kwargs)
        return [product.to_dict() for product in products]