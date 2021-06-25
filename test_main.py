from main import *
import pytest

# def test_always_passes():
#     assert True

# def test_always_fails():
#     assert False



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
    assert find_organisation_info('client') == \
    {'name': 'client', 'config': {'has_fixed_membership_fee': False, 'fixed_membership_fee_amount': 0}, 'parent': None}

################# CHECK FIXED FEE #################

