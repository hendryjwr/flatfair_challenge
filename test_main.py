from main import *
import pytest

with open('testOrgFixedClient.json') as f:
    fixed_client_config = json.load(f)

print(fixed_client_config)

# def test_always_passes():
#     assert True

# def test_always_fails():
#     assert False

# print(org_config)

################# VALIDATION CHECKS #################

def test_validation_below_min_weekly():
    with pytest.raises(Exception): 
        validation(2499, 'week') 

def test_validation_below_min_monthly():
    with pytest.raises(Exception): 
        validation(10999, 'month') 

def test_validation_above_min_weekly():
    with pytest.raises(Exception): 
        validation(200001, 'week') 

def test_validation_above_min_monthly():
    with pytest.raises(Exception): 
        validation(866001, 'month') 

def test_validation_acceptable_weekly():
   assert validation(100000, 'week') == None
    

def test_validation_acceptable_monthly():
    assert validation(500000, 'month') == None



############# FIND ORG INFO FROM CONFIG #############

def test_find_organisation_info_branch():
    assert find_organisation_info(BRANCH_E['parent']) == \
    {'name': 'area_b', 'config': {'has_fixed_membership_fee': False, 'fixed_membership_fee_amount': 0}, 'parent': 'division_a'}

def test_find_organisation_info_area():
    assert find_organisation_info('division_a') == \
    {'name': 'division_a', 'config': {'has_fixed_membership_fee': False, 'fixed_membership_fee_amount': 0}, 'parent': 'client'}

def test_find_organisation_info_division():
    assert find_organisation_info(org_config[1]['parent']) == \
    {'name': 'client', 'config': {'has_fixed_membership_fee': False, 'fixed_membership_fee_amount': 0}, 'parent': None}



################# CHECK FIXED FEE #################

def test_fixed_fee_config_is_none():
    # If config is None then we should look for the config of the parent node if it exists
    # branch_a has no config, we should then find the fixed membership fee from area_a
    branch_a = OrganisationUnit(org_config[7])
    assert check_for_fixed_fee(branch_a) == 45000

def test_fixed_fee_fixed_membership_fee_true():
    # If "has_fixed_membership_fee" is True then we should return the fixed membership fee
    branch_k = OrganisationUnit(org_config[17])
    assert check_for_fixed_fee(branch_k) == 25000

def test_fixed_fee_fixed_membership_fee_false():
    # If "has_fixed_membership_fee" is False then we should find a parent with a fixed fee
    branch_i = OrganisationUnit(org_config[15])
    assert check_for_fixed_fee(branch_i) == 45000

def test_fixed_fee_no_parent():
    # the top of the tree has no parent and should return None
    client = OrganisationUnit(org_config[0])
    assert check_for_fixed_fee(client) == None



############ CALCULATE MEMBERSHIP FEE BRANCH_E ############
##### USING BRANCH_E LEADS TO NO FIXED_MEMBERSHIP_FEE #####

def test_membership_fee_monthly_equals_weekly():
    # Should be possible to pass in either monthly or weekly amounts and convert to correct amount.
    assert calculate_membership_fee(25000, 'week', BRANCH_E) == calculate_membership_fee(108333, 'month', BRANCH_E)

def test_minimum_rent_amount_weekly():
    # Any weekly rent at 12000 or below should return 14400
    assert calculate_membership_fee(11000, 'week', BRANCH_E) == 14400

def test_minimum_rent_amount_monthly():
    # Any monthly rent at 52000 or below should return 14400
    assert calculate_membership_fee(50000, 'month', BRANCH_E) == 14400

def test_correct_rent_amount_weekly():
    assert calculate_membership_fee(20000, 'week', BRANCH_E) == 24000

def test_correct_rent_amount_monthly():
    assert calculate_membership_fee(86667, 'month', BRANCH_E) == 24000



############ CALCULATE MEMBERSHIP FIXED FEE ############

def test_membership_fee_fixed_branch():
    branch_k = org_config[17]
    assert calculate_membership_fee(20000, 'week', branch_k) == 25000

def test_membership_fee_fixed_area():
    # branch_a leads to area_a with a fixed fee
    branch_a = org_config[7]
    assert calculate_membership_fee(20000, 'week', branch_a) == 45000

def test_membership_fee_fixed_division():
    # branch_p leads to area_d and then division_b with fixed fee
    branch_p = org_config[22]
    assert calculate_membership_fee(20000, 'week', branch_p) == 35000

def test_membership_fee_fixed_client():
    fixed_client = fixed_client_config[1]
    assert calculate_membership_fee(20000, 'week', fixed_client, organisation_config=fixed_client_config) == 50000