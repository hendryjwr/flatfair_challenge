import json
from typing import Union

with open('testOrg.json') as f:
    org_config = json.load(f)

VAT = 1.2
MINIMUM_RENT_AMOUNT = 12000

OrganisationUnitConfig = dict[str, Union[str, int]]
OrganisationUnit = dict[str, Union[str, OrganisationUnitConfig, str]]

class OrganisationUnitConfig:
    def __init__(self, has_fixed_membership_fee: bool, fixed_membership_fee_amount: int) -> None:
        self.has_fixed_membership_fee = has_fixed_membership_fee
        self.fixed_membership_fee_amount = fixed_membership_fee_amount

class OrganisationUnit:
    """An individual unit within the digraph. E.g.: a branch, area, division or client."""
    
    def __init__(self, unit) -> None:
        self.name = unit['name']
        if unit['config'] is not None:
            self.config = OrganisationUnitConfig(unit['config']['has_fixed_membership_fee'], unit['config']['fixed_membership_fee_amount'])
        else:
            self.config = None
        self.parent = unit['parent']

BRANCH_E = org_config[11]

def calculate_membership_fee(rent_amount: int, rent_period: str, organisation_unit: OrganisationUnit = BRANCH_E, organisation_config=org_config) -> int:
    """
    Calculates membership fee. A default OrganisationUnit of BRANCH_E has been set.

    Input:
        rent_amount: Int in pence
        rent_period: String ['week', 'month']
        organisation_unit: OrganisationUnit 

    Output:
        membership fee: Int in pence
    """

    validation(rent_amount, rent_period)
    organisation_unit = OrganisationUnit(organisation_unit)

    # Handle all in weekly amounts
    if rent_period == 'month':
        rent_amount = round((rent_amount * 12)/52, 0)

    if rent_amount < MINIMUM_RENT_AMOUNT:
        rent_amount = round((MINIMUM_RENT_AMOUNT * VAT), 0)
    else:
        rent_amount = round((rent_amount * VAT), 0)

    # recursively search tree for fixed_membership_fee
    fixed_fee = check_for_fixed_fee(organisation_unit, organisation_config=organisation_config)

    if fixed_fee:
        return fixed_fee

    return rent_amount

def check_for_fixed_fee(organisation_unit: OrganisationUnit, organisation_config=org_config) -> int:
    if organisation_unit.config is None:
        return check_for_fixed_fee(OrganisationUnit(find_organisation_info(organisation_unit.parent, organisation_config)), organisation_config)
    elif organisation_unit.config.has_fixed_membership_fee:
        return organisation_unit.config.fixed_membership_fee_amount
    elif organisation_unit.parent is None:
        return None
    else:
        return check_for_fixed_fee(OrganisationUnit(find_organisation_info(organisation_unit.parent, organisation_config)), organisation_config)

def find_organisation_info(parent, organisation_config=org_config):
    """Finds parent's information from config"""
    for item in organisation_config:
        if item['name'] == parent:
            return item

def validation(rent_amount: int, rent_period: str) -> None:
    """Handles validation of rent_amount min and max"""
    if (rent_period == 'week' and rent_amount < 2500) or (rent_period == 'month' and rent_amount < 11000):
        raise Exception('Rent amount below minimum')
    if (rent_period == 'week' and rent_amount > 200000) or (rent_period == 'month' and rent_amount > 866000):
        raise Exception('Rent amount above maximum')


if __name__ == '__main__':
    print(int(calculate_membership_fee(280093, 'month', BRANCH_E)))