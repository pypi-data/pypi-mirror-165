from dataclasses import dataclass
from typing import List, Optional
from etsy_apiv3.models.ListingPropertyModel import ListingProperty
from etsy_apiv3.utils.APIV3 import EtsyAuth
from etsy_apiv3.utils.Response import Response
from etsy_apiv3.models.ListingModel import Listing, Inventory

@dataclass
class ListingResource:
    
    auth: EtsyAuth
    
    def get_listing(self, listing_id: int, includes: str = "") -> Listing:
        """
        Retrieves a listing record by listing ID.

        Args:
            listing_id (int): Listing Id
            includes (str, optional): An enumerated string that attaches a valid association. Acceptable inputs are 'Shipping', 'Shop', 'Images', 'User', 'Translations' and 'Inventory'. Defaults to "".

        Returns:
            Listing: A Single Listing Object
        """
        endpoint = f"listings/{listing_id}"
        json = self.auth.request(endpoint, params={"includes":includes})
        return Listing(**json)

    def find_all_active_listings(self, limit=25, offset=0, keywords="", sort_on="created", sort_order="desc", min_price=None, max_price=None, taxonomy_id=None, shop_location="US"):
        """
        Find All Active Listings By Keywords, Min price, Max Price Or Shop Location

        Args:
            limit (int, optional): Result Limit. Defaults to 25, Max 100.
            offset (int, optional): Result Offset. Defaults to 0.
            keywords (str, optional): Keywords For Active Listings. Defaults to "".
            sort_on (str, optional): Sort By Result. Defaults to "created".
            sort_order (str, optional): Sort By Order. Defaults to "desc".
            min_price (_type_, optional): Min Price. Defaults to None.
            max_price (_type_, optional): Max Price. Defaults to None.
            taxonomy_id (_type_, optional): Taxonomy Id. Defaults to None.
            shop_location (_type_, optional): Shop Location. Defaults to US.

        Returns:
            Response[Listing]: List of Listing Items
        """
        
        endpoint = f"listings/active"
        params = {
            "limit":limit, "offset":offset, "keywords":keywords, "sort_on":sort_on,
            "sort_order":sort_order, "min_price":min_price, "max_price":max_price,
            "taxonomy_id":taxonomy_id, "shop_location":shop_location
        }
        
        json = self.auth.request(endpoint, params=params)

        return Response[Listing](**json)
    
    
    def find_all_active_listings_by_shop(self, shop_id: int, limit: int = 25, sort_on: str = "created", sort_order: str = "desc", offset: int = 0, keywords: str = ""):
        endpoint = f"shops/{shop_id}/listings/active"
        
        params = {"limit": limit, "sort_on": sort_on, "sort_order": sort_order,
                  "offset": offset, "keywords": keywords
        }
        
        response = self.auth.request(endpoint, params=params)
        return Response[Listing](**response)
        
    def get_listings_by_receipt_id(self, shop_id: int, receipt_id: int, limit: int = 25, offset: int = 0) -> Response[Listing]:
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}/listings"
        params = {"limit": limit, "offset": offset}
        
        response = self.auth.request(endpoint, params=params)
        return Response[Listing](**response)
    
    def get_listing_properties(self, shop_id: int, listing_id: int):
        endpoint = f"shops/{shop_id}/listings/{listing_id}/properties"
        
        response = self.auth.request(endpoint)
        return Response[ListingProperty](**response)
    
    def get_listing_property(self, listing_id: int, property_id: int):
        endpoint = f"listings/{listing_id}/properties/{property_id}"
        
        response = self.auth.request(endpoint)
        return ListingProperty(**response)
    
    def get_listing_inventory(self, listing_id: int):
        endpoint = f"listings/{listing_id}/inventory"
        response = self.auth.request(endpoint)
        return Inventory(**response)
    
    def update_listing(self, shop_id: int, listing_id: int, **kwargs):
        endpoint = f"shops/{shop_id}/listings/{listing_id}"
        response = self.auth.request(endpoint, "PUT", data=kwargs)
        return Listing(**response)
    
    def update_listing_inventory(self, listing_id: int, products: List[dict], price_on_property: Optional[List[int]] = None, quantity_on_property: Optional[List[int]] = None, sku_on_property: Optional[List[int]] = None):
        
        data = {
            "products":products
        }

        if price_on_property is not None:
            data["price_on_property"] = price_on_property
        
        if quantity_on_property is not None:
            data["quantity_on_property"] = quantity_on_property
        
        if sku_on_property is not None:
            data["sku_on_property"] = sku_on_property
            
        endpoint = f"listings/{listing_id}/inventory"
        response = self.auth.request(endpoint, "PUT", json=data)
        return Inventory(**response)

    
    def get_listings_by_listing_ids(self, listing_ids: List[int], includes: str = ""):
        params = {
            "listing_ids":",".join(list(map(str, listing_ids))),
            "includes":includes
        }
        endpoint = "listings/batch"
        
        response = self.auth.request(endpoint, params=params)
        return Response[Listing](**response)