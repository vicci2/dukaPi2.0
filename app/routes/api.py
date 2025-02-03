# Here we explore the useful capabilites of of Fast API (Decoupling):
from fastapi import APIRouter
from .company import company_router
from .subscription import subscription_router
from .tier import tier_router
from .user import users_router
from .products import product_router
from .inventory import inventory_router
from .auth_routes import auth_router
from .sales import sales_router
from .vendor import vendor_router
from .mpesa import daraja_router

router=APIRouter()

# router.include_router(company_router,prefix='/companies',tags=["Companies"])
# router.include_router(subscription_router,prefix='/subscriptions',tags=["Subscriptions"])
# router.include_router(tier_router,prefix='/tiers',tags=["Tiers"])
router.include_router(product_router,prefix='/products',tags=["STOCK"])
router.include_router(inventory_router,prefix='/inventory',tags=["INVENTORY"])
# router.include_router(sales_router,prefix='/sales',tags=["SALES"])
router.include_router(auth_router,prefix='/auth',tags=["Authentication"])
# router.include_router(users_router,prefix='/users',tags=["Users"])
# router.include_router(vendor_router,prefix='/vendors',tags=["Vendors"])
# router.include_router(daraja_router,prefix='/daraja',tags=["Daraja"])